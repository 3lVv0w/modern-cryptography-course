"""
Day 4 Hands-On Code Exercises: Hashing, Digital Signatures, PKI & Capstone CTF
Course: Modern Cryptography & Network Security (University Undergraduate Level)

Student Name: ___________________________
Date: ___________________________________

Instructions:
Complete the exercises below and run `python3 day4_exercises.py` to verify your implementation!
"""

import datetime
import hashlib
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.x509.oid import NameOID

# ==============================================================================
# EXERCISE 1: Cryptographic Hash Properties & The Avalanche Effect
# ==============================================================================

def compute_sha256(data: bytes) -> str:
    """Computes SHA-256 hex digest of input bytes."""
    return hashlib.sha256(data).hexdigest()


def measure_avalanche_effect(text1: str, text2: str) -> float:
    """
    Measures the percentage of bits flipped between SHA-256(text1) and SHA-256(text2).
    A secure hash function exhibits an Avalanche Effect where a 1-bit input change
    results in ~50% of output bits changing unpredictably.
    """
    h1_hex = compute_sha256(text1.encode('utf-8'))
    h2_hex = compute_sha256(text2.encode('utf-8'))
    
    # Convert hex to binary strings padded to 256 bits
    b1 = bin(int(h1_hex, 16))[2:].zfill(256)
    b2 = bin(int(h2_hex, 16))[2:].zfill(256)
    
    # Count flipped bits
    flipped = sum(bit1 != bit2 for bit1, bit2 in zip(b1, b2))
    percentage = (flipped / 256.0) * 100.0
    return percentage


# ==============================================================================
# EXERCISE 2: Digital Signatures with Ed25519
# ==============================================================================

def generate_ed25519_keypair():
    """Generates Ed25519 private key and public key."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key


def sign_message(private_key: ed25519.Ed25519PrivateKey, message: bytes) -> bytes:
    """Signs message bytes using Ed25519 private key."""
    return private_key.sign(message)


def verify_signature(public_key: ed25519.Ed25519PublicKey, signature: bytes, message: bytes) -> bool:
    """
    Verifies Ed25519 signature over message bytes using public key.
    Returns True if authentic, False if signature or message was tampered with.
    """
    try:
        public_key.verify(signature, message)
        return True
    except Exception:
        return False


# ==============================================================================
# EXERCISE 3: X.509 Certificate Chain Inspection & Verification
# ==============================================================================

def create_mock_certificate_chain():
    """
    Generates a mock Root CA certificate and a Leaf domain certificate
    for testing X.509 PKI validation logic.
    """
    # Generate Root CA key & cert
    root_priv = ed25519.Ed25519PrivateKey.generate()
    root_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "University Root CA")])
    
    root_cert = x509.CertificateBuilder().subject_name(
        root_name
    ).issuer_name(
        root_name  # Self-signed
    ).public_key(
        root_priv.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    ).sign(root_priv, algorithm=None)

    # Generate Leaf Domain key & cert signed by Root CA
    leaf_priv = ed25519.Ed25519PrivateKey.generate()
    leaf_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "secure-university.edu")])
    
    leaf_cert = x509.CertificateBuilder().subject_name(
        leaf_name
    ).issuer_name(
        root_name  # Issued by Root CA
    ).public_key(
        leaf_priv.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
    ).sign(root_priv, algorithm=None)

    return root_cert, leaf_cert


def verify_leaf_against_root(leaf_cert: x509.Certificate, root_cert: x509.Certificate) -> bool:
    """
    Verifies that leaf_cert was issued and signed by root_cert's public key.
    """
    try:
        root_pubkey = root_cert.public_key()
        root_pubkey.verify(leaf_cert.signature, leaf_cert.tbs_certificate_bytes)
        return True
    except Exception:
        return False


# ==============================================================================
# EXERCISE 4: Capstone Mini-CTF Solver ("Operation Broken Envelope")
# ==============================================================================

def decrypt_caesar(ciphertext: str, shift: int) -> str:
    """Helper Caesar decrypt function."""
    res = []
    for c in ciphertext:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            res.append(chr((ord(c) - base - shift) % 26 + base))
        else:
            res.append(c)
    return "".join(res)


def solve_ctf_challenge(ciphertext: str, target_sha256: str, sender_pubkey: ed25519.Ed25519PublicKey, signature: bytes) -> str:
    """
    Automated Capstone CTF Solver.
    1. Brute-forces Caesar shifts [0..25].
    2. Filters candidates whose SHA-256 hash matches target_sha256.
    3. Verifies Ed25519 signature using sender_pubkey.
    4. Returns the verified secret flag!
    """
    for shift in range(26):
        candidate = decrypt_caesar(ciphertext, shift)
        cand_bytes = candidate.encode('utf-8')
        
        # Check Hash Match
        if compute_sha256(cand_bytes) == target_sha256:
            # Check Digital Signature Match
            if verify_signature(sender_pubkey, signature, cand_bytes):
                return candidate
                
    raise ValueError("CTF Solver failed to find valid payload!")


# ==============================================================================
# AUTOMATED TEST SUITE & VERIFICATION
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" 🚀 RUNNING DAY 4 CRYPTOGRAPHY LAB EXERCISES & VERIFICATION")
    print("=" * 70)

    # Test 1: Hash Avalanche Effect
    print("\n--- Testing Exercise 1: SHA-256 Avalanche Effect ---")
    str_a = "The quick brown fox jumps over the lazy dog"
    str_b = "The quick brown fox jumps over the lazy dot"  # 1 character changed ('g' -> 't')
    
    pct_flipped = measure_avalanche_effect(str_a, str_b)
    print(f"String A: '{str_a}'")
    print(f"String B: '{str_b}'")
    print(f"SHA-256 Hash A: {compute_sha256(str_a.encode('utf-8'))}")
    print(f"SHA-256 Hash B: {compute_sha256(str_b.encode('utf-8'))}")
    print(f"Percentage of output bits flipped: {pct_flipped:.2f}% (Ideal: ~50.0%)")
    assert 40.0 <= pct_flipped <= 60.0, "Avalanche effect percentage should be around ~50%!"
    print("✅ Exercise 1 Passed!\n")

    # Test 2: Ed25519 Digital Signature Verification
    print("--- Testing Exercise 2: Ed25519 Digital Signatures ---")
    priv_k, pub_k = generate_ed25519_keypair()
    original_doc = b"UNIVERSITY TRANSCRIPT: DEGREE AWARDED WITH HONORS"
    sig = sign_message(priv_k, original_doc)

    is_valid = verify_signature(pub_k, sig, original_doc)
    print(f"Signature Verification over original doc: {is_valid}")
    assert is_valid == True, "Signature verification failed!"

    # Tamper Test
    tampered_doc = b"UNIVERSITY TRANSCRIPT: DEGREE REVOKED"
    is_tampered_valid = verify_signature(pub_k, sig, tampered_doc)
    print(f"Signature Verification over tampered doc: {is_tampered_valid}")
    assert is_tampered_valid == False, "Signature verification MUST fail for tampered document!"
    print("✅ Exercise 2 Passed!\n")

    # Test 3: X.509 Certificate Chain Inspection
    print("--- Testing Exercise 3: X.509 Certificate Validation ---")
    root_c, leaf_c = create_mock_certificate_chain()
    print(f"Root Certificate Subject: {root_c.subject.rfc4514_string()}")
    print(f"Leaf Certificate Subject: {leaf_c.subject.rfc4514_string()}")
    print(f"Leaf Certificate Issuer:  {leaf_c.issuer.rfc4514_string()}")
    
    chain_valid = verify_leaf_against_root(leaf_c, root_c)
    print(f"Leaf Certificate Signature Verified against Root CA? {chain_valid}")
    assert chain_valid == True, "X.509 Certificate chain verification failed!"
    print("✅ Exercise 3 Passed!\n")

    # Test 4: Capstone Mini-CTF Solver
    print("--- Testing Exercise 4: Capstone Mini-CTF Solver ---")
    ctf_flag = "FLAG{m0dern_cryp70_m4st3r_2026}"
    ctf_shift = 7
    ctf_cipher = ""
    for char in ctf_flag:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            ctf_cipher += chr((ord(char) - base + ctf_shift) % 26 + base)
        else:
            ctf_cipher += char

    ctf_priv, ctf_pub = generate_ed25519_keypair()
    ctf_hash = compute_sha256(ctf_flag.encode('utf-8'))
    ctf_sig = sign_message(ctf_priv, ctf_flag.encode('utf-8'))

    print(f"CTF Ciphertext: {ctf_cipher}")
    print(f"Target Hash:    {ctf_hash}")

    solved_flag = solve_ctf_challenge(ctf_cipher, ctf_hash, ctf_pub, ctf_sig)
    print(f"CTF Solved Flag Result: {solved_flag}")
    assert solved_flag == ctf_flag, "CTF Solver failed to recover correct flag!"
    print("✅ Exercise 4 Passed!\n")

    print("=" * 70)
    print(" 🎉 ALL DAY 4 LAB EXERCISES PASSED SUCCESSFULLY!")
    print("=" * 70)
