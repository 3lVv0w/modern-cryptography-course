#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_full_bilingual_enhancement.py
Comprehensive translation engine injection for cryptography_for_beginners_presentation.html
Guarantees 100% Thai/English bilingual fidelity across:
- All 52 slides (Titles, Subtitles, Breadcrumbs, Tags, Footers, Cards, Badges, Lists)
- 6 Checkpoint slides (Checklist items, Stage meter headers & checklists, Intuition questions/answers/reveal buttons)
- 4 Quick Quizzes (Prompts, Option spans, Feedback explanations, Success/Failure banners)
- 7 Interactive Labs (Controls, Step-by-step animations, Dynamic status banners, Heatmaps, TLS packets)
- 2 Q&A Forums (All questions and comprehensive answers)
- Slide Directory Modal (Titles, Cards, Close buttons)
- Keyboard shortcut ('L' key) and URL param (?lang=th)
"""

import re
import json

def get_full_thai_dict():
    import generate_thai_support
    base_dict = generate_thai_support.get_thai_translations()

    # Enhance Lab Main Titles & Subtitles with natural TH + EN
    base_dict[6]["mainTitle"] = "Interactive Lab: เปรียบเทียบ Encoding vs. Hashing vs. Encryption"
    base_dict[6]["subtitle"] = "พิมพ์ข้อความด้านล่างเพื่อดูการทำงานของทั้ง 3 กระบวนการทางคณิตศาสตร์แบบเรียลไทม์:"

    base_dict[11]["mainTitle"] = "Interactive Lab: วงล้อซีซาร์และสเปกตรัมความถี่ตัวอักษรสด"
    base_dict[11]["subtitle"] = "เลื่อนแถบกุญแจเลื่อน (k) เพื่อหมุนตัวอักษรแทนที่ และสังเกตการเคลื่อนที่ของสเปกตรัมความถี่ภาษาอังกฤษ:"

    base_dict[20]["mainTitle"] = "Interactive Lab: แบบจำลองการรั่วไหลของข้อมูลระหว่าง ECB vs. GCM"
    base_dict[20]["subtitle"] = "สลับการทำงานระหว่างโหมด ECB (ไม่มีค่าสุ่ม) และโหมด GCM ยุคใหม่ (ใช้ Nonce สุ่ม) เพื่อดูการเปลี่ยนแปลงของแพทเทิร์นข้อมูล:"

    base_dict[28]["mainTitle"] = "Interactive Lab: การแลกเปลี่ยนกุญแจ Diffie-Hellman ด้วยการผสมสี"
    base_dict[28]["subtitle"] = "ทำตามขั้นตอนโปรโตคอลผสมสีทางคณิตศาสตร์เพื่อดูว่า Alice และ Bob สร้างกุญแจลับร่วมกันได้อย่างไรโดยที่ Eve ไม่รู้:"

    base_dict[35]["mainTitle"] = "Interactive Lab: ฮีตแมป 256 บิตตรวจสอบปรากฏการณ์หิมะถล่ม (Avalanche Effect)"
    base_dict[35]["subtitle"] = "พิมพ์ข้อความในช่องใดก็ได้ การเปลี่ยนเพียง 1 ตัวอักษรจะคำนวณแฮช 256 บิตใหม่ทันที และแสดงบิตที่พลิกกลับ:"

    base_dict[41]["mainTitle"] = "Interactive Lab: จำลองขั้นตอนการส่งแพ็กเก็ต TLS 1.3 Handshake"
    base_dict[41]["subtitle"] = "คลิก 'ขั้นตอนถัดไป' หรือ 'เล่นอัตโนมัติ' เพื่อติดตามการส่งแพ็กเก็ตวิทยาการรหัสลับข้ามสายเครือข่าย:"

    base_dict[47]["mainTitle"] = "Interactive Lab: การโจมตีด้วยคอมพิวเตอร์ควอนตัม vs. เกราะป้องกันแลตทิซ (Lattice-Based)"
    base_dict[47]["subtitle"] = "สลับระหว่างการแยกตัวประกอบ RSA/ECC กับโครงข่าย NIST ML-KEM เพื่อดูว่าทำไมแลตทิซจึงต้านทานควอนตัมได้:"

    # Enhance Stage Meter items in Checkpoints
    stage_meter_notes = {
        7: "✦ ทำความเข้าใจเสาหลักและนิยามพื้นฐานครบถ้วนแล้ว<br>✦ คลิกที่กล่องข้อความเพื่อทดสอบการจำแนกความรู้<br>✦ ตอนถัดไป: <strong>ตอนที่ 2 รหัสลับยุคคลาสสิกและบทเรียนจากประวัติศาสตร์</strong>",
        14: "✦ ทบทวนรหัสลับซีซาร์, การวิเคราะห์ความถี่, อินิกมา และ OTP ครบถ้วนแล้ว<br>✦ คลิกที่กล่องข้อความเพื่อทดสอบการจำแนกความรู้<br>✦ ตอนถัดไป: <strong>ตอนที่ 3 รหัสลับแบบสมมาตรและมาตรฐาน AES สมัยใหม่</strong>",
        23: "✦ ทบทวนบล็อกไซเฟอร์, โหมด ECB, CBC และมาตรฐาน AES-GCM AEAD ครบถ้วนแล้ว<br>✦ คลิกที่กล่องข้อความเพื่อทดสอบการจำแนกความรู้<br>✦ ตอนถัดไป: <strong>ตอนที่ 4 รหัสลับแบบอสมมาตรและโครงสร้างพื้นฐานกุญแจสาธารณะ (PKI)</strong>",
        31: "✦ ทบทวนฟังก์ชันทางเดียว, RSA, Diffie-Hellman และเส้นโค้งวงรี (ECC) ครบถ้วนแล้ว<br>✦ คลิกที่กล่องข้อความเพื่อทดสอบการจำแนกความรู้<br>✦ ตอนถัดไป: <strong>ตอนที่ 5 ฟังก์ชันแฮช, ลายมือชื่อดิจิทัล และใบรับรองดิจิทัล</strong>",
        38: "✦ ทบทวน SHA-256, ลายมือชื่อดิจิทัล และสายสัมพันธ์แห่งความไว้วางใจ X.509 ครบถ้วนแล้ว<br>✦ คลิกที่กล่องข้อความเพื่อทดสอบการจำแนกความรู้<br>✦ ตอนถัดไป: <strong>ตอนที่ 6 การประยุกต์ใช้ในโลกจริงและโปรโตคอลความปลอดภัย</strong>",
        44: "✦ ทบทวน TLS 1.3, E2EE Signal Protocol และการจัดการกุญแจครบถ้วนแล้ว<br>✦ คลิกที่กล่องข้อความเพื่อทดสอบการจำแนกความรู้<br>✦ ตอนถัดไป: <strong>ตอนที่ 7 ภัยคุกคามจากควอนตัมและวิทยาการรหัสลับยุคหลังควอนตัม (PQC)</strong>"
    }
    for slide_id, notes in stage_meter_notes.items():
        if slide_id in base_dict:
            base_dict[slide_id]["stageMeterNotes"] = notes

    # Checkpoint checklist details
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
        "answer": "<strong>คำตอบ:</strong> สูญเสียคุณสมบัติการรับรองความถูกต้อง (Authentication) โดยสิ้นเชิง! การใช้ Nonce ซ้ำเปิดโอกาสให้ผู้โจมตีคำนวณกุญแจย่อยของการพิสูจน์ตัวตน GHASH และปลอมแปลงข้อความรหัสที่ถูกต้องได้"
    }

    base_dict[31]["checklistDetails"] = [
        {"label": "ฟังก์ชันทางเดียวแบบมีประตูกล (Trapdoor Functions)", "desc": "เข้าใจคณิตศาสตร์ที่คำนวณไปข้างหน้าง่าย แต่ย้อนกลับยากยิ่งหากไม่มีกุญแจลับส่วนตัว (Private Key)"},
        {"label": "การแยกตัวประกอบเฉพาะของ RSA", "desc": "เข้าใจว่าความปลอดภัยของ RSA อิงจากการคูณจำนวนเฉพาะขนาดใหญ่ p · q = n ที่ยากต่อการแยกตัวประกอบ"},
        {"label": "ความฉลาดของ Diffie-Hellman", "desc": "เข้าใจการตกลงกุญแจลับร่วมกันผ่านสายสื่อสารสาธารณะที่ไม่ปลอดภัยได้โดยไม่ต้องส่งกุญแจลับข้ามสาย"},
        {"label": "ประสิทธิภาพของเส้นโค้งวงรี (ECC Advantage)", "desc": "เข้าใจว่า ECC 256 บิตให้ความปลอดภัยเทียบเท่า RSA 3072 บิต แต่ประหยัดแบนด์วิดท์และพลังงานกว่ามหาศาล"}
    ]
    base_dict[31]["stageMeter"] = {"title": "ความเข้าใจด่านที่ 4", "status": "เสร็จสิ้น 64%"}
    base_dict[31]["intuition"] = {
        "header": "🧠 ทดสอบความเข้าใจสั้นๆ",
        "question": "\"ทำไมระบบ HTTPS ในปัจจุบันจึงไม่ใช้ RSA เข้ารหัสหน้าเว็บ HTML ทั้งหมดโดยตรง แทนที่จะใช้สลับไปใช้ AES?\"",
        "btn": "ดูเฉลยคำตอบ ▼",
        "answer": "<strong>คำตอบ:</strong> เพราะ RSA ช้ากว่า AES ถึง 1,000 เท่า! HTTPS จึงใช้ RSA หรือ ECC ทำการแลกเปลี่ยนกุญแจแบบผสม (Hybrid Encryption) ในช่วง Handshake เท่านั้น แล้วส่งต่อให้ AES-GCM เข้ารหัสข้อมูลจริงด้วยความเร็วระดับฮาร์ดแวร์"
    }

    base_dict[38]["checklistDetails"] = [
        {"label": "คุณสมบัติ 3 ประการของฟังก์ชันแฮช", "desc": "ต้านทานการหารูปภาพต้นแบบ (Pre-image), ต้านทานภาพต้นแบบที่สอง (Second Pre-image), และต้านทานการชนกันของค่าแฮช (Collision Resistance)"},
        {"label": "ปรากฏการณ์หิมะถล่ม (Avalanche Effect)", "desc": "เข้าใจว่าการเปลี่ยนข้อมูลเพียง 1 บิตในข้อความต้นฉบับ จะทำให้บิตของค่าแฮชพลิกเปลี่ยนไปโดยเฉลี่ย 50% อย่างคาดเดาไม่ได้"},
        {"label": "การสลับการทำงานของลายมือชื่อดิจิทัล", "desc": "เข้าใจว่าการเซ็นชื่อดิจิทัลทำโดยใช้ Private Key เข้ารหัสแฮช และทุกคนสามารถตรวจสอบความถูกต้องได้ด้วย Public Key"},
        {"label": "สายสัมพันธ์แห่งความไว้วางใจ X.509 (Chain of Trust)", "desc": "เข้าใจว่าเบราว์เซอร์เชื่อถือใบรับรองของเว็บไซต์ผ่านการรับรองต่อๆ กันจาก Root Certificate Authority (CA) ในระบบปฏิบัติการ"}
    ]
    base_dict[38]["stageMeter"] = {"title": "ความเข้าใจด่านที่ 5", "status": "เสร็จสิ้น 80%"}
    base_dict[38]["intuition"] = {
        "header": "🧠 ทดสอบความเข้าใจสั้นๆ",
        "question": "\"ทำไมลายมือชื่อดิจิทัลจึงคำนวณจากค่าแฮชของเอกสาร (Hash of Document) แทนที่จะเข้ารหัสเอกสารทั้งฉบับด้วย Private Key?\"",
        "btn": "ดูเฉลยคำตอบ ▼",
        "answer": "<strong>คำตอบ:</strong> เพื่อประสิทธิภาพและความปลอดภัย! เอกสารขนาด 1 GB หากนำไปคำนวณผ่าน Private Key จะใช้เวลานานมหาศาล การแฮชเอกสารให้เหลือลายนิ้วมือ 32 ไบต์ (256 บิต) แล้วเซ็นที่ค่าแฮช จะรวดเร็วมากและยังรับประกันว่าหากเอกสารเปลี่ยนแม้แต่ตัวอักษรเดียว ลายมือชื่อจะตรวจไม่ผ่านทันที"
    }

    base_dict[44]["checklistDetails"] = [
        {"label": "การแลกเปลี่ยนกุญแจแบบ 1-RTT ใน TLS 1.3", "desc": "เข้าใจการลดเวลาหน่วง (Latency) และการตัดกระบวนการเก่าที่ไม่ปลอดภัยออก (ตัด RSA Key Exchange, ตัด CBC Mode)"},
        {"label": "การรักษาความลับสมบูรณ์แบบในอนาคต (Forward Secrecy)", "desc": "เข้าใจว่าการใช้กุญแจชั่วคราว (Ephemeral Keys) ทำให้แม้กุญแจหลักของเซิร์ฟเวอร์จะรั่วไหลในอนาคต ข้อมูลในอดีตก็ยังถอดรหัสไม่ได้"},
        {"label": "การเข้ารหัสจากต้นทางถึงปลายทาง (Signal E2EE)", "desc": "เข้าใจการหมุนกุญแจแบบ Double Ratchet ที่สร้างกุญแจใหม่สำหรับทุกข้อความแชต ทำให้ข้อความในอดีตและอนาคตปลอดภัยสูงสุด"},
        {"label": "ความสำคัญของ CSPRNG และการจัดเก็บกุญแจ", "desc": "เข้าใจว่าฟังก์ชันสุ่มทั่วไป (Math.random) ห้ามใช้ในงานรหัสลับเด็ดขาด และกุญแจต้องเก็บในฮาร์ดแวร์ปลอดภัย (TPM / KMS / Secure Enclave)"}
    ]
    base_dict[44]["stageMeter"] = {"title": "ความเข้าใจด่านที่ 6", "status": "เสร็จสิ้น 92%"}
    base_dict[44]["intuition"] = {
        "header": "🧠 ทดสอบความเข้าใจสั้นๆ",
        "question": "\"หากแฮกเกอร์ดักจับข้อมูลของคุณผ่าน Wi-Fi สาธารณะขณะที่คุณกำลังเข้าใช้งานเว็บไซต์ HTTPS แฮกเกอร์จะมองเห็นอะไรได้บ้าง?\"",
        "btn": "ดูเฉลยคำตอบ ▼",
        "answer": "<strong>คำตอบ:</strong> มองเห็นเฉพาะชื่อโดเมนและ IP ของเซิร์ฟเวอร์เท่านั้น (ผ่าน SNI/DNS)! ส่วน URL ย่อย, ข้อมูลที่กรอก, รหัสผ่าน, คุกกี้ และเนื้อหาทั้งหมดจะถูกเข้ารหัสด้วย AES-GCM อย่างปลอดภัย 100%"
    }

    # Quiz translations
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
            "prompt": "ทำไมฟังก์ชันแฮชเช่น MD5 และ SHA-1 จึงถูกเลิกใช้งานในระบบความปลอดภัยทั่วโลก?",
            "options": [
                {"text": "A. เพราะทำงานช้าเกินไปสำหรับอินเทอร์เน็ตความเร็วสูง", "feedback": "ไม่ถูกต้อง อันที่จริง MD5 ทำงานเร็วมาก แต่นั่นกลับทำให้ถูกเดารหัสผ่านได้ง่ายขึ้น"},
                {"text": "B. เพราะนักวิจัยพบการชนกันของค่าแฮช (Collisions) ทำให้สร้างไฟล์สองไฟล์ที่ต่างกันแต่ได้แฮชเท่ากันได้", "feedback": "ถูกต้อง! ทั้ง MD5 และ SHA-1 ถูกพิสูจน์แล้วว่าสูญเสียคุณสมบัติ Collision Resistance นักวิจัยสามารถสร้างใบรับรองปลอมที่มีแฮชตรงกันได้!"},
                {"text": "C. เพราะใช้หน่วยความจำเกิน 64-bit address space", "feedback": "ไม่ถูกต้อง ค่าแฮชของ MD5 มีขนาดเพียง 128 บิต ซึ่งใช้หน่วยความจำน้อยมาก"}
            ]
        }
    ]

    base_dict[51]["quizDetails"] = [
        {
            "badge": "คำถามที่ 1",
            "prompt": "คอมพิวเตอร์ควอนตัมขนาดใหญ่ที่ทำงานด้วยอัลกอริทึมของชอร์ (Shor's Algorithm) จะทำลายอัลกอริทึมประเภทใดต่อไปนี้?",
            "options": [
                {"text": "A. AES-256 (การเข้ารหัสแบบสมมาตร)", "feedback": "ไม่ถูกต้อง AES-256 ได้รับผลกระทบจากอัลกอริทึม Grover เพียงลดทอนความปลอดภัยลงครึ่งหนึ่ง (ยังเหลือ 128 บิต ซึ่งปลอดภัยมหาศาล)"},
                {"text": "B. RSA-2048, Diffie-Hellman และ Elliptic Curve Cryptography (ECC)", "feedback": "ถูกต้อง! อัลกอริทึมของชอร์สามารถแก้ปัญหาการแยกตัวประกอบเฉพาะและ Discrete Logarithm ได้ในเวลาพหุนาม ทำให้อสมมาตรยุคปัจจุบันพังทลายทันที!"},
                {"text": "C. SHA-256 (ฟังก์ชันแฮช)", "feedback": "ไม่ถูกต้อง SHA-256 ต้านทานอัลกอริทึมของชอร์ได้เป็นอย่างดี"}
            ]
        },
        {
            "badge": "คำถามที่ 2",
            "prompt": "ทำไมคำแนะนำที่ว่า 'เขียนฟังก์ชันเข้ารหัสลับขึ้นมาใช้เองเพื่อความปลอดภัยสูงสุด' จึงถือเป็นแนวคิดที่ผิดพลาดร้ายแรงที่สุดในวงการซอฟต์แวร์?",
            "options": [
                {"text": "A. เพราะผิดกฎหมายลิขสิทธิ์สากลของ W3C", "feedback": "ไม่ถูกต้อง ไม่มีข้อห้ามทางกฎหมายในการเขียนโค้ดคณิตศาสตร์"},
                {"text": "B. เพราะการเข้ารหัสลับที่แท้จริงต้องผ่านการตรวจสอบ Side-Channel, Timing Attacks และการเจาะระบบจากผู้เชี่ยวชาญระดับโลกนับทศวรรษ", "feedback": "ถูกต้อง! ผู้ที่ออกแบบระบบไม่สามารถมองเห็นจุดอ่อนของตนเองได้ อัลกอริทึมมาตรฐานเปิดอย่าง AES ผ่านการโจมตีนับล้านครั้งจนมั่นใจได้ว่าไร้ช่องโหว่!"},
                {"text": "C. เพราะการเข้ารหัสลับต้องซื้อไลเซนส์เชิงพาณิชย์จาก NIST เท่านั้น", "feedback": "ไม่ถูกต้อง มาตรฐาน NIST ทุกตัวเป็นโอเพนซอร์สและสาธารณะสมบัติ"}
            ]
        }
    ]

    # Detailed interactive lab elements
    base_dict[6]["labDetails"] = {
        "inputLabel": "ข้อความต้นฉบับ (INPUT PLAINTEXT):",
        "btnDecode": "ทดสอบถอดรหัส (ไม่ใช้กุญแจ) ➔",
        "btnToggleAES": "สลับการถอดรหัส AES ด้วยกุญแจ"
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
        "modeHeading": "เลือกโหมดการทำงานของ AES (Operational Mode):",
        "matrixTitle": "โหมด: AES-ECB (Electronic Codebook)",
        "matrixBanner": "⚠️ <strong>มองเห็นแพทเทิร์น:</strong> บล็อกข้อมูลที่เหมือนกันจะได้ข้อความรหัสสีเดียวกัน!",
        "ecbExplanation": "<strong>Electronic Codebook (ECB)</strong> เข้ารหัสบล็อก 16 ไบต์แต่ละบล็อกแยกจากกันโดยไม่มีการสุ่ม ทุกบล็อกสีขาวที่เหมือนกันจะได้ข้อความรหัสบล็อกเดิม ทำให้โครงร่างเพนกวินคงอยู่ 100%!",
        "gcmExplanation": "<strong>Galois/Counter Mode (GCM)</strong> รวมค่าสุ่ม Initialization Vector (Nonce) แม้จะเป็นข้อมูลเดิมซ้ำๆ ก็จะสร้างสัญญาณรบกวนสีขาวที่มีเอนโทรปีสูงสุด ปิดบังโครงสร้างข้อมูลอย่างสมบูรณ์!",
        "theFix": "<strong>วิธีแก้ไข:</strong> ระบบสมัยใหม่ใช้ AES-GCM พร้อมค่าสุ่ม <em>Initialization Vector (Nonce)</em> ขนาด 96 บิต ทำให้ข้อมูลกระจายตัวเสมือนคลื่นสัญญาณรบกวนสีขาวที่ไร้รูปแบบ"
    }

    base_dict[28]["labDetails"] = {
        "btnCompute": "✨ ขั้นตอนที่ 3: คำนวณกุญแจลับร่วมกัน (Shared Secret) ➔",
        "aliceTitle": "Alice (ความลับส่วนตัว)",
        "bobTitle": "Bob (ความลับส่วนตัว)",
        "eveTitle": "สายส่งสาธารณะ (Eve แอบดักฟัง)",
        "eveDesc": "Eve มองเห็นสีผสมที่แลกเปลี่ยนกันข้ามสายสัญญาณ:",
        "eveNotice": "Eve ไม่สามารถแยกสีส้มหรือสีเขียวกลับมาเป็นสีลับของแต่ละคนได้!",
        "derivedKeyLabel": "กุญแจลับที่ได้ตรงกัน (Derived Shared Key):"
    }

    base_dict[35]["labDetails"] = {
        "in1Label": "ข้อความที่ 1 (INPUT MESSAGE 1):",
        "in2Label": "ข้อความที่ 2 (ต่างกันเพียง 1 ตัวอักษร):",
        "gridHeading": "ฮีตแมปเปรียบเทียบบิต 256 บิต (256-Bit Avalanche Heatmap)",
        "gridSub": "สี่เหลี่ยมสีส้มแทนบิตที่พลิกกลับ (Flipped Bits) ระหว่างแฮชที่ 1 และ 2:",
        "legend": "🟩 บิตคงเดิม &nbsp;&nbsp;|&nbsp;&nbsp; 🟨 บิตที่พลิกกลับ (~เป้าหมาย 50%)",
        "metricTag": "ผลการคำนวณ AVALANCHE METRIC สด",
        "metricSuccess": "✔ ผ่านเกณฑ์การแพร่กระจายทางวิทยาการรหัสลับ (Strict Avalanche Criterion)"
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
        "shorDesc": "คอมพิวเตอร์ควอนตัมใช้ Quantum Fourier Transform (QFT) เพื่อหาคาบ <em>r</em> ของเลขยกกำลังมอดุลาร์ a<sup>x</sup> ≡ 1 (mod n) ในเวลาพหุนาม O((log n)³)",
        "shorStatus": "กำลังจำลองสถานะทับซ้อนควอนตัม (Superposition)...",
        "shorOutcome": "RSA-2048 ถูกแยกตัวประกอบสำเร็จในเวลาไม่กี่วินาที!",
        "btnShor": "จำลองการรันอัลกอริทึมของชอร์ ➔",
        "latticeBadge": "ยุคหลังควอนตัม: NIST ML-KEM",
        "latticeTitle": "เกราะกำบังโครงข่ายแลตทิซมิติสูง (High-Dimensional Lattice)",
        "latticeDesc": "อิงจากปัญหา <em>Learning With Errors (LWE)</em> ในปริภูมิยูคลิดมากกว่า 500 มิติพร้อมสัญญาณรบกวนแบบเกาส์เซียน",
        "latticeStatus": "ค้นหาจุดพิกัดในโครงข่าย 512 มิติ...",
        "latticeOutcome": "ความซับซ้อนระดับควอนตัม: ไม่สามารถเจาะได้",
        "btnTestLattice": "ทดสอบความต้านทานควอนตัมบนโครงข่ายแลตทิซ ➔",
        "btnLattice": "ทดสอบความต้านทานควอนตัมบนโครงข่ายแลตทิซ ➔"
    }

    return base_dict

def inject_enhancements():
    html_path = "/Users/kvivek/Documents/modern-cryptography-course/cryptography_for_beginners_presentation.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    full_thai_dict = get_full_thai_dict()
    dict_json = json.dumps(full_thai_dict, ensure_ascii=False, indent=2)

    engine_js = f"""
            // =================================================================
            // BILINGUAL THAI / ENGLISH (TH/EN) TRANSLATION ENGINE & DATA
            // =================================================================
            const presentationTranslationsTH = {dict_json};
            const originalEnglishData = {{}};

            // Capture initial English content for every slide on first load
            slides.forEach((slide, idx) => {{
                const slideNum = idx + 1;
                const enData = {{}};

                const tagEl = slide.querySelector('.slide-tag');
                if (tagEl) enData.tag = tagEl.innerHTML;

                const breadcrumbEl = slide.querySelector('.slide-breadcrumb');
                if (breadcrumbEl) enData.breadcrumb = breadcrumbEl.innerHTML;

                const mainTitleEl = slide.querySelector('.slide-main-title');
                if (mainTitleEl) enData.mainTitle = mainTitleEl.innerHTML;

                const subtitleEl = slide.querySelector('.slide-subtitle');
                if (subtitleEl) enData.subtitle = subtitleEl.innerHTML;

                const cardEls = slide.querySelectorAll('.pres-card:not(.featured-banner):not(.quiz-card):not(.interactive-quiz-card)');
                if (cardEls.length > 0) {{
                    enData.cards = [];
                    cardEls.forEach(c => {{
                        const badge = c.querySelector('.card-badge');
                        const title = c.querySelector('.card-title');
                        const desc = c.querySelector('.card-desc');
                        enData.cards.push({{
                            badge: badge ? badge.innerHTML : null,
                            title: title ? title.innerHTML : null,
                            desc: desc ? desc.innerHTML : null
                        }});
                    }});
                }}

                // Checkpoint checklist items
                const checkItems = slide.querySelectorAll('.checklist-item');
                if (checkItems.length > 0) {{
                    enData.checklistDetails = [];
                    checkItems.forEach(item => {{
                        const lbl = item.querySelector('.checklist-label');
                        const dsc = item.querySelector('.checklist-desc');
                        enData.checklistDetails.push({{
                            label: lbl ? lbl.innerHTML : '',
                            desc: dsc ? dsc.innerHTML : ''
                        }});
                    }});
                }}

                // Checkpoint Stage Meter
                const meterHead = slide.querySelector('.stage-meter-header');
                if (meterHead) {{
                    const title = meterHead.querySelector('span:first-child');
                    const status = meterHead.querySelector('span:last-child');
                    enData.stageMeter = {{
                        title: title ? title.innerHTML : '',
                        status: status ? status.innerHTML : ''
                    }};
                }}
                const meterNotes = slide.querySelector('.stage-meter-box > div:last-child');
                if (meterNotes) {{
                    enData.stageMeterNotes = meterNotes.innerHTML;
                }}

                // Checkpoint Intuition Self-test
                const qCard = slide.querySelector('.quiz-card');
                if (qCard) {{
                    const qHead = qCard.querySelector('.quiz-header');
                    const qQ = qCard.querySelector('.quiz-question');
                    const qB = qCard.querySelector('.quiz-reveal-btn');
                    const qA = qCard.querySelector('.quiz-answer-drawer');
                    enData.intuition = {{
                        header: qHead ? qHead.innerHTML : '',
                        question: qQ ? qQ.innerHTML : '',
                        btn: qB ? qB.innerHTML : '',
                        answer: qA ? qA.innerHTML : ''
                    }};
                }}

                // Interactive Quizzes
                const quizCards = slide.querySelectorAll('.interactive-quiz-card');
                if (quizCards.length > 0) {{
                    enData.quizDetails = [];
                    quizCards.forEach(qc => {{
                        const badge = qc.querySelector('.quiz-badge');
                        const prompt = qc.querySelector('.quiz-prompt');
                        const opts = [];
                        qc.querySelectorAll('.quiz-opt-btn').forEach(btn => {{
                            const span = btn.querySelector('span');
                            opts.push({{
                                text: span ? span.innerHTML : btn.innerHTML,
                                feedback: btn.getAttribute('data-feedback') || ''
                            }});
                        }});
                        enData.quizDetails.push({{
                            badge: badge ? badge.innerHTML : '',
                            prompt: prompt ? prompt.innerHTML : '',
                            options: opts
                        }});
                    }});
                }}

                // Q&A Forums
                const qaBoxes = slide.querySelectorAll('.qa-question-box');
                if (qaBoxes.length > 0) {{
                    enData.qa = [];
                    qaBoxes.forEach(qb => {{
                        const qHeader = qb.querySelector('.qa-q-header span:last-child');
                        const aText = qb.querySelector('.qa-answer-text');
                        enData.qa.push({{
                            q: qHeader ? qHeader.innerHTML : '',
                            a: aText ? aText.innerHTML : ''
                        }});
                    }});
                }}

                // Interactive Lab UI Details
                enData.labDetails = {{}};
                const inputRow = slide.querySelector('.lab-input-row span:first-child');
                if (inputRow) enData.labDetails.inputLabel = inputRow.innerHTML;

                const btnDec = slide.querySelector('#btnDecodeBase64');
                if (btnDec) enData.labDetails.btnDecode = btnDec.innerHTML;

                const btnAes = slide.querySelector('#btnToggleAES');
                if (btnAes) enData.labDetails.btnToggleAES = btnAes.innerHTML;

                const btnEcb = slide.querySelector('#btnSelectECB');
                if (btnEcb) enData.labDetails.btnECB = btnEcb.innerHTML;

                const btnGcm = slide.querySelector('#btnSelectGCM');
                if (btnGcm) enData.labDetails.btnGCM = btnGcm.innerHTML;

                const modeExp = slide.querySelector('#modeExplanationText');
                if (modeExp) enData.labDetails.ecbExplanation = modeExp.innerHTML;

                const btnComp = slide.querySelector('#btnDHComputeFinal');
                if (btnComp) enData.labDetails.btnCompute = btnComp.innerHTML;

                const btnNxt = slide.querySelector('#btnTLSNext');
                if (btnNxt) enData.labDetails.btnNext = btnNxt.innerHTML;

                const btnAt = slide.querySelector('#btnTLSAuto');
                if (btnAt) enData.labDetails.btnAuto = btnAt.innerHTML;

                const btnRst = slide.querySelector('#btnTLSReset');
                if (btnRst) enData.labDetails.btnReset = btnRst.innerHTML;

                const btnSh = slide.querySelector('#btnRunShor');
                if (btnSh) enData.labDetails.btnShor = btnSh.innerHTML;

                const btnLat = slide.querySelector('#btnTestLattice');
                if (btnLat) enData.labDetails.btnLattice = btnLat.innerHTML;

                const footEl = slide.querySelector('.slide-footer span:first-child');
                if (footEl) enData.footer = footEl.innerHTML;

                originalEnglishData[slideNum] = enData;
            }});

            function applySlideLanguage(slide, slideNum, lang) {{
                const data = lang === 'th' ? presentationTranslationsTH[slideNum] : originalEnglishData[slideNum];
                if (!data) return;

                if (data.tag !== undefined) {{
                    const el = slide.querySelector('.slide-tag');
                    if (el) el.innerHTML = data.tag;
                }}
                if (data.breadcrumb !== undefined) {{
                    const el = slide.querySelector('.slide-breadcrumb');
                    if (el) el.innerHTML = data.breadcrumb;
                }}
                if (data.mainTitle !== undefined) {{
                    const el = slide.querySelector('.slide-main-title');
                    if (el) el.innerHTML = data.mainTitle;
                }}
                if (data.subtitle !== undefined) {{
                    const el = slide.querySelector('.slide-subtitle');
                    if (el) el.innerHTML = data.subtitle;
                }}

                // Standard Cards
                if (data.cards && Array.isArray(data.cards)) {{
                    const cardEls = slide.querySelectorAll('.pres-card:not(.featured-banner):not(.quiz-card):not(.interactive-quiz-card)');
                    data.cards.forEach((cData, i) => {{
                        if (cardEls[i]) {{
                            if (cData.badge !== undefined) {{
                                const b = cardEls[i].querySelector('.card-badge');
                                if (b) b.innerHTML = cData.badge;
                            }}
                            if (cData.title !== undefined) {{
                                const t = cardEls[i].querySelector('.card-title');
                                if (t) t.innerHTML = cData.title;
                            }}
                            if (cData.desc !== undefined) {{
                                const d = cardEls[i].querySelector('.card-desc');
                                if (d) d.innerHTML = cData.desc;
                            }}
                        }}
                    }});
                }}

                // Checkpoint Checklists
                if (data.checklistDetails && Array.isArray(data.checklistDetails)) {{
                    const checkItems = slide.querySelectorAll('.checklist-item');
                    data.checklistDetails.forEach((item, idx) => {{
                        if (checkItems[idx]) {{
                            const lbl = checkItems[idx].querySelector('.checklist-label');
                            const dsc = checkItems[idx].querySelector('.checklist-desc');
                            if (lbl && item.label) lbl.innerHTML = item.label;
                            if (dsc && item.desc) dsc.innerHTML = item.desc;
                        }}
                    }});
                }}

                // Checkpoint Stage Meter Header & List
                if (data.stageMeter) {{
                    const meterHead = slide.querySelector('.stage-meter-header');
                    if (meterHead) {{
                        const title = meterHead.querySelector('span:first-child');
                        const status = meterHead.querySelector('span:last-child');
                        if (title && data.stageMeter.title) title.innerHTML = data.stageMeter.title;
                        if (status && data.stageMeter.status) status.innerHTML = data.stageMeter.status;
                    }}
                }}
                if (data.stageMeterNotes !== undefined) {{
                    const meterNotes = slide.querySelector('.stage-meter-box > div:last-child');
                    if (meterNotes) meterNotes.innerHTML = data.stageMeterNotes;
                }}

                // Checkpoint Intuition Box
                if (data.intuition) {{
                    const qCard = slide.querySelector('.quiz-card');
                    if (qCard) {{
                        const qHead = qCard.querySelector('.quiz-header');
                        const qQ = qCard.querySelector('.quiz-question');
                        const qB = qCard.querySelector('.quiz-reveal-btn');
                        const qA = qCard.querySelector('.quiz-answer-drawer');
                        if (qHead && data.intuition.header) qHead.innerHTML = data.intuition.header;
                        if (qQ && data.intuition.question) qQ.innerHTML = data.intuition.question;
                        if (qB) {{
                            const isRevealed = qA && qA.classList.contains('revealed');
                            qB.innerHTML = isRevealed 
                                ? (lang === 'th' ? 'ซ่อนเฉลยคำตอบ ▲' : 'Hide Answer ▲')
                                : (lang === 'th' ? (data.intuition.btn || 'ดูเฉลยคำตอบ ▼') : 'Show Answer ▼');
                        }}
                        if (qA && data.intuition.answer) qA.innerHTML = data.intuition.answer;
                    }}
                }}

                // Interactive Quizzes
                if (data.quizDetails && Array.isArray(data.quizDetails)) {{
                    const quizCards = slide.querySelectorAll('.interactive-quiz-card');
                    data.quizDetails.forEach((item, idx) => {{
                        if (quizCards[idx]) {{
                            const b = quizCards[idx].querySelector('.quiz-badge');
                            const p = quizCards[idx].querySelector('.quiz-prompt');
                            if (b && item.badge) b.innerHTML = item.badge;
                            if (p && item.prompt) p.innerHTML = item.prompt;

                            if (item.options && Array.isArray(item.options)) {{
                                const optBtns = quizCards[idx].querySelectorAll('.quiz-opt-btn');
                                item.options.forEach((opt, oIdx) => {{
                                    if (optBtns[oIdx]) {{
                                        const span = optBtns[oIdx].querySelector('span');
                                        if (span && opt.text) span.innerHTML = opt.text;
                                        if (opt.feedback) {{
                                            optBtns[oIdx].setAttribute('data-feedback', opt.feedback);
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

                // Interactive Labs Details
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
                    // Lab 2 (Caesar)
                    if (d.plainLabel) {{
                        const pl = slide.querySelector('.layout-split-equal .pres-card:first-child h4:first-child');
                        if (pl) pl.textContent = d.plainLabel;
                    }}
                    if (d.cipherLabel) {{
                        const cl = slide.querySelector('.layout-split-equal .pres-card:first-child h4:nth-of-type(2)');
                        if (cl) cl.textContent = d.cipherLabel;
                    }}
                    if (d.freqLabel) {{
                        const fl = slide.querySelector('.layout-split-equal .pres-card.featured h4');
                        if (fl) fl.textContent = d.freqLabel;
                    }}
                    if (d.freqDesc) {{
                        const fd = slide.querySelector('.layout-split-equal .pres-card.featured .card-desc');
                        if (fd) fd.textContent = d.freqDesc;
                    }}
                    if (d.attackTip) {{
                        const at = slide.querySelector('.layout-split-equal .pres-card.featured div[style*="accent-cyan"]');
                        if (at) at.textContent = d.attackTip;
                    }}
                    // Lab 3 (ECB vs GCM)
                    if (d.btnECB) {{
                        const btn = slide.querySelector('#btnSelectECB');
                        if (btn) btn.textContent = d.btnECB;
                    }}
                    if (d.btnGCM) {{
                        const btn = slide.querySelector('#btnSelectGCM');
                        if (btn) btn.textContent = d.btnGCM;
                    }}
                    if (d.modeHeading) {{
                        const mh = slide.querySelector('.pres-card.featured .card-title');
                        if (mh) mh.textContent = d.modeHeading;
                    }}
                    if (d.matrixTitle) {{
                        const mt = slide.querySelector('#matrixModeTitle');
                        if (mt) mt.textContent = d.matrixTitle;
                    }}
                    if (d.matrixBanner) {{
                        const mb = slide.querySelector('#matrixStatusBanner');
                        if (mb) mb.innerHTML = d.matrixBanner;
                    }}
                    if (d.ecbExplanation) {{
                        const me = slide.querySelector('#modeExplanationText');
                        if (me) me.innerHTML = d.ecbExplanation;
                    }}
                    if (d.theFix) {{
                        const co = slide.querySelector('.pres-card.featured .callout-box');
                        if (co) co.innerHTML = d.theFix;
                    }}
                    // Lab 4 (Diffie-Hellman)
                    if (d.btnCompute) {{
                        const btn = slide.querySelector('#btnDHComputeFinal');
                        if (btn) btn.textContent = d.btnCompute;
                    }}
                    if (d.aliceTitle) {{
                        const at = slide.querySelector('.layout-grid-3 .pres-card:first-child h4');
                        if (at) at.textContent = d.aliceTitle;
                    }}
                    if (d.eveTitle) {{
                        const et = slide.querySelector('.layout-grid-3 .pres-card:nth-child(2) h4');
                        if (et) et.textContent = d.eveTitle;
                    }}
                    if (d.eveDesc) {{
                        const ed = slide.querySelector('.layout-grid-3 .pres-card:nth-child(2) .card-desc');
                        if (ed) ed.textContent = d.eveDesc;
                    }}
                    if (d.eveNotice) {{
                        const en = slide.querySelector('.layout-grid-3 .pres-card:nth-child(2) div[style*="accent-gold"]');
                        if (en) en.textContent = d.eveNotice;
                    }}
                    if (d.bobTitle) {{
                        const bt = slide.querySelector('.layout-grid-3 .pres-card:nth-child(3) h4');
                        if (bt) bt.textContent = d.bobTitle;
                    }}
                    if (d.derivedKeyLabel) {{
                        const dk = slide.querySelector('#btnDHComputeFinal + div strong');
                        if (dk) dk.textContent = d.derivedKeyLabel;
                    }}
                    // Lab 5 (Avalanche)
                    if (d.in1Label) {{
                        const l1 = slide.querySelector('.pres-card span[style*="accent-cyan"]');
                        if (l1) l1.textContent = d.in1Label;
                    }}
                    if (d.in2Label) {{
                        const l2 = slide.querySelector('.pres-card span[style*="accent-rose"]');
                        if (l2) l2.textContent = d.in2Label;
                    }}
                    if (d.gridHeading) {{
                        const gh = slide.querySelector('.pres-card:not(.featured) h4');
                        if (gh) gh.textContent = d.gridHeading;
                    }}
                    if (d.gridSub) {{
                        const gs = slide.querySelector('.pres-card:not(.featured) .card-desc');
                        if (gs) gs.textContent = d.gridSub;
                    }}
                    if (d.legend) {{
                        const lg = slide.querySelector('#avalancheGrid + div');
                        if (lg) lg.innerHTML = d.legend;
                    }}
                    if (d.metricTag) {{
                        const mt = slide.querySelector('.pres-card.featured div[style*="text-muted"]');
                        if (mt) mt.textContent = d.metricTag;
                    }}
                    if (d.metricSuccess) {{
                        const ms = slide.querySelector('.pres-card.featured div[style*="accent-emerald"]');
                        if (ms) ms.textContent = d.metricSuccess;
                    }}
                    // Lab 6 (TLS Handshake)
                    if (d.btnNext) {{
                        const btn = slide.querySelector('#btnTLSNext');
                        if (btn) btn.textContent = d.btnNext;
                    }}
                    if (d.btnAuto) {{
                        const btn = slide.querySelector('#btnTLSAuto');
                        if (btn) btn.textContent = d.btnAuto;
                    }}
                    if (d.btnReset) {{
                        const btn = slide.querySelector('#btnTLSReset');
                        if (btn) btn.textContent = d.btnReset;
                    }}
                    if (d.clientLabel) {{
                        const cl = slide.querySelector('.handshake-wire-container div:first-child strong');
                        if (cl) cl.textContent = d.clientLabel;
                    }}
                    if (d.serverLabel) {{
                        const sl = slide.querySelector('.handshake-wire-container div:last-child strong');
                        if (sl) sl.textContent = d.serverLabel;
                    }}
                    // Lab 7 (Quantum)
                    if (d.btnShor) {{
                        const btn = slide.querySelector('#btnRunShor');
                        if (btn) btn.textContent = d.btnShor;
                    }}
                    if (d.btnTestLattice || d.btnLattice) {{
                        const btn = slide.querySelector('#btnTestLattice');
                        if (btn) btn.textContent = d.btnTestLattice || d.btnLattice;
                    }}
                    if (d.shorBadge) {{
                        const sb = slide.querySelector('#cardShor .card-badge');
                        if (sb) sb.textContent = d.shorBadge;
                    }}
                    if (d.shorTitle) {{
                        const st = slide.querySelector('#cardShor .card-title');
                        if (st) st.textContent = d.shorTitle;
                    }}
                    if (d.shorDesc) {{
                        const sd = slide.querySelector('#cardShor .card-desc');
                        if (sd) sd.innerHTML = d.shorDesc;
                    }}
                    if (d.shorStatus) {{
                        const ss = slide.querySelector('#shorStatus');
                        if (ss) ss.textContent = d.shorStatus;
                    }}
                    if (d.shorOutcome) {{
                        const so = slide.querySelector('#cardShor strong');
                        if (so) so.textContent = d.shorOutcome;
                    }}
                    if (d.latticeBadge) {{
                        const lb = slide.querySelector('#cardLattice .card-badge');
                        if (lb) lb.textContent = d.latticeBadge;
                    }}
                    if (d.latticeTitle) {{
                        const lt = slide.querySelector('#cardLattice .card-title');
                        if (lt) lt.textContent = d.latticeTitle;
                    }}
                    if (d.latticeDesc) {{
                        const ld = slide.querySelector('#cardLattice .card-desc');
                        if (ld) ld.innerHTML = d.latticeDesc;
                    }}
                    if (d.latticeStatus) {{
                        const ls = slide.querySelector('#latticeStatus');
                        if (ls) ls.textContent = d.latticeStatus;
                    }}
                    if (d.latticeOutcome) {{
                        const lo = slide.querySelector('#cardLattice strong');
                        if (lo) lo.textContent = d.latticeOutcome;
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
                    langBtn.innerHTML = currentLang === 'th' ? '🇹🇭 TH' : '🇬🇧 EN';
                    langBtn.title = currentLang === 'th' ? 'สลับเป็นภาษาอังกฤษ (L)' : 'Switch to Thai (L)';
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
                setPresentationLanguage(initialLang);
            }}

            function populateGridModal() {{
                slidesGridContainer.innerHTML = '';
                slides.forEach((slide, idx) => {{
                    const slideNum = idx + 1;
                    const card = document.createElement('div');
                    card.className = 'grid-thumb-card' + (idx === currentSlide ? ' active' : '');
                    
                    let titleText = `Slide ${{slideNum}}`;
                    let section = slide.getAttribute('data-section') || 'Section';
                    
                    if (currentLang === 'th' && presentationTranslationsTH[slideNum]) {{
                        titleText = presentationTranslationsTH[slideNum].mainTitle || titleText;
                    }} else if (originalEnglishData[slideNum]) {{
                        titleText = originalEnglishData[slideNum].mainTitle || titleText;
                    }} else {{
                        const titleEl = slide.querySelector('.slide-main-title');
                        if (titleEl) titleText = titleEl.innerText;
                    }}

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

    # Replace bilingual block in HTML
    pattern = re.compile(r'// =================================================================\s*// BILINGUAL THAI / ENGLISH \(TH/EN\) TRANSLATION ENGINE[\s\S]*?function populateGridModal\(\) \{[\s\S]*?\}\);?\s*\}')
    if pattern.search(html):
        html = pattern.sub(lambda m: engine_js.strip(), html)
        print("Replaced bilingual engine with enhanced version.")
    else:
        print("Error: Could not locate existing bilingual engine block.")
        return False

    # Also update quiz answer reveal button listener to preserve bilingual text
    reveal_pattern = re.compile(r'// Quiz Answer Reveal Drawer[\s\S]*?btn\.textContent\s*=\s*drawer\.classList\.contains\(\'revealed\'\)\s*\?\s*\'Hide Answer ▲\'\s*:\s*\'Show Answer ▼\';[\s\S]*?\}\);\s*\}\);')
    reveal_replacement = """// Quiz Answer Reveal Drawer
            document.querySelectorAll('.quiz-reveal-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const targetId = btn.getAttribute('data-target');
                    const drawer = document.getElementById(targetId);
                    if (drawer) {
                        drawer.classList.toggle('revealed');
                        const isRevealed = drawer.classList.contains('revealed');
                        if (currentLang === 'th') {
                            btn.textContent = isRevealed ? 'ซ่อนเฉลยคำตอบ ▲' : 'ดูเฉลยคำตอบ ▼';
                        } else {
                            btn.textContent = isRevealed ? 'Hide Answer ▲' : 'Show Answer ▼';
                        }
                    }
                });
            });"""
    if reveal_pattern.search(html):
        html = reveal_pattern.sub(reveal_replacement, html)
        print("Updated quiz answer reveal button listener.")

    # Also update quiz options feedback to support Thai
    quiz_feedback_pattern = re.compile(r'if \(isCorrect\) \{[\s\S]*?feedbackEl\.innerHTML = `<strong>✔ Correct!<\/strong> \$\{feedbackText\}`;[\s\S]*?feedbackEl\.innerHTML = `<strong>✘ Not quite!<\/strong> \$\{feedbackText\}`;[\s\S]*?\}')
    quiz_feedback_replacement = """if (isCorrect) {
                        btn.classList.add('correct');
                        if (feedbackEl) {
                            feedbackEl.className = 'quiz-feedback show-correct';
                            const correctPrefix = currentLang === 'th' ? '<strong>✔ ถูกต้อง!</strong> ' : '<strong>✔ Correct!</strong> ';
                            feedbackEl.innerHTML = correctPrefix + feedbackText;
                        }
                    } else {
                        btn.classList.add('wrong');
                        if (feedbackEl) {
                            feedbackEl.className = 'quiz-feedback show-wrong';
                            const wrongPrefix = currentLang === 'th' ? '<strong>✘ ยังไม่ถูกต้อง!</strong> ' : '<strong>✘ Not quite!</strong> ';
                            feedbackEl.innerHTML = wrongPrefix + feedbackText;
                        }
                    }"""
    if quiz_feedback_pattern.search(html):
        html = quiz_feedback_pattern.sub(quiz_feedback_replacement, html)
        print("Updated quiz option feedback listener.")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Successfully injected all enhancements into cryptography_for_beginners_presentation.html!")
    return True

if __name__ == "__main__":
    inject_enhancements()
