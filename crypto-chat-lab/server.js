import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(express.json());

const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// State Store
const connectedUsers = new Map(); // socket.id -> { username, role }
const messageLogs = []; // Global wiretap log for instructor
let activeMitmIntercept = false;
const interceptQueue = []; // Pending messages waiting for instructor approval

io.on('connection', (socket) => {
  console.log(`[SOCKET CONNECTED] ${socket.id}`);

  // Register User / Role
  socket.on('register-user', ({ username, role }) => {
    connectedUsers.set(socket.id, { username, role });
    socket.join(username); // Join personal room for 1-1 routing
    if (role === 'instructor') {
      socket.join('instructor_room');
    }

    console.log(`[REGISTER] ${username} as ${role} (Socket: ${socket.id})`);
    
    // Broadcast active users
    io.emit('active-users-update', Array.from(connectedUsers.values()));
    
    // Send existing wire logs to newly joined instructor
    if (role === 'instructor') {
      socket.emit('initial-wire-logs', { logs: messageLogs, activeMitmIntercept, queue: interceptQueue });
    }
  });

  // Handle Student 1-1 Message Send
  socket.on('send-message', (msgPayload) => {
    const messageItem = {
      id: 'MSG-' + Math.random().toString(36).substring(2, 9).toUpperCase(),
      sender: msgPayload.sender,
      recipient: msgPayload.recipient,
      ciphertext: msgPayload.ciphertext,
      cipherType: msgPayload.cipherType || 'Caesar',
      key: msgPayload.key || '',
      timestamp: new Date().toLocaleTimeString(),
      status: activeMitmIntercept ? 'INTERCEPTED' : 'DELIVERED',
      isTampered: false,
      isSpoofed: false
    };

    // Store in global wire log
    messageLogs.push(messageItem);

    // Broadcast wire log to instructor
    io.to('instructor_room').emit('new-wire-log', messageItem);

    if (activeMitmIntercept) {
      // Hold in queue for instructor approval/tampering
      interceptQueue.push(messageItem);
      io.to('instructor_room').emit('queue-update', interceptQueue);
      console.log(`[MITM INTERCEPT] Held message ${messageItem.id} from ${messageItem.sender} to ${messageItem.recipient}`);
    } else {
      // Direct relay to recipient AND sender so both chat windows stay updated!
      io.to(msgPayload.recipient).emit('receive-message', messageItem);
      io.to(msgPayload.sender).emit('receive-message', messageItem);
      socket.emit('message-sent-ack', messageItem);
    }
  });

  // Instructor Action: Impersonate / Spoof Message
  socket.on('mitm-impersonate', ({ spoofedSender, recipient, ciphertext, cipherType, key }) => {
    const spoofedItem = {
      id: 'SPOOF-' + Math.random().toString(36).substring(2, 9).toUpperCase(),
      sender: spoofedSender,
      recipient: recipient,
      ciphertext: ciphertext,
      cipherType: cipherType || 'Raw',
      key: key || '',
      timestamp: new Date().toLocaleTimeString(),
      status: 'SPOOFED',
      isTampered: false,
      isSpoofed: true
    };

    messageLogs.push(spoofedItem);

    // Notify instructor UI
    io.to('instructor_room').emit('new-wire-log', spoofedItem);

    // Deliver to BOTH recipient and spoofedSender so Alice AND Bob see the spoofed transmission!
    io.to(recipient).emit('receive-message', spoofedItem);
    io.to(spoofedSender).emit('receive-message', spoofedItem);

    console.log(`[INSTRUCTOR IMPERSONATION] Spoofed message delivered to ${recipient} and ${spoofedSender}`);
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
        io.to(msg.recipient).emit('receive-message', msg);
        io.to(msg.sender).emit('receive-message', msg);
        console.log(`[MITM RELEASED] ${msg.id} delivered to ${msg.recipient} & ${msg.sender}`);
      } else if (action === 'TAMPER') {
        msg.ciphertext = tamperedCiphertext;
        msg.status = 'TAMPERED';
        msg.isTampered = true;
        io.to(msg.recipient).emit('receive-message', msg);
        io.to(msg.sender).emit('receive-message', msg);
        console.log(`[MITM TAMPERED] ${msg.id} modified and sent to ${msg.recipient} & ${msg.sender}`);
      } else if (action === 'DROP') {
        msg.status = 'DROPPED';
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

const PORT = process.env.PORT || 3001;
httpServer.listen(PORT, () => {
  console.log(`\n=============================================================`);
  console.log(`🚀 CRYPTO CHAT LAB BACKEND RUNNING ON http://localhost:${PORT}`);
  console.log(`=============================================================\n`);
});
