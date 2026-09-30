"""
================================================================================
🎓 CS-1XX / ECE-1XX Modern Cryptography for Beginners
CLASS ASSIGNMENT: BEGINNER / NEWBIE STUDENT CODE TEMPLATE
(ใบงานปฏิบัติการวิทยาการรหัสลับระดับผู้เริ่มต้น)
================================================================================
Student Name (ชื่อ-นามสกุล) : ________________________________________
Student ID (รหัสนักศึกษา)   : ________________________________________
Submission Date (วันที่ส่ง) : ________________________________________

คำแนะนำสำหรับนักศึกษา (INSTRUCTIONS):
1. เติมโค้ดในฟังก์ชันที่มีคำสั่ง `# TODO: YOUR CODE HERE` ให้สมบูรณ์
2. ห้ามเปลี่ยนชื่อฟังก์ชัน (Function Signature), พารามิเตอร์ หรือชนิดข้อมูลที่คืนกลับ
3. ทดสอบการทำงานของโค้ดด้วยคำสั่ง:
       python3 assignments/assignment_beginner_student.py
4. เมื่อผ่านการทดสอบแล้ว ให้รันสคริปต์ตรวจสอบและรวมไฟล์ส่ง:
       python3 assignments/submit_check_beginner.py --student-id "รหัสของท่าน" --name "ชื่อ นามสกุล"
================================================================================
"""

import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ==============================================================================
# 🟢 MODULE 1: CLASSICAL CIPHERS & BITWISE SECRETS (DAY 1)
# ==============================================================================

def caesar_encrypt(plaintext: str, shift: int) -> str:
    """
    [Task 2.1] Encrypts plaintext using Caesar Shift Cipher modulo 26.
    [TH] เข้ารหัสข้อความด้วยการเลื่อนตัวอักษรแบบซีซาร์ (Caesar Cipher) มอดุโล 26

    Formula: C_i = (P_i + shift) mod 26
    
    Rules / กฎเกณฑ์:
    - Shift uppercase letters ('A'..'Z') to uppercase letters.
    - Shift lowercase letters ('a'..'z') to lowercase letters.
    - Non-alphabetic characters (spaces, numbers, punctuation) MUST remain unchanged.
    - Handle shifts >= 26 and negative shifts correctly using modulo arithmetic.
    
    Hint / คำแนะนำ:
    - ord('A') gives ASCII value (65), chr(65) gives 'A'.
    - For a char 'c', offset = (ord(c) - ord('A') + shift) % 26, then chr(ord('A') + offset).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.1: Implement caesar_encrypt")


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """
    [Task 2.1] Decrypts ciphertext using Caesar Shift Cipher key.
    [TH] ถอดรหัสข้อความด้วยกุญแจ Caesar Cipher

    Formula: P_i = (C_i - shift) mod 26
    
    Hint / คำแนะนำ:
    - Decryption is simply encryption with a negative shift: -shift!
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.1: Implement caesar_decrypt")


def xor_cipher(data: bytes, key: bytes) -> bytes:
    """
    [Task 2.2] Encrypts or decrypts bytes using bitwise XOR (⊕) with a key.
    [TH] เข้ารหัสหรือถอดรหัสข้อมูลไบต์ด้วยตัวดำเนินการบิตไวส์ XOR (⊕) กับกุญแจ

    Formula: C_i = Data_i ⊕ Key_{i % len(Key)}
    
    Properties / คุณสมบัติมหัศจรรย์ของ XOR:
    - (A ⊕ B) ⊕ B = A (Encrypting twice with the exact same key returns the original data!)
    
    Hint / คำแนะนำ:
    - In Python, use list comprehension:
      bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.2: Implement xor_cipher")


# ==============================================================================
# 🟢 MODULE 2: NUMBER THEORY BASICS & MODERN SYMMETRIC AES (DAY 2)
# ==============================================================================

def euclidean_gcd(a: int, b: int) -> int:
    """
    [Task 2.3] Computes the Greatest Common Divisor (GCD) using Euclid's Algorithm.
    [TH] คำนวณหาตัวหารร่วมมาก (ห.ร.ม. / GCD) ด้วยขั้นตอนวิธีของยุคลิด

    Algorithm / ขั้นตอนวิธี:
    - While b is not 0:
        a, b = b, a % b
    - Return a

    Example:
    euclidean_gcd(48, 18) -> 6
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.3: Implement euclidean_gcd")


def aes_gcm_encrypt(plaintext: str, key: bytes) -> tuple[bytes, bytes]:
    """
    [Task 2.4] Encrypts plaintext string using modern AES-256-GCM.
    [TH] เข้ารหัสข้อความด้วย AES-256-GCM พร้อมสร้าง Nonce สุ่มขนาด 12 ไบต์ (96 บิต)

    Steps / ขั้นตอน:
    1. Generate a secure random 12-byte nonce: secrets.token_bytes(12)
    2. Create AESGCM instance: aesgcm = AESGCM(key)
    3. Encrypt: ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    4. Return (nonce, ciphertext)
    
    Why GCM?
    - GCM is AEAD (Authenticated Encryption with Associated Data).
    - It provides both Confidentiality (secrecy) AND Integrity (tamper detection).
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.4: Implement aes_gcm_encrypt")


def aes_gcm_decrypt(nonce: bytes, ciphertext: bytes, key: bytes) -> str:
    """
    [Task 2.4] Decrypts and authenticates AES-256-GCM ciphertext.
    [TH] ถอดรหัสและตรวจสอบความถูกต้องของข้อความรหัส AES-256-GCM

    Steps / ขั้นตอน:
    1. Create AESGCM instance: aesgcm = AESGCM(key)
    2. Decrypt: plain_bytes = aesgcm.decrypt(nonce, ciphertext, None)
    3. Return plain_bytes.decode('utf-8')
    
    Note: If someone tampered with the ciphertext or nonce, aesgcm.decrypt will
          automatically raise cryptography.exceptions.InvalidTag.
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.4: Implement aes_gcm_decrypt")


# ==============================================================================
# 🟢 MODULE 3: PUBLIC-KEY CRYPTOGRAPHY MADE SIMPLE (DAY 3)
# ==============================================================================

def dh_compute_public_key(g: int, priv_key: int, p: int) -> int:
    """
    [Task 2.5] Computes Diffie-Hellman public key from a private key.
    [TH] คำนวณกุญแจสาธารณะ Diffie-Hellman จากกุญแจส่วนตัว

    Formula: Public_Key = (g ^ priv_key) mod p
    
    Hint / คำแนะนำ:
    - Use Python's built-in fast modular exponentiation: pow(base, exponent, modulus)
      Do NOT use (g ** priv_key) % p because large exponents will freeze your computer!
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.5: Implement dh_compute_public_key")


def dh_compute_shared_secret(peer_public_key: int, my_priv_key: int, p: int) -> int:
    """
    [Task 2.5] Computes Diffie-Hellman shared secret between two parties.
    [TH] คำนวณกุญแจลับร่วม (Shared Secret) Diffie-Hellman

    Formula: Shared_Secret = (peer_public_key ^ my_priv_key) mod p
    
    Magic of Diffie-Hellman:
    - Alice computes: (B ^ a) mod p = (g^b)^a mod p = g^(a*b) mod p
    - Bob computes:   (A ^ b) mod p = (g^a)^b mod p = g^(a*b) mod p
    - Both arrive at the exact same shared secret without Eve knowing it!
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.5: Implement dh_compute_shared_secret")


def rsa_encrypt_toy(m: int, e: int, n: int) -> int:
    """
    [Task 2.6] Encrypts integer message 'm' using RSA public key (n, e).
    [TH] เข้ารหัสข้อความตัวเลข 'm' ด้วยกุญแจสาธารณะ RSA (n, e)

    Formula: C = (m ^ e) mod n
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.6: Implement rsa_encrypt_toy")


def rsa_decrypt_toy(c: int, d: int, n: int) -> int:
    """
    [Task 2.6] Decrypts integer ciphertext 'c' using RSA private key (n, d).
    [TH] ถอดรหัสข้อความตัวเลข 'c' ด้วยกุญแจส่วนตัว RSA (n, d)

    Formula: M = (c ^ d) mod n
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Task 2.6: Implement rsa_decrypt_toy")


# ==============================================================================
# 🕵️ MODULE 4: BEGINNER DETECTIVE MISSION & INTEGRITY (DAY 4)
# ==============================================================================

def crack_simple_caesar(ciphertext: str, clue_word: str = "THE") -> tuple[int, str]:
    """
    [Mission 3.1] Decrypt an intercepted Caesar cipher message by brute force.
    [TH] ถอดรหัสข้อความสายลับ Caesar ด้วยการทดสอบคีย์ที่เป็นไปได้ (Brute Force 0..25)

    Scenario / สถานการณ์:
    - An intercepted enemy message is encrypted with an unknown Caesar shift.
    - We know the message is in English and contains the common word `clue_word` (e.g. "THE" or "SECRET").
    
    Steps / ขั้นตอน:
    1. Try every possible shift key from 0 to 25.
    2. Decrypt the ciphertext with that shift: candidate = caesar_decrypt(ciphertext, shift).
    3. If clue_word.upper() is found in candidate.upper():
         Return (shift, candidate)
    4. If not found after checking all 26 shifts, return (-1, "")
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Mission 3.1: Implement crack_simple_caesar")


def compute_sha256_hex(text: str) -> str:
    """
    [Mission 3.1] Computes the SHA-256 hexadecimal hash of a text string.
    [TH] คำนวณค่าแฮช SHA-256 (Hex Digest) เพื่อเป็นลายนิ้วมือดิจิทัลของข้อความ

    Steps / ขั้นตอน:
    1. Encode text to UTF-8 bytes: text.encode('utf-8')
    2. Compute SHA-256: hashlib.sha256(data).hexdigest()
    """
    # TODO: YOUR CODE HERE
    raise NotImplementedError("Mission 3.1: Implement compute_sha256_hex")


def measure_hash_avalanche(text1: str, text2: str) -> float:
    """
    [Bonus Mission 3.2] Measures the Avalanche Effect between two hashes.
    [TH] วัดปรากฏการณ์หิมะถล่ม (Avalanche Effect) เมื่อเปลี่ยนข้อความเพียงนิดเดียว

    The Avalanche Effect means that changing even a single character or bit in the
    input will cause roughly 50% of the output hash bits to flip randomly!

    Steps / ขั้นตอน:
    1. Compute SHA-256 hex digest for text1 and text2 using compute_sha256_hex.
    2. Convert each 64-character hex string into a 256-bit binary string:
       bin1 = bin(int(hex1, 16))[2:].zfill(256)
       bin2 = bin(int(hex2, 16))[2:].zfill(256)
    3. Count how many bit positions differ (flipped bits):
       flipped = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    4. Return percentage of flipped bits: (flipped / 256.0) * 100.0
    """
    # TODO: YOUR CODE HERE (OPTIONAL EXTRA CREDIT)
    raise NotImplementedError("Bonus Mission 3.2: Implement measure_hash_avalanche")


# ==============================================================================
# 🧪 LOCAL SELF-TEST EVALUATION SUITE
# ==============================================================================

def run_all_tests():
    print("\n" + "=" * 75)
    print(" 🧪 CS-1XX / ECE-1XX BEGINNER CRYPTOGRAPHY ASSIGNMENT TEST RUNNER")
    print("=" * 75)

    passed_tasks = 0
    total_tasks = 7
    code_score = 0
    bonus_passed = False

    # --------------------------------------------------------------------------
    # Test 1: Task 2.1 (Caesar Cipher)
    # --------------------------------------------------------------------------
    print("\n[TEST 1] Task 2.1: Caesar Cipher (Encrypt & Decrypt)...")
    try:
        sample = "Hello, World! 2026"
        c3 = caesar_encrypt(sample, 3)
        assert c3 == "Khoor, Zruog! 2026", f"Caesar encrypt failed! Got: {c3}"
        p3 = caesar_decrypt(c3, 3)
        assert p3 == sample, f"Caesar decrypt failed! Got: {p3}"

        # Wraparound test
        assert caesar_encrypt("XYZxyz", 3) == "ABCabc", "Caesar alphabet wrap failed!"
        assert caesar_decrypt("ABCabc", 3) == "XYZxyz", "Caesar alphabet unwrap failed!"
        assert caesar_encrypt("Pass", 26) == "Pass", "Shift 26 modulo failed!"

        print("  --> ✅ PASS: Task 2.1 Passed (10/10 pts)")
        code_score += 10
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Task 2.1 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.1 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 2: Task 2.2 (XOR Cipher)
    # --------------------------------------------------------------------------
    print("\n[TEST 2] Task 2.2: XOR Bitwise Cipher...")
    try:
        msg = b"Top Secret Message: Launch Code 99!"
        key = b"CYBERKEY"
        cipher_bytes = xor_cipher(msg, key)
        assert cipher_bytes != msg, "Ciphertext should not equal plaintext!"
        assert len(cipher_bytes) == len(msg), "Ciphertext length must match plaintext!"
        decrypted_bytes = xor_cipher(cipher_bytes, key)
        assert decrypted_bytes == msg, "XOR double-encryption decryption failed!"

        print("  --> ✅ PASS: Task 2.2 Passed (10/10 pts)")
        code_score += 10
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Task 2.2 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.2 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 3: Task 2.3 (Euclidean GCD)
    # --------------------------------------------------------------------------
    print("\n[TEST 3] Task 2.3: Euclidean GCD Algorithm...")
    try:
        assert euclidean_gcd(48, 18) == 6, "GCD(48, 18) should be 6"
        assert euclidean_gcd(101, 103) == 1, "GCD of twin primes should be 1"
        assert euclidean_gcd(252, 105) == 21, "GCD(252, 105) should be 21"
        assert euclidean_gcd(17, 0) == 17, "GCD(17, 0) should be 17"

        print("  --> ✅ PASS: Task 2.3 Passed (10/10 pts)")
        code_score += 10
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Task 2.3 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.3 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 4: Task 2.4 (AES-256-GCM AEAD)
    # --------------------------------------------------------------------------
    print("\n[TEST 4] Task 2.4: AES-256-GCM Modern Encryption & Decryption...")
    try:
        key_32 = secrets.token_bytes(32)
        plaintext = "Super confidential database credentials!"
        nonce, ciphertext = aes_gcm_encrypt(plaintext, key_32)
        assert len(nonce) == 12, f"Nonce must be 12 bytes! Got {len(nonce)}"
        assert len(ciphertext) > len(plaintext), "Ciphertext must include 16-byte authentication tag!"
        
        decrypted = aes_gcm_decrypt(nonce, ciphertext, key_32)
        assert decrypted == plaintext, "AES-GCM decrypted text does not match!"

        # Tamper detection test
        tampered_ciphertext = bytearray(ciphertext)
        tampered_ciphertext[0] ^= 0x01  # Flip one bit
        tamper_caught = False
        try:
            aes_gcm_decrypt(nonce, bytes(tampered_ciphertext), key_32)
        except Exception:
            tamper_caught = True
        assert tamper_caught, "AES-GCM failed to catch tampered ciphertext!"

        print("  --> ✅ PASS: Task 2.4 Passed (10/10 pts)")
        code_score += 10
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Task 2.4 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.4 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 5: Task 2.5 (Diffie-Hellman Key Exchange)
    # --------------------------------------------------------------------------
    print("\n[TEST 5] Task 2.5: Diffie-Hellman Key Exchange...")
    try:
        p = 23
        g = 5
        alice_priv = 6
        bob_priv = 15

        alice_pub = dh_compute_public_key(g, alice_priv, p)
        bob_pub = dh_compute_public_key(g, bob_priv, p)

        assert alice_pub == 8, f"Alice pub expected 8, got {alice_pub}"
        assert bob_pub == 19, f"Bob pub expected 19, got {bob_pub}"

        alice_shared = dh_compute_shared_secret(bob_pub, alice_priv, p)
        bob_shared = dh_compute_shared_secret(alice_pub, bob_priv, p)

        assert alice_shared == bob_shared == 2, f"Shared secret mismatch! Expected 2, got {alice_shared} and {bob_shared}"

        print("  --> ✅ PASS: Task 2.5 Passed (10/10 pts)")
        code_score += 10
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Task 2.5 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.5 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 6: Task 2.6 (Toy RSA)
    # --------------------------------------------------------------------------
    print("\n[TEST 6] Task 2.6: Toy RSA Cryptosystem...")
    try:
        # Small prime example: p=61, q=53 -> n=3233, e=17, d=2753
        n = 3233
        e = 17
        d = 2753
        test_m = 65  # ASCII 'A'
        c = rsa_encrypt_toy(test_m, e, n)
        assert c != test_m, "Ciphertext should not equal plaintext message!"
        decrypted_m = rsa_decrypt_toy(c, d, n)
        assert decrypted_m == test_m, f"RSA decrypt failed! Expected {test_m}, got {decrypted_m}"

        print("  --> ✅ PASS: Task 2.6 Passed (10/10 pts)")
        code_score += 10
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Task 2.6 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Task 2.6 Error: {e}")

    # --------------------------------------------------------------------------
    # Test 7: Mission 3.1 (Detective Spy Message & SHA-256)
    # --------------------------------------------------------------------------
    print("\n[TEST 7] Mission 3.1: Intercepted Spy Message & SHA-256 Integrity...")
    try:
        # Intercepted ciphertext encrypted with shift = 7
        secret_spy_cipher = "AOL ZLJYLA HNLUA PZ TLLAPUN HA TPKUPNOA"
        key_found, plain_found = crack_simple_caesar(secret_spy_cipher, clue_word="AGENT")
        assert key_found == 7, f"Expected shift 7, got {key_found}"
        assert plain_found == "THE SECRET AGENT IS MEETING AT MIDNIGHT", f"Decrypted text incorrect: {plain_found}"

        expected_hash = hashlib.sha256(plain_found.encode('utf-8')).hexdigest()
        my_hash = compute_sha256_hex(plain_found)
        assert my_hash == expected_hash, f"SHA-256 hash mismatch! Got {my_hash}"

        print("  --> ✅ PASS: Mission 3.1 Passed (10/10 pts)")
        code_score += 10
        passed_tasks += 1
    except NotImplementedError:
        print("  --> ⏭️ TODO: Mission 3.1 not implemented yet.")
    except Exception as e:
        print(f"  --> ❌ FAIL: Mission 3.1 Error: {e}")

    # --------------------------------------------------------------------------
    # Bonus Test: Mission 3.2 (Hash Avalanche Effect)
    # --------------------------------------------------------------------------
    print("\n[BONUS TEST] Mission 3.2: Avalanche Effect (+10 Bonus pts)...")
    try:
        t1 = "The quick brown fox jumps over the lazy dog"
        t2 = "The quick brown fox jumps over the lazy cog"  # changed 1 letter: d -> c
        avalanche_pct = measure_hash_avalanche(t1, t2)
        print(f"  [Info] Avalanche bit-flip rate: {avalanche_pct:.2f}%")
        assert 40.0 <= avalanche_pct <= 60.0, f"Avalanche rate unexpected: {avalanche_pct}% (expected ~45-55%)"
        print("  --> 🌟 PASS: Bonus Mission 3.2 Passed (+10 Bonus pts)!")
        bonus_passed = True
    except NotImplementedError:
        print("  --> ⏭️ SKIPPED: Bonus Mission 3.2 not implemented (Optional).")
    except Exception as e:
        print(f"  --> ❌ FAIL: Bonus Mission 3.2 Error: {e}")

    # --------------------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------------------
    bonus_score = 10 if bonus_passed else 0
    print("\n" + "=" * 75)
    print(f" 🏆 AUTOMATED CODE SCORE: {code_score} / 70 Points ({passed_tasks}/{total_tasks} Tasks Passed)")
    if bonus_passed:
        print(f" 🌟 BONUS SCORE: +{bonus_score} Extra Credit Points")
    print(" 📝 Note: Part 1 Theory (30 pts) will be evaluated from your REPORT_BEGINNER.md.")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    run_all_tests()
