# 📘 DAY 4 LEARNING MATERIAL: Message Integrity, Digital Signatures, PKI & TLS 1.3
**Course:** Modern Cryptography & Network Security (CS-4XX / ECE-4XX)  
**Target Audience:** University Computer Science & Engineering Students  
**Prerequisites:** Day 1–3 Material, Hash Properties, Asymmetric Math, Python 3  

---

## 📜 Real-World Story: "The Fake Google Certificate & TLS 1.3 Forward Secrecy"

> **Setting:** Global Web Infrastructure & Rogue Certificate Authorities  
> **Core Concepts:** X.509 Certificate Chains, Digital Signatures (Ed25519), TLS 1.3 Handshake, Perfect Forward Secrecy (PFS), Post-Quantum Cryptography (PQC).

In 2011, state-sponsored hackers compromised **DigiNotar**, a Dutch Certificate Authority (CA). The attackers stole the CA's private signing key and issued a fraudulent X.509 Wildcard Certificate for `*.google.com`.

Using the fake certificate, the attackers launched a Man-In-The-Middle (MITM) attack against 300,000 internet users in Iran, intercepting Gmail sessions. Because the fake certificate was signed by a trusted Root CA pre-installed in browsers, standard TLS validation initially passed!

### How Modern PKI & TLS 1.3 Prevent This:
1. **Certificate Transparency (CT) & Pinning:** Google Chrome detected the fake certificate because Google domain public keys were pinned to trusted hashes in the browser engine. DigiNotar's root authority was revoked globally within days.
2. **TLS 1.3 Perfect Forward Secrecy (PFS):** Under TLS 1.3, ephemeral ECDHE key exchange generates unique session keys for every connection. Even if an attacker steals a server's private RSA key 5 years later, they **cannot** decrypt past recorded traffic.
3. **The Quantum Horizon:** As quantum computers advance, Shor's algorithm threatens to break RSA and ECC. Systems are now preparing for **NIST Post-Quantum Cryptography (PQC)** standards (ML-KEM / Kyber) to safeguard future global communications.

**The Lesson:** Modern network security is a multi-layered shield: Hashes guarantee integrity, Digital Signatures guarantee identity, PKI establishes trust, and TLS 1.3 guarantees forward secrecy.

---

## 🎯 Day 4 Learning Objectives
By the end of Day 4, students will be able to:
1. Formally define cryptographic hash function requirements and prove the **Birthday Paradox** collision bound $\mathcal{O}(2^{n/2})$.
2. Explain the **Hash-and-Sign** paradigm for Digital Signatures (RSA-PSS, ECDSA, Ed25519) under **EUF-CMA** security.
3. Diagram X.509 Certificate validation algorithms and detail Certificate Authority (CA) Chains of Trust.
4. Trace the complete **TLS 1.3 Handshake** state machine and define Perfect Forward Secrecy (PFS).
5. Evaluate the threat of Shor's Quantum Algorithm and outline NIST Post-Quantum Cryptography (PQC) standards.

---

# 📖 Module 4.1: Cryptographic Hash Functions & Collision Bounds

### 1. The 5 Mandatory Hash Properties
1. **Deterministic:** Same input always yields identical hash output.
2. **Efficient Computation:** Linear time $O(|x|)$.
3. **Pre-image Resistance (One-Way):** Given $h$, finding $x$ takes $\mathcal{O}(2^n)$.
4. **Second Pre-image Resistance:** Given $x_1$, finding $x_2 \neq x_1$ such that $H(x_1) = H(x_2)$ takes $\mathcal{O}(2^n)$.
5. **Collision Resistance:** Finding *any* pair $x_1 \neq x_2$ such that $H(x_1) = H(x_2)$ takes $\mathcal{O}(2^{n/2})$.

### 2. Proof of Birthday Paradox Collision Bound
For $n$-bit hash space $N = 2^n$, probability of collision reaches $50\%$ in $k \approx 1.177 \sqrt{N} = \mathcal{O}(2^{n/2})$ operations.
* **MD5 ($n=128$):** Collisions in $2^{64}$ operations (Broken!).
* **SHA-256 ($n=256$):** Collision bound $2^{128}$ operations (Secure!).

---

# 📖 Module 4.2: Digital Signatures & Non-Repudiation

### 1. The Hash-and-Sign Paradigm
Documents are hashed first, then the hash digest is signed:
* **Signing:** $S = \text{Sign}_{d}(\text{SHA256}(M))$.
* **Verification:** $\text{Verify}_{e}(M, S) \implies S^e \bmod N \stackrel{?}{=} \text{SHA256}(M)$.
* **Security Model:** Existential Unforgeability under Chosen Message Attack (**EUF-CMA**).

---

# 📖 Module 4.3: Public Key Infrastructure (PKI) & TLS 1.3

### 1. X.509 Certificate Chain & TLS 1.3 Handshake
* **Chain of Trust:** Root CA (OS Trust Store) $\rightarrow$ Intermediate CA $\rightarrow$ Leaf Domain Certificate (`secure-university.edu`).
* **TLS 1.3 Handshake:** 1-RTT handshake providing **Perfect Forward Secrecy (PFS)** via ephemeral ECDHE keys.

---

# 📖 Module 4.4: Post-Quantum Cryptography (PQC) Horizon

### 1. Shor's Quantum Threat & NIST Standards (2024)
* Shor's algorithm running on a quantum computer breaks RSA/ECC in $O(n^3)$ polynomial time.
* **NIST PQC Standards:** ML-KEM (CRYSTALS-Kyber) for encryption; ML-DSA (CRYSTALS-Dilithium) for digital signatures.

---

## 🎮 Day 4 Gamification: "Capture The Flag (CTF) Championship"
* Capstone CTF Competition ("Operation Broken Envelope") combining Caesar decryption, SHA-256 hash checks, and Ed25519 signature verification.

---

## 💻 Day 4 Hands-On Lab Assignment
Students must complete `day4/lab_student.py` in terminal:
```bash
python3 day4/lab_student.py
```
Target Score: **100% (5/5 Tests Passed)**.
