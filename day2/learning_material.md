# 📘 DAY 2 LEARNING MATERIAL: Abstract Algebra, Number Theory & Symmetric Encryption (AES)
**Course:** Modern Cryptography & Network Security (CS-4XX / ECE-4XX)  
**Target Audience:** University Computer Science & Engineering Students  
**Prerequisites:** Day 1 Material, Basic Abstract Algebra, Python 3  

---

## 📜 Real-World Story: "The ECB Tux Penguin & The Nonce Disaster"

> **Setting:** Fintech Engineering & Cloud Storage Data Breach  
> **Core Concepts:** AES-256 Block Cipher Modes (ECB vs. CBC), AES-GCM AEAD, Nonce Reuse Stream Cipher Vulnerability.

### Part A: The ECB Penguin Pattern Leak
In 2018, a fintech mobile wallet startup stored customer profile pictures and check scans in a cloud database. Lead developer Marcus chose **AES-256 in ECB (Electronic Codebook) Mode** because it was fast and didn't require managing an Initialization Vector (IV).

During a security audit, penetration testers downloaded the encrypted image file. Although every individual byte was encrypted with 256-bit AES keys, identical 16-byte blocks of white background pixels produced identical ciphertext blocks! When rendered as an image, the complete silhouette of the Tux Penguin logo (and handwritten signatures on bank checks) remained 100% visible in the encrypted file!

### Part B: The $1,000,000 Nonce Reuse Catastrophe
To fix the leak, Marcus upgraded to **AES-256-GCM (Galois/Counter Mode)** for Authenticated Encryption. However, to save database storage, he hardcoded a fixed 12-byte Nonce: `nonce = b"FIXEDNONCE12"`.

An attacker intercepted two consecutive wire transfers ($C_1$ and $C_2$) sent by the same user:
1. $M_1$ = `"TRANSFER $10,000 TO ALICE"`
2. $M_2$ = `"TRANSFER $90,000 TO BOB  "`

Because AES-GCM operates as a stream cipher internally, reusing a Nonce meant $C_1 \oplus C_2 = M_1 \oplus M_2$. The attacker XORed the ciphertexts, extracted the keystream, and forged a valid-looking ciphertext $C_3$ for `"TRANSFER $990,000 TO ATTACKER"`.

**The Lesson:** Block cipher mode selection is critical. **ECB mode leaks structural patterns**, and **reusing a Nonce in AES-GCM destroys both confidentiality and authentication!**

---

## 🎯 Day 2 Learning Objectives
By the end of Day 2, students will be able to:
1. Define algebraic structures: Groups, Rings, Fields, and Galois Fields $GF(2^8)$.
2. Apply the Extended Euclidean Algorithm to derive modular multiplicative inverses ($a^{-1} \bmod n$).
3. Derive and apply Euler's Totient Function $\phi(n)$, Euler's Theorem, and Fermat's Little Theorem.
4. Diagram the 4 internal transformations of the **AES-256** round function (`SubBytes`, `ShiftRows`, `MixColumns`, `AddRoundKey`).
5. Evaluate Block Cipher Modes of Operation (ECB, CBC, GCM) and prove why Nonce reuse in **AES-GCM** destroys security.

---

# 📖 Module 2.1: Abstract Algebra & Group Theory

### 1. Algebraic Structures
* **Group $(\mathcal{G}, \circ)$:** A set $\mathcal{G}$ combined with an operation $\circ$ satisfying Closure, Associativity, Identity ($e$), and Inverse ($a^{-1}$).
* **Multiplicative Group $\mathbb{Z}_n^*:$** Set of integers modulo $n$ coprime to $n$:
  $$\mathbb{Z}_n^* = \{a \in \{1, \dots, n-1\} \mid \gcd(a, n) = 1\}$$
  Order $|\mathbb{Z}_n^*| = \phi(n)$.

---

# 📖 Module 2.2: Number Theory Primitives

### 1. Extended Euclidean Algorithm
Finds Bezout coefficients $x, y \in \mathbb{Z}$ such that:
$$a \cdot x + b \cdot y = \gcd(a, b)$$
If $\gcd(a, n) = 1$, then $x \pmod n$ is the modular multiplicative inverse $a^{-1} \bmod n$.

### 2. Euler's Totient & Euler's Theorem
* For primes $p, q$: $\phi(p \cdot q) = (p - 1)(q - 1)$.
* **Euler's Theorem:** If $\gcd(a, n) = 1$, then $a^{\phi(n)} \equiv 1 \pmod n$.
* **Fermat's Little Theorem:** If $p$ is prime, $a^{p-1} \equiv 1 \pmod p$.

### 3. Fast Modular Exponentiation (Square-and-Multiply)
Computes $b^e \bmod n$ in $O(\log e)$ time using binary representation of exponent $e$.

---

# 📖 Module 2.3: Advanced Encryption Standard (AES) & Cipher Modes

### 1. AES Architecture
Operates on 128-bit blocks arranged in a $4 \times 4$ byte State Matrix.
* **4 Round Transformations:** `SubBytes` (S-Box), `ShiftRows`, `MixColumns` ($GF(2^8)$ multiplication), `AddRoundKey`.

### 2. Cipher Modes
* **ECB:** Insecure block independence flaw.
* **CBC:** Sequential chaining via Initialization Vectors (IV).
* **AES-GCM:** Authenticated Encryption with Associated Data (AEAD). Nonce reuse yields $C_1 \oplus C_2 = M_1 \oplus M_2$.

---

## 🎮 Day 2 Gamification: "Clock Arithmetic Showdown & ECB Challenge"
* Speed modulo math sprints & ECB pattern exposure identification.

---

## 💻 Day 2 Hands-On Lab Assignment
Students must complete `day2/lab_student.py` in terminal:
```bash
python3 day2/lab_student.py
```
Target Score: **100% (5/5 Tests Passed)**.
