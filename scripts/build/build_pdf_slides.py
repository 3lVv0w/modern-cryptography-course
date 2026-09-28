import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# Output PDF path
pdf_path = "/Users/kvivek/Documents/modern-cryptography-course/history_of_cryptography_and_enigma.pdf"
enigma_img_path = "/Users/kvivek/.gemini/antigravity-ide/brain/a34aece2-17d3-4cea-b26a-dea8a137d8f7/enigma_machine_diagram_1784798692008.png"

# Page Dimensions (16:9 Widescreen Presentation Slides)
SLIDE_WIDTH = 13.333 * inch
SLIDE_HEIGHT = 7.5 * inch

def draw_background(canvas, doc):
    canvas.saveState()
    # Dark Navy Premium Slate Background (#0B0F19)
    canvas.setFillColor(colors.HexColor("#0B0F19"))
    canvas.rect(0, 0, SLIDE_WIDTH, SLIDE_HEIGHT, fill=True, stroke=False)
    
    # Top Accent Bar (Gradient Cyan-Gold)
    canvas.setFillColor(colors.HexColor("#06B6D4"))
    canvas.rect(0, SLIDE_HEIGHT - 6, SLIDE_WIDTH * 0.5, 6, fill=True, stroke=False)
    canvas.setFillColor(colors.HexColor("#F59E0B"))
    canvas.rect(SLIDE_WIDTH * 0.5, SLIDE_HEIGHT - 6, SLIDE_WIDTH * 0.5, 6, fill=True, stroke=False)
    
    # Footer Slide Number & Header
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(0.6 * inch, 0.4 * inch, "CS-4XX: Modern Cryptography & Network Security | History of Cryptography & Enigma")
    canvas.drawRightString(SLIDE_WIDTH - 0.6 * inch, 0.4 * inch, f"Slide {doc.page}")
    canvas.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=(SLIDE_WIDTH, SLIDE_HEIGHT),
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch
    )

    styles = getSampleStyleSheet()
    
    # Custom Color Palette
    GOLD = colors.HexColor("#F59E0B")
    CYAN = colors.HexColor("#06B6D4")
    LIGHT_GRAY = colors.HexColor("#E5E7EB")
    WHITE = colors.HexColor("#FFFFFF")
    DARK_CARD = colors.HexColor("#111827")
    BORDER_CYAN = colors.HexColor("#1E293B")

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=36,
        leading=44,
        textColor=GOLD,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=18,
        leading=24,
        textColor=CYAN,
        alignment=TA_CENTER
    )

    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=GOLD,
        alignment=TA_LEFT
    )

    slide_subtitle_style = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=CYAN,
        alignment=TA_LEFT
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=LIGHT_GRAY,
        alignment=TA_LEFT
    )

    bullet_style = ParagraphStyle(
        'SlideBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'SlideCode',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=11,
        leading=15,
        textColor=CYAN,
        alignment=TA_LEFT
    )

    story_quote_style = ParagraphStyle(
        'StoryQuote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#9CA3AF"),
        alignment=TA_LEFT
    )

    story = []

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("UNBROKEN CODES & BROKEN EMPIRES", title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("A Historically Accurate Journey Through Cryptography and the Enigma Machine", subtitle_style))
    story.append(Spacer(1, 0.4 * inch))
    
    meta_text = Paragraph(
        "<font color='#9CA3AF'><b>Course:</b> CS-4XX / ECE-4XX Modern Cryptography & Network Security<br/>"
        "<b>Focus:</b> Classical Ciphers, Polish Cipher Bureau (1932), Bletchley Park, Shannon & Public Key Era</font>",
        ParagraphStyle('Meta', parent=styles['Normal'], alignment=TA_CENTER, fontSize=12, leading=16)
    )
    story.append(meta_text)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: ERA 1 — ANCIENT CIPHERS & AL-KINDI (850 AD)
    # =========================================================================
    story.append(Paragraph("Era 1: Classical Antiquity & The Birth of Cryptanalysis", slide_title_style))
    story.append(Paragraph("From Spartan Scytales to 9th-Century Frequency Analysis in Baghdad", slide_subtitle_style))
    story.append(Spacer(1, 0.15 * inch))

    col1_content = [
        Paragraph("<b>1. Transposition & Monoalphabetic Ciphers</b>", slide_subtitle_style),
        Paragraph("• <b>Scytale of Sparta (5th C. BC):</b> Strip of leather wrapped around a wooden rod. Earliest transposition cipher.", bullet_style),
        Paragraph("• <b>Caesar Shift Cipher (c. 58 BC):</b> Monoalphabetic substitution over Z₂₆:<br/><font color='#06B6D4'>C_i = (P_i + 3) mod 26</font>", bullet_style),
        Paragraph("• Used by Julius Caesar for military directives. Easily brute-forced since key space |K| = 25.", bullet_style),
    ]

    col2_content = [
        Paragraph("<b>2. Al-Kindi & Frequency Analysis (c. 850 AD)</b>", slide_subtitle_style),
        Paragraph("• <b>Al-Kindi (Baghdad):</b> Polymath at the House of Wisdom.", bullet_style),
        Paragraph("• Published <i>A Manuscript on Deciphering Cryptographic Messages</i>.", bullet_style),
        Paragraph("• <b>The Breakthrough:</b> Discovered natural languages contain skewed letter frequencies (E ≈ 12.7%, T ≈ 9.1%).", bullet_style),
        Paragraph("• <b>Impact:</b> Rendered all monoalphabetic substitution ciphers obsolete forever.", bullet_style),
    ]

    t1 = Table([[col1_content, col2_content]], colWidths=[6.0 * inch, 6.0 * inch])
    t1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), DARK_CARD),
        ('BACKGROUND', (1,0), (1,0), DARK_CARD),
        ('BOX', (0,0), (0,0), 1, BORDER_CYAN),
        ('BOX', (1,0), (1,0), 1, BORDER_CYAN),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t1)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: ERA 2 — POLYALPHABETIC CIPHERS & VIGENÈRE (1553-1863)
    # =========================================================================
    story.append(Paragraph("Era 2: Polyalphabetic Substitution & Breaking Vigenère", slide_title_style))
    story.append(Paragraph("Defeating Single-Letter Frequency Analysis", slide_subtitle_style))
    story.append(Spacer(1, 0.15 * inch))

    c1 = [
        Paragraph("<b>1. The Vigenère Cipher (1553 / 1586)</b>", slide_subtitle_style),
        Paragraph("• Formulated by Giovan Battista Bellaso, popularized by Blaise de Vigenère.", bullet_style),
        Paragraph("• Uses a repeating keyword K to shift letters independently:<br/><font color='#06B6D4'>C_i = (P_i + K_{i mod m}) mod 26</font>", bullet_style),
        Paragraph("• Flattens single-letter frequency distribution. Dubbed <i>'Le Chiffre Indéchiffrable'</i> for 300 years.", bullet_style),
    ]

    c2 = [
        Paragraph("<b>2. Cracking the 'Unbreakable' Cipher (1854 / 1863)</b>", slide_subtitle_style),
        Paragraph("• <b>Charles Babbage (1854) & Friedrich Kasiski (1863):</b> Independently cracked Vigenère.", bullet_style),
        Paragraph("• <b>Kasiski Examination:</b> Distance between repeating n-grams reveals key length <i>m</i>.", bullet_style),
        Paragraph("• <b>Index of Coincidence (IC):</b> Developed by W.F. Friedman:<br/><font color='#06B6D4'>IC(T) = Σ f_i(f_i - 1) / [N(N - 1)]</font><br/>English text IC ≈ 0.0667 vs Random text IC ≈ 0.0385.", bullet_style),
    ]

    t2 = Table([[c1, c2]], colWidths=[6.0 * inch, 6.0 * inch])
    t2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), DARK_CARD),
        ('BACKGROUND', (1,0), (1,0), DARK_CARD),
        ('BOX', (0,0), (0,0), 1, BORDER_CYAN),
        ('BOX', (1,0), (1,0), 1, BORDER_CYAN),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t2)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: ERA 3 — THE ENIGMA MACHINE ARCHITECTURE & DIAGRAM
    # =========================================================================
    story.append(Paragraph("Era 3: The Mechanics of the WWII Enigma Machine", slide_title_style))
    story.append(Paragraph("Arthur Scherbius Patent (1918) & German Military Adoption", slide_subtitle_style))
    story.append(Spacer(1, 0.1 * inch))

    if os.path.exists(enigma_img_path):
        img = Image(enigma_img_path, width=5.5 * inch, height=5.0 * inch)
    else:
        img = Paragraph("[Enigma Diagram]", body_style)

    e_info = [
        Paragraph("<b>Enigma Hardware & Signal Path</b>", slide_subtitle_style),
        Paragraph("1. <b>Keyboard:</b> Keypress sends electrical current.", bullet_style),
        Paragraph("2. <b>Plugboard (Steckerbrett):</b> Swapped 10 pairs of letters before & after rotors.", bullet_style),
        Paragraph("3. <b>Rotors (Walzen):</b> 3 interchangeable rotors chosen from 5 (Kriegsmarine used 4/8). Rightmost rotor stepped every keypress.", bullet_style),
        Paragraph("4. <b>Reflector (Umkehrwalze):</b> Bounced signal back through rotors in reverse.", bullet_style),
        Paragraph("5. <b>Lampboard:</b> Final encrypted letter lit up.", bullet_style),
        Spacer(1, 0.1 * inch),
        Paragraph("<b>Astronomical Key Space:</b><br/><font color='#F59E0B'><b>~ 158,962,555,217,826,360,000 Key Combinations!</b></font>", bullet_style),
    ]

    t_enigma = Table([[img, e_info]], colWidths=[5.7 * inch, 6.3 * inch])
    t_enigma.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (1,0), (1,0), DARK_CARD),
        ('BOX', (1,0), (1,0), 1, BORDER_CYAN),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_enigma)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: THE POLISH CIPHER BUREAU BREAKTHROUGH (1932-1939)
    # =========================================================================
    story.append(Paragraph("The Unsung Heroes: Polish Cipher Bureau (Biuro Szyfrów)", slide_title_style))
    story.append(Paragraph("The Mathematical Breakthrough 7 Years Before Bletchley Park (1932–1939)", slide_subtitle_style))
    story.append(Spacer(1, 0.15 * inch))

    p1 = [
        Paragraph("<b>1. Marian Rejewski's Mathematical Proof (1932)</b>", slide_subtitle_style),
        Paragraph("• 27-year-old Polish mathematician at Biuro Szyfrów in Warsaw.", bullet_style),
        Paragraph("• Applied <b>Permutation Group Theory</b> to double-encrypted message indicators.", bullet_style),
        Paragraph("• Derived internal wiring equations of all 3 German rotors <b>without ever seeing a military Enigma machine!</b>", bullet_style),
    ]

    p2 = [
        Paragraph("<b>2. Electromechanical Hardware & Pyry Handover (1938-1939)</b>", slide_subtitle_style),
        Paragraph("• <b>The Bomba (1938):</b> Rejewski built electromechanical units using 6 synchronized Enigmas to search for daily rotor orders.", bullet_style),
        Paragraph("• <b>Zygalski Sheets:</b> Perforated paper sheets created by Henryk Zygalski to track rotor positions.", bullet_style),
        Paragraph("• <b>July 1939 Pyry Handover:</b> Realizing German invasion was imminent, Poland handed over replica Enigma machines, Bomba designs, and math proofs to Britain and France.", bullet_style),
    ]

    tp = Table([[p1, p2]], colWidths=[6.0 * inch, 6.0 * inch])
    tp.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), DARK_CARD),
        ('BACKGROUND', (1,0), (1,0), DARK_CARD),
        ('BOX', (0,0), (0,0), 1, BORDER_CYAN),
        ('BOX', (1,0), (1,0), 1, BORDER_CYAN),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(tp)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: BLETCHLEY PARK & ALAN TURING (1939-1945)
    # =========================================================================
    story.append(Paragraph("Bletchley Park, Alan Turing & The Ultra Secret (1939–1945)", slide_title_style))
    story.append(Paragraph("Exploiting Enigma's Fatal Architectural Flaw", slide_subtitle_style))
    story.append(Spacer(1, 0.15 * inch))

    b1 = [
        Paragraph("<b>1. Enigma's Fatal Design Flaw</b>", slide_subtitle_style),
        Paragraph("• Enigma contained a fatal electrical flaw:<br/><font color='#F59E0B'><b>A letter could NEVER encrypt to itself! (E(x) ≠ x)</b></font>", bullet_style),
        Paragraph("• <b>Cribs:</b> Predictable text in military cables (e.g. weather reports <i>'WETTERVORHERSAGE'</i>).", bullet_style),
        Paragraph("• If a crib matched a ciphertext letter at the same index, that alignment was mathematically impossible and ruled out instantly!", bullet_style),
    ]

    b2 = [
        Paragraph("<b>2. The Turing-Welchman Bombe & ULTRA Impact</b>", slide_subtitle_style),
        Paragraph("• <b>Alan Turing (Hut 8) & Gordon Welchman:</b> Designed the electromechanical <b>Turing Bombe</b>.", bullet_style),
        Paragraph("• Used Welchman's <i>Diagonal Board</i> to exploit plugboard symmetries and test thousands of rotor settings per second.", bullet_style),
        Paragraph("• <b>Historical Impact:</b> ULTRA intelligence shortened WWII in Europe by <b>2 to 4 years</b>, saving millions of lives.", bullet_style),
    ]

    tb = Table([[b1, b2]], colWidths=[6.0 * inch, 6.0 * inch])
    tb.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), DARK_CARD),
        ('BACKGROUND', (1,0), (1,0), DARK_CARD),
        ('BOX', (0,0), (0,0), 1, BORDER_CYAN),
        ('BOX', (1,0), (1,0), 1, BORDER_CYAN),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(tb)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: ERA 4 — SHANNON & SYMMETRIC BLOCK CIPHERS (1949-2001)
    # =========================================================================
    story.append(Paragraph("Era 4: Claude Shannon & Symmetric Block Ciphers", slide_title_style))
    story.append(Paragraph("Information Theory, Confusion, Diffusion & AES-256", slide_subtitle_style))
    story.append(Spacer(1, 0.15 * inch))

    s1 = [
        Paragraph("<b>1. Claude Shannon's Information Theory (1949)</b>", slide_subtitle_style),
        Paragraph("• Published <i>Communication Theory of Secrecy Systems</i>.", bullet_style),
        Paragraph("• Formulated <b>Confusion</b> (obscuring key-ciphertext link) and <b>Diffusion</b> (spreading plaintext redundancy).", bullet_style),
        Paragraph("• Proved <b>Perfect Secrecy</b> for One-Time Pad: P(M=m | C=c) = P(M=m).", bullet_style),
    ]

    s2 = [
        Paragraph("<b>2. DES to AES-256 Standardization</b>", slide_subtitle_style),
        Paragraph("• <b>DES (1977):</b> 56-bit Feistel Network block cipher. Broken by brute force in 1998.", bullet_style),
        Paragraph("• <b>AES (2001):</b> Substitution-Permutation Network over Galois Field GF(2⁸) matrix operations.", bullet_style),
        Paragraph("• Standardized with 128, 192, and 256-bit key sizes. Powers modern disk and TLS data encryption.", bullet_style),
    ]

    ts = Table([[s1, s2]], colWidths=[6.0 * inch, 6.0 * inch])
    ts.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), DARK_CARD),
        ('BACKGROUND', (1,0), (1,0), DARK_CARD),
        ('BOX', (0,0), (0,0), 1, BORDER_CYAN),
        ('BOX', (1,0), (1,0), 1, BORDER_CYAN),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(ts)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: ERA 5 — THE PUBLIC-KEY REVOLUTION (1976-PRESENT)
    # =========================================================================
    story.append(Paragraph("Era 5: The Public-Key Cryptography Revolution", slide_title_style))
    story.append(Paragraph("Solving the Key Distribution Paradox with Asymmetric Math", slide_subtitle_style))
    story.append(Spacer(1, 0.15 * inch))

    pk1 = [
        Paragraph("<b>1. Diffie-Hellman & RSA (1976-1977)</b>", slide_subtitle_style),
        Paragraph("• <b>Diffie-Hellman (1976):</b> Whitfield Diffie & Martin Hellman solved open key exchange using Discrete Logarithm Problem (gᵃ mod p).", bullet_style),
        Paragraph("• <b>RSA (1977):</b> Rivest, Shamir, & Adleman introduced trapdoor one-way functions based on Prime Factorization (N = p · q).", bullet_style),
    ]

    pk2 = [
        Paragraph("<b>2. Elliptic Curve Cryptography (ECC)</b>", slide_subtitle_style),
        Paragraph("• Koblitz & Miller (1985) introduced Weierstrass curves:<br/><font color='#06B6D4'>y² = x³ + ax + b mod p</font>", bullet_style),
        Paragraph("• <b>ECC Efficiency:</b> 256-bit ECC (Curve25519) matches 3072-bit RSA security level.", bullet_style),
        Paragraph("• Powers modern HTTPS web traffic, SSH keys, Signal messaging, and Bitcoin transactions.", bullet_style),
    ]

    tpk = Table([[pk1, pk2]], colWidths=[6.0 * inch, 6.0 * inch])
    tpk.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), DARK_CARD),
        ('BACKGROUND', (1,0), (1,0), DARK_CARD),
        ('BOX', (0,0), (0,0), 1, BORDER_CYAN),
        ('BOX', (1,0), (1,0), 1, BORDER_CYAN),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(tpk)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: ERA 6 — THE QUANTUM THREAT & NIST PQC (PRESENT-FUTURE)
    # =========================================================================
    story.append(Paragraph("Era 6: The Quantum Threat & Post-Quantum Cryptography (PQC)", slide_title_style))
    story.append(Paragraph("Preparing Global Security for Shor's Algorithm", slide_subtitle_style))
    story.append(Spacer(1, 0.15 * inch))

    q1 = [
        Paragraph("<b>1. Shor's Quantum Threat (1994)</b>", slide_subtitle_style),
        Paragraph("• Running on a Cryptographically Relevant Quantum Computer (CRQC), Shor's Algorithm solves prime factoring and discrete logs in <b>polynomial quantum time O(n³)</b>.", bullet_style),
        Paragraph("• <b>Result:</b> Quantum computers will break RSA, DHKE, and ECC simultaneously.", bullet_style),
    ]

    q2 = [
        Paragraph("<b>2. NIST Post-Quantum Standards (2024)</b>", slide_subtitle_style),
        Paragraph("• NIST finalized Post-Quantum Standards based on <b>Lattice Mathematics</b>:", bullet_style),
        Paragraph("• <b>ML-KEM (CRYSTALS-Kyber):</b> PQC Key Encapsulation Mechanism.", bullet_style),
        Paragraph("• <b>ML-DSA (CRYSTALS-Dilithium):</b> PQC Digital Signature Standard.", bullet_style),
        Paragraph("• <b>SLH-DSA (SPHINCS+):</b> Hash-based stateless signature standard.", bullet_style),
    ]

    tq = Table([[q1, q2]], colWidths=[6.0 * inch, 6.0 * inch])
    tq.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), DARK_CARD),
        ('BACKGROUND', (1,0), (1,0), DARK_CARD),
        ('BOX', (0,0), (0,0), 1, BORDER_CYAN),
        ('BOX', (1,0), (1,0), 1, BORDER_CYAN),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(tq)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 10: SUMMARY & CORE ENGINEERING LAWS
    # =========================================================================
    story.append(Paragraph("Summary: Core Laws of Security & Cryptography", slide_title_style))
    story.append(Paragraph("Lessons for Computer Engineers & Cybersecurity Professionals", slide_subtitle_style))
    story.append(Spacer(1, 0.2 * inch))

    laws_content = [
        Paragraph("<b>4 Immutable Engineering Principles of Cryptography</b>", slide_subtitle_style),
        Spacer(1, 0.1 * inch),
        Paragraph("<b>1. Kerckhoffs's Principle:</b> System security must depend solely on key secrecy, NEVER on keeping the algorithm hidden ('Security by Obscurity' fails).", bullet_style),
        Paragraph("<b>2. Mathematics > Hardware:</b> A single architectural flaw (e.g. Enigma's E(x) ≠ x) invalidates billions of key combinations.", bullet_style),
        Paragraph("<b>3. Never Reuse Nonces or Key Material:</b> OTP key reuse (Venona) & AES-GCM nonce reuse reduce stream ciphers to plaintext XOR.", bullet_style),
        Paragraph("<b>4. Don't Roll Your Own Crypto:</b> Always use audited standard implementations (e.g. libsodium, OpenSSL).", bullet_style),
    ]

    t_laws = Table([[laws_content]], colWidths=[12.0 * inch])
    t_laws.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), DARK_CARD),
        ('BOX', (0,0), (0,0), 2, GOLD),
        ('PADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(t_laws)

    # Build Document
    doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background)
    print(f"Successfully generated PDF slide deck at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
