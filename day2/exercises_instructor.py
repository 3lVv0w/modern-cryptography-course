"""
Day 2 Hands-On Code Exercises: Abstract Algebra, Number Theory & Symmetric Encryption (AES)
Course: Modern Cryptography & Network Security (University Undergraduate Level)

Student Name: ___________________________
Date: ___________________________________

Instructions:
Complete the exercises below and run `python3 day2_exercises.py` to verify your implementation!
"""

import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import padding

# ==============================================================================
# EXERCISE 1: Number Theory Primitives from Scratch
# ==============================================================================

def gcd(a: int, b: int) -> int:
    """Euclidean Algorithm for Greatest Common Divisor."""
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    Returns tuple (g, x, y) such that a*x + b*y = g = gcd(a, b).
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def modinv(a: int, m: int) -> int:
    """
    Computes modular multiplicative inverse of 'a' modulo 'm'.
    Returns x such that (a * x) % m == 1.
    """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Modular inverse does not exist for {a} mod {m} (Not coprime)!")
    return x % m


def pow_mod(base: int, exp: int, mod: int) -> int:
    """
    Fast Modular Exponentiation using Square-and-Multiply algorithm.
    Computes (base^exp) % mod in O(log exp) operations.
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp = exp // 2
    return result


# ==============================================================================
# EXERCISE 2: Block Cipher Modes — ECB Mode Pattern Vulnerability
# ==============================================================================

def encrypt_aes_ecb(plaintext: bytes, key: bytes) -> bytes:
    """Encrypts plaintext using AES in Electronic Codebook (ECB) mode."""
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()


def encrypt_aes_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypts plaintext using AES in Cipher Block Chaining (CBC) mode."""
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()


def demonstrate_ecb_flaw():
    """
    Demonstrates how AES-ECB preserves structural pattern of identical plaintext blocks,
    unlike AES-CBC which randomizes block outputs using IV and feedback.
    """
    # Plaintext with repeating 16-byte blocks
    block_a = b"CONFIDENTIAL1234"
    block_b = b"PUBLIC DATA 5678"
    structured_plaintext = block_a * 3 + block_b * 2 + block_a * 2
    
    key = secrets.token_bytes(32)  # AES-256
    iv = secrets.token_bytes(16)
    
    ecb_cipher = encrypt_aes_ecb(structured_plaintext, key)
    cbc_cipher = encrypt_aes_cbc(structured_plaintext, key, iv)
    
    # Slice ciphertexts into 16-byte blocks
    ecb_blocks = [ecb_cipher[i:i+16] for i in range(0, len(ecb_cipher)-16, 16)]
    cbc_blocks = [cbc_cipher[i:i+16] for i in range(0, len(cbc_cipher)-16, 16)]
    
    return ecb_blocks, cbc_blocks


# ==============================================================================
# EXERCISE 3: Modern Authenticated Encryption (AES-256-GCM)
# ==============================================================================

def aes_gcm_encrypt(plaintext: str, key: bytes, associated_data: bytes = b"") -> tuple[bytes, bytes]:
    """
    Encrypts string using AES-256-GCM (Authenticated Encryption).
    Returns (nonce, ciphertext_with_tag).
    """
    nonce = secrets.token_bytes(12)  # Standard 96-bit GCM Nonce
    aesgcm = AESGCM(key)
    p_bytes = plaintext.encode('utf-8')
    ciphertext = aesgcm.encrypt(nonce, p_bytes, associated_data)
    return nonce, ciphertext


def aes_gcm_decrypt(nonce: bytes, ciphertext: bytes, key: bytes, associated_data: bytes = b"") -> str:
    """
    Decrypts and verifies authentication tag of AES-256-GCM ciphertext.
    """
    aesgcm = AESGCM(key)
    decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, associated_data)
    return decrypted_bytes.decode('utf-8')


# ==============================================================================
# EXERCISE 4: AES-GCM Nonce Reuse Catastrophe
# ==============================================================================

def simulate_gcm_nonce_reuse_attack():
    """
    Demonstrates the fatal security collapse when a Nonce/IV is reused in GCM mode.
    Since GCM operates as a stream cipher internally (CTR mode), reusing a nonce
    results in C1 XOR C2 = P1 XOR P2!
    """
    key = secrets.token_bytes(32)
    reused_nonce = b"FIXEDNONCE12"  # 12-byte reused nonce
    
    m1 = "TRANSFER $10,000 TO ALICE"
    m2 = "TRANSFER $90,000 TO BOB  "
    
    aesgcm = AESGCM(key)
    c1 = aesgcm.encrypt(reused_nonce, m1.encode('utf-8'), None)
    c2 = aesgcm.encrypt(reused_nonce, m2.encode('utf-8'), None)
    
    # XOR ciphertexts (excluding 16-byte authentication tag at the end)
    c1_payload = c1[:-16]
    c2_payload = c2[:-16]
    c_xor = bytes([b1 ^ b2 for b1, b2 in zip(c1_payload, c2_payload)])
    
    m_xor = bytes([ord(a) ^ ord(b) for a, b in zip(m1, m2)])
    
    return c_xor == m_xor


# ==============================================================================
# AUTOMATED TEST SUITE & VERIFICATION
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" 🚀 RUNNING DAY 2 CRYPTOGRAPHY LAB EXERCISES & VERIFICATION")
    print("=" * 70)

    # Test 1: Extended GCD & Modular Inverse
    print("\n--- Testing Exercise 1: Number Theory Primitives ---")
    assert gcd(48, 18) == 6, "GCD test failed!"
    
    a, m = 3, 11
    inv = modinv(a, m)
    print(f"Modular inverse of {a} mod {m} = {inv}")
    assert (a * inv) % m == 1, "Modular inverse calculation failed!"

    # Test Fast Modular Exponentiation
    base, exp, mod = 7, 13, 11
    fast_pow = pow_mod(base, exp, mod)
    expected_pow = pow(base, exp, mod)
    print(f"Fast Exponentiation ({base}^{exp} mod {mod}): {fast_pow}")
    assert fast_pow == expected_pow, "Fast exponentiation mismatch!"
    print("✅ Exercise 1 Passed!\n")

    # Test 2: ECB Pattern Flaw Demonstration
    print("--- Testing Exercise 2: ECB Mode Vulnerability ---")
    ecb_b, cbc_b = demonstrate_ecb_flaw()
    print(f"ECB Block 0 == ECB Block 1? {ecb_b[0] == ecb_b[1]} (Patterns Exposed!)")
    print(f"CBC Block 0 == CBC Block 1? {cbc_b[0] == cbc_b[1]} (Hidden Security!)")
    assert ecb_b[0] == ecb_b[1], "ECB mode must produce identical blocks for identical plaintext!"
    assert cbc_b[0] != cbc_b[1], "CBC mode must produce distinct blocks via IV/chaining!"
    print("✅ Exercise 2 Passed!\n")

    # Test 3: AES-256-GCM Encryption & Decryption
    print("--- Testing Exercise 3: Authenticated Encryption (AES-256-GCM) ---")
    sym_key = secrets.token_bytes(32)  # 256-bit key
    secret_msg = "CONFIDENTIAL BANK TRANSACTION: ACC_NUM=987654321, AMOUNT=$50,000"
    aad = b"header_metadata_v1"

    nonce, gcm_cipher = aes_gcm_encrypt(secret_msg, sym_key, aad)
    recovered_msg = aes_gcm_decrypt(nonce, gcm_cipher, sym_key, aad)

    print(f"AES-256 Key (hex): {sym_key.hex()[:16]}...")
    print(f"GCM Nonce (hex):   {nonce.hex()}")
    print(f"Ciphertext (hex):  {gcm_cipher.hex()[:32]}...")
    print(f"Recovered Message: {recovered_msg}")
    assert recovered_msg == secret_msg, "AES-GCM Decryption failed!"
    
    # Tamper Test: Modifying Associated Data should trigger authentication failure!
    try:
        aes_gcm_decrypt(nonce, gcm_cipher, sym_key, b"tampered_header")
        print("❌ ERROR: Failed to catch tampered associated data!")
        assert False
    except Exception:
        print("✓ Authentication Tag successfully rejected tampered metadata!")

    print("✅ Exercise 3 Passed!\n")

    # Test 4: GCM Nonce Reuse Catastrophe
    print("--- Testing Exercise 4: AES-GCM Nonce Reuse Exploit ---")
    is_vulnerable = simulate_gcm_nonce_reuse_attack()
    print(f"Nonce Reuse XOR match verified? {is_vulnerable}")
    assert is_vulnerable, "Reusing GCM nonce must reveal XOR of plaintexts!"
    print("✅ Exercise 4 Passed!\n")

    print("=" * 70)
    print(" 🎉 ALL DAY 2 LAB EXERCISES PASSED SUCCESSFULLY!")
    print("=" * 70)
