#!/usr/bin/env python3
"""
================================================================================
🎓 CS-1XX / ECE-1XX Modern Cryptography for Beginners
BEGINNER CLASS ASSIGNMENT PRE-FLIGHT VALIDATOR & PACKAGER
(ระบบตรวจสอบความถูกต้องและรวมไฟล์ส่ง สำหรับใบงานระดับผู้เริ่มต้น)
================================================================================
Usage:
    python3 assignments/submit_check_beginner.py --student-id "65070001" --name "Jane Doe"
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
STUDENT_CODE_FILE = os.path.join(ASSIGNMENTS_DIR, "assignment_beginner_student.py")
REPORT_FILES_TO_CHECK = [
    os.path.join(ASSIGNMENTS_DIR, "REPORT_BEGINNER.md"),
    os.path.join(ASSIGNMENTS_DIR, "REPORT_BEGINNER_TH.md"),
    os.path.join(ASSIGNMENTS_DIR, "REPORT_TEMPLATE_BEGINNER_TH.md"),
    os.path.join(ASSIGNMENTS_DIR, "REPORT_TEMPLATE_BEGINNER.md")
]


def find_report_file() -> str:
    """Finds the active beginner student report file (EN or TH)."""
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
        return False, f"Report file not found: {os.path.basename(report_path)}"

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for unedited default placeholders (EN and TH)
    unfilled_count = 0
    placeholders = [
        "[Your Full Name Here]",
        "[Your Student ID Here]",
        "[Your answer here]",
        "[Your explanation here]",
        "[ระบุชื่อ-นามสกุล]",
        "[ระบุรหัสนักศึกษา]",
        "[เขียนคำตอบและคำอธิบายของคุณที่นี่]",
        "[อธิบายคำตอบของคุณที่นี่]"
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
        import assignment_beginner_student as student
    except Exception as e:
        return 0, 0, False, [f"Critical import error in student code: {e}"]

    test_logs = []
    code_score = 0
    passed_count = 0
    bonus_passed = False

    # Task 2.1: Caesar Cipher (10 pts)
    try:
        sample = "Hello, World! 2026"
        c3 = student.caesar_encrypt(sample, 3)
        p3 = student.caesar_decrypt(c3, 3)
        assert c3 == "Khoor, Zruog! 2026" and p3 == sample
        assert student.caesar_encrypt("XYZxyz", 3) == "ABCabc"
        assert student.caesar_decrypt("ABCabc", 3) == "XYZxyz"
        test_logs.append("Task 2.1: Caesar Cipher Encrypt & Decrypt ........... [ PASS ] (+10 pts)")
        code_score += 10
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Task 2.1: Caesar Cipher Encrypt & Decrypt ........... [ TODO ]")
    except Exception as e:
        test_logs.append(f"Task 2.1: Caesar Cipher Encrypt & Decrypt ........... [ FAIL ] ({e})")

    # Task 2.2: XOR Bitwise Cipher (10 pts)
    try:
        msg = b"Beginner Secret Data"
        key = b"KEY123"
        c_bytes = student.xor_cipher(msg, key)
        assert c_bytes != msg and len(c_bytes) == len(msg)
        assert student.xor_cipher(c_bytes, key) == msg
        test_logs.append("Task 2.2: XOR Bitwise Cipher ........................ [ PASS ] (+10 pts)")
        code_score += 10
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Task 2.2: XOR Bitwise Cipher ........................ [ TODO ]")
    except Exception as e:
        test_logs.append(f"Task 2.2: XOR Bitwise Cipher ........................ [ FAIL ] ({e})")

    # Task 2.3: Euclidean GCD (10 pts)
    try:
        assert student.euclidean_gcd(48, 18) == 6
        assert student.euclidean_gcd(101, 103) == 1
        assert student.euclidean_gcd(252, 105) == 21
        test_logs.append("Task 2.3: Euclidean GCD Algorithm ................... [ PASS ] (+10 pts)")
        code_score += 10
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Task 2.3: Euclidean GCD Algorithm ................... [ TODO ]")
    except Exception as e:
        test_logs.append(f"Task 2.3: Euclidean GCD Algorithm ................... [ FAIL ] ({e})")

    # Task 2.4: AES-256-GCM (10 pts)
    try:
        k = b"\x07" * 32
        txt = "Confidential Payload"
        nonce, ct = student.aes_gcm_encrypt(txt, k)
        assert len(nonce) == 12
        dec = student.aes_gcm_decrypt(nonce, ct, k)
        assert dec == txt
        # Tamper check
        tamper_ct = bytearray(ct)
        tamper_ct[0] ^= 0x01
        tamper_caught = False
        try:
            student.aes_gcm_decrypt(nonce, bytes(tamper_ct), k)
        except Exception:
            tamper_caught = True
        assert tamper_caught
        test_logs.append("Task 2.4: AES-256-GCM AEAD Encryption ............... [ PASS ] (+10 pts)")
        code_score += 10
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Task 2.4: AES-256-GCM AEAD Encryption ............... [ TODO ]")
    except Exception as e:
        test_logs.append(f"Task 2.4: AES-256-GCM AEAD Encryption ............... [ FAIL ] ({e})")

    # Task 2.5: Diffie-Hellman Key Exchange (10 pts)
    try:
        p, g = 23, 5
        a_priv, b_priv = 6, 15
        a_pub = student.dh_compute_public_key(g, a_priv, p)
        b_pub = student.dh_compute_public_key(g, b_priv, p)
        assert a_pub == 8 and b_pub == 19
        s_a = student.dh_compute_shared_secret(b_pub, a_priv, p)
        s_b = student.dh_compute_shared_secret(a_pub, b_priv, p)
        assert s_a == s_b == 2
        test_logs.append("Task 2.5: Diffie-Hellman Key Exchange ............... [ PASS ] (+10 pts)")
        code_score += 10
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Task 2.5: Diffie-Hellman Key Exchange ............... [ TODO ]")
    except Exception as e:
        test_logs.append(f"Task 2.5: Diffie-Hellman Key Exchange ............... [ FAIL ] ({e})")

    # Task 2.6: Toy RSA (10 pts)
    try:
        n, e, d = 3233, 17, 2753
        m = 42
        c = student.rsa_encrypt_toy(m, e, n)
        assert c != m
        assert student.rsa_decrypt_toy(c, d, n) == m
        test_logs.append("Task 2.6: Toy RSA Cryptosystem ...................... [ PASS ] (+10 pts)")
        code_score += 10
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Task 2.6: Toy RSA Cryptosystem ...................... [ TODO ]")
    except Exception as e:
        test_logs.append(f"Task 2.6: Toy RSA Cryptosystem ...................... [ FAIL ] ({e})")

    # Mission 3.1: Intercepted Spy Message & SHA-256 (10 pts)
    try:
        secret_spy_cipher = "AOL ZLJYLA HNLUA PZ TLLAPUN HA TPKUPNOA"
        k_found, p_found = student.crack_simple_caesar(secret_spy_cipher, clue_word="AGENT")
        assert k_found == 7 and p_found == "THE SECRET AGENT IS MEETING AT MIDNIGHT"
        h = student.compute_sha256_hex(p_found)
        expected_h = hashlib.sha256(p_found.encode('utf-8')).hexdigest()
        assert h == expected_h
        test_logs.append("Mission 3.1: Spy Message & SHA-256 Integrity ........ [ PASS ] (+10 pts)")
        code_score += 10
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Mission 3.1: Spy Message & SHA-256 Integrity ........ [ TODO ]")
    except Exception as e:
        test_logs.append(f"Mission 3.1: Spy Message & SHA-256 Integrity ........ [ FAIL ] ({e})")

    # Bonus Mission 3.2: Avalanche Effect (+10 pts)
    try:
        t1 = "Hello Crypto 1"
        t2 = "Hello Crypto 2"
        rate = student.measure_hash_avalanche(t1, t2)
        assert 35.0 <= rate <= 65.0
        test_logs.append(f"Bonus Mission 3.2: Avalanche Effect ({rate:.1f}%) ....... [ PASS ] (+10 Extra Credit)")
        bonus_passed = True
    except NotImplementedError:
        test_logs.append("Bonus Mission 3.2: Avalanche Effect ................. [ SKIPPED ] (Optional)")
    except Exception as e:
        test_logs.append(f"Bonus Mission 3.2: Avalanche Effect ................. [ FAIL ] ({e})")

    return code_score, 10 if bonus_passed else 0, bonus_passed, test_logs


def main():
    parser = argparse.ArgumentParser(description="Beginner Cryptography Assignment Validator & Packager")
    parser.add_argument("--student-id", default="", help="Your official Student ID")
    parser.add_argument("--name", default="", help="Your Full Name")
    parser.add_argument("--no-zip", action="store_true", help="Skip zip packaging, run validation only")
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print(" 🎓 BEGINNER CRYPTOGRAPHY ASSIGNMENT PRE-FLIGHT CHECKER")
    print(" (ระบบตรวจสอบความพร้อมก่อนส่งงาน วิทยาการรหัสลับระดับผู้เริ่มต้น)")
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
        print(f"[+] Student: {student_name} (ID: {student_id})")

    # 2. Check Code File Existence
    if not os.path.exists(STUDENT_CODE_FILE):
        print(f"[❌] Error: Could not find student code file at {STUDENT_CODE_FILE}")
        sys.exit(1)
    print(f"[+] Student code file found: assignment_beginner_student.py")

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
    print(f"[+] Theory Report Score : __ / 30 Points (Graded by Teaching Staff)")

    # 5. Calculate Integrity Hashes
    code_hash = compute_sha256(STUDENT_CODE_FILE)
    report_hash = compute_sha256(report_file) if os.path.exists(report_file) else "MISSING"

    print("\n[+] Cryptographic Integrity Hashes (SHA-256):")
    print(f"    • Python Code : {code_hash}")
    print(f"    • Report File : {report_hash}")

    # 6. Generate Metadata Receipt
    timestamp_utc = datetime.now(timezone.utc).isoformat()
    metadata = {
        "assignment": "Beginner Cryptography Assignment",
        "student_name": student_name,
        "student_id": student_id,
        "timestamp_utc": timestamp_utc,
        "code_score": code_score,
        "bonus_score": bonus_score,
        "code_sha256": code_hash,
        "report_sha256": report_hash,
        "validator_version": "1.0.0"
    }

    metadata_path = os.path.join(ASSIGNMENTS_DIR, "submission_metadata_beginner.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[+] Metadata receipt saved: submission_metadata_beginner.json")

    # 7. Package ZIP bundle
    if not args.no_zip:
        zip_filename = f"submission_{student_id}_beginner.zip"
        zip_filepath = os.path.join(ASSIGNMENTS_DIR, zip_filename)

        with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(STUDENT_CODE_FILE, arcname="assignment_beginner_student.py")
            if os.path.exists(report_file):
                zipf.write(report_file, arcname=os.path.basename(report_file))
            zipf.write(metadata_path, arcname="submission_metadata_beginner.json")

        zip_hash = compute_sha256(zip_filepath)
        print(f"\n[+] Submission archive packaged successfully:")
        print(f"    📁 Archive File : assignments/{zip_filename}")
        print(f"    🔒 Bundle SHA256: {zip_hash}")

    print("\n" + "=" * 70)
    print(" 🚀 PRE-FLIGHT EVALUATION COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
