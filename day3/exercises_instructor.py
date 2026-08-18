"""
Day 3 Hands-On Code Exercises: Public-Key Cryptography (DHKE, RSA & Elliptic Curves)
Course: Modern Cryptography & Network Security (University Undergraduate Level)

Student Name: ___________________________
Date: ___________________________________

Instructions:
Complete the exercises below and run `python3 day3_exercises.py` to verify your implementation!
"""

import math
import secrets
from cryptography.hazmat.primitives.asymmetric import x25519

# Helper functions from Day 2
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
        raise ValueError(f"Modular inverse does not exist for {a} mod {m}")
    return x % m


# ==============================================================================
# EXERCISE 1: Diffie-Hellman Key Exchange (DHKE)
# ==============================================================================

def dh_generate_keys(p: int, g: int) -> tuple[int, int]:
    """
    Generates Diffie-Hellman keypair for prime 'p' and generator 'g'.
    Returns (private_key, public_key) where public_key = (g ^ private_key) % p.
    """
    private_key = secrets.randbelow(p - 2) + 2
    public_key = pow(g, private_key, p)
    return private_key, public_key


def dh_compute_shared_secret(their_public_key: int, my_private_key: int, p: int) -> int:
    """Computes shared secret: S = (their_public_key ^ my_private_key) % p."""
    return pow(their_public_key, my_private_key, p)


# ==============================================================================
# EXERCISE 2: Complete RSA Implementation from Scratch
# ==============================================================================

def str_to_int(s: str) -> int:
    """Converts a text string to an integer."""
    return int.from_bytes(s.encode('utf-8'), byteorder='big')

def int_to_str(i: int) -> str:
    """Converts an integer back to a text string."""
    length = (i.bit_length() + 7) // 8
    return i.to_bytes(length, byteorder='big').decode('utf-8', errors='ignore')


def rsa_keygen(p: int, q: int, e: int = 65537) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Generates RSA Keypair given distinct primes p and q.
    Returns ( (N, e), (N, d) ) -> (Public Key, Private Key).
    """
    N = p * q
    phi_N = (p - 1) * (q - 1)
    
    if math.gcd(e, phi_N) != 1:
        e = 3  # Fallback for small prime test cases
        
    d = modinv(e, phi_N)
    return (N, e), (N, d)


def rsa_encrypt(message_int: int, public_key: tuple[int, int]) -> int:
    """RSA Encryption: C = (M^e) % N."""
    N, e = public_key
    if message_int >= N:
        raise ValueError(f"Message integer ({message_int}) must be strictly smaller than RSA modulus N ({N})!")
    return pow(message_int, e, N)


def rsa_decrypt(ciphertext_int: int, private_key: tuple[int, int]) -> int:
    """RSA Decryption: M = (C^d) % N."""
    N, d = private_key
    return pow(ciphertext_int, d, N)


# ==============================================================================
# EXERCISE 3: Cryptanalysis — Fermat's RSA Factorization Attack
# ==============================================================================

def fermat_factor(N: int) -> tuple[int, int]:
    """
    Fermat's Factorization Algorithm.
    Factors N = p * q when primes p and q are close to sqrt(N).
    Based on N = a^2 - b^2 = (a - b)(a + b).
    """
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
    """
    Cracks RSA ciphertext given only public key (N, e) using Fermat Factorization!
    1. Factors N -> p, q
    2. Calculates phi(N) = (p-1)(q-1)
    3. Computes private exponent d = modinv(e, phi(N))
    4. Decrypts ciphertext -> M
    """
    p, q = fermat_factor(N)
    phi_N = (p - 1) * (q - 1)
    d = modinv(e, phi_N)
    return rsa_decrypt(ciphertext, (N, d))


# ==============================================================================
# EXERCISE 4: Modern Elliptic Curve Cryptography (ECDH with X25519)
# ==============================================================================

def ecdh_x25519_key_exchange() -> tuple[bytes, bytes]:
    """
    Demonstrates Elliptic Curve Diffie-Hellman (ECDH) using Curve25519 (X25519).
    Returns (alice_shared_key, bob_shared_key) bytes.
    """
    # Alice generates X25519 keypair
    alice_private = x25519.X25519PrivateKey.generate()
    alice_public = alice_private.public_key()

    # Bob generates X25519 keypair
    bob_private = x25519.X25519PrivateKey.generate()
    bob_public = bob_private.public_key()

    # Alice & Bob derive shared 256-bit secret key
    alice_shared = alice_private.exchange(bob_public)
    bob_shared = bob_private.exchange(alice_public)

    return alice_shared, bob_shared


# ==============================================================================
# AUTOMATED TEST SUITE & VERIFICATION
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" 🚀 RUNNING DAY 3 CRYPTOGRAPHY LAB EXERCISES & VERIFICATION")
    print("=" * 70)

    # Test 1: Diffie-Hellman Key Exchange
    print("\n--- Testing Exercise 1: Diffie-Hellman Key Exchange ---")
    p = 23  # Public prime
    g = 5   # Public generator
    
    alice_priv, alice_pub = dh_generate_keys(p, g)
    bob_priv, bob_pub = dh_generate_keys(p, g)

    s_alice = dh_compute_shared_secret(bob_pub, alice_priv, p)
    s_bob = dh_compute_shared_secret(alice_pub, bob_priv, p)

    print(f"Alice Public Key: {alice_pub}, Bob Public Key: {bob_pub}")
    print(f"Alice Derived Secret: {s_alice}, Bob Derived Secret: {s_bob}")
    assert s_alice == s_bob, "Diffie-Hellman shared secret mismatch!"
    print("✅ Exercise 1 Passed!\n")

    # Test 2: RSA Encryption & Decryption
    print("--- Testing Exercise 2: RSA Implementation from Scratch ---")
    # Using primes large enough so N > message_int (e.g. N = 1009 * 1013 = 1022117)
    p_prime, q_prime = 1009, 1013
    pub_key, priv_key = rsa_keygen(p_prime, q_prime)
    
    secret_text = "HI"  # str_to_int("HI") = 18505 < 1022117
    msg_int = str_to_int(secret_text)
    cipher_int = rsa_encrypt(msg_int, pub_key)
    decrypted_int = rsa_decrypt(cipher_int, priv_key)
    recovered_text = int_to_str(decrypted_int)

    print(f"RSA Public Key (N, e):  {pub_key}")
    print(f"RSA Private Key (N, d): {priv_key}")
    print(f"Original Text: {secret_text} (Integer: {msg_int})")
    print(f"Ciphertext:    {cipher_int}")
    print(f"Recovered:     {recovered_text}")
    assert recovered_text == secret_text, "RSA Decryption Mismatch!"
    print("✅ Exercise 2 Passed!\n")

    # Test 3: Fermat Factorization Attack on Weak RSA
    print("--- Testing Exercise 3: RSA Fermat Factorization Attack ---")
    # Weak RSA key generated from close primes p=1009, q=1013 -> N = 1022117
    weak_p, weak_q = 1009, 1013
    weak_pub, weak_priv = rsa_keygen(weak_p, weak_q, e=65537)
    weak_N, weak_e = weak_pub
    
    target_msg = 12345
    target_cipher = rsa_encrypt(target_msg, weak_pub)
    
    print(f"Target Public Key N = {weak_N}, e = {weak_e}")
    print(f"Target Ciphertext   = {target_cipher}")

    cracked_msg = crack_rsa_ciphertext(weak_N, weak_e, target_cipher)
    print(f"Fermat Crack Result = {cracked_msg}")
    assert cracked_msg == target_msg, "Fermat RSA Factorization Attack failed!"
    print("✅ Exercise 3 Passed!\n")

    # Test 4: ECDH (X25519) Key Exchange
    print("--- Testing Exercise 4: Curve25519 (X25519) ECDH Key Exchange ---")
    alice_s, bob_s = ecdh_x25519_key_exchange()
    print(f"Alice ECDH Shared Key (hex): {alice_s.hex()}")
    print(f"Bob ECDH Shared Key   (hex): {bob_s.hex()}")
    assert alice_s == bob_s, "ECDH shared key mismatch!"
    print("✅ Exercise 4 Passed!\n")

    print("=" * 70)
    print(" 🎉 ALL DAY 3 LAB EXERCISES PASSED SUCCESSFULLY!")
    print("=" * 70)
