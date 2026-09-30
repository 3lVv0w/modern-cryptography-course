"""
================================================================================
🎓 DAY 1 FOCUS LAB & CLASS ASSIGNMENT: CLASSICAL CIPHERS & WHEEL MECHANICS
Course: Modern Cryptography & Network Security (CS-4XX / ECE-4XX)
Module: Day 1 — Substitution Ciphers, Mechanical Wheels & Stream Processing
================================================================================
Student Name (ชื่อ-นามสกุล) : ________________________________________
Student ID (รหัสนักศึกษา)   : ________________________________________
Submission Date (วันที่ส่ง) : ________________________________________

INSTRUCTIONS (คำแนะนำ):
This assignment focuses exclusively on Day 1: Encrypting and decrypting short
and long messages, both with and without mechanical wheel support.
1. Complete all functions marked with `# TODO: YOUR CODE HERE`.
2. Do not change function signatures, class interfaces, or return types.
3. Test your code locally at any time:
       python3 assignments/assignment_day1_student.py
4. Pre-flight check and package your submission:
       python3 assignments/submit_check_day1.py --student-id "YOUR_ID" --name "YOUR_NAME"
================================================================================
"""

# Standard English Alphabet for Wheel Mechanics
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ==============================================================================
# 🎡 CIPHER WHEEL MECHANISM CLASS (USED IN QUESTIONS 2, 3, 4, 5)
# ==============================================================================

class CipherWheel:
    """
    Simulation of a physical two-disk concentric cipher wheel (Alberti / Caesar Disk).
    - Outer Ring: Stationary alphabet ['A', 'B', ..., 'Z']
    - Inner Ring: Rotatable alphabet ['A', 'B', ..., 'Z'] shifted by 'shift' positions.
    """

    def __init__(self, shift: int = 0):
        """Initializes the wheel with a rotation offset (modulo 26)."""
        self.shift = shift % 26

    def rotate(self, steps: int = 1):
        """
        Rotates the inner wheel by 'steps' positions clockwise.
        [TH] หมุนวงล้อชั้นในตามเข็มนาฬิกาไป 'steps' ตำแหน่ง
        """
        self.shift = (self.shift + steps) % 26

    def set_shift(self, shift: int):
        """
        Sets the wheel directly to a specific shift position.
        [TH] ตั้งค่าตำแหน่งการเลื่อนของวงล้อโดยตรง
        """
        self.shift = shift % 26

    def get_inner_alphabet(self) -> str:
        """
        Returns the current letter order of the inner rotatable wheel.
        [TH] ส่งคืนลำดับตัวอักษรของวงล้อชั้นในตามตำแหน่งปัจจุบัน
        Example: shift = 3 -> "DEFGHIJKLMNOPQRSTUVWXYZABC"
        """
        return ALPHABET[self.shift:] + ALPHABET[:self.shift]

    def render_ascii_dial(self) -> str:
        """
        Renders a clean ASCII visualization of the concentric cipher wheel alignment.
        [TH] วาดภาพจำลองหน้าปัดวงล้อรหัสลับแบบ ASCII
        """
        outer_str = " ".join(ALPHABET)
        inner_str = " ".join(self.get_inner_alphabet())
        return (
            f"+-------------------------------------------------------------------+\n"
            f"| 🎡 CIPHER WHEEL ALIGNMENT (Current Shift: {self.shift:02d})                       |\n"
            f"+-------------------------------------------------------------------+\n"
            f"| Outer Disk (Plaintext) : {outer_str} |\n"
            f"| Inner Disk (Ciphertext): {inner_str} |\n"
            f"+-------------------------------------------------------------------+"
        )

    def encrypt_char(self, char: str) -> str:
        """
        Encrypts a single character using physical wheel track alignment.
        [TH] เข้ารหัสตัวอักษร 1 ตัวโดยดูจากแนวตรงกันของหน้าปัดวงล้อ
        - Uppercase stays uppercase, lowercase stays lowercase.
        - Non-alphabetic characters remain untouched.
        """
        if not char.isalpha():
            return char
        is_upper = char.isupper()
        plain_idx = ALPHABET.index(char.upper())
        cipher_char = self.get_inner_alphabet()[plain_idx]
        return cipher_char if is_upper else cipher_char.lower()

    def decrypt_char(self, char: str) -> str:
        """
        Decrypts a single character by finding it on the inner disk and reading outer disk.
        [TH] ถอดรหัสตัวอักษร 1 ตัวโดยหาตัวอักษรบนวงล้อชั้นในแล้วอ่านตัวอักษรตรงข้ามบนวงล้อชั้นนอก
        """
        if not char.isalpha():
            return char
        is_upper = char.isupper()
        inner_alphabet = self.get_inner_alphabet()
        inner_idx = inner_alphabet.index(char.upper())
        plain_char = ALPHABET[inner_idx]
        return plain_char if is_upper else plain_char.lower()


# ==============================================================================
# 📝 QUESTION 1: SHORT MESSAGE ENCRYPTION & DECRYPTION WITHOUT WHEEL SUPPORT
# ==============================================================================

def caesar_direct_encrypt(plaintext: str, shift: int) -> str:
    """
    [Question 1] Encrypts a short message WITHOUT wheel support using modular math.
    [TH] เข้ารหัสข้อความสั้นแบบไม่มีวงล้อ โดยใช้สูตรคณิตศาสตร์มอดุโล 26 โดยตรง

    Formula: C_i = (P_i + shift) mod 26
    
    Requirements:
    - Shift letters forward using ASCII offsets (ord and chr).
    - Preserves exact upper/lower casing.
    - Preserves spaces, punctuation, and digits.
    - Handles negative shifts or shifts > 26 cleanly.

    Example / ตัวอย่าง:
        caesar_direct_encrypt("ATTACK AT DAWN", 3) -> "DWWDFN DW GDZQ"
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Question 1: Implement caesar_direct_encrypt")


def caesar_direct_decrypt(ciphertext: str, shift: int) -> str:
    """
    [Question 1] Decrypts a short message WITHOUT wheel support using modular math.
    [TH] ถอดรหัสข้อความสั้นแบบไม่มีวงล้อ โดยใช้สูตรคณิตศาสตร์มอดุโล 26 โดยตรง

    Formula: P_i = (C_i - shift) mod 26
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Question 1: Implement caesar_direct_decrypt")


# ==============================================================================
# 🎡 QUESTION 2: SHORT MESSAGE ENCRYPTION & DECRYPTION WITH WHEEL SUPPORT
# ==============================================================================

def wheel_encrypt_short(plaintext: str, wheel: CipherWheel) -> str:
    """
    [Question 2] Encrypts a short message WITH wheel support using the CipherWheel instance.
    [TH] เข้ารหัสข้อความสั้นแบบมีวงล้อช่วย โดยจำลองการอ่านหน้าปัดวงล้อ CipherWheel

    Process:
    - Uses wheel.encrypt_char() on each character.
    - The wheel's shift position remains fixed for the entire message.
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Question 2: Implement wheel_encrypt_short")


def wheel_decrypt_short(ciphertext: str, wheel: CipherWheel) -> str:
    """
    [Question 2] Decrypts a short message WITH wheel support using the CipherWheel instance.
    [TH] ถอดรหัสข้อความสั้นแบบมีวงล้อช่วย โดยจำลองการอ่านหน้าปัดวงล้อ CipherWheel

    Process:
    - Uses wheel.decrypt_char() on each character.
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Question 2: Implement wheel_decrypt_short")


# ==============================================================================
# 📜 QUESTION 3: LONG MESSAGE PROCESSING & EQUIVALENCE (WITH VS WITHOUT WHEEL)
# ==============================================================================

def process_long_message_direct(text: str, shift: int, mode: str = "encrypt") -> str:
    """
    [Question 3] Encrypts or decrypts a LONG multi-line message WITHOUT wheel support.
    [TH] เข้ารหัสหรือถอดรหัสข้อความยาวหลายบรรทัดแบบไม่มีวงล้อ โดยใช้สูตรคณิตศาสตร์

    Parameters:
    - text: A long text string (may contain multiple paragraphs, newlines '\n', numbers).
    - shift: Integer shift key.
    - mode: "encrypt" or "decrypt".
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Question 3: Implement process_long_message_direct")


def process_long_message_wheel(text: str, wheel: CipherWheel, mode: str = "encrypt") -> str:
    """
    [Question 3] Encrypts or decrypts a LONG multi-line message WITH wheel support.
    [TH] เข้ารหัสหรือถอดรหัสข้อความยาวหลายบรรทัดแบบมีวงล้อช่วย โดยใช้ CipherWheel

    Parameters:
    - text: A long text string with paragraphs and formatting.
    - wheel: Configured CipherWheel instance.
    - mode: "encrypt" or "decrypt".
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Question 3: Implement process_long_message_wheel")


# ==============================================================================
# ⚙️ QUESTION 4: PROGRESSIVE ROTOR ADVANCE (STEPPING WHEEL CIPHER)
# ==============================================================================

def progressive_wheel_encrypt(plaintext: str, initial_shift: int, step: int = 1) -> str:
    """
    [Question 4] Encrypts text using a STEPPING wheel that physically rotates after each letter.
    [TH] เข้ารหัสข้อความด้วยวงล้อแบบก้าวหมุน (Stepping Wheel) ที่ขยับหมุน 1 กริ๊กหลังเข้ารหัสตัวอักษร

    Mechanism / กลไกการทำงาน:
    1. Initialize CipherWheel with initial_shift.
    2. For each character in plaintext:
       - If character is a letter (char.isalpha()):
           - Encrypt character with current wheel alignment.
           - Rotate wheel: wheel.rotate(step)
       - If character is not a letter (space, punct):
           - Keep unchanged, DO NOT rotate the wheel!
    3. Return resulting ciphertext.

    Why this matters / ทำไมจึงสำคัญ:
    - This turns a monoalphabetic cipher into a polyalphabetic stream!
    - Repeated identical letters (e.g. "AAAA") will encrypt to "BCDE", destroying frequency leaks!
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Question 4: Implement progressive_wheel_encrypt")


def progressive_wheel_decrypt(ciphertext: str, initial_shift: int, step: int = 1) -> str:
    """
    [Question 4] Decrypts text using a STEPPING wheel with matching initial shift and step.
    [TH] ถอดรหัสข้อความด้วยวงล้อแบบก้าวหมุน (Stepping Wheel)
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Question 4: Implement progressive_wheel_decrypt")


# ==============================================================================
# 🕵️ QUESTION 5: APPLIED CRYPTANALYSIS & INTERCEPTED CABLES
# ==============================================================================

def crack_without_wheel(ciphertext: str, clue_word: str = "THE") -> tuple[int, str]:
    """
    [Question 5A] Brute-force crack unknown shift WITHOUT wheel support.
    [TH] เจาะถอดรหัสข้อความดักจับแบบไม่มีวงล้อ โดยวนลูปทดสอบสูตรคณิตศาสตร์ 0..25

    Iterates through all 26 possible shifts (0..25) mathematically.
    Returns (discovered_shift, decrypted_plaintext).
    If clue_word is not found, returns (-1, "").
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Question 5A: Implement crack_without_wheel")


def crack_with_wheel(ciphertext: str, wheel: CipherWheel, clue_word: str = "THE") -> tuple[int, str]:
    """
    [Question 5B] Brute-force crack unknown shift WITH wheel support.
    [TH] เจาะถอดรหัสข้อความดักจับแบบมีวงล้อ โดยหมุนหน้าปัดวงล้อทีละคลิก 0..25

    Physically rotates the wheel through all 26 alignments (set_shift 0..25).
    Uses wheel_decrypt_short on ciphertext.
    Returns (discovered_shift, decrypted_plaintext).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Question 5B: Implement crack_with_wheel")


# ==============================================================================
# 🌟 BONUS QUESTION: CUSTOM KEYED SCRAMBLED ALPHABET WHEEL (+10 EXTRA CREDIT)
# ==============================================================================

class ScrambledCipherWheel(CipherWheel):
    """
    [Bonus Question] Advanced Wheel with a Keyed Scrambled Inner Alphabet.
    [TH] วงล้อรหัสลับขั้นสูงที่มีการเรียงตัวอักษรแบบสุ่มด้วยคีย์คำ (Keyed Alphabet)

    Instead of standard A..Z in sequence, the inner disk uses a keyword to scramble:
    Example keyword "SECRET":
    - Deduped letters from keyword: "S E C R T"
    - Followed by remaining unused alphabet: "A B D F G H I J K L M N O P Q U V W X Y Z"
    - Scrambled alphabet: "SECRTABDFGHIJKLMNOPQUVWXYZ"
    """

    def __init__(self, keyword: str, shift: int = 0):
        # Generate keyed scrambled alphabet
        deduped = []
        for c in keyword.upper():
            if c.isalpha() and c not in deduped:
                deduped.append(c)
        remaining = [c for c in ALPHABET if c not in deduped]
        self.keyed_alphabet = "".join(deduped + remaining)
        super().__init__(shift)

    def get_inner_alphabet(self) -> str:
        """Returns the rotated version of the scrambled alphabet."""
        return self.keyed_alphabet[self.shift:] + self.keyed_alphabet[:self.shift]


def scrambled_wheel_encrypt(plaintext: str, keyword: str, shift: int = 0) -> str:
    """Encrypts text using ScrambledCipherWheel."""
    # TODO: YOUR CODE HERE (OPTIONAL EXTRA CREDIT)
    raise NotImplementedError("Bonus: Implement scrambled_wheel_encrypt")


def scrambled_wheel_decrypt(ciphertext: str, keyword: str, shift: int = 0) -> str:
    """Decrypts text using ScrambledCipherWheel."""
    # TODO: YOUR CODE HERE (OPTIONAL EXTRA CREDIT)
    raise NotImplementedError("Bonus: Implement scrambled_wheel_decrypt")


# ==============================================================================
# 🧪 LOCAL SELF-TEST RUNNER (ชุดทดสอบการทำงานของโค้ด)
# ==============================================================================

# Benchmark Long Historical Message (Julius Caesar's Dispatch Excerpt)
LONG_HISTORICAL_MESSAGE = """Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae,
aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur.
All Gaul is divided into three parts, one of which the Belgae inhabit,
another the Aquitani, and the third who in their own language are called Celts.
Emergency Dispatch 101: Roman legions advance to river crossing at 06:00!"""


def run_all_tests():
    print("\n" + "=" * 75)
    print(" 🧪 DAY 1 FOCUS ASSIGNMENT LOCAL TEST RUNNER")
    print(" (Classical Ciphers: Short/Long Messages, With & Without Wheel Support)")
    print("=" * 75)

    passed_tasks = 0
    total_tasks = 5
    code_score = 0
    bonus_passed = False

    # --------------------------------------------------------------------------
    # Test 1: Question 1 (Short Message Without Wheel)
    # --------------------------------------------------------------------------
    print("\n[TEST 1] Question 1: Short Message Processing Without Wheel Support...")
    try:
        short_msg = "RETREAT AT ONCE! Code #99."
        c1 = caesar_direct_encrypt(short_msg, 4)
        assert c1 == "VIXVIEX EX SRGI! Gshi #99.", f"Direct encrypt failed! Got '{c1}'"
        p1 = caesar_direct_decrypt(c1, 4)
        assert p1 == short_msg, f"Direct decrypt failed! Got '{p1}'"
        assert caesar_direct_encrypt("XYZ", 3) == "ABC", "Modulo wrap failed!"
        assert caesar_direct_decrypt("ABC", 3) == "XYZ", "Modulo unwrap failed!"

        print("  --> ✅ PASS: Question 1 Passed! (+20 pts)")
        code_score += 20
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Question 1 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Question 1 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 2: Question 2 (Short Message With Wheel Support)
    # --------------------------------------------------------------------------
    print("\n[TEST 2] Question 2: Short Message Processing With Wheel Support...")
    try:
        wheel = CipherWheel(shift=4)
        short_msg = "RETREAT AT ONCE! Code #99."
        c2 = wheel_encrypt_short(short_msg, wheel)
        assert c2 == "VIXVIEX EX SRGI! Gshi #99.", f"Wheel encrypt failed! Got '{c2}'"
        p2 = wheel_decrypt_short(c2, wheel)
        assert p2 == short_msg, f"Wheel decrypt failed! Got '{p2}'"

        # Verify wheel dial rendering
        dial_output = wheel.render_ascii_dial()
        assert "CIPHER WHEEL ALIGNMENT" in dial_output, "Wheel dial render missing title!"
        assert "E F G H" in dial_output, "Inner alphabet rotation in dial incorrect!"

        print("  --> ✅ PASS: Question 2 Passed! (+20 pts)")
        code_score += 20
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Question 2 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Question 2 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 3: Question 3 (Long Message Processing & Equivalence)
    # --------------------------------------------------------------------------
    print("\n[TEST 3] Question 3: Long Message Processing & Direct vs. Wheel Equivalence...")
    try:
        shift_key = 11
        wheel_11 = CipherWheel(shift=shift_key)

        # 1. Encrypt long message via both methods
        c_direct = process_long_message_direct(LONG_HISTORICAL_MESSAGE, shift_key, mode="encrypt")
        c_wheel = process_long_message_wheel(LONG_HISTORICAL_MESSAGE, wheel_11, mode="encrypt")

        # Crucial Verification: Both methods must produce the EXACT same ciphertext!
        assert c_direct == c_wheel, "Mismatch between Direct Math and Wheel ciphertexts on long message!"
        assert c_direct != LONG_HISTORICAL_MESSAGE, "Ciphertext cannot match plaintext!"

        # 2. Decrypt long message via both methods
        p_direct = process_long_message_direct(c_direct, shift_key, mode="decrypt")
        p_wheel = process_long_message_wheel(c_wheel, wheel_11, mode="decrypt")

        assert p_direct == LONG_HISTORICAL_MESSAGE, "Direct decryption of long message failed!"
        assert p_wheel == LONG_HISTORICAL_MESSAGE, "Wheel decryption of long message failed!"

        print(f"  [Info] Successfully processed multi-paragraph message ({len(LONG_HISTORICAL_MESSAGE)} chars).")
        print("  --> ✅ PASS: Question 3 Passed! (+20 pts)")
        code_score += 20
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Question 3 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Question 3 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 4: Question 4 (Progressive Stepping Wheel)
    # --------------------------------------------------------------------------
    print("\n[TEST 4] Question 4: Progressive Rotor Stepping Wheel...")
    try:
        plain_repeats = "AAAAAA"
        # Initial shift 1, step 1: A+1=B, A+2=C, A+3=D, A+4=E, A+5=F, A+6=G
        stepped_cipher = progressive_wheel_encrypt(plain_repeats, initial_shift=1, step=1)
        assert stepped_cipher == "BCDEFG", f"Expected 'BCDEFG' for 'AAAAAA', got '{stepped_cipher}'"

        stepped_decrypted = progressive_wheel_decrypt(stepped_cipher, initial_shift=1, step=1)
        assert stepped_decrypted == plain_repeats, "Progressive decrypt failed!"

        # Test on sentence with punctuation (punctuation should NOT step the wheel!)
        test_sentence = "MEET AT NOON! DO NOT DELAY."
        c_step = progressive_wheel_encrypt(test_sentence, initial_shift=5, step=2)
        p_step = progressive_wheel_decrypt(c_step, initial_shift=5, step=2)
        assert p_step == test_sentence, "Stepping wheel failed with mixed sentence and punctuation!"

        print("  --> ✅ PASS: Question 4 Passed! (+20 pts)")
        code_score += 20
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Question 4 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Question 4 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 5: Question 5 (Cryptanalysis & Intercepted Cables)
    # --------------------------------------------------------------------------
    print("\n[TEST 5] Question 5: Applied Cryptanalysis (With & Without Wheel)...")
    try:
        # Intercepted transmission encrypted with unknown shift
        cable = "AOL JVUMLYLUJL PZ ZJOLKBSLK MVY TPKUPNOA HA AOL OPNI ZLJYLA IBURLY."
        # Method A: Without wheel
        shift_a, plain_a = crack_without_wheel(cable, clue_word="CONFERENCE")
        assert shift_a == 7, f"Expected shift 7 without wheel, got {shift_a}"
        assert "THE CONFERENCE IS SCHEDULED" in plain_a, "Decrypted plaintext without wheel incorrect!"

        # Method B: With wheel
        test_wheel = CipherWheel()
        shift_b, plain_b = crack_with_wheel(cable, test_wheel, clue_word="CONFERENCE")
        assert shift_b == 7, f"Expected shift 7 with wheel, got {shift_b}"
        assert plain_b == plain_a, "Mismatch between wheel and direct cracking results!"

        print("  --> ✅ PASS: Question 5 Passed! (+20 pts)")
        code_score += 20
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Question 5 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Question 5 Error: {e}")

    # --------------------------------------------------------------------------
    # Bonus Test: Scrambled Keyed Alphabet Wheel
    # --------------------------------------------------------------------------
    print("\n[BONUS TEST] Bonus Question: Custom Scrambled Alphabet Wheel (+10 Extra Credit)...")
    try:
        kw = "SECRET"
        p_bonus = "TOP SECRET OPERATION"
        c_bonus = scrambled_wheel_encrypt(p_bonus, keyword=kw, shift=2)
        dec_bonus = scrambled_wheel_decrypt(c_bonus, keyword=kw, shift=2)
        assert dec_bonus == p_bonus, f"Scrambled wheel decrypt failed: expected '{p_bonus}', got '{dec_bonus}'"
        print("  --> 🌟 PASS: Bonus Question Passed! (+10 Extra Credit pts)")
        bonus_passed = True
    except NotImplementedError:
        print("  --> ⏭️ SKIPPED: Bonus Question not implemented (Optional).")
    except Exception as e:
        print(f"  --> ❌ FAIL: Bonus Question Error: {e}")

    # --------------------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------------------
    bonus_score = 10 if bonus_passed else 0
    print("\n" + "=" * 75)
    print(f" 🏆 AUTOMATED CODE SCORE: {code_score} / 100 Points ({passed_tasks}/{total_tasks} Questions Passed)")
    if bonus_passed:
        print(f" 🌟 BONUS SCORE: +{bonus_score} Extra Credit Points")
    print(" 📝 Note: Conceptual reflections will be evaluated from your REPORT_DAY1.md.")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    run_all_tests()
