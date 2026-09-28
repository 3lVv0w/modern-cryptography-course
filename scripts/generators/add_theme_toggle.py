import re

def main():
    with open("cryptography_for_beginners_presentation.html", "r") as f:
        html = f.read()

    # 1. Add Light Theme CSS definition
    light_theme_css = """
        /* =====================================================================
           LIGHT THEME PALETTE & COMPONENT OVERRIDES
           ===================================================================== */
        body.light-theme {
            --bg-primary: #F8FAFC;
            --bg-surface: #FFFFFF;
            --bg-card: rgba(255, 255, 255, 0.92);
            --bg-card-border: rgba(15, 23, 42, 0.1);
            --bg-card-hover: rgba(241, 245, 249, 0.98);

            --accent-cyan: #0284C7;
            --accent-blue: #2563EB;
            --accent-indigo: #4F46E5;
            --accent-purple: #7C3AED;
            --accent-gold: #D97706;
            --accent-emerald: #059669;
            --accent-rose: #E11D48;

            --text-title: #0F172A;
            --text-body: #334155;
            --text-muted: #64748B;
            --text-bright: #020617;
        }

        /* Smooth Theme Transition */
        html, body, .slide, .pres-card, .callout-box, .interactive-quiz-card, 
        .qa-question-box, .controls-dock, .checklist-item, .quiz-opt-btn, .stage-meter-box {
            transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
        }

        body.light-theme .ambient-glow {
            background: 
                radial-gradient(circle at 15% 20%, rgba(2, 132, 199, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 85% 80%, rgba(79, 70, 229, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(241, 245, 249, 0.6) 0%, transparent 80%);
        }

        body.light-theme .grid-overlay {
            background-image: linear-gradient(to right, rgba(15, 23, 42, 0.04) 1px, transparent 1px),
                              linear-gradient(to bottom, rgba(15, 23, 42, 0.04) 1px, transparent 1px);
        }

        body.light-theme .slide-header {
            border-bottom-color: rgba(15, 23, 42, 0.08);
        }

        body.light-theme .slide-footer {
            border-top-color: rgba(15, 23, 42, 0.08);
        }

        body.light-theme .hero-title {
            color: #0F172A;
        }

        body.light-theme .hero-gradient-text {
            background: linear-gradient(135deg, #0284C7, #4F46E5, #DB2777);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        body.light-theme .badge-pill {
            background: rgba(15, 23, 42, 0.04);
            border-color: rgba(15, 23, 42, 0.12);
            color: #1E293B;
        }

        body.light-theme .pres-card {
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.04);
        }

        body.light-theme .pres-card:hover {
            box-shadow: 0 8px 28px rgba(15, 23, 42, 0.08);
            border-color: rgba(2, 132, 199, 0.35);
        }

        body.light-theme .pres-card.featured {
            border-color: rgba(2, 132, 199, 0.45);
            box-shadow: 0 8px 30px rgba(2, 132, 199, 0.1);
        }

        body.light-theme .callout-box {
            color: #0F172A;
            background: rgba(2, 132, 199, 0.08);
        }

        body.light-theme .callout-box strong {
            color: #0369A1;
        }

        body.light-theme .callout-box.warning {
            color: #881337;
            background: rgba(225, 29, 72, 0.08);
        }

        body.light-theme .callout-box.warning strong {
            color: #BE123C;
        }

        body.light-theme .callout-box.gold {
            color: #78350F;
            background: rgba(217, 119, 6, 0.08);
        }

        body.light-theme .callout-box.gold strong {
            color: #B45309;
        }

        body.light-theme .pres-table {
            background: #FFFFFF;
            border-color: rgba(15, 23, 42, 0.1);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.03);
        }

        body.light-theme .pres-table th {
            background: rgba(15, 23, 42, 0.04);
            color: #0F172A;
            border-bottom-color: rgba(15, 23, 42, 0.1);
        }

        body.light-theme .pres-table td {
            color: #334155;
            border-bottom-color: rgba(15, 23, 42, 0.06);
        }

        body.light-theme .controls-dock {
            background: rgba(255, 255, 255, 0.9);
            border-color: rgba(15, 23, 42, 0.14);
            box-shadow: 0 8px 30px rgba(15, 23, 42, 0.12);
        }

        body.light-theme .control-btn {
            color: #334155;
        }

        body.light-theme .control-btn:hover {
            background: rgba(15, 23, 42, 0.07);
            color: #0F172A;
        }

        body.light-theme .slide-grid-modal {
            background: rgba(248, 250, 252, 0.97);
        }

        body.light-theme .grid-thumb-card {
            background: #FFFFFF;
            border-color: rgba(15, 23, 42, 0.1);
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        }

        body.light-theme .grid-thumb-card:hover, body.light-theme .grid-thumb-card.active {
            border-color: var(--accent-cyan);
            background: rgba(2, 132, 199, 0.06);
        }

        body.light-theme .grid-thumb-title {
            color: #0F172A;
        }

        body.light-theme .grid-modal-title {
            color: #0F172A;
        }

        body.light-theme .grid-close-btn {
            background: rgba(15, 23, 42, 0.06);
            border-color: rgba(15, 23, 42, 0.15);
            color: #0F172A;
        }

        body.light-theme .grid-close-btn:hover {
            background: rgba(15, 23, 42, 0.12);
        }

        body.light-theme .quiz-card {
            background: #FFFFFF;
            border-color: rgba(217, 119, 6, 0.35);
            box-shadow: 0 4px 16px rgba(217, 119, 6, 0.05);
        }

        body.light-theme .quiz-question {
            color: #0F172A;
        }

        body.light-theme .quiz-answer-drawer {
            color: #334155;
            border-top-color: rgba(217, 119, 6, 0.25);
        }

        body.light-theme .qa-question-box {
            background: #FFFFFF;
            border-color: rgba(15, 23, 42, 0.1);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        }

        body.light-theme .interactive-quiz-card {
            background: #FFFFFF;
            border-color: rgba(15, 23, 42, 0.1);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        }

        body.light-theme .quiz-opt-btn {
            background: rgba(15, 23, 42, 0.03);
            border-color: rgba(15, 23, 42, 0.1);
            color: #1E293B;
        }

        body.light-theme .quiz-opt-btn:hover {
            background: rgba(2, 132, 199, 0.08);
            border-color: rgba(2, 132, 199, 0.4);
        }

        body.light-theme .stage-meter-box {
            background: #FFFFFF;
            border-color: rgba(15, 23, 42, 0.1);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        }

        body.light-theme .stage-meter-bar {
            background: rgba(15, 23, 42, 0.08);
        }

        body.light-theme .checklist-item {
            background: #FFFFFF;
            border-color: rgba(15, 23, 42, 0.1);
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.02);
        }

        body.light-theme .checklist-item:hover {
            background: rgba(2, 132, 199, 0.06);
            border-color: rgba(2, 132, 199, 0.35);
        }

        body.light-theme .checklist-item.checked {
            background: rgba(5, 150, 105, 0.08);
            border-color: rgba(5, 150, 105, 0.35);
        }

        body.light-theme .flow-step {
            background: #FFFFFF;
            border-color: rgba(15, 23, 42, 0.1);
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.02);
        }

        body.light-theme .metric-card {
            background: #FFFFFF;
            border-color: rgba(15, 23, 42, 0.1);
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
        }

        body.light-theme .metric-value {
            background: linear-gradient(135deg, #0F172A, #0284C7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        body.light-theme .diagram-box {
            background: #FFFFFF;
            border-color: rgba(15, 23, 42, 0.1);
        }
    """

    if "/* =====================================================================\n           LIGHT THEME PALETTE" not in html:
        html = html.replace("        /* Floating Controller Dock */", light_theme_css + "\n        /* Floating Controller Dock */")

    # 2. Add Theme Toggle button into .controls-dock
    dock_old = """    <!-- FLOATING CONTROLS DOCK -->
    <div class="controls-dock">
        <button class="control-btn" id="prevBtn" title="Previous Slide (Left Arrow)">◀</button>
        <span class="dock-indicator" id="dockIndicator">1 / 32</span>
        <button class="control-btn" id="nextBtn" title="Next Slide (Right Arrow or Space)">▶</button>
        <div style="width: 1px; height: 18px; background: rgba(255,255,255,0.2); margin: 0 4px;"></div>
        <button class="control-btn" id="gridBtn" title="Slide Overview Grid (G)">☵</button>
        <button class="control-btn" id="fullscreenBtn" title="Toggle Fullscreen (F)">⛶</button>
        <button class="control-btn" id="printBtn" title="Print / Export PDF">🖨️</button>
    </div>"""

    dock_replacement = """    <!-- FLOATING CONTROLS DOCK -->
    <div class="controls-dock">
        <button class="control-btn" id="prevBtn" title="Previous Slide (Left Arrow)">◀</button>
        <span class="dock-indicator" id="dockIndicator">1 / 45</span>
        <button class="control-btn" id="nextBtn" title="Next Slide (Right Arrow or Space)">▶</button>
        <div style="width: 1px; height: 18px; background: rgba(255,255,255,0.2); margin: 0 4px;"></div>
        <button class="control-btn" id="themeBtn" title="Toggle Light/Dark Theme (T)">☀️</button>
        <button class="control-btn" id="gridBtn" title="Slide Overview Grid (G)">☵</button>
        <button class="control-btn" id="fullscreenBtn" title="Toggle Fullscreen (F)">⛶</button>
        <button class="control-btn" id="printBtn" title="Print / Export PDF">🖨️</button>
    </div>"""

    # If dockIndicator was 1 / 32 or 1 / 45:
    html = re.sub(
        r'<div class="controls-dock">[\s\S]*?</div>',
        dock_replacement.replace('    <!-- FLOATING CONTROLS DOCK -->\n', ''),
        html,
        count=1
    )

    # 3. Update modal title to 45 slides
    html = html.replace("Presentation Slide Directory (32 Slides)", "Presentation Slide Directory (45 Slides)")

    # 4. Add Theme Toggle logic to JavaScript
    theme_js = """
            // Theme Management (Light / Dark)
            const themeBtn = document.getElementById('themeBtn');

            function applyTheme(isLight) {
                if (isLight) {
                    document.body.classList.add('light-theme');
                    if (themeBtn) {
                        themeBtn.textContent = '🌙';
                        themeBtn.title = 'Switch to Dark Theme (T)';
                    }
                } else {
                    document.body.classList.remove('light-theme');
                    if (themeBtn) {
                        themeBtn.textContent = '☀️';
                        themeBtn.title = 'Switch to Light Theme (T)';
                    }
                }
            }

            function initTheme() {
                const savedTheme = localStorage.getItem('crypto_presentation_theme');
                if (savedTheme === 'light') {
                    applyTheme(true);
                } else {
                    applyTheme(false);
                }
            }

            function toggleTheme() {
                const currentlyLight = document.body.classList.contains('light-theme');
                const nextLight = !currentlyLight;
                applyTheme(nextLight);
                localStorage.setItem('crypto_presentation_theme', nextLight ? 'light' : 'dark');
            }

            if (themeBtn) {
                themeBtn.addEventListener('click', toggleTheme);
            }
            initTheme();
    """

    if "// Theme Management (Light / Dark)" not in html:
        html = html.replace("const printBtn = document.getElementById('printBtn');", "const printBtn = document.getElementById('printBtn');\n" + theme_js)

    # 5. Add 't' / 'T' key shortcut to switch theme in keydown handler
    key_addition = """
                    case 't':
                    case 'T':
                        toggleTheme();
                        break;
    """
    if "case 't':" not in html:
        html = html.replace("case 'f':\n                    case 'F':\n                        toggleFullscreen();\n                        break;", 
                            "case 'f':\n                    case 'F':\n                        toggleFullscreen();\n                        break;\n" + key_addition)

    with open("cryptography_for_beginners_presentation.html", "w") as f:
        f.write(html)

    print("Added light/dark theme toggle to cryptography_for_beginners_presentation.html successfully!")

if __name__ == "__main__":
    main()
