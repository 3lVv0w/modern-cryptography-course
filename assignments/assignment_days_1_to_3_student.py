"""
================================================================================
🎓 CS-4XX / ECE-4XX การเข้ารหัสขั้นสูงและความปลอดภัยของเครือข่าย
CLASS ASSIGNMENT: DAYS 1–3 STUDENT CODE TEMPLATE (ใบงานปฏิบัติการวันที่ 1–3)
================================================================================
Student Name (ชื่อ-นามสกุล) : ________________________________________
Student ID (รหัสนักศึกษา)   : ________________________________________
Submission Date (วันที่ส่ง) : _____________________________________

คำแนะนำสำหรับนักศึกษา (INSTRUCTIONS):
1. เติมโค้ดในทุกฟังก์ชันที่มีสัญลักษณ์ `# TODO: YOUR CODE HERE` ให้สมบูรณ์
2. ห้ามเปลี่ยนชื่อฟังก์ชัน (Function Signature), ชื่อพารามิเตอร์ หรือชนิดข้อมูลที่ส่งคืน
3. ทดสอบโค้ดบนเครื่องของท่านด้วยคำสั่ง:
       python3 assignments/assignment_days_1_to_3_student.py
4. ก่อนส่งงาน ให้รันสคริปต์ตรวจสอบความถูกต้องและรวมไฟล์ส่ง:
       python3 assignments/submit_check.py --student-id "รหัสของท่าน" --name "ชื่อ นามสกุล"
================================================================================
"""

import math
import secrets
from collections import Counter
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import x25519

# Standard English Letter Frequencies (%) for Statistical Cryptanalysis
ENGLISH_FREQUENCIES = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.98, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.01, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}


# ==============================================================================
# 🟢 PART 2.1: SIMPLE CLASSICAL CIPHER (CAESAR ENCRYPT & DECRYPT) (DAY 1)
# ==============================================================================

def caesar_encrypt(plaintext: str, shift: int) -> str:
    """
    [Task 2.1] Encrypts plaintext using Caesar Shift Cipher modulo 26.
    [TH] เข้ารหัสข้อความด้วย Caesar Shift Cipher มอดุโล 26
    Formula: C_i = (P_i + shift) mod 26
    - Preserves uppercase/lowercase casing ('A'..'Z' and 'a'..'z').
    - Non-alphabetic characters (spaces, punctuation, numbers) MUST remain unchanged.
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.1: Implement caesar_encrypt")


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """
    [Task 2.1] Decrypts ciphertext using Caesar Shift Cipher key.
    [TH] ถอดรหัสข้อความด้วยกุญแจ Caesar Shift Cipher
    Formula: P_i = (C_i - shift) mod 26
    - Reverses the shift transformation.
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.1: Implement caesar_decrypt")


# ==============================================================================
# 🟢 PART 2.2: CLASSICAL STATISTICAL CRYPTANALYSIS (DAY 1)
# ==============================================================================

def compute_chi_squared(text: str) -> float:
    """
    [Task 2.2] Calculates the Chi-Squared (χ²) statistic of text compared to standard English.
    [TH] คำนวณค่าสถิติไคสแควร์ (χ²) เปรียบเทียบความถี่ตัวอักษรกับภาษาอังกฤษมาตรฐาน
    Formula: χ² = Sum( (Observed_i - Expected_i)² / Expected_i ) for i in A..Z
    Lower score indicates text distribution closely matching natural English.
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.2: Implement compute_chi_squared")


def compute_index_of_coincidence(text: str) -> float:
    """
    [Task 2.2] Calculates the Index of Coincidence (IC) of text.
    [TH] คำนวณค่าดัชนีความบังเอิญ (Index of Coincidence - IC) ของข้อความ
    Formula: IC = Sum( f_i * (f_i - 1) ) / ( N * (N - 1) )
    Natural English text exhibits IC ≈ 0.0667, while random text exhibits IC ≈ 0.0385.
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.2: Implement compute_index_of_coincidence")


def auto_break_caesar(ciphertext: str) -> tuple[int, str]:
    """
    [Task 2.2] Automated Caesar Breaker using Chi-Squared minimum score.
    [TH] โปรแกรมถอดรหัสซีซาร์อัตโนมัติ โดยทดสอบคีย์ทั้ง 26 ค่าและเลือกค่าที่ให้ χ² ต่ำสุด
    Iterates through all 26 possible shift keys, scores candidate plaintexts,
    and returns (best_shift_key, best_decrypted_plaintext).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.2: Implement auto_break_caesar")


# ==============================================================================
# 🟢 PART 2.3: NUMBER THEORY PRIMITIVES FROM SCRATCH (DAY 2)
# ==============================================================================

def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    [Task 2.3] Extended Euclidean Algorithm.
    [TH] ขั้นตอนวิธีแบบยุคลิดส่วนขยาย (Extended Euclidean Algorithm)
    Computes greatest common divisor and Bézout coefficients (g, x, y)
    such that: a*x + b*y = g = gcd(a, b).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.3: Implement extended_gcd")


def modinv(a: int, m: int) -> int:
    """
    [Task 2.3] Computes the modular multiplicative inverse of 'a' modulo 'm'.
    [TH] คำนวณหาตัวผกผันการคูณมอดุโล (Modular Multiplicative Inverse) ของ 'a' mod 'm'
    Returns x in [0, m-1] such that (a * x) % m == 1.
    Raises ValueError if gcd(a, m) != 1 (inverse does not exist).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.3: Implement modinv")


def pow_mod(base: int, exp: int, mod: int) -> int:
    """
    [Task 2.3] Fast Modular Exponentiation using Square-and-Multiply.
    [TH] ขั้นตอนวิธีการยกกำลังมอดุโลแบบเร็วด้วยเทคนิค Square-and-Multiply ในเวลา O(log exp)
    Computes (base^exp) % mod in O(log exp) multiplications.
    NOTE: You MUST implement the square-and-multiply loop manually.
          Do NOT call Python's built-in 3-argument pow(base, exp, mod).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.3: Implement pow_mod")


# ==============================================================================
# 🟡 PART 2.4: MODERN SYMMETRIC AEAD (AES-256-GCM) (DAY 2)
# ==============================================================================

def encrypt_aes_gcm(plaintext: str, key: bytes, aad: bytes = b"") -> tuple[bytes, bytes]:
    """
    [Task 2.4] Encrypts plaintext using AES-256-GCM.
    [TH] เข้ารหัสข้อความด้วย AES-256-GCM สุ่มสร้าง Nonce ขนาด 96 บิต (12 ไบต์) อย่างปลอดภัย
    Generates a secure 96-bit (12-byte) random nonce using secrets module.
    Returns: (nonce, ciphertext_with_tag)
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.4: Implement encrypt_aes_gcm")


def decrypt_aes_gcm(nonce: bytes, ciphertext: bytes, key: bytes, aad: bytes = b"") -> str:
    """
    [Task 2.4] Decrypts and verifies authentication tag for AES-256-GCM ciphertext.
    [TH] ถอดรหัสและตรวจสอบแท็กความถูกต้อง 16 ไบต์ของ AES-256-GCM
    Returns: Decrypted UTF-8 plaintext string.
    Raises: cryptography.exceptions.InvalidTag if ciphertext or AAD was tampered with.
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.4: Implement decrypt_aes_gcm")


# ==============================================================================
# 🟡 PART 2.5: RSA CRYPTOSYSTEM ENGINE & CURVE25519 ECDH (DAY 3)
# ==============================================================================

def str_to_int(s: str) -> int:
    """Encodes string to big-endian integer."""
    return int.from_bytes(s.encode('utf-8'), byteorder='big')


def int_to_str(i: int) -> str:
    """Decodes big-endian integer to string."""
    length = (i.bit_length() + 7) // 8
    return i.to_bytes(length, byteorder='big').decode('utf-8', errors='ignore')


def rsa_keygen(p: int, q: int, e: int = 65537) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Generates RSA Keypair given two prime numbers p and q.
    [TH] สร้างคู่กุญแจ RSA ((N, e), (N, d)) จากจำนวนเฉพาะ p และ q
    Computes:
      - N = p * q
      - phi(N) = (p - 1) * (q - 1)
      - d = modinv(e, phi(N))
    Returns: ((N, e), (N, d)) representing (public_key, private_key).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.5: Implement rsa_keygen")


def rsa_encrypt(message_int: int, public_key: tuple[int, int]) -> int:
    """
    Encrypts integer message using RSA public key: C = (M ^ e) mod N.
    [TH] เข้ารหัสข้อความตัวเลขด้วยกุญแจสาธารณะ RSA: C = (M ^ e) mod N
    Raises ValueError if message_int >= N.
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.5: Implement rsa_encrypt")


def rsa_decrypt(ciphertext_int: int, private_key: tuple[int, int]) -> int:
    """
    Decrypts integer ciphertext using RSA private key: M = (C ^ d) mod N.
    [TH] ถอดรหัสข้อความตัวเลขด้วยกุญแจส่วนตัว RSA: M = (C ^ d) mod N
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.5: Implement rsa_decrypt")


def ecdh_x25519_key_exchange() -> tuple[bytes, bytes]:
    """
    Simulates modern Curve25519 (X25519) Elliptic Curve Diffie-Hellman Key Exchange.
    [TH] จำลองการแลกเปลี่ยนกุญแจเส้นโค้งวงรี Curve25519 (X25519) ECDH ระหว่าง Alice และ Bob
    1. Generates ephemeral X25519 private/public keypair for Alice.
    2. Generates ephemeral X25519 private/public keypair for Bob.
    3. Alice computes shared secret using Bob's public key.
    4. Bob computes shared secret using Alice's public key.
    Returns: (alice_shared_secret, bob_shared_secret).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.5: Implement ecdh_x25519_key_exchange")


# ==============================================================================
# 🔴 PART 3: APPLIED OFFENSIVE CRYPTANALYSIS & INCIDENT RESPONSE
# ==============================================================================

def two_time_pad_crib_drag(c1_bytes: bytes, c2_bytes: bytes, crib: str) -> list[tuple[int, str]]:
    """
    [Attack 3.1] Two-Time Pad Keystream Reuse (Crib Dragging Attack).
    [TH] การโจมตี One-Time Pad ที่นำคีย์มาใช้ซ้ำ (Two-Time Pad) ด้วยวิธี Crib Dragging
    Given two ciphertexts C1, C2 encrypted under the same One-Time Pad key:
        C1 = M1 ^ K, C2 = M2 ^ K  ==>  C1 ^ C2 = M1 ^ M2
    Slides `crib` across (C1 ^ C2) byte-by-byte.
    Returns list of tuples: [(position_offset, candidate_plaintext_snippet), ...]
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Attack 3.1: Implement two_time_pad_crib_drag")


def exploit_gcm_nonce_reuse(c1_payload: bytes, c2_payload: bytes) -> bytes:
    """
    [Attack 3.2] AES-GCM Nonce Reuse Keystream Recovery.
    [TH] การโจมตีช่องโหว่การใช้ Nonce ซ้ำใน AES-GCM เพื่อกู้คืน Keystream: C1 ^ C2 = P1 ^ P2
    When AES-GCM reuses the same (Key, Nonce), the counter keystream is identical:
        C1 = P1 ^ Keystream,  C2 = P2 ^ Keystream
        ==> C1 ^ C2 = P1 ^ P2
    Returns byte-by-byte XOR stream (C1 ^ C2).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Attack 3.2: Implement exploit_gcm_nonce_reuse")


def fermat_factor(N: int) -> tuple[int, int]:
    """
    [Attack 3.3] Fermat's Factorization Attack on Weak RSA Moduli.
    [TH] การโจมตีแยกตัวประกอบของแฟร์มาต์ เมื่อจำนวนเฉพาะ p และ q มีค่าใกล้เคียงกันมาก
    When prime factors p and q are close to each other:
        N = a^2 - b^2 = (a - b)(a + b)
    Starts search at a = ceil(sqrt(N)), checks if (a^2 - N) is a perfect square b^2.
    Returns factors (p, q).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Attack 3.3: Implement fermat_factor")


def crack_rsa_ciphertext(N: int, e: int, ciphertext: int) -> int:
    """
    [Attack 3.3] Exploits Fermat Factorization to recover private key and decrypt ciphertext.
    [TH] ประยุกต์ใช้การแยกตัวประกอบ Fermat เพื่อคำนวณหากุญแจส่วนตัว d และถอดรหัสลับ RSA
    1. Factors N into p, q using fermat_factor(N).
    2. Computes phi(N) = (p-1)*(q-1).
    3. Derives private exponent d = modinv(e, phi(N)).
    4. Decrypts ciphertext: M = (C ^ d) mod N.
    Returns decrypted integer message M.
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Attack 3.3: Implement crack_rsa_ciphertext")


# ==============================================================================
# 🌟 BONUS EXTRA CREDIT: AUTOMATED VIGENÈRE CIPHER BREAKER (+15 PTS)
# ==============================================================================

def vigenere_encrypt(plaintext: str, keyword: str) -> str:
    """[Helper] Encrypts plaintext using Vigenère keyword."""
    keyword_clean = [c.upper() for c in keyword if c.isalpha()]
    m = len(keyword_clean)
    result = []
    key_idx = 0

    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            k_shift = ord(keyword_clean[key_idx % m]) - ord('A')
            result.append(chr((ord(char) - base + k_shift) % 26 + base))
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)


def vigenere_decrypt(ciphertext: str, keyword: str) -> str:
    """Decrypts ciphertext using Vigenère keyword."""
    keyword_clean = [c.upper() for c in keyword if c.isalpha()]
    m = len(keyword_clean)
    result = []
    key_idx = 0

    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            k_shift = ord(keyword_clean[key_idx % m]) - ord('A')
            result.append(chr((ord(char) - base - k_shift) % 26 + base))
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)


def crack_vigenere_cipher(ciphertext: str, max_key_len: int = 10) -> tuple[str, str]:
    """
    [BONUS EXTRA CREDIT] Autonomous Vigenère Cipher Breaker without key knowledge.
    [TH] โปรแกรมถอดรหัสลับ Vigenère อัตโนมัติโดยประเมินความยาวคีย์จาก IC และแก้คอลัมน์ด้วย Chi-Squared
    1. Estimate key length m in [1, max_key_len] by computing average IC across columns.
    2. Decompose ciphertext into m interleaved Caesar cosets.
    3. Use Chi-Squared automated Caesar breaker to recover each key letter.
    4. Return (recovered_keyword, decrypted_plaintext).
    """
    # TODO: YOUR CODE HERE (OPTIONAL FOR EXTRA CREDIT)
    raise NotImplementedError("Bonus: Implement crack_vigenere_cipher")


# ==============================================================================
# 🧪 LOCAL SELF-TEST EVALUATION SUITE
# ==============================================================================

def run_all_tests():
    print("\n" + "=" * 75)
    print(" 🧪 CS-4XX / ECE-4XX CLASS ASSIGNMENT (DAYS 1-3) LOCAL TEST RUNNER")
    print("=" * 75)

    passed_tasks = 0
    total_tasks = 8
    code_score = 0
    bonus_passed = False

    # --------------------------------------------------------------------------
    # Test 1: Task 2.1 (Caesar Cipher Encryption & Decryption)
    # --------------------------------------------------------------------------
    print("\n[TEST 1] Task 2.1: Simple Classical Cipher (Caesar Encrypt & Decrypt)...")
    try:
        # Test basic shift, case preservation, and punctuation handling
        test_plain = "HELLO WORLD! Secret #42: Attack at XYZ."
        c3 = caesar_encrypt(test_plain, 3)
        assert c3 == "KHOOR ZRUOG! Vhfuhw #42: Dwwdfn dw ABC.", f"Caesar encrypt failed: got {c3}"
        d3 = caesar_decrypt(c3, 3)
        assert d3 == test_plain, f"Caesar decrypt failed: got {d3}"

        # Test alphabet wraparound
        wrap_test = "XYZxyz"
        assert caesar_encrypt(wrap_test, 3) == "ABCabc", "Caesar wraparound failed!"
        assert caesar_decrypt("ABCabc", 3) == wrap_test, "Caesar wraparound decrypt failed!"
        assert caesar_encrypt("ABC", 26) == "ABC", "Shift 26 modulo failed!"
        assert caesar_encrypt("ABC", 29) == "DEF", "Shift > 26 modulo failed!"

        print("  --> ✅ PASS: Task 2.1 Passed (8/8 pts)")
        code_score += 8
        passed_tasks += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.1 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 2: Task 2.2 (Classical Statistical Cryptanalysis)
    # --------------------------------------------------------------------------
    print("\n[TEST 2] Task 2.2: Statistical Cryptanalysis (Chi-Square, IC, Auto-Caesar)...")
    try:
        sample_plain = "CRYPTOGRAPHY IS THE FOUNDATION OF MODERN DIGITAL SECURITY AND TRUST"
        cipher = caesar_encrypt(sample_plain, 7)
        best_k, cracked_plain = auto_break_caesar(cipher)
        assert best_k == 7, f"Caesar crack failed: Expected shift 7, got {best_k}"
        assert cracked_plain == sample_plain, "Plaintext mismatch!"
        ic_val = compute_index_of_coincidence(sample_plain)
        assert ic_val > 0.050, f"IC calculation out of range: {ic_val}"
        print("  --> ✅ PASS: Task 2.2 Passed (8/8 pts)")
        code_score += 8
        passed_tasks += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.2 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 3: Task 2.3 (Number Theory Primitives)
    # --------------------------------------------------------------------------
    print("\n[TEST 3] Task 2.3: Number Theory Primitives (Ext-GCD, ModInv, PowMod)...")
    try:
        g, x, y = extended_gcd(240, 46)
        assert g == 2 and 240 * x + 46 * y == 2, "Extended GCD failed!"
        inv = modinv(17, 3120)
        assert (17 * inv) % 3120 == 1, "Modular inverse failed!"
        # Check custom square-and-multiply
        assert pow_mod(7, 256, 1000) == pow(7, 256, 1000), "Fast pow_mod failed!"
        print("  --> ✅ PASS: Task 2.3 Passed (8/8 pts)")
        code_score += 8
        passed_tasks += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.3 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 4: Task 2.4 (Modern Symmetric AEAD - AES-256-GCM)
    # --------------------------------------------------------------------------
    print("\n[TEST 4] Task 2.4: Modern Symmetric AEAD (AES-256-GCM)...")
    try:
        key = secrets.token_bytes(32)
        secret_msg = "CONFIDENTIAL MILITARY INTEL: COORDINATES 45.123, -93.456"
        auth_aad = b"system_epoch=2026-Q1|classification=TOP_SECRET"
        nonce, ciphertext = encrypt_aes_gcm(secret_msg, key, auth_aad)
        assert len(nonce) == 12, "Nonce must be exactly 96 bits (12 bytes)!"
        decrypted = decrypt_aes_gcm(nonce, ciphertext, key, auth_aad)
        assert decrypted == secret_msg, "Decrypted text mismatch!"

        # Tamper verification check
        tamper_detected = False
        try:
            decrypt_aes_gcm(nonce, ciphertext, key, b"tampered_header")
        except Exception:
            tamper_detected = True
        assert tamper_detected, "AES-GCM failed to reject tampered AAD!"

        print("  --> ✅ PASS: Task 2.4 Passed (8/8 pts)")
        code_score += 8
        passed_tasks += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.4 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 5: Task 2.5 (RSA Engine & Curve25519 ECDH)
    # --------------------------------------------------------------------------
    print("\n[TEST 5] Task 2.5: RSA Engine & Curve25519 ECDH...")
    try:
        p_val, q_val = 1009, 1013
        pub_k, priv_k = rsa_keygen(p_val, q_val, e=65537)
        N_val, e_val = pub_k
        assert N_val == p_val * q_val, "RSA N incorrect!"
        test_int = 424242
        c_val = rsa_encrypt(test_int, pub_k)
        m_val = rsa_decrypt(c_val, priv_k)
        assert m_val == test_int, "RSA Encrypt/Decrypt integer mismatch!"

        alice_s, bob_s = ecdh_x25519_key_exchange()
        assert alice_s == bob_s and len(alice_s) == 32, "ECDH X25519 shared secret mismatch!"
        print("  --> ✅ PASS: Task 2.5 Passed (8/8 pts)")
        code_score += 8
        passed_tasks += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.5 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 6: Attack 3.1 (Two-Time Pad Crib Dragging)
    # --------------------------------------------------------------------------
    print("\n[TEST 6] Attack 3.1: Two-Time Pad Keystream Reuse & Crib Dragging...")
    try:
        p1 = "OPERATION OVERLORD LAUNCH"
        p2 = "DEFEND NORMANDY BEACHHEAD"
        pad_key = secrets.token_bytes(len(p1))
        c1 = bytes([ord(a) ^ b for a, b in zip(p1, pad_key)])
        c2 = bytes([ord(a) ^ b for a, b in zip(p2, pad_key)])

        drag_matches = two_time_pad_crib_drag(c1, c2, "OPERATION")
        assert len(drag_matches) > 0, "No crib drag matches found!"
        assert "DEFEND " in drag_matches[0][1], f"Expected 'DEFEND ' in crib drag result, got {drag_matches[0][1]}"
        print("  --> ✅ PASS: Attack 3.1 Passed (10/10 pts)")
        code_score += 10
        passed_tasks += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Attack 3.1 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 7: Attack 3.2 (AES-GCM Nonce Reuse Keystream Recovery)
    # --------------------------------------------------------------------------
    print("\n[TEST 7] Attack 3.2: AES-GCM Nonce Reuse Keystream Recovery...")
    try:
        shared_key = secrets.token_bytes(32)
        fixed_nonce = b"FIXEDNONCE12"
        known_p1 = "WIRE_TRANSFER:$10,000_TO_ALICE"
        target_p2 = "WIRE_TRANSFER:$99,999_TO_HACKR"

        aesgcm = AESGCM(shared_key)
        # Exclude 16-byte tag to extract raw CTR ciphertext stream
        c1_stream = aesgcm.encrypt(fixed_nonce, known_p1.encode('utf-8'), None)[:-16]
        c2_stream = aesgcm.encrypt(fixed_nonce, target_p2.encode('utf-8'), None)[:-16]

        xor_stream = exploit_gcm_nonce_reuse(c1_stream, c2_stream)
        # Verify target recovery: P2 = (C1 ^ C2) ^ P1
        recovered_p2_bytes = bytes([x ^ ord(p) for x, p in zip(xor_stream, known_p1)])
        assert recovered_p2_bytes.decode('utf-8') == target_p2, "Failed to recover target plaintext!"
        print("  --> ✅ PASS: Attack 3.2 Passed (10/10 pts)")
        code_score += 10
        passed_tasks += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Attack 3.2 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 8: Attack 3.3 (Fermat Factorization of Flawed RSA)
    # --------------------------------------------------------------------------
    print("\n[TEST 8] Attack 3.3: Fermat Factorization of Flawed RSA...")
    try:
        weak_p, weak_q = 65539, 65543  # Close primes
        weak_N = weak_p * weak_q
        weak_e = 65537
        fact_p, fact_q = fermat_factor(weak_N)
        assert {fact_p, fact_q} == {weak_p, weak_q}, "Fermat factorization failed!"

        test_secret = 13371337
        weak_pub = (weak_N, weak_e)
        cipher_val = rsa_encrypt(test_secret, weak_pub)
        recovered_secret = crack_rsa_ciphertext(weak_N, weak_e, cipher_val)
        assert recovered_secret == test_secret, "RSA crack failed!"
        print("  --> ✅ PASS: Attack 3.3 Passed (10/10 pts)")
        code_score += 10
        passed_tasks += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Attack 3.3 Error: {e}")

    # --------------------------------------------------------------------------
    # Bonus Test: Extra Credit (Autonomous Vigenère Breaker)
    # --------------------------------------------------------------------------
    print("\n[BONUS TEST] Autonomous Vigenère Breaker (Extra Credit)...")
    try:
        vig_sample = "THE ONE TIME PAD IS UNCONDITIONALLY SECURE PROVIDED THE KEY IS TRULY RANDOM AND NEVER REUSED AGAIN IN PRODUCTION SYSTEMS"
        sample_key = "CRYPTO"
        v_cipher = vigenere_encrypt(vig_sample, sample_key)

        found_key, cracked_plain = crack_vigenere_cipher(v_cipher, max_key_len=10)
        assert found_key == sample_key, f"Expected key {sample_key}, got {found_key}"
        assert cracked_plain == vig_sample, "Plaintext mismatch!"
        print("  --> 🌟 PASS: Extra Credit Vigenère Breaker Passed (+15 Bonus pts)!")
        bonus_passed = True
    except NotImplementedError:
        print("  --> ⏭️ SKIPPED: Extra Credit not implemented (Optional).")
    except Exception as e:
        print(f"  --> ❌ FAIL: Extra Credit Error: {e}")

    # --------------------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------------------
    bonus_score = 15 if bonus_passed else 0
    print("\n" + "=" * 75)
    print(f" 🏆 AUTOMATED CODE SCORE: {code_score} / 70 Points ({passed_tasks}/{total_tasks} Tasks Passed)")
    if bonus_passed:
        print(f" 🌟 BONUS SCORE: +{bonus_score} Extra Credit Points")
    print(f" 📝 Note: Part 1 Theory (30 pts) will be evaluated from your REPORT.md.")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    run_all_tests()
