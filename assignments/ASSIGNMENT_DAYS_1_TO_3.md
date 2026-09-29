# 🎓 CS-4XX / ECE-4XX Modern Cryptography & Network Security
## Class Assignment: Days 1–3
**Classical Cryptanalysis, Modern Symmetric Ciphers & Public-Key Cryptosystems**

* 🌐 **Language / ภาษา:** [🇺🇸 English Version](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_DAYS_1_TO_3.md) | [🇹🇭 ฉบับภาษาไทย (Thai Version)](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_DAYS_1_TO_3_TH.md)
* **Term:** Spring / Fall Semester
* **Target Audience:** Undergraduate (Upper-Division CS/ECE) & Graduate Students
* **Assigned:** Day 3 (Post-Public Key Lecture)
* **Due Date:** Sunday 23:59:59 (7 Days from Assignment Date)
* **Total Points:** 100 Points (+ 15 Points Extra Credit / Bonus)
* **Starter Code:** [`assignments/assignment_days_1_to_3_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_days_1_to_3_student.py)
* **Report Template:** [`assignments/REPORT_TEMPLATE.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE.md) (หรือ [`REPORT_TEMPLATE_TH.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_TH.md))
* **Submission Validator:** [`assignments/submit_check.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/submit_check.py)

---

## 🎯 Executive Summary & Learning Objectives

This assignment synthesizes the core mathematical principles, symmetric cryptographic constructions, and asymmetric trapdoor systems mastered during **Days 1, 2, and 3** of the course. You will step into the shoes of both a **cryptographic protocol engineer** and an **offensive cryptanalyst**.

By completing this assignment, you will demonstrate mastery in:
1. **Classical & Information-Theoretic Foundations (Day 1):** Proving Shannon's Perfect Secrecy, evaluating frequency distributions via the Chi-Squared ($\chi^2$) statistic, measuring Index of Coincidence (IC), and exploiting Two-Time Pad key reuse via automated crib dragging.
2. **Abstract Algebra, Number Theory & Symmetric Primitives (Day 2):** Implementing the Extended Euclidean Algorithm, computing modular inverses, building fast modular exponentiation (Square-and-Multiply), analyzing AES block cipher modes (ECB vs CBC vs GCM), and executing the catastrophic AES-GCM Nonce Reuse keystream recovery exploit.
3. **Public-Key Cryptosystems & Trapdoor Security (Day 3):** Simulating Diffie-Hellman Key Exchange (DHKE) over finite cyclic groups, implementing an end-to-end RSA engine from mathematical scratch, assessing semantic security (IND-CPA) and malleability, executing Fermat's Factorization Attack against flawed RSA moduli, and conducting modern Curve25519 (X25519) ECDH key agreement.

---

## 📋 Assignment Structure & Score Allocation

| Section | Topic & Deliverables | Type | Points |
| :--- | :--- | :--- | :---: |
| **Part 1** | **Mathematical Foundations & Theoretical Proofs** | Written Report (`REPORT.md`) | **30 pts** |
| | • Problem 1.1: Information-Theoretic Security & Shannon's Theorem | Proof & Derivation | 10 pts |
| | • Problem 1.2: AES Architecture & Cipher Mode Analysis | Architecture & Analysis | 10 pts |
| | • Problem 1.3: RSA Correctness via CRT & Chosen-Ciphertext Attack | Mathematical Proof | 10 pts |
| **Part 2** | **Core Algorithm Implementation from Scratch** | Python Code (`student.py`) | **40 pts** |
| | • Task 2.1: Simple Classical Cipher (Caesar Encrypt & Decrypt) | Python Functions | 8 pts |
| | • Task 2.2: Statistical Cryptanalysis ($\chi^2$, IC, Auto-Caesar) | Python Functions | 8 pts |
| | • Task 2.3: Number Theory Primitives (Ext-GCD, ModInv, PowMod) | Python Functions | 8 pts |
| | • Task 2.4: Modern Symmetric AEAD (AES-256-GCM with Tamper Verification) | Python Functions | 8 pts |
| | • Task 2.5: Complete RSA Engine & Curve25519 ECDH Key Exchange | Python Functions | 8 pts |
| **Part 3** | **Applied Offensive Cryptanalysis & Incident Response** | Attack Scripts & Analysis | **30 pts** |
| | • Attack 3.1: Two-Time Pad Keystream Recovery & Crib Dragging | Attack Implementation | 10 pts |
| | • Attack 3.2: AES-GCM Nonce Reuse Stream Exploit | Attack Implementation | 10 pts |
| | • Attack 3.3: Fermat's Factorization Attack on Weak RSA | Attack Implementation | 10 pts |
| **Bonus** | **Extra Credit: Automated Vigenère Polyalphabetic Breaker** | Advanced Attack | **+15 pts** |
| **Total** | | | **100 pts (+15)** |

---

# 📖 Part 1: Mathematical Foundations & Rigorous Proofs (30 Points)

Write your rigorous derivations in [`assignments/REPORT_TEMPLATE.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE.md) (or compile into a clean PDF).

### Problem 1.1: Information-Theoretic Security & Shannon's Theorem (10 Points)
1. **Definition of Perfect Secrecy:** Claude Shannon (1949) defined that an encryption scheme $(\text{Gen}, \text{Enc}, \text{Dec})$ over message space $\mathcal{M}$ and ciphertext space $\mathcal{C}$ achieves *Perfect Secrecy* if and only if:
   $$P(M = m \mid C = c) = P(M = m) \quad \forall m \in \mathcal{M}, \forall c \in \mathcal{C}$$
   Prove rigorously using **Bayes' Theorem** that the One-Time Pad ($C = M \oplus K$, where $K \leftarrow \{0, 1\}^L$ uniformly at random) achieves perfect secrecy. Show all intermediate probabilistic steps. (5 pts)
2. **Shannon's Lower Bound on Key Size:** Prove that for any cipher achieving perfect secrecy, the key space $|\mathcal{K}|$ must be at least as large as the message space $|\mathcal{M}|$ (i.e., $|\mathcal{K}| \ge |\mathcal{M}|$). Explain the real-world operational consequence known as the **Key Distribution Paradox**. (5 pts)

### Problem 1.2: AES Architectural Analysis & Mode Security Comparison (10 Points)
1. **Confusion & Diffusion in AES:**
   * Explain how the **SubBytes** step provides *Confusion* via non-linear inversion over the Galois Field $\text{GF}(2^8)$ followed by an affine transformation.
   * Explain how the combination of **ShiftRows** and **MixColumns** achieves *Diffusion* (avalanche effect). What is the branch number of the MixColumns Maximum Distance Separable (MDS) matrix? (4 pts)
2. **Electronic Codebook (ECB) Mode IND-CPA Failure:**
   * Formally describe the **IND-CPA (Indistinguishability under Chosen-Plaintext Attack)** security game between an Adversary $\mathcal{A}$ and a Challenger.
   * Show an adversarial strategy against AES-ECB with success probability $P(\text{Win}) = 1.0$ using a single query to the encryption oracle. (3 pts)
3. **AES-GCM (Galois/Counter Mode) Mechanics:**
   * Explain how AES-GCM combines counter-mode encryption (CTR) with the GHASH polynomial authenticator over $\text{GF}(2^{128})$.
   * Detail what happens when an implementation **reuses the 96-bit Nonce $N$** across two distinct messages under the same key $K$. Explain both the loss of **Confidentiality** ($C_1 \oplus C_2$) and the loss of **Integrity** (recovery of the authentication hash key $H$). (3 pts)

### Problem 1.3: RSA Correctness Proof & Malleability Analysis (10 Points)
1. **RSA Decryption Proof:** Let $N = p \cdot q$ with distinct primes $p, q$. Let $e, d$ satisfy $e \cdot d \equiv 1 \pmod{\phi(N)}$, where $\phi(N) = (p-1)(q-1)$.
   Prove that for **every** message $M \in \mathbb{Z}_N$ (including when $\gcd(M, N) > 1$):
   $$(M^e)^d \equiv M \pmod N$$
   *Hint: Apply Fermat's Little Theorem modulo $p$ and modulo $q$, then invoke the Chinese Remainder Theorem (CRT).* (5 pts)
2. **Chosen-Ciphertext Attack (CCA1) on Textbook RSA:**
   * Textbook RSA is strictly deterministic: $C = M^e \bmod N$.
   * Suppose an adversary intercepts ciphertext $C = M^e \bmod N$. The adversary cannot ask the decryption oracle to decrypt $C$, but is allowed one query for any ciphertext $C' \neq C$.
   * Formulate the mathematical attack that allows the adversary to choose a blinding factor $r \in \mathbb{Z}_N^*$, construct $C'$, query the oracle for $M' = \text{Dec}(C')$, and recover $M$.
   * Why does modern **RSA-OAEP (Optimal Asymmetric Encryption Padding)** completely eliminate this vulnerability? (5 pts)

---

# 💻 Part 2: Practical Implementation Tasks (40 Points)

Open [`assignments/assignment_days_1_to_3_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_days_1_to_3_student.py). Complete all functions marked with `# TODO: YOUR CODE HERE`.

### Task 2.1: Simple Classical Cipher (Caesar Encrypt & Decrypt) (8 Points)
* `caesar_encrypt(plaintext: str, shift: int) -> str`: Encrypt `plaintext` using the classical Caesar Shift Cipher modulo 26 ($C_i = (P_i + \text{shift}) \bmod 26$).
  * Preserves uppercase and lowercase casing (`'A'..'Z'` and `'a'..'z'`).
  * Non-alphabetic characters (spaces, punctuation, digits) must remain unchanged.
  * Correctly handles shifts greater than 26 or negative shifts via modulo arithmetic.
* `caesar_decrypt(ciphertext: str, shift: int) -> str`: Decrypt `ciphertext` by reversing the shift transformation ($P_i = (C_i - \text{shift}) \bmod 26$).

### Task 2.2: Classical Statistical Cryptanalysis (8 Points)
* `compute_chi_squared(text: str) -> float`: Compute the $\chi^2$ statistic comparing the observed letter frequencies of `text` against natural English text distributions.
  $$\chi^2 = \sum_{i \in \{A..Z\}} \frac{(O_i - E_i)^2}{E_i}$$
* `compute_index_of_coincidence(text: str) -> float`: Calculate the Index of Coincidence (IC) metric:
  $$\text{IC} = \frac{\sum_{i=A}^Z f_i (f_i - 1)}{N (N - 1)}$$
* `auto_break_caesar(ciphertext: str) -> tuple[int, str]`: Automatically exhaust all 26 shift keys, evaluate the candidate plaintexts using $\chi^2$, and return the optimal shift key and decrypted string.

### Task 2.3: Number Theory Primitives from Scratch (8 Points)
*Do not use Python's built-in 3-argument `pow(base, exp, mod)` inside `pow_mod()`, and do not use external math libraries for modular inversion.*
* `extended_gcd(a: int, b: int) -> tuple[int, int, int]`: Implement the Extended Euclidean Algorithm. Return `(g, x, y)` such that $a \cdot x + b \cdot y = g = \gcd(a, b)$.
* `modinv(a: int, m: int) -> int`: Compute the modular multiplicative inverse $a^{-1} \pmod m$. Raise `ValueError` if $\gcd(a, m) \neq 1$.
* `pow_mod(base: int, exp: int, mod: int) -> int`: Implement Fast Modular Exponentiation using the **Square-and-Multiply (Binary Exponentiation)** algorithm in $\mathcal{O}(\log \text{exp})$ time.

### Task 2.4: Modern Symmetric AEAD (AES-256-GCM) (8 Points)
* `encrypt_aes_gcm(plaintext: str, key: bytes, aad: bytes = b"") -> tuple[bytes, bytes]`: Encrypt `plaintext` using AES-256-GCM with a securely generated 96-bit (12-byte) random nonce. Return `(nonce, ciphertext_with_tag)`.
* `decrypt_aes_gcm(nonce: bytes, ciphertext_with_tag: bytes, key: bytes, aad: bytes = b"") -> str`: Decrypt the ciphertext and verify the 16-byte authentication tag against the provided `aad`. If tampering is detected, ensure the function allows the cryptography exception to trigger.

### Task 2.5: Complete RSA Engine & Curve25519 ECDH (8 Points)
* `rsa_keygen(p: int, q: int, e: int = 65537) -> tuple[tuple[int, int], tuple[int, int]]`: Generate RSA public key $(N, e)$ and private key $(N, d)$ given prime factors $p$ and $q$.
* `rsa_encrypt(message_int: int, public_key: tuple[int, int]) -> int`: Encrypt an integer message: $C = M^e \bmod N$.
* `rsa_decrypt(ciphertext_int: int, private_key: tuple[int, int]) -> int`: Decrypt an integer ciphertext: $M = C^d \bmod N$.
* `ecdh_x25519_key_exchange() -> tuple[bytes, bytes]`: Generate ephemeral Curve25519 keypairs for Alice and Bob, compute the mutual shared secret via ECDH, and return `(alice_shared, bob_shared)`.

---

# ⚔️ Part 3: Applied Offensive Cryptanalysis & Incident Response (30 Points)

### Attack 3.1: Two-Time Pad Keystream Recovery & Crib Dragging (10 Points)
* Scenario: You have intercepted two encrypted diplomatic telegrams $C_1$ and $C_2$ generated using a One-Time Pad, but the operator negligently reused the exact same secret key:
  $$C_1 = M_1 \oplus K, \quad C_2 = M_2 \oplus K \implies C_1 \oplus C_2 = M_1 \oplus M_2$$
* Task: Implement `two_time_pad_crib_drag(c1_bytes: bytes, c2_bytes: bytes, crib: str) -> list[tuple[int, str]]`. Slide candidate crib words across $C_1 \oplus C_2$ and recover the target plaintext.

### Attack 3.2: AES-GCM Nonce Reuse Keystream Recovery (10 Points)
* Scenario: A flawed financial API transmits JSON wire payments using AES-256-GCM. Because of an initialization bug, the same 12-byte nonce was reused across two successive payment transfers under the identical 256-bit symmetric key.
* Task: Implement `exploit_gcm_nonce_reuse(c1_payload: bytes, c2_payload: bytes) -> bytes`.
* Verify that given $C_1$ (with known plaintext $P_1$) and $C_2$ (with unknown target plaintext $P_2$), you can directly compute:
  $$P_2 = C_2 \oplus (C_1 \oplus P_1)$$
  Extract the unauthorized wire amount and destination account number.

### Attack 3.3: Fermat's Factorization Attack on Weak RSA (10 Points)
* Scenario: An IoT hardware vendor manufactured security cameras with a flawed prime generation routine: $p$ and $q$ were chosen such that $|p - q| < 2 N^{1/4}$.
* Task: Implement `fermat_factor(N: int) -> tuple[int, int]` using Fermat's difference-of-squares method ($N = a^2 - b^2 = (a-b)(a+b)$).
* Implement `crack_rsa_ciphertext(N: int, e: int, ciphertext: int) -> int` to factor $N$, derive the private exponent $d$, and decrypt the intercepted video feed authentication token.

---

# 🌟 Extra Credit: Automated Vigenère Cipher Breaker (+15 Points)

* Implement `crack_vigenere_cipher(ciphertext: str, max_key_len: int = 10) -> tuple[str, str]`:
  1. Determine the key length $m$ by computing the average Index of Coincidence across $m$ interleaved cosets.
  2. Slice the ciphertext into $m$ independent Caesar ciphers.
  3. Run the $\chi^2$ automated breaker on each slice to recover each keyword character.
  4. Return the discovered keyword and full decrypted text.

---

# 📦 Detailed Submission Instructions

Follow these instructions to package and submit your work:

### 1. Deliverables Checklist
Before submitting, ensure your submission contains the following files:
```text
assignments/
├── assignment_days_1_to_3_student.py  # Your completed implementation code
├── REPORT.md                         # Your mathematical proofs, answers & attack analysis
└── submission_metadata.json          # Generated by the validator script
```

### 2. Pre-Submission Self-Test & Validation
We have provided an automated pre-submission script that checks your code, runs the test suite, validates your report, and computes a cryptographic SHA-256 integrity receipt.

Run the validator from the project root:
```bash
python3 assignments/submit_check.py --student-id "YOUR_STUDENT_ID" --name "YOUR_FULL_NAME"
```

Expected output:
```text
======================================================================
🎓 MODERN CRYPTOGRAPHY ASSIGNMENT (DAYS 1-3) PRE-FLIGHT CHECKER
======================================================================
[+] Validating student information: Jane Doe (ID: 65070001)
[+] Running Automated Test Suite...
    -> Task 2.1: Statistical Cryptanalysis ................ [ PASS ]
    -> Task 2.2: Number Theory Primitives ................. [ PASS ]
    -> Task 2.3: Modern Symmetric AEAD (AES-GCM) .......... [ PASS ]
    -> Task 2.4: RSA Engine & Curve25519 .................. [ PASS ]
    -> Attack 3.1: Two-Time Pad Crib Drag ................. [ PASS ]
    -> Attack 3.2: AES-GCM Nonce Reuse .................... [ PASS ]
    -> Attack 3.3: Fermat RSA Factorization ............... [ PASS ]
    -> Bonus Task: Automated Vigenère Breaker ............. [ PASS ]
[+] Automated Test Score: 70/70 Code Points (+15 Bonus)
[+] Validating REPORT.md completeness ..................... [ PASS ]
[+] Calculating SHA-256 Submission Checksum ............... [ DONE ]
[+] Packaging submission: submission_65070001_days1_to_3.zip [ CREATED ]
======================================================================
🚀 ALL PRE-FLIGHT CHECKS PASSED! Ready for submission.
======================================================================
```

### 3. Submission Methods

#### Method A: Learning Management System (Canvas / Moodle / Blackboard)
1. Run `python3 assignments/submit_check.py --student-id "<YOUR_STUDENT_ID>" --name "<YOUR_NAME>"`.
2. Upload the generated zip file `submission_<YOUR_STUDENT_ID>_days1_to_3.zip` to the assignment portal on your course LMS.
3. Save your generated SHA-256 verification hash as proof of on-time submission.

#### Method B: Git / GitHub Classroom
If your course uses GitHub Classroom or GitLab:
1. Ensure your changes are on a clean submission branch:
   ```bash
   git checkout -b submission-days1-to-3
   git add assignments/assignment_days_1_to_3_student.py assignments/REPORT.md
   git commit -m "Submit Class Assignment (Days 1-3) - [Your Name] - [Student ID]"
   git tag -a v1.0-submission -m "Final Submission"
   git push origin submission-days1-to-3 --tags
   ```
2. Verify that your GitHub Actions autograder workflow turns green.

---

## ⚖️ Academic Integrity & AI Policy

* **Honor Code:** All code and written mathematical proofs must represent your own intellectual work.
* **AI Assistance Policy:** You may use AI assistants (such as Antigravity, ChatGPT, Claude) as interactive tutors to clarify concepts and debug syntax errors. However, **you must be able to explain every line of code and mathematical derivation in an oral code defense if requested by teaching staff**. Direct copying of unverified AI outputs without comprehension is a violation of the Academic Integrity Policy.
* **Collaboration:** High-level conceptual discussions with peers are encouraged, but sharing code, copy-pasting solutions, or distributing test exploits is strictly prohibited.

---

## 📊 Comprehensive Grading Rubric

```text
Total Score: 100 Points (+15 Extra Credit)

Part 1: Theory & Mathematical Proofs (30 Points)
├── Problem 1.1 (10 pts): Shannon Perfect Secrecy proof (5 pts) + Key Size Bound (5 pts)
├── Problem 1.2 (10 pts): AES Confusion/Diffusion (4 pts) + ECB IND-CPA (3 pts) + GCM Nonce Reuse (3 pts)
└── Problem 1.3 (10 pts): RSA CRT Proof (5 pts) + Chosen-Ciphertext Attack & OAEP (5 pts)

Part 2: Core Algorithm Implementation (40 Points)
├── Task 2.1 (10 pts): Chi-Squared & IC (5 pts) + Caesar Auto-Breaker (5 pts)
├── Task 2.2 (10 pts): Extended Euclidean (4 pts) + ModInv (3 pts) + PowMod (3 pts)
├── Task 2.3 (10 pts): AES-256-GCM Encrypt/Decrypt (6 pts) + Tamper Exception (4 pts)
└── Task 2.4 (10 pts): RSA Keygen/Enc/Dec (6 pts) + Curve25519 ECDH (4 pts)

Part 3: Offensive Cryptanalysis (30 Points)
├── Attack 3.1 (10 pts): Two-Time Pad Crib Dragging Implementation & Message Recovery
├── Attack 3.2 (10 pts): AES-GCM Keystream Recovery & Target Plaintext Extraction
└── Attack 3.3 (10 pts): Fermat Factorization of Weak Modulus & Private Key Derivation

Bonus Extra Credit (+15 Points)
└── Bonus 3.4 (15 pts): Autonomous Vigenère Cipher Breaker (IC Key Length + Chi-Sq Column Solving)
```
