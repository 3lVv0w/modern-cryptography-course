"""
================================================================================
🎓 DAY 1 STUDENT LAB NOTEBOOK: 3-TIER CHALLENGES
Course: Modern Cryptography & Network Security (CS-4XX)
Duration: 3 Hours (Afternoon Hands-On Lab)
================================================================================

CHALLENGE DIFFICULTY TIERS:
🟢 LEVEL 1: Novice / Fundamentals (Caesar Shift & Frequency Counting)
🟡 LEVEL 2: Intermediate / Applied (Chi-Squared Automated Breaker & IC Analysis)
🔴 LEVEL 3: Advanced / Hardcore Cryptanalyst (Full Vigenère Breaker & Two-Time Pad Crib Dragging)

STUDENT NAME: ____________________________
STUDENT ID:   ____________________________
================================================================================
"""

import math
import secrets
from collections import Counter

# Standard English Letter Frequencies (%)
ENGLISH_FREQUENCIES = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.98, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.01, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

# ==============================================================================
# 🟢 LEVEL 1: NOVICE CHALLENGES (Fundamentals & Basic Ciphers)
# ==============================================================================

def caesar_encrypt(plaintext: str, shift: int) -> str:
    """
    [LEVEL 1] Encrypt plaintext string using Caesar Shift Cipher.
    Formula: C_i = (P_i + shift) mod 26
    """
    result = []
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return "".join(result)


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """
    [LEVEL 1] Decrypt ciphertext string using Caesar Shift key.
    """
    return caesar_encrypt(ciphertext, -shift)


# ==============================================================================
# 🟡 LEVEL 2: INTERMEDIATE CHALLENGES (Statistical Cryptanalysis & IC)
# ==============================================================================

def compute_chi_squared(text: str) -> float:
    """
    [LEVEL 2] Calculate the Chi-Squared statistic of text compared to standard English.
    Formula: Chi^2 = Sum( (Observed_i - Expected_i)^2 / Expected_i )
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


def auto_break_caesar(ciphertext: str) -> tuple[int, str]:
    """
    [LEVEL 2] Automated Caesar Breaker using Chi-Squared minimum score.
    Returns (best_shift_key, best_decrypted_plaintext).
    """
    best_key = 0
    best_score = float('inf')
    best_plaintext = ""

    for k in range(26):
        candidate = caesar_decrypt(ciphertext, k)
        score = compute_chi_squared(candidate)
        if score < best_score:
            best_score = score
            best_key = k
            best_plaintext = candidate

    return best_key, best_plaintext


def compute_index_of_coincidence(text: str) -> float:
    """
    [LEVEL 2] Calculate Index of Coincidence (IC).
    Formula: IC = Sum( f_i * (f_i - 1) ) / ( N * (N - 1) )
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
# 🔴 LEVEL 3: ADVANCED / HARDCORE CHALLENGES (Vigenère Breaker & Two-Time Pad)
# ==============================================================================

def vigenere_encrypt(plaintext: str, keyword: str) -> str:
    """[LEVEL 3] Encrypt plaintext using Vigenère Cipher."""
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
    """[LEVEL 3] Decrypt ciphertext using Vigenère Cipher."""
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
    [LEVEL 3 HARDCORE] Full Automated Vigenère Cipher Breaker.
    1. Estimate key length 'm' using Index of Coincidence across columns.
    2. Decompose ciphertext into 'm' Caesar columns.
    3. Run Chi-Squared Caesar breaker on each column to recover keyword characters.
    4. Decrypt full plaintext.
    Returns (discovered_keyword, decrypted_plaintext).
    """
    clean_text = [c.upper() for c in ciphertext if c.isalpha()]
    
    # Step 1: Estimate key length m
    best_m = 1
    closest_diff = float('inf')
    for m in range(1, max_key_len + 1):
        column_ics = []
        for col_idx in range(m):
            col_text = "".join(clean_text[i] for i in range(col_idx, len(clean_text), m))
            if len(col_text) > 1:
                column_ics.append(compute_index_of_coincidence(col_text))
        if column_ics:
            avg_ic = sum(column_ics) / len(column_ics)
            if abs(avg_ic - 0.0667) < closest_diff:
                closest_diff = abs(avg_ic - 0.0667)
                best_m = m

    # Step 2: Recover keyword letter for each column
    discovered_key = []
    for col_idx in range(best_m):
        col_text = "".join(clean_text[i] for i in range(col_idx, len(clean_text), best_m))
        best_col_shift, _ = auto_break_caesar(col_text)
        discovered_key.append(chr(best_col_shift + ord('A')))
        
    recovered_keyword = "".join(discovered_key)
    decrypted_plain = vigenere_decrypt(ciphertext, recovered_keyword)
    return recovered_keyword, decrypted_plain


def otp_encrypt(plaintext: str, key: bytes) -> bytes:
    p_bytes = plaintext.encode('utf-8')
    return bytes([p ^ k for p, k in zip(p_bytes, key)])


def two_time_pad_crib_drag(c1_bytes: bytes, c2_bytes: bytes, crib: str) -> list[tuple[int, str]]:
    """
    [LEVEL 3 HARDCORE] Two-Time Pad (Crib Dragging Attack).
    Sliding crib_str across C1 ^ C2 reveals candidate plaintexts.
    """
    c_xor = bytes([b1 ^ b2 for b1, b2 in zip(c1_bytes, c2_bytes)])
    crib_bytes = crib.encode('utf-8')
    crib_len = len(crib_bytes)
    results = []

    for i in range(len(c_xor) - crib_len + 1):
        window = c_xor[i : i + crib_len]
        revealed_bytes = bytes([w ^ c for w, c in zip(window, crib_bytes)])
        results.append((i, revealed_bytes.decode('ascii', errors='ignore')))

    return results


# ==============================================================================
# AUTOMATED GRADED LAB TEST SUITE
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 75)
    print(" 🧪 DAY 1 LAB EVALUATION: 3-TIER DIFFICULTY CHALLENGES")
    print("=" * 75)

    passed_count = 0
    total_tests = 5

    # 🟢 LEVEL 1 TEST
    print("\n🟢 [LEVEL 1 - NOVICE] Caesar Cipher Encryption & Decryption...")
    try:
        sample_p = "ATTACK AT NOON"
        sample_c = caesar_encrypt(sample_p, 5)
        assert sample_c == "FYYFHP FY STTS", f"Incorrect: {sample_c}"
        assert caesar_decrypt(sample_c, 5) == sample_p, "Decryption failed!"
        print("  --> ✅ PASS: Level 1 Novice Challenge Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 1 failed ({e})")

    # 🟡 LEVEL 2 TEST A
    print("\n🟡 [LEVEL 2 - INTERMEDIATE] Automated Caesar Breaker (Chi-Squared)...")
    try:
        target_p = "SECURITY IS NOT A PRODUCT BUT A PROCESS"
        target_c = caesar_encrypt(target_p, 19)
        cracked_k, cracked_p = auto_break_caesar(target_c)
        assert cracked_k == 19 and cracked_p == target_p, "Caesar breaker failed!"
        print("  --> ✅ PASS: Level 2 Automated Cryptanalysis Passed!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 2 Caesar breaker failed ({e})")

    # 🟡 LEVEL 2 TEST B
    print("\n🟡 [LEVEL 2 - INTERMEDIATE] Index of Coincidence (IC) Calculation...")
    try:
        eng_text = "THE ONE TIME PAD IS UNCONDITIONALLY SECURE PROVIDED THE KEY IS TRULY RANDOM AND NEVER REUSED AGAIN IN PRODUCTION SYSTEMS"
        ic_v = compute_index_of_coincidence(eng_text)
        assert ic_v > 0.055, f"IC metric failed ({ic_v})!"
        print(f"  --> ✅ PASS: Level 2 IC Calculation Passed (IC = {ic_v:.4f})!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 2 IC calculation failed ({e})")

    # 🔴 LEVEL 3 TEST A
    print("\n🔴 [LEVEL 3 - HARDCORE] Full Automated Vigenère Cipher Breaker...")
    try:
        vig_text = "THE ONE TIME PAD IS UNCONDITIONALLY SECURE PROVIDED THE KEY IS TRULY RANDOM AND NEVER REUSED AGAIN IN PRODUCTION SYSTEMS"
        vig_key = "CRYPTO"
        vig_c = vigenere_encrypt(vig_text, vig_key)
        
        found_kw, recovered_p = crack_vigenere_cipher(vig_c, max_key_len=10)
        assert found_kw == vig_key, f"Expected key {vig_key}, got {found_kw}"
        assert recovered_p == vig_text, "Vigenere plaintext mismatch!"
        print(f"  --> ✅ PASS: Level 3 Hardcore Vigenère Breaker Passed (Key='{found_kw}')!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 3 Vigenere breaker failed ({e})")

    # 🔴 LEVEL 3 TEST B
    print("\n🔴 [LEVEL 3 - HARDCORE] Two-Time Pad (Crib Dragging Attack)...")
    try:
        m1 = "PROJECT MANHATTAN READY"
        m2 = "LAUNCH MISSION TONIGHT"
        shared_k = secrets.token_bytes(len(m1))
        c1 = otp_encrypt(m1, shared_k)
        c2 = otp_encrypt(m2, shared_k)
        
        drag_res = two_time_pad_crib_drag(c1, c2, "PROJECT")
        assert "LAUNCH " in drag_res[0][1], "Crib drag failed!"
        print(f"  --> ✅ PASS: Level 3 Two-Time Pad Attack Passed (Exposed: '{drag_res[0][1]}')!")
        passed_count += 1
    except Exception as e:
        print(f"  --> ❌ FAIL: Level 3 Two-Time Pad failed ({e})")

    # Final Grade Summary
    print("\n" + "=" * 75)
    print(f" 🏆 DAY 1 LAB SCORE: {passed_count} / {total_tests} Tests Passed ({(passed_count/total_tests)*100:.0f}%)")
    print("=" * 75 + "\n")
