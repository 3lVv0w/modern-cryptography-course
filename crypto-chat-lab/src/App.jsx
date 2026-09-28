import React, { useState, useEffect, useRef } from 'react';
import { io } from 'socket.io-client';
import { 
  Lock, ShieldAlert, ShieldCheck, UserCheck, Eye, Terminal, 
  Send, AlertTriangle, Key, Cpu, Zap, Radio, CheckCircle2, 
  MessageSquare, Activity, Sparkles, Sliders, ChevronRight, User, 
  RefreshCw, Users, Globe, Copy, Check, Info, Share2, HelpCircle,
  Settings, Wifi, RadioTower, Layers, ExternalLink, X
} from 'lucide-react';
import { 
  caesarEncrypt, caesarDecrypt, vigenereEncrypt, vigenereDecrypt, 
  rot13, autoBreakCipher, generateRSAKeyPair, rsaEncrypt, rsaDecrypt, crackRSAModulus 
} from './utils/cryptoUtils.js';

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [userRole, setUserRole] = useState('student');
  const [selectedRecipient, setSelectedRecipient] = useState('Classroom Broadcast');
  const [customNameInput, setCustomNameInput] = useState('');
  
  // Server Connection & Tunneling State
  const defaultServer = localStorage.getItem('crypto_chat_server_url') || window.location.origin;
  const [serverUrl, setServerUrl] = useState(defaultServer);
  const [serverInputUrl, setServerInputUrl] = useState(defaultServer);
  const [isServerModalOpen, setIsServerModalOpen] = useState(false);
  const [isMqttModalOpen, setIsMqttModalOpen] = useState(false);
  const [socketConnected, setSocketConnected] = useState(false);

  // Network and Participant Directory State
  const [networkInfo, setNetworkInfo] = useState({ 
    primaryUrl: defaultServer, 
    urls: [],
    hasNgrok: false,
    ngrokUrl: null,
    wssUrl: null,
    mqttTcpPort: 1883,
    mqttWsPath: '/mqtt'
  });
  const [activeUsers, setActiveUsers] = useState([]);
  const [copiedServerUrl, setCopiedServerUrl] = useState(false);
  const [copiedNgrokUrl, setCopiedNgrokUrl] = useState(false);

  // Student Encryption State
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [cipherType, setCipherType] = useState('Caesar'); // 'Caesar', 'Vigenère', 'RSA', 'ROT13', 'Plaintext'
  const [cipherKey, setCipherKey] = useState('3');

  // RSA Asymmetric Key Directory
  const [myRsaKeys, setMyRsaKeys] = useState(null);
  const [publicDirectory, setPublicDirectory] = useState({}); // username -> publicKey { N, e }

  // Instructor State
  const [wireLogs, setWireLogs] = useState([]);
  const [activeMitmIntercept, setActiveMitmIntercept] = useState(false);
  const [interceptQueue, setInterceptQueue] = useState([]);
  const [selectedLogForDecrypt, setSelectedLogForDecrypt] = useState(null);
  const [autoDecryptResult, setAutoDecryptResult] = useState(null);

  // Impersonation Form State
  const [spoofSender, setSpoofSender] = useState('Alice');
  const [spoofRecipient, setSpoofRecipient] = useState('Classroom Broadcast');
  const [spoofText, setSpoofText] = useState('');
  const [spoofCipherType, setSpoofCipherType] = useState('Caesar');
  const [spoofKey, setSpoofKey] = useState('3');

  // Tamper Form State
  const [tamperInput, setTamperInput] = useState('');

  const chatBottomRef = useRef(null);
  const socketRef = useRef(null);

  // Fetch host network discovery details from Express
  const fetchNetworkInfo = (targetUrl) => {
    fetch(`${targetUrl}/api/network-info`)
      .then(res => res.json())
      .then(data => {
        if (data) {
          setNetworkInfo(data);
          if (data.publicDirectory) {
            setPublicDirectory(prev => ({ ...data.publicDirectory, ...prev }));
          }
        }
      })
      .catch(() => {
        // Fallback
        setNetworkInfo(prev => ({ ...prev, primaryUrl: targetUrl }));
      });
  };

  useEffect(() => {
    fetchNetworkInfo(serverUrl);
  }, [serverUrl]);

  // Initialize Default RSA Keys for Alice & Bob
  useEffect(() => {
    const aliceKeys = generateRSAKeyPair(true);
    const bobKeys = generateRSAKeyPair(true);
    setPublicDirectory(prev => ({
      Alice: aliceKeys.publicKey,
      Bob: bobKeys.publicKey,
      ...prev
    }));
  }, []);

  // Establish & Manage Socket.IO Connection (supports custom server, ngrok WSS, or local)
  useEffect(() => {
    console.log(`Connecting Socket.IO to: ${serverUrl}`);
    const socket = io(serverUrl, {
      transports: ['websocket', 'polling'],
      reconnectionAttempts: 10,
      timeout: 10000
    });
    socketRef.current = socket;

    socket.on('connect', () => {
      console.log('[SOCKET CONNECTED]', socket.id);
      setSocketConnected(true);
      if (currentUser) {
        socket.emit('register-user', {
          username: currentUser,
          role: userRole,
          publicKey: myRsaKeys ? myRsaKeys.publicKey : null
        });
      }
    });

    socket.on('disconnect', () => {
      console.log('[SOCKET DISCONNECTED]');
      setSocketConnected(false);
    });

    const handleNewMessage = (msg) => {
      setMessages((prev) => {
        if (prev.some((m) => m.id === msg.id)) return prev;
        return [...prev, msg];
      });
    };

    socket.on('receive-message', handleNewMessage);
    socket.on('message-sent-ack', handleNewMessage);

    socket.on('initial-wire-logs', ({ logs, activeMitmIntercept, queue }) => {
      setWireLogs(logs || []);
      setActiveMitmIntercept(!!activeMitmIntercept);
      setInterceptQueue(queue || []);
    });

    socket.on('new-wire-log', (logItem) => {
      setWireLogs((prev) => [logItem, ...prev]);
    });

    socket.on('intercept-mode-changed', ({ activeMitmIntercept }) => {
      setActiveMitmIntercept(activeMitmIntercept);
    });

    socket.on('queue-update', (queue) => {
      setInterceptQueue(queue || []);
    });

    socket.on('active-users-update', (users) => {
      setActiveUsers(users || []);
    });

    socket.on('public-directory-update', (directory) => {
      if (directory) {
        setPublicDirectory(prev => ({ ...prev, ...directory }));
      }
    });

    return () => {
      socket.disconnect();
    };
  }, [serverUrl]);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleApplyCustomServer = (e) => {
    e.preventDefault();
    let cleanUrl = serverInputUrl.trim().replace(/\/+$/, '');
    if (!cleanUrl) return;
    if (!cleanUrl.startsWith('http://') && !cleanUrl.startsWith('https://')) {
      cleanUrl = 'https://' + cleanUrl;
    }
    setServerUrl(cleanUrl);
    localStorage.setItem('crypto_chat_server_url', cleanUrl);
    setIsServerModalOpen(false);
  };

  const handleResetToOrigin = () => {
    setServerUrl(window.location.origin);
    setServerInputUrl(window.location.origin);
    localStorage.removeItem('crypto_chat_server_url');
    setIsServerModalOpen(false);
  };

  const handleLogin = (username, role) => {
    const cleanName = username.trim();
    if (!cleanName) return;

    setCurrentUser(cleanName);
    setUserRole(role);

    // Auto-generate RSA keypair for student if missing
    let currentKeys = myRsaKeys;
    if (role === 'student' && !currentKeys) {
      currentKeys = generateRSAKeyPair(true);
      setMyRsaKeys(currentKeys);
      setPublicDirectory(prev => ({
        ...prev,
        [cleanName]: currentKeys.publicKey
      }));
    }

    if (socketRef.current) {
      socketRef.current.emit('register-user', { 
        username: cleanName, 
        role, 
        publicKey: currentKeys ? currentKeys.publicKey : null 
      });
    }
  };

  const handleGenerateNewRsaKeys = () => {
    const keys = generateRSAKeyPair(true);
    setMyRsaKeys(keys);
    if (currentUser) {
      setPublicDirectory(prev => ({
        ...prev,
        [currentUser]: keys.publicKey
      }));
      // Broadcast new public key to all participants over Socket.IO
      if (socketRef.current) {
        socketRef.current.emit('publish-public-key', {
          username: currentUser,
          publicKey: keys.publicKey
        });
      }
    }
  };

  const copyServerLink = () => {
    const urlToCopy = networkInfo.primaryUrl || serverUrl;
    navigator.clipboard.writeText(urlToCopy).then(() => {
      setCopiedServerUrl(true);
      setTimeout(() => setCopiedServerUrl(false), 2500);
    }).catch(() => {
      alert(`Server URL: ${urlToCopy}`);
    });
  };

  const copyNgrokLink = () => {
    if (!networkInfo.ngrokUrl) return;
    navigator.clipboard.writeText(networkInfo.ngrokUrl).then(() => {
      setCopiedNgrokUrl(true);
      setTimeout(() => setCopiedNgrokUrl(false), 2500);
    }).catch(() => {
      alert(`ngrok Tunnel: ${networkInfo.ngrokUrl}`);
    });
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputText.trim() || !currentUser || !socketRef.current) return;

    const isBroadcast = selectedRecipient === 'Classroom Broadcast';

    if (isBroadcast && cipherType === 'RSA') {
      alert("⚠️ Asymmetric RSA is designed for 1-to-1 communication using an individual recipient's Public Key. For Classroom Group Broadcast, please choose a Symmetric Cipher (Caesar, Vigenère, ROT13) so all participants can decrypt using the shared key!");
      return;
    }

    let encryptedPayload = inputText;

    if (cipherType === 'Caesar') {
      encryptedPayload = caesarEncrypt(inputText, parseInt(cipherKey, 10) || 0);
    } else if (cipherType === 'Vigenère') {
      encryptedPayload = vigenereEncrypt(inputText, cipherKey);
    } else if (cipherType === 'ROT13') {
      encryptedPayload = rot13(inputText);
    } else if (cipherType === 'RSA') {
      const recipientPubKey = publicDirectory[selectedRecipient];
      if (!recipientPubKey) {
        alert(`Public Key for ${selectedRecipient} not found in RSA Directory! Wait for classmate to join or select another recipient.`);
        return;
      }
      try {
        encryptedPayload = rsaEncrypt(inputText, recipientPubKey);
      } catch (err) {
        alert(err.message);
        return;
      }
    }

    const payload = {
      sender: currentUser,
      recipient: selectedRecipient,
      isBroadcast: isBroadcast,
      ciphertext: encryptedPayload,
      cipherType: cipherType,
      key: cipherKey,
      rsaPublicKey: isBroadcast ? null : (publicDirectory[selectedRecipient] || null),
      plaintextSent: inputText
    };

    socketRef.current.emit('send-message', payload);
    setInputText('');
  };

  const handleInspectAndDecrypt = (logItem) => {
    setSelectedLogForDecrypt(logItem);

    if (logItem.ciphertext.startsWith('RSA-CIPHER:')) {
      const pubKey = logItem.rsaPublicKey || publicDirectory[logItem.recipient] || { N: '3FE5', e: '3' };
      const result = crackRSAModulus(pubKey.N, pubKey.e, logItem.ciphertext);
      setAutoDecryptResult(result);
    } else {
      const result = autoBreakCipher(logItem.ciphertext, logItem.cipherType, logItem.key);
      setAutoDecryptResult(result);
    }
  };

  const handleSpoofMessage = (e) => {
    e.preventDefault();
    if (!spoofText.trim() || !socketRef.current) return;

    const isBroadcast = spoofRecipient === 'Classroom Broadcast';

    let encryptedPayload = spoofText;
    if (spoofCipherType === 'Caesar') {
      encryptedPayload = caesarEncrypt(spoofText, parseInt(spoofKey, 10) || 0);
    } else if (spoofCipherType === 'Vigenère') {
      encryptedPayload = vigenereEncrypt(spoofText, spoofKey);
    } else if (spoofCipherType === 'ROT13') {
      encryptedPayload = rot13(spoofText);
    } else if (spoofCipherType === 'RSA') {
      const recipientPubKey = publicDirectory[spoofRecipient] || { N: '3FE5', e: '3' };
      encryptedPayload = rsaEncrypt(spoofText, recipientPubKey);
    }

    socketRef.current.emit('mitm-impersonate', {
      spoofedSender: spoofSender,
      recipient: spoofRecipient,
      ciphertext: encryptedPayload,
      cipherType: spoofCipherType,
      key: spoofKey,
      isBroadcast: isBroadcast
    });

    setSpoofText('');
  };

  const toggleMitmIntercept = () => {
    if (!socketRef.current) return;
    const nextState = !activeMitmIntercept;
    setActiveMitmIntercept(nextState);
    socketRef.current.emit('mitm-toggle-intercept', { enabled: nextState });
  };

  const handleProcessQueuedMessage = (messageId, action) => {
    if (!socketRef.current) return;
    socketRef.current.emit('mitm-process-queued-message', {
      messageId,
      action,
      tamperedCiphertext: tamperInput
    });
    setTamperInput('');
  };

  const getDecryptedTextForStudent = (msg) => {
    if (msg.sender === currentUser) return msg.plaintextSent || msg.ciphertext;
    if (msg.ciphertext.startsWith('RSA-CIPHER:')) {
      if (myRsaKeys) {
        return rsaDecrypt(msg.ciphertext, myRsaKeys.privateKey);
      }
      return '[RSA ASYMMETRIC ENCRYPTED PAYLOAD]';
    }
    if (msg.cipherType === 'Caesar') return caesarDecrypt(msg.ciphertext, parseInt(msg.key, 10) || 0);
    if (msg.cipherType === 'Vigenère') return vigenereDecrypt(msg.ciphertext, msg.key);
    if (msg.cipherType === 'ROT13') return rot13(msg.ciphertext);
    return msg.ciphertext;
  };

  // Build list of recipient choices for current user
  const knownPartners = ['Bob', 'Alice', 'Charlie'];
  const onlinePeerNames = activeUsers
    .map(u => u.username)
    .filter(name => name && name !== currentUser && name !== 'Instructor_Dr_Smith');
  
  const availableRecipients = Array.from(new Set([...onlinePeerNames, ...knownPartners.filter(p => p !== currentUser)]));

  // Filter messages for current chat view
  const currentChatMessages = messages.filter((msg) => {
    const isBroadcast = msg.recipient === 'Classroom Broadcast' || msg.isBroadcast;
    if (selectedRecipient === 'Classroom Broadcast') {
      return isBroadcast;
    }
    return (
      ((msg.sender === currentUser && msg.recipient === selectedRecipient) ||
       (msg.recipient === currentUser && msg.sender === selectedRecipient) ||
       (msg.isSpoofed && (msg.sender === currentUser || msg.recipient === selectedRecipient))) &&
      !isBroadcast
    );
  });

  // LANDING HERO & ROLE SELECTION SCREEN
  if (!currentUser) {
    return (
      <main className="overflow-x-hidden w-full max-w-full" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '36px 20px' }}>
        <div style={{ maxWidth: '1120px', margin: '0 auto', width: '100%' }}>
          
          <div style={{ textAlign: 'center', marginBottom: '32px' }}>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '6px 16px', background: 'rgba(6, 182, 212, 0.1)', border: '1px solid rgba(6, 182, 212, 0.3)', borderRadius: '30px', color: '#06B6D4', fontSize: '13px', fontWeight: '600', marginBottom: '16px' }}>
              <Sparkles size={14} /> UNIVERSITY LAB PLATFORM · CS-4XX MODERN CRYPTOGRAPHY
            </div>

            <h1 style={{ fontSize: 'clamp(2.1rem, 3.8vw, 3.6rem)', fontWeight: '800', lineHeight: '1.15', color: '#F8FAFC', maxWidth: '980px', margin: '0 auto 14px auto' }}>
              Encrypted Chat & <span style={{ color: '#F59E0B' }}>RSA Public-Key</span> Cryptanalysis Lab
            </h1>

            <p style={{ fontSize: '15px', color: '#94A3B8', maxWidth: '720px', margin: '0 auto', lineHeight: '1.6' }}>
              Perform live Symmetric & Asymmetric RSA encryption, execute Man-in-the-Middle wiretaps, simulate in-flight packet tampering, and connect participants worldwide via <strong>ngrok WSS Tunneling & MQTT</strong>.
            </p>

            {/* Protocol & Tunnel Status Bar */}
            <div style={{ marginTop: '20px', display: 'flex', flexWrap: 'wrap', justifyContent: 'center', alignItems: 'center', gap: '10px' }}>
              
              {/* Active ngrok Tunnel Badge if detected */}
              {networkInfo.hasNgrok ? (
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: 'rgba(16, 185, 129, 0.15)', padding: '8px 16px', borderRadius: '30px', border: '1px solid #10B981', color: '#10B981', fontSize: '12px', fontWeight: '600' }}>
                  <RadioTower size={15} /> 🚇 ngrok WSS Active: <span style={{ fontFamily: 'JetBrains Mono, monospace', color: '#F8FAFC' }}>{networkInfo.ngrokUrl}</span>
                  <button onClick={copyNgrokLink} style={{ background: 'transparent', border: 'none', color: '#10B981', cursor: 'pointer', display: 'inline-flex', alignItems: 'center' }}>
                    {copiedNgrokUrl ? <Check size={13} /> : <Copy size={13} />}
                  </button>
                </div>
              ) : (
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: 'rgba(15, 23, 42, 0.85)', padding: '8px 16px', borderRadius: '30px', border: '1px solid rgba(6, 182, 212, 0.35)', fontSize: '12px', color: '#94A3B8' }}>
                  <Globe size={15} color="#06B6D4" /> Server: <strong style={{ color: '#F8FAFC', fontFamily: 'JetBrains Mono, monospace' }}>{networkInfo.primaryUrl}</strong>
                  <button onClick={copyServerLink} style={{ background: 'transparent', border: 'none', color: '#06B6D4', cursor: 'pointer', display: 'inline-flex', alignItems: 'center' }}>
                    {copiedServerUrl ? <Check size={13} color="#10B981" /> : <Copy size={13} />}
                  </button>
                </div>
              )}

              {/* Protocol Badges */}
              <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'rgba(59, 130, 246, 0.12)', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '6px 12px', borderRadius: '20px', fontSize: '11px', color: '#60A5FA', fontWeight: '600' }}>
                <Wifi size={13} /> WSS WebSocket: Active
              </div>

              <div 
                onClick={() => setIsMqttModalOpen(true)}
                style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'rgba(245, 158, 11, 0.12)', border: '1px solid rgba(245, 158, 11, 0.3)', padding: '6px 12px', borderRadius: '20px', fontSize: '11px', color: '#F59E0B', fontWeight: '600', cursor: 'pointer' }}
                title="Click to view MQTT broker details"
              >
                <RadioTower size={13} /> MQTT: TCP 1883 & /mqtt
              </div>

              <button 
                onClick={() => setIsServerModalOpen(true)}
                style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.15)', color: '#CBD5E1', padding: '6px 12px', borderRadius: '20px', fontSize: '11px', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '5px' }}
              >
                <Settings size={13} /> Server Settings
              </button>
            </div>
          </div>

          {/* Quick Join Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(290px, 1fr))', gap: '20px', marginBottom: '24px' }}>
            
            <div className="glass-panel" style={{ padding: '26px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '240px' }}>
              <div>
                <div style={{ width: '42px', height: '42px', borderRadius: '12px', background: 'rgba(6, 182, 212, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '14px' }}>
                  <User size={20} color="#06B6D4" />
                </div>
                <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#F8FAFC', marginBottom: '4px' }}>Student Alice</h3>
                <p style={{ fontSize: '13px', color: '#94A3B8', lineHeight: '1.4' }}>Generate RSA Keypairs, broadcast encrypted messages, and communicate securely with classmates.</p>
              </div>
              <button className="btn-primary" style={{ width: '100%', justifyContent: 'center' }} onClick={() => handleLogin('Alice', 'student')}>
                Join as Alice <ChevronRight size={16} />
              </button>
            </div>

            <div className="glass-panel" style={{ padding: '26px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '240px' }}>
              <div>
                <div style={{ width: '42px', height: '42px', borderRadius: '12px', background: 'rgba(59, 130, 246, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '14px' }}>
                  <User size={20} color="#3B82F6" />
                </div>
                <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#F8FAFC', marginBottom: '4px' }}>Student Bob</h3>
                <p style={{ fontSize: '13px', color: '#94A3B8', lineHeight: '1.4' }}>Publish RSA Public Keys, participate in classroom group broadcasts, and decrypt incoming payloads.</p>
              </div>
              <button className="btn-primary" style={{ width: '100%', justifyContent: 'center', background: 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)' }} onClick={() => handleLogin('Bob', 'student')}>
                Join as Bob <ChevronRight size={16} />
              </button>
            </div>

            <div className="glass-panel glass-panel-accent" style={{ padding: '26px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '240px' }}>
              <div>
                <div style={{ width: '42px', height: '42px', borderRadius: '12px', background: 'rgba(245, 158, 11, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '14px' }}>
                  <Eye size={20} color="#F59E0B" />
                </div>
                <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#F59E0B', marginBottom: '4px' }}>Instructor MITM Suite</h3>
                <p style={{ fontSize: '13px', color: '#94A3B8', lineHeight: '1.4' }}>Wiretap packets, intercept in-flight messages, execute Fermat factorization, and spoof senders.</p>
              </div>
              <button className="btn-amber" style={{ width: '100%', justifyContent: 'center' }} onClick={() => handleLogin('Instructor_Dr_Smith', 'instructor')}>
                Launch MITM Dashboard <ChevronRight size={16} />
              </button>
            </div>

          </div>

          {/* Custom Participant Join Card (For Multi-Participant LAN / ngrok Classroom) */}
          <div className="glass-panel" style={{ padding: '24px 28px', borderRadius: '16px', border: '1px dashed rgba(6, 182, 212, 0.4)', background: 'rgba(15, 23, 42, 0.7)' }}>
            <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '18px' }}>
              <div style={{ flex: 1, minWidth: '280px' }}>
                <h3 style={{ fontSize: '17px', fontWeight: '700', color: '#F8FAFC', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Users size={18} color="#06B6D4" /> Join as Custom Participant
                </h3>
                <p style={{ fontSize: '13px', color: '#94A3B8', marginTop: '3px' }}>
                  Joining over LAN or ngrok WSS? Enter your real name or alias to connect to the centralized server.
                </p>
              </div>

              <div style={{ display: 'flex', gap: '10px', flex: 1, minWidth: '300px', maxWidth: '480px' }}>
                <input 
                  type="text" 
                  placeholder="Enter your student name (e.g. Charlie, Dave, Sarah)" 
                  value={customNameInput} 
                  onChange={(e) => setCustomNameInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && customNameInput.trim()) {
                      handleLogin(customNameInput.trim(), 'student');
                    }
                  }}
                  style={{ flex: 1, padding: '9px 14px', fontSize: '13px' }}
                />
                <button 
                  className="btn-primary" 
                  disabled={!customNameInput.trim()}
                  onClick={() => handleLogin(customNameInput.trim(), 'student')}
                  style={{ whiteSpace: 'nowrap', fontSize: '13px' }}
                >
                  Join Classroom <ChevronRight size={15} />
                </button>
              </div>
            </div>
          </div>

          {/* Server Settings Modal */}
          {isServerModalOpen && (
            <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(6px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999, padding: '16px' }}>
              <div className="glass-panel" style={{ maxWidth: '520px', width: '100%', padding: '28px', borderRadius: '16px', position: 'relative' }}>
                <button onClick={() => setIsServerModalOpen(false)} style={{ position: 'absolute', top: '16px', right: '16px', background: 'transparent', border: 'none', color: '#94A3B8', cursor: 'pointer' }}>
                  <X size={18} />
                </button>

                <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#F8FAFC', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Settings size={18} color="#06B6D4" /> Server & Tunnel Endpoint Configuration
                </h3>
                <p style={{ fontSize: '13px', color: '#94A3B8', lineHeight: '1.5', marginBottom: '18px' }}>
                  Connect your web client to an instructor's machine hosted via <strong>ngrok HTTPS/WSS</strong>, a custom domain, or a local LAN address.
                </p>

                <form onSubmit={handleApplyCustomServer}>
                  <label style={{ display: 'block', fontSize: '12px', fontWeight: '600', color: '#CBD5E1', marginBottom: '6px' }}>
                    Target Server Endpoint URL (HTTP/HTTPS/WSS):
                  </label>
                  <input 
                    type="text" 
                    value={serverInputUrl} 
                    onChange={(e) => setServerInputUrl(e.target.value)} 
                    placeholder="https://xxxx.ngrok-free.app or http://192.168.1.104:3005"
                    style={{ width: '100%', padding: '10px 14px', fontSize: '13px', marginBottom: '14px', fontFamily: 'JetBrains Mono, monospace' }}
                  />

                  <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                    <button type="button" onClick={handleResetToOrigin} style={{ background: 'transparent', border: '1px solid rgba(255,255,255,0.15)', color: '#94A3B8', padding: '8px 14px', borderRadius: '8px', fontSize: '12px', cursor: 'pointer' }}>
                      Reset to Default
                    </button>
                    <button type="submit" className="btn-primary" style={{ padding: '8px 16px', fontSize: '12px' }}>
                      Connect & Save
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}

          {/* MQTT Protocol Information Modal */}
          {isMqttModalOpen && (
            <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(6px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999, padding: '16px' }}>
              <div className="glass-panel" style={{ maxWidth: '600px', width: '100%', padding: '28px', borderRadius: '16px', position: 'relative' }}>
                <button onClick={() => setIsMqttModalOpen(false)} style={{ position: 'absolute', top: '16px', right: '16px', background: 'transparent', border: 'none', color: '#94A3B8', cursor: 'pointer' }}>
                  <X size={18} />
                </button>

                <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#F59E0B', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <RadioTower size={18} /> Embedded Aedes MQTT Broker Architecture
                </h3>
                <p style={{ fontSize: '13px', color: '#94A3B8', lineHeight: '1.5', marginBottom: '16px' }}>
                  This laboratory runs an embedded MQTT broker supporting both <strong>Native TCP (Port 1883)</strong> and <strong>WebSockets (/mqtt)</strong>. External Python, Mosquitto, and IoT clients can bridge directly into the chat!
                </p>

                <div style={{ background: '#0F172A', padding: '14px', borderRadius: '10px', border: '1px solid rgba(255,255,255,0.08)', marginBottom: '14px', fontSize: '12px', lineHeight: '1.6' }}>
                  <strong style={{ color: '#06B6D4' }}>Active MQTT Topics:</strong><br/>
                  • <code>crypto/classroom/broadcast</code> — Classroom Group Chat Broadcast<br/>
                  • <code>crypto/direct/{"{recipient}"}</code> — 1-1 Encrypted Peer Transmissions<br/>
                  • <code>crypto/wiretap</code> — Passive Packet Sniffing Stream (All Captured Frames)<br/>
                </div>

                <div style={{ background: '#070A12', padding: '12px', borderRadius: '8px', border: '1px solid rgba(245, 158, 11, 0.3)', fontSize: '11px', fontFamily: 'JetBrains Mono, monospace', color: '#F8FAFC' }}>
                  <span style={{ color: '#F59E0B' }}># Sniff packets from terminal with Mosquitto CLI:</span><br/>
                  mosquitto_sub -h localhost -p 1883 -t "crypto/#" -v
                </div>
              </div>
            </div>
          )}

        </div>
      </main>
    );
  }

  return (
    <main className="overflow-x-hidden w-full max-w-full" style={{ padding: '20px', maxWidth: '1440px', margin: '0 auto' }}>
      
      {/* Top Header Bar */}
      <div className="glass-panel" style={{ padding: '14px 22px', marginBottom: '18px', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Radio color={userRole === 'instructor' ? '#F59E0B' : '#06B6D4'} className="glow-cyan" size={18} />
          <div>
            <h2 style={{ fontSize: '17px', fontWeight: '700', color: '#F8FAFC', letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '8px' }}>
              Crypto Chat Lab <span style={{ fontSize: '11px', padding: '2px 8px', borderRadius: '12px', background: userRole === 'instructor' ? 'rgba(245, 158, 11, 0.2)' : 'rgba(6, 182, 212, 0.2)', color: userRole === 'instructor' ? '#F59E0B' : '#06B6D4', fontWeight: '600' }}>{userRole.toUpperCase()}</span>
            </h2>
          </div>
        </div>

        {/* Central Server, Protocol, and User Info Bar */}
        <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '10px' }}>
          
          {/* Server / ngrok Status */}
          <div style={{ background: '#0F172A', border: '1px solid rgba(255,255,255,0.08)', padding: '5px 12px', borderRadius: '30px', fontSize: '12px', color: '#94A3B8', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Globe size={13} color="#06B6D4" /> Server: 
            <span style={{ color: '#F8FAFC', fontFamily: 'JetBrains Mono, monospace' }}>
              {networkInfo.hasNgrok ? 'ngrok (WSS)' : (networkInfo.primaryUrl || serverUrl)}
            </span>
            <button 
              onClick={copyServerLink} 
              style={{ background: 'transparent', border: 'none', color: '#06B6D4', cursor: 'pointer', padding: '0 3px', display: 'flex', alignItems: 'center' }}
              title="Copy server link to invite classmates"
            >
              {copiedServerUrl ? <Check size={13} color="#10B981" /> : <Copy size={13} />}
            </button>
            <button 
              onClick={() => setIsServerModalOpen(true)}
              style={{ background: 'transparent', border: 'none', color: '#94A3B8', cursor: 'pointer', padding: '0 2px' }}
              title="Change target server / tunnel URL"
            >
              <Settings size={13} />
            </button>
          </div>

          {/* MQTT Protocol Badge */}
          <button 
            onClick={() => setIsMqttModalOpen(true)}
            style={{ background: 'rgba(245, 158, 11, 0.1)', border: '1px solid rgba(245, 158, 11, 0.3)', padding: '5px 10px', borderRadius: '20px', fontSize: '11px', color: '#F59E0B', fontWeight: '600', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}
          >
            <RadioTower size={12} /> MQTT: 1883
          </button>

          <div style={{ background: '#0F172A', border: '1px solid rgba(255,255,255,0.08)', padding: '5px 12px', borderRadius: '30px', fontSize: '12px', color: '#94A3B8', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Users size={13} color="#10B981" /> Online: <strong style={{ color: '#10B981' }}>{activeUsers.length || 1}</strong>
          </div>

          <div style={{ background: '#0F172A', border: '1px solid rgba(255,255,255,0.08)', padding: '5px 12px', borderRadius: '30px', fontSize: '12px', color: '#94A3B8', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <User size={13} color="#06B6D4" /> User: <strong style={{ color: '#F8FAFC' }}>{currentUser}</strong>
          </div>

          <button className="btn-danger" style={{ padding: '6px 12px', fontSize: '11px' }} onClick={() => setCurrentUser(null)}>
            Switch User
          </button>
        </div>
      </div>

      {/* STUDENT VIEW */}
      {userRole === 'student' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'minmax(320px, 360px) 1fr', gap: '20px' }}>
          
          {/* Cipher Control & RSA Keypair Drawer */}
          <div className="glass-panel" style={{ padding: '22px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#06B6D4', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Sliders size={18} /> Transmission Mode
              </h3>

              {/* Recipient Dropdown (Broadcast vs 1-1 Peers) */}
              <div style={{ marginBottom: '14px' }}>
                <label style={{ display: 'block', fontSize: '12px', color: '#94A3B8', marginBottom: '6px', fontWeight: '600' }}>
                  Chat Destination:
                </label>
                <select 
                  style={{ width: '100%', fontWeight: '600' }} 
                  value={selectedRecipient} 
                  onChange={(e) => setSelectedRecipient(e.target.value)}
                >
                  <option value="Classroom Broadcast" style={{ fontWeight: 'bold', color: '#06B6D4' }}>
                    📢 Classroom Broadcast (All Participants)
                  </option>
                  <optgroup label="1-1 Direct End-to-End Partners">
                    {availableRecipients.map(peer => (
                      <option key={peer} value={peer}>
                        👤 {peer} {activeUsers.some(u => u.username === peer) ? '(Online)' : ''}
                      </option>
                    ))}
                  </optgroup>
                </select>
              </div>

              {/* Cipher Algorithm Selector */}
              <div style={{ marginBottom: '14px' }}>
                <label style={{ display: 'block', fontSize: '12px', color: '#94A3B8', marginBottom: '6px', fontWeight: '600' }}>
                  Encryption Algorithm:
                </label>
                <select style={{ width: '100%' }} value={cipherType} onChange={(e) => setCipherType(e.target.value)}>
                  <option value="Caesar">Caesar Shift Cipher (Symmetric)</option>
                  <option value="Vigenère">Vigenère Polyalphabetic (Symmetric)</option>
                  <option value="RSA">🔑 RSA Asymmetric (Public/Private Key)</option>
                  <option value="ROT13">ROT13 (Fixed Shift 13)</option>
                  <option value="Plaintext">Plaintext (No Encryption)</option>
                </select>
              </div>

              {cipherType === 'Caesar' && (
                <div style={{ marginBottom: '14px' }}>
                  <label style={{ display: 'block', fontSize: '12px', color: '#94A3B8', marginBottom: '6px', fontWeight: '600' }}>Shift Key (0 - 25):</label>
                  <input type="number" min="0" max="25" style={{ width: '100%' }} value={cipherKey} onChange={(e) => setCipherKey(e.target.value)} />
                </div>
              )}

              {cipherType === 'Vigenère' && (
                <div style={{ marginBottom: '14px' }}>
                  <label style={{ display: 'block', fontSize: '12px', color: '#94A3B8', marginBottom: '6px', fontWeight: '600' }}>Keyword Secret:</label>
                  <input type="text" style={{ width: '100%' }} value={cipherKey} placeholder="e.g. CRYPTO" onChange={(e) => setCipherKey(e.target.value)} />
                </div>
              )}

              {cipherType === 'RSA' && (
                <div style={{ marginBottom: '14px', background: '#0F172A', padding: '14px', borderRadius: '10px', border: '1px solid rgba(6, 182, 212, 0.3)' }}>
                  {selectedRecipient === 'Classroom Broadcast' ? (
                    <div style={{ color: '#F59E0B', fontSize: '12px', lineHeight: '1.5' }}>
                      <AlertTriangle size={15} style={{ verticalAlign: 'middle', marginRight: '6px' }} />
                      <strong>1-to-1 Asymmetric Notice:</strong> RSA requires a single recipient's Public Key. To broadcast to everyone, select a Symmetric cipher (Caesar/Vigenère) or choose an individual classmate for 1-1 RSA!
                    </div>
                  ) : (
                    <>
                      <label style={{ display: 'block', fontSize: '11px', color: '#06B6D4', marginBottom: '4px', fontWeight: '700' }}>
                        TARGET PUBLIC KEY ({selectedRecipient}):
                      </label>
                      <div style={{ fontSize: '11px', color: '#F8FAFC', fontFamily: 'JetBrains Mono, monospace', wordBreak: 'break-all', marginBottom: '6px' }}>
                        Modulus N: 0x{publicDirectory[selectedRecipient]?.N || '3FE5'}<br/>
                        Exponent e: {publicDirectory[selectedRecipient]?.e || '10001'}
                      </div>
                      <p style={{ fontSize: '11px', color: '#94A3B8', lineHeight: '1.4' }}>
                        Encrypted with {selectedRecipient}'s public key ($C = M^e \bmod N$). Only {selectedRecipient}'s private key $d$ can decrypt.
                      </p>
                    </>
                  )}
                </div>
              )}
            </div>

            {/* My RSA Key Management Panel */}
            <div style={{ padding: '16px', background: 'rgba(15, 23, 42, 0.9)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.08)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ fontSize: '12px', color: '#F59E0B', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Key size={14} /> MY RSA KEYPAIR
                </span>
                <button className="btn-primary" style={{ padding: '4px 8px', fontSize: '11px' }} onClick={handleGenerateNewRsaKeys} title="Generate new keypair and broadcast public key to directory">
                  <RefreshCw size={12} /> Regenerate
                </button>
              </div>

              {myRsaKeys ? (
                <div style={{ fontSize: '11px', fontFamily: 'JetBrains Mono, monospace', color: '#94A3B8', lineHeight: '1.6' }}>
                  <span style={{ color: '#10B981' }}>Public (N): 0x{myRsaKeys.publicKey.N}</span><br/>
                  <span style={{ color: '#EF4444' }}>Private (d): 0x{myRsaKeys.privateKey.d}</span><br/>
                  <span>Factors: p={myRsaKeys.p}, q={myRsaKeys.q}</span>
                </div>
              ) : (
                <p style={{ fontSize: '11px', color: '#64748B' }}>Generating RSA keypair...</p>
              )}
            </div>

            {/* Classroom Active Users Online List */}
            <div style={{ padding: '14px', background: 'rgba(15, 23, 42, 0.6)', borderRadius: '10px', border: '1px solid rgba(255, 255, 255, 0.05)' }}>
              <div style={{ fontSize: '12px', fontWeight: '700', color: '#94A3B8', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Users size={14} color="#10B981" /> Connected Participants ({activeUsers.length})
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                {activeUsers.map(u => (
                  <span 
                    key={u.username}
                    onClick={() => {
                      if (u.username !== currentUser) setSelectedRecipient(u.username);
                    }}
                    style={{
                      fontSize: '11px',
                      padding: '3px 8px',
                      borderRadius: '12px',
                      background: u.username === currentUser ? 'rgba(6, 182, 212, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                      color: u.username === currentUser ? '#06B6D4' : '#F8FAFC',
                      cursor: u.username !== currentUser ? 'pointer' : 'default',
                      border: '1px solid rgba(255,255,255,0.08)'
                    }}
                    title={u.username !== currentUser ? `Click to chat 1-1 with ${u.username}` : 'You'}
                  >
                    {u.username === currentUser ? `★ ${u.username} (You)` : `● ${u.username}`}
                  </span>
                ))}
              </div>
            </div>

          </div>

          {/* Chat Feed Card */}
          <div className="glass-panel" style={{ padding: '22px', display: 'flex', flexDirection: 'column', height: '680px' }}>
            <div style={{ paddingBottom: '14px', borderBottom: '1px solid rgba(255,255,255,0.08)', marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ fontSize: '17px', fontWeight: '700', color: '#F8FAFC', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <MessageSquare size={18} color="#06B6D4" /> 
                {selectedRecipient === 'Classroom Broadcast' ? (
                  <span>📢 <span style={{ color: '#06B6D4' }}>Classroom Broadcast</span> (All Participants)</span>
                ) : (
                  <span>🔒 1-1 Channel with <span style={{ color: '#06B6D4' }}>{selectedRecipient}</span></span>
                )}
              </h3>
              <span style={{ fontSize: '12px', color: '#10B981', display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '600' }}>
                <Activity size={14} /> Active Channel
              </span>
            </div>

            {/* Chat Scroll Area */}
            <div style={{ flex: 1, overflowY: 'auto', paddingRight: '8px' }}>
              {currentChatMessages.length === 0 ? (
                <div style={{ textAlign: 'center', color: '#64748B', marginTop: '140px', fontSize: '14px' }}>
                  {selectedRecipient === 'Classroom Broadcast' 
                    ? 'No classroom broadcast messages sent yet. Pick a cipher and transmit to all participants!' 
                    : `No direct messages between you and ${selectedRecipient}. Send an encrypted payload to begin.`}
                </div>
              ) : (
                currentChatMessages.map((msg, i) => {
                  const isMe = msg.sender === currentUser;
                  const decrypted = getDecryptedTextForStudent(msg);
                  const isBroadcast = msg.recipient === 'Classroom Broadcast' || msg.isBroadcast;

                  return (
                    <div key={i} style={{ display: 'flex', justifyContent: isMe ? 'flex-end' : 'flex-start', marginBottom: '16px' }}>
                      <div style={{
                        maxWidth: '72%',
                        padding: '14px 18px',
                        borderRadius: '14px',
                        background: isMe ? 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)' : '#0F172A',
                        border: isMe ? '1px solid #06B6D4' : '1px solid rgba(255,255,255,0.1)'
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px', marginBottom: '8px', fontSize: '11px', color: '#94A3B8' }}>
                          <span>
                            <strong>{msg.sender}</strong> {isBroadcast ? '→ 📢 Classroom' : `→ ${msg.recipient}`}
                            <span style={{ marginLeft: '8px', color: '#06B6D4', fontSize: '10px' }}>({msg.cipherType})</span>
                            {msg.viaMqtt && <span style={{ marginLeft: '6px', color: '#F59E0B', fontSize: '10px' }}>[MQTT]</span>}
                          </span>
                          <span>{msg.timestamp}</span>
                        </div>

                        {msg.isSpoofed && (
                          <div style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#EF4444', padding: '4px 10px', borderRadius: '6px', fontSize: '11px', fontWeight: '600', marginBottom: '8px', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                            <AlertTriangle size={13} /> Unverified Sender (Impersonation Detected)
                          </div>
                        )}

                        {msg.isTampered && (
                          <div style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#F59E0B', padding: '4px 10px', borderRadius: '6px', fontSize: '11px', fontWeight: '600', marginBottom: '8px', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                            <ShieldAlert size={13} /> Tampered in Transit (MITM Injection)
                          </div>
                        )}

                        <div style={{ fontSize: '15px', color: '#F8FAFC', marginBottom: '8px', fontWeight: '500' }}>
                          {decrypted}
                        </div>

                        <div style={{ background: '#070A12', padding: '8px 12px', borderRadius: '8px', fontSize: '12px', color: '#06B6D4', fontFamily: 'JetBrains Mono, monospace', wordBreak: 'break-all' }}>
                          Wire: {msg.ciphertext}
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
              <div ref={chatBottomRef} />
            </div>

            {/* Input Bar */}
            <form onSubmit={handleSendMessage} style={{ display: 'flex', gap: '12px', marginTop: '16px', paddingTop: '16px', borderTop: '1px solid rgba(255,255,255,0.08)' }}>
              <input
                type="text"
                style={{ flex: 1 }}
                placeholder={selectedRecipient === 'Classroom Broadcast' ? 'Type message to broadcast to classroom...' : `Type message for ${selectedRecipient}...`}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
              <button type="submit" className="btn-primary">
                <Send size={16} /> Encrypt & Transmit
              </button>
            </form>
          </div>
        </div>
      )}

      {/* INSTRUCTOR DASHBOARD VIEW */}
      {userRole === 'instructor' && (
        <div style={{ display: 'grid', gridTemplateRows: 'auto 1fr', gap: '20px' }}>
          
          {/* Top Control Center */}
          <div className="glass-panel glass-panel-accent" style={{ padding: '20px 24px', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '16px' }}>
            <div>
              <h3 style={{ fontSize: '18px', fontWeight: '700', color: '#F59E0B', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Eye size={22} /> Instructor Wiretap & Cryptanalysis Control Center
              </h3>
              <p style={{ fontSize: '13px', color: '#94A3B8', marginTop: '4px' }}>
                Passive eavesdropping & active MITM intercept across 1-1, Classroom Broadcast, and MQTT topics.
              </p>
            </div>

            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <button 
                className={activeMitmIntercept ? "btn-danger" : "btn-amber"} 
                onClick={toggleMitmIntercept}
                style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}
              >
                <Zap size={16} /> 
                {activeMitmIntercept ? "Active Intercept Mode: ON" : "Enable Active Intercept Queue"}
              </button>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr minmax(380px, 420px)', gap: '20px' }}>
            
            {/* Left Column: Intercept Feed & Active Queue */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              
              {/* Active Intercept Queue */}
              {activeMitmIntercept && (
                <div className="glass-panel" style={{ padding: '20px', border: '1px solid #EF4444' }}>
                  <h4 style={{ fontSize: '15px', fontWeight: '700', color: '#EF4444', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <ShieldAlert size={18} /> In-Flight Interception Queue ({interceptQueue.length} Pending)
                  </h4>

                  {interceptQueue.length === 0 ? (
                    <p style={{ fontSize: '13px', color: '#64748B' }}>Awaiting classroom transmissions (Socket.IO / MQTT)...</p>
                  ) : (
                    interceptQueue.map((item) => (
                      <div key={item.id} style={{ background: '#0F172A', padding: '14px', borderRadius: '12px', marginBottom: '12px', border: '1px solid rgba(255,255,255,0.1)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#94A3B8', marginBottom: '6px' }}>
                          <span><strong>{item.sender}</strong> → <strong>{item.recipient}</strong></span>
                          <span style={{ color: '#F59E0B', fontWeight: '600' }}>ID: {item.id}</span>
                        </div>
                        <div style={{ background: '#070A12', padding: '10px', borderRadius: '8px', fontSize: '12px', color: '#06B6D4', fontFamily: 'JetBrains Mono, monospace', marginBottom: '10px', wordBreak: 'break-all' }}>
                          Ciphertext: {item.ciphertext}
                        </div>

                        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                          <input
                            type="text"
                            placeholder="Tamper payload..."
                            style={{ flex: 1, padding: '6px 10px', fontSize: '12px' }}
                            value={tamperInput}
                            onChange={(e) => setTamperInput(e.target.value)}
                          />
                          <button className="btn-primary" style={{ padding: '6px 12px', fontSize: '12px' }} onClick={() => handleProcessQueuedMessage(item.id, 'APPROVE')}>
                            Release
                          </button>
                          <button className="btn-amber" style={{ padding: '6px 12px', fontSize: '12px' }} onClick={() => handleProcessQueuedMessage(item.id, 'TAMPER')}>
                            Tamper
                          </button>
                          <button className="btn-danger" style={{ padding: '6px 12px', fontSize: '12px' }} onClick={() => handleProcessQueuedMessage(item.id, 'DROP')}>
                            Drop
                          </button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* Wiretap Table */}
              <div className="glass-panel" style={{ padding: '20px', flex: 1 }}>
                <h4 style={{ fontSize: '15px', fontWeight: '700', color: '#06B6D4', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Terminal size={18} /> Live Wiretap Transmissions ({wireLogs.length} Frames Captured)
                </h4>

                <div style={{ maxHeight: '440px', overflowY: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
                    <thead>
                      <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', color: '#94A3B8' }}>
                        <th style={{ padding: '8px' }}>Time</th>
                        <th style={{ padding: '8px' }}>Sender</th>
                        <th style={{ padding: '8px' }}>Recipient</th>
                        <th style={{ padding: '8px' }}>Payload</th>
                        <th style={{ padding: '8px' }}>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {wireLogs.map((log) => (
                        <tr key={log.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', color: log.isSpoofed ? '#EF4444' : '#F8FAFC' }}>
                          <td style={{ padding: '8px', color: '#94A3B8' }}>{log.timestamp}</td>
                          <td style={{ padding: '8px', fontWeight: 'bold' }}>
                            {log.sender} {log.viaMqtt && <span style={{ color: '#F59E0B', fontSize: '10px' }}>[MQTT]</span>}
                          </td>
                          <td style={{ padding: '8px' }}>{log.recipient}</td>
                          <td style={{ padding: '8px', fontFamily: 'JetBrains Mono, monospace', color: '#06B6D4', maxWidth: '180px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                            {log.ciphertext}
                          </td>
                          <td style={{ padding: '8px' }}>
                            <button className="btn-primary" style={{ padding: '5px 10px', fontSize: '11px' }} onClick={() => handleInspectAndDecrypt(log)}>
                              Crack Cipher
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Right Column: Automated Decrypter & Impersonation Engine */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              
              {/* Cryptanalysis Panel */}
              <div className="glass-panel" style={{ padding: '20px' }}>
                <h4 style={{ fontSize: '15px', fontWeight: '700', color: '#F59E0B', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Cpu size={18} /> Automated Cryptanalysis Suite
                </h4>

                {selectedLogForDecrypt ? (
                  <div style={{ background: '#0F172A', padding: '14px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)' }}>
                    <p style={{ fontSize: '12px', color: '#94A3B8', marginBottom: '4px' }}>
                      Packet ID: <strong style={{ color: '#06B6D4' }}>{selectedLogForDecrypt.id}</strong>
                    </p>
                    <p style={{ fontSize: '12px', color: '#94A3B8', marginBottom: '12px', wordBreak: 'break-all' }}>
                      Ciphertext: <code style={{ color: '#F59E0B' }}>{selectedLogForDecrypt.ciphertext}</code>
                    </p>

                    {autoDecryptResult && (
                      <div style={{ background: '#070A12', padding: '12px', borderRadius: '10px', borderLeft: '4px solid #10B981' }}>
                        <p style={{ fontSize: '12px', color: '#10B981', fontWeight: '700', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <CheckCircle2 size={14} /> Decrypted Plaintext Result:
                        </p>
                        <p style={{ fontSize: '15px', color: '#F8FAFC', marginBottom: '8px', fontWeight: '600' }}>
                          "{autoDecryptResult.bestText}"
                        </p>
                        <div style={{ fontSize: '11px', color: '#94A3B8', lineHeight: '1.5' }}>
                          <span>Key Recovered: <strong style={{ color: '#F8FAFC' }}>{autoDecryptResult.bestKey}</strong></span><br/>
                          <span>Metric Score: <strong style={{ color: '#F8FAFC' }}>{autoDecryptResult.score}</strong></span>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <p style={{ fontSize: '13px', color: '#64748B', lineHeight: '1.5' }}>
                    Click "Crack Cipher" on any captured wireframe to execute frequency analysis or Fermat's $N=p \times q$ factorization.
                  </p>
                )}
              </div>

              {/* Impersonation / Packet Spoofing Engine */}
              <div className="glass-panel" style={{ padding: '20px' }}>
                <h4 style={{ fontSize: '15px', fontWeight: '700', color: '#EF4444', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <UserCheck size={18} /> Packet Impersonation (Spoofing)
                </h4>

                <form onSubmit={handleSpoofMessage}>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '10px' }}>
                    <div>
                      <label style={{ fontSize: '11px', color: '#94A3B8', fontWeight: '600' }}>Spoof Sender:</label>
                      <input 
                        type="text" 
                        value={spoofSender} 
                        onChange={(e) => setSpoofSender(e.target.value)} 
                        style={{ width: '100%', fontSize: '12px', padding: '6px 10px' }} 
                        placeholder="Alice"
                      />
                    </div>
                    <div>
                      <label style={{ fontSize: '11px', color: '#94A3B8', fontWeight: '600' }}>Target Recipient:</label>
                      <select style={{ width: '100%', fontSize: '12px', padding: '6px 10px' }} value={spoofRecipient} onChange={(e) => setSpoofRecipient(e.target.value)}>
                        <option value="Classroom Broadcast">📢 Classroom Broadcast</option>
                        <option value="Bob">Bob</option>
                        <option value="Alice">Alice</option>
                        <option value="Charlie">Charlie</option>
                        {onlinePeerNames.map(name => (
                          <option key={name} value={name}>{name}</option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div style={{ marginBottom: '10px' }}>
                    <label style={{ fontSize: '11px', color: '#94A3B8', fontWeight: '600' }}>Cipher Type:</label>
                    <select style={{ width: '100%', fontSize: '12px', padding: '6px 10px' }} value={spoofCipherType} onChange={(e) => setSpoofCipherType(e.target.value)}>
                      <option value="Caesar">Caesar Shift</option>
                      <option value="Vigenère">Vigenère</option>
                      <option value="RSA">🔑 RSA Asymmetric</option>
                      <option value="ROT13">ROT13</option>
                    </select>
                  </div>

                  <div style={{ marginBottom: '10px' }}>
                    <label style={{ fontSize: '11px', color: '#94A3B8', fontWeight: '600' }}>Shift / Key:</label>
                    <input type="text" style={{ width: '100%', fontSize: '12px', padding: '6px 10px' }} value={spoofKey} onChange={(e) => setSpoofKey(e.target.value)} />
                  </div>

                  <div style={{ marginBottom: '14px' }}>
                    <label style={{ fontSize: '11px', color: '#94A3B8', fontWeight: '600' }}>Spoofed Message Content:</label>
                    <input type="text" placeholder="e.g. CLASSROOM ANNOUNCEMENT: EXAM CANCELLED" style={{ width: '100%', fontSize: '12px', padding: '6px 10px' }} value={spoofText} onChange={(e) => setSpoofText(e.target.value)} />
                  </div>

                  <button type="submit" className="btn-danger" style={{ width: '100%', justifyContent: 'center' }}>
                    Inject Forged Packet
                  </button>
                </form>
              </div>

            </div>
          </div>
        </div>
      )}
    </main>
  );
}
