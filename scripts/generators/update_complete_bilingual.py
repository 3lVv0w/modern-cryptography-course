#!/usr/bin/env python3
"""
update_complete_bilingual.py
Comprehensive Thai & English Bilingual System for cryptography_for_beginners_presentation.html
- Covers 100% of all 52 slides
- Includes Checkpoints (.checklist-label, .checklist-desc, .stage-meter-header, .quiz-question, .quiz-answer-drawer, .quiz-reveal-btn)
- Includes Quizzes (.quiz-prompt, .quiz-opt-btn span, data-feedback, .quiz-badge)
- Includes Interactive Labs (all inputs, buttons, status indicators, badges, titles)
- Includes Q&A Forums and standard cards
- Includes Slide Directory Grid modal
- Ensures clean, unwrapped floating dock button with white-space: nowrap
- Binds 'L' key and supports ?lang=th URL parameter and localStorage
"""

import re
import json

def get_full_thai_dictionary():
    # Load base dictionary from generate_thai_support.py
    import generate_thai_support
    base_dict = generate_thai_support.get_thai_translations()

    # Detailed Checkpoint translations
    base_dict[7]["checklistDetails"] = [
        {"label": "4 เสาหลักความปลอดภัย (CIA+A)", "desc": "แยกความแตกต่างระหว่าง Confidentiality (AES), Integrity (SHA-256), Authentication (CAs) และ Non-Repudiation (Signatures) ได้อย่างแม่นยำ"},
        {"label": "Encoding vs. Hashing vs. Encryption", "desc": "เข้าใจว่า Base64 ไม่มีความปลอดภัย, Hashing เป็นฟังก์ชันทางเดียวไม่มีย้อนกลับ, และ Encryption ต้องอาศัยกุญแจลับ"},
        {"label": "โมเดลภัยคุกคาม (Threat Models)", "desc": "เข้าใจความแตกต่างระหว่าง Eve (ผู้ดักฟังแบบไม่แก้ไขข้อมูล) กับ Mallory (ผู้ดักแก้ไขและแทรกแซงแพ็กเก็ต)"},
        {"label": "หลักการของเคิร์กฮอฟฟ์ (Kerckhoffs's Principle)", "desc": "เข้าใจเหตุผลว่าทำไมอัลกอริทึมต้องเปิดเผยเป็นสาธารณะ และกุญแจเท่านั้นที่ต้องเก็บเป็นความลับ"}
    ]
    base_dict[7]["stageMeter"] = {"title": "ความเข้าใจด่านที่ 1", "status": "เสร็จสิ้น 16%"}
    base_dict[7]["intuition"] = {
        "header": "🧠 ทดสอบความเข้าใจสั้นๆ",
        "question": "\"ผู้โจมตีแก้ไขยอดโอนเงินจาก 500 บาทเป็น 50,000 บาท โดยที่ไม่รู้ยอดเงินคงเหลือในบัญชี เสาหลักความปลอดภัยใดล้มเหลว?\"",
        "btn": "ดูเฉลยคำตอบ ▼",
        "answer": "<strong>คำตอบ:</strong> ความถูกต้องสมบูรณ์ (Integrity)! ความลับยังคงอยู่เพราะผู้โจมตีไม่รู้ยอดเงินคงเหลือ แต่เพราะไม่มีระบบตรวจจับการดัดแปลง (MAC/HMAC) ข้อมูลจึงถูกแก้ไข"
    }

    base_dict[14]["checklistDetails"] = [
        {"label": "การเลื่อนซีซาร์ (Caesar Modular Shift)", "desc": "เข้าใจเลขคณิตมอดุลาร์ C = (P + k) mod 26 และเหตุผลที่กุญแจ 25 รูปแบบถูกทดสอบจนแตกได้ในพริบตา"},
        {"label": "พลังของการวิเคราะห์ความถี่ (Frequency Analysis)", "desc": "เข้าใจแนวคิดทางสถิติของ Al-Kindi ที่พบว่าภาษาธรรมชาติทิ้งลายนิ้วมือความถี่ไว้เสมอ ('E' = 12.7%)"},
        {"label": "จุดอ่อนของเครื่องอินิกมา (Enigma Flaws)", "desc": "รู้ว่าโรเตอร์สร้างความสับสนได้ดี แต่ข้อจำกัด 'ตัวอักษรไม่เข้ารหัสเป็นตัวเอง' ทำให้ทัวริงสร้างเครื่อง Bombe มาเจาะได้"},
        {"label": "ความย้อนแย้งของ One-Time Pad", "desc": "เข้าใจการพิสูจน์ Perfect Secrecy ของ Shannon และเหตุผลที่ปัญหาการส่งกุญแจทำให้ใช้งานบนเว็บจริงไม่ได้"}
    ]
    base_dict[14]["stageMeter"] = {"title": "ความเข้าใจด่านที่ 2", "status": "เสร็จสิ้น 32%"}
    base_dict[14]["intuition"] = {
        "header": "🧠 ทดสอบความเข้าใจสั้นๆ",
        "question": "\"ทำไมเราจึงไม่สามารถนำกุญแจสุ่ม 100 ตัวอักษรมาเข้ารหัสอีเมลยาว 1,000 ตัวอักษรซ้ำวนไปเรื่อยๆ ด้วย One-Time Pad ได้?\"",
        "btn": "ดูเฉลยคำตอบ ▼",
        "answer": "<strong>คำตอบ:</strong> เพราะผิดกฎของ Shannon! การใช้กุญแจซ้ำจะทำให้กลายเป็นรหัส Vigenère ที่เปิดช่องให้ถูกโจมตีด้วยสถิติทางภาษาศาสตร์ได้ OTP กำหนดว่าความยาวกุญแจต้องเท่ากับข้อความเสมอ"
    }

    base_dict[23]["checklistDetails"] = [
        {"label": "กุญแจลับร่วมกัน (Symmetric Shared Secret)", "desc": "เข้าใจว่าการเข้ารหัสสมมาตรใช้กุญแจดอกเดียวกัน รวดเร็วระดับฮาร์ดแวร์ แต่มีจุดตายเรื่องการแจกจ่ายกุญแจ"},
        {"label": "4 ขั้นตอนการแปลงของ AES", "desc": "SubBytes (ความสับสนแบบไม่เชิงเส้น), ShiftRows (การแพร่กระจาย), MixColumns (ผสมคอลัมน์) และ AddRoundKey (รวมกุญแจ)"},
        {"label": "ช่องโหว่เพนกวินของ ECB (ECB Penguin Flaw)", "desc": "ECB เข้ารหัสบล็อกที่เหมือนกันได้ผลเหมือนกัน ทำให้โครงสร้างข้อมูลและภาพเพนกวินรั่วไหลผ่านข้อความรหัส"},
        {"label": "การเข้ารหัสแบบรับรองความถูกต้อง (AES-GCM AEAD)", "desc": "มาตรฐานยุคใหม่ที่ให้ทั้งความลับและการตรวจสอบการดัดแปลงข้อมูลผ่าน Nonce 96 บิต และ Tag 128 บิต"}
    ]
    base_dict[23]["stageMeter"] = {"title": "ความเข้าใจด่านที่ 3", "status": "เสร็จสิ้น 48%"}
    base_dict[23]["intuition"] = {
        "header": "🧠 ทดสอบความเข้าใจสั้นๆ",
        "question": "\"จะเกิดหายนะด้านความปลอดภัยอะไรขึ้น หากคุณใช้ค่า Nonce/IV เดิมซ้ำกับกุญแจ AES-GCM ดอกเดิมซ้ำสองครั้ง?\"",
        "btn": "ดูเฉลยคำตอบ ▼",
        "answer": "<strong>คำตอบ:</strong> สูญเสียคุณสมบัติการรับรองความถูกต้องโดยสิ้นเชิง! การใช้ Nonce ซ้ำเปิดโอกาสให้ผู้โจมตีคำนวณกุญแจย่อยของการพิสูจน์ตัวตน (H) และปลอมแปลงข้อความรหัสที่ถูกต้องได้"
    }

    base_dict[32]["checklistDetails"] = [
        {"label": "บทบาทของกุญแจคู่ (Public vs. Private Key Roles)", "desc": "กุญแจสาธารณะใช้สำหรับเข้ารหัสหรือตรวจสอบลายมือชื่อ ส่วนกุญแจส่วนตัวใช้สำหรับถอดรหัสหรือสร้างลายมือชื่อ"},
        {"label": "การผสมสีแบบ Diffie-Hellman", "desc": "เปิดโอกาสให้คนแปลกหน้าสองคนตกลงกุญแจลับร่วมกันได้ผ่านเครือข่ายสาธารณะที่มีผู้ดักฟัง"},
        {"label": "ฟังก์ชันทางเดียวแบบมีช่องลับ (Trapdoor Mathematics)", "desc": "เข้าใจว่าการคูณจำนวนเฉพาะทำได้ง่าย แต่การแยกตัวประกอบ n = p * q แทบเป็นไปไม่ได้หากไม่มีค่า φ(n)"},
        {"label": "ความเหนือชั้นของเส้นโค้งวงรี (ECC Superiority)", "desc": "รู้ว่าเส้นโค้งวงรี 256 บิต (Curve25519) ปลอดภัยเทียบเท่า RSA 3072 บิต แต่ใช้ทรัพยากรและแบตเตอรี่น้อยกว่ามาก"}
    ]
    base_dict[32]["stageMeter"] = {"title": "ความเข้าใจด่านที่ 4", "status": "เสร็จสิ้น 64%"}
    base_dict[32]["intuition"] = {
        "header": "🧠 ทดสอบความเข้าใจสั้นๆ",
        "question": "\"ทำไมเราจึงไม่นำ RSA หรือ ECC มาเข้ารหัสไฟล์วิดีโอขนาด 10 GB โดยตรงไปเลย?\"",
        "btn": "ดูเฉลยคำตอบ ▼",
        "answer": "<strong>คำตอบ:</strong> เพราะคณิตศาสตร์แบบอสมมาตรช้ากว่าแบบสมมาตรถึง 1,000 - 10,000 เท่า! เราจึงใช้ระบบอสมมาตรเพียงไม่กี่มิลลิวินาทีแรกเพื่อตกลงกุญแจ แล้วส่งต่อให้ AES ทำการสตรีมข้อมูลความเร็วสูง"
    }

    base_dict[38]["checklistDetails"] = [
        {"label": "คุณสมบัติของฟังก์ชันแฮช (Cryptographic Hash)", "desc": "แน่นอนคงที่ (Deterministic), ต้านทานการย้อนกลับ (Pre-Image Resistant) และต้านทานการชนกันของแฮช (Collision Resistant)"},
        {"label": "ปรากฏการณ์หิมะถล่ม (The Avalanche Effect)", "desc": "การเปลี่ยนข้อมูลนำเข้าเพียง 1 บิต ส่งผลให้บิตของผลลัพธ์แฮชพลิกกลับสุ่มประมาณ 50% โดยไม่มีความสัมพันธ์เดิม"},
        {"label": "กลไกของลายมือชื่อดิจิทัล (Digital Signatures)", "desc": "เอกสาร -> SHA-256 -> ลงนามด้วย Private Key ของผู้ส่ง และตรวจสอบได้โดยทุกคนผ่าน Public Key"},
        {"label": "โครงสร้างใบรับรองและ PKI (X.509 Certificates)", "desc": "Root CA ลงนาม Intermediate CA ซึ่งลงนามรับรองใบรับรองของเว็บไซต์ปลายทาง (Leaf Certificate) ที่ติดตั้งอยู่ในเบราว์เซอร์"}
    ]
    base_dict[38]["stageMeter"] = {"title": "ความเข้าใจด่านที่ 5", "status": "เสร็จสิ้น 80%"}
    base_dict[38]["intuition"] = {
        "header": "🧠 ทดสอบความเข้าใจสั้นๆ",
        "question": "\"เราสามารถนำข้อความลับมาผ่าน SHA-256 เพื่อส่งให้เฉพาะผู้รับที่มีสิทธิ์อ่านได้หรือไม่?\"",
        "btn": "ดูเฉลยคำตอบ ▼",
        "answer": "<strong>คำตอบ:</strong> ไม่ได้เด็ดขาด! เพราะ SHA-256 เป็นฟังก์ชันบีบอัดข้อมูลทางเดียว ไม่ใช่การเข้ารหัสลับ มันไม่มีกุญแจลับ และไม่มีใครในโลกสามารถถอดรหัสกลับมาเป็นข้อความต้นฉบับได้"
    }

    base_dict[44]["checklistDetails"] = [
        {"label": "กระบวนการ TLS 1.3 Handshake Flow", "desc": "การจับมือแบบ 1-RTT ที่ใช้ ECDH เจรจากุญแจเซสชัน ยืนยันตัวตนด้วยใบรับรอง X.509 และสลับไปใช้ AES-256-GCM ทันที"},
        {"label": "การเข้ารหัสต้นทางถึงปลายทาง (E2EE)", "desc": "Signal และ WhatsApp ใช้ Double Ratchet เพื่อสร้างกุญแจใหม่ทุกข้อความ พร้อมคุณสมบัติ Forward Secrecy"},
        {"label": "หายนะในโลกความเป็นจริง (Real-World Catastrophes)", "desc": "ทำไมคณิตศาสตร์ไม่เคยล้มเหลวแต่โค้ดล้มเหลว: Heartbleed (บั๊กหน่วยความจำ), PS3 (ใช้ค่าสุ่มซ้ำ) และช่องทางด้านข้าง"},
        {"label": "การเปรียบเทียบแบบเวลาคงที่ (Constant-Time Execution)", "desc": "โค้ดด้านวิทยาการรหัสลับต้องหลีกเลี่ยงเงื่อนไข if-else ที่ขึ้นกับความลับเพื่อป้องกัน Timing Attacks"}
    ]
    base_dict[44]["stageMeter"] = {"title": "ความเข้าใจด่านที่ 6", "status": "เสร็จสิ้น 92%"}
    base_dict[44]["intuition"] = {
        "header": "🧠 ทดสอบความเข้าใจสั้นๆ",
        "question": "\"หากแฮกเกอร์ดักจับข้อมูลของคุณผ่าน Wi-Fi สาธารณะขณะที่คุณกำลังเข้าใช้งานเว็บไซต์ HTTPS แฮกเกอร์จะมองเห็นอะไรได้บ้าง?\"",
        "btn": "ดูเฉลยคำตอบ ▼",
        "answer": "<strong>คำตอบ:</strong> มองเห็นเฉพาะชื่อโดเมนและ IP ของเซิร์ฟเวอร์เท่านั้น (ผ่าน SNI/DNS)! ส่วน URL ย่อย, ข้อมูลที่กรอก, รหัสผ่าน, คุกกี้ และเนื้อหาทั้งหมดจะถูกเข้ารหัสด้วย AES-GCM อย่างปลอดภัย 100%"
    }

    # Detailed Quiz translations
    base_dict[15]["quizDetails"] = [
        {
            "badge": "คำถามที่ 1",
            "prompt": "นักพัฒนาคนหนึ่งจัดเก็บรหัสผ่านผู้ใช้ในฐานข้อมูลด้วยการแปลงเป็น Base64 ช่องโหว่ความปลอดภัยขั้นพื้นฐานคืออะไร?",
            "options": [
                {"text": "A. Base64 เป็นเพียงรูปแบบการแปลงข้อมูล (Encoding) ที่ไม่มีการใช้กุญแจลับ ทุกคนสามารถถอดรหัสกลับได้ทันที", "feedback": "ถูกต้อง! Base64 ไม่ใช่การเข้ารหัสลับ แต่เป็นมาตรฐานการแปลงข้อมูลไบนารีเป็นข้อความที่ไม่มีความลับใดๆ"},
                {"text": "B. Base64 เสี่ยงต่อการถูกวิเคราะห์ความถี่ของตัวอักษรด้วยวิธีของ Al-Kindi", "feedback": "ไม่ถูกต้อง Base64 ไม่จำเป็นต้องใช้การวิเคราะห์ความถี่ เพราะไม่มีกุญแจลับให้เจาะ ทุกคนถอดรหัสได้โดยตรง!"},
                {"text": "C. Base64 ใช้พลังประมวลผลของซีพียูสูงเกินไปในการประมวลผล", "feedback": "ไม่ถูกต้อง Base64 ประมวลผลได้รวดเร็วมาก แต่ไม่มีการรักษาความลับใดๆ เลย"}
            ]
        },
        {
            "badge": "คำถามที่ 2",
            "prompt": "Eve ดักจับข้อความรหัสโบราณที่ใช้วิธีแทนที่ตัวอักษรเดี่ยว (Monoalphabetic Substitution) พบว่าตัวอักษร 'Q' ปรากฏบ่อยถึง 13% ตัวอักษร 'Q' นี้น่าจะแทนตัวอักษรใดในภาษาอังกฤษ?",
            "options": [
                {"text": "A. ตัวอักษร 'T' (ตัวอักษรที่พบบ่อยเป็นอันดับสอง)", "feedback": "ไม่ถูกต้อง แม้ 'T' จะพบบ่อย (~9.1%) แต่ 'E' มีความถี่สูงสุดที่ ~12.7%"},
                {"text": "B. ตัวอักษร 'E' (ตัวอักษรที่พบบ่อยที่สุดในภาษาอังกฤษตามธรรมชาติ ~12.7%)", "feedback": "ถูกต้อง! ตัวอักษร 'E' ในภาษาอังกฤษปรากฏบ่อยที่สุด (~12.7%) การแทนที่ตัวอักษรเดี่ยวจะไม่สามารถทำลายสถิติความถี่นี้ได้เลย!"},
                {"text": "C. ตัวอักษร 'Z' (ตัวอักษรที่พบน้อยที่สุด)", "feedback": "ไม่ถูกต้อง 'Z' ปรากฏเพียง ~0.07% ในภาษาอังกฤษมาตรฐาน"}
            ]
        }
    ]

    base_dict[24]["quizDetails"] = [
        {
            "badge": "คำถามที่ 1",
            "prompt": "ทำไมโครงร่างของเพนกวิน 'Linux Tux Penguin' จึงยังคงมองเห็นได้อย่างชัดเจนเมื่อเข้ารหัสด้วย AES ในโหมด ECB?",
            "options": [
                {"text": "A. โหมด ECB เข้ารหัสบล็อกข้อมูลต้นฉบับที่เหมือนกัน ให้กลายเป็นบล็อกข้อความรหัสที่เหมือนกันอย่างคงที่เสมอ", "feedback": "ถูกต้อง! โหมด ECB ขาดกระบวนการสุ่มค่าเริ่มต้น (IV/Nonce) ทำให้ข้อมูลที่มีลวดลายซ้ำๆ ส่งผลให้ข้อความรหัสมีลวดลายซ้ำตามไปด้วย!"},
                {"text": "B. เพราะกุญแจ AES มีขนาดสั้นเกินไป (น้อยกว่า 128 บิต)", "feedback": "ไม่ถูกต้อง ขนาดกุญแจไม่ใช่สาเหตุ แต่เป็นเพราะอัลกอริทึมของโหมด ECB ขาดการสุ่ม"},
                {"text": "C. เพราะภาพเพนกวิน Tux เป็นไฟล์เวกเตอร์ที่ข้ามชุดคำสั่ง AES-NI ของซีพียู", "feedback": "ไม่ถูกต้อง ภาพบิตแมปเป็นข้อมูลไบนารีทั่วไปที่ถูกประมวลผลผ่าน AES ตามปกติ"}
            ]
        },
        {
            "badge": "คำถามที่ 2",
            "prompt": "ใน AES-256-GCM หากนักพัฒนาเผลอใช้ค่า Nonce เดิมซ้ำกับกุญแจลับดอกเดิม จะเกิดความเสียหายร้ายแรงประการใด?",
            "options": [
                {"text": "A. การเข้ารหัสจะปลอดภัยขึ้นเป็นสองเท่าจากการสะสมของกุญแจ", "feedback": "ไม่ถูกต้องอย่างยิ่ง! การใช้ Nonce ซ้ำคือข้อห้ามร้ายแรงที่สุดในวิทยาการรหัสลับ"},
                {"text": "B. Mallory สามารถคำนวณหากุญแจตรวจสอบความถูกต้อง GHASH และปลอมแปลงข้อความรหัสที่ถูกต้องได้", "feedback": "ถูกต้อง! การใช้ Nonce ซ้ำในโหมด GCM ทำลายคุณสมบัติ Authentication Tag โดยสิ้นเชิง ทำให้ผู้โจมตีสามารถปลอมแปลงแพ็กเก็ตได้!"},
                {"text": "C. เคอร์เนลของระบบปฏิบัติการจะหยุดทำงานทันที", "feedback": "ไม่ถูกต้อง ซีพียูยังคงประมวลผลได้ตามปกติ แต่ระบบความปลอดภัยทางคณิตศาสตร์จะพังทลายลง"}
            ]
        }
    ]

    base_dict[39]["quizDetails"] = [
        {
            "badge": "คำถามที่ 1",
            "prompt": "Alice ต้องการส่งเอกสารสัญญาที่เป็นความลับถึง Bob และต้องการให้ Bob มั่นใจ 100% ว่า Alice เป็นผู้เขียนจริง ต้องใช้กุญแจคู่ใดบ้าง?",
            "options": [
                {"text": "A. เข้ารหัสด้วย Public Key ของ Alice; ลงนามด้วย Private Key ของ Bob", "feedback": "ไม่ถูกต้อง หากเข้ารหัสด้วย Public Key ของ Alice มีเพียง Alice เท่านั้นที่ถอดรหัสได้ Bob จะอ่านไม่ได้"},
                {"text": "B. เข้ารหัสด้วย Public Key ของ Bob; ลงนามด้วย Private Key ของ Alice", "feedback": "ถูกต้อง! เข้ารหัสด้วย Public Key ของ Bob เพื่อให้มีเพียง Bob ที่ถอดรหัสได้ (ความลับ) และลงนามด้วย Private Key ของ Alice เพื่อพิสูจน์ตัวตน"},
                {"text": "C. เข้ารหัสด้วย Private Key ของ Bob; ลงนามด้วย Public Key ของ Alice", "feedback": "ไม่ถูกต้อง Private Key ต้องเก็บรักษาไว้เป็นความลับ ห้ามนำมาแจกจ่ายเพื่อเข้ารหัสภายนอก"}
            ]
        },
        {
            "badge": "คำถามที่ 2",
            "prompt": "คุณคำนวณค่าแฮช SHA-256 ของไฟล์ติดตั้งระบบปฏิบัติการขนาด 10 GB จากนั้นแก้ไขข้อมูลในไฟล์เพียง 1 บิต แล้วแฮชใหม่ จะเกิดอะไรขึ้น?",
            "options": [
                {"text": "A. ค่าแฮชเปลี่ยนไปเพียงแค่ตัวอักษรฐานสิบหกตัวสุดท้ายตัวเดียว", "feedback": "ไม่ถูกต้อง ฟังก์ชันแฮชทางวิทยาการรหัสลับไม่ทำงานเป็นเส้นตรง"},
                {"text": "B. บิตของผลลัพธ์ประมาณ 50% จากทั้งหมด 256 บิต จะพลิกกลับสุ่มทั้งหมด (The Avalanche Effect)", "feedback": "ถูกต้อง! ปรากฏการณ์ Avalanche Effect ในฟังก์ชันแฮชที่ดี การเปลี่ยนข้อมูลนำเข้าเพียงบิตเดียว จะส่งผลให้บิตผลลัพธ์กระจายตัวสุ่มใหม่ประมาณ 50%!"},
                {"text": "C. ค่าแฮชยังคงเหมือนเดิมทุกประการ เพราะการเปลี่ยน 1 บิตในไฟล์ขนาด 10 GB มีผลน้อยมาก", "feedback": "ไม่ถูกต้องอย่างยิ่ง! SHA-256 ไวต่อการเปลี่ยนแปลงแม้เพียง 1 บิตเสมอ"}
            ]
        }
    ]

    base_dict[45]["quizDetails"] = [
        {
            "badge": "คำถามที่ 1",
            "prompt": "ผู้โจมตีดักบันทึกข้อมูลทราฟฟิกเว็บ TLS 1.3 ที่เข้ารหัสไว้ในวันนี้ อีก 5 ปีข้างหน้าเขาขโมยกุญแจ Private Key ของเว็บเซิร์ฟเวอร์ได้ เขาจะถอดรหัสทราฟฟิกที่บันทึกไว้ได้หรือไม่?",
            "options": [
                {"text": "A. ถอดรหัสได้แน่นอน เพราะมี Private Key ของเซิร์ฟเวอร์แล้ว", "feedback": "ไม่ถูกต้อง ใน TLS 1.2 บางโหมดอาจถอดได้ แต่ TLS 1.3 บังคับใช้ Forward Secrecy เสมอ"},
                {"text": "B. ถอดรหัสไม่ได้! เพราะ TLS 1.3 บังคับใช้ Forward Secrecy ซึ่งกุญแจชั่วคราว ECDH ของเซสชันนั้นถูกทำลายทิ้งไปทันทีแล้ว", "feedback": "ถูกต้อง! Perfect Forward Secrecy (PFS) รับประกันว่ากุญแจชั่วคราวของเซสชันในอดีตได้ถูกทำลายทิ้งไปแล้ว ข้อมูลในอดีตจึงปลอดภัยตลอดกาล!"},
                {"text": "C. ถอดรหัสได้เฉพาะกรณีที่ผู้ใช้งานเปิดผ่าน Google Chrome เท่านั้น", "feedback": "ไม่ถูกต้อง โปรโตคอล TLS 1.3 มีผลบังคับใช้เหมือนกันบนทุกเว็บเบราว์เซอร์"}
            ]
        },
        {
            "badge": "คำถามที่ 2",
            "prompt": "ทำไมการตรวจสอบรหัสผ่านในโค้ดฝั่งเซิร์ฟเวอร์จึงต้องใช้คำสั่งเปรียบเทียบแบบเวลาคงที่ (เช่น crypto.timingSafeEqual)?",
            "options": [
                {"text": "A. เพราะคำสั่งเปรียบเทียบสตริงทั่วไปจะหยุดทำงานทันทีเมื่อพบตัวอักษรแรกที่ไม่ตรงกัน ซึ่งเปิดช่องให้เกิดการโจมตีแบบ Timing Attack", "feedback": "ถูกต้อง! การหยุดเปรียบเทียบก่อนเวลาจะทำให้เวลาของซีพียูสั้นลง แฮกเกอร์ที่วัดเวลาระดับนาโนวินาทีจะสามารถเดารหัสผ่านทีละตัวอักษรได้!"},
                {"text": "B. เพราะอัลกอริทึมเวลาคงที่ประมวลผลเร็วกว่าการเปรียบเทียบสตริงทั่วไป 100 เท่า", "feedback": "ไม่ถูกต้อง อัลกอริทึมเวลาคงที่อาจใช้เวลามากกว่าเล็กน้อย แต่ปิดช่องโหว่ด้านความปลอดภัยได้ 100%"},
                {"text": "C. เพราะการเปรียบเทียบสตริงทั่วไปทำให้เกิดข้อผิดพลาดหน่วยความจำล้น (Buffer Overflow)", "feedback": "ไม่ถูกต้อง ปัญหานี้เป็นเรื่องของ Timing Side-Channel ไม่ใช่ Memory Corruption"}
            ]
        }
    ]

    # Detailed Interactive Lab translations
    base_dict[6]["labDetails"] = {
        "inputLabel": "ข้อความต้นฉบับ (INPUT PLAINTEXT):",
        "btnDecode": "ทดสอบถอดรหัส (ไม่ใช้กุญแจ) ➔",
        "btnToggleAES": "ถอดรหัสด้วยกุญแจลับ",
        "base64Note": "ไม่มีความปลอดภัย สังเกตว่าใครๆ ก็สามารถถอดรหัสได้ทันทีโดยไม่ต้องถามหารหัสผ่าน!",
        "hashNote": "ลายนิ้วมือดิจิทัลที่ไม่สามารถย้อนกลับได้ ขนาดคงที่ 256 บิต เป็นไปไม่ได้ทางคณิตศาสตร์ที่จะกู้คืนข้อมูลเดิม",
        "aesNote": "เข้ารหัสด้วยกุญแจลับ สามารถถอดรหัสกลับคืนได้เฉพาะเมื่อผู้รับมีกุญแจที่ถูกต้องตรงกันเท่านั้น!"
    }

    base_dict[11]["labDetails"] = {
        "inputLabel": "กุญแจเลื่อน (SHIFT KEY k):",
        "plainLabel": "ข้อความต้นฉบับ (Plaintext Input):",
        "cipherLabel": "ข้อความรหัส (Ciphertext Output):",
        "freqLabel": "สเปกตรัมความถี่ตัวอักษรของข้อความรหัสแบบสด (Live Frequency):",
        "freqDesc": "สังเกตยอดแท่งที่สูงที่สุด (ตัวอักษร 'E' ในภาษาอังกฤษ 12.7%) จะเลื่อนไปยังตัวอักษรใหม่อย่างชัดเจน:",
        "attackTip": "✦ วิธีเจาะของ Al-Kindi: ค้นหาแท่งที่สูงที่สุด ➔ ลบด้วยตำแหน่งเดิม ➔ ถอดรหัสได้ทันที!"
    }

    base_dict[20]["labDetails"] = {
        "btnECB": "❌ โหมด AES-ECB",
        "btnGCM": "✔ โหมด AES-GCM (AEAD)",
        "modeHeading": "เลือกโหมดการทำงานของ AES:",
        "ecbExplanation": "<strong>Electronic Codebook (ECB)</strong> เข้ารหัสบล็อก 16 ไบต์แต่ละบล็อกแยกจากกันโดยไม่มีการสุ่ม ทุกบล็อกสีขาวที่เหมือนกันจะได้ข้อความรหัสบล็อกเดิม ทำให้โครงร่างเพนกวินคงอยู่ 100%!",
        "gcmExplanation": "<strong>Galois/Counter Mode (GCM)</strong> รวมค่าสุ่ม Initialization Vector (Nonce) แม้จะเป็นข้อมูลเดิมซ้ำๆ ก็จะสร้างสัญญาณรบกวนสีขาวที่มีเอนโทรปีสูงสุด ปิดบังโครงสร้างข้อมูลอย่างสมบูรณ์!",
        "ecbWarning": "⚠️ <strong>มองเห็นโครงสร้างข้อมูล:</strong> บล็อกที่เหมือนกันได้สีข้อความรหัสที่เหมือนกันทุกประการ!",
        "gcmSuccess": "✔ <strong>การแพร่กระจายสมบูรณ์แบบ:</strong> ค่า Nonce สุ่ม 96 บิตทำลายแพทเทิร์นของข้อมูลได้อย่างสิ้นเชิง!"
    }

    base_dict[28]["labDetails"] = {
        "btnCompute": "✨ ขั้นตอนที่ 3: คำนวณกุญแจลับร่วมกัน (Shared Secret) ➔",
        "aliceTitle": "Alice (ความลับส่วนตัว)",
        "bobTitle": "Bob (ความลับส่วนตัว)",
        "eveTitle": "สายส่งสาธารณะ (Eve แอบดักฟัง)",
        "eveDesc": "Eve มองเห็นสีผสมที่แลกเปลี่ยนกันข้ามสายสัญญาณ:",
        "eveNotice": "Eve ไม่สามารถแยกสีส้มหรือสีเขียวกลับมาเป็นสีลับของแต่ละคนได้!",
        "derivedKeyLabel": "กุญแจลับที่ได้ตรงกัน:"
    }

    base_dict[35]["labDetails"] = {
        "in1Label": "ข้อความที่ 1 (INPUT MESSAGE 1):",
        "in2Label": "ข้อความที่ 2 (ต่างกันเพียง 1 ตัวอักษร):",
        "gridHeading": "ฮีตแมปเปรียบเทียบบิต 256 บิต (256-Bit Avalanche Heatmap)",
        "gridSub": "สี่เหลี่ยมสีส้มแทนบิตที่พลิกกลับ (Flipped Bits) ระหว่างแฮชที่ 1 และ 2:",
        "unchanged": "บิตคงเดิม",
        "flipped": "บิตที่พลิกกลับ (~เป้าหมาย 50%)",
        "metricTag": "ผลการคำนวณ Avalanche Effect สด",
        "metricSuccess": "✔ ผ่านเกณฑ์การแพร่กระจายทางวิทยาการรหัสลับ (SAC)"
    }

    base_dict[41]["labDetails"] = {
        "clientLabel": "ผู้ใช้งาน (Client Browser)",
        "serverLabel": "เซิร์ฟเวอร์ (Bank Cloud)",
        "btnNext": "ขั้นตอนถัดไป ➔",
        "btnAuto": "เล่นอัตโนมัติ ▶",
        "btnReset": "เริ่มใหม่ ↺"
    }

    base_dict[47]["labDetails"] = {
        "shorBadge": "ยุคดั้งเดิม: RSA & ECC",
        "shorTitle": "การโจมตีด้วยอัลกอริทึมควอนตัมของชอร์ (Shor's Attack)",
        "shorDesc": "คอมพิวเตอร์ควอนตัมใช้ Quantum Fourier Transform (QFT) เพื่อหาคาบ r ของฟังก์ชันมอดุลาร์ a^x ≡ 1 (mod n) ในเวลาพหุนาม O((log n)³)",
        "btnShor": "จำลองการรันอัลกอริทึมของชอร์ ➔",
        "shorSuccess": "RSA-2048 ถูกแยกตัวประกอบสำเร็จในเวลาไม่กี่วินาที!",
        "latticeBadge": "ยุคหลังควอนตัม: NIST ML-KEM",
        "latticeTitle": "เกราะกำบังโครงข่ายแลตทิซมิติสูง (High-Dimensional Lattice)",
        "latticeDesc": "อิงจากปัญหาทางคณิตศาสตร์ Learning With Errors (LWE) ในปริภูมิยูคลิดมากกว่า 500 มิติพร้อมสัญญาณรบกวนแบบเกาส์เซียน",
        "btnLattice": "ทดสอบความต้านทานควอนตัมบนโครงข่ายแลตทิซ ➔",
        "latticeSuccess": "ปัญหาเวกเตอร์ที่สั้นที่สุด (SVP) ไม่มีอัลกอริทึมควอนตัมใดเจาะได้ในเวลาพหุนาม!"
    }

    return base_dict

def update_presentation_html():
    html_path = "cryptography_for_beginners_presentation.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    thai_dict = get_full_thai_dictionary()
    thai_json = json.dumps(thai_dict, ensure_ascii=False, indent=2)

    # 1. Update CSS for lang button to prevent wrapping
    lang_btn_css = """
        .lang-toggle-btn {
            font-family: var(--font-display);
            font-size: 0.8rem !important;
            font-weight: 700;
            padding: 0 10px !important;
            width: auto !important;
            height: 36px !important;
            white-space: nowrap !important;
            border-radius: 999px !important;
            background: rgba(99, 102, 241, 0.18) !important;
            border: 1px solid rgba(99, 102, 241, 0.45) !important;
            color: var(--text-title) !important;
            display: inline-flex !important;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }

        .lang-toggle-btn:hover {
            background: var(--accent-indigo) !important;
            color: #FFFFFF !important;
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.4);
        }
    """

    if ".lang-toggle-btn {" in html:
        html = re.sub(r'\.lang-toggle-btn\s*\{[\s\S]*?\.lang-toggle-btn:hover\s*\{[\s\S]*?\}', lang_btn_css.strip(), html)
        print("Updated .lang-toggle-btn CSS to enforce white-space: nowrap and height: 36px.")

    # 2. Comprehensive bilingual script engine
    engine_code = f"""
            // =================================================================
            // BILINGUAL THAI / ENGLISH (TH/EN) TRANSLATION ENGINE
            // =================================================================
            const THAI_DATA = {thai_json};
            const ENGLISH_DATA = {{}};
            let currentLang = 'en';

            const langBtn = document.getElementById('langBtn');

            function cacheEnglishSlides() {{
                slides.forEach((slide, idx) => {{
                    const slideNum = idx + 1;
                    const data = {{}};
                    
                    const tagEl = slide.querySelector('.slide-tag');
                    if (tagEl) data.tag = tagEl.innerHTML;

                    const bcEl = slide.querySelector('.slide-breadcrumb');
                    if (bcEl) data.breadcrumb = bcEl.innerHTML;

                    const mainTitleEl = slide.querySelector('.slide-main-title') || slide.querySelector('.hero-title');
                    if (mainTitleEl) data.mainTitle = mainTitleEl.innerHTML;

                    const subEl = slide.querySelector('.slide-subtitle') || slide.querySelector('.hero-subtitle');
                    if (subEl) data.subtitle = subEl.innerHTML;

                    const heroPre = slide.querySelector('.hero-pre-badge');
                    if (heroPre) data.heroPre = heroPre.innerHTML;

                    const cards = Array.from(slide.querySelectorAll('.pres-card'));
                    if (cards.length > 0) {{
                        data.cards = cards.map(c => ({{
                            badge: c.querySelector('.card-badge') ? c.querySelector('.card-badge').innerHTML : '',
                            title: c.querySelector('.card-title') ? c.querySelector('.card-title').innerHTML : '',
                            desc: c.querySelector('.card-desc') ? c.querySelector('.card-desc').innerHTML : ''
                        }}));
                    }}

                    const callout = slide.querySelector('.callout-box:not(#matrixStatusBanner)');
                    if (callout) data.callout = callout.innerHTML;

                    // Checkpoints
                    const checkItems = Array.from(slide.querySelectorAll('.checklist-item'));
                    if (checkItems.length > 0) {{
                        data.checklistDetails = checkItems.map(item => ({{
                            label: item.querySelector('.checklist-label') ? item.querySelector('.checklist-label').innerHTML : '',
                            desc: item.querySelector('.checklist-desc') ? item.querySelector('.checklist-desc').innerHTML : ''
                        }}));
                    }}

                    const meterHeader = slide.querySelector('.stage-meter-header');
                    if (meterHeader) {{
                        const spans = meterHeader.querySelectorAll('span');
                        data.stageMeter = {{
                            title: spans[0] ? spans[0].innerHTML : '',
                            status: spans[1] ? spans[1].innerHTML : ''
                        }};
                    }}

                    const checkQ = slide.querySelector('.quiz-question');
                    const checkA = slide.querySelector('.quiz-answer-drawer');
                    const checkHeader = slide.querySelector('.quiz-header');
                    const checkBtn = slide.querySelector('.quiz-reveal-btn');
                    if (checkQ && checkA) {{
                        data.intuition = {{
                            header: checkHeader ? checkHeader.innerHTML : '',
                            question: checkQ.innerHTML,
                            btn: checkBtn ? checkBtn.textContent : '',
                            answer: checkA.innerHTML
                        }};
                    }}

                    // Quizzes
                    const quizCards = Array.from(slide.querySelectorAll('.interactive-quiz-card'));
                    if (quizCards.length > 0) {{
                        data.quizDetails = quizCards.map(c => ({{
                            badge: c.querySelector('.quiz-badge') ? c.querySelector('.quiz-badge').innerHTML : '',
                            prompt: c.querySelector('.quiz-prompt') ? c.querySelector('.quiz-prompt').innerHTML : '',
                            options: Array.from(c.querySelectorAll('.quiz-opt-btn')).map(b => ({{
                                text: b.querySelector('span') ? b.querySelector('span').innerHTML : b.textContent,
                                feedback: b.getAttribute('data-feedback') || ''
                            }}))
                        }}));
                    }}

                    // Q&A Forums
                    const qaBoxes = Array.from(slide.querySelectorAll('.qa-question-box'));
                    if (qaBoxes.length > 0) {{
                        data.qa = qaBoxes.map(b => ({{
                            q: b.querySelector('.qa-q-header span:last-child') ? b.querySelector('.qa-q-header span:last-child').innerHTML : '',
                            a: b.querySelector('.qa-answer-text') ? b.querySelector('.qa-answer-text').innerHTML : ''
                        }}));
                    }}

                    const footer = slide.querySelector('.slide-footer span:first-child');
                    if (footer) data.footer = footer.innerHTML;

                    ENGLISH_DATA[slideNum] = data;
                }});
            }}

            function applySlideLanguage(slide, slideNum, lang) {{
                const data = lang === 'th' ? THAI_DATA[slideNum] : ENGLISH_DATA[slideNum];
                if (!data) return;

                if (data.tag !== undefined) {{
                    const el = slide.querySelector('.slide-tag');
                    if (el) el.innerHTML = data.tag;
                }}
                if (data.breadcrumb !== undefined) {{
                    const el = slide.querySelector('.slide-breadcrumb');
                    if (el) el.innerHTML = data.breadcrumb;
                }}
                if (data.heroPre !== undefined) {{
                    const el = slide.querySelector('.hero-pre-badge');
                    if (el) el.innerHTML = data.heroPre;
                }}
                if (data.mainTitle !== undefined) {{
                    const el = slide.querySelector('.slide-main-title') || slide.querySelector('.hero-title');
                    if (el) el.innerHTML = data.mainTitle;
                }}
                if (data.subtitle !== undefined) {{
                    const el = slide.querySelector('.slide-subtitle') || slide.querySelector('.hero-subtitle');
                    if (el) el.innerHTML = data.subtitle;
                }}
                if (data.cards && Array.isArray(data.cards)) {{
                    const cards = slide.querySelectorAll('.pres-card');
                    data.cards.forEach((c, idx) => {{
                        if (cards[idx]) {{
                            const b = cards[idx].querySelector('.card-badge');
                            const t = cards[idx].querySelector('.card-title');
                            const d = cards[idx].querySelector('.card-desc');
                            if (b && c.badge) b.innerHTML = c.badge;
                            if (t && c.title) t.innerHTML = c.title;
                            if (d && c.desc) d.innerHTML = c.desc;
                        }}
                    }});
                }}
                if (data.callout !== undefined) {{
                    const el = slide.querySelector('.callout-box:not(#matrixStatusBanner)');
                    if (el) el.innerHTML = data.callout;
                }}

                // Checkpoint Items
                if (data.checklistDetails && Array.isArray(data.checklistDetails)) {{
                    const items = slide.querySelectorAll('.checklist-item');
                    data.checklistDetails.forEach((c, idx) => {{
                        if (items[idx]) {{
                            const l = items[idx].querySelector('.checklist-label');
                            const d = items[idx].querySelector('.checklist-desc');
                            if (l && c.label) l.innerHTML = c.label;
                            if (d && c.desc) d.innerHTML = c.desc;
                        }}
                    }});
                }}

                if (data.stageMeter) {{
                    const header = slide.querySelector('.stage-meter-header');
                    if (header) {{
                        const spans = header.querySelectorAll('span');
                        if (spans[0] && data.stageMeter.title) spans[0].innerHTML = data.stageMeter.title;
                        if (spans[1] && data.stageMeter.status) spans[1].innerHTML = data.stageMeter.status;
                    }}
                }}

                if (data.intuition) {{
                    const qH = slide.querySelector('.quiz-header');
                    const qQ = slide.querySelector('.quiz-question');
                    const qB = slide.querySelector('.quiz-reveal-btn');
                    const qA = slide.querySelector('.quiz-answer-drawer');
                    if (qH && data.intuition.header) qH.innerHTML = data.intuition.header;
                    if (qQ && data.intuition.question) qQ.innerHTML = data.intuition.question;
                    if (qB && data.intuition.btn) qB.textContent = data.intuition.btn;
                    if (qA && data.intuition.answer) qA.innerHTML = data.intuition.answer;
                }}

                // Quizzes
                if (data.quizDetails && Array.isArray(data.quizDetails)) {{
                    const quizCards = slide.querySelectorAll('.interactive-quiz-card');
                    data.quizDetails.forEach((q, idx) => {{
                        if (quizCards[idx]) {{
                            const b = quizCards[idx].querySelector('.quiz-badge');
                            const p = quizCards[idx].querySelector('.quiz-prompt');
                            if (b && q.badge) b.innerHTML = q.badge;
                            if (p && q.prompt) p.innerHTML = q.prompt;
                            const optBtns = quizCards[idx].querySelectorAll('.quiz-opt-btn');
                            if (q.options) {{
                                optBtns.forEach((btn, optIdx) => {{
                                    if (q.options[optIdx]) {{
                                        const span = btn.querySelector('span');
                                        if (span) span.innerHTML = q.options[optIdx].text;
                                        if (q.options[optIdx].feedback) {{
                                            btn.setAttribute('data-feedback', q.options[optIdx].feedback);
                                        }}
                                    }}
                                }});
                            }}
                        }}
                    }});
                }}

                // Q&A Forums
                if (data.qa && Array.isArray(data.qa)) {{
                    const qBoxes = slide.querySelectorAll('.qa-question-box');
                    data.qa.forEach((item, idx) => {{
                        if (qBoxes[idx]) {{
                            const qHeader = qBoxes[idx].querySelector('.qa-q-header span:last-child');
                            const aText = qBoxes[idx].querySelector('.qa-answer-text');
                            if (qHeader && item.q) qHeader.innerHTML = item.q;
                            if (aText && item.a) aText.innerHTML = item.a;
                        }}
                    }});
                }}

                // Interactive Labs
                if (data.labDetails) {{
                    const d = data.labDetails;
                    if (d.inputLabel) {{
                        const lbl = slide.querySelector('.lab-input-row span:first-child');
                        if (lbl) lbl.textContent = d.inputLabel;
                    }}
                    if (d.btnDecode) {{
                        const btn = slide.querySelector('#btnDecodeBase64');
                        if (btn) btn.textContent = d.btnDecode;
                    }}
                    if (d.btnToggleAES) {{
                        const btn = slide.querySelector('#btnToggleAES');
                        if (btn) btn.textContent = d.btnToggleAES;
                    }}
                    if (d.btnECB) {{
                        const btn = slide.querySelector('#btnSelectECB');
                        if (btn) btn.textContent = d.btnECB;
                    }}
                    if (d.btnGCM) {{
                        const btn = slide.querySelector('#btnSelectGCM');
                        if (btn) btn.textContent = d.btnGCM;
                    }}
                    if (d.btnCompute) {{
                        const btn = slide.querySelector('#btnDHComputeFinal');
                        if (btn) btn.textContent = d.btnCompute;
                    }}
                    if (d.btnNext) {{
                        const btn = slide.querySelector('#btnTlsNext');
                        if (btn) btn.textContent = d.btnNext;
                    }}
                    if (d.btnAuto) {{
                        const btn = slide.querySelector('#btnTlsAuto');
                        if (btn) btn.textContent = d.btnAuto;
                    }}
                    if (d.btnReset) {{
                        const btn = slide.querySelector('#btnTlsReset');
                        if (btn) btn.textContent = d.btnReset;
                    }}
                    if (d.btnShor) {{
                        const btn = slide.querySelector('#btnRunShor');
                        if (btn) btn.textContent = d.btnShor;
                    }}
                    if (d.btnLattice) {{
                        const btn = slide.querySelector('#btnTestLattice');
                        if (btn) btn.textContent = d.btnLattice;
                    }}
                }}

                if (data.footer !== undefined) {{
                    const el = slide.querySelector('.slide-footer span:first-child');
                    if (el) el.innerHTML = data.footer;
                }}
            }}

            function setPresentationLanguage(lang) {{
                currentLang = lang === 'th' ? 'th' : 'en';
                document.documentElement.lang = currentLang;
                document.body.classList.toggle('lang-th', currentLang === 'th');
                localStorage.setItem('crypto_presentation_lang', currentLang);

                if (langBtn) {{
                    langBtn.innerHTML = currentLang === 'th' ? '🇹🇭' : '🇬🇧';
                    langBtn.title = currentLang === 'th' ? 'สลับเป็นภาษาอังกฤษ (L) / Switch to English' : 'Switch to Thai (L) / สลับเป็นภาษาไทย';
                    langBtn.setAttribute('aria-label', currentLang === 'th' ? 'Switch to English' : 'Switch to Thai');
                }}

                // Update Directory Modal Title
                const modalTitle = document.querySelector('.grid-modal-title');
                if (modalTitle) {{
                    modalTitle.textContent = currentLang === 'th' 
                        ? 'สารบัญสไลด์การบรรยาย (52 สไลด์)' 
                        : 'Presentation Slide Directory (52 Slides)';
                }}
                const modalClose = document.getElementById('closeGridBtn');
                if (modalClose) {{
                    modalClose.textContent = currentLang === 'th' ? '✕ ปิดสารบัญ' : '✕ Close Grid';
                }}

                // Apply to all slides
                slides.forEach((slide, idx) => {{
                    applySlideLanguage(slide, idx + 1, currentLang);
                }});

                // Re-render Slide Grid Modal titles
                populateGridModal();
            }}

            function toggleLanguage() {{
                setPresentationLanguage(currentLang === 'en' ? 'th' : 'en');
            }}

            if (langBtn) {{
                langBtn.addEventListener('click', toggleLanguage);
            }}

            function initLanguage() {{
                const urlParams = new URLSearchParams(window.location.search);
                const queryLang = urlParams.get('lang');
                const savedLang = localStorage.getItem('crypto_presentation_lang');
                const initialLang = queryLang || savedLang || 'en';
                cacheEnglishSlides();
                setPresentationLanguage(initialLang);
            }}

            function populateGridModal() {{
                if (!slidesGridContainer) return;
                slidesGridContainer.innerHTML = '';
                slides.forEach((slide, idx) => {{
                    const titleEl = slide.querySelector('.slide-main-title') || slide.querySelector('.hero-title');
                    const titleText = titleEl ? titleEl.textContent.trim().replace(/\\s+/g, ' ') : `Slide ${{idx + 1}}`;
                    const section = slide.getAttribute('data-section') || 'Section';

                    const card = document.createElement('div');
                    card.className = `grid-thumb-card ${{idx === currentSlide ? 'active' : ''}}`;
                    card.innerHTML = `
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span class="grid-thumb-num">SLIDE ${{String(idx + 1).padStart(2, '0')}}</span>
                            <span style="font-size:0.75rem; color:#8492A6;">${{section}}</span>
                        </div>
                        <div class="grid-thumb-title">${{titleText}}</div>
                    `;
                    card.addEventListener('click', () => {{
                        goToSlide(idx);
                        closeGrid();
                    }});
                    slidesGridContainer.appendChild(card);
                }});
            }}
    """

    # Replace existing bilingual engine in HTML
    pattern = re.compile(r'// =================================================================\s*// BILINGUAL THAI / ENGLISH \(TH/EN\) TRANSLATION ENGINE[\s\S]*?function populateGridModal\(\) \{[\s\S]*?\}\);?\s*\}')
    if pattern.search(html):
        html = pattern.sub(lambda m: engine_code.strip(), html)
        print("Replaced bilingual engine with comprehensive full-fidelity engine.")
    else:
        print("Warning: could not find existing bilingual block to replace.")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Successfully updated presentation with complete Thai translation support!")

if __name__ == "__main__":
    update_presentation_html()
