# 🎓 CS-4XX / ECE-4XX การเข้ารหัสขั้นสูงและความปลอดภัยของเครือข่าย (Modern Cryptography & Network Security)
## ใบงานและการบ้านปฏิบัติการประจำวิชา: เนื้อหาวันที่ 1–3 (Class Assignment: Days 1–3)
**การวิเคราะห์ถอดรหัสลับแบบคลาสสิก, รหัสลับสมมาตรยุคใหม่ และระบบการเข้ารหัสกุญแจสาธารณะ**  
*(Classical Cryptanalysis, Modern Symmetric Ciphers & Public-Key Cryptosystems)*

* 🌐 **ภาษา:** [🇹🇭 ภาษาไทย (Thai)](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_DAYS_1_TO_3_TH.md) | [🇺🇸 English Version](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_DAYS_1_TO_3.md)
* **ระดับการศึกษา:** นักศึกษาปริญญาตรีชั้นปีที่ 3-4 / ปริญญาโท (สาขาวิชาวิทยาการคอมพิวเตอร์ และวิศวกรรมคอมพิวเตอร์)
* **ช่วงเวลาที่มอบหมาย:** วันที่ 3 (หลังจบบทเรียน Public-Key Cryptography & RSA)
* **กำหนดส่ง (Due Date):** วันอาทิตย์ เวลา 23:59:59 น. (7 วันหลังจากวันที่มอบหมาย)
* **คะแนนเต็ม:** 100 คะแนน (+ 15 คะแนนพิเศษ Bonus / Extra Credit)
* **ไฟล์โค้ดเริ่มต้นสำหรับนักศึกษา (Starter Code):** [`assignments/assignment_days_1_to_3_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_days_1_to_3_student.py)
* **เทมเพลตรายงานผล (Report Template):** [`assignments/REPORT_TEMPLATE_TH.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_TH.md) (หรือ [`REPORT_TEMPLATE.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE.md))
* **สคริปต์ตรวจสอบและรวมไฟล์ส่ง (Submission Validator):** [`assignments/submit_check.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/submit_check.py)

---

## 🎯 วัตถุประสงค์และภาพรวมการเรียนรู้ (Executive Summary & Learning Objectives)

ใบงานนี้เป็นการบูรณาการองค์ความรู้ทางคณิตศาสตร์, การสร้างโครงสร้างรหัสลับสมมาตร (Symmetric Cryptography) และระบบดักทางฟังก์ชันทางเดียวแบบกุญแจสาธารณะ (Asymmetric Trapdoor Systems) ที่ได้ศึกษาใน **วันที่ 1, 2 และ 3** ของหลักสูตร โดยนักศึกษาจะได้สวมบทบาทเป็นทั้ง **วิศวกรออกแบบโพรโทคอลรหัสลับ (Cryptographic Protocol Engineer)** และ **นักวิเคราะห์เจาะระบบถอดรหัสลับ (Offensive Cryptanalyst)**

เมื่อสำเร็จใบงานนี้นักศึกษาจะมีความเชี่ยวชาญในด้าน:
1. **รากฐานดั้งเดิมและความปลอดภัยเชิงทฤษฎีสารสนเทศ (Day 1):** การพิสูจน์ภาวะความลับสมบูรณ์แบบของแชนนอน (Shannon's Perfect Secrecy), การคำนวณสถิติไคสแควร์ ($\chi^2$), การวัดดัชนีความบังเอิญ (Index of Coincidence - IC) และการถอดรหัสการใช้คีย์ซ้ำ Two-Time Pad ด้วยวิธี Crib Dragging
2. **พีชคณิตนามธรรม, ทฤษฎีจำนวน และบล็อกไซเฟอร์ (Day 2):** การพัฒนาขั้นตอนวิธียุคลิดส่วนขยาย (Extended Euclidean Algorithm), การหาตัวผกผันมอดุโล (Modular Inverse), การยกกำลังมอดุโลแบบเร็ว (Square-and-Multiply), การเปรียบเทียบโหมดของ AES (ECB vs CBC vs GCM) และการโจมตีถอดรหัสจากช่องโหว่ AES-GCM Nonce Reuse
3. **ระบบรหัสลับกุญแจสาธารณะและความมั่นคงปลอดภัย (Day 3):** การจำลองโพรโทคอล Diffie-Hellman Key Exchange (DHKE), การสร้างระบบ RSA จากศูนย์ (Scratch), การวิเคราะห์ความปลอดภัยเชิงความหมาย (IND-CPA) และช่องโหว่ความดัดแปลงได้ (Malleability), การโจมตีแยกตัวประกอบของแฟร์มาต์ (Fermat's Factorization Attack) และการแลกเปลี่ยนคีย์สมัยใหม่ด้วย Curve25519 (X25519) ECDH

---

## 📋 โครงสร้างคะแนนและการประเมินผล (Score Allocation)

| ส่วนที่ | หัวข้อและสิ่งที่ต้องส่ง | รูปแบบ | คะแนน |
| :--- | :--- | :--- | :---: |
| **ส่วนที่ 1** | **รากฐานทางคณิตศาสตร์และการพิสูจน์ทฤษฎี (Mathematical Foundations & Proofs)** | รายงานข้อเขียน (`REPORT.md`) | **30 คะแนน** |
| | • ข้อ 1.1: ความปลอดภัยเชิงทฤษฎีสารสนเทศและทฤษฎีบทของแชนนอน | การพิสูจน์สูตรคณิตศาสตร์ | 10 คะแนน |
| | • ข้อ 1.2: สถาปัตยกรรม AES และการวิเคราะห์ความปลอดภัยของโหมดไซเฟอร์ | บทวิเคราะห์ทางเทคนิค | 10 คะแนน |
| | • ข้อ 1.3: การพิสูจน์ความถูกต้องของ RSA ผ่าน CRT และการโจมตี Chosen-Ciphertext | การพิสูจน์สูตรคณิตศาสตร์ | 10 คะแนน |
| **ส่วนที่ 2** | **การเขียนโปรแกรมสร้างอัลกอริทึมจากศูนย์ (Core Implementation Tasks)** | ไฟล์โค้ด Python (`student.py`) | **40 คะแนน** |
| | • งาน 2.1: การเข้ารหัสและถอดรหัสซีซาร์อย่างง่าย (Caesar Encrypt & Decrypt) | ฟังก์ชัน Python | 8 คะแนน |
| | • งาน 2.2: การวิเคราะห์ทางสถิติ ($\chi^2$, IC และ Auto-Caesar) | ฟังก์ชัน Python | 8 คะแนน |
| | • งาน 2.3: พื้นฐานทฤษฎีจำนวน (Ext-GCD, ModInv, PowMod) | ฟังก์ชัน Python | 8 คะแนน |
| | • งาน 2.4: การเข้ารหัสลับแบบรับรองความถูกต้องสมัยใหม่ (AES-256-GCM AEAD) | ฟังก์ชัน Python | 8 คะแนน |
| | • งาน 2.5: เอนจิน RSA แบบสมบูรณ์ และ Curve25519 ECDH Key Exchange | ฟังก์ชัน Python | 8 คะแนน |
| **ส่วนที่ 3** | **การวิเคราะห์การโจมตีและการตอบสนองต่อเหตุการณ์ (Offensive Cryptanalysis)** | สคริปต์โจมตีและบทวิเคราะห์ | **30 คะแนน** |
| | • การโจมตี 3.1: การกู้คืน Keystream จาก Two-Time Pad ด้วยวิธี Crib Dragging | โค้ดโจมตีและถอดรหัส | 10 คะแนน |
| | • การโจมตี 3.2: การเจาะช่องโหว่ AES-GCM Nonce Reuse เพื่อกู้คืนข้อความลับ | โค้ดโจมตีและถอดรหัส | 10 คะแนน |
| | • การโจมตี 3.3: การโจมตีแยกตัวประกอบ Fermat Attack บนกุญแจ RSA ที่อ่อนแอ | โค้ดโจมตีและถอดรหัส | 10 คะแนน |
| **โบนัส** | **คะแนนพิเศษ: โปรแกรมถอดรหัส Vigenère อัตโนมัติ (Automated Vigenère Breaker)** | ฟังก์ชันโจมตีขั้นสูง | **+15 คะแนน** |
| **รวมทั้งสิ้น** | | | **100 คะแนน (+15)** |

---

# 📖 ส่วนที่ 1: รากฐานทางคณิตศาสตร์และการพิสูจน์ทฤษฎี (30 คะแนน)

ให้นักศึกษาเขียนคำตอบและการพิสูจน์อย่างละเอียดลงในไฟล์ [`assignments/REPORT_TEMPLATE_TH.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_TH.md) (หรือแปลงเป็น PDF ส่ง)

### ข้อ 1.1: ความปลอดภัยเชิงทฤษฎีสารสนเทศและทฤษฎีบทของแชนนอน (10 คะแนน)
1. **นิยามของ Perfect Secrecy:** โคลด แชนนอน (Claude Shannon, 1949) นิยามว่าระบบการเข้ารหัส $(\text{Gen}, \text{Enc}, \text{Dec})$ บนปริภูมิต้นฉบับ $\mathcal{M}$ และปริภูมิข้อความรหัส $\mathcal{C}$ จะบรรลุ *Perfect Secrecy (ความลับสมบูรณ์แบบ)* ก็ต่อเมื่อ:
   $$P(M = m \mid C = c) = P(M = m) \quad \forall m \in \mathcal{M}, \forall c \in \mathcal{C}$$
   จงใช้ **ทฤษฎีบทของเบย์ส (Bayes' Theorem)** พิสูจน์อย่างรัดกุมว่าระบบ One-Time Pad ($C = M \oplus K$ โดยที่ $K \leftarrow \{0, 1\}^L$ สุ่มอย่างเอกรูป) มีคุณสมบัติ Perfect Secrecy โดยแสดงขั้นตอนการคำนวณความน่าจะเป็นอย่างละเอียดทุกขั้นตอน (5 คะแนน)
2. **ขอบเขตล่างของขนาดกุญแจของแชนนอน (Shannon's Lower Bound):** จงพิสูจน์ว่าระบบรหัสลับใดๆ ที่บรรลุ Perfect Secrecy จะต้องมีขนาดของปริภูมิกุญแจ $|\mathcal{K}|$ ไม่น้อยกว่าขนาดของปริภูมิข้อความ $|\mathcal{M}|$ เสมอ ($|\mathcal{K}| \ge |\mathcal{M}|$) และอธิบายผลกระทบในทางวิศวกรรมจริงที่เรียกว่า **"ปัญหาความย้อนแย้งของการแจกจ่ายกุญแจ (Key Distribution Paradox)"** (5 คะแนน)

### ข้อ 1.2: สถาปัตยกรรม AES และการวิเคราะห์ความปลอดภัยของโหมดไซเฟอร์ (10 คะแนน)
1. **ความสับสน (Confusion) และการกระจาย (Diffusion) ใน AES:**
   * จงอธิบายว่าขั้นตอน **SubBytes** ให้คุณสมบัติ *Confusion* อย่างไร ผ่านการหาตัวผกผันแบบไม่เชิงเส้นบนสนามกาลัวส์ $\text{GF}(2^8)$ ตามด้วยการแปลงสัมพรรค (Affine Transformation)
   * จงอธิบายว่าขั้นตอน **ShiftRows** และ **MixColumns** ร่วมกันสร้าง *Diffusion* (ปรากฏการณ์หิมะถล่ม / Avalanche Effect) ได้อย่างไร และค่า Branch Number ของเมทริกซ์ MDS ใน MixColumns มีค่าเท่าใด? (4 คะแนน)
2. **ความล้มเหลวของโหมด Electronic Codebook (ECB) ต่อความปลอดภัย IND-CPA:**
   * จงนิยามรูปแบบการทดสอบความปลอดภัย **IND-CPA (Indistinguishability under Chosen-Plaintext Attack)** อย่างเป็นทางการระหว่างผู้โจมตี $\mathcal{A}$ กับผู้ท้าทาย (Challenger)
   * จงนำเสนอกลยุทธ์ของผู้โจมตีที่สามารถเอาชนะระบบเข้ารหัส AES-ECB ได้ด้วยความน่าจะเป็น $P(\text{Win}) = 1.0$ โดยใช้การสืบค้นเพียงครั้งเดียว (3 คะแนน)
3. **กลไกของ AES-GCM (Galois/Counter Mode):**
   * อธิบายว่า AES-GCM รวมการเข้ารหัสแบบ Counter Mode (CTR) เข้ากับการรับรองความถูกต้องด้วยพหุนาม GHASH บน $\text{GF}(2^{128})$ อย่างไร
   * อธิบายผลกระทบหายนะที่เกิดขึ้นเมื่อระบบ **นำค่าตัวแปรสุ่มใช้ครั้งเดียว 96 บิต (Nonce $N$) มาใช้ซ้ำ** กับข้อความที่ต่างกันภายใต้กุญแจ $K$ เดียวกัน ทั้งในแง่ของ **การสูญเสียความลับ (Confidentiality Breakdown)** ($C_1 \oplus C_2$) และ **การสูญเสียความถูกต้องสมบูรณ์ (Integrity Breakdown)** (การถอดรหัสกุญแจแฮช $H$) (3 คะแนน)

### ข้อ 1.3: การพิสูจน์ความถูกต้องของ RSA ผ่าน CRT และการโจมตี Chosen-Ciphertext (10 คะแนน)
1. **การพิสูจน์การถอดรหัสของ RSA:** กำหนดให้ $N = p \cdot q$ โดย $p, q$ เป็นจำนวนเฉพาะที่ไม่ซ้ำกัน และ $e \cdot d \equiv 1 \pmod{\phi(N)}$ โดย $\phi(N) = (p-1)(q-1)$  
   จงพิสูจน์ว่าสำหรับ **ทุกๆ** ข้อความ $M \in \mathbb{Z}_N$ (รวมถึงกรณีที่ $\gcd(M, N) > 1$):
   $$(M^e)^d \equiv M \pmod N$$
   *(คำแนะนำ: ประยุกต์ใช้ทฤษฎีบทเล็กของแฟร์มาต์มอดุโล $p$ และมอดุโล $q$ จากนั้นเชื่อมโยงด้วยทฤษฎีบทเศษเหลือของจีน Chinese Remainder Theorem - CRT)* (5 คะแนน)
2. **การโจมตี Chosen-Ciphertext Attack (CCA1) บน Textbook RSA:**
   * Textbook RSA มีลักษณะแบบดีเทอร์มินิสติก (Deterministic): $C = M^e \bmod N$
   * สมมติว่าผู้โจมตีดักจับข้อความรหัส $C = M^e \bmod N$ ได้ ผู้โจมตีไม่สามารถขอให้ออราเคิลถอดรหัส $C$ ตรงๆ ได้ แต่ได้รับอนุญาตให้ส่งข้อความรหัสอื่นใดๆ $C' \neq C$ ไปถอดรหัสได้ 1 ครั้ง
   * จงสร้างสูตรการโจมตีทางคณิตศาสตร์ที่ผู้โจมตีเลือกตัวสุ่มกำบังตา (Blinding Factor) $r \in \mathbb{Z}_N^*$ เพื่อสร้าง $C'$ และนำผลลัพธ์ $M' = \text{Dec}(C')$ มาคำนวณหา $M$ ดั้งเดิม
   * อธิบายว่าทำไมกลไกการเติมเต็มสมัยใหม่ **RSA-OAEP (Optimal Asymmetric Encryption Padding)** จึงสามารถป้องกันการโจมตีนี้ได้อย่างสมบูรณ์ (5 คะแนน)

---

# 💻 ส่วนที่ 2: งานเขียนโปรแกรมสร้างอัลกอริทึมจากศูนย์ (40 คะแนน)

เปิดไฟล์ [`assignments/assignment_days_1_to_3_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_days_1_to_3_student.py) และเติมโค้ดในฟังก์ชันที่มีสัญลักษณ์ `# TODO: YOUR CODE HERE`

### งาน 2.1: การเข้ารหัสและถอดรหัสซีซาร์อย่างง่าย (Caesar Encrypt & Decrypt) (8 คะแนน)
* `caesar_encrypt(plaintext: str, shift: int) -> str`: เข้ารหัสข้อความด้วยการเลื่อนตัวอักษรมอดุโล 26 ($C_i = (P_i + \text{shift}) \bmod 26$)
  * คงสถานะตัวพิมพ์ใหญ่และตัวพิมพ์เล็กตามเดิม (`'A'..'Z'` และ `'a'..'z'`)
  * ตัวอักษรที่ไม่ใช่ภาษาอังกฤษ (ช่องว่าง, เครื่องหมายวรรคตอน, ตัวเลข) จะต้องคงเดิมไม่เปลี่ยนแปลง
  * รองรับค่าเลื่อนที่มากกว่า 26 หรือค่าเลื่อนติดลบด้วยเลขคณิตมอดุโล
* `caesar_decrypt(ciphertext: str, shift: int) -> str`: ถอดรหัสข้อความซีซาร์โดยการย้อนกลับการเลื่อน ($P_i = (C_i - \text{shift}) \bmod 26$)

### งาน 2.2: การวิเคราะห์ทางสถิติและถอดรหัสซีซาร์อัตโนมัติ (8 คะแนน)
* `compute_chi_squared(text: str) -> float`: คำนวณค่าสถิติไคสแควร์ ($\chi^2$) โดยเปรียบเทียบการกระจายความถี่ของตัวอักษรใน `text` กับภาษาอังกฤษมาตรฐาน
  $$\chi^2 = \sum_{i \in \{A..Z\}} \frac{(O_i - E_i)^2}{E_i}$$
* `compute_index_of_coincidence(text: str) -> float`: คำนวณค่าดัชนีความบังเอิญ (Index of Coincidence - IC):
  $$\text{IC} = \frac{\sum_{i=A}^Z f_i (f_i - 1)}{N (N - 1)}$$
* `auto_break_caesar(ciphertext: str) -> tuple[int, str]`: ทดสอบคีย์การเลื่อนทั้ง 26 ค่าโดยอัตโนมัติ ประเมินผลข้อความถอดรหัสด้วย $\chi^2$ และส่งคืน `(best_shift_key, best_decrypted_plaintext)`

### งาน 2.3: พื้นฐานทฤษฎีจำนวนจากศูนย์ (8 คะแนน)
*ห้ามใช้ฟังก์ชัน `pow(base, exp, mod)` แบบ 3 อาร์กิวเมนต์ที่ติดมากับภาษาไพทอนในฟังก์ชัน `pow_mod()` และห้ามใช้โมดูลภายนอกในการหา modular inverse*
* `extended_gcd(a: int, b: int) -> tuple[int, int, int]`: พัฒนาขั้นตอนวิธียุคลิดส่วนขยาย (Extended Euclidean Algorithm) โดยส่งคืน `(g, x, y)` ที่สอดคล้องกับ $a \cdot x + b \cdot y = g = \gcd(a, b)$
* `modinv(a: int, m: int) -> int`: คำนวณตัวผกผันการคูณมอดุโล $a^{-1} \pmod m$ หาก $\gcd(a, m) \neq 1$ ให้โยนข้อผิดพลาด `ValueError`
* `pow_mod(base: int, exp: int, mod: int) -> int`: พัฒนาขั้นตอนวิธีการยกกำลังมอดุโลแบบเร็วด้วยเทคนิค **Square-and-Multiply (Binary Exponentiation)** ซึ่งทำงานในเวลา $\mathcal{O}(\log \text{exp})$

### งาน 2.4: ระบบการเข้ารหัสแบบรับรองความถูกต้องสมัยใหม่ (AES-256-GCM) (8 คะแนน)
* `encrypt_aes_gcm(plaintext: str, key: bytes, aad: bytes = b"") -> tuple[bytes, bytes]`: เข้ารหัส `plaintext` ด้วย AES-256-GCM โดยสร้างค่า Nonce สุ่มขนาด 96 บิต (12 ไบต์) อย่างปลอดภัย ส่งคืน `(nonce, ciphertext_with_tag)`
* `decrypt_aes_gcm(nonce: bytes, ciphertext_with_tag: bytes, key: bytes, aad: bytes = b"") -> str`: ถอดรหัสและตรวจสอบแท็กความถูกต้อง 16 ไบต์ หากตรวจพบการดัดแปลงแก้ไขข้อความรหัสหรือข้อมูลประกอบ (AAD) ต้องให้ระบบโยนข้อยกเว้นความปลอดภัย (`InvalidTag`) ออกมา

### งาน 2.5: เอนจิน RSA แบบสมบูรณ์ และ Curve25519 ECDH (8 คะแนน)
* `rsa_keygen(p: int, q: int, e: int = 65537) -> tuple[tuple[int, int], tuple[int, int]]`: สร้างกุญแจสาธารณะ $(N, e)$ และกุญแจส่วนตัว $(N, d)$ จากจำนวนเฉพาะ $p$ และ $q$
* `rsa_encrypt(message_int: int, public_key: tuple[int, int]) -> int`: เข้ารหัสข้อความตัวเลข: $C = M^e \bmod N$
* `rsa_decrypt(ciphertext_int: int, private_key: tuple[int, int]) -> int`: ถอดรหัสข้อความตัวเลข: $M = C^d \bmod N$
* `ecdh_x25519_key_exchange() -> tuple[bytes, bytes]`: จำลองการสร้างคู่กุญแจ Curve25519 สำหรับ Alice และ Bob คำนวณกุญแจลับร่วมกัน (Shared Secret) และส่งคืน `(alice_shared, bob_shared)`

---

# ⚔️ ส่วนที่ 3: การวิเคราะห์การโจมตีและการตอบสนองต่อเหตุการณ์ (30 คะแนน)

### การโจมตี 3.1: การกู้คืน Keystream จาก Two-Time Pad ด้วยวิธี Crib Dragging (10 คะแนน)
* **สถานการณ์จำลอง:** คุณดักจับโทรเลขทางการทูตที่ถูกเข้ารหัส 2 ฉบับ คือ $C_1$ และ $C_2$ ซึ่งใช้ One-Time Pad แต่เจ้าหน้าที่ฝ่ายสื่อสารประมาทนำกุญแจสุ่มแผ่นเดียวกันมาใช้ซ้ำ:
  $$C_1 = M_1 \oplus K, \quad C_2 = M_2 \oplus K \implies C_1 \oplus C_2 = M_1 \oplus M_2$$
* **ภารกิจ:** พัฒนาฟังก์ชัน `two_time_pad_crib_drag(c1_bytes: bytes, c2_bytes: bytes, crib: str) -> list[tuple[int, str]]` โดยการเลื่อนคำเดา (Crib) ไปบนสตรีม $C_1 \oplus C_2$ เพื่อกู้คืนข้อความต้นฉบับที่ถูกซ่อนอยู่

### การโจมตี 3.2: การเจาะช่องโหว่ AES-GCM Nonce Reuse (10 คะแนน)
* **สถานการณ์จำลอง:** API การโอนเงินของสถาบันการเงินแห่งหนึ่งมีข้อผิดพลาดร้ายแรง โดยระบบนำค่า Nonce 12 ไบต์ค่าเดิมมาเข้ารหัสรายการโอนเงิน 2 รายการติดต่อกันภายใต้กุญแจสมมาตร 256 บิตดอกเดียวกัน
* **ภารกิจ:** พัฒนาฟังก์ชัน `exploit_gcm_nonce_reuse(c1_payload: bytes, c2_payload: bytes) -> bytes`
* พิสูจน์ว่าเมื่อคุณทราบข้อความต้นฉบับของรายการแรก $P_1$ คุณสามารถคำนวณข้อความเป้าหมาย $P_2$ ได้โดยตรงจาก:
  $$P_2 = C_2 \oplus (C_1 \oplus P_1)$$
  จงถอดรหัสจำนวนเงินที่ถูกโอนและหมายเลขบัญชีปลายทางของผู้โจมตี

### การโจมตี 3.3: การโจมตีแยกตัวประกอบ Fermat Attack บนกุญแจ RSA ที่อ่อนแอ (10 คะแนน)
* **สถานการณ์จำลอง:** กล้องวงจรปิด IoT รุ่นหนึ่งมีฟังก์ชันสร้างจำนวนเฉพาะที่ผิดพลาดอย่างรุนแรง โดยเลือกค่า $p$ และ $q$ ที่มีค่าใกล้เคียงกันมาก ($|p - q| < 2 N^{1/4}$)
* **ภารกิจ:** พัฒนาฟังก์ชัน `fermat_factor(N: int) -> tuple[int, int]` โดยใช้วิธีผลต่างกำลังสองของแฟร์มาต์ ($N = a^2 - b^2 = (a-b)(a+b)$)
* พัฒนาฟังก์ชัน `crack_rsa_ciphertext(N: int, e: int, ciphertext: int) -> int` เพื่อแยกตัวประกอบ $N$ คำนวณหากุญแจลับ $d$ และถอดรหัสโทเค็นยืนยันตัวตนของสัญญาณกล้องวงจรปิด

---

# 🌟 คะแนนพิเศษ (Bonus / Extra Credit): โปรแกรมถอดรหัส Vigenère อัตโนมัติ (+15 คะแนน)

* พัฒนาฟังก์ชัน `crack_vigenere_cipher(ciphertext: str, max_key_len: int = 10) -> tuple[str, str]`:
  1. ประเมินความยาวคีย์ $m$ โดยคำนวณหาค่าเฉลี่ยของ Index of Coincidence จากคอลัมน์ย่อยที่กระจายออกไป
  2. แยกข้อความรหัสออกเป็น $m$ คอลัมน์อิสระ ซึ่งแต่ละคอลัมน์จะมีลักษณะเป็นรหัสซีซาร์ (Caesar Cipher)
  3. รันตัวถอดรหัสไคสแควร์ $\chi^2$ เพื่อค้นหาตัวอักษรของคีย์เวิร์ดในแต่ละคอลัมน์
  4. ประกอบคีย์เวิร์ดกลับคืนมาและถอดรหัสข้อความต้นฉบับฉบับเต็มโดยไม่ต้องทราบคีย์ล่วงหน้า

---

# 📦 คำแนะนำและขั้นตอนการส่งงานอย่างละเอียด (Detailed Submission Instructions)

### 1. รายการไฟล์ที่ต้องส่ง (Deliverables Checklist)
ตรวจสอบให้แน่ใจว่าโฟลเดอร์ส่งงานของคุณมีไฟล์ดังต่อไปนี้:
```text
assignments/
├── assignment_days_1_to_3_student.py  # โค้ดที่เติมฟังก์ชันสมบูรณ์แล้ว
├── REPORT.md                         # รายงานการพิสูจน์คณิตศาสตร์และบทวิเคราะห์ (หรือ REPORT_TH.md)
└── submission_metadata.json          # ไฟล์ใบเสร็จดิจิทัลที่สร้างโดยสคริปต์ตรวจสอบ
```

### 2. การตรวจสอบโค้ดและทดสอบอัตโนมัติก่อนส่ง (Pre-Submission Self-Test)
ทางหลักสูตรได้จัดเตรียมสคริปต์ตรวจสอบความถูกต้องอัตโนมัติ ซึ่งจะทำการรันเทสเคสทั้งหมด ตรวจสอบความสมบูรณ์ของรายงาน และสร้างรหัสแฮช SHA-256 สำหรับใช้เป็นหลักฐานการส่งงาน

รันคำสั่งตรวจสอบจากรากของโปรเจกต์ (Terminal):
```bash
python3 assignments/submit_check.py --student-id "รหัสนักศึกษา" --name "ชื่อ นามสกุล"
```

ตัวอย่างผลการทำงานที่ถูกต้อง:
```text
======================================================================
🎓 MODERN CRYPTOGRAPHY ASSIGNMENT (DAYS 1-3) PRE-FLIGHT CHECKER
======================================================================
[+] Candidate: สมชาย ใจดี (ID: 65070001)
[+] Running Automated Test Suite...
    -> Task 2.1: Statistical Cryptanalysis ................ [ PASS ]
    -> Task 2.2: Number Theory Primitives ................. [ PASS ]
    -> Task 2.3: Modern Symmetric AEAD (AES-GCM) .......... [ PASS ]
    -> Task 2.4: RSA Engine & Curve25519 .................. [ PASS ]
    -> Attack 3.1: Two-Time Pad Crib Drag ................. [ PASS ]
    -> Attack 3.2: AES-GCM Nonce Reuse .................... [ PASS ]
    -> Attack 3.3: Fermat RSA Factorization ............... [ PASS ]
    -> Bonus Task: Automated Vigenère Breaker ............. [ PASS ]
[+] Automated Test Score: 70/70 Code Points (+15 Bonus)
[+] Validating REPORT.md completeness ..................... [ PASS ]
[+] Calculating SHA-256 Submission Checksum ............... [ DONE ]
[+] Packaging submission: submission_65070001_days1_to_3.zip [ CREATED ]
======================================================================
🚀 ALL PRE-FLIGHT CHECKS PASSED! Ready for submission.
======================================================================
```

### 3. ช่องทางการส่งงาน (Submission Methods)

#### วิธีที่ 1: ระบบจัดการการเรียนรู้ของมหาวิทยาลัย (LMS / Canvas / Moodle / Google Classroom)
1. รันสคริปต์ `python3 assignments/submit_check.py --student-id "รหัสนักศึกษา" --name "ชื่อ นามสกุล"`
2. ระบบจะสร้างไฟล์บีบอัด `submission_<รหัสนักศึกษา>_days1_to_3.zip` ขึ้นมาในโฟลเดอร์ `assignments/`
3. ให้อัปโหลดไฟล์ `.zip` ดังกล่าวเข้าสู่ระบบส่งงานของรายวิชา
4. บันทึกค่า **SHA-256 Checksum** ที่ระบบพิมพ์ออกมาไว้เป็นหลักฐานยืนยันความถูกต้องและเวลาส่งงาน

#### วิธีที่ 2: การส่งผ่านระบบ Git / GitHub Classroom
หากรายวิชาของคุณใช้ระบบ GitHub Classroom:
```bash
# 1. สร้างกิ่งใหม่สำหรับการส่งงาน
git checkout -b submission-days1-to-3

# 2. ทำการ Stage ไฟล์งานที่เสร็จสมบูรณ์
git add assignments/assignment_days_1_to_3_student.py assignments/REPORT.md

# 3. Commit พร้อมระบุชื่อและรหัสนักศึกษา
git commit -m "Submit Class Assignment (Days 1-3) - [ชื่อ นามสกุล] - [รหัสนักศึกษา]"

# 4. ติดแท็กและ Push ขึ้นสู่ Remote Repository
git tag -a v1.0-submission -m "Final Submission"
git push origin submission-days1-to-3 --tags
```

---

## ⚖️ จริยธรรมทางวิชาการและนโยบายการใช้ AI (Academic Integrity & AI Policy)

* **ความซื่อสัตย์ทางวิชาการ (Honor Code):** โค้ดโปรแกรมทั้งหมดรวมถึงการพิสูจน์ทางคณิตศาสตร์ต้องเป็นผลงานทางปัญญาของตัวนักศึกษาเอง
* **นโยบายการใช้งานปัญญาประดิษฐ์ (AI Assistance):** นักศึกษาสามารถใช้เครื่องมือ AI (เช่น Antigravity, ChatGPT, Claude) เพื่อเป็นผู้ช่วยสอนในการทำความเข้าใจมโนทัศน์หรือแก้ไขข้อผิดพลาดของไวยากรณ์โค้ดได้ **อย่างไรก็ตาม นักศึกษาต้องสามารถอธิบายที่มาของโค้ดทุกบรรทัดและขั้นตอนการพิสูจน์ทุกขั้นตอนได้อย่างกระจ่างแจ้ง หากได้รับการเรียกสัมภาษณ์เพื่อสอบถามรายบุคคลจากคณาจารย์ผู้สอน**
* **การทำงานร่วมกัน:** อนุญาตให้แลกเปลี่ยนและปรึกษาแนวคิดระดับสูงกับเพื่อนร่วมชั้นได้ แต่ไม่อนุญาตให้คัดลอกโค้ด แชร์ไฟล์คำตอบ หรือนำโค้ดของผู้อื่นมาส่งโดยเด็ดขาด

---

## 📊 เกณฑ์การให้คะแนนแบบละเอียด (Rubric Matrix)

```text
คะแนนเต็มรวม: 100 คะแนน (+15 คะแนนพิเศษ)

ส่วนที่ 1: การพิสูจน์ทฤษฎีและคณิตศาสตร์ (30 คะแนน)
├── ข้อ 1.1 (10 คะแนน): การพิสูจน์ Shannon Perfect Secrecy (5 คะแนน) + ขอบเขตขนาดกุญแจ (5 คะแนน)
├── ข้อ 1.2 (10 คะแนน): AES Confusion/Diffusion (4 คะแนน) + ECB IND-CPA (3 คะแนน) + GCM Nonce Reuse (3 คะแนน)
└── ข้อ 1.3 (10 คะแนน): การพิสูจน์ RSA CRT (5 คะแนน) + การโจมตี Chosen-Ciphertext & OAEP (5 คะแนน)

ส่วนที่ 2: การเขียนโปรแกรมอัลกอริทึม (40 คะแนน)
├── งาน 2.1 (10 คะแนน): ฟังก์ชัน Chi-Squared & IC (5 คะแนน) + Caesar Auto-Breaker (5 คะแนน)
├── งาน 2.2 (10 คะแนน): Extended Euclidean (4 คะแนน) + ModInv (3 คะแนน) + PowMod (3 คะแนน)
├── งาน 2.3 (10 คะแนน): การเข้ารหัส/ถอดรหัส AES-256-GCM (6 คะแนน) + การดักจับข้อผิดพลาดการดัดแปลง (4 คะแนน)
└── งาน 2.4 (10 คะแนน): เอนจิน RSA Keygen/Enc/Dec (6 คะแนน) + Curve25519 ECDH (4 คะแนน)

ส่วนที่ 3: การวิเคราะห์และโจมตีระบบรหัสลับ (30 คะแนน)
├── การโจมตี 3.1 (10 คะแนน): พัฒนา Crib Dragging และกู้คืนข้อความจาก Two-Time Pad
├── การโจมตี 3.2 (10 คะแนน): ถอดรหัส Keystream และกู้คืนข้อความลับจากการใช้ซ้ำ GCM Nonce
└── การโจมตี 3.3 (10 คะแนน): การแยกตัวประกอบ Fermat Factorization บน RSA และถอดรหัสข้อความลับ

คะแนนพิเศษ Extra Credit (+15 คะแนน)
└── โบนัส 3.4 (15 คะแนน): โปรแกรมถอดรหัส Vigenère อัตโนมัติโดยใช้ IC หาความยาวคีย์และ Chi-Square แก้คอลัมน์
```
