"""
Day 1 Hands-On Code Exercises: Classical Cryptanalysis & Information Theory
Course: Modern Cryptography & Network Security (University Undergraduate Level)

Student Name: ___________________________
Date: ___________________________________

Instructions:
Complete the TODO blocks in Exercise 1 through Exercise 4.
Run this script using `python3 day1_exercises.py` to test your solutions!
"""

import math
import secrets
import string
from collections import Counter

# Standard English Letter Frequencies (in percentage)
ENGLISH_FREQUENCIES = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.98, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.01, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

# ==============================================================================
# EXERCISE 1: Caesar Cipher & Chi-Squared Cryptanalysis
# ==============================================================================

def caesar_encrypt(plaintext: str, shift: int) -> str:
    """Encrypts plaintext using a Caesar shift cipher."""
    result = []
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return "".join(result)


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Decrypts ciphertext using a Caesar shift key."""
    # TODO: Implement decrypt by calling caesar_encrypt with negative shift or shift formula
    return caesar_encrypt(ciphertext, -shift)


def calculate_chi_squared(text: str) -> float:
    """
    Calculates the Chi-Squared statistic of the text compared to standard English letter frequencies.
    Formula: Chi^2 = Sum( (Observed_i - Expected_i)^2 / Expected_i )
    Lower score = Closer to standard English text.
    """
    clean_text = [c.upper() for c in text if c.isalpha()]
    N = len(clean_text)
    if N == 0:
        return float('inf')

    counts = Counter(clean_text)
    chi_sq = 0.0

    for letter, expected_pct in ENGLISH_FREQUENCIES.items():
        expected_count = N * (expected_pct / 100.0)
        observed_count = counts.get(letter, 0)
        chi_sq += ((observed_count - expected_count) ** 2) / (expected_count + 1e-6)

    return chi_sq


def crack_caesar(ciphertext: str) -> tuple[int, str]:
    """
    Automated Caesar Cipher Breaker.
    Iterates all 26 possible shift keys, scores each candidate plaintext using Chi-Squared,
    and returns (best_shift_key, best_decrypted_plaintext).
    """
    best_key = 0
    best_chi_sq = float('inf')
    best_plaintext = ""

    for shift in range(26):
        candidate_text = caesar_decrypt(ciphertext, shift)
        score = calculate_chi_squared(candidate_text)
        
        if score < best_chi_sq:
            best_chi_sq = score
            best_key = shift
            best_plaintext = candidate_text

    return best_key, best_plaintext


# ==============================================================================
# EXERCISE 2: Index of Coincidence (IC)
# ==============================================================================

def calculate_index_of_coincidence(text: str) -> float:
    """
    Calculates the Index of Coincidence (IC) of a given text string.
    Formula: IC = Sum( f_i * (f_i - 1) ) / ( N * (N - 1) )
    where f_i is the frequency count of letter i, and N is total letter count.
    
    Expected Values:
    - Random Uniform Text over 26 letters: ~0.0385
    - Monolingual English Text:            ~0.0667
    """
    clean_text = [c.upper() for c in text if c.isalpha()]
    N = len(clean_text)
    if N <= 1:
        return 0.0

    counts = Counter(clean_text)
    numerator = sum(f * (f - 1) for f in counts.values())
    denominator = N * (N - 1)
    
    return numerator / denominator


# ==============================================================================
# EXERCISE 3: One-Time Pad (OTP) Implementation
# ==============================================================================

def otp_generate_key(length: int) -> bytes:
    """Generates a cryptographically secure random key of specified byte length."""
    return secrets.token_bytes(length)


def otp_encrypt(plaintext: str, key: bytes) -> bytes:
    """Encrypts plaintext string using One-Time Pad XOR with key bytes."""
    p_bytes = plaintext.encode('utf-8')
    if len(p_bytes) > len(key):
        raise ValueError("Key length must be greater than or equal to plaintext length!")
    return bytes([p ^ k for p, k in zip(p_bytes, key)])


def otp_decrypt(ciphertext: bytes, key: bytes) -> str:
    """Decrypts OTP ciphertext bytes using key bytes."""
    decrypted_bytes = bytes([c ^ k for c, k in zip(ciphertext, key)])
    return decrypted_bytes.decode('utf-8', errors='replace')


# ==============================================================================
# EXERCISE 4: Two-Time Pad (Crib Dragging Attack)
# ==============================================================================

def crib_drag(c1_bytes: bytes, c2_bytes: bytes, crib: str) -> list[tuple[int, str]]:
    """
    Performs a Crib Dragging Attack when two messages C1 and C2 are encrypted with the same OTP key.
    Since C1 XOR C2 = M1 XOR M2, sliding a guessed word ('crib') across C1 XOR C2
    reveals candidate plaintext characters of the other message!
    
    Returns a list of (position_index, candidate_revealed_string).
    """
    c_xor = bytes([b1 ^ b2 for b1, b2 in zip(c1_bytes, c2_bytes)])
    crib_bytes = crib.encode('utf-8')
    crib_len = len(crib_bytes)
    results = []

    for i in range(len(c_xor) - crib_len + 1):
        # XOR crib slice against c_xor window
        window = c_xor[i : i + crib_len]
        revealed_bytes = bytes([w ^ c for w, c in zip(window, crib_bytes)])
        
        # Check if revealed bytes contain printable ASCII characters
        revealed_str = repr(revealed_bytes.decode('ascii', errors='ignore'))
        results.append((i, revealed_str))

    return results


# ==============================================================================
# AUTOMATED TEST SUITE & VERIFICATION
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" 🚀 RUNNING DAY 1 CRYPTOGRAPHY LAB EXERCISES & VERIFICATION")
    print("=" * 70)

    # Test 1: Caesar Cipher Encryption & Automated Decryption
    print("\n--- Testing Exercise 1: Caesar Cipher & Chi-Squared ---")
    secret_text = "SHANNON PERFECT SECRECY IS THE FOUNDATION OF MODERN CRYPTOGRAPHY"
    shift_key = 14
    cipher = caesar_encrypt(secret_text, shift_key)
    print(f"Original Text:  {secret_text}")
    print(f"Shift Key:      {shift_key}")
    print(f"Ciphertext:     {cipher}")

    found_key, recovered_text = crack_caesar(cipher)
    print(f"Discovered Key: {found_key}")
    print(f"Recovered Text: {recovered_text}")
    assert found_key == shift_key, f"Expected key {shift_key}, but got {found_key}"
    assert recovered_text == secret_text, "Decrypted text mismatch!"
    print("✅ Exercise 1 Passed!\n")

    # Test 2: Index of Coincidence
    print("--- Testing Exercise 2: Index of Coincidence (IC) ---")
    sample_english = "Cryptography is the practice and study of techniques for secure communication in the presence of adversarial third parties."
    sample_random = "".join(secrets.choice(string.ascii_uppercase) for _ in range(500))
    
    ic_english = calculate_index_of_coincidence(sample_english)
    ic_random = calculate_index_of_coincidence(sample_random)

    print(f"English Sample IC: {ic_english:.4f} (Expected: ~0.0667)")
    print(f"Random Sample IC:  {ic_random:.4f} (Expected: ~0.0385)")
    assert ic_english > 0.055, "English IC should be significantly higher than random!"
    assert ic_random < 0.048, "Random IC should be near 0.0385!"
    print("✅ Exercise 2 Passed!\n")

    # Test 3: OTP Encryption & Decryption
    print("--- Testing Exercise 3: One-Time Pad (OTP) ---")
    otp_msg = "TOP SECRET MILITARY PAYLOAD"
    otp_key = otp_generate_key(len(otp_msg.encode('utf-8')))
    otp_cipher = otp_encrypt(otp_msg, otp_key)
    otp_recovered = otp_decrypt(otp_cipher, otp_key)

    print(f"OTP Plaintext:  {otp_msg}")
    print(f"OTP Key (hex):   {otp_key.hex()}")
    print(f"OTP Ciphertext: {otp_cipher.hex()}")
    print(f"OTP Recovered:  {otp_recovered}")
    assert otp_recovered == otp_msg, "OTP Decryption Failed!"
    print("✅ Exercise 3 Passed!\n")

    # Test 4: Two-Time Pad Crib Drag Attack
    print("--- Testing Exercise 4: Two-Time Pad (Crib Drag) ---")
    m1 = "ATTACK AT DAWN TODAY"
    m2 = "DEFEND AT DUSK TODAY"
    shared_key = otp_generate_key(len(m1))
    
    c1 = otp_encrypt(m1, shared_key)
    c2 = otp_encrypt(m2, shared_key)
    
    crib_results = crib_drag(c1, c2, "ATTACK")
    print(f"Message 1: {m1}")
    print(f"Message 2: {m2}")
    print("Crib Drag Results for crib 'ATTACK':")
    for pos, revealed in crib_results[:3]:
        print(f"  Pos {pos}: Revealed plaintext candidate -> {revealed}")
    
    # At index 0, dragging 'ATTACK' against C1^C2 reveals 'DEFEND'!
    pos_0_revealed = crib_results[0][1]
    assert "DEFEND" in pos_0_revealed, "Crib dragging should reveal 'DEFEND' at position 0!"
    print("✅ Exercise 4 Passed!\n")

    print("=" * 70)
    print(" 🎉 ALL DAY 1 LAB EXERCISES PASSED SUCCESSFULLY!")
    print("=" * 70)
