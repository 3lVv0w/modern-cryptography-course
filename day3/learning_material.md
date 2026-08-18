# 📘 DAY 3 LEARNING MATERIAL: Public-Key Cryptography (DHKE, RSA & Elliptic Curves)
**Course:** Modern Cryptography & Network Security (CS-4XX / ECE-4XX)  
**Target Audience:** University Computer Science & Engineering Students  
**Prerequisites:** Day 1 & Day 2 Material, Group Theory, Fast Exponentiation, Python 3  

---

## 📜 Real-World Story: "The Smart Grid Blackout & Fermat's RSA Factorization"

> **Setting:** IoT Smart Grid Infrastructure & Hardware Security  
> **Core Concepts:** RSA Cryptosystem, Fermat Factorization Attack, Elliptic Curve Cryptography (ECC / Curve25519).

In 2021, an energy utility company deployed 100,000 smart electricity meters across a major metropolitan area. Each smart meter generated an RSA-2048 public key pair to authenticate remote firmware updates sent from the central server.

To save CPU cycles on tiny 8-bit ARM microcontrollers, the firmware engineer implemented a custom Pseudo-Random Number Generator (PRNG) for generating prime numbers $p$ and $q$. Due to poor entropy, the PRNG generated prime pairs $p$ and $q$ that were extremely close to each other ($|p - q| < 2^{16}$).

Security researchers realized that when $p \approx q \approx \sqrt{N}$, the modulus $N = p \cdot q$ can be written as $N = a^2 - b^2 = (a - b)(a + b)$.

By setting $a = \lceil \sqrt{N} \rceil$ and checking if $b^2 = a^2 - N$ is a perfect square, researchers factored the 2048-bit RSA keys in **under 2 milliseconds**! They derived private exponent $d = e^{-1} \bmod \phi(N)$ and forged administrative commands that could trigger rolling blackouts.

**The Lesson:** RSA requires large, independent, random primes. Today's modern systems are migrating away from RSA to **Elliptic Curve Cryptography (Curve25519 / X25519)**, which achieves higher security with 256-bit keys that run 10x faster on microcontrollers.

---

## 🎯 Day 3 Learning Objectives
By the end of Day 3, students will be able to:
1. Define **One-Way Trapdoor Functions** and analyze formal computational hardness assumptions (**DLP**, **IFP**, **CDH**).
2. Diagram the **Diffie-Hellman Key Exchange (DHKE)** protocol and prove why both parties compute identical shared secrets.
3. Derive RSA Key Generation, Encryption, Decryption, and complete the formal decryption proof using Fermat's Little Theorem and the Chinese Remainder Theorem (CRT).
4. Define **IND-CPA** (Indistinguishability under Chosen Plaintext Attack) security and explain why padding (RSA-OAEP) is required.
5. Explain **Elliptic Curve Cryptography (ECC)** point addition, ECDH, and compare ECC-256 vs RSA-3072 efficiency.

---

# 📖 Module 3.1: One-Way Trapdoors & Computational Hardness

### 1. Hardness Assumptions
* **Integer Factorization Problem (IFP):** Factoring $N = pq$ using GNFS algorithm $O(\exp(c (\ln N)^{1/3} (\ln \ln N)^{2/3}))$.
* **Discrete Logarithm Problem (DLP):** Finding $x$ given $y = g^x \bmod p$.
* **Computational Diffie-Hellman (CDH):** Computing $g^{ab}$ given $(g^a, g^b)$.

---

# 📖 Module 3.2: Diffie-Hellman Key Exchange (DHKE)

### 1. Protocol Derivation
* Alice sends $A = g^a \bmod p$; Bob sends $B = g^b \bmod p$.
* Shared Secret $S = B^a \bmod p = (g^b)^a = g^{ab} \bmod p = (g^a)^b = A^b \bmod p$.
* **MITM Vulnerability:** Unauthenticated DHKE allows Eve to substitute her key shares ($E$) and eavesdrop.

---

# 📖 Module 3.3: RSA Cryptosystem & IND-CPA Security

### 1. RSA Mathematics
* $N = pq$, $\phi(N) = (p-1)(q-1)$, $e \cdot d \equiv 1 \pmod{\phi(N)}$.
* Encryption: $C = M^e \bmod N$; Decryption: $M = C^d \bmod N$.
* **Formal Proof:** $C^d \equiv M^{ed} \equiv M^{k\phi(N)+1} \equiv M \pmod N$ via CRT.

### 2. IND-CPA Security & Padding
* Textbook RSA is deterministic $\implies$ Fails IND-CPA.
* **RSA-OAEP** adds randomness and hashes to achieve IND-CPA and IND-CCA2 security.

### 3. Fermat's Factorization Attack
* If $|p - q|$ is small, $N = a^2 - b^2 \implies a = \lceil\sqrt{N}\rceil$, factor $N$ in $O(\sqrt{N})$.

---

# 📖 Module 3.4: Elliptic Curve Cryptography (ECC)

### 1. Geometry & Security
* Weierstrass Curve: $y^2 = x^3 + ax + b \pmod p$. Point Addition & Scalar Multiplication ($k \cdot P$).
* **ECC Efficiency:** 256-bit ECC (Curve25519) matches 3072-bit RSA security level.

---

## 🎮 Day 3 Gamification: "Public Key Trading Floor & RSA Factorization Race"
* Trading floor DHKE roleplay & speed key cracking competition.

---

## 💻 Day 3 Hands-On Lab Assignment
Students must complete `day3/lab_student.py` in terminal:
```bash
python3 day3/lab_student.py
```
Target Score: **100% (5/5 Tests Passed)**.
