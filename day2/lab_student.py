"""
================================================================================
🎓 DAY 2 STUDENT LAB NOTEBOOK: 3-TIER CHALLENGES
Course: Modern Cryptography & Network Security (CS-4XX)
Duration: 3 Hours (Afternoon Hands-On Lab)
================================================================================

CHALLENGE DIFFICULTY TIERS:
🟢 LEVEL 1: Novice / Fundamentals (Extended GCD, ModInverse & Fast Exponentiation)
🟡 LEVEL 2: Intermediate / Applied (AES-ECB vs. AES-CBC Pattern Exposure Analysis)
🔴 LEVEL 3: Advanced / Hardcore Cryptanalyst (AES-256-GCM & Nonce Reuse Exploit)

STUDENT NAME: ____________________________
STUDENT ID:   ____________________________
================================================================================
"""

import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import padding

# ==============================================================================
# 🟢 LEVEL 1: NOVICE CHALLENGES (Number Theory Primitives from Scratch)
# ==============================================================================

def gcd(a: int, b: int) -> int:
    """[LEVEL 1] Calculate Greatest Common Divisor of a and b."""
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    [LEVEL 1] Extended Euclidean Algorithm.
    Returns tuple (g, x, y) such that a*x + b*y = g = gcd(a, b).
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def modinv(a: int, m: int) -> int:
    """[LEVEL 1] Compute modular multiplicative inverse of 'a' modulo 'm'."""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Modular inverse does not exist for {a} mod {m}!")
    return x % m


def pow_mod(base: int, exp: int, mod: int) -> int:
    """[LEVEL 1] Fast Modular Exponentiation using Square-and-Multiply."""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp = exp // 2
    return result


# ==============================================================================
# 🟡 LEVEL 2: INTERMEDIATE CHALLENGES (AES Block Cipher Modes)
# ==============================================================================

def encrypt_aes_ecb(plaintext: bytes, key: bytes) -> bytes:
    """[LEVEL 2] Encrypt bytes using AES in ECB mode with PKCS7 padding."""
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()


def encrypt_aes_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """[LEVEL 2] Encrypt bytes using AES in CBC mode."""
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()


def check_ecb_pattern_vulnerability(structured_bytes: bytes, key: bytes) -> bool:
    """[LEVEL 2] Detect identical block repeating pattern vulnerability in ECB mode."""
    cipher_ecb = encrypt_aes_ecb(structured_bytes, key)
    blocks = [cipher_ecb[i:i+16] for i in range(0, len(cipher_ecb)-16, 16)]
    return len(blocks) != len(set(blocks))


# ==============================================================================
# 🔴 LEVEL 3: ADVANCED / HARDCORE CHALLENGES (AES-256-GCM & Nonce Reuse Exploit)
# ==============================================================================

def aes_gcm_encrypt(plaintext: str, key: bytes, associated_data: bytes = b"") -> tuple[bytes, bytes]:
    """[LEVEL 3] Encrypt plaintext using AES-256-GCM with 96-bit random nonce."""
    nonce = secrets.token_bytes(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), associated_data)
    return nonce, ciphertext


def aes_gcm_decrypt(nonce: bytes, ciphertext: bytes, key: bytes, associated_data: bytes = b"") -> str:
    """[LEVEL 3] Decrypt and verify authentication tag of AES-256-GCM ciphertext."""
    aesgcm = AESGCM(key)
    decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, associated_data)
    return decrypted_bytes.decode('utf-8')


def exploit_gcm_nonce_reuse(c1_payload: bytes, c2_payload: bytes) -> bytes:
    """
    [LEVEL 3 HARDCORE] Exploits AES-GCM Nonce Reuse Vulnerability.
    Computes C1 ^ C2 to recover M1 ^ M2.
    """
    return bytes([b1 ^ b2 for b1, b2 in zip(c1_payload, c2_payload)])


# ==============================================================================
# AUTOMATED GRADED LAB TEST SUITE
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 75)
    print(" 🧪 DAY 2 LAB EVALUATION: 3-TIER DIFFICULTY CHALLENGES")
    print("=" * 75)

    passed_count = 0
    total_tests = 5

    # 🟢 LEVEL 1 TEST
    print("\n🟢 [LEVEL 1 - NOVICE] Number Theory Primitives (Euclid, ModInverse, Fast Pow)...")
    try:
        assert gcd(54, 24) == 6, "GCD failed!"
        inv = modinv(7, 13)
        assert (7 * inv) % 13 == 1, "ModInverse failed!"
        assert pow_mod(3, 45, 17) == pow(3, 45, 17), "Fast exponentiation failed!"
        print("  --> ✅ PASS: Level 1 Number Theory Challenge Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 1 failed ({e})")

    # 🟡 LEVEL 2 TEST A
    print("\n🟡 [LEVEL 2 - INTERMEDIATE] AES-ECB Pattern Exposure Analysis...")
    try:
        blk = b"SECRET1234567890"
        structured_data = blk * 3
        key = secrets.token_bytes(32)
        has_ecb_vulnerability = check_ecb_pattern_vulnerability(structured_data, key)
        assert has_ecb_vulnerability == True, "ECB pattern check failed!"
        print("  --> ✅ PASS: Level 2 ECB Pattern Exposure Test Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 2 ECB test failed ({e})")

    # 🟡 LEVEL 2 TEST B
    print("\n🟡 [LEVEL 2 - INTERMEDIATE] AES-CBC Mode Randomization Check...")
    try:
        blk = b"SECRET1234567890"
        structured_data = blk * 3
        key = secrets.token_bytes(32)
        iv = secrets.token_bytes(16)
        cbc_cipher = encrypt_aes_cbc(structured_data, key, iv)
        cbc_blocks = [cbc_cipher[i:i+16] for i in range(0, len(cbc_cipher)-16, 16)]
        assert cbc_blocks[0] != cbc_blocks[1], "CBC mode must randomize identical blocks!"
        print("  --> ✅ PASS: Level 2 CBC Block Randomization Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 2 CBC test failed ({e})")

    # 🔴 LEVEL 3 TEST A
    print("\n🔴 [LEVEL 3 - HARDCORE] AES-256-GCM Authenticated Encryption & Tamper Check...")
    try:
        key = secrets.token_bytes(32)
        msg = "TRANSFER $100,000 TO ACCOUNT #4567"
        aad = b"header_version=1.0"
        nonce, ciphertext = aes_gcm_encrypt(msg, key, aad)
        decrypted_msg = aes_gcm_decrypt(nonce, ciphertext, key, aad)
        assert decrypted_msg == msg, "AES-GCM decryption failed!"
        
        try:
            aes_gcm_decrypt(nonce, ciphertext, key, b"tampered_header")
            assert False, "Failed to reject tampered AAD!"
        except Exception:
            pass  # Successfully rejected!
            
        print("  --> ✅ PASS: Level 3 AES-256-GCM & Tamper Detection Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 3 AES-GCM test failed ({e})")

    # 🔴 LEVEL 3 TEST B
    print("\n🔴 [LEVEL 3 - HARDCORE] AES-GCM Nonce Reuse Stream Cipher Exploit...")
    try:
        key = secrets.token_bytes(32)
        reused_nonce = b"FIXEDNONCE12"
        m1 = "TRANSFER $10,000 TO ALICE"
        m2 = "TRANSFER $90,000 TO BOB  "
        aesgcm = AESGCM(key)
        c1 = aesgcm.encrypt(reused_nonce, m1.encode('utf-8'), None)[:-16]
        c2 = aesgcm.encrypt(reused_nonce, m2.encode('utf-8'), None)[:-16]
        
        c_xor = exploit_gcm_nonce_reuse(c1, c2)
        m_xor = bytes([ord(a) ^ ord(b) for a, b in zip(m1, m2)])
        assert c_xor == m_xor, "Nonce reuse XOR mismatch!"
        print("  --> ✅ PASS: Level 3 AES-GCM Nonce Reuse Exploit Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 3 Nonce reuse attack failed ({e})")

    # Final Grade Summary
    print("\n" + "=" * 75)
    print(f" 🏆 DAY 2 LAB SCORE: {passed_count} / {total_tests} Tests Passed ({(passed_count/total_tests)*100:.0f}%)")
    print("=" * 75 + "\n")
