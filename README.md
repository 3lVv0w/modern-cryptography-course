# 🎓 Modern Cryptography & Network Security Course Repository

**Level:** University CS-4XX / ECE-4XX Undergraduate & Graduate Level
**Format:** 4-Day Intensive Workshop (Theory Lectures + 3-Tier Hands-On Labs + Full-Stack Interactive Chat Suite)
**Live Masterclass Presentation:** [https://crypto-masterclass-2026.web.app](https://crypto-masterclass-2026.web.app)
**Live Interactive Lab Client:** [https://crypto-masterclass-2026.web.app/lab](https://crypto-masterclass-2026.web.app/lab)

---

## 📁 Repository Directory Structure

```text
modern-cryptography-course/
│
├── 📖 docs/                               # Supplementary Courseware & Theory Handbooks
│   ├── course_outline.md                  # Complete 4-Day Master Syllabus, Rubrics & Schedule
│   ├── real_world_stories.md              # Historical & Real-World Exploits (Enigma, Stuxnet, Dual_EC_DRBG)
│   ├── history_of_cryptography_and_enigma.md # History of classical ciphers and WW2 cryptanalysis
│   └── history_of_cryptography_and_enigma.pdf # Supplementary historical lecture PDF
│
├── 📝 assignments/                        # University Graded Assignments & Projects
│   ├── ASSIGNMENT_DAYS_1_TO_3.md          # Class Assignment Specification (Days 1–3: Theory, Labs & Exploits)
│   ├── assignment_days_1_to_3_student.py  # Student Code Starter Template & Local Test Suite
│   ├── REPORT_TEMPLATE.md                 # Formal Mathematical Proof & Attack Analysis Report
│   └── submit_check.py                    # Pre-flight Automated Validator, Hasher & Packager
│
├── 🖥️ presentation/                       # 53-Slide Interactive Masterclass Presentation
│   ├── cryptography_for_beginners_presentation.html # Source HTML presentation (TH/EN bilingual, theme toggle)
│   └── cryptography_for_beginners_presentation.pdf  # Compiled masterclass slide deck PDF (7.3 MB)
│
├── 🧪 day1/                               # DAY 1: Classical Cryptanalysis & Information Theory
│   ├── learning_material.md               # Lecture handbook & Shannon proof of Perfect Secrecy
│   ├── lab_student.py                     # 3-Tier Student Lab Notebook (Chi-Sq, IC, OTP, Crib Drag)
│   └── exercises_instructor.py            # Instructor solution & test verification suite
│
├── 🧪 day2/                               # DAY 2: Number Theory & Symmetric Encryption (AES)
│   ├── learning_material.md               # Lecture handbook (Z_n*, AES Galois Field Matrix, Block Modes)
│   ├── lab_student.py                     # 3-Tier Student Lab Notebook (Ext-GCD, AES-ECB flaw, AES-GCM)
│   └── exercises_instructor.py            # Instructor solution & test verification suite
│
├── 🧪 day3/                               # DAY 3: Public-Key Cryptography (DHKE, RSA & ECC)
│   ├── learning_material.md               # Lecture handbook (DHKE, RSA proofs, IND-CPA, Curve25519)
│   ├── lab_student.py                     # 3-Tier Student Lab Notebook (DHKE, RSA from scratch, Fermat attack)
│   └── exercises_instructor.py            # Instructor solution & test verification suite
│
├── 🧪 day4/                               # DAY 4: Integrity, Signatures, PKI & TLS 1.3
│   ├── learning_material.md               # Lecture handbook (Birthday paradox, Ed25519, TLS 1.3, PQC)
│   ├── lab_student.py                     # 3-Tier Student Lab Notebook (Avalanche effect, Cert chain, CTF)
│   └── exercises_instructor.py            # Instructor solution & test verification suite
│
├── 💬 crypto-chat-lab/                    # Full-Stack Cryptographic Messaging & MITM Workbench
│   ├── server.js                          # Node.js backend (Socket.IO + Embedded Aedes MQTT broker)
│   ├── src/                               # React frontend (Vite, Tailwind, Lucide, WebCrypto)
│   ├── start.sh / start.bat / start.ps1   # Platform-specific automated launchers
│   ├── start_lab.py                       # Cross-platform Python launcher
│   ├── ngrok_tunnel.sh / ngrok_tunnel.bat # Automated ngrok HTTPS & WSS tunnel launchers
│   ├── mqtt_sniffer.py                    # Real-time Python MQTT wiretap packet sniffer
│   ├── mqtt_publisher.py                  # Python MQTT message injector (Caesar, Vigenère, raw)
│   └── README.md                          # Full lab manual & 7 instructional scenarios
│
├── ⚙️ scripts/                             # Build & Generation Tooling
│   ├── build/                             # PDF compilation pipelines
│   │   ├── build_pdf_slides.py            # Slide deck PDF generator
│   │   └── build_cryptography_beginner_slides_pdf.py # Playwright rendering script
│   └── generators/                        # Slide generation & enhancement toolchain
│       ├── add_standards_and_references.py
│       ├── apply_full_bilingual_enhancement.py
│       ├── generate_thai_support.py
│       └── ...
│
├── 🚀 public/                             # Production Web Hosting Build (Firebase Hosting)
├── ⚙️ firebase.json                        # Firebase Hosting rules, headers & rewrites
└── 🛡️ .gitignore                          # Enterprise security rules (keys, credentials, caches)
```

---

## 🚀 Running Student Python Labs (Days 1–4)

Students can run their daily lab scripts directly from the terminal:

```bash
# Day 1 Lab: Classical Ciphers, Frequency Analysis & OTP
python3 day1/lab_student.py

# Day 2 Lab: Number Theory, AES Modes & GCM
python3 day2/lab_student.py

# Day 3 Lab: Diffie-Hellman Key Exchange & RSA Keygen
python3 day3/lab_student.py

# Day 4 Lab: SHA-256 Avalanche, X.509 PKI & Capstone CTF
python3 day4/lab_student.py
```

### 🎯 3-Tier Challenge System:

* 🟢 **LEVEL 1 (Novice):** Basic algorithm implementations & fundamentals.
* 🟡 **LEVEL 2 (Intermediate):** Statistical cryptanalysis, Index of Coincidence, AES pattern flaw checks, X.509 cert validation.
* 🔴 **LEVEL 3 (Hardcore):** Vigenère breaker, Two-Time Pad crib dragging, GCM nonce reuse exploit, Fermat RSA factorization attack, and Capstone CTF solver.

---

## 📝 Class Assignment (Days 1–3)

This class assignment synthesizes **Classical Cryptanalysis**, **Modern Symmetric AEAD**, and **Public-Key Cryptosystems**:

* **Full Specification:** [`assignments/ASSIGNMENT_DAYS_1_TO_3.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_DAYS_1_TO_3.md) | [🇹🇭 ฉบับภาษาไทย](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_DAYS_1_TO_3_TH.md)
* **Student Starter Code:** [`assignments/assignment_days_1_to_3_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_days_1_to_3_student.py)
* **Theory Report Template:** [`assignments/REPORT_TEMPLATE.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE.md) | [🇹🇭 เทมเพลตภาษาไทย](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_TH.md)

### 🏃 Quick Workflow for Students:

```bash
# 1. Complete implementation functions in:
#    assignments/assignment_days_1_to_3_student.py

# 2. Run local automated test suite:
python3 assignments/assignment_days_1_to_3_student.py

# 3. Write mathematical derivations & proofs in:
#    assignments/REPORT.md (copied from REPORT_TEMPLATE.md)

# 4. Run automated pre-flight validator, integrity hasher & packager:
python3 assignments/submit_check.py --student-id "65070001" --name "Jane Doe"
```

The validator runs all unit tests, verifies report completeness, calculates SHA-256 integrity checksums, and produces `submission_<student_id>_days1_to_3.zip` ready for LMS or Git submission.

---

## 💬 Launching the Interactive Crypto Chat Lab

To launch the full-stack interactive messaging laboratory and instructor MITM dashboard:

```bash
cd crypto-chat-lab

# macOS & Linux
./start.sh

# Windows (Command Prompt)
start.bat

# Cross-Platform Python Launcher
python3 start_lab.py
```

Once started, open your browser to **`http://localhost:3005`**.

### 🌐 Hosting for Remote / Hybrid Participants via Ngrok:

If you are the instructor / server owner and want external students to connect from their machines or smartphones:

```bash
cd crypto-chat-lab
./ngrok_tunnel.sh
```

Ngrok provides an instant public HTTPS/WSS URL (`https://xxxx.ngrok-free.app`). Remote participants can open it directly or click **"Server: Localhost:3005"** in the app and paste the ngrok URL to connect over **WSS (WebSocket Secure)**.

### 📡 Multi-Protocol MQTT Inspection:

The central server runs an embedded Aedes MQTT broker on TCP `1883` and `/mqtt` WebSockets:

```bash
# Listen to live wire traffic across the network
python3 crypto-chat-lab/mqtt_sniffer.py

# Inject encrypted messages via Python
python3 crypto-chat-lab/mqtt_publisher.py --sender "IoT_Node" --cipher caesar --shift 4 --message "STATUS OK"
```

---

## 📜 Academic Standards Reference

- **NIST FIPS 197**: Advanced Encryption Standard (AES).
- **NIST SP 800-38D**: Galois/Counter Mode (GCM) for Authenticated Encryption.
- **NIST FIPS 203/204/205**: Post-Quantum Cryptography Standards (ML-KEM, ML-DSA, SLH-DSA).
- **RFC 8446**: The Transport Layer Security (TLS) Protocol Version 1.3.
- **RFC 7748**: Elliptic Curves for Security (Curve25519 / X25519).
- **RFC 3447**: Public-Key Cryptography Standards (PKCS) #1: RSA Cryptography Specifications.
- **OASIS MQTT v3.1.1**: Message Queuing Telemetry Transport Standard.
