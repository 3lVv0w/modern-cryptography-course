"""
================================================================================
🎓 DAY 4 STUDENT LAB NOTEBOOK: 3-TIER CHALLENGES
Course: Modern Cryptography & Network Security (CS-4XX)
Duration: 3 Hours (Afternoon Hands-On Lab & Capstone CTF)
================================================================================

CHALLENGE DIFFICULTY TIERS:
🟢 LEVEL 1: Novice / Fundamentals (SHA-256 Avalanche Effect & Ed25519 Signatures)
🟡 LEVEL 2: Intermediate / Applied (Tamper Rejection & X.509 Certificate Chain Inspection)
🔴 LEVEL 3: Advanced / Hardcore Cryptanalyst (Capstone CTF "Operation Broken Envelope" Solver)

STUDENT NAME: ____________________________
STUDENT ID:   ____________________________
================================================================================
"""

import datetime
import hashlib
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.x509.oid import NameOID

# ==============================================================================
# 🟢 LEVEL 1: NOVICE CHALLENGES (SHA-256 & Ed25519 Signatures)
# ==============================================================================

def compute_sha256(data: bytes) -> str:
    """[LEVEL 1] Compute SHA-256 hex digest of input bytes."""
    return hashlib.sha256(data).hexdigest()


def measure_avalanche_effect(text1: str, text2: str) -> float:
    """
    [LEVEL 1] Measure percentage of output bits flipped between SHA256(text1) and SHA256(text2).
    Returns bit-flip percentage (Expected ~50%).
    """
    h1_hex = compute_sha256(text1.encode('utf-8'))
    h2_hex = compute_sha256(text2.encode('utf-8'))
    
    b1 = bin(int(h1_hex, 16))[2:].zfill(256)
    b2 = bin(int(h2_hex, 16))[2:].zfill(256)
    
    flipped = sum(bit1 != bit2 for bit1, bit2 in zip(b1, b2))
    return (flipped / 256.0) * 100.0


def generate_ed25519_keypair():
    """[LEVEL 1] Generate Ed25519 private and public keypair."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key


def sign_message(private_key: ed25519.Ed25519PrivateKey, message: bytes) -> bytes:
    """[LEVEL 1] Sign message bytes using Ed25519 private key."""
    return private_key.sign(message)


def verify_signature(public_key: ed25519.Ed25519PublicKey, signature: bytes, message: bytes) -> bool:
    """[LEVEL 1] Verify Ed25519 signature over message bytes."""
    try:
        public_key.verify(signature, message)
        return True
    except Exception:
        return False


# ==============================================================================
# 🟡 LEVEL 2: INTERMEDIATE CHALLENGES (X.509 PKI Certificate Inspection)
# ==============================================================================

def create_mock_certificate_chain():
    """[LEVEL 2] Generate mock Root CA certificate and Leaf domain certificate."""
    root_priv = ed25519.Ed25519PrivateKey.generate()
    root_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "University Root CA")])
    
    root_cert = x509.CertificateBuilder().subject_name(
        root_name
    ).issuer_name(
        root_name
    ).public_key(
        root_priv.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    ).sign(root_priv, algorithm=None)

    leaf_priv = ed25519.Ed25519PrivateKey.generate()
    leaf_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "secure-university.edu")])
    
    leaf_cert = x509.CertificateBuilder().subject_name(
        leaf_name
    ).issuer_name(
        root_name
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
    """[LEVEL 2] Verify leaf_cert signature against root_cert's public key."""
    try:
        root_pubkey = root_cert.public_key()
        root_pubkey.verify(leaf_cert.signature, leaf_cert.tbs_certificate_bytes)
        return True
    except Exception:
        return False


# ==============================================================================
# 🔴 LEVEL 3: ADVANCED / HARDCORE CHALLENGES (Capstone CTF Solver)
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
    [LEVEL 3 HARDCORE] Capstone CTF Solver ("Operation Broken Envelope").
    1. Brute-forces Caesar shifts [0..25].
    2. Filters candidates whose SHA-256 hash matches target_sha256.
    3. Verifies Ed25519 digital signature using sender_pubkey.
    4. Returns verified flag!
    """
    for shift in range(26):
        candidate = decrypt_caesar(ciphertext, shift)
        cand_bytes = candidate.encode('utf-8')
        
        if compute_sha256(cand_bytes) == target_sha256:
            if verify_signature(sender_pubkey, signature, cand_bytes):
                return candidate
                
    raise ValueError("CTF Solver failed to find valid payload!")


# ==============================================================================
# AUTOMATED GRADED LAB TEST SUITE
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 75)
    print(" 🧪 DAY 4 LAB EVALUATION: 3-TIER DIFFICULTY CHALLENGES")
    print("=" * 75)

    passed_count = 0
    total_tests = 5

    # 🟢 LEVEL 1 TEST A
    print("\n🟢 [LEVEL 1 - NOVICE] SHA-256 Avalanche Effect Measurement...")
    try:
        s1 = "The quick brown fox jumps over the lazy dog"
        s2 = "The quick brown fox jumps over the lazy dot"
        pct = measure_avalanche_effect(s1, s2)
        assert 40.0 <= pct <= 60.0, f"Avalanche metric failed: {pct:.2f}%"
        print(f"  --> ✅ PASS: Level 1 SHA-256 Avalanche Effect Passed ({pct:.2f}% bit flip)!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 1 failed ({e})")

    # 🟢 LEVEL 1 TEST B
    print("\n🟢 [LEVEL 1 - NOVICE] Ed25519 Digital Signature Generation & Verification...")
    try:
        priv_k, pub_k = generate_ed25519_keypair()
        doc = b"OFFICIAL DEGREE CERTIFICATE: HONORS"
        sig = sign_message(priv_k, doc)
        assert verify_signature(pub_k, sig, doc) == True, "Signature verification failed!"
        print("  --> ✅ PASS: Level 1 Ed25519 Signature Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 1 signature failed ({e})")

    # 🟡 LEVEL 2 TEST A
    print("\n🟡 [LEVEL 2 - INTERMEDIATE] Ed25519 Tamper Rejection Check...")
    try:
        priv_k, pub_k = generate_ed25519_keypair()
        doc = b"OFFICIAL DEGREE CERTIFICATE: HONORS"
        tampered = b"OFFICIAL DEGREE CERTIFICATE: REVOKED"
        sig = sign_message(priv_k, doc)
        assert verify_signature(pub_k, sig, tampered) == False, "Tamper check failed!"
        print("  --> ✅ PASS: Level 2 Signature Tamper Rejection Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 2 tamper check failed ({e})")

    # 🟡 LEVEL 2 TEST B
    print("\n🟡 [LEVEL 2 - INTERMEDIATE] X.509 Certificate Chain Inspection...")
    try:
        root_c, leaf_c = create_mock_certificate_chain()
        assert verify_leaf_against_root(leaf_c, root_c) == True, "Cert verification failed!"
        print("  --> ✅ PASS: Level 2 X.509 Certificate Validation Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 2 Cert validation failed ({e})")

    # 🔴 LEVEL 3 TEST
    print("\n🔴 [LEVEL 3 - HARDCORE] Capstone Mini-CTF Solver ('Operation Broken Envelope')...")
    try:
        flag = "FLAG{m0dern_cryp70_m4st3r_2026}"
        shift = 7
        cipher = ""
        for char in flag:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                cipher += chr((ord(char) - base + shift) % 26 + base)
            else:
                cipher += char

        priv_k, pub_k = generate_ed25519_keypair()
        target_hash = compute_sha256(flag.encode('utf-8'))
        sig = sign_message(priv_k, flag.encode('utf-8'))

        solved = solve_ctf_challenge(cipher, target_hash, pub_k, sig)
        assert solved == flag, "CTF solver failed!"
        print(f"  --> ✅ PASS: Level 3 Capstone CTF Solver Passed (Flag = '{solved}')!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 3 CTF solver failed ({e})")

    # Final Grade Summary
    print("\n" + "=" * 75)
    print(f" 🏆 DAY 4 LAB SCORE: {passed_count} / {total_tests} Tests Passed ({(passed_count/total_tests)*100:.0f}%)")
    print("=" * 75 + "\n")
