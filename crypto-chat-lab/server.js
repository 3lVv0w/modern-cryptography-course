import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import path from 'path';
import os from 'os';
import net from 'net';
import { fileURLToPath } from 'url';
import { Aedes } from 'aedes';
import { WebSocketServer, createWebSocketStream } from 'ws';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.set('trust proxy', 1); // Trust reverse proxy / ngrok headers
app.use(cors({
  origin: "*",
  methods: ["GET", "POST", "OPTIONS"]
}));
app.use(express.json());

const httpServer = createServer(app);

// Socket.IO Server with WSS and Polling support
const io = new Server(httpServer, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  },
  transports: ['websocket', 'polling']
});

// Initialize Embedded Aedes MQTT Broker
const aedes = await Aedes.createBroker();

// MQTT over WebSocket Server (Listens on path /mqtt)
const wssMqtt = new WebSocketServer({ noServer: true });
wssMqtt.on('connection', (ws) => {
  const stream = createWebSocketStream(ws);
  aedes.handle(stream);
});

// Intercept HTTP upgrade requests: Route /mqtt to MQTT WebSocket server
httpServer.on('upgrade', (request, socket, head) => {
  try {
    const url = new URL(request.url, `http://${request.headers.host || 'localhost'}`);
    if (url.pathname === '/mqtt' || url.pathname === '/mqtt/') {
      wssMqtt.handleUpgrade(request, socket, head, (ws) => {
        wssMqtt.emit('connection', ws, request);
      });
    }
    // Note: socket.io handles its own upgrade requests on /socket.io/
  } catch (err) {
    socket.destroy();
  }
});

// Start Native MQTT TCP Server on port 1883
const MQTT_PORT = Number(process.env.MQTT_PORT || 1883);
const mqttTcpServer = net.createServer(aedes.handle);
mqttTcpServer.on('error', (err) => {
  console.warn(`[MQTT TCP WARNING] Port ${MQTT_PORT} unavailable: ${err.message}. (MQTT over WebSockets on /mqtt is active!)`);
});
mqttTcpServer.listen(MQTT_PORT, '0.0.0.0', () => {
  console.log(`📡 MQTT TCP Broker listening on 0.0.0.0:${MQTT_PORT}`);
});

// Helper: Inspect local IPv4 network interfaces
function getNetworkAddresses() {
  const interfaces = os.networkInterfaces();
  const addresses = [];
  for (const name of Object.keys(interfaces)) {
    for (const net of interfaces[name]) {
      if ((net.family === 'IPv4' || net.family === 4) && !net.internal) {
        addresses.push({ iface: name, address: net.address });
      }
    }
  }
  return addresses;
}

// Helper: Query local ngrok API to auto-detect active public tunnel
async function getNgrokUrl() {
  if (process.env.NGROK_URL) return process.env.NGROK_URL;
  if (process.env.PUBLIC_URL) return process.env.PUBLIC_URL;
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 800);
    const res = await fetch('http://127.0.0.1:4040/api/tunnels', { signal: controller.signal });
    clearTimeout(timeout);
    if (res.ok) {
      const data = await res.json();
      if (data && data.tunnels && data.tunnels.length > 0) {
        const httpsTunnel = data.tunnels.find(t => t.proto === 'https') || data.tunnels[0];
        return httpsTunnel.public_url;
      }
    }
  } catch (e) {
    // ngrok is not running locally, return null
  }
  return null;
}

// State Store
const connectedUsers = new Map(); // socket.id -> { username, role }
const messageLogs = []; // Global wiretap log for instructor
let activeMitmIntercept = false;
const interceptQueue = []; // Pending messages waiting for instructor approval
const publicDirectory = {}; // username -> { N, e }

// API: Network Discovery for Participants (LAN, ngrok, WSS & MQTT details)
app.get('/api/network-info', async (req, res) => {
  const addresses = getNetworkAddresses();
  const port = Number(process.env.PORT || 3005);
  const ngrokUrl = await getNgrokUrl();
  
  res.json({
    port: port,
    addresses: addresses.map(a => a.address),
    urls: addresses.map(a => `http://${a.address}:${port}`),
    primaryUrl: ngrokUrl || (addresses.length > 0 ? `http://${addresses[0].address}:${port}` : `http://localhost:${port}`),
    ngrokUrl: ngrokUrl,
    hasNgrok: !!ngrokUrl,
    wssUrl: ngrokUrl ? ngrokUrl.replace('https://', 'wss://') : null,
    mqttTcpPort: MQTT_PORT,
    mqttWsPath: '/mqtt',
    connectedUsersCount: connectedUsers.size,
    publicDirectory
  });
});

// Aedes MQTT Event: Handle Inbound Messages from external MQTT clients
aedes.on('publish', (packet, client) => {
  // Only process if published by an external client (not internal server bridge)
  if (client && packet.topic && packet.topic.startsWith('crypto/')) {
    try {
      const payloadStr = packet.payload.toString();
      let parsed;
      try {
        parsed = JSON.parse(payloadStr);
      } catch {
        parsed = {
          ciphertext: payloadStr,
          sender: client.id || 'MQTT_Client',
          cipherType: 'MQTT_Raw',
          key: ''
        };
      }

      const isBroadcast = packet.topic === 'crypto/classroom/broadcast' || 
                          packet.topic === 'crypto/broadcast' || 
                          parsed.recipient === 'Classroom Broadcast';

      const messageItem = {
        id: 'MQTT-' + Math.random().toString(36).substring(2, 9).toUpperCase(),
        sender: parsed.sender || client.id || 'MQTT_Node',
        recipient: isBroadcast ? 'Classroom Broadcast' : (parsed.recipient || 'Classroom Broadcast'),
        ciphertext: parsed.ciphertext || payloadStr,
        cipherType: parsed.cipherType || 'MQTT_Raw',
        key: parsed.key || '',
        timestamp: new Date().toLocaleTimeString(),
        status: activeMitmIntercept ? 'INTERCEPTED' : 'DELIVERED',
        isTampered: false,
        isSpoofed: false,
        isBroadcast: isBroadcast,
        viaMqtt: true
      };

      messageLogs.push(messageItem);
      io.to('instructor_room').emit('new-wire-log', messageItem);

      if (activeMitmIntercept) {
        interceptQueue.push(messageItem);
        io.to('instructor_room').emit('queue-update', interceptQueue);
      } else {
        if (isBroadcast) {
          io.emit('receive-message', messageItem);
        } else {
          io.to(messageItem.recipient).emit('receive-message', messageItem);
          io.to(messageItem.sender).emit('receive-message', messageItem);
        }
      }
    } catch (err) {
      console.error('[MQTT INBOUND ERROR]', err);
    }
  }
});

// Helper: Bridge messages into MQTT topics
function publishToMqtt(messageItem) {
  try {
    const topic = messageItem.isBroadcast 
      ? 'crypto/classroom/broadcast' 
      : `crypto/direct/${messageItem.recipient}`;

    const payloadBuffer = Buffer.from(JSON.stringify(messageItem));

    // Publish to destination topic
    aedes.publish({
      topic,
      payload: payloadBuffer,
      qos: 0,
      retain: false
    });

    // Also publish to global wiretap stream for external sniffers
    aedes.publish({
      topic: 'crypto/wiretap',
      payload: payloadBuffer,
      qos: 0,
      retain: false
    });
  } catch (err) {
    console.error('[MQTT BRIDGE ERROR]', err);
  }
}

io.on('connection', (socket) => {
  console.log(`[SOCKET CONNECTED] ${socket.id} (Transport: ${socket.conn.transport.name})`);

  // Send current public key directory immediately
  socket.emit('public-directory-update', publicDirectory);

  // Register User / Role
  socket.on('register-user', ({ username, role, publicKey }) => {
    connectedUsers.set(socket.id, { username, role });
    socket.join(username); // Join personal room for 1-1 routing
    
    if (publicKey) {
      publicDirectory[username] = publicKey;
      io.emit('public-directory-update', publicDirectory);
    }

    if (role === 'instructor') {
      socket.join('instructor_room');
    }

    console.log(`[REGISTER] ${username} as ${role} (Socket: ${socket.id})`);
    
    // Broadcast active users and public keys to all connected clients
    io.emit('active-users-update', Array.from(connectedUsers.values()));
    io.emit('public-directory-update', publicDirectory);
    
    // Send existing wire logs to newly joined instructor
    if (role === 'instructor') {
      socket.emit('initial-wire-logs', { logs: messageLogs, activeMitmIntercept, queue: interceptQueue });
    }
  });

  // Dynamic Public Key Exchange
  socket.on('publish-public-key', ({ username, publicKey }) => {
    if (username && publicKey) {
      publicDirectory[username] = publicKey;
      io.emit('public-directory-update', publicDirectory);
      console.log(`[KEY DIRECTORY] Synchronized RSA Public Key for ${username}`);
    }
  });

  // Handle Message Send (Both 1-1 and Classroom Broadcast)
  socket.on('send-message', (msgPayload) => {
    const isBroadcast = msgPayload.recipient === 'Classroom Broadcast' || 
                        msgPayload.recipient === 'ALL' || 
                        msgPayload.isBroadcast === true;

    const messageItem = {
      id: 'MSG-' + Math.random().toString(36).substring(2, 9).toUpperCase(),
      sender: msgPayload.sender,
      recipient: isBroadcast ? 'Classroom Broadcast' : msgPayload.recipient,
      ciphertext: msgPayload.ciphertext,
      cipherType: msgPayload.cipherType || 'Caesar',
      key: msgPayload.key || '',
      timestamp: new Date().toLocaleTimeString(),
      status: activeMitmIntercept ? 'INTERCEPTED' : 'DELIVERED',
      isTampered: false,
      isSpoofed: false,
      isBroadcast: isBroadcast,
      rsaPublicKey: msgPayload.rsaPublicKey || null,
      plaintextSent: msgPayload.plaintextSent || ''
    };

    // Store in global wire log
    messageLogs.push(messageItem);

    // Broadcast wire log to instructor
    io.to('instructor_room').emit('new-wire-log', messageItem);

    // Cross-publish to MQTT broker
    publishToMqtt(messageItem);

    if (activeMitmIntercept) {
      // Hold in queue for instructor approval/tampering
      interceptQueue.push(messageItem);
      io.to('instructor_room').emit('queue-update', interceptQueue);
      console.log(`[MITM INTERCEPT] Held ${isBroadcast ? 'BROADCAST' : '1-1'} message ${messageItem.id} from ${messageItem.sender}`);
    } else {
      if (isBroadcast) {
        // Broadcast to ALL connected participants in the classroom!
        io.emit('receive-message', messageItem);
        console.log(`[BROADCAST DELIVERED] ${messageItem.id} from ${messageItem.sender} to Classroom`);
      } else {
        // Direct relay to recipient AND sender so both chat windows stay updated!
        io.to(msgPayload.recipient).emit('receive-message', messageItem);
        io.to(msgPayload.sender).emit('receive-message', messageItem);
        socket.emit('message-sent-ack', messageItem);
        console.log(`[1-1 DELIVERED] ${messageItem.id} from ${messageItem.sender} to ${msgPayload.recipient}`);
      }
    }
  });

  // Instructor Action: Impersonate / Spoof Message
  socket.on('mitm-impersonate', ({ spoofedSender, recipient, ciphertext, cipherType, key, isBroadcast }) => {
    const broadcastFlag = isBroadcast || recipient === 'Classroom Broadcast' || recipient === 'ALL';
    
    const spoofedItem = {
      id: 'SPOOF-' + Math.random().toString(36).substring(2, 9).toUpperCase(),
      sender: spoofedSender,
      recipient: broadcastFlag ? 'Classroom Broadcast' : recipient,
      ciphertext: ciphertext,
      cipherType: cipherType || 'Raw',
      key: key || '',
      timestamp: new Date().toLocaleTimeString(),
      status: 'SPOOFED',
      isTampered: false,
      isSpoofed: true,
      isBroadcast: broadcastFlag
    };

    messageLogs.push(spoofedItem);

    // Notify instructor UI
    io.to('instructor_room').emit('new-wire-log', spoofedItem);

    // Cross-publish spoofed packet to MQTT
    publishToMqtt(spoofedItem);

    if (broadcastFlag) {
      io.emit('receive-message', spoofedItem);
    } else {
      io.to(recipient).emit('receive-message', spoofedItem);
      io.to(spoofedSender).emit('receive-message', spoofedItem);
    }

    console.log(`[INSTRUCTOR IMPERSONATION] Spoofed message delivered as ${spoofedSender} to ${spoofedItem.recipient}`);
  });

  // Instructor Action: Toggle Active Intercept Mode
  socket.on('mitm-toggle-intercept', ({ enabled }) => {
    activeMitmIntercept = enabled;
    io.to('instructor_room').emit('intercept-mode-changed', { activeMitmIntercept });
    console.log(`[MITM MODE] Intercept active = ${enabled}`);
  });

  // Instructor Action: Approve or Tamper Message in Queue
  socket.on('mitm-process-queued-message', ({ messageId, action, tamperedCiphertext }) => {
    const idx = interceptQueue.findIndex(m => m.id === messageId);
    if (idx !== -1) {
      const msg = interceptQueue.splice(idx, 1)[0];
      io.to('instructor_room').emit('queue-update', interceptQueue);

      if (action === 'APPROVE') {
        msg.status = 'DELIVERED';
        publishToMqtt(msg);
        io.to('instructor_room').emit('new-wire-log', msg);
        if (msg.isBroadcast || msg.recipient === 'Classroom Broadcast') {
          io.emit('receive-message', msg);
        } else {
          io.to(msg.recipient).emit('receive-message', msg);
          io.to(msg.sender).emit('receive-message', msg);
        }
        console.log(`[MITM RELEASED] ${msg.id} delivered`);
      } else if (action === 'TAMPER') {
        msg.ciphertext = tamperedCiphertext || msg.ciphertext;
        msg.status = 'TAMPERED';
        msg.isTampered = true;
        publishToMqtt(msg);
        io.to('instructor_room').emit('new-wire-log', msg);
        if (msg.isBroadcast || msg.recipient === 'Classroom Broadcast') {
          io.emit('receive-message', msg);
        } else {
          io.to(msg.recipient).emit('receive-message', msg);
          io.to(msg.sender).emit('receive-message', msg);
        }
        console.log(`[MITM TAMPERED] ${msg.id} modified and released`);
      } else if (action === 'DROP') {
        msg.status = 'DROPPED';
        io.to('instructor_room').emit('new-wire-log', msg);
        console.log(`[MITM DROPPED] ${msg.id} destroyed by instructor`);
      }
    }
  });

  socket.on('disconnect', () => {
    const user = connectedUsers.get(socket.id);
    if (user) {
      console.log(`[DISCONNECT] ${user.username}`);
      connectedUsers.delete(socket.id);
      io.emit('active-users-update', Array.from(connectedUsers.values()));
    }
  });
});

// Serve production static assets if built
app.use(express.static(path.join(__dirname, 'dist')));

// Fallback to index.html for SPA routing
app.get('*', (req, res, next) => {
  if (req.path.startsWith('/api') || req.path.startsWith('/socket.io') || req.path.startsWith('/mqtt')) {
    return next();
  }
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

const PORT = Number(process.env.PORT || 3005);
const HOST = '0.0.0.0';

httpServer.listen(PORT, HOST, async () => {
  const addresses = getNetworkAddresses();
  const ngrokUrl = await getNgrokUrl();

  console.log(`\n=============================================================`);
  console.log(`🚀 CRYPTO CHAT LAB SERVER LISTENING ON 0.0.0.0:${PORT}`);
  console.log(`👉 Local:              http://localhost:${PORT}`);
  if (addresses.length > 0) {
    addresses.forEach(a => {
      console.log(`🌐 Classroom LAN (${a.iface}): http://${a.address}:${PORT}`);
    });
  }
  if (ngrokUrl) {
    console.log(`🚇 Public ngrok Tunnel: ${ngrokUrl} (WSS & HTTPS Active)`);
    console.log(`   WSS Endpoint:       ${ngrokUrl.replace('https://', 'wss://')}`);
  } else {
    console.log(`🚇 ngrok Tunnel:      Not active. Run "ngrok http ${PORT}" to open a public WSS tunnel!`);
  }
  console.log(`📡 MQTT Broker:        TCP port ${MQTT_PORT} & WebSockets at /mqtt`);
  console.log(`=============================================================\n`);
});
