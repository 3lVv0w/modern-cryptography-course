# 🎓 CS-1XX / ECE-1XX Modern Cryptography for Beginners
## Class Assignment: Introductory Foundations & Hands-On Security
**Classical Secrets, Modern Symmetric Ciphers & Public-Key Exchange**

* 🌐 **Language / ภาษา:** [🇺🇸 English Version](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_BEGINNER.md) | [🇹🇭 ฉบับภาษาไทย (Thai Version)](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_BEGINNER_TH.md)
* **Target Audience:** Beginners, First/Second-Year CS/IT/Engineering Students, Bootcampers & Cybersecurity Novices
* **Prerequisites:** Basic familiarity with Python (variables, loops, functions). No advanced mathematics required!
* **Assigned:** Day 3 (Post-Public Key Lecture)
* **Due Date:** Sunday 23:59:59 (7 Days from Assignment Date)
* **Total Points:** 100 Points (+ 10 Points Extra Credit / Bonus)
* **Starter Code:** [`assignments/assignment_beginner_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_beginner_student.py)
* **Report Template:** [`assignments/REPORT_TEMPLATE_BEGINNER.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_BEGINNER.md) (or [`REPORT_TEMPLATE_BEGINNER_TH.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_BEGINNER_TH.md))
* **Submission Validator:** [`assignments/submit_check_beginner.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/submit_check_beginner.py)

---

## 🎯 Executive Summary & Learning Objectives

Welcome to your first hands-on cryptography assignment! In this project, you will discover how humans have protected secrets across history—from Julius Caesar's military orders, to the mathematical magic of bitwise XOR, to the modern AES algorithms that safeguard banking apps, and the public-key trapdoors that power the secure Internet (HTTPS).

By completing this assignment, you will:
1. **Understand Classical Ciphers & Frequency Analysis:** Implement the Caesar Shift Cipher, explore why simple shifts are easily broken, and understand how bitwise XOR ($A \oplus B \oplus B = A$) serves as the fundamental building block of modern digital encryption.
2. **Master Modern Symmetric Encryption (AES-GCM):** Learn how modern block ciphers work, why the flawed "ECB mode" leaks data patterns (the famous "AES Penguin"), and use Python's industry-standard `cryptography` library to implement secure AES-256-GCM with built-in tamper detection.
3. **Demystify Public-Key Cryptography (Diffie-Hellman & RSA):** Experience the magic of agreeing on a secret key over a public network using modular arithmetic without an eavesdropper learning the key, and test a working toy model of the RSA cryptosystem.
4. **Investigate Digital Integrity & Hashes (SHA-256):** Understand why hashing is not encryption, how cryptographic hashes act as digital fingerprints, and measure the dramatic "Avalanche Effect" where changing one tiny letter scrambles the entire output.

---

## 📋 Assignment Structure & Score Allocation

| Section | Topic & Deliverables | Format | Points |
| :--- | :--- | :--- | :---: |
| **Part 1** | **Conceptual Foundations & Intuitive Cryptography** | Written Report (`REPORT_BEGINNER.md`) | **30 pts** |
| | • Question 1.1: Classical Ciphers & Why Simple Shifts Fail | Short Answer & Frequency Intuition | 7 pts |
| | • Question 1.2: Symmetric vs. Asymmetric Encryption in Everyday Life | Analogies & HTTPS Hybrid Model | 8 pts |
| | • Question 1.3: The AES Penguin Mystery & Why Cipher Modes Matter | Pattern Exposure Analysis | 7 pts |
| | • Question 1.4: Hashing vs. Encryption & The Avalanche Effect | Comparison Table & Hash Analysis | 8 pts |
| **Part 2** | **Hands-On Beginner Coding Lab** | Python Code (`student.py`) | **60 pts** |
| | • Task 2.1: Caesar Cipher (Encrypt & Decrypt) | Python Functions | 10 pts |
| | • Task 2.2: XOR Bitwise Secret Stream | Python Function | 10 pts |
| | • Task 2.3: Euclidean Greatest Common Divisor (GCD) | Python Function | 10 pts |
| | • Task 2.4: Modern Symmetric Protection (AES-256-GCM) | Python Functions | 10 pts |
| | • Task 2.5: The Secret Handshake (Diffie-Hellman Key Exchange) | Python Functions | 10 pts |
| | • Task 2.6: The Magic Lockbox (Toy RSA Encrypt & Decrypt) | Python Functions | 10 pts |
| **Part 3** | **Beginner Detective Mission: Intercepted Spy Message** | Python Script & Report | **10 pts** |
| | • Mission 3.1: Decrypt Intercepted Transmission & Verify SHA-256 | Brute Force & Hash Verification | 10 pts |
| **Bonus** | **Extra Credit: The Butterfly Effect (Avalanche Detector)** | Python Function | **+10 pts** |
| **Total** | | | **100 pts (+10)** |

---

# 📖 Part 1: Conceptual Foundations & Intuitive Cryptography (30 Points)

Write your answers in [`assignments/REPORT_TEMPLATE_BEGINNER.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_BEGINNER.md) (or [`REPORT_TEMPLATE_BEGINNER_TH.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_BEGINNER_TH.md)).

### Question 1.1: Classical Ciphers & Why Simple Shifts Fail (7 Points)
1. **Exhaustive Key Search (Brute Force):**
   * Julius Caesar shifted every letter in his messages forward by 3 places (e.g., $A \to D, B \to E$).
   * Why is a shift cipher trivially insecure today? How many possible shift keys exist in the English alphabet ($A..Z$), and how fast can a computer test every key?
2. **The Frequency Analysis Trick:**
   * In English, letters do not appear with equal probability. The letter **'E'** accounts for approximately 12.7% of all text, followed by **'T'** (~9.1%) and **'A'** (~8.2%).
   * If you intercept an encrypted message where the letter **'Q'** appears 13% of the time, what letter is 'Q' most likely to be? Explain how frequency analysis allows an eavesdropper to break substitution ciphers without knowing the key.

### Question 1.2: Symmetric vs. Asymmetric Encryption in Everyday Life (8 Points)
1. **Real-World Physical Analogies:**
   * **Symmetric Key Encryption:** Explain how this is like a physical safe where two people hold identical duplicate keys. What is the fundamental risk (The Key Distribution Dilemma)?
   * **Asymmetric Key Encryption:** Explain how this is like an open padlock or a public mailbox slot. Anyone can snap the lock shut or drop an envelope in (Public Key), but who can unlock it (Private Key)?
2. **The HTTPS Hybrid Architecture:**
   * When your browser connects securely to `https://google.com`, it uses **both** asymmetric and symmetric cryptography together.
   * Why don't we use RSA or ECC to encrypt everything, like streaming 4K Netflix videos? Why is the hybrid model (Asymmetric for the initial handshake, Symmetric AES for the actual data stream) the global standard?

### Question 1.3: The AES Penguin Mystery & Why Cipher Modes Matter (7 Points)
1. **The "ECB Penguin" Phenomenon:**
   * Electronic Codebook (ECB) mode encrypts each 16-byte block of plaintext completely independently with the same key.
   * Why does encrypting an image of Tux the Linux Penguin with AES-ECB still leave the penguin clearly visible, even though every individual block is scrambled?
2. **The Fix: IVs and Nonces:**
   * How do modern modes like CBC (Cipher Block Chaining) and GCM (Galois/Counter Mode) fix this?
   * What is an **Initialization Vector (IV)** or **Nonce**, and why does adding randomness ensure that identical plaintext blocks produce completely unique ciphertexts?

### Question 1.4: Hashing vs. Encryption & The Avalanche Effect (8 Points)
1. **Encryption vs. Hashing:**
   * Complete the comparison table in your report: Can a hash be decrypted? Does a hash use a key? What is the main purpose of hashing versus encryption?
2. **The Avalanche Effect:**
   * What is the "Avalanche Effect"? Why is it essential that changing a single character (e.g. changing an invoice total from `$1,000` to `$9,000`) completely changes the resulting hash output?

---

# 💻 Part 2: Hands-On Beginner Coding Lab (60 Points)

Open [`assignments/assignment_beginner_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_beginner_student.py). Complete each function marked with `# TODO: YOUR CODE HERE`.

### Task 2.1: Caesar Shift Cipher (10 Points)
* `caesar_encrypt(plaintext: str, shift: int) -> str`:
  * Shift each letter forward by `shift` positions modulo 26: $C_i = (P_i + \text{shift}) \bmod 26$.
  * Preserves upper and lower case (`'A'..'Z'` and `'a'..'z'`).
  * Leaves punctuation, spaces, and numbers completely untouched.
  * Correctly handles shifts larger than 26 or negative numbers using `% 26`.
* `caesar_decrypt(ciphertext: str, shift: int) -> str`:
  * Reverses the encryption transformation: $P_i = (C_i - \text{shift}) \bmod 26$ (or simply `caesar_encrypt(ciphertext, -shift)`).

### Task 2.2: XOR Bitwise Secret Stream (10 Points)
* `xor_cipher(data: bytes, key: bytes) -> bytes`:
  * Takes input `data` bytes and applies bitwise XOR (`^`) with `key` bytes in a repeating cycle.
  * Formula: $C_i = \text{Data}_i \oplus \text{Key}_{i \bmod \text{len(Key)}}$.
  * Demonstrates the fundamental reversible property: $(A \oplus B) \oplus B = A$.

### Task 2.3: Euclidean Greatest Common Divisor (GCD) (10 Points)
* `euclidean_gcd(a: int, b: int) -> int`:
  * Implements Euclid's ancient algorithm (300 BC) to find the largest integer that divides both $a$ and $b$.
  * Repeatedly replaces `a, b = b, a % b` until `b == 0`, then returns `a`.

### Task 2.4: Modern Symmetric Protection: AES-256-GCM (10 Points)
* `aes_gcm_encrypt(plaintext: str, key: bytes) -> tuple[bytes, bytes]`:
  * Uses Python's `cryptography.hazmat.primitives.ciphers.aead.AESGCM`.
  * Generates a secure random 12-byte (96-bit) nonce using `secrets.token_bytes(12)`.
  * Encrypts the UTF-8 plaintext bytes and returns `(nonce, ciphertext)`.
* `aes_gcm_decrypt(nonce: bytes, ciphertext: bytes, key: bytes) -> str`:
  * Decrypts the ciphertext using the same key and nonce.
  * Verifies the 16-byte authentication tag automatically. If someone modified even one bit of the ciphertext, it will raise an error, protecting data integrity!

### Task 2.5: The Secret Handshake: Diffie-Hellman Key Exchange (10 Points)
* `dh_compute_public_key(g: int, priv_key: int, p: int) -> int`:
  * Computes $A = g^{\text{priv\_key}} \bmod p$ using Python's fast `pow(g, priv_key, p)`.
* `dh_compute_shared_secret(peer_public_key: int, my_priv_key: int, p: int) -> int`:
  * Computes $S = (\text{peer\_public\_key})^{\text{my\_priv\_key}} \bmod p$.
  * Proves that Alice and Bob arrive at the exact same secret $S$ without ever sending $S$ over the wire!

### Task 2.6: The Magic Lockbox: Toy RSA (10 Points)
* `rsa_encrypt_toy(m: int, e: int, n: int) -> int`:
  * Encrypts integer message $m$ with public exponent $e$ and modulus $n$: $C = m^e \bmod n$.
* `rsa_decrypt_toy(c: int, d: int, n: int) -> int`:
  * Decrypts integer ciphertext $c$ with private exponent $d$ and modulus $n$: $M = c^d \bmod n$.

---

# 🕵️ Part 3: Beginner Detective Mission (10 Points + 10 Bonus)

### Mission 3.1: Intercepted Spy Message & SHA-256 Integrity (10 Points)
* **The Scenario:**
  You intercepted an encrypted radio transmission:
  `"AOL ZLJYLA HNLUA PZ TLLAPUN HA TPKUPNOA"`
  Intelligence tells you the message contains the clue word `"AGENT"`.
* **Your Tasks:**
  1. Implement `crack_simple_caesar(ciphertext: str, clue_word: str = "THE") -> tuple[int, str]`:
     * Loop through all 26 shifts ($0..25$).
     * Decrypt the text with each shift.
     * When `clue_word.upper()` is detected in the decrypted candidate, return `(shift, candidate)`.
  2. Implement `compute_sha256_hex(text: str) -> str`:
     * Compute the SHA-256 digital fingerprint using `hashlib.sha256()`.
     * Verify that the decrypted message produces the authentic SHA-256 fingerprint.

### Bonus Mission 3.2: The Butterfly Effect (Avalanche Detector) (+10 Points Extra Credit)
* Implement `measure_hash_avalanche(text1: str, text2: str) -> float`:
  * Compares two nearly identical texts (differing by only 1 character!).
  * Converts the two SHA-256 hashes into 256 binary bits.
  * Calculates what percentage of bits flipped between the two outputs.
  * In a high-quality cryptographic hash function, approximately **50%** of all bits should flip!

---

# 🧪 Testing & Pre-Flight Verification

You can test your code locally at any time:

```bash
# Run local self-test suite
python3 assignments/assignment_beginner_student.py
```

When you are ready to submit, run the automated validator:
```bash
python3 assignments/submit_check_beginner.py --student-id "YOUR_STUDENT_ID" --name "YOUR_FULL_NAME"
```

The script will:
1. Validate your code against all unit tests.
2. Confirm that your report (`REPORT_BEGINNER.md` or `REPORT_TEMPLATE_BEGINNER.md`) is completed.
3. Compute SHA-256 checksums to prove your submission integrity.
4. Bundle your files into `assignments/submission_<STUDENT_ID>_beginner.zip`.

---

## ⚖️ Academic Integrity & AI Policy

* **Learning with AI:** You are encouraged to use AI tools (ChatGPT, Claude, Antigravity) to explain difficult concepts, clarify syntax errors, or discuss the intuition behind algorithms.
* **The Golden Rule:** You must personally understand every piece of code you submit. You should be able to explain how your Caesar cipher, XOR loop, or Diffie-Hellman calculations work in plain English.
* **Collaboration:** Brainstorming and discussing conceptual questions with classmates is welcome. Direct copying of code or answers is strictly forbidden.

---

## 📊 Comprehensive Grading Rubric

```text
Total Score: 100 Points (+10 Extra Credit)

Part 1: Conceptual Understanding & Report (30 Points)
├── Question 1.1 (7 pts): Caesar Cipher Brute Force (3 pts) + Frequency Analysis (4 pts)
├── Question 1.2 (8 pts): Physical Lockbox Analogies (4 pts) + HTTPS Hybrid Model (4 pts)
├── Question 1.3 (7 pts): The AES Penguin Leak (4 pts) + IVs and Nonces (3 pts)
└── Question 1.4 (8 pts): Encryption vs. Hashing Table (4 pts) + Avalanche Effect (4 pts)

Part 2: Code Implementation Lab (60 Points)
├── Task 2.1 (10 pts): Caesar Encrypt (5 pts) & Decrypt (5 pts)
├── Task 2.2 (10 pts): Bitwise XOR Symmetric Stream Cipher
├── Task 2.3 (10 pts): Euclidean Greatest Common Divisor (GCD)
├── Task 2.4 (10 pts): AES-256-GCM Encryption (5 pts), Decryption & Tamper Check (5 pts)
├── Task 2.5 (10 pts): Diffie-Hellman Public Key (5 pts) & Shared Secret Agreement (5 pts)
└── Task 2.6 (10 pts): Toy RSA Message Encryption (5 pts) & Decryption (5 pts)

Part 3: Detective Mission (10 Points)
└── Mission 3.1 (10 pts): Brute Force Caesar Spy Cracker (5 pts) & SHA-256 Fingerprint (5 pts)

Bonus Extra Credit (+10 Points)
└── Mission 3.2 (10 pts): Hash Avalanche Bit-Flip Measurement Function
```
