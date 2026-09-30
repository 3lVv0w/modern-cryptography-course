#!/usr/bin/env python3
"""
================================================================================
🎓 DAY 1 FOCUS ASSIGNMENT PRE-FLIGHT VALIDATOR & PACKAGER
Course: Modern Cryptography & Network Security (CS-4XX / ECE-4XX)
Module: Day 1 — Classical Ciphers & Wheel Mechanics
================================================================================
Usage:
    python3 assignments/submit_check_day1.py --student-id "65070001" --name "Jane Doe"
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
STUDENT_CODE_FILE = os.path.join(ASSIGNMENTS_DIR, "assignment_day1_student.py")
REPORT_FILES_TO_CHECK = [
    os.path.join(ASSIGNMENTS_DIR, "REPORT_DAY1.md"),
    os.path.join(ASSIGNMENTS_DIR, "REPORT_DAY1_TH.md"),
    os.path.join(ASSIGNMENTS_DIR, "REPORT_TEMPLATE_DAY1_TH.md"),
    os.path.join(ASSIGNMENTS_DIR, "REPORT_TEMPLATE_DAY1.md")
]


def find_report_file() -> str:
    """Finds active Day 1 report file (EN or TH)."""
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
        import assignment_day1_student as student
    except Exception as e:
        return 0, 0, False, [f"Critical import error in student code: {e}"]

    test_logs = []
    code_score = 0
    passed_count = 0
    bonus_passed = False

    # Question 1: Short Message Without Wheel (20 pts)
    try:
        c = student.caesar_direct_encrypt("ATTACK AT DAWN!", 3)
        p = student.caesar_direct_decrypt(c, 3)
        assert c == "DWWDFN DW GDZQ!" and p == "ATTACK AT DAWN!"
        test_logs.append("Question 1: Short Message Encrypt/Decrypt (Without Wheel) ... [ PASS ] (+20 pts)")
        code_score += 20
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Question 1: Short Message Encrypt/Decrypt (Without Wheel) ... [ TODO ]")
    except Exception as e:
        test_logs.append(f"Question 1: Short Message Encrypt/Decrypt (Without Wheel) ... [ FAIL ] ({e})")

    # Question 2: Short Message With Wheel (20 pts)
    try:
        wheel = student.CipherWheel(shift=3)
        c = student.wheel_encrypt_short("ATTACK AT DAWN!", wheel)
        p = student.wheel_decrypt_short(c, wheel)
        assert c == "DWWDFN DW GDZQ!" and p == "ATTACK AT DAWN!"
        test_logs.append("Question 2: Short Message Encrypt/Decrypt (With Wheel) ...... [ PASS ] (+20 pts)")
        code_score += 20
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Question 2: Short Message Encrypt/Decrypt (With Wheel) ...... [ TODO ]")
    except Exception as e:
        test_logs.append(f"Question 2: Short Message Encrypt/Decrypt (With Wheel) ...... [ FAIL ] ({e})")

    # Question 3: Long Message Processing (20 pts)
    try:
        long_txt = student.LONG_HISTORICAL_MESSAGE
        c_dir = student.process_long_message_direct(long_txt, 7, "encrypt")
        c_whl = student.process_long_message_wheel(long_txt, student.CipherWheel(7), "encrypt")
        assert c_dir == c_whl and c_dir != long_txt
        p_dir = student.process_long_message_direct(c_dir, 7, "decrypt")
        assert p_dir == long_txt
        test_logs.append("Question 3: Long Message Processing & Equivalence .......... [ PASS ] (+20 pts)")
        code_score += 20
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Question 3: Long Message Processing & Equivalence .......... [ TODO ]")
    except Exception as e:
        test_logs.append(f"Question 3: Long Message Processing & Equivalence .......... [ FAIL ] ({e})")

    # Question 4: Progressive Rotor Stepping Wheel (20 pts)
    try:
        s_enc = student.progressive_wheel_encrypt("AAAAAA", 1, 1)
        assert s_enc == "BCDEFG"
        s_dec = student.progressive_wheel_decrypt(s_enc, 1, 1)
        assert s_dec == "AAAAAA"
        test_logs.append("Question 4: Progressive Rotor Stepping Wheel ............... [ PASS ] (+20 pts)")
        code_score += 20
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Question 4: Progressive Rotor Stepping Wheel ............... [ TODO ]")
    except Exception as e:
        test_logs.append(f"Question 4: Progressive Rotor Stepping Wheel ............... [ FAIL ] ({e})")

    # Question 5: Applied Cryptanalysis Intercept (20 pts)
    try:
        cable = "AOL JVUMLYLUJL PZ ZJOLKBSLK MVY TPKUPNOA HA AOL OPNI ZLJYLA IBURLY."
        s_a, p_a = student.crack_without_wheel(cable, "CONFERENCE")
        s_b, p_b = student.crack_with_wheel(cable, student.CipherWheel(), "CONFERENCE")
        assert s_a == s_b == 7 and "THE CONFERENCE IS SCHEDULED" in p_a
        test_logs.append("Question 5: Intercept Cryptanalysis (With & Without Wheel) . [ PASS ] (+20 pts)")
        code_score += 20
        passed_count += 1
    except NotImplementedError:
        test_logs.append("Question 5: Intercept Cryptanalysis (With & Without Wheel) . [ TODO ]")
    except Exception as e:
        test_logs.append(f"Question 5: Intercept Cryptanalysis (With & Without Wheel) . [ FAIL ] ({e})")

    # Bonus Question: Scrambled Keyed Wheel (+10 pts)
    try:
        c_scram = student.scrambled_wheel_encrypt("TEST SECRET", "KEYWORD", 3)
        p_scram = student.scrambled_wheel_decrypt(c_scram, "KEYWORD", 3)
        assert p_scram == "TEST SECRET"
        test_logs.append("Bonus Question: Scrambled Keyed Alphabet Wheel ............. [ PASS ] (+10 Extra Credit)")
        bonus_passed = True
    except NotImplementedError:
        test_logs.append("Bonus Question: Scrambled Keyed Alphabet Wheel ............. [ SKIPPED ] (Optional)")
    except Exception as e:
        test_logs.append(f"Bonus Question: Scrambled Keyed Alphabet Wheel ............. [ FAIL ] ({e})")

    return code_score, 10 if bonus_passed else 0, bonus_passed, test_logs


def main():
    parser = argparse.ArgumentParser(description="Day 1 Focus Assignment Pre-Flight Validator & Packager")
    parser.add_argument("--student-id", default="", help="Your Student ID")
    parser.add_argument("--name", default="", help="Your Full Name")
    parser.add_argument("--no-zip", action="store_true", help="Skip zip packaging, run validation only")
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print(" 🎓 DAY 1 FOCUS ASSIGNMENT PRE-FLIGHT CHECKER")
    print(" (Classical Ciphers: Short/Long Messages, With & Without Wheel Support)")
    print("=" * 70)

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

    if not os.path.exists(STUDENT_CODE_FILE):
        print(f"[❌] Error: Could not find student code file at {STUDENT_CODE_FILE}")
        sys.exit(1)
    print(f"[+] Student code file found: assignment_day1_student.py")

    report_file = find_report_file()
    report_ok, report_msg = validate_report(report_file)
    report_basename = os.path.basename(report_file)
    if report_ok:
        print(f"[+] Written report found: {report_basename} ({report_msg})")
    else:
        print(f"[⚠️] Written report warning: {report_basename} -> {report_msg}")

    print("\n[+] Running Automated Test Suite (5 Core Questions)...")
    code_score, bonus_score, bonus_ok, logs = run_student_tests()
    for log in logs:
        print(f"    -> {log}")

    print(f"\n[+] Automated Code Score: {code_score} / 100 Points")
    if bonus_ok:
        print(f"[+] Bonus Extra Credit  : +{bonus_score} Points")
    print(f"[+] Theory Report Score : Graded via REPORT_DAY1.md")

    code_hash = compute_sha256(STUDENT_CODE_FILE)
    report_hash = compute_sha256(report_file) if os.path.exists(report_file) else "MISSING"

    print("\n[+] Cryptographic Integrity Hashes (SHA-256):")
    print(f"    • Python Code : {code_hash}")
    print(f"    • Report File : {report_hash}")

    timestamp_utc = datetime.now(timezone.utc).isoformat()
    metadata = {
        "assignment": "Day 1 Focus Assignment (Classical Ciphers & Wheel Mechanics)",
        "student_name": student_name,
        "student_id": student_id,
        "timestamp_utc": timestamp_utc,
        "code_score": code_score,
        "bonus_score": bonus_score,
        "code_sha256": code_hash,
        "report_sha256": report_hash,
        "validator_version": "1.0.0"
    }

    metadata_path = os.path.join(ASSIGNMENTS_DIR, "submission_metadata_day1.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[+] Metadata receipt saved: submission_metadata_day1.json")

    if not args.no_zip:
        zip_filename = f"submission_{student_id}_day1.zip"
        zip_filepath = os.path.join(ASSIGNMENTS_DIR, zip_filename)

        with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(STUDENT_CODE_FILE, arcname="assignment_day1_student.py")
            if os.path.exists(report_file):
                zipf.write(report_file, arcname=os.path.basename(report_file))
            zipf.write(metadata_path, arcname="submission_metadata_day1.json")

        zip_hash = compute_sha256(zip_filepath)
        print(f"\n[+] Submission archive packaged successfully:")
        print(f"    📁 Archive File : assignments/{zip_filename}")
        print(f"    🔒 Bundle SHA256: {zip_hash}")

    print("\n" + "=" * 70)
    print(" 🚀 PRE-FLIGHT EVALUATION COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
