#!/usr/bin/env python3
"""
add_responsive_support.py
Enhance cryptography_for_beginners_presentation.html with comprehensive responsive design
supporting Mobile, Tablet, Desktop, and various screen sizes / aspect ratios.
"""

import re
import os

HTML_PATH = "/Users/kvivek/Documents/modern-cryptography-course/cryptography_for_beginners_presentation.html"

def enhance_responsiveness():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update viewport meta tag for edge-to-edge cover support on iOS and Android
    viewport_old = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    viewport_new = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">'
    if viewport_old in html:
        html = html.replace(viewport_old, viewport_new, 1)
        print("Updated viewport meta tag.")
    elif 'viewport-fit=cover' not in html:
        html = re.sub(r'<meta name="viewport"[^>]*>', viewport_new, html, count=1)
        print("Replaced viewport meta tag with regex.")

    # 2. Update base CSS for .slide and .slide-body so they support overflow scrolling on smaller screens
    old_slide_rule = re.search(r'\.slide\s*\{[\s\S]*?visibility:\s*0\.4s;\s*\}', html)
    if old_slide_rule:
        new_slide_rule = """.slide {
            position: absolute;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            height: 100dvh;
            padding: clamp(0.9rem, 2.5vw, 2.8rem) clamp(1rem, 4vw, 4rem);
            padding-top: calc(clamp(0.9rem, 2.5vw, 2.8rem) + env(safe-area-inset-top, 0px));
            padding-bottom: calc(clamp(0.9rem, 2.5vw, 2.8rem) + env(safe-area-inset-bottom, 0px));
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
            transform: scale(0.98) translateY(12px);
            transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1), 
                        transform 0.4s cubic-bezier(0.16, 1, 0.3, 1),
                        visibility 0.4s;
            overflow-y: auto;
            overflow-x: hidden;
            -webkit-overflow-scrolling: touch;
            scroll-behavior: smooth;
        }

        /* Sleek Modern Scrollbar for Slide Content on Mobile / Small Screens */
        .slide::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .slide::-webkit-scrollbar-track {
            background: transparent;
        }
        .slide::-webkit-scrollbar-thumb {
            background: rgba(6, 182, 212, 0.28);
            border-radius: 999px;
        }
        .slide::-webkit-scrollbar-thumb:hover {
            background: rgba(6, 182, 212, 0.55);
        }
        body.light-theme .slide::-webkit-scrollbar-thumb {
            background: rgba(2, 132, 199, 0.35);
        }"""
        html = html.replace(old_slide_rule.group(0), new_slide_rule, 1)
        print("Updated .slide base CSS with smooth scrolling and safe area padding.")

    # 3. Update .slide-body rule
    old_slide_body_rule = re.search(r'\.slide-body\s*\{[\s\S]*?max-height:\s*calc\(100vh\s*-\s*140px\);[\s\S]*?\}', html)
    if old_slide_body_rule:
        new_slide_body_rule = """.slide-body {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: min-content;
            gap: clamp(0.6rem, 1.8vh, 1.6rem);
            padding: 4px 0;
        }"""
        html = html.replace(old_slide_body_rule.group(0), new_slide_body_rule, 1)
        print("Updated .slide-body base CSS to allow natural min-height expansion.")

    # 4. Clean up corrupted / duplicate dock HTML buttons at end of body
    dock_pattern = re.compile(
        r'<div class="controls-dock">[\s\S]*?<!-- MODAL SLIDE GRID OVERVIEW',
        re.MULTILINE
    )
    clean_dock = """<div class="controls-dock" id="controlsDock">
        <button class="control-btn" id="prevBtn" title="Previous Slide (Left Arrow / Swipe Right)" aria-label="Previous Slide">◀</button>
        <span class="dock-indicator" id="dockIndicator">1 / 52</span>
        <button class="control-btn" id="nextBtn" title="Next Slide (Right Arrow / Swipe Left)" aria-label="Next Slide">▶</button>
        <div class="dock-divider"></div>
        <button class="control-btn lang-toggle-btn" id="langBtn" title="Toggle Thai / English Language (L)" aria-label="Toggle Language">🇬🇧</button>
        <button class="control-btn" id="themeBtn" title="Toggle Light/Dark Theme (T)" aria-label="Toggle Theme">☀️</button>
        <button class="control-btn" id="gridBtn" title="Slide Overview Grid (G)" aria-label="Overview Grid">☵</button>
        <button class="control-btn" id="fullscreenBtn" title="Toggle Fullscreen (F)" aria-label="Toggle Fullscreen">⛶</button>
        <button class="control-btn" id="printBtn" title="Print / Export PDF" aria-label="Print">🖨️</button>
    </div>

    <!-- MODAL SLIDE GRID OVERVIEW"""
    if dock_pattern.search(html):
        html = dock_pattern.sub(clean_dock, html)
        print("Cleaned up floating controls dock HTML and removed stray tags.")

    # 5. Insert Comprehensive Responsive Media Queries before /* Print styles */
    responsive_css = """
        /* =====================================================================
           RESPONSIVE DESIGN SYSTEM (MOBILE, TABLET, DESKTOP, ULTRA-WIDE)
           ===================================================================== */
        .dock-divider {
            width: 1px;
            height: 18px;
            background: rgba(255, 255, 255, 0.2);
            margin: 0 4px;
            flex-shrink: 0;
        }
        body.light-theme .dock-divider {
            background: rgba(15, 23, 42, 0.15);
        }

        /* Touch Device Swipe Cue / Badge */
        .touch-swipe-cue {
            display: none;
            align-items: center;
            gap: 5px;
            font-family: var(--font-mono);
            font-size: 0.7rem;
            color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.25);
            padding: 2px 8px;
            border-radius: 999px;
            animation: pulseSwipe 2.5s infinite ease-in-out;
        }
        @keyframes pulseSwipe {
            0%, 100% { opacity: 0.7; transform: translateX(0); }
            50% { opacity: 1; transform: translateX(2px); }
        }

        /* Large Desktop & 4K Displays (>= 1600px) */
        @media (min-width: 1600px) {
            .slide {
                padding: 3rem 6rem;
            }
            .slide-main-title {
                font-size: 3.4rem;
            }
            .hero-title {
                font-size: 5rem;
            }
            .card-title {
                font-size: 1.55rem;
            }
            .card-desc {
                font-size: 1.05rem;
            }
            .pres-card {
                padding: 1.8rem 2.2rem;
            }
        }

        /* Large Tablet / Small Desktop (<= 1024px) */
        @media (max-width: 1024px) {
            .slide {
                padding: clamp(0.9rem, 2vw, 1.8rem) clamp(1rem, 2.8vw, 2.2rem);
                padding-bottom: calc(75px + env(safe-area-inset-bottom, 0px));
            }
            .layout-grid-4 {
                grid-template-columns: repeat(2, 1fr);
                gap: 14px;
            }
            .image-card-container {
                max-height: min(42vh, 320px);
            }
            .controls-dock {
                bottom: max(16px, env(safe-area-inset-bottom, 16px));
                right: 20px;
            }
        }

        /* Tablet Portrait & Phablets (<= 900px) */
        @media (max-width: 900px) {
            .slide {
                padding: 1rem 1.4rem;
                padding-bottom: calc(85px + env(safe-area-inset-bottom, 0px));
            }
            .slide-body {
                justify-content: flex-start;
                gap: 14px;
            }
            .layout-split {
                grid-template-columns: 1fr;
                gap: 16px;
            }
            .layout-split-equal {
                grid-template-columns: 1fr;
                gap: 16px;
            }
            .checklist-layout {
                grid-template-columns: 1fr;
                gap: 16px;
            }
            .quiz-arena-grid {
                grid-template-columns: 1fr;
                gap: 16px;
            }
            .qa-card-grid {
                grid-template-columns: 1fr;
                gap: 16px;
            }
            .layout-grid-3 {
                grid-template-columns: repeat(2, 1fr);
                gap: 14px;
            }
            .slide-hero {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            .slide-hero .hero-badges {
                margin-top: 14px;
            }
            .controls-dock {
                left: 50%;
                right: auto;
                transform: translateX(-50%);
                bottom: max(12px, env(safe-area-inset-bottom, 12px));
                width: min(calc(100vw - 32px), 480px);
                justify-content: space-between;
                padding: 6px 12px;
            }
            .touch-swipe-cue {
                display: inline-flex;
            }
        }

        /* Mobile Devices (<= 768px) */
        @media (max-width: 768px) {
            .slide {
                padding: 0.9rem 1.1rem;
                padding-top: calc(0.85rem + env(safe-area-inset-top, 0px));
                padding-bottom: calc(85px + env(safe-area-inset-bottom, 0px));
            }
            .slide-body {
                justify-content: flex-start;
                padding: 6px 0;
                gap: 12px;
            }
            .slide-header {
                flex-direction: row;
                flex-wrap: wrap;
                align-items: center;
                gap: 6px;
                margin-bottom: 8px;
                padding-bottom: 6px;
            }
            .slide-tag {
                font-size: 0.68rem;
                padding: 3px 8px;
            }
            .slide-breadcrumb {
                font-size: 0.72rem;
            }
            .slide-main-title {
                font-size: clamp(1.4rem, 5.5vw, 1.95rem);
                line-height: 1.2;
            }
            .slide-subtitle {
                font-size: clamp(0.84rem, 3.2vw, 0.98rem);
                line-height: 1.45;
            }
            .hero-title {
                font-size: clamp(1.8rem, 7vw, 2.5rem);
                line-height: 1.1;
                margin-bottom: 12px;
            }
            .layout-grid-3,
            .layout-grid-4,
            .layout-grid-2 {
                grid-template-columns: 1fr;
                gap: 12px;
            }
            .pres-card {
                padding: 1rem 1.15rem;
                border-radius: 14px;
            }
            .image-card-container {
                max-height: 220px;
                border-radius: 14px;
            }
            .flow-container {
                flex-direction: column;
                gap: 8px;
                align-items: stretch;
            }
            .flow-step {
                padding: 10px 14px;
                border-radius: 10px;
            }
            .flow-arrow {
                transform: rotate(90deg);
                text-align: center;
                font-size: 1.2rem;
            }
            .pres-table {
                display: block;
                width: 100%;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                font-size: 0.82rem;
            }
            .pres-table th, .pres-table td {
                padding: 8px 10px;
                white-space: nowrap;
            }
            .lab-input-row {
                flex-direction: column;
                align-items: stretch;
                gap: 8px;
                padding: 10px;
            }
            .lab-text-input {
                width: 100%;
            }
            .handshake-wire-container {
                padding: 0 10px;
                height: 100px;
            }
            .wire-track {
                left: 45px;
                right: 45px;
            }
            .pixel-matrix-grid {
                width: min(180px, 50vw);
                height: min(180px, 50vw);
            }
            .avalanche-heatmap-grid {
                max-width: 100%;
                height: auto;
                aspect-ratio: 16 / 9;
                gap: 2px;
            }
            .controls-dock {
                left: 50%;
                right: auto;
                transform: translateX(-50%);
                bottom: max(10px, env(safe-area-inset-bottom, 10px));
                width: min(calc(100vw - 20px), 430px);
                padding: 5px 8px;
                gap: 4px;
            }
            .control-btn {
                width: 38px;
                height: 38px;
                font-size: 1rem;
            }
            .control-btn.lang-toggle-btn {
                font-size: 0.72rem;
                padding: 0 6px;
                width: auto;
                border-radius: 999px;
            }
            .dock-indicator {
                font-size: 0.76rem;
                min-width: 50px;
                padding: 0 4px;
            }
            .slide-grid-modal {
                padding: 20px 16px;
            }
            .grid-modal-header {
                margin-bottom: 16px;
            }
            .grid-modal-title {
                font-size: 1.25rem;
            }
            .slides-grid {
                grid-template-columns: repeat(auto-fill, minmax(135px, 1fr));
                gap: 10px;
            }
            .grid-thumb-card {
                padding: 10px;
                border-radius: 10px;
                gap: 4px;
            }
            .grid-thumb-title {
                font-size: 0.82rem;
                line-height: 1.2;
            }
            .slide-footer {
                flex-direction: column;
                align-items: flex-start;
                gap: 4px;
            }
        }

        /* Small Phones (<= 480px) */
        @media (max-width: 480px) {
            .slide {
                padding: 0.8rem 0.9rem;
                padding-top: calc(0.7rem + env(safe-area-inset-top, 0px));
                padding-bottom: calc(85px + env(safe-area-inset-bottom, 0px));
            }
            .slide-main-title {
                font-size: 1.35rem;
            }
            .hero-title {
                font-size: 1.65rem;
            }
            .badge-pill {
                font-size: 0.72rem;
                padding: 4px 10px;
            }
            #printBtn,
            #fullscreenBtn {
                display: none !important;
            }
            .controls-dock {
                width: calc(100vw - 16px);
                justify-content: space-around;
                padding: 4px 6px;
            }
            .control-btn {
                width: 36px;
                height: 36px;
            }
            .dock-indicator {
                font-size: 0.72rem;
                min-width: 44px;
            }
        }

        /* Height-Constrained Displays & Mobile Landscape (<= 600px height) */
        @media (max-height: 600px) {
            .slide {
                padding-top: 0.5rem;
                padding-bottom: 75px;
            }
            .slide-body {
                justify-content: flex-start;
                gap: 8px;
            }
            .slide-header {
                margin-bottom: 4px;
                padding-bottom: 4px;
            }
            .slide-footer {
                margin-top: 4px;
                padding-top: 4px;
            }
            .image-card-container {
                max-height: 160px;
            }
            .slide-hero {
                grid-template-columns: 1.2fr 0.8fr;
                gap: 16px;
            }
            .hero-title {
                font-size: 1.8rem;
                margin-bottom: 6px;
            }
        }

        @media (max-height: 480px) and (orientation: landscape) {
            .slide-header, .slide-footer {
                display: flex;
            }
            .slide-body {
                gap: 6px;
            }
            .layout-split, .layout-split-equal {
                grid-template-columns: 1fr 1fr;
                gap: 12px;
            }
            .image-card-container {
                max-height: 140px;
            }
        }
"""

    if "/* RESPONSIVE DESIGN SYSTEM" not in html:
        print_style_target = "        /* Print styles */"
        if print_style_target in html:
            html = html.replace(print_style_target, responsive_css + "\n" + print_style_target, 1)
            print("Inserted responsive CSS media queries before print styles.")
        else:
            html = html.replace("    </style>", responsive_css + "\n    </style>", 1)
            print("Inserted responsive CSS media queries before </style>.")

    # 6. Add touch gesture navigation & scroll reset to JavaScript
    touch_js = """
            // =================================================================
            // TOUCH & SWIPE NAVIGATION FOR MOBILE / TABLET
            // =================================================================
            (function setupTouchGestures() {
                let touchStartX = 0;
                let touchStartY = 0;
                let touchEndX = 0;
                let touchEndY = 0;
                const minSwipeDistance = 45;
                const maxPerpendicularDistance = 80;

                window.addEventListener('touchstart', (e) => {
                    if (!e.touches || e.touches.length === 0) return;
                    touchStartX = e.touches[0].clientX;
                    touchStartY = e.touches[0].clientY;
                }, { passive: true });

                window.addEventListener('touchend', (e) => {
                    if (!e.changedTouches || e.changedTouches.length === 0) return;
                    
                    // Don't intercept swipe if user is interacting with interactive elements
                    const target = e.target;
                    if (target && target.closest && target.closest('input, textarea, select, button, .quiz-opt-btn, .checklist-item, .slide-grid-modal.open, .avalanche-heatmap-grid, .pixel-matrix-grid')) {
                        return;
                    }

                    touchEndX = e.changedTouches[0].clientX;
                    touchEndY = e.changedTouches[0].clientY;

                    const deltaX = touchEndX - touchStartX;
                    const deltaY = touchEndY - touchStartY;

                    if (Math.abs(deltaX) >= minSwipeDistance && Math.abs(deltaY) <= maxPerpendicularDistance) {
                        if (deltaX < 0) {
                            // Swiped Left -> Go to Next Slide
                            nextSlide();
                        } else {
                            // Swiped Right -> Go to Previous Slide
                            prevSlide();
                        }
                    }
                }, { passive: true });

                // Responsive resize & orientation change handler
                window.addEventListener('resize', () => {
                    updateUI();
                });
                window.addEventListener('orientationchange', () => {
                    setTimeout(updateUI, 120);
                });
            })();
    """

    # Check if goToSlide resets scroll position
    old_goto = re.search(r'function goToSlide\(index, updateHash = true\) \{[\s\S]*?updateUI\(\);\s*\}', html)
    if old_goto and 'scrollTop = 0' not in old_goto.group(0):
        new_goto = """function goToSlide(index, updateHash = true) {
                if (index < 0) index = 0;
                if (index >= totalSlides) index = totalSlides - 1;
                currentSlide = index;
                if (updateHash && window.history && window.history.replaceState) {
                    window.history.replaceState(null, '', `#slide-${index + 1}`);
                }
                // Reset scroll position on active slide for mobile / tablet
                if (slides[currentSlide]) {
                    slides[currentSlide].scrollTop = 0;
                }
                updateUI();
            }"""
        html = html.replace(old_goto.group(0), new_goto, 1)
        print("Updated goToSlide to reset slide scrollTop on slide change.")

    if "TOUCH & SWIPE NAVIGATION FOR MOBILE / TABLET" not in html:
        init_target = "            // Initialize\n            readHash();\n            updateUI();"
        if init_target in html:
            html = html.replace(init_target, touch_js + "\n" + init_target, 1)
            print("Inserted touch swipe navigation logic into script.")

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print("Responsive support successfully added to presentation!")

if __name__ == "__main__":
    enhance_responsiveness()
