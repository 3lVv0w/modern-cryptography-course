import re

def generate_checklist_slide(stage_num, stage_title, subtitle, items, quiz_q, quiz_a, meter_pct, next_section):
    checklist_items_html = ""
    for label, desc in items:
        checklist_items_html += f"""
                    <div class="checklist-item checked">
                        <div class="check-box">✔</div>
                        <div class="checklist-content">
                            <div class="checklist-label">{label}</div>
                            <div class="checklist-desc">{desc}</div>
                        </div>
                    </div>"""

    quiz_id = f"quiz_drawer_{stage_num}"
    return f"""
        <!-- ===================================================================
             CHECKLIST SLIDE: STAGE {stage_num} REFRESHER
             =================================================================== -->
        <section class="slide" data-slide="CHECKPOINT_{stage_num}" data-section="Stage {stage_num} Checklist">
            <div class="slide-header">
                <span class="slide-tag" style="background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.35); color: var(--accent-emerald);">STAGE {stage_num} CHECKPOINT • KNOWLEDGE RECAP</span>
                <span class="slide-breadcrumb">Progress Check • {meter_pct}% Syllabus Completed</span>
            </div>
            <div class="slide-body">
                <div class="slide-titles">
                    <h2 class="slide-main-title">{stage_title}</h2>
                    <p class="slide-subtitle">{subtitle}</p>
                </div>
                <div class="checklist-layout">
                    <!-- Left: Interactive Checklist Items -->
                    <div class="checklist-items-column">
                        {checklist_items_html}
                    </div>

                    <!-- Right: Progress Status & Quick Self-Test -->
                    <div class="checklist-side-card">
                        <div class="stage-meter-box">
                            <div class="stage-meter-header">
                                <span>STAGE {stage_num} MASTERY</span>
                                <span>{meter_pct}% COMPLETE</span>
                            </div>
                            <div class="stage-meter-bar">
                                <div class="stage-meter-fill" style="width: {meter_pct}%;"></div>
                            </div>
                            <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.45;">
                                ✦ All core axioms in this module have been reviewed.<br>
                                ✦ Click any checkbox to test your recall.<br>
                                ✦ Next up: <strong>{next_section}</strong>
                            </div>
                        </div>

                        <!-- Self-Test Intuition Box -->
                        <div class="quiz-card">
                            <div class="quiz-header">
                                <span>🧠</span> Quick Intuition Check
                            </div>
                            <div class="quiz-question">
                                "{quiz_q}"
                            </div>
                            <button class="quiz-reveal-btn" data-target="{quiz_id}">Show Answer ▼</button>
                            <div class="quiz-answer-drawer" id="{quiz_id}">
                                <strong>Answer:</strong> {quiz_a}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>Checkpoint {stage_num} of 6 • Ready to advance?</span>
                <span class="slide-counter">CHECKPOINT / 38</span>
            </div>
        </section>
"""

def main():
    with open("cryptography_for_beginners_presentation.html", "r") as f:
        html = f.read()

    # 1. Add CSS for checklists before .controls-dock
    checklist_css = """
        /* =====================================================================
           CHECKLIST SLIDE COMPONENTS (INTERACTIVE STAGE RECAPS)
           ===================================================================== */
        .checklist-layout {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: clamp(1.2rem, 2.5vw, 2.8rem);
            align-items: stretch;
            height: 100%;
        }

        .checklist-items-column {
            display: flex;
            flex-direction: column;
            gap: clamp(0.5rem, 1vh, 0.9rem);
            justify-content: center;
        }

        .checklist-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            border-radius: 14px;
            padding: clamp(0.6rem, 1.2vh, 0.95rem) clamp(0.8rem, 1.4vw, 1.2rem);
            cursor: pointer;
            transition: var(--transition-smooth);
        }

        .checklist-item:hover {
            border-color: rgba(6, 182, 212, 0.4);
            background: var(--bg-card-hover);
            transform: translateX(4px);
        }

        .checklist-item.checked {
            border-color: rgba(16, 185, 129, 0.5);
            background: rgba(16, 185, 129, 0.08);
        }

        .check-box {
            width: 22px;
            height: 22px;
            border-radius: 6px;
            border: 2px solid var(--accent-cyan);
            background: rgba(6, 182, 212, 0.1);
            color: var(--accent-cyan);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: 800;
            flex-shrink: 0;
            margin-top: 2px;
            transition: var(--transition-smooth);
        }

        .checklist-item.checked .check-box {
            background: var(--accent-emerald);
            border-color: var(--accent-emerald);
            color: #FFFFFF;
        }

        .checklist-content {
            flex: 1;
        }

        .checklist-label {
            font-family: var(--font-display);
            font-size: clamp(0.92rem, 1.15vw, 1.15rem);
            font-weight: 700;
            color: var(--text-bright);
            line-height: 1.25;
            margin-bottom: 2px;
        }

        .checklist-desc {
            font-size: clamp(0.78rem, 0.95vw, 0.9rem);
            color: var(--text-body);
            line-height: 1.4;
        }

        .checklist-side-card {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 12px;
            height: 100%;
        }

        .stage-meter-box {
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            border-radius: 16px;
            padding: clamp(0.8rem, 1.5vh, 1.4rem);
        }

        .stage-meter-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: var(--accent-cyan);
            font-weight: 600;
        }

        .stage-meter-bar {
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 12px;
        }

        .stage-meter-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-emerald));
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
        }

        .quiz-card {
            background: rgba(14, 20, 36, 0.85);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 16px;
            padding: clamp(0.8rem, 1.5vh, 1.3rem);
            position: relative;
        }

        .quiz-header {
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: var(--font-display);
            font-weight: 700;
            font-size: clamp(0.88rem, 1.1vw, 1.05rem);
            color: var(--accent-gold);
            margin-bottom: 6px;
        }

        .quiz-question {
            font-size: clamp(0.78rem, 0.95vw, 0.92rem);
            color: #E2E8F0;
            line-height: 1.45;
            margin-bottom: 10px;
        }

        .quiz-reveal-btn {
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.4);
            color: var(--accent-gold);
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 0.78rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition-smooth);
        }

        .quiz-reveal-btn:hover {
            background: var(--accent-gold);
            color: #000;
        }

        .quiz-answer-drawer {
            display: none;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px dashed rgba(245, 158, 11, 0.3);
            font-size: clamp(0.75rem, 0.9vw, 0.88rem);
            color: #CBD5E1;
            line-height: 1.4;
        }

        .quiz-answer-drawer.revealed {
            display: block;
        }
    """

    if "/* =====================================================================\n           CHECKLIST SLIDE COMPONENTS" not in html:
        html = html.replace("        /* Floating Controller Dock */", checklist_css + "\n        /* Floating Controller Dock */")

    # Define 6 checklist slides
    chk1 = generate_checklist_slide(
        1,
        "Stage 1 Checkpoint: Foundations & Goals",
        "Make sure these fundamental definitions and security pillars are solid before examining classical ciphers.",
        [
            ("The 4 Security Pillars (CIA+A)", "Can clearly distinguish Confidentiality (AES), Integrity (SHA-256), Authentication (CAs), and Non-Repudiation (Signatures)."),
            ("Encoding vs. Hashing vs. Encryption", "Know that Base64 has zero security, hashing is one-way irreversible, and encryption is two-way with a secret key."),
            ("Adversary Threat Models", "Understand Eve (passive wire listener) vs Mallory (active packet-tampering attacker)."),
            ("Kerckhoffs's Principle", "Understand why algorithms must remain public and open source, while only keys are kept secret.")
        ],
        "An attacker modifies a bank wire transfer from $500 to $50,000 without ever learning the sender's account balance. Which core pillar failed?",
        "Integrity! Confidentiality was preserved because the balance stayed private, but without cryptographic tamper detection (MAC/HMAC), the message was modified.",
        16,
        "Part 2: Classical Ciphers & Lessons from History"
    )

    chk2 = generate_checklist_slide(
        2,
        "Stage 2 Checkpoint: Classical Ciphers & Lessons",
        "Confirm the mathematical insights of historical cryptanalysis before exploring modern symmetric block ciphers.",
        [
            ("Caesar Modular Shift", "Understand modular shift arithmetic C = (P + k) mod 26 and why a 25-key space is trivially brute-forced."),
            ("Frequency Analysis Power", "Understand Al-Kindi's statistical insight: human languages leave fixed letter frequency fingerprints ('E' = 12.7%)."),
            ("Enigma Rotor Flaws", "Know why mechanical rotors created polyalphabetic confusion, but the constraint 'a letter never encrypts to itself' enabled Turing's Bombe."),
            ("The One-Time Pad Paradox", "Understand Shannon's mathematical proof of Perfect Secrecy, and why physical key distribution makes it impractical for the web.")
        ],
        "Why can't we use a 100-character random key to securely encrypt a 1,000-character email using the One-Time Pad?",
        "Shannon's Theorem violation! Repeating the key makes it a polyalphabetic Vigenère cipher vulnerable to statistical cracking. OTP strictly requires |Key| >= |Message|.",
        32,
        "Part 3: Symmetric Cryptography & AES"
    )

    chk3 = generate_checklist_slide(
        3,
        "Stage 3 Checkpoint: Symmetric Ciphers & AES",
        "Double-check your comprehension of block modes, AEAD, and key sharing before entering public-key mathematics.",
        [
            ("Symmetric Shared Secret", "Know that both sender and receiver use the exact same secret key for ultra-fast (10+ GB/s) bulk hardware encryption."),
            ("AES 4-Layer Transformation", "Understand SubBytes (confusion), ShiftRows & MixColumns (diffusion), and AddRoundKey across 14 rounds."),
            ("The ECB Penguin Flaw", "Understand why encrypting identical 16-byte blocks deterministically preserves image outlines and data structures."),
            ("AES-GCM Authenticated Encryption", "Understand why nonces must never repeat, and how Galois auth tags detect bit-flipping attacks in transit.")
        ],
        "What is the single biggest architectural crisis that prevented symmetric encryption from securing the worldwide web alone?",
        "The Key Distribution Problem! Two strangers across the globe cannot safely agree on a shared secret key across the public internet without an eavesdropper intercepting it.",
        50,
        "Part 4: Asymmetric / Public-Key Cryptography"
    )

    chk4 = generate_checklist_slide(
        4,
        "Stage 4 Checkpoint: Public-Key Cryptography",
        "Verify your grasp of asymmetric keypairs, Diffie-Hellman, and RSA before moving to integrity and digital signatures.",
        [
            ("Public vs. Private Key Roles", "Public key encrypts (the open padlock); only the private key decrypts (the physical key in your pocket)."),
            ("Diffie-Hellman Paint Swap", "Public yellow base + private red/blue colors produce orange/green swaps that compute the identical shared brown secret."),
            ("Trapdoor One-Way Mathematics", "Multiplying large primes (n = p * q) is instant; factoring a 600-digit product n back into p and q takes billions of years."),
            ("Elliptic Curve Superiority", "256-bit ECC (Curve25519) provides equivalent security to 3,072-bit RSA with 90% smaller keys and 10x faster execution.")
        ],
        "If Alice encrypts a confidential contract using Bob's public key, can Alice herself decrypt the ciphertext to verify her work?",
        "No! Asymmetric encryption separates locking from unlocking. Once locked with Bob's public key, only Bob's private key can open it.",
        68,
        "Part 5: Message Integrity, Hashes & Digital Signatures"
    )

    chk5 = generate_checklist_slide(
        5,
        "Stage 5 Checkpoint: Hashes, Signatures & PKI",
        "Confirm your understanding of message integrity, signatures, and trust hierarchies before examining TLS 1.3 handshakes.",
        [
            ("Cryptographic Hash Properties", "Deterministic, irreversible, fixed-size (SHA-256 = 256 bits), and pre-image and collision resistant."),
            ("The Avalanche Effect", "Changing 1 bit or character in a large document completely randomizes 50% of the entire output hash."),
            ("Digital Signature Mechanics", "Author encrypts the document hash with their Private Key; any verifier decrypts and checks it with the Public Key."),
            ("PKI & X.509 Certificates", "Certificate Authorities sign domain identities, chaining down to trusted pre-installed operating system Root CAs.")
        ],
        "Why does a digital signature encrypt the SHA-256 hash of a file rather than encrypting the entire 1 GB file with the private key?",
        "Computational speed! Asymmetric math is 1,000x slower than symmetric encryption. Hashing condenses any file into 32 bytes instantly, allowing rapid signing.",
        82,
        "Part 6: Real-World Protocols (TLS 1.3 & E2EE)"
    )

    chk6 = generate_checklist_slide(
        6,
        "Stage 6 Checkpoint: Applied Protocols & Disasters",
        "Review real-world web handshakes, E2EE, and implementation traps before exploring post-quantum security.",
        [
            ("TLS 1.3 Handshake Flow", "1-RTT handshake: Public-key ECDH negotiates session keys, verified by X.509 certs, switching immediately to AES-256-GCM."),
            ("End-to-End Encryption (E2EE)", "Signal & WhatsApp use the Double Ratchet to generate fresh keys per message with Forward Secrecy and self-healing."),
            ("Real-World Catastrophes", "Why math doesn't fail, but code does: Heartbleed (memory leak), PS3 (nonce reuse), and timing side channels."),
            ("Constant-Time Execution", "Cryptographic code must avoid secret-dependent branches or array index lookups that leak data through CPU nanoseconds.")
        ],
        "If a hacker intercepts your web traffic through a rogue public Wi-Fi hotspot on an HTTPS site, what can they see?",
        "Only the server domain name (IP/SNI)! All URLs, paths, passwords, cookies, and page content are fully encrypted by the negotiated TLS session key.",
        92,
        "Part 7: Post-Quantum Cryptography & Best Practices"
    )

    # Insert Checkpoints into HTML at appropriate sections:
    # Checkpoint 1 after Slide 5:
    html = re.sub(
        r'(<section class="slide" data-slide="5"[^>]*>[\s\S]*?</section>)',
        r'\1\n' + chk1,
        html
    )

    # Checkpoint 2 after Slide 10:
    html = re.sub(
        r'(<section class="slide" data-slide="10"[^>]*>[\s\S]*?</section>)',
        r'\1\n' + chk2,
        html
    )

    # Checkpoint 3 after Slide 16:
    html = re.sub(
        r'(<section class="slide" data-slide="16"[^>]*>[\s\S]*?</section>)',
        r'\1\n' + chk3,
        html
    )

    # Checkpoint 4 after Slide 22:
    html = re.sub(
        r'(<section class="slide" data-slide="22"[^>]*>[\s\S]*?</section>)',
        r'\1\n' + chk4,
        html
    )

    # Checkpoint 5 after Slide 26:
    html = re.sub(
        r'(<section class="slide" data-slide="26"[^>]*>[\s\S]*?</section>)',
        r'\1\n' + chk5,
        html
    )

    # Checkpoint 6 after Slide 29:
    html = re.sub(
        r'(<section class="slide" data-slide="29"[^>]*>[\s\S]*?</section>)',
        r'\1\n' + chk6,
        html
    )

    # Now re-number all slides sequentially from 1 to 38
    slide_matches = list(re.finditer(r'<section class="slide([^"]*)" data-slide="([^"]*)" data-section="([^"]*)">', html))
    total_slides = len(slide_matches)
    print(f"Total slides found after insertion: {total_slides}")

    # Renumber in order
    idx = 1
    def replace_slide_tag(m):
        nonlocal idx
        classes = m.group(1)
        section = m.group(3)
        res = f'<section class="slide{classes}" data-slide="{idx}" data-section="{section}">'
        idx += 1
        return res

    html = re.sub(r'<section class="slide([^"]*)" data-slide="([^"]*)" data-section="([^"]*)">', replace_slide_tag, html)

    # Also update slide-counter spans and JavaScript
    html = re.sub(r'<span class="slide-counter">[^<]*</span>', f'<span class="slide-counter">01 / {total_slides}</span>', html)

    # Update JS script with checkbox interactivity and quiz reveal logic
    js_addition = f"""
            // Update individual slide counter spans dynamically
            slides.forEach((slide, idx) => {{
                const counterEl = slide.querySelector('.slide-counter');
                if (counterEl) {{
                    counterEl.textContent = `${{String(idx + 1).padStart(2, '0')}} / ${{totalSlides}}`;
                }}
            }});

            // Interactive Checklists
            document.querySelectorAll('.checklist-item').forEach(item => {{
                item.addEventListener('click', () => {{
                    item.classList.toggle('checked');
                    const box = item.querySelector('.check-box');
                    if (box) {{
                        box.textContent = item.classList.contains('checked') ? '✔' : '';
                    }}
                }});
            }});

            // Quiz Answer Reveal Drawer
            document.querySelectorAll('.quiz-reveal-btn').forEach(btn => {{
                btn.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    const targetId = btn.getAttribute('data-target');
                    const drawer = document.getElementById(targetId);
                    if (drawer) {{
                        drawer.classList.toggle('revealed');
                        btn.textContent = drawer.classList.contains('revealed') ? 'Hide Answer ▲' : 'Show Answer ▼';
                    }}
                }});
            }});
    """

    if "// Interactive Checklists" not in html:
        html = html.replace("            // Initialize\n            updateUI();", js_addition + "\n            // Initialize\n            updateUI();")

    with open("cryptography_for_beginners_presentation.html", "w") as f:
        f.write(html)

    print("Updated cryptography_for_beginners_presentation.html successfully!")

if __name__ == "__main__":
    main()
