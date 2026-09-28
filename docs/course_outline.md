# 🎓 4-Day University Course Syllabus: Modern Cryptography & Network Security
**Course Code / Level:** CS-4XX / ECE-4XX (Upper-Division Undergraduate / Graduate Syllabus)  
**Curriculum Alignment:** ACM/IEEE Computer Science Curricula (IAS - Information Assurance & Security)  
**Format:** 4 Days (Each Day: 3 Hours Theory Lecture + 3 Hours Hands-On Lab & Gamification)  
**Prerequisites:** Data Structures & Algorithms, Discrete Mathematics (Elementary Number Theory), Basic Python 3

---

## 🎯 3-Tier Challenge System for Daily Labs

| Tier Level | Target Audience | Challenge Description & Expectations |
| :--- | :--- | :--- |
| 🟢 **LEVEL 1: Novice** | Warm-Up / Core Fundamentals | Implementing basic cryptographic algorithms from scratch (Caesar shifts, Euclidean GCD, RSA basic keygen, SHA-256 hash generation). |
| 🟡 **LEVEL 2: Intermediate** | Applied Security Analysis | Statistical cryptanalysis ($\chi^2$ scoring), Index of Coincidence (IC), AES-ECB pattern exposure detection, and X.509 Certificate verification. |
| 🔴 **LEVEL 3: Hardcore** | Advanced Offensive Cryptanalysis | Full automated Vigenère cipher breaker, Two-time pad crib dragging attacks, AES-GCM nonce reuse exploits, Fermat RSA factorization attacks, and Capstone CTF solvers. |

---

## 📚 Textbooks & Reference Literature
1. **Katz, J., & Lindell, Y.** (2020). *Introduction to Modern Cryptography* (3rd ed.). CRC Press.
2. **Paar, C., & Pelzl, J.** (2010). *Understanding Cryptography: A Textbook for Students and Practitioners*. Springer.
3. **Khan Academy Cryptography Series** (Visual Intuition & Interactive Demonstrations).

---

## 📅 4-Day Master Schedule Overview

```
 DAY 1: Classical Ciphers, Entropy & Information Theory
 ├── Morning (09:00 - 12:00): Substitution Ciphers, Frequency Analysis, Shannon Perfect Secrecy & OTP
 └── Afternoon (13:00 - 16:00): Lab 1 (3-Tier Challenges: Caesar, Chi-Sq, IC & Two-Time Pad Crib Drag) + Game 1

 DAY 2: Abstract Algebra, Number Theory & Symmetric Encryption (AES)
 ├── Morning (09:00 - 12:00): Groups Z_n*, Euclidean Algorithm, AES Architecture & Block Cipher Modes (GCM)
 └── Afternoon (13:00 - 16:00): Lab 2 (3-Tier Challenges: Ext-GCD, AES-ECB Pattern Exposure & GCM Nonce Exploit) + Game 2

 DAY 3: Public-Key Cryptography (Diffie-Hellman, RSA & Elliptic Curves)
 ├── Morning (09:00 - 12:00): One-Way Trapdoors, DHKE, RSA Proofs, IND-CPA, OAEP & ECC (Curve25519)
 └── Afternoon (13:00 - 16:00): Lab 3 (3-Tier Challenges: DHKE, RSA from Scratch, Fermat Attack & X25519) + Game 3

 DAY 4: Message Integrity, Signatures, PKI, TLS 1.3 & Post-Quantum Cryptography
 ├── Morning (09:00 - 12:00): Hash Functions, Birthday Bound, Signatures (ECDSA), PKI X.509 & TLS 1.3
 └── Afternoon (13:00 - 16:00): Lab 4 (3-Tier Challenges: Avalanche Effect, Ed25519, X.509 & Capstone CTF) + Game 4
```

---

# 📖 DAY 1: Classical Ciphers, Entropy & Information Theory

### Morning Session: Theory & Mathematical Foundations (09:00 - 12:00)
* **Module 1.1: Historical Cipher Evolution & Cryptanalysis**
  * Caesar / Shift Cipher over $\mathbb{Z}_{26}$: $e_k(m) = (m + k) \bmod 26$. Exhaustive key search ($|\mathcal{K}| = 25$).
  * Polyalphabetic Substitution (Vigenère Cipher): $e_k(m)_i = (m_i + k_{i \bmod m}) \bmod 26$.
  * Statistical Cryptanalysis: Natural language letter frequency distributions ($E \approx 12.7\%$).
  * **Kasiski Examination & Index of Coincidence (IC):**
    $$\text{IC}(T) = \frac{\sum_{i=A}^Z f_i (f_i - 1)}{N(N - 1)}$$
* **Module 1.2: Information-Theoretic Security & The One-Time Pad (OTP)**
  * **Shannon's Perfect Secrecy Definition:** $P(M = m \mid C = c) = P(M = m) \quad \forall m, c$.
  * **Proof for One-Time Pad ($C = M \oplus K$):** Showing $P(C = c \mid M = m) = 1/2^L$ using Bayes' Theorem.
  * Key Space Requirements & **The Key Distribution Paradox**.

### Afternoon Session: 3-Tier Hands-On Lab (`day1_lab_student.py`)
* 🟢 **Level 1 (Novice):** Implement `caesar_encrypt()` and `caesar_decrypt()`.
* 🟡 **Level 2 (Intermediate):** Implement `compute_chi_squared()` and `compute_index_of_coincidence()`.
* 🔴 **Level 3 (Hardcore):** Implement `crack_vigenere_cipher()` (automated Vigenère breaker) and `two_time_pad_crib_drag()`.
* 🎮 **Interactive Game 1:** *"The Human Frequency Decoder & Two-Time Pad Race"*

---

# 📖 DAY 2: Abstract Algebra, Number Theory & Symmetric Encryption (AES)

### Morning Session: Theory & Mathematical Foundations (09:00 - 12:00)
* **Module 2.1: Algebraic Structures & Group Theory**
  * Multiplicative group of integers modulo $n$: $\mathbb{Z}_n^*$, Order $|\mathbb{Z}_n^*| = \phi(n)$.
* **Module 2.2: Number Theory Primitives**
  * Extended Euclidean Algorithm: $ax + by = \gcd(a, b)$, Modular inverse $a^{-1} \bmod n$, Euler's Totient $\phi(n)$, Euler's Theorem ($a^{\phi(n)} \equiv 1 \pmod n$).
* **Module 2.3: Advanced Encryption Standard (AES-256) & Cipher Modes**
  * AES Transformations (`SubBytes`, `ShiftRows`, `MixColumns`, `AddRoundKey`).
  * ECB Flaw ("AES Penguin"), CBC IVs, AES-256-GCM AEAD & Nonce Reuse vulnerability.

### Afternoon Session: 3-Tier Hands-On Lab (`day2_lab_student.py`)
* 🟢 **Level 1 (Novice):** Implement `extended_gcd()`, `modinv()`, and `pow_mod()`.
* 🟡 **Level 2 (Intermediate):** Implement `encrypt_aes_ecb()` vs `encrypt_aes_cbc()` and `check_ecb_pattern_vulnerability()`.
* 🔴 **Level 3 (Hardcore):** Implement `aes_gcm_encrypt()`, `aes_gcm_decrypt()`, and `exploit_gcm_nonce_reuse()`.
* 🎮 **Interactive Game 2:** *"Clock Arithmetic Showdown & The ECB Penguin Challenge"*

---

# 📖 DAY 3: Public-Key Cryptography (Diffie-Hellman, RSA & Elliptic Curves)

### Morning Session: Theory & Mathematical Foundations (09:00 - 12:00)
* **Module 3.1: One-Way Trapdoors & Hard Computational Assumptions**
  * Trapdoor Functions, DLP, CDH, IFP & GNFS algorithm complexity.
* **Module 3.2: Diffie-Hellman Key Exchange (DHKE)**
  * Protocol derivation ($A = g^a \bmod p, B = g^b \bmod p \implies S = g^{ab} \bmod p$) & MITM attacks.
* **Module 3.3: RSA Cryptosystem & IND-CPA Security**
  * Keygen, Encryption, Decryption, CRT proof, IND-CPA security & RSA-OAEP padding.
* **Module 3.4: Elliptic Curve Cryptography (ECC)**
  * Weierstrass Curve $y^2 = x^3 + ax + b \pmod p$, point addition, ECDH (Curve25519).

### Afternoon Session: 3-Tier Hands-On Lab (`day3_lab_student.py`)
* 🟢 **Level 1 (Novice):** Implement `dh_generate_keypair()` and `dh_compute_shared_secret()`.
* 🟡 **Level 2 (Intermediate):** Implement `rsa_keygen()`, `rsa_encrypt()`, and `rsa_decrypt()`.
* 🔴 **Level 3 (Hardcore):** Implement `fermat_factor(N)`, `crack_rsa_ciphertext()`, and `ecdh_x25519_key_exchange()`.
* 🎮 **Interactive Game 3:** *"The Public Key Trading Floor & RSA Factorization Race"*

---

# 📖 DAY 4: Message Integrity, Signatures, PKI, TLS 1.3 & Post-Quantum Crypto

### Morning Session: Theory & Mathematical Foundations (09:00 - 12:00)
* **Module 4.1: Cryptographic Hash Functions & Collision Bounds**
  * 5 Hash properties, Avalanche Effect, Birthday Paradox proof ($\mathcal{O}(2^{n/2})$).
* **Module 4.2: Digital Signatures & Non-Repudiation**
  * Hash-and-sign paradigm, EUF-CMA security model, Ed25519 signatures.
* **Module 4.3: Public Key Infrastructure (PKI) & TLS 1.3**
  * X.509 Certificate Chain of Trust & TLS 1.3 1-RTT Handshake state machine.
* **Module 4.4: Post-Quantum Cryptography (PQC)**
  * Shor's Quantum Algorithm threat & NIST PQC standards (CRYSTALS-Kyber / CRYSTALS-Dilithium).

### Afternoon Session: 3-Tier Hands-On Lab (`day4_lab_student.py`)
* 🟢 **Level 1 (Novice):** Implement `compute_sha256()`, `measure_avalanche_effect()`, and Ed25519 `sign_message()`.
* 🟡 **Level 2 (Intermediate):** Implement `create_mock_certificate_chain()` and `verify_leaf_against_root()`.
* 🔴 **Level 3 (Hardcore):** Implement `solve_ctf_challenge()` Capstone CTF Solver ("Operation Broken Envelope").
* 🎮 **Interactive Game 4:** *"Capture The Flag (CTF) Championship & Award Ceremony"*

---

## 📊 University Grading & Assessment Rubric

| Component | Weight | Description |
| :--- | :--- | :--- |
| **Day 1 & Day 2 Labs** | **30%** | Completion of Level 1, Level 2, and Level 3 challenges in `day1_lab_student.py` & `day2_lab_student.py`. |
| **Day 3 RSA & DH Labs** | **25%** | Completion of Level 1–3 challenges in `day3_lab_student.py`. |
| **Day 4 OpenSSL & PKI** | **20%** | X.509 Certificate validation and Ed25519 digital signature tasks in `day4_lab_student.py`. |
| **Capstone CTF Challenge** | **15%** | Successful solution of Level 3 Capstone CTF Challenge. |
| **Class & Game Participation** | **10%** | Active engagement in daily interactive gamification and roleplay challenges. |
