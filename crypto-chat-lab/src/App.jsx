import React, { useState, useEffect, useRef } from 'react';
import { io } from 'socket.io-client';
import { 
  Lock, ShieldAlert, ShieldCheck, UserCheck, Eye, Terminal, 
  Send, AlertTriangle, Key, Cpu, Zap, Radio, CheckCircle2, 
  MessageSquare, Activity, Sparkles, Sliders, ChevronRight, User, RefreshCw
} from 'lucide-react';
import { 
  caesarEncrypt, caesarDecrypt, vigenereEncrypt, vigenereDecrypt, 
  rot13, autoBreakCipher, generateRSAKeyPair, rsaEncrypt, rsaDecrypt, crackRSAModulus 
} from './utils/cryptoUtils.js';

const socket = io(window.location.origin, {
  autoConnect: false
});

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [userRole, setUserRole] = useState('student');
  const [selectedRecipient, setSelectedRecipient] = useState('Bob');
  
  // Student Encryption State
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [cipherType, setCipherType] = useState('Caesar'); // 'Caesar', 'Vigenère', 'RSA', 'ROT13', 'Plaintext'
  const [cipherKey, setCipherKey] = useState('3');

  // RSA Asymmetric Key Directory (Shared across sockets in React state / Socket broadcast)
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
  const [spoofRecipient, setSpoofRecipient] = useState('Bob');
  const [spoofText, setSpoofText] = useState('');
  const [spoofCipherType, setSpoofCipherType] = useState('Caesar');
  const [spoofKey, setSpoofKey] = useState('3');

  // Tamper Form State
  const [tamperInput, setTamperInput] = useState('');

  const chatBottomRef = useRef(null);

  // Initialize Default RSA Keys for Alice & Bob
  useEffect(() => {
    const aliceKeys = generateRSAKeyPair(true);
    const bobKeys = generateRSAKeyPair(true);
    setPublicDirectory({
      Alice: aliceKeys.publicKey,
      Bob: bobKeys.publicKey
    });
  }, []);

  useEffect(() => {
    socket.connect();

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

    return () => {
      socket.off('receive-message', handleNewMessage);
      socket.off('message-sent-ack', handleNewMessage);
      socket.off('initial-wire-logs');
      socket.off('new-wire-log');
      socket.off('intercept-mode-changed');
      socket.off('queue-update');
      socket.disconnect();
    };
  }, []);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleLogin = (username, role) => {
    setCurrentUser(username);
    setUserRole(role);

    // Auto-generate RSA keypair for student if missing
    if (role === 'student' && !myRsaKeys) {
      const keys = generateRSAKeyPair(true);
      setMyRsaKeys(keys);
      setPublicDirectory(prev => ({
        ...prev,
        [username]: keys.publicKey
      }));
    }

    socket.emit('register-user', { username, role });
  };

  const handleGenerateNewRsaKeys = () => {
    const keys = generateRSAKeyPair(true);
    setMyRsaKeys(keys);
    if (currentUser) {
      setPublicDirectory(prev => ({
        ...prev,
        [currentUser]: keys.publicKey
      }));
    }
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputText.trim() || !currentUser) return;

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
        alert(`Public Key for ${selectedRecipient} not found in RSA Directory!`);
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
      ciphertext: encryptedPayload,
      cipherType: cipherType,
      key: cipherKey,
      rsaPublicKey: publicDirectory[selectedRecipient] || null,
      plaintextSent: inputText
    };

    socket.emit('send-message', payload);
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
    if (!spoofText.trim()) return;

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

    socket.emit('mitm-impersonate', {
      spoofedSender: spoofSender,
      recipient: spoofRecipient,
      ciphertext: encryptedPayload,
      cipherType: spoofCipherType,
      key: spoofKey
    });

    setSpoofText('');
  };

  const toggleMitmIntercept = () => {
    const nextState = !activeMitmIntercept;
    setActiveMitmIntercept(nextState);
    socket.emit('mitm-toggle-intercept', { enabled: nextState });
  };

  const handleProcessQueuedMessage = (messageId, action) => {
    socket.emit('mitm-process-queued-message', {
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

  // LANDING HERO & ROLE SELECTION SCREEN
  if (!currentUser) {
    return (
      <main className="overflow-x-hidden w-full max-w-full" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '60px 24px' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', width: '100%' }}>
          
          <div style={{ textAlign: 'center', marginBottom: '48px' }}>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '6px 16px', background: 'rgba(6, 182, 212, 0.1)', border: '1px solid rgba(6, 182, 212, 0.3)', borderRadius: '30px', color: '#06B6D4', fontSize: '13px', fontWeight: '600', marginBottom: '24px' }}>
              <Sparkles size={14} /> UNIVERSITY LAB PLATFORM · CS-4XX
            </div>

            <h1 style={{ fontSize: 'clamp(2.5rem, 4.5vw, 4.2rem)', fontWeight: '800', lineHeight: '1.15', color: '#F8FAFC', maxWidth: '1000px', margin: '0 auto 20px auto' }}>
              Encrypted 1-1 Messaging & <span style={{ color: '#F59E0B' }}>RSA Public-Key Cryptography</span>
            </h1>

            <p style={{ fontSize: '17px', color: '#94A3B8', maxWidth: '680px', margin: '0 auto', lineHeight: '1.6' }}>
              Perform live Symmetric (Caesar/Vigenère) & Asymmetric RSA Public/Private Key encryption, monitor wiretap packet logs, and execute automated Fermat RSA prime factorization.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>
            
            <div className="glass-panel" style={{ padding: '32px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '260px' }}>
              <div>
                <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'rgba(6, 182, 212, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px' }}>
                  <User size={24} color="#06B6D4" />
                </div>
                <h3 style={{ fontSize: '20px', fontWeight: '700', color: '#F8FAFC', marginBottom: '8px' }}>Student Alice</h3>
                <p style={{ fontSize: '14px', color: '#94A3B8', lineHeight: '1.5' }}>Generate RSA-1024 Keypairs, configure public keys, and send encrypted payloads to Bob.</p>
              </div>
              <button className="btn-primary" style={{ width: '100%', justifyContent: 'center' }} onClick={() => handleLogin('Alice', 'student')}>
                Join as Alice <ChevronRight size={16} />
              </button>
            </div>

            <div className="glass-panel" style={{ padding: '32px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '260px' }}>
              <div>
                <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'rgba(59, 130, 246, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px' }}>
                  <User size={24} color="#3B82F6" />
                </div>
                <h3 style={{ fontSize: '20px', fontWeight: '700', color: '#F8FAFC', marginBottom: '8px' }}>Student Bob</h3>
                <p style={{ fontSize: '14px', color: '#94A3B8', lineHeight: '1.5' }}>Publish RSA Public Keys, decrypt incoming RSA payloads with your Private Key.</p>
              </div>
              <button className="btn-primary" style={{ width: '100%', justifyContent: 'center', background: 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)' }} onClick={() => handleLogin('Bob', 'student')}>
                Join as Bob <ChevronRight size={16} />
              </button>
            </div>

            <div className="glass-panel glass-panel-accent" style={{ padding: '32px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '260px' }}>
              <div>
                <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'rgba(245, 158, 11, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px' }}>
                  <Eye size={24} color="#F59E0B" />
                </div>
                <h3 style={{ fontSize: '20px', fontWeight: '700', color: '#F59E0B', marginBottom: '8px' }}>Instructor MITM Suite</h3>
                <p style={{ fontSize: '14px', color: '#94A3B8', lineHeight: '1.5' }}>Wiretap transmissions, execute Chi-Squared & Fermat RSA Modulus Factorization attacks.</p>
              </div>
              <button className="btn-amber" style={{ width: '100%', justifyContent: 'center' }} onClick={() => handleLogin('Instructor_Dr_Smith', 'instructor')}>
                Launch MITM Dashboard <ChevronRight size={16} />
              </button>
            </div>

          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="overflow-x-hidden w-full max-w-full" style={{ padding: '24px', maxWidth: '1440px', margin: '0 auto' }}>
      
      {/* Header Bar */}
      <div className="glass-panel" style={{ padding: '16px 28px', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <Radio color={userRole === 'instructor' ? '#F59E0B' : '#06B6D4'} className="glow-cyan" size={20} />
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: '700', color: '#F8FAFC', letterSpacing: '-0.02em' }}>
              Crypto Chat Lab <span style={{ fontSize: '13px', color: userRole === 'instructor' ? '#F59E0B' : '#06B6D4', fontWeight: '600', marginLeft: '6px' }}>({userRole.toUpperCase()})</span>
            </h2>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ background: '#0F172A', border: '1px solid rgba(255,255,255,0.08)', padding: '6px 14px', borderRadius: '30px', fontSize: '13px', color: '#94A3B8', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <User size={14} color="#06B6D4" /> User: <strong style={{ color: '#F8FAFC' }}>{currentUser}</strong>
          </div>
          <button className="btn-danger" style={{ padding: '8px 14px', fontSize: '13px' }} onClick={() => setCurrentUser(null)}>
            Switch User
          </button>
        </div>
      </div>

      {/* STUDENT VIEW */}
      {userRole === 'student' && (
        <div style={{ display: 'grid', gridTemplateColumns: '360px 1fr', gap: '24px' }}>
          
          {/* Cipher Control & RSA Keypair Drawer */}
          <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: '700', color: '#06B6D4', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Sliders size={18} /> Encryption Configuration
              </h3>

              <div style={{ marginBottom: '16px' }}>
                <label style={{ display: 'block', fontSize: '12px', color: '#94A3B8', marginBottom: '6px', fontWeight: '600' }}>Chat Partner:</label>
                <select style={{ width: '100%' }} value={selectedRecipient} onChange={(e) => setSelectedRecipient(e.target.value)}>
                  <option value="Bob">Student Bob</option>
                  <option value="Alice">Student Alice</option>
                  <option value="Charlie">Student Charlie</option>
                </select>
              </div>

              <div style={{ marginBottom: '16px' }}>
                <label style={{ display: 'block', fontSize: '12px', color: '#94A3B8', marginBottom: '6px', fontWeight: '600' }}>Cipher Algorithm:</label>
                <select style={{ width: '100%' }} value={cipherType} onChange={(e) => setCipherType(e.target.value)}>
                  <option value="RSA">🔑 RSA Asymmetric (Public/Private Key)</option>
                  <option value="Caesar">Caesar Shift Cipher (Symmetric)</option>
                  <option value="Vigenère">Vigenère Polyalphabetic (Symmetric)</option>
                  <option value="ROT13">ROT13 (Fixed Shift 13)</option>
                  <option value="Plaintext">Plaintext (No Encryption)</option>
                </select>
              </div>

              {cipherType === 'Caesar' && (
                <div style={{ marginBottom: '16px' }}>
                  <label style={{ display: 'block', fontSize: '12px', color: '#94A3B8', marginBottom: '6px', fontWeight: '600' }}>Shift Key (0 - 25):</label>
                  <input type="number" min="0" max="25" style={{ width: '100%' }} value={cipherKey} onChange={(e) => setCipherKey(e.target.value)} />
                </div>
              )}

              {cipherType === 'Vigenère' && (
                <div style={{ marginBottom: '16px' }}>
                  <label style={{ display: 'block', fontSize: '12px', color: '#94A3B8', marginBottom: '6px', fontWeight: '600' }}>Keyword Secret:</label>
                  <input type="text" style={{ width: '100%' }} value={cipherKey} placeholder="e.g. SECRET" onChange={(e) => setCipherKey(e.target.value)} />
                </div>
              )}

              {cipherType === 'RSA' && (
                <div style={{ marginBottom: '16px', background: '#0F172A', padding: '14px', borderRadius: '10px', border: '1px solid rgba(6, 182, 212, 0.3)' }}>
                  <label style={{ display: 'block', fontSize: '11px', color: '#06B6D4', marginBottom: '4px', fontWeight: '700' }}>
                    PUBLIC KEY TARGET ({selectedRecipient}):
                  </label>
                  <div style={{ fontSize: '11px', color: '#F8FAFC', fontFamily: 'JetBrains Mono, monospace', wordBreak: 'break-all', marginBottom: '8px' }}>
                    Modulus N: {publicDirectory[selectedRecipient]?.N || 'N/A'}<br/>
                    Exponent e: {publicDirectory[selectedRecipient]?.e || '10001'}
                  </div>
                  <p style={{ fontSize: '11px', color: '#94A3B8' }}>
                    Messages sent using RSA will be encrypted with <b>{selectedRecipient}'s Public Key</b> ($C = M^e \bmod N$).
                  </p>
                </div>
              )}
            </div>

            {/* My RSA Key Management Panel */}
            <div style={{ padding: '16px', background: 'rgba(15, 23, 42, 0.9)', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.08)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ fontSize: '12px', color: '#F59E0B', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Key size={14} /> MY RSA KEYPAIR
                </span>
                <button className="btn-primary" style={{ padding: '4px 8px', fontSize: '11px' }} onClick={handleGenerateNewRsaKeys}>
                  <RefreshCw size={12} /> Regenerate
                </button>
              </div>

              {myRsaKeys ? (
                <div style={{ fontSize: '11px', fontFamily: 'JetBrains Mono, monospace', color: '#94A3B8', lineHeight: '1.6' }}>
                  <span style={{ color: '#10B981' }}>Public (N): 0x{myRsaKeys.publicKey.N}</span><br/>
                  <span style={{ color: '#EF4444' }}>Private (d): 0x{myRsaKeys.privateKey.d}</span><br/>
                  <span>Primes: p={myRsaKeys.p}, q={myRsaKeys.q}</span>
                </div>
              ) : (
                <p style={{ fontSize: '11px', color: '#64748B' }}>No RSA keypair generated.</p>
              )}
            </div>
          </div>

          {/* 1-1 Chat Feed Card */}
          <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', height: '680px' }}>
            <div style={{ paddingBottom: '16px', borderBottom: '1px solid rgba(255,255,255,0.08)', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ fontSize: '17px', fontWeight: '700', color: '#F8FAFC', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <MessageSquare size={18} color="#06B6D4" /> 1-1 Channel with <span style={{ color: '#06B6D4' }}>{selectedRecipient}</span>
              </h3>
              <span style={{ fontSize: '12px', color: '#10B981', display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '600' }}>
                <Activity size={14} /> Active Channel
              </span>
            </div>

            {/* Chat Scroll Area */}
            <div style={{ flex: 1, overflowY: 'auto', paddingRight: '8px' }}>
              {messages.filter((msg) => 
                (msg.sender === currentUser && msg.recipient === selectedRecipient) ||
                (msg.recipient === currentUser && msg.sender === selectedRecipient) ||
                (msg.isSpoofed && (msg.sender === currentUser || msg.recipient === currentUser))
              ).length === 0 ? (
                <div style={{ textAlign: 'center', color: '#64748B', marginTop: '140px', fontSize: '14px' }}>
                  No messages transmitted. Send an encrypted payload to begin communication.
                </div>
              ) : (
                messages
                  .filter((msg) => 
                    (msg.sender === currentUser && msg.recipient === selectedRecipient) ||
                    (msg.recipient === currentUser && msg.sender === selectedRecipient) ||
                    (msg.isSpoofed && (msg.sender === currentUser || msg.recipient === currentUser))
                  )
                  .map((msg, i) => {
                  const isMe = msg.sender === currentUser;
                  const decrypted = getDecryptedTextForStudent(msg);

                  return (
                    <div key={i} style={{ display: 'flex', justifyContent: isMe ? 'flex-end' : 'flex-start', marginBottom: '18px' }}>
                      <div style={{
                        maxWidth: '68%',
                        padding: '16px 20px',
                        borderRadius: '14px',
                        background: isMe ? 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)' : '#0F172A',
                        border: isMe ? '1px solid #06B6D4' : '1px solid rgba(255,255,255,0.1)'
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px', marginBottom: '8px', fontSize: '11px', color: '#94A3B8' }}>
                          <span><strong>{msg.sender}</strong> → {msg.recipient}</span>
                          <span>{msg.timestamp}</span>
                        </div>

                        {msg.isSpoofed && (
                          <div style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#EF4444', padding: '4px 10px', borderRadius: '6px', fontSize: '11px', fontWeight: '600', marginBottom: '10px', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                            <AlertTriangle size={13} /> Unverified Sender (Impersonation Detected)
                          </div>
                        )}

                        {msg.isTampered && (
                          <div style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#F59E0B', padding: '4px 10px', borderRadius: '6px', fontSize: '11px', fontWeight: '600', marginBottom: '10px', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                            <ShieldAlert size={13} /> Tampered in Transit (MITM Injection)
                          </div>
                        )}

                        <div style={{ fontSize: '15px', color: '#F8FAFC', marginBottom: '10px', fontWeight: '500' }}>
                          {decrypted}
                        </div>

                        <div style={{ background: '#070A12', padding: '8px 12px', borderRadius: '8px', fontSize: '12px', color: '#06B6D4', fontFamily: 'JetBrains Mono, monospace', wordBreak: 'break-all' }}>
                          Payload: {msg.ciphertext}
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
              <div ref={chatBottomRef} />
            </div>

            {/* Input Bar */}
            <form onSubmit={handleSendMessage} style={{ display: 'flex', gap: '12px', marginTop: '20px', paddingTop: '20px', borderTop: '1px solid rgba(255,255,255,0.08)' }}>
              <input
                type="text"
                style={{ flex: 1 }}
                placeholder={`Type encrypted message for ${selectedRecipient}...`}
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
        <div style={{ display: 'grid', gridTemplateRows: 'auto 1fr', gap: '24px' }}>
          
          {/* Top Control Center */}
          <div className="glass-panel glass-panel-accent" style={{ padding: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h3 style={{ fontSize: '19px', fontWeight: '700', color: '#F59E0B', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Eye size={22} /> Instructor Wiretap & Cryptanalysis Control Center
              </h3>
              <p style={{ fontSize: '14px', color: '#94A3B8', marginTop: '4px' }}>
                Monitor active socket packets, execute Chi-Squared & Fermat RSA Prime Factorization attacks, or simulate Man-in-the-Middle wiretaps.
              </p>
            </div>

            <button 
              className={activeMitmIntercept ? "btn-danger" : "btn-amber"} 
              onClick={toggleMitmIntercept}
              style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}
            >
              <Zap size={16} /> 
              {activeMitmIntercept ? "Active Intercept Mode: ON" : "Enable Active Intercept Queue"}
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 420px', gap: '24px' }}>
            
            {/* Left Column: Intercept Feed & Active Queue */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              
              {/* Active Intercept Queue */}
              {activeMitmIntercept && (
                <div className="glass-panel" style={{ padding: '24px', border: '1px solid #EF4444' }}>
                  <h4 style={{ fontSize: '16px', fontWeight: '700', color: '#EF4444', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <ShieldAlert size={18} /> Intercepted Inspection Queue ({interceptQueue.length} Pending)
                  </h4>

                  {interceptQueue.length === 0 ? (
                    <p style={{ fontSize: '13px', color: '#64748B' }}>Queue empty. Awaiting student socket transmissions...</p>
                  ) : (
                    interceptQueue.map((item) => (
                      <div key={item.id} style={{ background: '#0F172A', padding: '16px', borderRadius: '12px', marginBottom: '14px', border: '1px solid rgba(255,255,255,0.1)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#94A3B8', marginBottom: '8px' }}>
                          <span><strong>{item.sender}</strong> → {item.recipient}</span>
                          <span style={{ color: '#F59E0B', fontWeight: '600' }}>ID: {item.id}</span>
                        </div>
                        <div style={{ background: '#070A12', padding: '10px', borderRadius: '8px', fontSize: '13px', color: '#06B6D4', fontFamily: 'JetBrains Mono, monospace', marginBottom: '12px', wordBreak: 'break-all' }}>
                          Ciphertext: {item.ciphertext}
                        </div>

                        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                          <input
                            type="text"
                            placeholder="Tamper payload..."
                            style={{ flex: 1, padding: '8px 12px', fontSize: '13px' }}
                            value={tamperInput}
                            onChange={(e) => setTamperInput(e.target.value)}
                          />
                          <button className="btn-primary" style={{ padding: '8px 14px', fontSize: '12px' }} onClick={() => handleProcessQueuedMessage(item.id, 'APPROVE')}>
                            Release
                          </button>
                          <button className="btn-amber" style={{ padding: '8px 14px', fontSize: '12px' }} onClick={() => handleProcessQueuedMessage(item.id, 'TAMPER')}>
                            Tamper
                          </button>
                          <button className="btn-danger" style={{ padding: '8px 14px', fontSize: '12px' }} onClick={() => handleProcessQueuedMessage(item.id, 'DROP')}>
                            Drop
                          </button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* Wiretap Table */}
              <div className="glass-panel" style={{ padding: '24px', flex: 1 }}>
                <h4 style={{ fontSize: '16px', fontWeight: '700', color: '#06B6D4', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Terminal size={18} /> Live Wiretap Transmissions ({wireLogs.length} Frames Captured)
                </h4>

                <div style={{ maxHeight: '440px', overflowY: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
                    <thead>
                      <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', color: '#94A3B8' }}>
                        <th style={{ padding: '10px' }}>Time</th>
                        <th style={{ padding: '10px' }}>Sender</th>
                        <th style={{ padding: '10px' }}>Recipient</th>
                        <th style={{ padding: '10px' }}>Ciphertext Payload</th>
                        <th style={{ padding: '10px' }}>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {wireLogs.map((log) => (
                        <tr key={log.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', color: log.isSpoofed ? '#EF4444' : '#F8FAFC' }}>
                          <td style={{ padding: '10px', color: '#94A3B8' }}>{log.timestamp}</td>
                          <td style={{ padding: '10px', fontWeight: 'bold' }}>{log.sender}</td>
                          <td style={{ padding: '10px' }}>{log.recipient}</td>
                          <td style={{ padding: '10px', fontFamily: 'JetBrains Mono, monospace', color: '#06B6D4', maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis' }}>{log.ciphertext}</td>
                          <td style={{ padding: '10px' }}>
                            <button className="btn-primary" style={{ padding: '6px 12px', fontSize: '12px' }} onClick={() => handleInspectAndDecrypt(log)}>
                              Cracking Analysis
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
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              
              {/* Cryptanalysis Panel */}
              <div className="glass-panel" style={{ padding: '24px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: '700', color: '#F59E0B', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Cpu size={18} /> Automated Cryptanalysis Suite
                </h4>

                {selectedLogForDecrypt ? (
                  <div style={{ background: '#0F172A', padding: '16px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)' }}>
                    <p style={{ fontSize: '13px', color: '#94A3B8', marginBottom: '6px' }}>
                      Inspecting Packet: <strong style={{ color: '#06B6D4' }}>{selectedLogForDecrypt.id}</strong>
                    </p>
                    <p style={{ fontSize: '13px', color: '#94A3B8', marginBottom: '14px', wordBreak: 'break-all' }}>
                      Ciphertext: <code style={{ color: '#F59E0B' }}>{selectedLogForDecrypt.ciphertext}</code>
                    </p>

                    {autoDecryptResult && (
                      <div style={{ background: '#070A12', padding: '14px', borderRadius: '10px', borderLeft: '4px solid #10B981' }}>
                        <p style={{ fontSize: '12px', color: '#10B981', fontWeight: '700', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <CheckCircle2 size={14} /> Decrypted Plaintext Result:
                        </p>
                        <p style={{ fontSize: '16px', color: '#F8FAFC', marginBottom: '10px', fontWeight: '600' }}>
                          "{autoDecryptResult.bestText}"
                        </p>
                        <div style={{ fontSize: '12px', color: '#94A3B8', lineHeight: '1.6' }}>
                          <span>Key Recovered: <strong style={{ color: '#F8FAFC' }}>{autoDecryptResult.bestKey}</strong></span><br/>
                          <span>Metric Score: <strong style={{ color: '#F8FAFC' }}>{autoDecryptResult.score}</strong></span>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <p style={{ fontSize: '13px', color: '#64748B', lineHeight: '1.5' }}>
                    Select "Cracking Analysis" on any wire log frame to launch the Chi-Squared or Fermat RSA Prime Factorization attack suite.
                  </p>
                )}
              </div>

              {/* Impersonation / Packet Spoofing Engine */}
              <div className="glass-panel" style={{ padding: '24px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: '700', color: '#EF4444', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <UserCheck size={18} /> Packet Impersonation (Spoofing) Engine
                </h4>

                <form onSubmit={handleSpoofMessage}>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '12px' }}>
                    <div>
                      <label style={{ fontSize: '12px', color: '#94A3B8', fontWeight: '600' }}>Spoof Sender:</label>
                      <select style={{ width: '100%', fontSize: '13px' }} value={spoofSender} onChange={(e) => setSpoofSender(e.target.value)}>
                        <option value="Alice">Alice</option>
                        <option value="Bob">Bob</option>
                        <option value="Charlie">Charlie</option>
                      </select>
                    </div>
                    <div>
                      <label style={{ fontSize: '12px', color: '#94A3B8', fontWeight: '600' }}>Target Recipient:</label>
                      <select style={{ width: '100%', fontSize: '13px' }} value={spoofRecipient} onChange={(e) => setSpoofRecipient(e.target.value)}>
                        <option value="Bob">Bob</option>
                        <option value="Alice">Alice</option>
                        <option value="Charlie">Charlie</option>
                      </select>
                    </div>
                  </div>

                  <div style={{ marginBottom: '12px' }}>
                    <label style={{ fontSize: '12px', color: '#94A3B8', fontWeight: '600' }}>Cipher Type:</label>
                    <select style={{ width: '100%', fontSize: '13px' }} value={spoofCipherType} onChange={(e) => setSpoofCipherType(e.target.value)}>
                      <option value="RSA">🔑 RSA Asymmetric</option>
                      <option value="Caesar">Caesar Shift</option>
                      <option value="Vigenère">Vigenère</option>
                      <option value="ROT13">ROT13</option>
                    </select>
                  </div>

                  <div style={{ marginBottom: '12px' }}>
                    <label style={{ fontSize: '12px', color: '#94A3B8', fontWeight: '600' }}>Shift / Key:</label>
                    <input type="text" style={{ width: '100%', fontSize: '13px' }} value={spoofKey} onChange={(e) => setSpoofKey(e.target.value)} />
                  </div>

                  <div style={{ marginBottom: '16px' }}>
                    <label style={{ fontSize: '12px', color: '#94A3B8', fontWeight: '600' }}>Spoofed Message Content:</label>
                    <input type="text" placeholder="e.g. TRANSFER $10,000 IMMEDIATELY" style={{ width: '100%', fontSize: '13px' }} value={spoofText} onChange={(e) => setSpoofText(e.target.value)} />
                  </div>

                  <button type="submit" className="btn-danger" style={{ width: '100%', justifyContent: 'center' }}>
                    Inject Spoofed Message
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
