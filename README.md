# 🎓 Modern Cryptography & Network Security Course Repository
**Level:** University CS-4XX / ECE-4XX Undergraduate & Graduate Level  
**Format:** 4-Day Intensive Workshop (Theory Lectures + 3-Tier Hands-On Labs)

---

## 📁 Repository Directory Structure

```text
modern-cryptography-course/
├── README.md                      <-- Course overview & instructions
├── course_outline.md              <-- Full 4-Day Master Syllabus & Rubrics
│
├── day1/                          <-- DAY 1: Classical Cryptanalysis & Information Theory
│   ├── learning_material.md       <-- Lecture handbook & Shannon proof
│   ├── lab_student.py             <-- 3-Tier Student Lab Notebook (Chi-Sq, IC, OTP, Crib Drag)
│   └── exercises_instructor.py    <-- Instructor solution & test verification suite
│
├── day2/                          <-- DAY 2: Number Theory & Symmetric Encryption (AES)
│   ├── learning_material.md       <-- Lecture handbook (Z_n*, AES State Matrix, Block Cipher Modes)
│   ├── lab_student.py             <-- 3-Tier Student Lab Notebook (Ext-GCD, AES-ECB flaw, AES-GCM)
│   └── exercises_instructor.py    <-- Instructor solution & test verification suite
│
├── day3/                          <-- DAY 3: Public-Key Cryptography (DHKE, RSA & ECC)
│   ├── learning_material.md       <-- Lecture handbook (DHKE, RSA proofs, IND-CPA, Curve25519)
│   ├── lab_student.py             <-- 3-Tier Student Lab Notebook (DHKE, RSA from scratch, Fermat attack)
│   └── exercises_instructor.py    <-- Instructor solution & test verification suite
│
└── day4/                          <-- DAY 4: Integrity, Signatures, PKI & TLS 1.3
    ├── learning_material.md       <-- Lecture handbook (Birthday paradox proof, Ed25519, TLS 1.3, PQC)
    ├── lab_student.py             <-- 3-Tier Student Lab Notebook (Avalanche effect, Cert chain, Capstone CTF)
    └── exercises_instructor.py    <-- Instructor solution & test verification suite
```

---

## 🚀 Running Student Labs

Students can run their daily lab scripts from the course directory:

```bash
# Day 1 Lab
python3 day1/lab_student.py

# Day 2 Lab
python3 day2/lab_student.py

# Day 3 Lab
python3 day3/lab_student.py

# Day 4 Lab
python3 day4/lab_student.py
```

---

## 🎯 3-Tier Challenge System

Each lab contains 3 difficulty tiers:
* 🟢 **LEVEL 1 (Novice):** Basic algorithm implementations & fundamentals.
* 🟡 **LEVEL 2 (Intermediate):** Statistical cryptanalysis, Index of Coincidence, AES pattern flaw checks, X.509 cert validation.
* 🔴 **LEVEL 3 (Hardcore):** Vigenère breaker, Two-Time Pad crib dragging, GCM nonce reuse exploit, Fermat RSA factorization attack, and Capstone CTF solver.
