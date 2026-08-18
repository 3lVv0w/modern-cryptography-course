"""
================================================================================
🎓 DAY 3 STUDENT LAB NOTEBOOK: 3-TIER CHALLENGES
Course: Modern Cryptography & Network Security (CS-4XX)
Duration: 3 Hours (Afternoon Hands-On Lab)
================================================================================

CHALLENGE DIFFICULTY TIERS:
🟢 LEVEL 1: Novice / Fundamentals (Diffie-Hellman Key Exchange Simulator)
🟡 LEVEL 2: Intermediate / Applied (Full RSA Implementation & String Converter)
🔴 LEVEL 3: Advanced / Hardcore Cryptanalyst (Fermat RSA Factorization Attack & Curve25519)

STUDENT NAME: ____________________________
STUDENT ID:   ____________________________
================================================================================
"""

import math
import secrets
from cryptography.hazmat.primitives.asymmetric import x25519

# Number Theory Helpers
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def modinv(a: int, m: int) -> int:
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Modular inverse does not exist for {a} mod {m}!")
    return x % m


# ==============================================================================
# 🟢 LEVEL 1: NOVICE CHALLENGES (Diffie-Hellman Key Exchange)
# ==============================================================================

def dh_generate_keypair(p: int, g: int) -> tuple[int, int]:
    """[LEVEL 1] Generate Diffie-Hellman keypair for prime 'p' and generator 'g'."""
    private_key = secrets.randbelow(p - 2) + 2
    public_key = pow(g, private_key, p)
    return private_key, public_key


def dh_compute_shared_secret(their_public_key: int, my_private_key: int, p: int) -> int:
    """[LEVEL 1] Compute shared secret: S = (their_public_key ^ my_private_key) % p."""
    return pow(their_public_key, my_private_key, p)


# ==============================================================================
# 🟡 LEVEL 2: INTERMEDIATE CHALLENGES (Full RSA Cryptosystem)
# ==============================================================================

def str_to_int(s: str) -> int:
    """Converts text string to integer representation."""
    return int.from_bytes(s.encode('utf-8'), byteorder='big')

def int_to_str(i: int) -> str:
    """Converts integer back to text string."""
    length = (i.bit_length() + 7) // 8
    return i.to_bytes(length, byteorder='big').decode('utf-8', errors='ignore')


def rsa_keygen(p: int, q: int, e: int = 65537) -> tuple[tuple[int, int], tuple[int, int]]:
    """[LEVEL 2] RSA Key Generation (Compute N, phi(N), and d)."""
    N = p * q
    phi_N = (p - 1) * (q - 1)
    if math.gcd(e, phi_N) != 1:
        e = 3  # Fallback for small test primes
    d = modinv(e, phi_N)
    return (N, e), (N, d)


def rsa_encrypt(message_int: int, public_key: tuple[int, int]) -> int:
    """[LEVEL 2] RSA Encryption: C = (M ^ e) % N."""
    N, e = public_key
    if message_int >= N:
        raise ValueError(f"Message integer ({message_int}) must be strictly smaller than N ({N})!")
    return pow(message_int, e, N)


def rsa_decrypt(ciphertext_int: int, private_key: tuple[int, int]) -> int:
    """[LEVEL 2] RSA Decryption: M = (C ^ d) % N."""
    N, d = private_key
    return pow(ciphertext_int, d, N)


# ==============================================================================
# 🔴 LEVEL 3: ADVANCED / HARDCORE CHALLENGES (Fermat Attack & Curve25519)
# ==============================================================================

def fermat_factor(N: int) -> tuple[int, int]:
    """[LEVEL 3 HARDCORE] Factor N = p * q when p and q are close (a^2 - b^2 = N)."""
    a = math.isqrt(N)
    if a * a < N:
        a += 1
    
    b2 = a * a - N
    while not math.isqrt(b2) ** 2 == b2:
        a += 1
        b2 = a * a - N
        
    b = math.isqrt(b2)
    p = a - b
    q = a + b
    return p, q


def crack_rsa_ciphertext(N: int, e: int, ciphertext: int) -> int:
    """[LEVEL 3 HARDCORE] Crack RSA ciphertext without private key via Fermat factorization."""
    p, q = fermat_factor(N)
    phi_N = (p - 1) * (q - 1)
    d = modinv(e, phi_N)
    return rsa_decrypt(ciphertext, (N, d))


def ecdh_x25519_key_exchange() -> tuple[bytes, bytes]:
    """[LEVEL 3 HARDCORE] Curve25519 (X25519) Elliptic Curve Key Exchange."""
    alice_private = x25519.X25519PrivateKey.generate()
    alice_public = alice_private.public_key()

    bob_private = x25519.X25519PrivateKey.generate()
    bob_public = bob_private.public_key()

    alice_shared = alice_private.exchange(bob_public)
    bob_shared = bob_private.exchange(alice_public)

    return alice_shared, bob_shared


# ==============================================================================
# AUTOMATED GRADED LAB TEST SUITE
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 75)
    print(" 🧪 DAY 3 LAB EVALUATION: 3-TIER DIFFICULTY CHALLENGES")
    print("=" * 75)

    passed_count = 0
    total_tests = 5

    # 🟢 LEVEL 1 TEST
    print("\n🟢 [LEVEL 1 - NOVICE] Diffie-Hellman Key Exchange (DHKE)...")
    try:
        p_val, g_val = 23, 5
        a_priv, a_pub = dh_generate_keypair(p_val, g_val)
        b_priv, b_pub = dh_generate_keypair(p_val, g_val)
        s_a = dh_compute_shared_secret(b_pub, a_priv, p_val)
        s_b = dh_compute_shared_secret(a_pub, b_priv, p_val)
        assert s_a == s_b, "DHKE shared secret mismatch!"
        print(f"  --> ✅ PASS: Level 1 DHKE Handshake Passed (Shared Secret = {s_a})!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 1 failed ({e})")

    # 🟡 LEVEL 2 TEST A
    print("\n🟡 [LEVEL 2 - INTERMEDIATE] RSA Key Generation & Math Proof...")
    try:
        p_t, q_t = 61, 53
        pub_k, priv_k = rsa_keygen(p_t, q_t)
        N_t, e_t = pub_k
        _, d_t = priv_k
        assert N_t == 61 * 53 == 3233, "Modulus N incorrect!"
        assert (e_t * d_t) % ((p_t - 1) * (q_t - 1)) == 1, "(e * d) mod phi(N) must be 1!"
        print("  --> ✅ PASS: Level 2 RSA Key Generation Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 2 RSA Keygen failed ({e})")

    # 🟡 LEVEL 2 TEST B
    print("\n🟡 [LEVEL 2 - INTERMEDIATE] RSA String Encryption & Decryption...")
    try:
        p_t, q_t = 1009, 1013  # N = 1022117
        pub_k, priv_k = rsa_keygen(p_t, q_t)
        secret_s = "HI"
        c_int = rsa_encrypt(str_to_int(secret_s), pub_k)
        d_int = rsa_decrypt(c_int, priv_k)
        assert int_to_str(d_int) == secret_s, "RSA String Decryption failed!"
        print("  --> ✅ PASS: Level 2 RSA Encryption/Decryption Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 2 RSA Encrypt/Decrypt failed ({e})")

    # 🔴 LEVEL 3 TEST A
    print("\n🔴 [LEVEL 3 - HARDCORE] Fermat Factorization Attack on Weak RSA...")
    try:
        weak_p, weak_q = 1009, 1013
        weak_pub, _ = rsa_keygen(weak_p, weak_q, e=65537)
        weak_N, weak_e = weak_pub
        target_m = 9999
        target_c = rsa_encrypt(target_m, weak_pub)
        
        cracked_m = crack_rsa_ciphertext(weak_N, weak_e, target_c)
        assert cracked_m == target_m, "Fermat RSA attack failed!"
        print(f"  --> ✅ PASS: Level 3 Fermat RSA Attack Passed (Cracked = {cracked_m})!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 3 Fermat attack failed ({e})")

    # 🔴 LEVEL 3 TEST B
    print("\n🔴 [LEVEL 3 - HARDCORE] Curve25519 (X25519) Elliptic Curve Key Exchange...")
    try:
        alice_s, bob_s = ecdh_x25519_key_exchange()
        assert alice_s == bob_s and len(alice_s) == 32, "ECDH test failed!"
        print("  --> ✅ PASS: Level 3 Curve25519 ECDH Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 3 ECDH test failed ({e})")

    # Final Grade Summary
    print("\n" + "=" * 75)
    print(f" 🏆 DAY 3 LAB SCORE: {passed_count} / {total_tests} Tests Passed ({(passed_count/total_tests)*100:.0f}%)")
    print("=" * 75 + "\n")
