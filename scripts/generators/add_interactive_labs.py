import re

def main():
    with open("cryptography_for_beginners_presentation.html", "r") as f:
        html = f.read()

    # 1. Add CSS for all 7 Interactive Labs
    labs_css = """
        /* =====================================================================
           INTERACTIVE LABS & INFOGRAPHIC ANIMATIONS
           ===================================================================== */
        .lab-container {
            display: flex;
            flex-direction: column;
            gap: clamp(0.6rem, 1.2vh, 1rem);
            height: 100%;
            justify-content: center;
        }

        .lab-input-row {
            display: flex;
            align-items: center;
            gap: 12px;
            background: var(--bg-card);
            border: 1px solid var(--bg-card-border);
            padding: 8px 14px;
            border-radius: 12px;
        }

        .lab-text-input {
            flex: 1;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 8px 14px;
            color: var(--text-bright);
            font-family: var(--font-mono);
            font-size: 0.9rem;
            outline: none;
            transition: var(--transition-smooth);
        }

        body.light-theme .lab-text-input {
            background: #FFFFFF;
            border-color: rgba(15, 23, 42, 0.15);
            color: #0F172A;
        }

        .lab-text-input:focus {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
        }

        .lab-btn {
            background: rgba(6, 182, 212, 0.15);
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
            padding: 7px 14px;
            border-radius: 8px;
            font-family: var(--font-display);
            font-size: 0.82rem;
            font-weight: 700;
            cursor: pointer;
            transition: var(--transition-smooth);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .lab-btn:hover {
            background: var(--accent-cyan);
            color: #000;
            transform: translateY(-2px);
        }

        body.light-theme .lab-btn {
            background: rgba(2, 132, 199, 0.1);
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }

        body.light-theme .lab-btn:hover {
            background: var(--accent-cyan);
            color: #FFF;
        }

        .lab-btn.accent-gold {
            border-color: var(--accent-gold);
            color: var(--accent-gold);
            background: rgba(245, 158, 11, 0.15);
        }

        .lab-btn.accent-gold:hover {
            background: var(--accent-gold);
            color: #000;
        }

        .lab-btn.accent-emerald {
            border-color: var(--accent-emerald);
            color: var(--accent-emerald);
            background: rgba(16, 185, 129, 0.15);
        }

        .lab-btn.accent-emerald:hover {
            background: var(--accent-emerald);
            color: #000;
        }

        .code-box-display {
            font-family: var(--font-mono);
            font-size: 0.82rem;
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 8px 12px;
            color: var(--accent-cyan);
            word-break: break-all;
            min-height: 38px;
            display: flex;
            align-items: center;
        }

        body.light-theme .code-box-display {
            background: #F1F5F9;
            border-color: rgba(15, 23, 42, 0.1);
            color: #0369A1;
        }

        /* 8x8 Pixel Grid for ECB vs GCM */
        .pixel-matrix-grid {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 4px;
            width: 190px;
            height: 190px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 6px;
            margin: 0 auto;
        }

        .pixel-cell {
            border-radius: 3px;
            transition: all 0.3s ease;
        }

        /* 16x16 Avalanche Heatmap Matrix */
        .avalanche-heatmap-grid {
            display: grid;
            grid-template-columns: repeat(16, 1fr);
            gap: 3px;
            width: 100%;
            max-width: 320px;
            height: 190px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 6px;
            margin: 0 auto;
        }

        .bit-cell {
            border-radius: 2px;
            background: #1E293B;
            transition: background-color 0.25s ease, transform 0.25s ease;
        }

        .bit-cell.flipped {
            background: #F59E0B;
            box-shadow: 0 0 6px #F59E0B;
            transform: scale(1.08);
        }

        /* Color Mixing Swatches */
        .paint-swatch {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
        }

        /* Animated Handshake Network Wire */
        .handshake-wire-container {
            position: relative;
            width: 100%;
            height: 120px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 30px;
        }

        .wire-track {
            position: absolute;
            left: 90px;
            right: 90px;
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
        }

        body.light-theme .wire-track {
            background: rgba(15, 23, 42, 0.1);
        }

        .wire-packet-dot {
            position: absolute;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: var(--accent-cyan);
            box-shadow: 0 0 14px var(--accent-cyan);
            top: -9px;
            left: 0;
            transition: left 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
        }
    """

    if "/* =====================================================================\n           INTERACTIVE LABS" not in html:
        html = html.replace("        /* Floating Controller Dock */", labs_css + "\n        /* Floating Controller Dock */")

    # LAB 1: Crypto Triad
    lab1_html = """
        <!-- ===================================================================
             INTERACTIVE LAB 1: THE CRYPTOGRAPHIC TRIAD
             =================================================================== -->
        <section class="slide" data-slide="lab1" data-section="Interactive Lab 1">
            <div class="slide-header">
                <span class="slide-tag" style="background: rgba(6, 182, 212, 0.15); border-color: rgba(6, 182, 212, 0.35); color: var(--accent-cyan);">⚡ LIVE LAB 01 • REAL-TIME CONVERTER</span>
                <span class="slide-breadcrumb">Encoding vs Hashing vs Encryption in Action</span>
            </div>
            <div class="slide-body">
                <div class="slide-titles">
                    <h2 class="slide-main-title">Interactive Lab: Encoding vs. Hashing vs. Encryption</h2>
                    <p class="slide-subtitle">Type any text below to watch how the 3 fundamental operations process your message in real-time:</p>
                </div>
                <div class="lab-container">
                    <div class="lab-input-row">
                        <span style="font-weight: 700; font-family: var(--font-mono); color: var(--accent-cyan);">INPUT PLAINTEXT:</span>
                        <input type="text" id="triadInput" class="lab-text-input" value="Antigravity 2026">
                        <span style="font-size: 0.8rem; color: var(--text-muted);">Live WebCrypto Engine</span>
                    </div>

                    <div class="layout-grid-3">
                        <!-- Column 1: Base64 -->
                        <div class="pres-card">
                            <span class="card-badge" style="background: rgba(6, 182, 212, 0.2); color: var(--accent-cyan);">1. ENCODING (BASE64)</span>
                            <div class="code-box-display" id="triadBase64">QW50aWdyYXZpdHkgMjAyNg==</div>
                            <p class="card-desc">Zero security. Notice anyone can decode it instantly without asking for a password!</p>
                            <button class="lab-btn" id="btnDecodeBase64">Test Reversal (No Key) ➔</button>
                            <div id="base64ReversalResult" style="font-size: 0.8rem; color: var(--accent-cyan); height: 18px;"></div>
                        </div>

                        <!-- Column 2: SHA-256 -->
                        <div class="pres-card">
                            <span class="card-badge" style="background: rgba(16, 185, 129, 0.2); color: var(--accent-emerald);">2. HASHING (SHA-256)</span>
                            <div class="code-box-display" id="triadHash" style="color: var(--accent-emerald); font-size: 0.72rem;">computing...</div>
                            <p class="card-desc">Irreversible digital fingerprint. Exactly 256 bits. Permanent compression—mathematically impossible to undo.</p>
                            <div class="callout-box" style="padding: 6px 10px; font-size: 0.75rem;">
                                ✔ 1-Way Only • Fixed 32 Bytes
                            </div>
                        </div>

                        <!-- Column 3: AES Simulation -->
                        <div class="pres-card featured">
                            <span class="card-badge" style="background: rgba(245, 158, 11, 0.2); color: var(--accent-gold);">3. ENCRYPTION (AES-256)</span>
                            <div class="code-box-display" id="triadCipher" style="color: var(--accent-gold);">8f4a2c09ef78b...</div>
                            <p class="card-desc">Scrambled with secret key. Reversible ONLY when the recipient enters the matching key!</p>
                            <div style="display: flex; gap: 8px;">
                                <button class="lab-btn accent-gold" id="btnToggleAES">🔓 Decrypt with Key</button>
                                <span id="aesStateText" style="font-size: 0.8rem; color: var(--accent-gold); align-self: center;">Status: Encrypted</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>Experiment: Change the text input above to see outputs adapt</span>
                <span class="slide-counter">LAB / 52</span>
            </div>
        </section>
"""

    # LAB 2: Caesar Rotor & Frequency Spectrum
    lab2_html = """
        <!-- ===================================================================
             INTERACTIVE LAB 2: CAESAR SHIFT & FREQUENCY SPECTRUM
             =================================================================== -->
        <section class="slide" data-slide="lab2" data-section="Interactive Lab 2">
            <div class="slide-header">
                <span class="slide-tag" style="background: rgba(6, 182, 212, 0.15); border-color: rgba(6, 182, 212, 0.35); color: var(--accent-cyan);">⚙️ LIVE LAB 02 • CAESAR WHEEL & FREQUENCY</span>
                <span class="slide-breadcrumb">Slide the Shift Key to See Frequency Analysis Shift</span>
            </div>
            <div class="slide-body">
                <div class="slide-titles">
                    <h2 class="slide-main-title">Interactive Caesar Wheel & Live Frequency Spectrum</h2>
                    <p class="slide-subtitle">Drag the shift key slider to rotate the substitution alphabet and watch English letter frequency shift with it:</p>
                </div>
                <div class="lab-container">
                    <div class="lab-input-row">
                        <span style="font-weight: 700; font-family: var(--font-mono); color: var(--accent-cyan);">SHIFT KEY (k):</span>
                        <input type="range" id="caesarSlider" min="0" max="25" value="3" style="flex: 1; accent-color: var(--accent-cyan); cursor: pointer;">
                        <span id="caesarKeyLabel" style="font-family: var(--font-mono); font-weight: 800; color: var(--accent-cyan); min-width: 100px;">k = 3 (D)</span>
                    </div>

                    <div class="layout-split-equal">
                        <!-- Left: Live Caesar Conversion -->
                        <div class="pres-card">
                            <h4 style="color: var(--accent-cyan); margin-bottom: 6px;">Plaintext Input:</h4>
                            <input type="text" id="caesarPlainInput" class="lab-text-input" value="THE SECRET TREASURE IS BURIED AT DAWN" style="width: 100%; margin-bottom: 8px;">
                            
                            <h4 style="color: var(--accent-gold); margin-bottom: 6px;">Ciphertext Output:</h4>
                            <div class="code-box-display" id="caesarCipherOutput" style="color: var(--accent-gold); font-size: 0.95rem; font-weight: 700;">WKX VHFUHW WUHDVXUH LV EXULHG DW GDZQ</div>
                            
                            <div style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--text-muted); margin-top: 8px;">
                                Mapping: A➔<span id="mapA" style="color:var(--accent-cyan);">D</span> | E➔<span id="mapE" style="color:var(--accent-cyan);">H</span> | T➔<span id="mapT" style="color:var(--accent-cyan);">W</span>
                            </div>
                        </div>

                        <!-- Right: Live Letter Frequency Visualizer -->
                        <div class="pres-card featured">
                            <h4 style="color: var(--text-bright); margin-bottom: 6px;">Live Ciphertext Letter Frequency:</h4>
                            <p class="card-desc" style="font-size: 0.78rem;">Notice how the highest peak (English 'E' at 12.7%) moves directly to the shifted letter:</p>
                            
                            <!-- SVG Frequency Bars -->
                            <div id="caesarFreqBars" style="display: flex; align-items: flex-end; gap: 4px; height: 95px; background: rgba(0,0,0,0.3); border-radius: 8px; padding: 8px 10px; border: 1px solid rgba(255,255,255,0.08);">
                                <!-- Populated dynamically by JS -->
                            </div>
                            <div style="font-size: 0.75rem; color: var(--accent-cyan); margin-top: 6px; text-align: center;">
                                ✦ Al-Kindi's attack: Locate the tallest bar ➔ Subtract its position ➔ Key cracked!
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>Drag slider k from 0 to 25 to see the frequency peaks shift dynamically</span>
                <span class="slide-counter">LAB / 52</span>
            </div>
        </section>
"""

    # LAB 3: ECB Penguin Matrix Simulator
    lab3_html = """
        <!-- ===================================================================
             INTERACTIVE LAB 3: AES MODES & THE ECB PENGUIN SIMULATOR
             =================================================================== -->
        <section class="slide" data-slide="lab3" data-section="Interactive Lab 3">
            <div class="slide-header">
                <span class="slide-tag" style="background: rgba(244, 63, 94, 0.15); border-color: rgba(244, 63, 94, 0.35); color: var(--accent-rose);">🐧 LIVE LAB 03 • AES MODES SIMULATOR</span>
                <span class="slide-breadcrumb">Witness Why ECB Leaks Image Outlines</span>
            </div>
            <div class="slide-body">
                <div class="slide-titles">
                    <h2 class="slide-main-title">Interactive Simulator: ECB vs. CBC/GCM Pattern Leak</h2>
                    <p class="slide-subtitle">Switch between ECB (naive deterministic blocks) and modern GCM (randomized nonce) to see what happens to data patterns:</p>
                </div>
                <div class="lab-container">
                    <div class="layout-split">
                        <!-- Left: Matrix Display -->
                        <div class="pres-card" style="text-align: center;">
                            <h4 id="matrixModeTitle" style="color: var(--accent-rose); margin-bottom: 8px;">Mode: AES-ECB (Electronic Codebook)</h4>
                            <div class="pixel-matrix-grid" id="pixelMatrix">
                                <!-- 64 pixels generated by JS -->
                            </div>
                            <div id="matrixStatusBanner" class="callout-box warning" style="margin-top: 10px; font-size: 0.8rem; padding: 6px 10px;">
                                ⚠️ <strong>PATTERN VISIBLE:</strong> Identical blocks produce identical ciphertext colors!
                            </div>
                        </div>

                        <!-- Right: Controls & Technical Rationale -->
                        <div class="pres-card featured">
                            <h3 class="card-title">Choose AES Operational Mode:</h3>
                            <div style="display: flex; gap: 10px; margin: 10px 0;">
                                <button class="lab-btn" id="btnSelectECB" style="border-color: var(--accent-rose); color: var(--accent-rose);">❌ AES-ECB Mode</button>
                                <button class="lab-btn accent-emerald" id="btnSelectGCM">✔ AES-GCM (AEAD)</button>
                            </div>
                            <p class="card-desc" id="modeExplanationText">
                                <strong>Electronic Codebook (ECB)</strong> encrypts each 16-byte block independently. Every white pixel block turns into the exact same cipher block, preserving the penguin outline!
                            </p>
                            <div class="callout-box" style="margin-top: 10px; font-size: 0.8rem;">
                                <strong>The Fix:</strong> Modern AES-GCM uses a unique randomized 96-bit <em>Initialization Vector (Nonce)</em> for every block, spreading pure visual white-noise entropy.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>Click between ECB and GCM to observe instantaneous pattern diffusion</span>
                <span class="slide-counter">LAB / 52</span>
            </div>
        </section>
"""

    # LAB 4: Diffie-Hellman Color Mixing Simulator
    lab4_html = """
        <!-- ===================================================================
             INTERACTIVE LAB 4: DIFFIE-HELLMAN COLOR MIXING
             =================================================================== -->
        <section class="slide" data-slide="lab4" data-section="Interactive Lab 4">
            <div class="slide-header">
                <span class="slide-tag" style="background: rgba(245, 158, 11, 0.15); border-color: rgba(245, 158, 11, 0.35); color: var(--accent-gold);">🎨 LIVE LAB 04 • KEY EXCHANGE SIMULATOR</span>
                <span class="slide-breadcrumb">Agreeing on a Shared Secret Over an Insecure Line</span>
            </div>
            <div class="slide-body">
                <div class="slide-titles">
                    <h2 class="slide-main-title">Interactive Diffie-Hellman Color Mixing Simulator</h2>
                    <p class="slide-subtitle">Step through the mathematical paint-mixing protocol to see how Alice and Bob compute the exact same secret key:</p>
                </div>
                <div class="lab-container">
                    <div class="layout-grid-3">
                        <!-- Alice Node -->
                        <div class="pres-card" style="border-top: 3px solid var(--accent-cyan); text-align: center;">
                            <h4 style="color: var(--accent-cyan);">Alice (Private Secret)</h4>
                            <div style="display: flex; justify-content: center; gap: 12px; margin: 10px 0;">
                                <div>
                                    <div class="paint-swatch" id="aliceSecretSwatch" style="background: #EF4444; margin: 0 auto;"></div>
                                    <span style="font-size: 0.72rem; color: var(--text-muted);">Secret: Red</span>
                                </div>
                                <div style="align-self: center; font-size: 1.2rem;">+</div>
                                <div>
                                    <div class="paint-swatch" style="background: #EAB308; margin: 0 auto;"></div>
                                    <span style="font-size: 0.72rem; color: var(--text-muted);">Public: Yellow</span>
                                </div>
                            </div>
                            <div style="font-size: 0.8rem; color: var(--text-bright); margin-top: 6px;">
                                Alice's Public Mix: <strong style="color: #F97316;">Orange</strong>
                            </div>
                        </div>

                        <!-- Public Insecure Channel (Eve) -->
                        <div class="pres-card" style="border-top: 3px solid var(--accent-gold); text-align: center; background: rgba(0,0,0,0.4);">
                            <h4 style="color: var(--accent-gold);">Public Wire (Eve Eavesdropping)</h4>
                            <p class="card-desc" style="font-size: 0.78rem;">Eve sees the swapped mixed colors crossing the line:</p>
                            <div style="display: flex; justify-content: center; gap: 16px; margin: 10px 0;">
                                <div class="paint-swatch" id="eveWireLeft" style="background: #F97316;"></div>
                                <div style="align-self: center; color: var(--accent-gold); font-weight: 800;">⇄</div>
                                <div class="paint-swatch" id="eveWireRight" style="background: #10B981;"></div>
                            </div>
                            <div style="font-size: 0.75rem; color: var(--accent-gold);">
                                Eve cannot unmix Orange or Teal back to private colors!
                            </div>
                        </div>

                        <!-- Bob Node -->
                        <div class="pres-card" style="border-top: 3px solid var(--accent-blue); text-align: center;">
                            <h4 style="color: var(--accent-blue);">Bob (Private Secret)</h4>
                            <div style="display: flex; justify-content: center; gap: 12px; margin: 10px 0;">
                                <div>
                                    <div class="paint-swatch" id="bobSecretSwatch" style="background: #3B82F6; margin: 0 auto;"></div>
                                    <span style="font-size: 0.72rem; color: var(--text-muted);">Secret: Blue</span>
                                </div>
                                <div style="align-self: center; font-size: 1.2rem;">+</div>
                                <div>
                                    <div class="paint-swatch" style="background: #EAB308; margin: 0 auto;"></div>
                                    <span style="font-size: 0.72rem; color: var(--text-muted);">Public: Yellow</span>
                                </div>
                            </div>
                            <div style="font-size: 0.8rem; color: var(--text-bright); margin-top: 6px;">
                                Bob's Public Mix: <strong style="color: #10B981;">Teal</strong>
                            </div>
                        </div>
                    </div>

                    <!-- Final Secret Calculation Row -->
                    <div class="pres-card featured" style="display: flex; flex-direction: row; justify-content: space-between; align-items: center; padding: 12px 20px;">
                        <button class="lab-btn accent-emerald" id="btnDHComputeFinal" style="font-size: 0.9rem; padding: 10px 18px;">
                            ✨ Step 3: Compute Final Shared Secret ➔
                        </button>
                        <div style="display: flex; align-items: center; gap: 14px;">
                            <div style="text-align: right; font-size: 0.85rem;">
                                <strong>Derived Shared Key:</strong><br>
                                <span style="font-family: var(--font-mono); color: var(--accent-emerald);" id="dhKeyHex">K = g^(ab) mod p</span>
                            </div>
                            <div class="paint-swatch" id="dhFinalSecretSwatch" style="background: #334155; width: 44px; height: 44px;"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>Click the Compute button to simulate Alice and Bob deriving identical keys</span>
                <span class="slide-counter">LAB / 52</span>
            </div>
        </section>
"""

    # LAB 5: Real-Time Avalanche Bit-Heatmap
    lab5_html = """
        <!-- ===================================================================
             INTERACTIVE LAB 5: SHA-256 AVALANCHE BIT-HEATMAP
             =================================================================== -->
        <section class="slide" data-slide="lab5" data-section="Interactive Lab 5">
            <div class="slide-header">
                <span class="slide-tag" style="background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.35); color: var(--accent-emerald);">⚡ LIVE LAB 05 • 256-BIT HEATMAP</span>
                <span class="slide-breadcrumb">Watch 50% of Bits Explode Over 1 Changed Character</span>
            </div>
            <div class="slide-body">
                <div class="slide-titles">
                    <h2 class="slide-main-title">Interactive SHA-256 Avalanche Bit-Heatmap</h2>
                    <p class="slide-subtitle">Type into either box below. Changing even one character recalculates both 256-bit hashes and displays which bits flip:</p>
                </div>
                <div class="lab-container">
                    <div class="layout-split">
                        <!-- Left: Live Inputs & Stats -->
                        <div style="display: flex; flex-direction: column; gap: 10px;">
                            <div class="pres-card">
                                <span style="font-size: 0.75rem; color: var(--accent-cyan); font-weight: 700;">INPUT MESSAGE 1:</span>
                                <input type="text" id="avalancheIn1" class="lab-text-input" value="AntigravitySecurity1" style="width: 100%; margin: 4px 0;">
                                <div class="code-box-display" id="avalancheHash1" style="font-size: 0.7rem; color: var(--accent-cyan);">hashing...</div>
                            </div>
                            <div class="pres-card">
                                <span style="font-size: 0.75rem; color: var(--accent-rose); font-weight: 700;">INPUT MESSAGE 2 (Differing by 1 Char):</span>
                                <input type="text" id="avalancheIn2" class="lab-text-input" value="AntigravitySecurity2" style="width: 100%; margin: 4px 0;">
                                <div class="code-box-display" id="avalancheHash2" style="font-size: 0.7rem; color: var(--accent-gold);">hashing...</div>
                            </div>
                            <!-- Live Metric Box -->
                            <div class="pres-card featured" style="padding: 10px 14px; text-align: center;">
                                <div style="font-size: 0.75rem; color: var(--text-muted);">LIVE AVALANCHE METRIC</div>
                                <div style="font-family: var(--font-display); font-size: 1.6rem; font-weight: 800; color: var(--accent-gold);" id="avalancheRateText">128 / 256 Bits Flipped (50.0%)</div>
                                <div style="font-size: 0.75rem; color: var(--accent-emerald);">✔ Strict Cryptographic Diffusion Benchmark Met</div>
                            </div>
                        </div>

                        <!-- Right: 16x16 Bit Heatmap Grid -->
                        <div class="pres-card" style="text-align: center;">
                            <h4 style="color: var(--text-bright); margin-bottom: 6px;">256-Bit Avalanche Heatmap</h4>
                            <p class="card-desc" style="font-size: 0.75rem; margin-bottom: 8px;">Amber squares represent bits that flipped between Hash 1 and Hash 2:</p>
                            <div class="avalanche-heatmap-grid" id="avalancheGrid">
                                <!-- 256 bit cells populated by JS -->
                            </div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); margin-top: 6px;">
                                🟩 Unchanged Bit &nbsp;&nbsp;|&nbsp;&nbsp; 🟨 Flipped Bit (~50% target)
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>Edit either input string to watch the 256-bit heatmap re-randomize in real time</span>
                <span class="slide-counter">LAB / 52</span>
            </div>
        </section>
"""

    # LAB 6: 4-Step Animated TLS 1.3 Handshake Simulator
    lab6_html = """
        <!-- ===================================================================
             INTERACTIVE LAB 6: ANIMATED TLS 1.3 HANDSHAKE
             =================================================================== -->
        <section class="slide" data-slide="lab6" data-section="Interactive Lab 6">
            <div class="slide-header">
                <span class="slide-tag" style="background: rgba(59, 130, 246, 0.15); border-color: rgba(59, 130, 246, 0.35); color: var(--accent-blue);">🌐 LIVE LAB 06 • HANDSHAKE ANIMATOR</span>
                <span class="slide-breadcrumb">Step-by-Step 1-RTT Packet Exchange</span>
            </div>
            <div class="slide-body">
                <div class="slide-titles">
                    <h2 class="slide-main-title">Interactive TLS 1.3 Handshake Packet Simulator</h2>
                    <p class="slide-subtitle">Click 'Next Step' or 'Auto Play' to trace the cryptographic handshake packets travelling across the network wire:</p>
                </div>
                <div class="lab-container">
                    <!-- Network Wire Canvas -->
                    <div class="pres-card" style="padding: 14px 20px;">
                        <div class="handshake-wire-container">
                            <div style="text-align: center; z-index: 2;">
                                <div style="font-size: 2rem;">💻</div>
                                <strong style="color: var(--accent-cyan); font-size: 0.85rem;">Client (Browser)</strong>
                            </div>
                            
                            <div class="wire-track">
                                <div class="wire-packet-dot" id="handshakeDot"></div>
                            </div>

                            <div style="text-align: center; z-index: 2;">
                                <div style="font-size: 2rem;">☁️</div>
                                <strong style="color: var(--accent-emerald); font-size: 0.85rem;">Server (Bank Cloud)</strong>
                            </div>
                        </div>

                        <!-- Packet Info Display -->
                        <div style="background: rgba(0,0,0,0.3); border-radius: 10px; padding: 10px 16px; border: 1px solid rgba(255,255,255,0.08); margin-top: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span id="handshakeStepBadge" class="card-badge" style="background: rgba(6, 182, 212, 0.2); color: var(--accent-cyan);">STEP 1 OF 4</span>
                                <span id="handshakeTiming" style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--text-muted);">Elapsed: 0 ms</span>
                            </div>
                            <div id="handshakeTitle" style="font-family: var(--font-display); font-weight: 700; color: var(--text-bright); font-size: 1.05rem; margin-top: 4px;">
                                ClientHello (ECDH Share g^a + Cipher Suites)
                            </div>
                            <div id="handshakeDesc" style="font-size: 0.82rem; color: var(--text-body); margin-top: 4px;">
                                Browser opens connection, announcing supported algorithms (AES-256-GCM, ChaCha20) and sends its public ephemeral Diffie-Hellman share.
                            </div>
                        </div>
                    </div>

                    <!-- Controls Row -->
                    <div style="display: flex; gap: 12px; justify-content: center; align-items: center;">
                        <button class="lab-btn" id="btnTLSNext">Next Step ➔</button>
                        <button class="lab-btn accent-emerald" id="btnTLSAuto">Auto Play ▶</button>
                        <button class="lab-btn accent-gold" id="btnTLSReset">Reset Handshake ↺</button>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>Simulating the exact 1-RTT handshake powering modern web browsers</span>
                <span class="slide-counter">LAB / 52</span>
            </div>
        </section>
"""

    # LAB 7: Quantum Shor vs Lattice Shield Simulator
    lab7_html = """
        <!-- ===================================================================
             INTERACTIVE LAB 7: QUANTUM SHOR VS LATTICE SHIELD
             =================================================================== -->
        <section class="slide" data-slide="lab7" data-section="Interactive Lab 7">
            <div class="slide-header">
                <span class="slide-tag" style="background: rgba(168, 85, 247, 0.15); border-color: rgba(168, 85, 247, 0.35); color: var(--accent-purple);">⚛️ LIVE LAB 07 • QUANTUM RESISTANCE</span>
                <span class="slide-breadcrumb">Comparing Shor's Period-Finding vs Lattice Hardness</span>
            </div>
            <div class="slide-body">
                <div class="slide-titles">
                    <h2 class="slide-main-title">Interactive Simulator: Quantum Shor Attack vs. Lattice Shield</h2>
                    <p class="slide-subtitle">Toggle between RSA/ECC factorization and NIST Lattice-Based ML-KEM to see why lattices resist quantum computing:</p>
                </div>
                <div class="lab-container">
                    <div class="layout-split-equal">
                        <!-- Left: Classical RSA / Shor Attack -->
                        <div class="pres-card" id="cardShor" style="border-top: 3px solid var(--accent-rose);">
                            <span class="card-badge" style="background: rgba(244, 63, 94, 0.2); color: var(--accent-rose);">CLASSICAL: RSA & ECC</span>
                            <h3 class="card-title" style="margin-top: 6px;">Shor's Algorithm Quantum Attack</h3>
                            <p class="card-desc">Quantum computers use Quantum Fourier Transform (QFT) to find the period <em>r</em> of modular powers a<sup>x</sup> ≡ 1 (mod n) in polynomial time O((log n)³).</p>
                            
                            <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; margin: 10px 0; text-align: center;">
                                <div style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--accent-rose);" id="shorStatus">
                                    Simulating Quantum Superposition...
                                </div>
                                <div style="font-size: 1.8rem; margin: 4px 0;" id="shorLockIcon">🔓</div>
                                <strong style="color: var(--accent-rose); font-size: 0.85rem;">RSA-2048 Broken in Seconds</strong>
                            </div>
                            <button class="lab-btn" id="btnRunShor" style="border-color: var(--accent-rose); color: var(--accent-rose); width: 100%;">
                                Trigger Quantum Shor's Algorithm ➔
                            </button>
                        </div>

                        <!-- Right: Post-Quantum Lattice Defense -->
                        <div class="pres-card featured" id="cardLattice" style="border-top: 3px solid var(--accent-purple);">
                            <span class="card-badge" style="background: rgba(168, 85, 247, 0.2); color: var(--accent-purple);">POST-QUANTUM: NIST ML-KEM</span>
                            <h3 class="card-title" style="margin-top: 6px;">High-Dimensional Lattice Shield</h3>
                            <p class="card-desc">Lattice cryptography relies on the <em>Learning With Errors (LWE)</em> problem in 500+ dimensional Euclidean space with Gaussian noise.</p>
                            
                            <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px; margin: 10px 0; text-align: center;">
                                <div style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--accent-purple);" id="latticeStatus">
                                    Searching 512-Dimensional Lattice Points...
                                </div>
                                <div style="font-size: 1.8rem; margin: 4px 0;" id="latticeShieldIcon">🛡️</div>
                                <strong style="color: var(--accent-purple); font-size: 0.85rem;">Quantum Complexity: Unbreakable</strong>
                            </div>
                            <button class="lab-btn accent-emerald" id="btnTestLattice" style="width: 100%;">
                                Test Quantum Resistance on Lattice ➔
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>NIST PQC Standards (ML-KEM / Kyber) rely on high-dimensional geometric hardness</span>
                <span class="slide-counter">LAB / 52</span>
            </div>
        </section>
"""

    # Injections using lambda replacement to avoid backslash escaping issues
    def insert_after(pattern, content, target_str):
        return re.sub(pattern, lambda m: m.group(1) + '\n' + content, target_str, count=1)

    # 1. Lab 1 after Slide 5 (The Big Distinction)
    html = insert_after(r'(<section class="slide"[^>]*data-section="The Big Distinction"[^>]*>[\s\S]*?</section>)', lab1_html, html)

    # 2. Lab 2 after Frequency Analysis
    html = insert_after(r'(<section class="slide"[^>]*data-section="Frequency Analysis"[^>]*>[\s\S]*?</section>)', lab2_html, html)

    # 3. Lab 3 after ECB Mode Flaw
    html = insert_after(r'(<section class="slide"[^>]*data-section="ECB Mode Flaw"[^>]*>[\s\S]*?</section>)', lab3_html, html)

    # 4. Lab 4 after Diffie-Hellman
    html = insert_after(r'(<section class="slide"[^>]*data-section="Diffie-Hellman"[^>]*>[\s\S]*?</section>)', lab4_html, html)

    # 5. Lab 5 after Avalanche Effect
    html = insert_after(r'(<section class="slide"[^>]*data-section="Avalanche Effect"[^>]*>[\s\S]*?</section>)', lab5_html, html)

    # 6. Lab 6 after TLS 1.3 Handshake
    html = insert_after(r'(<section class="slide"[^>]*data-section="TLS 1.3 Handshake"[^>]*>[\s\S]*?</section>)', lab6_html, html)

    # 7. Lab 7 after Post-Quantum
    html = insert_after(r'(<section class="slide"[^>]*data-section="Post-Quantum"[^>]*>[\s\S]*?</section>)', lab7_html, html)

    # Renumber all slides sequentially
    slide_matches = list(re.finditer(r'<section class="slide([^"]*)" data-slide="([^"]*)" data-section="([^"]*)">', html))
    total_slides = len(slide_matches)
    print(f"Total slides found after inserting 7 Interactive Labs: {total_slides}")

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
    html = html.replace("Presentation Slide Directory (45 Slides)", f"Presentation Slide Directory ({total_slides} Slides)")
    html = html.replace("dockIndicator.textContent = `${currentSlide + 1} / ${totalSlides}`;", f"dockIndicator.textContent = `${{currentSlide + 1}} / ${{totalSlides}}`;")

    # JavaScript logic for all 7 labs
    labs_js = """
            // =================================================================
            // LAB 1: CRYPTO TRIAD LIVE CONVERTER
            // =================================================================
            const triadInput = document.getElementById('triadInput');
            const triadBase64 = document.getElementById('triadBase64');
            const triadHash = document.getElementById('triadHash');
            const triadCipher = document.getElementById('triadCipher');
            const btnDecodeBase64 = document.getElementById('btnDecodeBase64');
            const base64ReversalResult = document.getElementById('base64ReversalResult');
            const btnToggleAES = document.getElementById('btnToggleAES');
            const aesStateText = document.getElementById('aesStateText');

            let aesEncrypted = true;

            async function updateTriad() {
                const text = triadInput ? triadInput.value : '';
                // 1. Base64
                if (triadBase64) {
                    try {
                        triadBase64.textContent = btoa(unescape(encodeURIComponent(text)));
                    } catch(e) {
                        triadBase64.textContent = btoa(text);
                    }
                }
                if (base64ReversalResult) base64ReversalResult.textContent = '';

                // 2. Real SHA-256 via SubtleCrypto
                if (triadHash && window.crypto && crypto.subtle) {
                    const msgBuffer = new TextEncoder().encode(text);
                    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
                    const hashArray = Array.from(new Uint8Array(hashBuffer));
                    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
                    triadHash.textContent = hashHex;
                }

                // 3. Simulated AES-256 GCM
                if (triadCipher) {
                    if (aesEncrypted) {
                        let simHex = '';
                        for (let i = 0; i < text.length; i++) {
                            simHex += ((text.charCodeAt(i) * 31 + 17) % 256).toString(16).padStart(2, '0');
                        }
                        simHex += 'a8f902c4e1';
                        triadCipher.textContent = simHex;
                    } else {
                        triadCipher.textContent = text;
                    }
                }
            }

            if (triadInput) {
                triadInput.addEventListener('input', updateTriad);
                updateTriad();
            }

            if (btnDecodeBase64) {
                btnDecodeBase64.addEventListener('click', () => {
                    try {
                        const b64 = triadBase64.textContent;
                        const decoded = decodeURIComponent(escape(atob(b64)));
                        base64ReversalResult.textContent = `Reversed without key: "${decoded}"`;
                    } catch(e) {
                        base64ReversalResult.textContent = `Reversed without key: "${atob(triadBase64.textContent)}"`;
                    }
                });
            }

            if (btnToggleAES) {
                btnToggleAES.addEventListener('click', () => {
                    aesEncrypted = !aesEncrypted;
                    if (aesEncrypted) {
                        btnToggleAES.textContent = '🔓 Decrypt with Key';
                        aesStateText.textContent = 'Status: Encrypted';
                        aesStateText.style.color = 'var(--accent-gold)';
                    } else {
                        btnToggleAES.textContent = '🔒 Encrypt with Key';
                        aesStateText.textContent = 'Status: Decrypted!';
                        aesStateText.style.color = 'var(--accent-emerald)';
                    }
                    updateTriad();
                });
            }

            // =================================================================
            // LAB 2: CAESAR WHEEL & FREQUENCY SPECTRUM
            // =================================================================
            const caesarSlider = document.getElementById('caesarSlider');
            const caesarKeyLabel = document.getElementById('caesarKeyLabel');
            const caesarPlainInput = document.getElementById('caesarPlainInput');
            const caesarCipherOutput = document.getElementById('caesarCipherOutput');
            const caesarFreqBars = document.getElementById('caesarFreqBars');
            const mapA = document.getElementById('mapA');
            const mapE = document.getElementById('mapE');
            const mapT = document.getElementById('mapT');

            function updateCaesar() {
                const k = parseInt(caesarSlider ? caesarSlider.value : 3, 10);
                const shiftChar = String.fromCharCode(65 + k);
                if (caesarKeyLabel) caesarKeyLabel.textContent = `k = ${k} (${shiftChar})`;

                if (mapA) mapA.textContent = String.fromCharCode(65 + ((0 + k) % 26));
                if (mapE) mapE.textContent = String.fromCharCode(65 + ((4 + k) % 26));
                if (mapT) mapT.textContent = String.fromCharCode(65 + ((19 + k) % 26));

                const text = (caesarPlainInput ? caesarPlainInput.value : '').toUpperCase();
                let cipher = '';
                const counts = {};
                for (let i = 0; i < 26; i++) counts[String.fromCharCode(65 + i)] = 0;

                for (let i = 0; i < text.length; i++) {
                    const code = text.charCodeAt(i);
                    if (code >= 65 && code <= 90) {
                        const shifted = String.fromCharCode(((code - 65 + k) % 26) + 65);
                        cipher += shifted;
                        counts[shifted]++;
                    } else {
                        cipher += text[i];
                    }
                }

                if (caesarCipherOutput) caesarCipherOutput.textContent = cipher;

                // Render Frequency Bars for top letters
                if (caesarFreqBars) {
                    caesarFreqBars.innerHTML = '';
                    const sampleLetters = ['A', 'C', 'D', 'E', 'H', 'L', 'O', 'R', 'S', 'T', 'W'];
                    let maxCount = Math.max(...Object.values(counts), 1);

                    sampleLetters.forEach(ch => {
                        const count = counts[ch] || 0;
                        const heightPct = Math.max(10, Math.round((count / maxCount) * 100));
                        const isHighest = count === maxCount && count > 0;
                        const bar = document.createElement('div');
                        bar.style.flex = '1';
                        bar.style.display = 'flex';
                        bar.style.flexDirection = 'column';
                        bar.style.alignItems = 'center';
                        bar.style.gap = '2px';
                        bar.style.height = '100%';
                        bar.style.justifyContent = 'flex-end';
                        bar.innerHTML = `
                            <div style="width: 100%; height: ${heightPct}%; background: ${isHighest ? 'var(--accent-gold)' : 'var(--accent-cyan)'}; border-radius: 3px; transition: height 0.25s ease;"></div>
                            <span style="font-family: var(--font-mono); font-size: 0.65rem; color: ${isHighest ? 'var(--accent-gold)' : 'var(--text-muted)'}; font-weight: ${isHighest ? '800' : '400'};">${ch}</span>
                        `;
                        caesarFreqBars.appendChild(bar);
                    });
                }
            }

            if (caesarSlider) caesarSlider.addEventListener('input', updateCaesar);
            if (caesarPlainInput) caesarPlainInput.addEventListener('input', updateCaesar);
            updateCaesar();

            // =================================================================
            // LAB 3: ECB PENGUIN SIMULATOR
            // =================================================================
            const pixelMatrix = document.getElementById('pixelMatrix');
            const btnSelectECB = document.getElementById('btnSelectECB');
            const btnSelectGCM = document.getElementById('btnSelectGCM');
            const matrixModeTitle = document.getElementById('matrixModeTitle');
            const matrixStatusBanner = document.getElementById('matrixStatusBanner');
            const modeExplanationText = document.getElementById('modeExplanationText');

            // 8x8 Penguin outline pattern (1 = penguin body, 0 = background)
            const penguinBitmap = [
                0,0,1,1,1,1,0,0,
                0,1,1,0,0,1,1,0,
                0,1,1,1,1,1,1,0,
                0,0,1,1,1,1,0,0,
                0,1,1,1,1,1,1,0,
                1,1,0,1,1,0,1,1,
                1,1,1,1,1,1,1,1,
                0,1,1,0,0,1,1,0
            ];

            function renderPixelMatrix(isGCM) {
                if (!pixelMatrix) return;
                pixelMatrix.innerHTML = '';
                for (let i = 0; i < 64; i++) {
                    const cell = document.createElement('div');
                    cell.className = 'pixel-cell';
                    if (!isGCM) {
                        // ECB Mode: Identical plain blocks become identical cipher blocks!
                        const isPenguin = penguinBitmap[i] === 1;
                        cell.style.background = isPenguin ? '#06B6D4' : '#0B132B';
                        cell.style.boxShadow = isPenguin ? '0 0 6px rgba(6,182,212,0.4)' : 'none';
                    } else {
                        // GCM Mode: High entropy randomized visual static
                        const r = Math.floor(Math.random() * 200 + 40);
                        const g = Math.floor(Math.random() * 200 + 40);
                        const b = Math.floor(Math.random() * 200 + 40);
                        cell.style.background = `rgb(${r}, ${g}, ${b})`;
                        cell.style.boxShadow = 'none';
                    }
                    pixelMatrix.appendChild(cell);
                }
            }

            if (btnSelectECB) {
                btnSelectECB.addEventListener('click', () => {
                    matrixModeTitle.textContent = 'Mode: AES-ECB (Electronic Codebook)';
                    matrixModeTitle.style.color = 'var(--accent-rose)';
                    matrixStatusBanner.className = 'callout-box warning';
                    matrixStatusBanner.innerHTML = '⚠️ <strong>PATTERN VISIBLE:</strong> Identical blocks produce identical ciphertext colors!';
                    modeExplanationText.innerHTML = '<strong>Electronic Codebook (ECB)</strong> encrypts each 16-byte block independently with no randomness. Notice that the entire penguin outline remains 100% visible!';
                    renderPixelMatrix(false);
                });
            }

            if (btnSelectGCM) {
                btnSelectGCM.addEventListener('click', () => {
                    matrixModeTitle.textContent = 'Mode: AES-GCM (Authenticated Encryption)';
                    matrixModeTitle.style.color = 'var(--accent-emerald)';
                    matrixStatusBanner.className = 'callout-box';
                    matrixStatusBanner.style.borderLeftColor = 'var(--accent-emerald)';
                    matrixStatusBanner.innerHTML = '✔ <strong>DIFFUSION ACTIVE:</strong> Randomized 96-bit Nonce destroys all structural patterns completely!';
                    modeExplanationText.innerHTML = '<strong>Galois/Counter Mode (GCM)</strong> incorporates an Initialization Vector (IV). Even repeated plaintext bytes produce completely distinct, random-looking ciphertext bits!';
                    renderPixelMatrix(true);
                });
            }
            renderPixelMatrix(false);

            // =================================================================
            // LAB 4: DIFFIE-HELLMAN COLOR MIXING
            // =================================================================
            const btnDHComputeFinal = document.getElementById('btnDHComputeFinal');
            const dhFinalSecretSwatch = document.getElementById('dhFinalSecretSwatch');
            const dhKeyHex = document.getElementById('dhKeyHex');

            if (btnDHComputeFinal) {
                btnDHComputeFinal.addEventListener('click', () => {
                    if (dhFinalSecretSwatch) {
                        dhFinalSecretSwatch.style.background = '#854D0E'; // Muddy Brown
                        dhFinalSecretSwatch.style.boxShadow = '0 0 16px rgba(234, 179, 8, 0.8)';
                        dhFinalSecretSwatch.style.transform = 'scale(1.15)';
                    }
                    if (dhKeyHex) {
                        dhKeyHex.textContent = 'MATCH! K = 0x9f482a17b...';
                    }
                    btnDHComputeFinal.textContent = '🎉 Shared Secret Agreed! (Identical Bronze)';
                });
            }

            // =================================================================
            // LAB 5: AVALANCHE BIT-HEATMAP
            // =================================================================
            const avalancheIn1 = document.getElementById('avalancheIn1');
            const avalancheIn2 = document.getElementById('avalancheIn2');
            const avalancheHash1 = document.getElementById('avalancheHash1');
            const avalancheHash2 = document.getElementById('avalancheHash2');
            const avalancheGrid = document.getElementById('avalancheGrid');
            const avalancheRateText = document.getElementById('avalancheRateText');

            async function updateAvalanche() {
                if (!window.crypto || !crypto.subtle) return;
                const text1 = avalancheIn1 ? avalancheIn1.value : '';
                const text2 = avalancheIn2 ? avalancheIn2.value : '';

                const b1 = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text1));
                const b2 = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text2));

                const u1 = new Uint8Array(b1);
                const u2 = new Uint8Array(b2);

                const hex1 = Array.from(u1).map(x => x.toString(16).padStart(2, '0')).join('');
                const hex2 = Array.from(u2).map(x => x.toString(16).padStart(2, '0')).join('');

                if (avalancheHash1) avalancheHash1.textContent = hex1;
                if (avalancheHash2) avalancheHash2.textContent = hex2;

                if (!avalancheGrid) return;
                avalancheGrid.innerHTML = '';
                let flippedCount = 0;

                for (let byteIdx = 0; byteIdx < 32; byteIdx++) {
                    const byte1 = u1[byteIdx];
                    const byte2 = u2[byteIdx];
                    for (let bitIdx = 7; bitIdx >= 0; bitIdx--) {
                        const bit1 = (byte1 >> bitIdx) & 1;
                        const bit2 = (byte2 >> bitIdx) & 1;
                        const isFlipped = bit1 !== bit2;
                        if (isFlipped) flippedCount++;

                        const cell = document.createElement('div');
                        cell.className = `bit-cell ${isFlipped ? 'flipped' : ''}`;
                        avalancheGrid.appendChild(cell);
                    }
                }

                if (avalancheRateText) {
                    const pct = ((flippedCount / 256) * 100).toFixed(1);
                    avalancheRateText.textContent = `${flippedCount} / 256 Bits Flipped (${pct}%)`;
                }
            }

            if (avalancheIn1) avalancheIn1.addEventListener('input', updateAvalanche);
            if (avalancheIn2) avalancheIn2.addEventListener('input', updateAvalanche);
            updateAvalanche();

            // =================================================================
            // LAB 6: TLS 1.3 ANIMATED HANDSHAKE
            // =================================================================
            const handshakeDot = document.getElementById('handshakeDot');
            const handshakeStepBadge = document.getElementById('handshakeStepBadge');
            const handshakeTiming = document.getElementById('handshakeTiming');
            const handshakeTitle = document.getElementById('handshakeTitle');
            const handshakeDesc = document.getElementById('handshakeDesc');
            const btnTLSNext = document.getElementById('btnTLSNext');
            const btnTLSAuto = document.getElementById('btnTLSAuto');
            const btnTLSReset = document.getElementById('btnTLSReset');

            const tlsSteps = [
                {
                    step: 1,
                    pos: '10%',
                    title: 'Step 1: ClientHello (ECDH Share + Ciphers)',
                    timing: '0 ms (Initiated)',
                    desc: 'Browser announces supported cipher suites (AES-256-GCM, TLS_CHACHA20) and transmits its public Diffie-Hellman share g^a.'
                },
                {
                    step: 2,
                    pos: '85%',
                    title: 'Step 2: ServerHello + X.509 Certificate',
                    timing: '8 ms (Server Response)',
                    desc: 'Server selects cipher suite, provides server share g^b, and signs handshake with its digital certificate to prove identity.'
                },
                {
                    step: 3,
                    pos: '50%',
                    title: 'Step 3: Key Derivation (Master Session Key Derived)',
                    timing: '12 ms (Both Parties Derive K)',
                    desc: 'Both Client and Server independently compute K = g^(ab) without Eve seeing it. Master symmetric keys activated!'
                },
                {
                    step: 4,
                    pos: '85%',
                    title: 'Step 4: Armored AES-256-GCM Bulk Session Active',
                    timing: '16 ms (1-RTT Complete)',
                    desc: 'Handshake complete! Full gigabit encrypted web traffic begins streaming over the high-speed symmetric AES tunnel.'
                }
            ];

            let tlsCurrentStep = 0;
            let tlsAutoTimer = null;

            function renderTLSStep(stepIdx) {
                const s = tlsSteps[stepIdx];
                if (handshakeDot) handshakeDot.style.left = s.pos;
                if (handshakeStepBadge) handshakeStepBadge.textContent = `STEP ${s.step} OF 4`;
                if (handshakeTiming) handshakeTiming.textContent = `Elapsed: ${s.timing}`;
                if (handshakeTitle) handshakeTitle.textContent = s.title;
                if (handshakeDesc) handshakeDesc.textContent = s.desc;
            }

            if (btnTLSNext) {
                btnTLSNext.addEventListener('click', () => {
                    tlsCurrentStep = (tlsCurrentStep + 1) % tlsSteps.length;
                    renderTLSStep(tlsCurrentStep);
                });
            }

            if (btnTLSReset) {
                btnTLSReset.addEventListener('click', () => {
                    if (tlsAutoTimer) clearInterval(tlsAutoTimer);
                    tlsCurrentStep = 0;
                    renderTLSStep(0);
                });
            }

            if (btnTLSAuto) {
                btnTLSAuto.addEventListener('click', () => {
                    if (tlsAutoTimer) clearInterval(tlsAutoTimer);
                    tlsCurrentStep = 0;
                    renderTLSStep(0);
                    tlsAutoTimer = setInterval(() => {
                        tlsCurrentStep++;
                        if (tlsCurrentStep >= tlsSteps.length) {
                            clearInterval(tlsAutoTimer);
                        } else {
                            renderTLSStep(tlsCurrentStep);
                        }
                    }, 1200);
                });
            }

            // =================================================================
            // LAB 7: QUANTUM SHOR VS LATTICE
            // =================================================================
            const btnRunShor = document.getElementById('btnRunShor');
            const shorStatus = document.getElementById('shorStatus');
            const shorLockIcon = document.getElementById('shorLockIcon');

            const btnTestLattice = document.getElementById('btnTestLattice');
            const latticeStatus = document.getElementById('latticeStatus');
            const latticeShieldIcon = document.getElementById('latticeShieldIcon');

            if (btnRunShor) {
                btnRunShor.addEventListener('click', () => {
                    shorStatus.textContent = 'QFT Period Finding Complete: Factors p, q Found in 0.4s!';
                    shorStatus.style.color = 'var(--accent-rose)';
                    shorLockIcon.textContent = '💥🔓';
                    btnRunShor.textContent = '✔ Shor Factorization Succeeded!';
                });
            }

            if (btnTestLattice) {
                btnTestLattice.addEventListener('click', () => {
                    latticeStatus.textContent = 'Closest Vector Problem Intractable: 2^256 Complexity Shielding Data!';
                    latticeStatus.style.color = 'var(--accent-emerald)';
                    latticeShieldIcon.textContent = '💎🛡️';
                    btnTestLattice.textContent = '✔ Quantum Resistance Confirmed!';
                });
            }
    """

    if "// =================================================================" not in html:
        html = html.replace("// Interactive Multiple-Choice Quizzes", labs_js + "\n            // Interactive Multiple-Choice Quizzes")

    with open("cryptography_for_beginners_presentation.html", "w") as f:
        f.write(html)

    print(f"Added all 7 Interactive Labs to HTML! Total slides: {total_slides}")

if __name__ == "__main__":
    main()
