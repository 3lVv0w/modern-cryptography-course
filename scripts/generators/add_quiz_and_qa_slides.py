import re

def generate_quiz_slide(quiz_id, tag, title, subtitle, q1_data, q2_data):
    """
    q_data format:
    {
        "prompt": "...",
        "options": [
            ("A. text", True/False, "explanation"),
            ("B. text", True/False, "explanation"),
            ("C. text", True/False, "explanation")
        ]
    }
    """
    def render_q(q_num, data):
        opts_html = ""
        for idx, (opt_text, is_correct, explanation) in enumerate(data["options"]):
            corr_val = "true" if is_correct else "false"
            clean_exp = explanation.replace('"', '&quot;')
            opts_html += f"""
                            <button class="quiz-opt-btn" data-correct="{corr_val}" data-feedback="{clean_exp}">
                                <span>{opt_text}</span>
                            </button>"""
        
        feed_id = f"{quiz_id}_feedback_{q_num}"
        return f"""
                    <div class="interactive-quiz-card">
                        <div>
                            <span class="quiz-badge">QUESTION {q_num}</span>
                            <div class="quiz-prompt" style="margin-top: 8px;">{data["prompt"]}</div>
                        </div>
                        <div class="quiz-options-list">
                            {opts_html}
                        </div>
                        <div class="quiz-feedback" id="{feed_id}"></div>
                    </div>"""

    card1 = render_q(1, q1_data)
    card2 = render_q(2, q2_data)

    return f"""
        <!-- ===================================================================
             QUIZ SLIDE: {quiz_id.upper()}
             =================================================================== -->
        <section class="slide" data-slide="{quiz_id}" data-section="Quiz Challenge">
            <div class="slide-header">
                <span class="slide-tag" style="background: rgba(245, 158, 11, 0.15); border-color: rgba(245, 158, 11, 0.35); color: var(--accent-gold);">{tag}</span>
                <span class="slide-breadcrumb">Interactive Knowledge Check • Click Options to Test</span>
            </div>
            <div class="slide-body">
                <div class="slide-titles">
                    <h2 class="slide-main-title">{title}</h2>
                    <p class="slide-subtitle">{subtitle}</p>
                </div>
                <div class="quiz-arena-grid">
                    {card1}
                    {card2}
                </div>
            </div>
            <div class="slide-footer">
                <span>Click any option to test your understanding</span>
                <span class="slide-counter">QUIZ / 45</span>
            </div>
        </section>
"""

def generate_qa_slide(qa_id, tag, title, subtitle, q1_text, a1_text, q2_text, a2_text):
    return f"""
        <!-- ===================================================================
             Q&A SLIDE: {qa_id.upper()}
             =================================================================== -->
        <section class="slide" data-slide="{qa_id}" data-section="Participant Q&A">
            <div class="slide-header">
                <span class="slide-tag" style="background: rgba(99, 102, 241, 0.15); border-color: rgba(99, 102, 241, 0.35); color: var(--accent-indigo);">{tag}</span>
                <span class="slide-breadcrumb">Frequently Asked Questions • Masterclass Forum</span>
            </div>
            <div class="slide-body">
                <div class="slide-titles">
                    <h2 class="slide-main-title">{title}</h2>
                    <p class="slide-subtitle">{subtitle}</p>
                </div>
                <div class="qa-card-grid">
                    <div class="qa-question-box">
                        <div class="qa-q-header">
                            <span style="font-size: 1.5rem;">❓</span>
                            <span>{q1_text}</span>
                        </div>
                        <div class="qa-answer-text">
                            {a1_text}
                        </div>
                    </div>
                    <div class="qa-question-box">
                        <div class="qa-q-header">
                            <span style="font-size: 1.5rem;">❓</span>
                            <span>{q2_text}</span>
                        </div>
                        <div class="qa-answer-text">
                            {a2_text}
                        </div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>Common Dilemmas & Deep Explanations</span>
                <span class="slide-counter">Q&A / 45</span>
            </div>
        </section>
"""

def main():
    with open("cryptography_for_beginners_presentation.html", "r") as f:
        html = f.read()

    # 1. Add Quiz and Q/A CSS
    quiz_css = """
        /* =====================================================================
           QUIZ & Q/A SLIDE COMPONENTS
           ===================================================================== */
        .quiz-arena-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: clamp(1rem, 2vw, 2rem);
            align-items: stretch;
            height: 100%;
        }

        .interactive-quiz-card {
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            border-radius: 18px;
            padding: clamp(1rem, 1.8vh, 1.5rem);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: clamp(0.5rem, 1vh, 0.8rem);
            backdrop-filter: blur(16px);
            transition: var(--transition-smooth);
        }

        .quiz-badge {
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--accent-gold);
            background: rgba(245, 158, 11, 0.15);
            padding: 3px 10px;
            border-radius: 999px;
            border: 1px solid rgba(245, 158, 11, 0.3);
            display: inline-block;
            align-self: flex-start;
        }

        .quiz-prompt {
            font-family: var(--font-display);
            font-size: clamp(0.92rem, 1.2vw, 1.15rem);
            font-weight: 700;
            color: var(--text-bright);
            line-height: 1.35;
        }

        .quiz-options-list {
            display: flex;
            flex-direction: column;
            gap: 7px;
        }

        .quiz-opt-btn {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 8px 12px;
            color: var(--text-body);
            font-family: var(--font-body);
            font-size: clamp(0.78rem, 0.92vw, 0.88rem);
            text-align: left;
            cursor: pointer;
            transition: var(--transition-smooth);
            display: flex;
            align-items: center;
            gap: 8px;
            line-height: 1.3;
        }

        .quiz-opt-btn:hover {
            border-color: rgba(6, 182, 212, 0.4);
            background: rgba(6, 182, 212, 0.08);
            transform: translateX(4px);
        }

        .quiz-opt-btn.correct {
            background: rgba(16, 185, 129, 0.2) !important;
            border-color: var(--accent-emerald) !important;
            color: #FFFFFF !important;
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.3);
        }

        .quiz-opt-btn.wrong {
            background: rgba(244, 63, 94, 0.2) !important;
            border-color: var(--accent-rose) !important;
            color: #FECDD3 !important;
        }

        .quiz-feedback {
            display: none;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.82rem;
            line-height: 1.4;
            margin-top: 4px;
        }

        .quiz-feedback.show-correct {
            display: block;
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #A7F3D0;
        }

        .quiz-feedback.show-wrong {
            display: block;
            background: rgba(244, 63, 94, 0.12);
            border: 1px solid rgba(244, 63, 94, 0.4);
            color: #FECDD3;
        }

        /* Q/A Forum Cards */
        .qa-card-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: clamp(1rem, 2.5vw, 2.5rem);
            align-items: stretch;
            height: 100%;
        }

        .qa-question-box {
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            border-radius: 18px;
            padding: clamp(1.1rem, 2vh, 1.8rem);
            display: flex;
            flex-direction: column;
            gap: 12px;
            transition: var(--transition-smooth);
        }

        .qa-question-box:hover {
            border-color: rgba(99, 133, 255, 0.4);
            transform: translateY(-3px);
        }

        .qa-q-header {
            display: flex;
            align-items: center;
            gap: 10px;
            font-family: var(--font-display);
            font-size: clamp(1.02rem, 1.25vw, 1.25rem);
            font-weight: 700;
            color: var(--accent-cyan);
            line-height: 1.25;
        }

        .qa-answer-text {
            font-size: clamp(0.82rem, 1vw, 0.95rem);
            color: var(--text-body);
            line-height: 1.55;
        }
    """

    if "/* =====================================================================\n           QUIZ & Q/A SLIDE COMPONENTS" not in html:
        html = html.replace("        /* Floating Controller Dock */", quiz_css + "\n        /* Floating Controller Dock */")

    # Construct the 4 Quiz Slides
    quiz1 = generate_quiz_slide(
        "quiz_classical",
        "PARTICIPANT CHALLENGE • FOUNDATIONS & CLASSICAL",
        "Quick Quiz: Foundations & Classical Ciphers",
        "Test your intuition on basic encoding and letter frequency before moving to symmetric algorithms.",
        {
            "prompt": "A developer encodes user passwords in their database as Base64 strings. What is the fundamental security flaw?",
            "options": [
                ("A. Base64 is merely an encoding scheme with zero keys; anyone can decode it instantly.", True, "Correct! Base64 is not encryption. It is a formatting standard for binary-to-text with zero cryptographic secrecy."),
                ("B. Base64 is vulnerable to letter frequency analysis by Al-Kindi's method.", False, "Incorrect. Base64 doesn't need frequency analysis because there is no secret key to crack—anyone can decode it directly!"),
                ("C. Base64 takes too much CPU computing power to execute.", False, "Incorrect. Base64 is lightning fast, but provides zero confidentiality.")
            ]
        },
        {
            "prompt": "Eve intercepts an ancient monoalphabetic substitution ciphertext. Letter 'Q' appears 13% of the time. What does 'Q' likely represent in English?",
            "options": [
                ("A. The letter 'T' (second most common letter).", False, "Incorrect. While 'T' is common (9.1%), 'E' is the highest at ~12.7%."),
                ("B. The letter 'E' (most frequent letter in natural English).", True, "Correct! English letter 'E' appears ~12.7% of the time. Monoalphabetic substitution preserves this exact frequency distribution!"),
                ("C. The letter 'Z' (least frequent letter).", False, "Incorrect. 'Z' appears only ~0.07% of the time in standard English.")
            ]
        }
    )

    quiz2 = generate_quiz_slide(
        "quiz_symmetric",
        "PARTICIPANT CHALLENGE • SYMMETRIC & BLOCK MODES",
        "Quick Quiz: Symmetric Ciphers & AES",
        "Challenge your understanding of AES, block modes, and the dangers of nonce reuse.",
        {
            "prompt": "Why was the famous 'Linux Tux Penguin' outline still clearly visible when encrypted with AES in ECB mode?",
            "options": [
                ("A. ECB mode deterministically encrypts identical plaintext blocks into identical ciphertext blocks.", True, "Correct! Identical white blocks always produce identical cipher blocks, completely leaking the silhouette of the penguin."),
                ("B. The AES key was too short (under 128 bits).", False, "Incorrect. Even with an unbreakable AES-256 key, ECB mode preserves structural image patterns!"),
                ("C. Tux the Penguin is a vector graphic that bypassed the CPU's AES-NI instruction set.", False, "Incorrect. The vulnerability lies in the Electronic Codebook mode architecture, not the graphic format.")
            ]
        },
        {
            "prompt": "In AES-256-GCM, what catastrophic failure occurs if a developer accidentally reuses the same Nonce with the same key?",
            "options": [
                ("A. The encryption becomes twice as secure due to key accumulation.", False, "Incorrect. Reusing a nonce in GCM is an immediate security catastrophe."),
                ("B. Mallory can recover the internal GHASH authentication key and forge authentic-looking messages.", True, "Correct! Reusing a nonce in AES-GCM allows an attacker to compute the GHASH key and forge message authentication tags."),
                ("C. The operating system kernel immediately crashes.", False, "Incorrect. The code runs normally, but all integrity and authenticity guarantees are completely lost.")
            ]
        }
    )

    quiz3 = generate_quiz_slide(
        "quiz_asymmetric",
        "PARTICIPANT CHALLENGE • ASYMMETRIC & HASHES",
        "Quick Quiz: Public-Key Cryptography & Hashes",
        "Test your grasp of dual-key encryption, digital signatures, and one-way hash properties.",
        {
            "prompt": "Alice wants to send a confidential contract to Bob, and wants Bob to be 100% sure that Alice authored it. Which keys are used?",
            "options": [
                ("A. Encrypt with Alice's Public Key; Sign with Bob's Private Key.", False, "Incorrect. Only Alice can open Alice's public key locks, and Alice does not possess Bob's private key!"),
                ("B. Encrypt with Bob's Public Key; Sign with Alice's Private Key.", True, "Correct! Encrypting with Bob's Public Key ensures only Bob can decrypt (Confidentiality). Signing with Alice's Private Key proves Alice created it (Authentication & Non-Repudiation)."),
                ("C. Encrypt with Bob's Private Key; Sign with Alice's Public Key.", False, "Incorrect. Bob's private key must never be shared, and Alice's public key cannot create signatures!")
            ]
        },
        {
            "prompt": "You compute the SHA-256 hash of a 10 GB operating system installer. Then you flip exactly 1 bit in the file and rehash. What happens?",
            "options": [
                ("A. Only the last hex character of the hash changes.", False, "Incorrect. Hash algorithms do not map changes linearly."),
                ("B. Approximately 50% of all 256 bits flip randomly (The Avalanche Effect).", True, "Correct! Cryptographic hashes exhibit strict Avalanche Effect: any 1-bit change completely randomizes the entire output digest."),
                ("C. The hash remains identical because a 1-bit change in 10 GB is negligible.", False, "Incorrect. Even in a 100 TB file, changing 1 bit completely alters the entire hash!")
            ]
        }
    )

    quiz4 = generate_quiz_slide(
        "quiz_applied",
        "PARTICIPANT CHALLENGE • APPLIED PROTOCOLS",
        "Quick Quiz: TLS Handshakes, E2EE & Traps",
        "Verify your comprehension of modern web handshakes, forward secrecy, and side-channel traps.",
        {
            "prompt": "An attacker records all encrypted TLS 1.3 web traffic passing through a fiber cable today. In 5 years, they steal the web server's private key. Can they decrypt the recorded traffic?",
            "options": [
                ("A. Yes, possessing the server's private key allows decrypting all past traffic.", False, "Incorrect. This was a vulnerability in older RSA key exchanges, but TLS 1.3 strictly prevents this!"),
                ("B. No! TLS 1.3 mandates Forward Secrecy via ephemeral ECDH keys that were erased immediately after the session.", True, "Correct! Ephemeral Diffie-Hellman session keys are destroyed after each connection, ensuring stolen long-term private keys cannot decrypt past sessions."),
                ("C. Yes, but only if the user was using Google Chrome.", False, "Incorrect. Forward secrecy is built into the protocol standard across all browsers.")
            ]
        },
        {
            "prompt": "Why must password verification in backend server code use constant-time comparison (e.g. crypto.timingSafeEqual)?",
            "options": [
                ("A. Standard string comparison leaks secret characters by terminating early upon the first mismatched byte (Timing Attack).", True, "Correct! An attacker measuring nanosecond response times can guess passwords character-by-character if comparison time varies."),
                ("B. Constant-time algorithms execute 100x faster than standard string comparisons.", False, "Incorrect. Constant-time checks actually do slightly more work to ensure uniform execution duration."),
                ("C. Standard string comparisons cause memory buffer overflows.", False, "Incorrect. The vulnerability is a timing side-channel leak, not a buffer overflow.")
            ]
        }
    )

    # Construct the 3 Q/A Forum Slides
    qa1 = generate_qa_slide(
        "qa_hybrid_crypto",
        "FORUM • CRITICAL PARADOXES",
        "Participant Q&A: Fundamental Cryptographic Mysteries",
        "Detailed answers to the questions computer science students and engineers ask most.",
        "If Asymmetric Cryptography (RSA/ECC) is so powerful, why don't we encrypt all files and videos with it?",
        "<strong>The Hybrid Cryptography Solution:</strong><br/>Asymmetric mathematics involves heavy modular exponentiation and complex point addition on elliptic curves. It is approximately <strong>1,000 to 10,000 times slower</strong> than symmetric encryption.<br/><br/>Modern protocols solve this elegantly by combining them: Asymmetric crypto (ECDH) is used for 5 milliseconds at the start to safely agree on a temporary symmetric key. Then, ultra-fast hardware-accelerated <strong>AES-256-GCM</strong> takes over to stream bulk video at 10+ GB per second!",
        "Can a supercomputer or quantum computer ever reverse a SHA-256 hash back to the original plaintext?",
        "<strong>Mathematical Impossibility (Lossy Compression):</strong><br/>Cryptographic hashes are one-way compression functions. A 10 GB video file is condensed down to a fixed <strong>256 bits (32 bytes)</strong>.<br/><br/>Because an infinite number of different files compress to the exact same 256-bit hash, there is no unique original input to 'reverse' back to. You cannot mathematically reconstitute 10 gigabytes of data out of 32 bytes of information. Hashes are permanently irreversible."
    )

    qa2 = generate_qa_slide(
        "qa_network_pki",
        "FORUM • REAL-WORLD NETWORK SECURITY",
        "Participant Q&A: Public Wi-Fi & Certificate Trust",
        "Understanding what HTTPS encrypts and how the global web of trust detects rogue authorities.",
        "When I use HTTPS on public coffee shop Wi-Fi, what can the hacker sitting next to me see?",
        "<strong>Only Domain Metadata, Never Private Content:</strong><br/>The hacker can see which server IP and domain name you connect to (e.g. <code>bankofamerica.com</code>) via unencrypted DNS queries or TLS Server Name Indication (SNI).<br/><br/>However, all specific page URLs (<code>/account/transfer</code>), passwords, credit card numbers, form inputs, session cookies, and message contents are <strong>100% encrypted</strong> inside the TLS tunnel. They see only scrambled AES ciphertext.",
        "What prevents a rogue Certificate Authority (or authoritarian government) from issuing a fake certificate for Google?",
        "<strong>Certificate Transparency (CT) Logs:</strong><br/>Modern web browsers mandate Certificate Transparency. Every valid certificate must be recorded in publicly verifiable, append-only, tamper-proof audit ledgers.<br/><br/>Google and security researchers monitor CT logs in real-time. If an unauthorized CA issues a fraudulent certificate for <code>google.com</code>, it is detected within minutes, and all browsers immediately blacklist the offending CA worldwide."
    )

    qa3 = generate_qa_slide(
        "qa_open_floor",
        "FORUM • OPEN PARTICIPANT DISCUSSION",
        "Participant Q&A: Open Floor & Architectural Debates",
        "Engaging prompts for workshop discussions, security engineering reviews, and classroom debates.",
        "Debate: Should governments have a cryptographic backdoor for national security?",
        "<strong>The Engineering Consensus:</strong><br/>Cryptographers almost universally agree: <em>there is no such thing as a backdoor that only 'good guys' can open</em>.<br/><br/>A backdoor is simply an intentional mathematical vulnerability. If an encryption algorithm has a master bypass key, it becomes the ultimate target for foreign adversaries, rogue insiders, and hackers. Weakening cryptography for law enforcement destroys the security of banking, energy grids, and private citizens.",
        "Architectural Readiness: How should engineering teams prepare for Post-Quantum Cryptography (PQC)?",
        "<strong>Adopt Cryptographic Agility Now:</strong><br/>Organizations must decouple their applications from hardcoded RSA/ECC algorithms.<br/><br/>1. Audit where public-key cryptography is stored in databases and certificates.<br/>2. Transition to hybrid key exchanges (combining X25519 with NIST's <strong>ML-KEM / Kyber</strong>).<br/>3. Ensure communication buffers can handle larger quantum-resistant public keys and signatures."
    )

    # Insertion strategy:
    # 1. Insert quiz1 after Checkpoint 2 (Stage 2 Checklist)
    html = re.sub(
        r'(<section class="slide"[^>]*data-section="Stage 2 Checklist"[^>]*>[\s\S]*?</section>)',
        r'\1\n' + quiz1,
        html
    )

    # 2. Insert quiz2 after Checkpoint 3 (Stage 3 Checklist)
    html = re.sub(
        r'(<section class="slide"[^>]*data-section="Stage 3 Checklist"[^>]*>[\s\S]*?</section>)',
        r'\1\n' + quiz2,
        html
    )

    # 3. Insert quiz3 after Checkpoint 5 (Stage 5 Checklist)
    html = re.sub(
        r'(<section class="slide"[^>]*data-section="Stage 5 Checklist"[^>]*>[\s\S]*?</section>)',
        r'\1\n' + quiz3,
        html
    )

    # 4. Insert quiz4 after Checkpoint 6 (Stage 6 Checklist)
    html = re.sub(
        r'(<section class="slide"[^>]*data-section="Stage 6 Checklist"[^>]*>[\s\S]*?</section>)',
        r'\1\n' + quiz4,
        html
    )

    # 5. Insert qa1, qa2, qa3 before Conclusion slide (Slide with data-section="Conclusion")
    qa_block = qa1 + "\n" + qa2 + "\n" + qa3
    html = re.sub(
        r'(<section class="slide"[^>]*data-section="Conclusion"[^>]*>)',
        qa_block + r'\n\1',
        html
    )

    # Renumber all slides sequentially
    slide_matches = list(re.finditer(r'<section class="slide([^"]*)" data-slide="([^"]*)" data-section="([^"]*)">', html))
    total_slides = len(slide_matches)
    print(f"Total slides found after inserting Quiz & Q/A: {total_slides}")

    idx = 1
    def replace_slide_tag(m):
        nonlocal idx
        classes = m.group(1)
        section = m.group(3)
        res = f'<section class="slide{classes}" data-slide="{idx}" data-section="{section}">'
        idx += 1
        return res

    html = re.sub(r'<section class="slide([^"]*)" data-slide="([^"]*)" data-section="([^"]*)">', replace_slide_tag, html)

    # Update slide-counter spans
    html = re.sub(r'<span class="slide-counter">[^<]*</span>', f'<span class="slide-counter">01 / {total_slides}</span>', html)

    # Interactive Quiz JavaScript logic
    quiz_js = """
            // Interactive Multiple-Choice Quizzes
            document.querySelectorAll('.quiz-opt-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const card = btn.closest('.interactive-quiz-card');
                    if (!card) return;

                    // Deselect previous
                    card.querySelectorAll('.quiz-opt-btn').forEach(b => {
                        b.classList.remove('correct', 'wrong');
                    });

                    const isCorrect = btn.getAttribute('data-correct') === 'true';
                    const feedbackText = btn.getAttribute('data-feedback');
                    const feedbackEl = card.querySelector('.quiz-feedback');

                    if (isCorrect) {
                        btn.classList.add('correct');
                        if (feedbackEl) {
                            feedbackEl.className = 'quiz-feedback show-correct';
                            feedbackEl.innerHTML = `<strong>✔ Correct!</strong> ${feedbackText}`;
                        }
                    } else {
                        btn.classList.add('wrong');
                        if (feedbackEl) {
                            feedbackEl.className = 'quiz-feedback show-wrong';
                            feedbackEl.innerHTML = `<strong>✘ Not quite!</strong> ${feedbackText}`;
                        }
                    }
                });
            });
    """

    if "// Interactive Multiple-Choice Quizzes" not in html:
        html = html.replace("// Interactive Checklists", quiz_js + "\n            // Interactive Checklists")

    with open("cryptography_for_beginners_presentation.html", "w") as f:
        f.write(html)

    print("Updated cryptography_for_beginners_presentation.html with 45 slides successfully!")

if __name__ == "__main__":
    main()
