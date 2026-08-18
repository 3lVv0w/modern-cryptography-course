# 📘 DAY 1 LEARNING MATERIAL: Classical Cryptanalysis & Information Theory
**Course:** Modern Cryptography & Network Security (CS-4XX / ECE-4XX)  
**Target Audience:** University Computer Science & Engineering Students  
**Prerequisites:** Elementary Probability, Basic Modular Math, Python 3  

---

## 📜 Real-World Story: "The Intercepted Wiretap & The Venona Key Reuse Incident"

> **Setting:** Cold War Espionage (Project Venona, 1943)  
> **Core Concepts:** One-Time Pad (OTP), Information-Theoretic Security, Two-Time Pad Key Reuse Exploit.

In 1943 during World War II, Soviet intelligence agents transmitted thousands of encrypted diplomatic cables between Moscow and Washington D.C. To guarantee secrecy, they used the **One-Time Pad (OTP)**—a cryptosystem mathematically proven by Claude Shannon to achieve **Perfect Secrecy** ($P(M=m \mid C=c) = P(M=m)$).

However, generating true random keys in huge volumes was tedious. A factory printing OTP keybooks in Moscow accidentally printed duplicate pages of key material and distributed them to different diplomatic posts.

US Army Signals Intelligence Service cryptanalyst Meredith Gardner noticed that several encrypted messages shared identical key material. When two plaintexts $M_1$ and $M_2$ are encrypted with the same key $K$:
* $C_1 = M_1 \oplus K$
* $C_2 = M_2 \oplus K$
* $C_1 \oplus C_2 = (M_1 \oplus K) \oplus (M_2 \oplus K) = M_1 \oplus M_2$

The key $K$ vanished completely! By sliding common Russian words (a technique called **Crib Dragging**, such as guessing `"DIPLOMATIC"` or `"MINISTRY"`), Western cryptanalysts gradually unraveled the XORed payload $M_1 \oplus M_2$, recovering both messages and exposing top-secret atomic spy rings.

**The Lesson:** A cryptosystem with mathematical "Perfect Secrecy" becomes 100% vulnerable if operational rules are violated. **Never reuse a One-Time Pad key!**

---

## 🎯 Day 1 Learning Objectives
By the end of Day 1, students will be able to:
1. Formally define classical substitution ciphers over the ring $\mathbb{Z}_{26}$.
2. Analyze the vulnerability of monoalphabetic ciphers to statistical frequency analysis.
3. Calculate the **Index of Coincidence (IC)** and apply Kasiski Examination to estimate polyalphabetic key lengths.
4. Derive Claude Shannon's mathematical proof of **Perfect Secrecy** for the One-Time Pad (OTP).
5. Explain the **Key Distribution Paradox** and compare Stream Ciphers with Block Ciphers.

---

# 📖 Module 1.1: Classical Ciphers & Cryptanalysis

### 1. The Caesar (Shift) Cipher over $\mathbb{Z}_{26}$
The Caesar cipher is a monoalphabetic substitution cipher where each character in the plaintext is shifted by a fixed integer key $k \in \{0, 1, \dots, 25\}$.

#### Mathematical Definition:
Let the alphabet be mapped to integers $\mathbb{Z}_{26} = \{0, 1, 2, \dots, 25\}$ where $A=0, B=1, \dots, Z=25$.
* **Key Space:** $\mathcal{K} = \{0, 1, 2, \dots, 25\}$ ($|\mathcal{K}| = 25$ non-trivial keys).
* **Encryption Function:**
  $$e_k(m_i) = (m_i + k) \bmod 26$$
* **Decryption Function:**
  $$d_k(c_i) = (c_i - k) \bmod 26$$

#### Vulnerability (Exhaustive Key Search):
Because the key space $|\mathcal{K}| = 25$ is extremely small, an attacker under the **Ciphertext-Only Attack (COA)** model can brute-force all 25 possible keys in milliseconds.

---

### 2. Frequency Analysis & Natural Language Redundancy
Languages are not uniform random noise; they contain statistical redundancy. In standard English prose, letter probabilities are highly skewed:

```
Letter Frequency Distribution in English:
E: 12.70%    T: 9.06%    A: 8.17%    O: 7.51%    I: 6.97%    N: 6.75%
S: 6.33%     H: 6.09%    R: 5.98%    D: 4.25%    L: 4.03%    C: 2.78%
```

#### Chi-Squared ($\chi^2$) Statistical Scoring:
To programmatically find the correct shift key $k$, we compute the Chi-Squared statistic between candidate decrypted letter counts and expected English frequencies:

$$\chi^2 = \sum_{i=A}^{Z} \frac{(\text{Observed}_i - \text{Expected}_i)^2}{\text{Expected}_i}$$

Where $\text{Expected}_i = N \times \left(\frac{\text{Frequency}_i}{100}\right)$ for text length $N$.  
The shift key $k$ that minimizes $\chi^2$ is the true decryption key.

---

### 3. Polyalphabetic Substitution: The Vigenère Cipher
To defeat single-letter frequency analysis, the Vigenère cipher uses a repeating keyword $K = (k_0, k_1, \dots, k_{m-1})$ of length $m$.

#### Mathematical Definition:
$$e_K(m_i) = (m_i + k_{i \bmod m}) \bmod 26$$

#### Polyalphabetic Cryptanalysis:
1. **Kasiski Examination:** Search for repeating n-grams (e.g. 3-letter sequences) in the ciphertext. The distance $D$ between repetitions is likely a multiple of the key length $m$.
2. **Index of Coincidence (IC):** Measures the probability that two randomly chosen letters from a text are identical.
   $$\text{IC}(T) = \frac{\sum_{i=A}^Z f_i(f_i - 1)}{N(N - 1)}$$
   * **Uniform Random Text:** $\text{IC} \approx \frac{1}{26} \approx 0.0385$
   * **Monolingual English Text:** $\text{IC} \approx \sum p_i^2 \approx 0.0667$

---

# 📖 Module 1.2: Information-Theoretic Security & One-Time Pad (OTP)

### 1. Claude Shannon's Perfect Secrecy (1949)
A cryptosystem achieves **Information-Theoretic Security (Perfect Secrecy)** if the ciphertext provides zero information about the plaintext to an adversary with infinite computational power.

#### Formal Mathematical Definition:
A cryptosystem $(\mathcal{P}, \mathcal{C}, \mathcal{K}, E, D)$ achieves Perfect Secrecy if for all plaintexts $m \in \mathcal{P}$ and ciphertexts $c \in \mathcal{C}$ with $P(C=c) > 0$:

$$P(M = m \mid C = c) = P(M = m)$$

---

### 2. The One-Time Pad (OTP)
The One-Time Pad (OTP) encrypts $L$-bit binary plaintext $M$ using an $L$-bit random key $K$ via bitwise XOR ($\oplus$).

#### Mathematical Protocol:
* **Encryption:** $C = M \oplus K$
* **Decryption:** $M = C \oplus K$

#### Formal Proof of OTP Perfect Secrecy:
We want to prove $P(M = m \mid C = c) = P(M = m)$.
By Bayes' Theorem:
$$P(M = m \mid C = c) = \frac{P(C = c \mid M = m) \cdot P(M = m)}{P(C = c)}$$

1. Compute $P(C = c \mid M = m)$:
   $$P(C = c \mid M = m) = P(M \oplus K = c \mid M = m) = P(K = m \oplus c)$$
   Since key $K$ is selected uniformly at random from $\{0, 1\}^L$:
   $$P(K = m \oplus c) = \frac{1}{2^L}$$

2. Compute $P(C = c)$:
   $$P(C = c) = \sum_{m' \in \mathcal{P}} P(C = c \mid M = m') \cdot P(M = m') = \sum_{m'} \frac{1}{2^L} \cdot P(M = m') = \frac{1}{2^L} \sum_{m'} P(M = m') = \frac{1}{2^L}$$

3. Substitute back into Bayes' Theorem:
   $$P(M = m \mid C = c) = \frac{\frac{1}{2^L} \cdot P(M = m)}{\frac{1}{2^L}} = P(M = m) \quad \blacksquare$$

---

### 3. The Three Mandatory Rules of OTP
To maintain perfect secrecy, OTP requires:
1. **True Randomness:** Key $K$ must be generated using a True Random Number Generator (TRNG).
2. **Key Length:** $|K| \ge |M|$ (Key must be at least as long as the message).
3. **Never Reused:** Key $K$ must be used **exactly ONCE**.

---

# 📖 Module 1.3: Symmetric Cipher Architecture

```
                       SYMMETRIC CIPHERS
                              │
         ┌────────────────────┴────────────────────┐
         ▼                                         ▼
   STREAM CIPHERS                            BLOCK CIPHERS
 (Encrypt bit-by-bit)                    (Encrypt fixed blocks)
  e.g., ChaCha20, LFSR                    e.g., AES-256, DES
```

---

## 🎮 Day 1 Gamification: "The Human Frequency Decoder"
* **Goal:** Break a physical Caesar-encrypted text using paper tally sheets and letter frequency charts before other teams!

---

## 💻 Day 1 Hands-On Lab Assignment
Students must complete `day1/lab_student.py` in terminal:
```bash
python3 day1/lab_student.py
```
Target Score: **100% (5/5 Tests Passed)**.
