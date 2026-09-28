# 🔐 Crypto Chat Lab: Interactive Cryptographic Messaging & MITM Workbench

An educational, full-stack cryptographic messaging laboratory and cryptanalysis suite designed for modern cybersecurity, computer science, and cryptography masterclasses.

This application allows participants to experiment hands-on with both **Symmetric Ciphers** (Caesar, Vigenère, ROT13) and **Asymmetric Public-Key Cryptography** (RSA-1024/educational prime keypairs), while simultaneously demonstrating **Passive Eavesdropping** (Wiretap), **Active Man-in-the-Middle (MITM) Interception**, **Payload Tampering**, **Identity Spoofing**, and **Automated Cryptanalysis** (Chi-Squared Frequency Analysis & Fermat's RSA Modulus Factorization).

---

## 📋 Table of Contents
1. [Key Features](#-key-features)
2. [Cryptographic Architecture](#-cryptographic-architecture)
3. [System Requirements](#-system-requirements)
4. [Quick Start Installation & Scripts](#-quick-start-installation--scripts)
   - [macOS & Linux (`./start.sh`)](#1-macos--linux)
   - [Windows Command Prompt (`start.bat`)](#2-windows-command-prompt)
   - [Windows PowerShell (`start.ps1`)](#3-windows-powershell)
   - [Universal Cross-Platform Python Launcher (`start_lab.py`)](#4-universal-cross-platform-python-launcher)
6. [Classroom Centralized Server Setup (LAN / Wi-Fi)](#-classroom-centralized-server-setup-lan--wi-fi)
7. [Remote Access via Ngrok Tunneling & WSS (WebSocket Secure)](#-remote-access-via-ngrok-tunneling--wss-websocket-secure)
8. [Multi-Protocol Architecture: MQTT Broker & Packet Sniffing](#-multi-protocol-architecture-mqtt-broker--packet-sniffing)
9. [Hands-On Classroom Instruction Scenarios](#-hands-on-classroom-instruction-scenarios)
   - [Scenario 1: Breaking Caesar Shift via Chi-Squared Analysis](#scenario-1-breaking-caesar-shift-via-chi-squared-frequency-analysis)
   - [Scenario 2: The Polyalphabetic Illusion (Vigenère)](#scenario-2-the-polyalphabetic-illusion-vigenère)
   - [Scenario 3: Asymmetric RSA Key Exchange & Fermat Factorization](#scenario-3-asymmetric-rsa-key-exchange--fermat-factorization)
   - [Scenario 4: Active In-Flight MITM Tampering](#scenario-4-active-in-flight-mitm-tampering)
   - [Scenario 5: Packet Spoofing & Identity Impersonation](#scenario-5-packet-spoofing--identity-impersonation)
   - [Scenario 6: Centralized Classroom Group Broadcast](#scenario-6-centralized-classroom-group-broadcast)
   - [Scenario 7: Remote MQTT Packet Sniffing & External Node Injection](#scenario-7-remote-mqtt-packet-sniffing--external-node-injection)
10. [Mathematical Rigor & Ground Truth Verification](#-mathematical-rigor--ground-truth-verification)
11. [Troubleshooting & Network FAQ](#-troubleshooting--network-faq)

---

## ⚡ Key Features

- **Dual Operation Modes**:
  - **Local Solo Mode**: Run everything on a single laptop using multiple browser tabs or split-screen windows.
  - **Centralized Classroom LAN Mode**: The instructor (or a student host) runs the server on their laptop, and all classroom participants connect over local Wi-Fi to chat and intercept in real-time.
- **Dynamic Group Broadcast & 1-1 Channels**:
  - `📢 Classroom Broadcast`: Group chat room accessible to all participants on the server.
  - `1-1 Channels`: Direct end-to-end peer channels between any connected students.
- **Live Wiretap (Passive Adversary)**:
  - Captures raw wireframe packets, timestamps, senders, recipients, and ciphertext in real-time.
- **Active In-Flight MITM Interception**:
  - Freezes transmissions mid-flight in an inspection queue. The instructor can **Release**, **Tamper** (modify payload), or **Drop** packets.
- **Automated Cryptanalysis Engine**:
  - **Chi-Squared ($\chi^2$) Frequency Analysis**: Automatically computes letter frequencies against the English standard alphabet to instantly break Caesar shift ciphers.
  - **Fermat's Factorization ($N = a^2 - b^2$)**: Automatically cracks weak RSA moduli where primes $p$ and $q$ are close, recovering private exponent $d$ in milliseconds.
- **Dynamic RSA Public Key Directory**:
  - When participants generate RSA keypairs, their public keys are automatically synchronized across all connected clients via WebSockets.

---

## 🏗 Cryptographic Architecture

```
                          [ CENTRALIZED NODE.JS SERVER ]
                            Listening on 0.0.0.0:3005
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            │                          │                          │
            ▼                          ▼                          ▼
    [ Student: Alice ]         [ Student: Bob ]        [ Instructor: Dr. Smith ]
    ┌────────────────┐         ┌────────────────┐      ┌─────────────────────────┐
    │ Encrypt:       │         │ Encrypt:       │      │ • Passive Wiretap Log   │
    │  - Caesar      │         │  - Caesar      │      │ • Active MITM Queue     │
    │  - Vigenère    │◄───────►│  - Vigenère    │◄────►│ • In-Flight Tampering   │
    │  - RSA Asymm   │ WebSocket  - RSA Asymm   │      │ • Identity Spoofing     │
    │  - Group Cast  │ Channel │  - Group Cast  │      │ • Chi^2 & Fermat Cracker│
    └────────────────┘         └────────────────┘      └─────────────────────────┘
```

---

## 💻 System Requirements

- **Operating System**: macOS (10.15+), Windows (10/11), or Linux (Ubuntu, Debian, Fedora, Arch, etc.)
- **Node.js**: Version **v18.0.0** or higher (`node -v`)
- **NPM**: Version **v9.0.0** or higher (`npm -v`)
- **Network**: Local localhost or shared Wi-Fi / Local Area Network (LAN)
- **Web Browser**: Any modern browser (Google Chrome, Mozilla Firefox, Apple Safari, Microsoft Edge)

---

## 🚀 Quick Start Installation & Scripts

We have provided ready-to-run, automated startup scripts for all major operating systems. These scripts automatically check for Node.js, install dependencies, compile the production React bundle, detect your local IP address, and launch the server.

### 1. macOS & Linux

Open your terminal and run:

```bash
# Navigate to the lab folder
cd crypto-chat-lab

# Run the automated launch script
./start.sh
```

*Note: If permissions are needed, run `chmod +x start.sh` first.*

**Manual Command Line Alternative (macOS/Linux):**
```bash
cd crypto-chat-lab
npm install
npm run build
node server.js
```

---

### 2. Windows Command Prompt

Double-click `start.bat` in File Explorer, or run in Command Prompt (`cmd.exe`):

```cmd
cd crypto-chat-lab
start.bat
```

---

### 3. Windows PowerShell

Open PowerShell and execute:

```powershell
cd crypto-chat-lab
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

---

### 4. Universal Cross-Platform Python Launcher

If Python 3 is installed on your computer (macOS, Windows, or Linux):

```bash
cd crypto-chat-lab
python3 start_lab.py
```

Once started, the terminal will display:
```
=============================================================
🚀 CRYPTO CHAT LAB BACKEND ACTIVE & LISTENING ON 0.0.0.0:3005
👉 Local:              http://localhost:3005
🌐 Classroom LAN (en0): http://192.168.1.105:3005
📢 Centralized Server Ready: Share the Classroom LAN URL with all participants!
=============================================================
```

Open your browser to: **`http://localhost:3005`**

---

## 🌐 Classroom Centralized Server Setup (LAN / Wi-Fi)

To host a live workshop where **all participants chat and interact with each other over your machine**:

### Step 1: Ensure Everyone is on the Same Wi-Fi Network
- Connect your computer and your participants' laptops or tablets to the **same Wi-Fi network** or a smartphone personal hotspot.

### Step 2: Start the Server on the Instructor/Host Machine
Run `./start.sh` (macOS/Linux) or `start.bat` (Windows). The server automatically binds to `0.0.0.0:3005` and announces your machine's LAN IP address, for example:
```
http://192.168.1.105:3005
```

### Step 3: Share the URL with Participants
- Direct students to open **`http://192.168.1.105:3005`** (replace with your host IP) in their browser.
- Participants can click **"Join as Custom Participant"**, type their name (e.g., *Charlie*, *Sarah*, *Dave*), and hit **Join Classroom**.
- The host clicks **"Launch MITM Dashboard"** to monitor all traffic, execute attacks, and demonstrate packet manipulation.

### Step 4: Group Chat vs. 1-1 Channels
- In the **Chat Destination** dropdown:
  - Choosing **`📢 Classroom Broadcast (All Participants)`** transmits the message to every student in the room.
  - Choosing a classmate's name establishes a private **1-1 end-to-end encrypted channel** between those two students.

---

## 🌐 Remote Access via Ngrok Tunneling & WSS (WebSocket Secure)

When hosting workshops across different physical locations, or when your classroom Wi-Fi enforces **NAT / Client Isolation** (which prevents participants from opening `http://192.168.x.x:3005`), you can instantly expose your local server securely to the internet using **ngrok tunneling**.

### Why Ngrok + WSS?
1. **Zero Firewall & Router Config**: Bypasses NATs, CGNAT, firewalls, and corporate proxies without port forwarding.
2. **Instant HTTPS & WSS**: Provides valid TLS certificates (`https://*.ngrok-free.app`), allowing browsers to establish secure WebSockets (`wss://`).
3. **Remote Participation**: Anyone in the world can connect from laptops, iPads, or smartphones simply by opening your ngrok URL.
4. **Auto-Discovery**: The lab server automatically detects running ngrok tunnels via `http://127.0.0.1:4040` and broadcasts the public link directly into the UI!

### How to Launch Ngrok Tunnel:

#### Method A: Using the Automated Script
In a separate terminal window on the host machine:
```bash
# macOS / Linux
./ngrok_tunnel.sh

# Windows
ngrok_tunnel.bat
```

#### Method B: Manual CLI Command
```bash
ngrok http 3005
```

Ngrok will initialize a forwarding tunnel:
```
Forwarding                    https://a1b2-c3d4.ngrok-free.app -> http://localhost:3005
Web Interface                 http://127.0.0.1:4040
```

### How Remote Clients Connect:
1. **Direct Web Access**:
   Share `https://a1b2-c3d4.ngrok-free.app` with remote students. They can open it directly in any browser.
2. **Dynamic Client Switching**:
   If a participant already has the web app open (e.g. on Firebase Hosting `https://crypto-masterclass-2026.web.app/` or another computer):
   - Click the **"Server: Localhost:3005"** status badge in the top navigation bar.
   - Enter your ngrok HTTPS endpoint: `https://a1b2-c3d4.ngrok-free.app`
   - Click **"Connect"** — Socket.IO immediately establishes a secure **WSS** connection to your machine!
3. **Real-Time Traffic Inspection**:
   Open `http://127.0.0.1:4040` on the instructor machine to observe raw HTTP/WSS headers, payloads, and latency.

---

## 📡 Multi-Protocol Architecture: MQTT Broker & Packet Sniffing

To demonstrate real-world IoT, industrial control, and machine-to-machine cryptography, the server includes an **embedded Aedes MQTT Broker**:
- **TCP Port `1883`**: Standard MQTT TCP transport for Python scripts, Mosquitto CLI, embedded microcontrollers (ESP32/Arduino), and servers.
- **WebSocket Path `/mqtt` (Port 3005 or WSS via ngrok)**: High-speed MQTT over WebSockets for browser clients and cloud apps.
- **Bi-Directional Bridging**: Messages sent via WebSockets automatically bridge into MQTT topics, and external MQTT publications bridge into student chat feeds and the instructor wiretap!

### MQTT Topic Directory:
| Topic | Purpose | Payload Format |
| :--- | :--- | :--- |
| `crypto/classroom/broadcast` | Classroom broadcast channel | JSON: `{"sender","recipient","ciphertext","cipherType","key"}` |
| `crypto/direct/<recipient>` | Direct 1-1 peer encrypted message | JSON payload targeted at `<recipient>` |
| `crypto/wiretap` | Global eavesdropping stream | All encrypted packets passing through the server |
| `crypto/#` | Wildcard pattern | Captures all course traffic across every topic |

### Educational MQTT Tools Included:

#### 1. Real-Time Packet Sniffer (`mqtt_sniffer.py`)
Run an external wire sniffer in a separate terminal:
```bash
# Requires paho-mqtt: pip install paho-mqtt
python3 mqtt_sniffer.py
```
This tool listens on `crypto/#` and prints decoded packet headers, cipher types, ciphertext, and tampering/spoofing alerts as packets traverse the wire.

#### 2. External Message Publisher (`mqtt_publisher.py`)
Inject cryptographic messages directly into the classroom from Python:
```bash
# Send Caesar ciphered message to the whole class
python3 mqtt_publisher.py --sender "PythonNode_1" --cipher caesar --shift 5 --message "CRITICAL ALERT FROM IOT GATEWAY"

# Send Vigenère ciphered message to Alice
python3 mqtt_publisher.py --sender "Sensor_Hub" --recipient "Alice" --cipher vigenere --key "SHIELD" --message "TEMPERATURE EXCEEDED"
```

#### 3. Mosquitto CLI Integration
If you have `mosquitto-clients` installed (`brew install mosquitto` or `apt install mosquitto-clients`):
```bash
# Eavesdrop on classroom broadcast
mosquitto_sub -h localhost -p 1883 -t "crypto/classroom/broadcast" -v

# Inject raw message into wiretap
mosquitto_pub -h localhost -p 1883 -t "crypto/classroom/broadcast" -m '{"sender":"HackerCLI","recipient":"Classroom Broadcast","ciphertext":"KHOOR","cipherType":"Caesar","key":"3"}'
```

---

## 🧪 Hands-On Classroom Instruction Scenarios

### Scenario 1: Breaking Caesar Shift via Chi-Squared Frequency Analysis
**Cryptographic Principle**: *Small key space ($K = 26$) & monoalphabetic letter frequency leakage.*

1. **Student Setup**:
   - Alice selects **Chat Destination**: `📢 Classroom Broadcast` (or `Student Bob`).
   - Selects **Cipher**: `Caesar Shift Cipher (Symmetric)`.
   - Sets **Shift Key**: `7`.
   - Sends: `"THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AND ATTACKS AT MIDNIGHT"`
   - Ciphertext generated: `AOL XBPJR IYVDU MVE QBTWZ VCLY AOL SHGF KVN HUK HAAHARZ HA TPKUPNOA`
2. **Instructor Interception**:
   - The instructor opens the **Wiretap Transmissions** table and locates Alice's packet.
   - Clicks **"Crack Cipher"**.
3. **Observation**:
   - The Automated Cryptanalysis engine tests all 26 shift values, calculates the $\chi^2$ statistic against English unigram frequencies, identifies Key `7` with the lowest error score, and reconstructs the plaintext in milliseconds.
   - **Takeaway**: Why Caesar provides zero confidentiality in the modern era.

---

### Scenario 2: The Polyalphabetic Illusion (Vigenère)
**Cryptographic Principle**: *Multi-alphabet shifts flatten simple frequency distributions but remain vulnerable to periodic Kasiski analysis.*

1. **Student Setup**:
   - Alice selects **Cipher**: `Vigenère Polyalphabetic (Symmetric)`.
   - Sets **Keyword**: `CRYPTO`.
   - Sends: `"DEFEND THE EAST WALL AT DAWN"`
   - Ciphertext generated: `FVDUFR KVV VYLM NYNN NF UYKM`
2. **Instructor Action**:
   - Inspect the wire log. Notice that letter frequency is obscured because the same plaintext letter (e.g., `'E'`) maps to multiple different ciphertext letters depending on its alignment with `C-R-Y-P-T-O`.
   - Demonstrate that if the key length is short and reused, the cipher degrades into parallel Caesar ciphers.

---

### Scenario 3: Asymmetric RSA Key Exchange & Fermat Factorization
**Cryptographic Principle**: *Asymmetric cryptography eliminates the shared secret distribution problem, but weak prime generation ($p \approx q$) allows rapid modulus factorization.*

1. **Student Setup**:
   - Bob selects his profile and views **My RSA Keypair**:
     - Public Key $(N, e)$: Modulus $N$, Exponent $e = 65537$ (or $3$).
     - Private Key $d$: Held strictly on Bob's client.
   - Alice selects **Chat Destination**: `Student Bob`.
   - Alice selects **Cipher**: `🔑 RSA Asymmetric`.
   - Alice enters: `"SECRET PASSCODE 9942"` and clicks **Encrypt & Transmit**.
   - The payload sent over the wire is encrypted with Bob's Public Key:
     $$C = M^e \pmod N$$
2. **Instructor Cryptanalysis**:
   - The instructor intercepts the frame starting with `RSA-CIPHER:...`.
   - Clicks **"Crack Cipher"**.
   - The engine executes **Fermat's Factorization Method**:
     $$N = a^2 - b^2 = (a - b)(a + b) = p \times q$$
   - Since $p$ and $q$ are within close proximity, the factor search completes almost instantly, discovering:
     $$\phi(N) = (p - 1)(q - 1)$$
     $$d \equiv e^{-1} \pmod{\phi(N)}$$
   - The instructor recovers the private key $d$ and reads the plaintext without Bob's permission!
   - **Takeaway**: Why production RSA mandates 2048-bit or 4096-bit randomly generated primes that are mathematically distant.

---

### Scenario 4: Active In-Flight MITM Tampering
**Cryptographic Principle**: *Encryption alone does NOT guarantee Integrity. Without MACs or Digital Signatures, ciphertext can be altered in transit.*

1. **Instructor Action**:
   - In the MITM Control Center, toggle **Enable Active Intercept Queue** to **ON**.
2. **Student Action**:
   - Alice types to Bob: `"TRANSFER $100 TO ACCOUNT 551"`.
   - Hits **Encrypt & Transmit**.
   - Notice that the message **does not arrive** at Bob's screen!
3. **Instructor Action**:
   - In the **In-Flight Interception Queue**, Alice's message is held.
   - In the tamper field, the instructor modifies the text to: `"TRANSFER $999999 TO ACCOUNT HACKER"`.
   - Clicks **"Tamper"**.
4. **Bob's Screen**:
   - Bob receives the message with a prominent warning:
     `⚠️ Tampered in Transit (MITM Injection)`.
   - **Takeaway**: Why modern systems use Authenticated Encryption (AES-GCM) and Digital Signatures (ECDSA / Ed25519) to detect bit-flipping and tampering.

---

### Scenario 5: Packet Spoofing & Identity Impersonation
**Cryptographic Principle**: *Without Authenticity guarantees, an attacker on the network can forge packets from any sender.*

1. **Instructor Action**:
   - In the **Packet Impersonation (Spoofing)** card:
   - Sets **Spoof Sender**: `Alice` (or `Instructor`).
   - Sets **Target Recipient**: `📢 Classroom Broadcast` (or `Student Bob`).
   - Sets **Message Content**: `"CLASS CANCELLED - EVERYONE GETS AN A+"`.
   - Clicks **Inject Forged Packet**.
2. **Classroom Screen**:
   - Every student receives the broadcast appearing to originate from `Alice`.
   - The client displays: `⚠️ Unverified Sender (Impersonation Detected)`.
   - **Takeaway**: Demonstrates why Public Key Infrastructure (PKI) and Digital Signatures are mandatory to prove sender identity.

---

### Scenario 6: Centralized Classroom Group Broadcast
**Cryptographic Principle**: *Multi-party classroom interaction over shared wireless network.*

1. The host sets up the central server on their laptop.
2. 5–30 students join the URL `http://<HOST-IP>:3005` (or via the ngrok public HTTPS/WSS URL).
3. Everyone chooses **`📢 Classroom Broadcast`**.
4. The instructor challenges the class:
   > *"I have broadcast an encrypted Caesar ciphertext with an unknown key to the classroom channel. The first student to factor or crack the shift and reply in plaintext wins!"*
5. Students practice cryptanalysis live in the classroom.

---

### Scenario 7: Remote MQTT Packet Sniffing & External Node Injection
**Cryptographic Principle**: *Cross-protocol interception (M2M/IoT) and wire vulnerability in unauthenticated broker architectures.*

1. **Passive MQTT Wire Sniffer**:
   - In a terminal, run: `python3 mqtt_sniffer.py --topic "crypto/#"`
   - A student on the web interface sends an encrypted message (e.g. Caesar or RSA).
   - Notice the packet immediately appears in the Python terminal in real-time, showing how an attacker on the same network or with broker access can eavesdrop on machine-to-machine streams.
2. **External IoT Injection**:
   - In another terminal, run:
     ```bash
     python3 mqtt_publisher.py --sender "IoT_Telemetry_Bot" --cipher caesar --shift 4 --message "ALERT: SENSOR TAMPERING DETECTED"
     ```
   - Watch the web client: The message arrives in the classroom broadcast with the `[MQTT]` protocol badge!
   - In the MITM Dashboard, the instructor can inspect, tamper with, or crack the cipher just like any browser client.
   - **Takeaway**: Modern cryptographic systems must secure transport across all protocols (WebSockets, WSS, MQTT, TCP) using TLS and end-to-end payload cryptography.

---

## 📐 Mathematical Rigor & Ground Truth Verification

| Algorithm | Formula / Mechanism | Key Parameter | Attack Vector in Lab |
| :--- | :--- | :--- | :--- |
| **Caesar Cipher** | $C_i = (P_i + k) \pmod{26}$ | Shift $k \in [0, 25]$ | Brute-force & Chi-Squared Frequency Analysis ($\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$) |
| **Vigenère Cipher** | $C_i = (P_i + K_{i \bmod m}) \pmod{26}$ | Polyalphabetic string key $K$ | Periodicity deduction & letter frequency flattening |
| **ROT13** | $C_i = (P_i + 13) \pmod{26}$ | Fixed shift $k = 13$ | Involution ($D(D(M)) = M$), zero cryptographic security |
| **Educational RSA** | $C = M^e \pmod N$, $M = C^d \pmod N$ | Modulus $N = p \times q$, $e = 65537$ | Fermat's Difference of Squares: $N = a^2 - b^2 \Rightarrow (a-b)(a+b)$ |
| **Active MITM** | In-flight socket interception & payload rewrite | Network positioning | Demonstrates lack of Authenticated Encryption (HMAC / AES-GCM) |
| **Spoofing** | Forged sender header injection | Network layer trust | Demonstrates absence of Asymmetric Digital Signatures |

---

## 🛠 Troubleshooting & Network FAQ

#### Q1: "Port 3005 is already in use"
**Fix**: Specify an alternate port when running:
```bash
PORT=3005 ./start.sh
# or on Windows
set PORT=3005 && node server.js
```

#### Q2: "Participants cannot open the URL on their laptops"
1. **Firewall**: Check if your host OS firewall is blocking incoming connections on port 3005.
   - **macOS**: System Settings → Network → Firewall → Allow Node.js.
   - **Windows**: Windows Defender Firewall → Allow an app through firewall → Allow Node.js on Private Networks.
2. **Wi-Fi AP Isolation**: Some university/enterprise Wi-Fi networks block client-to-client communication for security.
   - **Solution**: Turn on your smartphone's **Personal Hotspot**, connect the instructor laptop and participant laptops to the hotspot. The server will work seamlessly!

#### Q3: "Do students need to install Node.js?"
**No!** Only the host machine running the server needs Node.js. All participants simply open their web browser (Chrome, Safari, Firefox, Edge) to the host machine's IP address.

#### Q4: "How do I run in development mode with hot-reloading?"
```bash
cd crypto-chat-lab
npm run dev
```
Vite will start the client dev server on `http://localhost:3000` with hot-reloading, proxying socket connections to the backend on port 3005.

---

## 📜 Academic Standards Reference

- **NIST SP 800-57 Part 1 Rev. 5**: Recommendation for Key Management.
- **RFC 3447**: Public-Key Cryptography Standards (PKCS) #1: RSA Cryptography Specifications.
- **Kerckhoffs's Principle (1883)**: A cryptosystem should be secure even if everything about the system, except the key, is public knowledge.
- **Dolev-Yao Threat Model (1983)**: Network adversary can eavesdrop, intercept, tamper, and inject arbitrary messages.

---
*Created for CS-4XX: Modern Cryptography & Network Security Course (2026).*
