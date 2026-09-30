# 🎓 Day 1 Focus Class Assignment: Classical Ciphers & Wheel Mechanics
## Short & Long Message Processing: With vs. Without Mechanical Wheel Support
**Course:** Modern Cryptography & Network Security (CS-4XX / ECE-4XX)  
**Module:** Day 1 — Substitution Ciphers, Concentric Cipher Disks & Rotor Stream Processing

* 🌐 **Language / ภาษา:** [🇺🇸 English Version](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_DAY1.md) | [🇹🇭 ฉบับภาษาไทย (Thai Version)](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_DAY1_TH.md)
* **Target Audience:** Undergraduate & Graduate CS/ECE Students, Cryptography & Cybersecurity Learners
* **Focus Module:** Day 1 (Classical Cryptanalysis & Information Theory)
* **Due Date:** Sunday 23:59:59 (7 Days from Assignment Date)
* **Total Points:** 100 Points (+ 10 Points Extra Credit / Bonus)
* **Starter Code:** [`assignments/assignment_day1_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_day1_student.py)
* **Report Template:** [`assignments/REPORT_TEMPLATE_DAY1.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_DAY1.md) (or [`REPORT_TEMPLATE_DAY1_TH.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_DAY1_TH.md))
* **Submission Validator:** [`assignments/submit_check_day1.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/submit_check_day1.py)

---

## 🎯 Executive Summary & Learning Objectives

During **Day 1** of our cryptography journey, we explored the foundations of secrecy: how humans historically concealed military messages, and how physical mechanical devices like the **Alberti Concentric Cipher Disk (1467)** bridged the gap between manual pen-and-paper encryption and automated rotor engines.

This assignment focuses specifically on the dual paradigms of classical cryptography:
1. **Mathematical / Direct Approach (Without Wheel Support):** Performing fast modular arithmetic over the finite ring $\mathbb{Z}_{26}$ ($C = (P + k) \bmod 26$).
2. **Mechanical / Dial Approach (With Wheel Support):** Simulating a physical concentric two-disk rotor mechanism, tracking mechanical wheel alignment, and visually looking up letter pairs along concentric tracks.

You will implement both approaches for **short tactical commands** and **long multi-line diplomatic dispatches**, prove that both physical wheels and digital math produce identical ciphertexts, investigate why stepping rotor wheels defeat monoalphabetic frequency attacks, and crack an intercepted battlefield cable.

---

## 📋 Assignment Structure & Score Allocation (5 Questions)

| Question | Topic & Deliverables | Method | Points |
| :---: | :--- | :---: | :---: |
| **Question 1** | **Short Message Processing Without Wheel Support** | Direct Modular Math ($\mathbb{Z}_{26}$) | **20 pts** |
| | • `caesar_direct_encrypt(plaintext, shift)` | Python Function | 10 pts |
| | • `caesar_direct_decrypt(ciphertext, shift)` | Python Function | 10 pts |
| **Question 2** | **Short Message Processing With Wheel Support** | Mechanical Concentric Wheel Simulation | **20 pts** |
| | • `CipherWheel` class implementation & ASCII dial rendering | Python Class | 10 pts |
| | • `wheel_encrypt_short()` & `wheel_decrypt_short()` | Python Functions | 10 pts |
| **Question 3** | **Long Message Processing & Equivalence Verification** | Stream Processing & Performance | **20 pts** |
| | • `process_long_message_direct(text, shift, mode)` | Python Function | 10 pts |
| | • `process_long_message_wheel(text, wheel, mode)` & Equivalence Check | Python Function & Report | 10 pts |
| **Question 4** | **Progressive Rotor Advance (Stepping Wheel Cipher)** | Dynamic Polyalphabetic Stream | **20 pts** |
| | • `progressive_wheel_encrypt(plaintext, initial_shift, step)` | Python Function | 10 pts |
| | • `progressive_wheel_decrypt(ciphertext, initial_shift, step)` | Python Function | 10 pts |
| **Question 5** | **Applied Cryptanalysis & Intercepted Cable Cracking** | Ciphertext-Only Attack (COA) | **20 pts** |
| | • `crack_without_wheel(ciphertext, clue_word)` | Direct Math Loop | 10 pts |
| | • `crack_with_wheel(ciphertext, wheel, clue_word)` | Wheel Rotation Scan | 10 pts |
| **Bonus** | **Extra Credit: Keyed Scrambled Alphabet Wheel** | Custom Substituted Inner Disk | **+10 pts** |
| **Total** | | | **100 pts (+10)** |

---

# 📖 The 5 Assignment Questions in Detail

Open [`assignments/assignment_day1_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_day1_student.py). Complete each section marked `# TODO: YOUR CODE HERE`.

---

### 📝 Question 1: Short Message Processing Without Wheel Support (20 Points)

In this question, you will implement classical Caesar encryption and decryption without any wheel state, relying purely on modular arithmetic:

$$C_i = (P_i + \text{shift}) \bmod 26$$
$$P_i = (C_i - \text{shift}) \bmod 26$$

#### Specifications:
* `caesar_direct_encrypt(plaintext: str, shift: int) -> str`:
  * Shifts each alphabetic character forward by `shift` places.
  * Preserves exact uppercase and lowercase casing.
  * Leaves spaces, punctuation, numbers, and symbols untouched.
  * Handles shifts greater than 26 or negative shifts correctly using modulo arithmetic.
* `caesar_direct_decrypt(ciphertext: str, shift: int) -> str`:
  * Reverses the encryption transformation.

---

### 🎡 Question 2: Short Message Processing With Wheel Support (20 Points)

In 1467, Leon Battista Alberti introduced the first mechanical cipher disk: two concentric circular plates where an outer stationary disk (Plaintext: A–Z) aligns against an inner rotatable disk (Ciphertext: A–Z rotated by $k$).

```
+-------------------------------------------------------------------+
| 🎡 CIPHER WHEEL ALIGNMENT (Current Shift: 04)                       |
+-------------------------------------------------------------------+
| Outer Disk (Plaintext) : A B C D E F G H I J K L M N O P Q R S T U V W X Y Z |
| Inner Disk (Ciphertext): E F G H I J K L M N O P Q R S T U V W X Y Z A B C D |
+-------------------------------------------------------------------+
```

#### Specifications:
* Complete the `CipherWheel` class methods in [`assignment_day1_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_day1_student.py):
  * `rotate(steps: int)`: Adjusts the mechanical alignment.
  * `set_shift(shift: int)`: Directly aligns the wheel to a specific offset.
  * `get_inner_alphabet() -> str`: Returns the rotated 26-character sequence.
  * `render_ascii_dial() -> str`: Generates the formatted ASCII dial display.
  * `encrypt_char(char: str) -> str` & `decrypt_char(char: str) -> str`: Reads the opposite letter across the wheel tracks.
* Implement:
  * `wheel_encrypt_short(plaintext: str, wheel: CipherWheel) -> str`
  * `wheel_decrypt_short(ciphertext: str, wheel: CipherWheel) -> str`

---

### 📜 Question 3: Long Message Processing & Equivalence (20 Points)

In field operations, encryption must scale beyond a 3-word password to encrypt full reconnaissance reports and diplomatic dispatches containing multi-line paragraphs, numbers, and formatting.

We provide a benchmark historical text: an excerpt from Julius Caesar's *Gallic Wars* (`LONG_HISTORICAL_MESSAGE`, 370 characters).

#### Specifications:
* `process_long_message_direct(text: str, shift: int, mode: str = "encrypt") -> str`:
  * Processes long texts with paragraphs and newlines using direct modular arithmetic.
* `process_long_message_wheel(text: str, wheel: CipherWheel, mode: str = "encrypt") -> str`:
  * Processes long texts using the `CipherWheel` simulation.
* **The Equivalence Theorem:**
  * In your report ([`REPORT_TEMPLATE_DAY1.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_DAY1.md)), record evidence that:
    $$\text{Ciphertext}_{\text{direct}} \equiv \text{Ciphertext}_{\text{wheel}}$$
  * Explain why digital computers abandoned mechanical wheel lookup tables in favor of arithmetic register instructions.

---

### ⚙️ Question 4: Progressive Rotor Advance (Stepping Wheel Cipher) (20 Points)

The fatal flaw of static ciphers (both direct and static wheel) is **monoalphabetic frequency leakage**: the most frequent plaintext letter ('E') always turns into the exact same ciphertext letter.

To overcome this, early mechanical disk designers realized the inner wheel could **step forward 1 notch after each letter encrypted**!

```
Plaintext:  A   A   A   A   A   A
Wheel Pos:  1   2   3   4   5   6
Ciphertext: B   C   D   E   F   G   <-- Look! Identical letters produce unique outputs!
```

#### Specifications:
* `progressive_wheel_encrypt(plaintext: str, initial_shift: int, step: int = 1) -> str`:
  * Initializes wheel at `initial_shift`.
  * For each letter: encrypts with the current wheel alignment, then calls `wheel.rotate(step)`.
  * Non-alphabetic characters (spaces, punctuation) are NOT encrypted and do NOT rotate the wheel.
* `progressive_wheel_decrypt(ciphertext: str, initial_shift: int, step: int = 1) -> str`:
  * Decrypts the progressive stream and steps the wheel identically.

---

### 🕵️ Question 5: Applied Cryptanalysis & Intercepted Cable Cracking (20 Points)

An enemy military wiretap intercepted this confidential diplomatic telegram:
`"AOL JVUMLYLUJL PZ ZJOLKBSLK MVY TPKUPNOA HA AOL OPNI ZLJYLA IBURLY."`

Intelligence operatives know the telegram discusses a `"CONFERENCE"`.

#### Specifications:
* `crack_without_wheel(ciphertext: str, clue_word: str = "THE") -> tuple[int, str]`:
  * Exhaustively tests all 26 shifts mathematically ($0..25$).
  * Searches for `clue_word.upper()` in the decrypted candidates.
  * Returns `(shift, decrypted_plaintext)`.
* `crack_with_wheel(ciphertext: str, wheel: CipherWheel, clue_word: str = "THE") -> tuple[int, str]`:
  * Physically rotates the `CipherWheel` through all 26 mechanical alignments (`set_shift(0..25)`).
  * Decrypts using the wheel and returns `(shift, decrypted_plaintext)`.

---

# 🌟 Bonus Question: Custom Scrambled Alphabet Wheel (+10 Extra Credit)

In standard Caesar wheels, the alphabet on both rings is strictly A to Z in order. In keyed substitution wheels, the inner ring is scrambled using a secret keyword (e.g. `"SECRET"` $\to$ `"SECRTABDFGHIJKLMNOPQUVWXYZ"`).

* Implement `scrambled_wheel_encrypt(plaintext, keyword, shift)` and `scrambled_wheel_decrypt(ciphertext, keyword, shift)`.
* Explain how this expands the key space from 25 to $26! \approx 4 \times 10^{26}$ possible keys.

---

# 🧪 Local Self-Testing & Submission

Run your code locally at any time:
```bash
# Run the Day 1 unit test runner:
python3 assignments/assignment_day1_student.py
```

When all tests pass, run the pre-flight submission validator:
```bash
python3 assignments/submit_check_day1.py --student-id "YOUR_STUDENT_ID" --name "YOUR_FULL_NAME"
```

The script will:
1. Validate your code against all 5 question tests.
2. Confirm that your report ([`REPORT_TEMPLATE_DAY1.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_DAY1.md)) is filled out.
3. Compute SHA-256 cryptographic submission receipts.
4. Package your submission into `assignments/submission_<STUDENT_ID>_day1.zip`.

---

## 📊 Comprehensive Grading Rubric

```text
Total Score: 100 Points (+10 Extra Credit)

Question 1: Short Message Processing Without Wheel Support (20 Points)
├── caesar_direct_encrypt(): 10 pts (Shift, casing, punctuation, wraparound)
└── caesar_direct_decrypt(): 10 pts (Reversing shift cleanly)

Question 2: Short Message Processing With Wheel Support (20 Points)
├── CipherWheel class methods & ASCII dial rendering: 10 pts
└── wheel_encrypt_short() & wheel_decrypt_short(): 10 pts

Question 3: Long Message Processing & Equivalence (20 Points)
├── process_long_message_direct(): 5 pts
├── process_long_message_wheel(): 5 pts
└── Exact Equivalence Verification & Written Performance Analysis: 10 pts

Question 4: Progressive Rotor Stepping Wheel (20 Points)
├── progressive_wheel_encrypt(): 10 pts (Letter advance, punct handling)
└── progressive_wheel_decrypt(): 10 pts (Symmetric reverse step)

Question 5: Applied Cryptanalysis & Cable Cracking (20 Points)
├── crack_without_wheel(): 10 pts (Modular mathematical scan)
└── crack_with_wheel(): 10 pts (Simulated mechanical dial scan)

Bonus Question (+10 Extra Credit)
└── ScrambledKeyedWheel implementation & Key space expansion proof: +10 pts
```
