import { io } from 'socket.io-client';
import { spawn } from 'child_process';
import { 
  caesarEncrypt, caesarDecrypt, vigenereEncrypt, vigenereDecrypt, 
  generateRSAKeyPair, rsaEncrypt, rsaDecrypt, crackRSAModulus, autoBreakCipher 
} from './src/utils/cryptoUtils.js';

const SERVER_URL = 'http://127.0.0.1:3005';

// ANSI Colors
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const CYAN = '\x1b[36m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RED = '\x1b[31m';
const MAGENTA = '\x1b[35m';
const BLUE = '\x1b[34m';

function log(prefix, color, message) {
  console.log(`${color}${BOLD}[${prefix}]${RESET} ${message}`);
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ---------------------------------------------------------------------------
// Agent Base Class
// ---------------------------------------------------------------------------
class ChatAgent {
  constructor(name, role) {
    this.name = name;
    this.role = role;
    this.socket = null;
    this.rsaKeys = role === 'student' ? generateRSAKeyPair(true) : null;
    this.receivedMessages = [];
    this.wireLogs = [];
    this.interceptQueue = [];
    this.publicDirectory = {};
    this.activeUsers = [];
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.socket = io(SERVER_URL, {
        transports: ['websocket'],
        reconnection: false,
        timeout: 5000
      });

      this.socket.on('connect', () => {
        log(this.name, CYAN, `Connected to server (Socket ID: ${this.socket.id})`);
        this.socket.emit('register-user', {
          username: this.name,
          role: this.role,
          publicKey: this.rsaKeys ? this.rsaKeys.publicKey : null
        });
        resolve();
      });

      this.socket.on('connect_error', (err) => {
        reject(err);
      });

      this.socket.on('receive-message', (msg) => {
        this.receivedMessages.push(msg);
        log(this.name, GREEN, `Received message ${msg.id} from ${msg.sender}: "${msg.ciphertext.substring(0, 40)}..." [Status: ${msg.status}]`);
      });

      this.socket.on('public-directory-update', (dir) => {
        this.publicDirectory = { ...this.publicDirectory, ...dir };
      });

      this.socket.on('active-users-update', (users) => {
        this.activeUsers = users;
      });

      if (this.role === 'instructor') {
        this.socket.on('new-wire-log', (logItem) => {
          this.wireLogs.unshift(logItem);
          log(this.name, MAGENTA, `Wiretap Intercept [${logItem.id}]: ${logItem.sender} -> ${logItem.recipient} (${logItem.cipherType})`);
        });

        this.socket.on('queue-update', (queue) => {
          this.interceptQueue = queue;
          log(this.name, YELLOW, `In-Flight Intercept Queue updated: ${queue.length} packets pending approval`);
        });
      }
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      log(this.name, BLUE, 'Disconnected');
    }
  }

  sendMessage({ recipient, ciphertext, cipherType, key, isBroadcast, rsaPublicKey, plaintextSent }) {
    this.socket.emit('send-message', {
      sender: this.name,
      recipient,
      ciphertext,
      cipherType,
      key,
      isBroadcast,
      rsaPublicKey,
      plaintextSent
    });
  }
}

// ---------------------------------------------------------------------------
// Master Test Orchestrator
// ---------------------------------------------------------------------------
async function runAllScenarios() {
  console.log('\n' + '='.repeat(80));
  console.log(`${CYAN}${BOLD}       🔐 CRYPTO CHAT LAB · MULTI-AGENT VERIFICATION HARNESS${RESET}`);
  console.log(`${CYAN}${BOLD}     Testing Scenarios 1-7 from README.md with Live Agents${RESET}`);
  console.log('='.repeat(80) + '\n');

  // Step 1: Verify API endpoint
  log('SETUP', BLUE, 'Testing API Network Info endpoint...');
  try {
    const netRes = await fetch(`${SERVER_URL}/api/network-info`);
    if (!netRes.ok) throw new Error(`HTTP ${netRes.status}`);
    const netData = await netRes.json();
    log('SETUP', GREEN, `✓ Network info retrieved: Port ${netData.port}, MQTT Port ${netData.mqttTcpPort}`);
  } catch (err) {
    log('SETUP', RED, `❌ Failed to connect to ${SERVER_URL}: ${err.message}`);
    process.exit(1);
  }

  // Step 2: Initialize Agents
  log('SETUP', BLUE, 'Spawning agents: Server Master, Participant A (Alice), Participant B (Bob), Participant C (Charlie)...');
  const serverMaster = new ChatAgent('Instructor_Dr_Smith', 'instructor');
  const participantA = new ChatAgent('Alice', 'student');
  const participantB = new ChatAgent('Bob', 'student');
  const participantC = new ChatAgent('Charlie', 'student');

  await serverMaster.connect();
  await participantA.connect();
  await participantB.connect();
  await participantC.connect();

  await delay(600);
  log('SETUP', GREEN, `✓ All 4 agents connected and registered in active directory!`);
  console.log(`  Active users count: ${serverMaster.activeUsers.length}`);
  console.log(`  Public RSA Directory keys: ${Object.keys(participantA.publicDirectory).join(', ')}\n`);

  let testFailures = 0;

  // -------------------------------------------------------------------------
  // Scenario 1: Breaking Caesar Shift via Chi-Squared Frequency Analysis
  // -------------------------------------------------------------------------
  console.log('-'.repeat(80));
  log('SCENARIO 1', CYAN, 'Breaking Caesar Shift via Chi-Squared Frequency Analysis');
  console.log('-'.repeat(80));

  const s1Plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AND ATTACKS AT MIDNIGHT";
  const s1Shift = 7;
  const s1Ciphertext = caesarEncrypt(s1Plaintext, s1Shift);
  const expectedS1Cipher = "AOL XBPJR IYVDU MVE QBTWZ VCLY AOL SHGF KVN HUK HAAHJRZ HA TPKUPNOA";

  if (s1Ciphertext === expectedS1Cipher) {
    log('Alice', GREEN, `✓ Caesar encryption matches README exact expected ciphertext:\n  "${s1Ciphertext}"`);
  } else {
    log('Alice', RED, `❌ Ciphertext mismatch! Got "${s1Ciphertext}", expected "${expectedS1Cipher}"`);
    testFailures++;
  }

  // Alice broadcasts to Classroom
  participantA.sendMessage({
    recipient: 'Classroom Broadcast',
    ciphertext: s1Ciphertext,
    cipherType: 'Caesar',
    key: String(s1Shift),
    isBroadcast: true,
    plaintextSent: s1Plaintext
  });

  await delay(600);

  // Instructor intercepts and cracks cipher
  const s1Intercepted = serverMaster.wireLogs.find(l => l.ciphertext === s1Ciphertext);
  if (!s1Intercepted) {
    log('Instructor', RED, '❌ Scenario 1 wireframe not found in Instructor wire logs!');
    testFailures++;
  } else {
    log('Instructor', GREEN, `✓ Wireframe intercepted: ID ${s1Intercepted.id}`);
    const crackResult = autoBreakCipher(s1Intercepted.ciphertext, 'Caesar');
    log('Instructor', MAGENTA, `Automated Cryptanalysis output:`);
    console.log(`    Recovered Plaintext: "${crackResult.bestText}"`);
    console.log(`    Identified Key:      ${crackResult.bestKey}`);
    console.log(`    Chi-Square Score:    ${crackResult.score}`);

    if (crackResult.bestText === s1Plaintext && crackResult.bestKey.includes('Shift 7')) {
      log('Instructor', GREEN, `✓ SUCCESS: Caesar Shift 7 completely broken by Chi-Squared Cryptanalysis!`);
    } else {
      log('Instructor', RED, `❌ Cryptanalysis failed to recover shift 7.`);
      testFailures++;
    }
  }

  // -------------------------------------------------------------------------
  // Scenario 2: The Polyalphabetic Illusion (Vigenère)
  // -------------------------------------------------------------------------
  console.log('\n' + '-'.repeat(80));
  log('SCENARIO 2', CYAN, 'The Polyalphabetic Illusion (Vigenère)');
  console.log('-'.repeat(80));

  const s2Plaintext = "DEFEND THE EAST WALL AT DAWN";
  const s2Key = "CRYPTO";
  const s2Ciphertext = vigenereEncrypt(s2Plaintext, s2Key);
  const expectedS2Cipher = "FVDTGR VYC TTGV NYAE OV UYLG";

  if (s2Ciphertext === expectedS2Cipher) {
    log('Alice', GREEN, `✓ Vigenère encryption matches README exact expected ciphertext:\n  "${s2Ciphertext}"`);
  } else {
    log('Alice', RED, `❌ Ciphertext mismatch! Got "${s2Ciphertext}", expected "${expectedS2Cipher}"`);
    testFailures++;
  }

  participantA.sendMessage({
    recipient: 'Bob',
    ciphertext: s2Ciphertext,
    cipherType: 'Vigenère',
    key: s2Key,
    isBroadcast: false,
    plaintextSent: s2Plaintext
  });

  await delay(600);

  const bobS2Msg = participantB.receivedMessages.find(m => m.ciphertext === s2Ciphertext);
  if (bobS2Msg) {
    const bobDecrypted = vigenereDecrypt(bobS2Msg.ciphertext, s2Key);
    log('Bob', GREEN, `✓ Bob received 1-1 Vigenère packet and decrypted with key "${s2Key}": "${bobDecrypted}"`);
    if (bobDecrypted === s2Plaintext) {
      log('Bob', GREEN, `✓ SUCCESS: Vigenère transmission verified.`);
    } else {
      log('Bob', RED, `❌ Decrypted text does not match plaintext.`);
      testFailures++;
    }
  } else {
    log('Bob', RED, '❌ Bob did not receive Vigenère message from Alice.');
    testFailures++;
  }

  // -------------------------------------------------------------------------
  // Scenario 3: Asymmetric RSA Key Exchange & Fermat Factorization
  // -------------------------------------------------------------------------
  console.log('\n' + '-'.repeat(80));
  log('SCENARIO 3', CYAN, 'Asymmetric RSA Key Exchange & Fermat Factorization');
  console.log('-'.repeat(80));

  const s3Plaintext = "SECRET PASSCODE 9942";
  log('Bob', BLUE, `Bob's RSA Public Key: N=0x${participantB.rsaKeys.publicKey.N}, e=0x${participantB.rsaKeys.publicKey.e}`);
  log('Bob', BLUE, `Bob's RSA Private Key: d=0x${participantB.rsaKeys.privateKey.d} (kept secret)`);

  const bobPubKey = participantA.publicDirectory['Bob'] || participantB.rsaKeys.publicKey;
  const s3Ciphertext = rsaEncrypt(s3Plaintext, bobPubKey);
  log('Alice', GREEN, `✓ Alice encrypted "${s3Plaintext}" with Bob's Public Key:`);
  console.log(`    Payload: ${s3Ciphertext}`);

  participantA.sendMessage({
    recipient: 'Bob',
    ciphertext: s3Ciphertext,
    cipherType: 'RSA',
    key: '',
    isBroadcast: false,
    rsaPublicKey: bobPubKey,
    plaintextSent: s3Plaintext
  });

  await delay(600);

  // Bob decrypts with his private key
  const bobS3Msg = participantB.receivedMessages.find(m => m.ciphertext === s3Ciphertext);
  if (bobS3Msg) {
    const bobRsaDecrypted = rsaDecrypt(bobS3Msg.ciphertext, participantB.rsaKeys.privateKey);
    log('Bob', GREEN, `✓ Bob decrypted with private key d: "${bobRsaDecrypted}"`);
    if (bobRsaDecrypted === s3Plaintext) {
      log('Bob', GREEN, `✓ Asymmetric end-to-end encryption verified!`);
    } else {
      log('Bob', RED, `❌ Bob's RSA decryption mismatch.`);
      testFailures++;
    }
  } else {
    log('Bob', RED, `❌ Bob did not receive RSA message.`);
    testFailures++;
  }

  // Instructor intercepts and cracks RSA modulus using Fermat's Factorization
  const s3Intercepted = serverMaster.wireLogs.find(l => l.ciphertext === s3Ciphertext);
  if (s3Intercepted) {
    log('Instructor', MAGENTA, `Intercepted RSA frame. Cracking modulus N via Fermat Factorization...`);
    const rsaCrack = crackRSAModulus(bobPubKey.N, bobPubKey.e, s3Ciphertext);
    console.log(`    Cracked Plaintext: "${rsaCrack.bestText}"`);
    console.log(`    Factored Info:     ${rsaCrack.bestKey}`);
    console.log(`    Error Score:       ${rsaCrack.score}`);

    if (rsaCrack.bestText === s3Plaintext) {
      log('Instructor', GREEN, `✓ SUCCESS: Weak RSA modulus factored & private key recovered via Fermat!`);
    } else {
      log('Instructor', RED, `❌ Fermat factorization failed to decrypt RSA ciphertext.`);
      testFailures++;
    }
  } else {
    log('Instructor', RED, `❌ RSA frame not found in wire logs.`);
    testFailures++;
  }

  // -------------------------------------------------------------------------
  // Scenario 4: Active In-Flight MITM Tampering
  // -------------------------------------------------------------------------
  console.log('\n' + '-'.repeat(80));
  log('SCENARIO 4', CYAN, 'Active In-Flight MITM Tampering');
  console.log('-'.repeat(80));

  // Instructor enables interception queue
  serverMaster.socket.emit('mitm-toggle-intercept', { enabled: true });
  await delay(300);
  log('Instructor', YELLOW, 'Active In-Flight Interception Queue toggled to ON.');

  // Alice sends payment order to Bob
  const s4Plaintext = "TRANSFER $100 TO ACCOUNT 551";
  const prevBobMsgCount = participantB.receivedMessages.length;

  participantA.sendMessage({
    recipient: 'Bob',
    ciphertext: s4Plaintext,
    cipherType: 'Plaintext',
    key: '',
    isBroadcast: false,
    plaintextSent: s4Plaintext
  });

  await delay(600);

  // Check that message did NOT arrive at Bob
  const bobHasNewMsg = participantB.receivedMessages.length > prevBobMsgCount;
  if (!bobHasNewMsg) {
    log('Bob', GREEN, `✓ Confirmed: Transmission FROZEN in-flight! (Bob did not receive message).`);
  } else {
    log('Bob', RED, `❌ Message leaked to Bob before approval!`);
    testFailures++;
  }

  // Instructor inspects held packet in queue
  if (serverMaster.interceptQueue.length === 0) {
    log('Instructor', RED, '❌ Intercept queue is empty!');
    testFailures++;
  } else {
    const heldItem = serverMaster.interceptQueue[0];
    log('Instructor', MAGENTA, `Held packet ID: ${heldItem.id} from ${heldItem.sender}: "${heldItem.ciphertext}"`);
    
    // Tamper text
    const tamperedPayload = "TRANSFER $999999 TO ACCOUNT HACKER";
    log('Instructor', YELLOW, `Tampering payload to: "${tamperedPayload}" and releasing packet...`);

    serverMaster.socket.emit('mitm-process-queued-message', {
      messageId: heldItem.id,
      action: 'TAMPER',
      tamperedCiphertext: tamperedPayload
    });

    await delay(600);

    const bobTamperedMsg = participantB.receivedMessages.find(m => m.id === heldItem.id);
    if (bobTamperedMsg) {
      log('Bob', GREEN, `✓ Bob received tampered message!`);
      console.log(`    Status:      ${bobTamperedMsg.status}`);
      console.log(`    isTampered:  ${bobTamperedMsg.isTampered}`);
      console.log(`    Content:     "${bobTamperedMsg.ciphertext}"`);

      if (bobTamperedMsg.isTampered === true && bobTamperedMsg.ciphertext === tamperedPayload) {
        log('Bob', GREEN, `✓ SUCCESS: Active MITM payload tampering and integrity violation verified!`);
      } else {
        log('Bob', RED, `❌ Tampered flags or content incorrect.`);
        testFailures++;
      }
    } else {
      log('Bob', RED, `❌ Bob did not receive released tampered message.`);
      testFailures++;
    }
  }

  // Reset intercept queue
  serverMaster.socket.emit('mitm-toggle-intercept', { enabled: false });
  await delay(300);

  // -------------------------------------------------------------------------
  // Scenario 5: Packet Spoofing & Identity Impersonation
  // -------------------------------------------------------------------------
  console.log('\n' + '-'.repeat(80));
  log('SCENARIO 5', CYAN, 'Packet Spoofing & Identity Impersonation');
  console.log('-'.repeat(80));

  const spoofedSender = "Alice";
  const spoofedContent = "CLASS CANCELLED - EVERYONE GETS AN A+";
  log('Instructor', MAGENTA, `Injecting forged broadcast packet appearing to originate from "${spoofedSender}"...`);

  serverMaster.socket.emit('mitm-impersonate', {
    spoofedSender,
    recipient: 'Classroom Broadcast',
    ciphertext: spoofedContent,
    cipherType: 'Plaintext',
    key: '',
    isBroadcast: true
  });

  await delay(600);

  const bobSpoofedMsg = participantB.receivedMessages.find(m => m.ciphertext === spoofedContent);
  const charlieSpoofedMsg = participantC.receivedMessages.find(m => m.ciphertext === spoofedContent);

  if (bobSpoofedMsg && charlieSpoofedMsg) {
    log('Bob', GREEN, `✓ Bob received spoofed broadcast from "${bobSpoofedMsg.sender}": "${bobSpoofedMsg.ciphertext}" (isSpoofed: ${bobSpoofedMsg.isSpoofed})`);
    log('Charlie', GREEN, `✓ Charlie received spoofed broadcast from "${charlieSpoofedMsg.sender}": "${charlieSpoofedMsg.ciphertext}" (isSpoofed: ${charlieSpoofedMsg.isSpoofed})`);
    if (bobSpoofedMsg.isSpoofed && bobSpoofedMsg.sender === 'Alice') {
      log('Ecosystem', GREEN, `✓ SUCCESS: Identity spoofing detected and highlighted with warnings.`);
    } else {
      log('Ecosystem', RED, `❌ Spoofed message flags invalid.`);
      testFailures++;
    }
  } else {
    log('Ecosystem', RED, `❌ Students did not receive spoofed broadcast.`);
    testFailures++;
  }

  // -------------------------------------------------------------------------
  // Scenario 6: Centralized Classroom Group Broadcast
  // -------------------------------------------------------------------------
  console.log('\n' + '-'.repeat(80));
  log('SCENARIO 6', CYAN, 'Centralized Classroom Group Broadcast');
  console.log('-'.repeat(80));

  const s6Plaintext = "CLASSROOM CHALLENGE: FACTOR 899";
  const s6Cipher = caesarEncrypt(s6Plaintext, 5);

  log('Charlie', CYAN, `Participant C (Charlie) broadcasting challenge to whole room: "${s6Cipher}"`);
  participantC.sendMessage({
    recipient: 'Classroom Broadcast',
    ciphertext: s6Cipher,
    cipherType: 'Caesar',
    key: '5',
    isBroadcast: true,
    plaintextSent: s6Plaintext
  });

  await delay(600);

  const aliceGotCast = participantA.receivedMessages.some(m => m.ciphertext === s6Cipher);
  const bobGotCast = participantB.receivedMessages.some(m => m.ciphertext === s6Cipher);

  if (aliceGotCast && bobGotCast) {
    log('Classroom', GREEN, `✓ SUCCESS: Both Alice & Bob received Charlie's group broadcast in real-time.`);
  } else {
    log('Classroom', RED, `❌ Not all participants received classroom broadcast.`);
    testFailures++;
  }

  // -------------------------------------------------------------------------
  // Scenario 7: Remote MQTT Packet Sniffing & External Node Injection
  // -------------------------------------------------------------------------
  console.log('\n' + '-'.repeat(80));
  log('SCENARIO 7', CYAN, 'Remote MQTT Packet Sniffing & External Node Injection');
  console.log('-'.repeat(80));

  // Launch external Python MQTT publisher
  log('MQTT_AGENT', BLUE, 'Executing python3 mqtt_publisher.py to inject IoT telemetry into classroom...');
  
  await new Promise((resolve) => {
    const py = spawn('python3', [
      'mqtt_publisher.py',
      '--sender', 'IoT_Telemetry_Bot',
      '--cipher', 'caesar',
      '--shift', '4',
      '--message', 'ALERT: SENSOR TAMPERING DETECTED'
    ], { stdio: 'pipe' });

    py.stdout.on('data', (d) => process.stdout.write(`    [Python stdout] ${d.toString()}`));
    py.stderr.on('data', (d) => process.stderr.write(`    [Python stderr] ${d.toString()}`));

    py.on('close', (code) => {
      log('MQTT_AGENT', code === 0 ? GREEN : RED, `Python publisher exited with code ${code}`);
      resolve();
    });
  });

  await delay(1000);

  // Verify MQTT packet bridged into WebSockets
  const mqttPacket = serverMaster.wireLogs.find(l => l.sender === 'IoT_Telemetry_Bot');
  if (mqttPacket) {
    log('ServerMaster', GREEN, `✓ SUCCESS: MQTT transmission bridged from TCP 1883 to WebSockets!`);
    console.log(`    Sender:    ${mqttPacket.sender}`);
    console.log(`    Cipher:    ${mqttPacket.cipherType}`);
    console.log(`    Wire:      ${mqttPacket.ciphertext}`);
    console.log(`    viaMqtt:   ${mqttPacket.viaMqtt}`);
  } else {
    log('ServerMaster', RED, `❌ MQTT packet not found in server wire logs!`);
    testFailures++;
  }

  // -------------------------------------------------------------------------
  // Teardown & Summary
  // -------------------------------------------------------------------------
  serverMaster.disconnect();
  participantA.disconnect();
  participantB.disconnect();
  participantC.disconnect();

  console.log('\n' + '='.repeat(80));
  if (testFailures === 0) {
    console.log(`${GREEN}${BOLD} 🎉 ALL 7 SCENARIOS VERIFIED SUCCESSFULLY WITH 4 ACTIVE AGENTS!${RESET}`);
    console.log(`${GREEN}   • Scenario 1: Caesar + Chi-Squared Cracker:    PASSED${RESET}`);
    console.log(`${GREEN}   • Scenario 2: Vigenère Polyalphabetic Cipher:   PASSED${RESET}`);
    console.log(`${GREEN}   • Scenario 3: RSA Key Exchange & Fermat Factor: PASSED${RESET}`);
    console.log(`${GREEN}   • Scenario 4: Active In-Flight MITM Tampering:  PASSED${RESET}`);
    console.log(`${GREEN}   • Scenario 5: Packet Spoofing & Impersonation:  PASSED${RESET}`);
    console.log(`${GREEN}   • Scenario 6: Classroom Multi-Party Broadcast:  PASSED${RESET}`);
    console.log(`${GREEN}   • Scenario 7: MQTT TCP Bridge & Python Ingest:  PASSED${RESET}`);
  } else {
    console.log(`${RED}${BOLD} ❌ COMPLETED WITH ${testFailures} FAILURES!${RESET}`);
    process.exit(1);
  }
  console.log('='.repeat(80) + '\n');
}

runAllScenarios().catch(err => {
  console.error('Test Harness Exception:', err);
  process.exit(1);
});
