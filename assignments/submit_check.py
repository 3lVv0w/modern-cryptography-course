#!/usr/bin/env python3
"""
================================================================================
🎓 CS-4XX / ECE-4XX Modern Cryptography & Network Security
CLASS ASSIGNMENT (DAYS 1–3) PRE-FLIGHT VALIDATOR & PACKAGER
================================================================================
Usage:
    python3 assignments/submit_check.py --student-id "65070001" --name "Jane Doe"
================================================================================
"""

import os
import sys
import json
import zipfile
import hashlib
import argparse
from datetime import datetime, timezone

ASSIGNMENTS_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENT_CODE_FILE = os.path.join(ASSIGNMENTS_DIR, "assignment_days_1_to_3_student.py")
REPORT_FILES_TO_CHECK = [
    os.path.join(ASSIGNMENTS_DIR, "REPORT.md"),
    os.path.join(ASSIGNMENTS_DIR, "REPORT_TH.md"),
    os.path.join(ASSIGNMENTS_DIR, "REPORT_TEMPLATE_TH.md"),
    os.path.join(ASSIGNMENTS_DIR, "REPORT_TEMPLATE.md")
]


def find_report_file() -> str:
    """Finds the active student report file (EN or TH)."""
    for path in REPORT_FILES_TO_CHECK:
        if os.path.exists(path):
            return path
    return REPORT_FILES_TO_CHECK[0]


def compute_sha256(filepath: str) -> str:
    """Computes SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def validate_report(report_path: str) -> tuple[bool, str]:
    """Checks whether student report exists and has been populated."""
    if not os.path.exists(report_path):
        return False, f"Report file not found: {report_path}"

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for unedited default placeholders (EN and TH)
    unfilled_count = 0
    placeholders = [
        "[Your Full Name Here]",
        "[Your Student ID Here]",
        "[Your LaTeX or text proof here]",
        "[Your answer here]",
        "[ระบุชื่อ-นามสกุลภาษาไทย หรือ ภาษาอังกฤษ]",
        "[ระบุรหัสนักศึกษา เช่น 65070001]",
        "[เขียนการพิสูจน์ทางคณิตศาสตร์ หรือ LaTeX ที่นี่]",
        "[เขียนคำตอบและคำอธิบายของคุณที่นี่]"
    ]
    for p in placeholders:
        if p in content:
            unfilled_count += 1

    if unfilled_count >= 3:
        return False, f"Report contains {unfilled_count} uncompleted placeholder sections!"

    return True, "Report appears populated."


def run_student_tests() -> tuple[int, int, bool, list[str]]:
    """Runs tests defined in student template and captures results."""
    sys.path.insert(0, ASSIGNMENTS_DIR)
    try:
        import assignment_days_1_to_3_student as student
    except Exception as e:
        return 0, 0, False, [f"Critical import error in student code: {e}"]

    test_logs = []
    code_score = 0
    passed_count = 0
    bonus_passed = False

    # Task 2.1: Caesar Cipher Encrypt & Decrypt (8 pts)
    try:
        t_plain = "HELLO WORLD! Secret #42: Attack at XYZ."
        c3 = student.caesar_encrypt(t_plain, 3)
        d3 = student.caesar_decrypt(c3, 3)
        assert c3 == "KHOOR ZRUOG! Vhfuhw #42: Dwwdfn dw ABC." and d3 == t_plain
        assert student.caesar_encrypt("XYZxyz", 3) == "ABCabc"
        assert student.caesar_decrypt("ABCabc", 3) == "XYZxyz"
        test_logs.append("Task 2.1: Caesar Cipher Encrypt & Decrypt ........... [ PASS ] (+8 pts)")
        code_score += 8
        passed_count += 1
    except Exception as e:
        test_logs.append(f"Task 2.1: Caesar Cipher Encrypt & Decrypt ........... [ FAIL ] ({e})")

    # Task 2.2: Statistical Cryptanalysis (8 pts)
    try:
        sample_plain = "CRYPTOGRAPHY IS THE FOUNDATION OF MODERN DIGITAL SECURITY AND TRUST"
        cipher = student.caesar_encrypt(sample_plain, 7)
        best_k, cracked_plain = student.auto_break_caesar(cipher)
        ic_val = student.compute_index_of_coincidence(sample_plain)
        assert best_k == 7 and cracked_plain == sample_plain and ic_val > 0.050
        test_logs.append("Task 2.2: Statistical Cryptanalysis ................ [ PASS ] (+8 pts)")
        code_score += 8
        passed_count += 1
    except Exception as e:
        test_logs.append(f"Task 2.2: Statistical Cryptanalysis ................ [ FAIL ] ({e})")

    # Task 2.3: Number Theory Primitives (8 pts)
    try:
        g, x, y = student.extended_gcd(240, 46)
        inv = student.modinv(17, 3120)
        p_val = student.pow_mod(7, 256, 1000)
        assert g == 2 and 240 * x + 46 * y == 2 and (17 * inv) % 3120 == 1 and p_val == pow(7, 256, 1000)
        test_logs.append("Task 2.3: Number Theory Primitives ................. [ PASS ] (+8 pts)")
        code_score += 8
        passed_count += 1
    except Exception as e:
        test_logs.append(f"Task 2.3: Number Theory Primitives ................. [ FAIL ] ({e})")

    # Task 2.4: Modern Symmetric AEAD (AES-GCM) (8 pts)
    try:
        key = b"\x01" * 32
        nonce, ciphertext = student.encrypt_aes_gcm("TEST MSG", key, b"AAD")
        dec = student.decrypt_aes_gcm(nonce, ciphertext, key, b"AAD")
        assert dec == "TEST MSG"
        tamper_ok = False
        try:
            student.decrypt_aes_gcm(nonce, ciphertext, key, b"BAD")
        except Exception:
            tamper_ok = True
        assert tamper_ok
        test_logs.append("Task 2.4: Modern Symmetric AEAD (AES-GCM) .......... [ PASS ] (+8 pts)")
        code_score += 8
        passed_count += 1
    except Exception as e:
        test_logs.append(f"Task 2.4: Modern Symmetric AEAD (AES-GCM) .......... [ FAIL ] ({e})")

    # Task 2.5: RSA Engine & Curve25519 (8 pts)
    try:
        pub_k, priv_k = student.rsa_keygen(1009, 1013, e=65537)
        c = student.rsa_encrypt(12345, pub_k)
        m = student.rsa_decrypt(c, priv_k)
        assert m == 12345
        a_s, b_s = student.ecdh_x25519_key_exchange()
        assert a_s == b_s and len(a_s) == 32
        test_logs.append("Task 2.5: RSA Engine & Curve25519 .................. [ PASS ] (+8 pts)")
        code_score += 8
        passed_count += 1
    except Exception as e:
        test_logs.append(f"Task 2.5: RSA Engine & Curve25519 .................. [ FAIL ] ({e})")

    # Attack 3.1: Two-Time Pad Crib Drag (10 pts)
    try:
        p1 = "OPERATION OVERLORD LAUNCH"
        p2 = "DEFEND NORMANDY BEACHHEAD"
        pad = b"\xaa" * len(p1)
        c1 = bytes([ord(a) ^ b for a, b in zip(p1, pad)])
        c2 = bytes([ord(a) ^ b for a, b in zip(p2, pad)])
        res = student.two_time_pad_crib_drag(c1, c2, "OPERATION")
        assert "DEFEND " in res[0][1]
        test_logs.append("Attack 3.1: Two-Time Pad Crib Drag ................. [ PASS ] (+10 pts)")
        code_score += 10
        passed_count += 1
    except Exception as e:
        test_logs.append(f"Attack 3.1: Two-Time Pad Crib Drag ................. [ FAIL ] ({e})")

    # Attack 3.2: AES-GCM Nonce Reuse (10 pts)
    try:
        c1 = b"\x10\x20\x30"
        c2 = b"\x05\x05\x05"
        xor_res = student.exploit_gcm_nonce_reuse(c1, c2)
        assert xor_res == bytes([0x10 ^ 0x05, 0x20 ^ 0x05, 0x30 ^ 0x05])
        test_logs.append("Attack 3.2: AES-GCM Nonce Reuse .................... [ PASS ] (+10 pts)")
        code_score += 10
        passed_count += 1
    except Exception as e:
        test_logs.append(f"Attack 3.2: AES-GCM Nonce Reuse .................... [ FAIL ] ({e})")

    # Attack 3.3: Fermat RSA Factorization (10 pts)
    try:
        p, q = student.fermat_factor(65539 * 65543)
        assert {p, q} == {65539, 65543}
        test_logs.append("Attack 3.3: Fermat RSA Factorization ............... [ PASS ] (+10 pts)")
        code_score += 10
        passed_count += 1
    except Exception as e:
        test_logs.append(f"Attack 3.3: Fermat RSA Factorization ............... [ FAIL ] ({e})")

    # Bonus Task (+15 pts)
    try:
        vig_sample = "THE ONE TIME PAD IS UNCONDITIONALLY SECURE PROVIDED THE KEY IS TRULY RANDOM AND NEVER REUSED AGAIN IN PRODUCTION SYSTEMS"
        sample_key = "CRYPTO"
        v_cipher = student.vigenere_encrypt(vig_sample, sample_key)
        found_key, cracked_plain = student.crack_vigenere_cipher(v_cipher, max_key_len=10)
        assert found_key == sample_key and cracked_plain == vig_sample
        test_logs.append("Bonus Task: Automated Vigenère Breaker ............. [ PASS ] (+15 Extra Credit)")
        bonus_passed = True
    except NotImplementedError:
        test_logs.append("Bonus Task: Automated Vigenère Breaker ............. [ SKIPPED ] (Optional)")
    except Exception as e:
        test_logs.append(f"Bonus Task: Automated Vigenère Breaker ............. [ FAIL ] ({e})")

    return code_score, 15 if bonus_passed else 0, bonus_passed, test_logs


def main():
    parser = argparse.ArgumentParser(description="Cryptographic Class Assignment Validator & Packager")
    parser.add_argument("--student-id", default="", help="Your official University Student ID")
    parser.add_argument("--name", default="", help="Your Full Name")
    parser.add_argument("--no-zip", action="store_true", help="Skip zip packaging, run validation only")
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print(" 🎓 MODERN CRYPTOGRAPHY ASSIGNMENT (DAYS 1-3) PRE-FLIGHT CHECKER")
    print("=" * 70)

    # 1. Validate ID & Name
    student_id = args.student_id.strip()
    student_name = args.name.strip()
    if not student_id or not student_name:
        print("[!] Warning: Student ID or Name omitted.")
        print("    Run with: --student-id \"YOUR_ID\" --name \"YOUR_NAME\"")
        if not student_id:
            student_id = "UNKNOWN_ID"
        if not student_name:
            student_name = "UNKNOWN_STUDENT"
    else:
        print(f"[+] Candidate: {student_name} (ID: {student_id})")

    # 2. Check Code File Existence
    if not os.path.exists(STUDENT_CODE_FILE):
        print(f"[❌] Error: Could not find student code file at {STUDENT_CODE_FILE}")
        sys.exit(1)
    print(f"[+] Student code file found: assignment_days_1_to_3_student.py")

    # 3. Check Report File Existence
    report_file = find_report_file()
    report_ok, report_msg = validate_report(report_file)
    report_basename = os.path.basename(report_file)
    if report_ok:
        print(f"[+] Written report found: {report_basename} ({report_msg})")
    else:
        print(f"[⚠️] Written report warning: {report_basename} -> {report_msg}")

    # 4. Run Automated Test Suite
    print("\n[+] Running Automated Test Suite...")
    code_score, bonus_score, bonus_ok, logs = run_student_tests()
    for log in logs:
        print(f"    -> {log}")

    print(f"\n[+] Automated Code Score: {code_score} / 70 Points")
    if bonus_ok:
        print(f"[+] Bonus Extra Credit  : +{bonus_score} Points")
    print(f"[+] Theory Report Score : __ / 30 Points (Graded by Course Staff)")

    # 5. Calculate Integrity Hashes
    code_hash = compute_sha256(STUDENT_CODE_FILE)
    report_hash = compute_sha256(report_file) if os.path.exists(report_file) else "MISSING"

    print("\n[+] Cryptographic Integrity Hashes (SHA-256):")
    print(f"    • Python Code : {code_hash}")
    print(f"    • Report File : {report_hash}")

    # 6. Generate Metadata Receipt
    timestamp_utc = datetime.now(timezone.utc).isoformat()
    metadata = {
        "assignment": "Class Assignment (Days 1-3)",
        "student_name": student_name,
        "student_id": student_id,
        "timestamp_utc": timestamp_utc,
        "code_score": code_score,
        "bonus_score": bonus_score,
        "code_sha256": code_hash,
        "report_sha256": report_hash,
        "validator_version": "1.0.0"
    }

    metadata_path = os.path.join(ASSIGNMENTS_DIR, "submission_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[+] Metadata receipt saved: submission_metadata.json")

    # 7. Package ZIP bundle
    if not args.no_zip:
        zip_filename = f"submission_{student_id}_days1_to_3.zip"
        zip_filepath = os.path.join(ASSIGNMENTS_DIR, zip_filename)

        with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(STUDENT_CODE_FILE, arcname="assignment_days_1_to_3_student.py")
            if os.path.exists(report_file):
                zipf.write(report_file, arcname=os.path.basename(report_file))
            zipf.write(metadata_path, arcname="submission_metadata.json")

        zip_hash = compute_sha256(zip_filepath)
        print(f"\n[+] Submission archive packaged successfully:")
        print(f"    📁 Archive File : assignments/{zip_filename}")
        print(f"    🔒 Bundle SHA256: {zip_hash}")

    print("\n" + "=" * 70)
    print(" 🚀 PRE-FLIGHT EVALUATION COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
