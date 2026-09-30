# 🎓 ใบงานปฏิบัติการเน้นเนื้อหาวันที่ 1: รหัสลับคลาสสิกและกลไกวงล้อรหัสลับ
## การประมวลผลข้อความสั้นและข้อความยาว: แบบมีวงล้อช่วย เทียบกับ แบบไม่มีวงล้อช่วย (5 ข้อปฏิบัติการ)
**หลักสูตร:** การเข้ารหัสขั้นสูงและความปลอดภัยของเครือข่าย (CS-4XX / ECE-4XX)  
**เนื้อหาประจำวัน:** วันที่ 1 — รหัสลับแบบแทนที่, แผ่นจานรหัสลับซ้อน และการประมวลผลสตรีมข้อความ

* 🌐 **ภาษา / Language:** [🇹🇭 ภาษาไทย (Thai)](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_DAY1_TH.md) | [🇺🇸 English Version](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/ASSIGNMENT_DAY1.md)
* **กลุ่มเป้าหมาย:** นักศึกษาปริญญาตรีและโท (วิทยาการคอมพิวเตอร์ / วิศวกรรมคอมพิวเตอร์) และผู้สนใจศึกษาความปลอดภัยทางไซเบอร์
* **เนื้อหาหลัก:** วันที่ 1 (Classical Cryptanalysis & Information Theory)
* **กำหนดส่ง (Due Date):** วันอาทิตย์ เวลา 23:59:59 น. (7 วันหลังจากวันที่มอบหมาย)
* **ไฟล์โค้ดเริ่มต้นสำหรับนักศึกษา (Starter Code):** [`assignments/assignment_day1_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_day1_student.py)
* **เทมเพลตรายงานผล (Report Template):** [`assignments/REPORT_TEMPLATE_DAY1_TH.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_DAY1_TH.md) (หรือ [`REPORT_TEMPLATE_DAY1.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_DAY1.md))
* **สคริปต์ตรวจสอบความพร้อมก่อนส่ง (Submission Validator):** [`assignments/submit_check_day1.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/submit_check_day1.py)

---

## 🎯 วัตถุประสงค์และภาพรวมการเรียนรู้ (Executive Summary)

ในเนื้อหา **วันที่ 1** ของหลักสูตร เราได้ศึกษารากฐานของความลับ: มนุษย์ในอดีตปกป้องคำสั่งทางทหารได้อย่างไร และอุปกรณ์กลไกอย่าง **แผ่นจานรหัสลับของอัลแบร์ตี (Alberti Cipher Disk, 1467)** เชื่อมโยงการเข้ารหัสด้วยกระดาษและปากกา เข้าสู่เครื่องเข้ารหัสลับจานหมุนยุคใหม่ได้อย่างไร

ใบงานชุดนี้เน้นเจาะลึก 2 กระบวนทัศน์หลักของวิทยาการรหัสลับคลาสสิก:
1. **กระบวนทัศน์ทางคณิตศาสตร์ / คำนวณตรง (แบบไม่มีวงล้อช่วย - Without Wheel Support):** การคำนวณเลขคณิตมอดุโลบนวงแหวน $\mathbb{Z}_{26}$ ($C = (P + k) \bmod 26$) ที่รวดเร็วและใช้คำสั่งระดับรีจิสเตอร์ของซีพียู
2. **กระบวนทัศน์เชิงกลไก / หน้าปัดจำลอง (แบบมีวงล้อช่วย - With Wheel Support):** การจำลองวงล้อรหัสลับซ้อนสองวง (Concentric Wheel), การหมุนตั้งตำแหน่งหน้าปัด และการอ่านตัวอักษรคู่ขนานบนวงล้อชั้นนอกและชั้นใน

นักศึกษาจะได้ลงมือเขียนโปรแกรมประมวลผลทั้ง **ข้อความสั้น (คำสั่งทางยุทธวิธี)** และ **ข้อความยาวหลายบรรทัด (โทรเลขทางการทูต)**, พิสูจน์ความสมมูลทางคณิตศาสตร์ระหว่างวงล้อและสูตรคำนวณ, สังเกตว่าวงล้อแบบก้าวหมุน (Stepping Wheel) ทำลายการวิเคราะห์ความถี่ได้อย่างไร และลงมือเจาะรหัสลับโทรเลขสนามรบที่ดักจับได้

---

# 📖 รายละเอียดคำถามทั้ง 5 ข้อในใบงาน

เปิดไฟล์ [`assignments/assignment_day1_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_day1_student.py) และเติมโค้ดในจุดที่มีคำสั่ง `# TODO: YOUR CODE HERE`

---

### 📝 ข้อที่ 1: การประมวลผลข้อความสั้นแบบไม่มีวงล้อช่วย

ในข้อนี้ นักศึกษาจะพัฒนาการเข้ารหัสและถอดรหัสซีซาร์โดยไม่พึ่งพาวงล้อใดๆ โดยใช้เลขคณิตมอดุโลบนภาษา Python:

$$C_i = (P_i + \text{shift}) \bmod 26$$
$$P_i = (C_i - \text{shift}) \bmod 26$$

#### ข้อกำหนด:
* `caesar_direct_encrypt(plaintext: str, shift: int) -> str`:
  * เลื่อนตัวอักษรภาษาอังกฤษไปข้างหน้าตามค่า `shift`
  * รักษาสถานะตัวพิมพ์ใหญ่และตัวพิมพ์เล็กตามเดิม
  * เว้นวรรค, เครื่องหมายวรรคตอน และตัวเลข ต้องคงเดิมไม่เปลี่ยนแปลง
  * รองรับค่าการเลื่อนที่มากกว่า 26 หรือค่าติดลบด้วยการมอดุโล 26
* `caesar_direct_decrypt(ciphertext: str, shift: int) -> str`:
  * ทำการย้อนกลับการเลื่อนเพื่อถอดรหัสข้อความเดิม

---

### 🎡 ข้อที่ 2: การประมวลผลข้อความสั้นแบบมีวงล้อช่วย

ในปี ค.ศ. 1467 เลออน บัตติสตา อัลแบร์ตี ประดิษฐ์แผ่นจานรหัสลับซ้อนสองวง โดยวงนอกอยู่นิ่ง (ข้อความต้นฉบับ: A–Z) และวงในหมุนได้ (ข้อความรหัสลับ: A–Z เลื่อนไป $k$ ตำแหน่ง)

```
+-------------------------------------------------------------------+
| 🎡 CIPHER WHEEL ALIGNMENT (Current Shift: 04)                       |
+-------------------------------------------------------------------+
| Outer Disk (Plaintext) : A B C D E F G H I J K L M N O P Q R S T U V W X Y Z |
| Inner Disk (Ciphertext): E F G H I J K L M N O P Q R S T U V W X Y Z A B C D |
+-------------------------------------------------------------------+
```

#### ข้อกำหนด:
* เติมเมธอดในคลาส `CipherWheel` ในไฟล์ [`assignment_day1_student.py`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/assignment_day1_student.py):
  * `rotate(steps: int)`: หมุนวงล้อชั้นในตามเข็มนาฬิกา
  * `set_shift(shift: int)`: ตั้งตำแหน่งการหมุนของวงล้อโดยตรง
  * `get_inner_alphabet() -> str`: ส่งคืนลำดับตัวอักษร 26 ตัวของวงใน
  * `render_ascii_dial() -> str`: วาดภาพจำลองหน้าปัดวงล้อแบบ ASCII
  * `encrypt_char(char: str)` และ `decrypt_char(char: str)`: อ่านตัวอักษรคู่ขนานบนหน้าปัดวงล้อ
* พัฒนาฟังก์ชัน:
  * `wheel_encrypt_short(plaintext: str, wheel: CipherWheel) -> str`
  * `wheel_decrypt_short(ciphertext: str, wheel: CipherWheel) -> str`

---

### 📜 ข้อที่ 3: การประมวลผลข้อความยาวและการพิสูจน์ความสมมูล

ในการปฏิบัติการจริง การเข้ารหัสจะต้องรองรับเอกสารยาวหลายบรรทัด รายงานข่าวกรองที่มีการเว้นวรรค ตัวเลข และย่อหน้า

เราได้เตรียมข้อความประวัติศาสตร์บันทึกสงครามกอลของซีซาร์ (`LONG_HISTORICAL_MESSAGE`, ความยาว 370 ตัวอักษร)

#### ข้อกำหนด:
* `process_long_message_direct(text: str, shift: int, mode: str = "encrypt") -> str`:
  * ประมวลผลข้อความยาวแบบไม่มีวงล้อช่วย โดยใช้สูตรคณิตศาสตร์
* `process_long_message_wheel(text: str, wheel: CipherWheel, mode: str = "encrypt") -> str`:
  * ประมวลผลข้อความยาวแบบมีวงล้อช่วย โดยใช้การจำลอง `CipherWheel`
* **การพิสูจน์ความสมมูล (Equivalence Verification):**
  * บันทึกหลักฐานในรายงาน ([`REPORT_TEMPLATE_DAY1_TH.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_DAY1_TH.md)) ว่า:
    $$\text{Ciphertext}_{\text{direct}} \equiv \text{Ciphertext}_{\text{wheel}}$$
  * อธิบายว่าทำไมคอมพิวเตอร์ดิจิทัลจึงไม่ใช้วิธีตารางจำลองวงล้อ แต่ใช้การคำนวณมอดุโลตรงๆ ในซีพียู

---

### ⚙️ ข้อที่ 4: วงล้อรหัสลับแบบก้าวหมุนต่อเนื่อง (Stepping Rotor)

จุดอ่อนร้ายแรงของรหัสลับซีซาร์แบบดั้งเดิม (วงล้ออยู่นิ่ง) คือ **การรั่วไหลของความถี่ตัวอักษร**: ตัวอักษรยอดนิยมอย่าง 'E' จะถูกแปลงเป็นตัวอักษรเดิมซ้ำๆ เสมอ

เพื่อแก้ปัญหานี้ นักประดิษฐ์ในอดีตจึงออกแบบให้ **วงล้อชั้นในหมุนก้าวไปข้างหน้า 1 กริ๊กทุกครั้งหลังเข้ารหัสตัวอักษร 1 ตัว**!

```
Plaintext:  A   A   A   A   A   A
Wheel Pos:  1   2   3   4   5   6
Ciphertext: B   C   D   E   F   G   <-- ตัวอักษรเหมือนกัน 6 ตัว ถูกแปลงเป็นตัวอักษรที่ไม่ซ้ำกันเลย!
```

#### ข้อกำหนด:
* `progressive_wheel_encrypt(plaintext: str, initial_shift: int, step: int = 1) -> str`:
  * ตั้งค่าวงล้อเริ่มต้นที่ `initial_shift`
  * ทุกครั้งที่เข้ารหัสตัวอักษร ให้หมุนวงล้อไป `step` ตำแหน่ง (`wheel.rotate(step)`)
  * ตัวอักษรที่ไม่ใช่ภาษาอังกฤษ (ช่องว่าง, ตัวเลข) จะไม่เข้ารหัสและไม่หมุนวงล้อ
* `progressive_wheel_decrypt(ciphertext: str, initial_shift: int, step: int = 1) -> str`:
  * ถอดรหัสสตรีมก้าวหมุนด้วยการหมุนย้อนกลับที่ตรงกัน

---

### 🕵️ ข้อที่ 5: การวิเคราะห์เจาะรหัสลับข้อความดักจับ

หน่วยดักฟังสัญญาณดักจับโทรเลขทางการทูตลับได้ดังนี้:
`"AOL JVUMLYLUJL PZ ZJOLKBSLK MVY TPKUPNOA HA AOL OPNI ZLJYLA IBURLY."`

ฝ่ายข่าวกรองทราบว่าในข้อความนี้พูดถึงการประชุมลับ (`"CONFERENCE"`)

#### ข้อกำหนด:
* `crack_without_wheel(ciphertext: str, clue_word: str = "THE") -> tuple[int, str]`:
  * วนลูปทดสอบคีย์ทั้ง 26 ค่าทางคณิตศาสตร์ ($0..25$)
  * ค้นหาคำว่า `clue_word.upper()` ในข้อความที่ถอดรหัสได้
  * ส่งคืนค่า `(shift, decrypted_plaintext)`
* `crack_with_wheel(ciphertext: str, wheel: CipherWheel, clue_word: str = "THE") -> tuple[int, str]`:
  * หมุนหน้าปัด `CipherWheel` ทดสอบทั้ง 26 ตำแหน่ง (`set_shift(0..25)`)
  * ถอดรหัสผ่านวงล้อและส่งคืนค่า `(shift, decrypted_plaintext)`

---

# 🌟 ข้อโบนัสพิเศษ: วงล้อรหัสลับแบบสลับตัวอักษรด้วยคีย์คำ

ในวงล้อซีซาร์มาตรฐาน ทั้งสองวงล้อจะเรียง A ถึง Z ตามลำดับ แต่ในวงล้อขั้นสูง วงล้อชั้นในจะถูกสลับลำดับด้วยคำกุญแจลับ (เช่น คีย์คำ `"SECRET"` $\to$ `"SECRTABDFGHIJKLMNOPQUVWXYZ"`)

* พัฒนาฟังก์ชัน `scrambled_wheel_encrypt()` และ `scrambled_wheel_decrypt()`
* อธิบายในรายงานว่าการสลับลำดับตัวอักษรทำให้ปริภูมิกุญแจขยายจาก 25 แบบ เพิ่มขึ้นเป็น $26! \approx 4 \times 10^{26}$ แบบได้อย่างไร

---

# 🧪 การทดสอบและการส่งงาน

ทดสอบโค้ดบนเครื่องของท่านได้ตลอดเวลา:
```bash
# รันชุดทดสอบโค้ดประจำวันที่ 1:
python3 assignments/assignment_day1_student.py
```

เมื่อเขียนโค้ดและรายงานครบถ้วนแล้ว ให้รันสคริปต์ตรวจสอบและรวมไฟล์ส่ง:
```bash
python3 assignments/submit_check_day1.py --student-id "รหัสนักศึกษา" --name "ชื่อ นามสกุล"
```

สคริปต์จะดำเนินการโดยอัตโนมัติ:
1. ทดสอบโค้ดของท่านกับคำถามทั้ง 5 ข้อ
2. ตรวจสอบความสมบูรณ์ของรายงาน ([`REPORT_TEMPLATE_DAY1_TH.md`](file:///Users/kvivek/Documents/modern-cryptography-course/assignments/REPORT_TEMPLATE_DAY1_TH.md))
3. คำนวณรหัสตรวจสอบ SHA-256 Checksum เพื่อเป็นหลักฐานการส่งงานที่ตรงต่อเวลา
4. รวมไฟล์เป็นแพ็กเกจส่งงาน: `assignments/submission_<รหัสนักศึกษา>_day1.zip`
