#!/usr/bin/env python3
"""
update_typography_scaling.py
Scales up all typography across cryptography_for_beginners_presentation.html
to be proportional with the slide dimensions and viewport across all devices.
"""

import re
import os

HTML_PATH = "/Users/kvivek/Documents/modern-cryptography-course/cryptography_for_beginners_presentation.html"

def scale_typography():
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update root html typography to fluid responsive clamp
    html_rule_old = """        html, body {
            width: 100vw;
            height: 100vh;
            height: 100dvh;
            overflow: hidden;
            background-color: var(--bg-primary);
            color: var(--text-body);
            font-family: var(--font-body);
            -webkit-font-smoothing: antialiased;
        }"""

    html_rule_new = """        html {
            /* Fluid presentation typography scaling: scales smoothly from 16px on mobile up to 21.5px on 1920x1080 and 24px on 4K */
            font-size: clamp(16px, 0.45vw + 12px, 22px);
        }

        html, body {
            width: 100vw;
            height: 100vh;
            height: 100dvh;
            overflow: hidden;
            background-color: var(--bg-primary);
            color: var(--text-body);
            font-family: var(--font-body);
            -webkit-font-smoothing: antialiased;
        }"""

    if html_rule_old in html:
        html = html.replace(html_rule_old, html_rule_new, 1)
        print("1. Added fluid responsive root html font-size clamp.")
    else:
        print("Warning: html_rule_old not found directly.")

    # 2. Update .slide-tag
    slide_tag_old = """        .slide-tag {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: clamp(0.68rem, 0.9vw, 0.82rem);
            font-family: var(--font-mono);
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.1);
            padding: 4px 12px;
            border-radius: 999px;
            border: 1px solid rgba(6, 182, 212, 0.25);
        }"""
    slide_tag_new = """        .slide-tag {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: clamp(0.82rem, 1.1vw, 1.05rem);
            font-family: var(--font-mono);
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.12);
            padding: 5px 14px;
            border-radius: 999px;
            border: 1px solid rgba(6, 182, 212, 0.28);
        }"""
    if slide_tag_old in html:
        html = html.replace(slide_tag_old, slide_tag_new, 1)
        print("2. Updated .slide-tag.")

    # 3. Update .slide-breadcrumb
    bread_old = """        .slide-breadcrumb {
            font-size: clamp(0.7rem, 0.95vw, 0.85rem);
            color: var(--text-muted);
            font-weight: 500;
        }"""
    bread_new = """        .slide-breadcrumb {
            font-size: clamp(0.85rem, 1.15vw, 1.1rem);
            color: var(--text-muted);
            font-weight: 600;
        }"""
    if bread_old in html:
        html = html.replace(bread_old, bread_new, 1)
        print("3. Updated .slide-breadcrumb.")

    # 4. Update .slide-main-title and .slide-subtitle
    title_sub_old = """        .slide-main-title {
            font-family: var(--font-display);
            font-size: clamp(1.8rem, 3.2vw, 3rem);
            font-weight: 800;
            color: var(--text-title);
            line-height: 1.15;
            letter-spacing: -0.02em;
        }

        .slide-subtitle {
            font-size: clamp(0.95rem, 1.3vw, 1.25rem);
            color: var(--text-muted);
            margin-top: clamp(0.2rem, 0.6vh, 0.4rem);
            font-weight: 400;
            max-width: 900px;
            line-height: 1.4;
        }"""
    title_sub_new = """        .slide-main-title {
            font-family: var(--font-display);
            font-size: clamp(2.1rem, 3.8vw, 3.6rem);
            font-weight: 800;
            color: var(--text-title);
            line-height: 1.16;
            letter-spacing: -0.025em;
        }

        .slide-subtitle {
            font-size: clamp(1.1rem, 1.55vw, 1.5rem);
            color: var(--text-muted);
            margin-top: clamp(0.25rem, 0.7vh, 0.5rem);
            font-weight: 400;
            max-width: 1050px;
            line-height: 1.48;
        }"""
    if title_sub_old in html:
        html = html.replace(title_sub_old, title_sub_new, 1)
        print("4. Updated .slide-main-title and .slide-subtitle.")

    # 5. Update .card-icon, .card-title, .card-desc, .card-badge
    card_typo_old = """        .card-icon {
            font-size: clamp(1.5rem, 2.4vw, 2.4rem);
            line-height: 1;
            margin-bottom: 2px;
        }

        .card-title {
            font-family: var(--font-display);
            font-size: clamp(1.1rem, 1.4vw, 1.45rem);
            font-weight: 700;
            color: var(--text-bright);
        }

        .card-desc {
            font-size: clamp(0.82rem, 1.05vw, 0.98rem);
            color: var(--text-body);
            line-height: 1.5;
        }

        .card-badge {
            align-self: flex-start;
            font-family: var(--font-mono);
            font-size: 0.72rem;
            padding: 3px 10px;
            border-radius: 6px;
            font-weight: 600;
        }"""
    card_typo_new = """        .card-icon {
            font-size: clamp(1.8rem, 2.8vw, 3rem);
            line-height: 1;
            margin-bottom: 4px;
        }

        .card-title {
            font-family: var(--font-display);
            font-size: clamp(1.25rem, 1.75vw, 1.85rem);
            font-weight: 700;
            color: var(--text-bright);
            line-height: 1.25;
        }

        .card-desc {
            font-size: clamp(0.98rem, 1.25vw, 1.22rem);
            color: var(--text-body);
            line-height: 1.58;
        }

        .card-badge {
            align-self: flex-start;
            font-family: var(--font-mono);
            font-size: clamp(0.8rem, 0.95vw, 0.92rem);
            padding: 4px 12px;
            border-radius: 8px;
            font-weight: 700;
        }"""
    if card_typo_old in html:
        html = html.replace(card_typo_old, card_typo_new, 1)
        print("5. Updated card typography (.card-icon, .card-title, .card-desc, .card-badge).")

    # 6. Update .image-caption-overlay
    img_cap_old = """        .image-caption-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0, 0, 0, 0.9), transparent);
            padding: 16px 20px 12px;
            font-size: 0.85rem;
            color: #E2E8F0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }"""
    img_cap_new = """        .image-caption-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0, 0, 0, 0.9), transparent);
            padding: 18px 24px 14px;
            font-size: clamp(0.92rem, 1.15vw, 1.12rem);
            color: #E2E8F0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }"""
    if img_cap_old in html:
        html = html.replace(img_cap_old, img_cap_new, 1)
        print("6. Updated .image-caption-overlay.")

    # 7. Update .flow-arrow and .flow-step
    flow_old = """        .flow-step {
            flex: 1;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            padding: clamp(0.8rem, 1.5vh, 1.3rem);
            text-align: center;
            position: relative;
        }

        .flow-step.active-step {
            border-color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.08);
        }

        .flow-arrow {
            font-size: 1.5rem;
            color: var(--accent-cyan);
            opacity: 0.7;
        }"""
    flow_new = """        .flow-step {
            flex: 1;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            padding: clamp(0.9rem, 1.7vh, 1.5rem);
            text-align: center;
            position: relative;
            font-size: clamp(0.95rem, 1.2vw, 1.18rem);
        }

        .flow-step.active-step {
            border-color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.08);
        }

        .flow-arrow {
            font-size: 1.8rem;
            color: var(--accent-cyan);
            opacity: 0.75;
        }"""
    if flow_old in html:
        html = html.replace(flow_old, flow_new, 1)
        print("7. Updated .flow-step and .flow-arrow.")

    # 8. Update .pres-table th and td
    table_old = """        .pres-table th {
            background: rgba(255, 255, 255, 0.05);
            padding: clamp(0.6rem, 1.2vh, 1rem) clamp(0.8rem, 1.5vw, 1.4rem);
            font-family: var(--font-display);
            font-weight: 700;
            color: var(--text-bright);
            font-size: clamp(0.85rem, 1.1vw, 1.05rem);
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .pres-table td {
            padding: clamp(0.6rem, 1.2vh, 1rem) clamp(0.8rem, 1.5vw, 1.4rem);
            font-size: clamp(0.8rem, 1vw, 0.95rem);
            color: var(--text-body);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }"""
    table_new = """        .pres-table th {
            background: rgba(255, 255, 255, 0.06);
            padding: clamp(0.75rem, 1.4vh, 1.2rem) clamp(0.9rem, 1.6vw, 1.5rem);
            font-family: var(--font-display);
            font-weight: 700;
            color: var(--text-bright);
            font-size: clamp(1rem, 1.3vw, 1.28rem);
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        }

        .pres-table td {
            padding: clamp(0.7rem, 1.3vh, 1.1rem) clamp(0.9rem, 1.6vw, 1.5rem);
            font-size: clamp(0.95rem, 1.2vw, 1.18rem);
            color: var(--text-body);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            line-height: 1.5;
        }"""
    if table_old in html:
        html = html.replace(table_old, table_new, 1)
        print("8. Updated .pres-table th and td.")

    # 9. Update .callout-box
    callout_old = """        .callout-box {
            border-left: 4px solid var(--accent-cyan);
            background: rgba(6, 182, 212, 0.06);
            padding: clamp(0.7rem, 1.4vh, 1.2rem) clamp(1rem, 1.8vw, 1.6rem);
            border-radius: 0 12px 12px 0;
            font-size: clamp(0.85rem, 1.1vw, 1.05rem);
            line-height: 1.5;
            color: #E2E8F0;
        }"""
    callout_new = """        .callout-box {
            border-left: 5px solid var(--accent-cyan);
            background: rgba(6, 182, 212, 0.08);
            padding: clamp(0.85rem, 1.6vh, 1.35rem) clamp(1.1rem, 2vw, 1.8rem);
            border-radius: 0 14px 14px 0;
            font-size: clamp(1.02rem, 1.32vw, 1.3rem);
            line-height: 1.58;
            color: #E2E8F0;
        }"""
    if callout_old in html:
        html = html.replace(callout_old, callout_new, 1)
        print("9. Updated .callout-box.")

    # 10. Update .metric-value and .metric-label
    metric_old = """        .metric-value {
            font-family: var(--font-display);
            font-size: clamp(2rem, 3.8vw, 3.6rem);
            font-weight: 800;
            line-height: 1;
            margin-bottom: 6px;
            background: linear-gradient(135deg, #FFFFFF, var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .metric-label {
            font-size: clamp(0.78rem, 1vw, 0.95rem);
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }"""
    metric_new = """        .metric-value {
            font-family: var(--font-display);
            font-size: clamp(2.4rem, 4.4vw, 4.4rem);
            font-weight: 800;
            line-height: 1;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #FFFFFF, var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .metric-label {
            font-size: clamp(0.92rem, 1.2vw, 1.15rem);
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 600;
        }"""
    if metric_old in html:
        html = html.replace(metric_old, metric_new, 1)
        print("10. Updated .metric-value and .metric-label.")

    # 11. Update .slide-footer and .slide-counter
    footer_old = """        .slide-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            border-top: 1px solid rgba(255, 255, 255, 0.07);
            padding-top: clamp(0.4rem, 1vh, 0.8rem);
            font-size: clamp(0.7rem, 0.9vw, 0.85rem);
            color: var(--text-muted);
        }

        .slide-counter {
            font-family: var(--font-mono);
            font-weight: 600;
            color: var(--accent-cyan);
        }"""
    footer_new = """        .slide-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            padding-top: clamp(0.45rem, 1.1vh, 0.9rem);
            font-size: clamp(0.85rem, 1.1vw, 1.05rem);
            color: var(--text-muted);
        }

        .slide-counter {
            font-family: var(--font-mono);
            font-weight: 700;
            font-size: clamp(0.9rem, 1.15vw, 1.1rem);
            color: var(--accent-cyan);
        }"""
    if footer_old in html:
        html = html.replace(footer_old, footer_new, 1)
        print("11. Updated .slide-footer and .slide-counter.")

    # 12. Update .hero-title and .badge-pill
    hero_old = """        .hero-title {
            font-family: var(--font-display);
            font-size: clamp(2.4rem, 4.8vw, 4.6rem);
            font-weight: 900;
            line-height: 1.05;
            letter-spacing: -0.03em;
            color: #FFFFFF;
            margin-bottom: clamp(1rem, 2.5vh, 2rem);
        }

        .hero-gradient-text {
            background: linear-gradient(135deg, #38BDF8, #818CF8, #F472B6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-badges {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 24px;
        }

        .badge-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            color: #E2E8F0;
        }"""
    hero_new = """        .hero-title {
            font-family: var(--font-display);
            font-size: clamp(2.8rem, 5.8vw, 5.4rem);
            font-weight: 900;
            line-height: 1.08;
            letter-spacing: -0.035em;
            color: #FFFFFF;
            margin-bottom: clamp(1.2rem, 2.8vh, 2.2rem);
        }

        .hero-gradient-text {
            background: linear-gradient(135deg, #38BDF8, #818CF8, #F472B6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-badges {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 24px;
        }

        .badge-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.16);
            padding: 8px 18px;
            border-radius: 999px;
            font-size: clamp(0.88rem, 1.1vw, 1.12rem);
            font-weight: 600;
            color: #E2E8F0;
        }"""
    if hero_old in html:
        html = html.replace(hero_old, hero_new, 1)
        print("12. Updated .hero-title and .badge-pill.")

    # 13. Update Checklist typography
    chk_old = """        .check-box {
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
        }"""
    chk_new = """        .check-box {
            width: 26px;
            height: 26px;
            border-radius: 7px;
            border: 2px solid var(--accent-cyan);
            background: rgba(6, 182, 212, 0.1);
            color: var(--accent-cyan);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
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
            font-size: clamp(1.1rem, 1.45vw, 1.45rem);
            font-weight: 700;
            color: var(--text-bright);
            line-height: 1.28;
            margin-bottom: 4px;
        }

        .checklist-desc {
            font-size: clamp(0.95rem, 1.2vw, 1.18rem);
            color: var(--text-body);
            line-height: 1.52;
        }"""
    if chk_old in html:
        html = html.replace(chk_old, chk_new, 1)
        print("13. Updated checklist typography (.check-box, .checklist-label, .checklist-desc).")

    # 14. Update .stage-meter-header, .quiz-header, .quiz-question, .quiz-reveal-btn, .quiz-answer-drawer
    chk_sub_old = """        .stage-meter-header {
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
        }"""
    chk_sub_new = """        .stage-meter-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            font-family: var(--font-mono);
            font-size: clamp(0.9rem, 1.1vw, 1.05rem);
            color: var(--accent-cyan);
            font-weight: 700;
        }

        .stage-meter-bar {
            height: 9px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 14px;
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
            padding: clamp(0.9rem, 1.7vh, 1.5rem);
            position: relative;
        }

        .quiz-header {
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: var(--font-display);
            font-weight: 700;
            font-size: clamp(1.05rem, 1.35vw, 1.32rem);
            color: var(--accent-gold);
            margin-bottom: 8px;
        }

        .quiz-question {
            font-size: clamp(0.95rem, 1.2vw, 1.16rem);
            color: #E2E8F0;
            line-height: 1.52;
            margin-bottom: 12px;
        }

        .quiz-reveal-btn {
            background: rgba(245, 158, 11, 0.16);
            border: 1px solid rgba(245, 158, 11, 0.45);
            color: var(--accent-gold);
            padding: 7px 16px;
            border-radius: 8px;
            font-size: clamp(0.88rem, 1.05vw, 1.02rem);
            font-weight: 700;
            cursor: pointer;
            transition: var(--transition-smooth);
        }

        .quiz-reveal-btn:hover {
            background: var(--accent-gold);
            color: #000;
        }

        .quiz-answer-drawer {
            display: none;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px dashed rgba(245, 158, 11, 0.35);
            font-size: clamp(0.92rem, 1.15vw, 1.12rem);
            color: #CBD5E1;
            line-height: 1.5;
        }"""
    if chk_sub_old in html:
        html = html.replace(chk_sub_old, chk_sub_new, 1)
        print("14. Updated stage meters & checklist quiz card typography.")

    # 15. Update Interactive Quizzes & Q/A Arena (.quiz-badge, .quiz-prompt, .quiz-opt-btn, .quiz-feedback, .qa-q-header, .qa-answer-text)
    quiz_qa_old = """        .quiz-badge {
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
        }"""
    quiz_qa_new = """        .quiz-badge {
            font-family: var(--font-mono);
            font-size: clamp(0.82rem, 1vw, 0.95rem);
            color: var(--accent-gold);
            background: rgba(245, 158, 11, 0.16);
            padding: 4px 12px;
            border-radius: 999px;
            border: 1px solid rgba(245, 158, 11, 0.35);
            display: inline-block;
            align-self: flex-start;
            font-weight: 700;
        }

        .quiz-prompt {
            font-family: var(--font-display);
            font-size: clamp(1.12rem, 1.5vw, 1.48rem);
            font-weight: 700;
            color: var(--text-bright);
            line-height: 1.38;
        }

        .quiz-options-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .quiz-opt-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            padding: 10px 16px;
            color: var(--text-body);
            font-family: var(--font-body);
            font-size: clamp(0.95rem, 1.2vw, 1.18rem);
            text-align: left;
            cursor: pointer;
            transition: var(--transition-smooth);
            display: flex;
            align-items: center;
            gap: 10px;
            line-height: 1.38;
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
            padding: 10px 16px;
            border-radius: 10px;
            font-size: clamp(0.92rem, 1.15vw, 1.12rem);
            line-height: 1.48;
            margin-top: 6px;
        }"""
    if quiz_qa_old in html:
        html = html.replace(quiz_qa_old, quiz_qa_new, 1)
        print("15. Updated interactive quiz typography.")

    # 16. Update QA question & answer typography
    qa_old = """        .qa-q-header {
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
        }"""
    qa_new = """        .qa-q-header {
            display: flex;
            align-items: center;
            gap: 10px;
            font-family: var(--font-display);
            font-size: clamp(1.22rem, 1.55vw, 1.62rem);
            font-weight: 700;
            color: var(--accent-cyan);
            line-height: 1.28;
        }

        .qa-answer-text {
            font-size: clamp(0.98rem, 1.28vw, 1.25rem);
            color: var(--text-body);
            line-height: 1.62;
        }"""
    if qa_old in html:
        html = html.replace(qa_old, qa_new, 1)
        print("16. Updated QA typography (.qa-q-header, .qa-answer-text).")

    # 17. Update Interactive Lab input, button, and code display typography
    lab_old = """        .lab-text-input {
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
        }"""
    lab_new = """        .lab-text-input {
            flex: 1;
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 10px;
            padding: 10px 16px;
            color: var(--text-bright);
            font-family: var(--font-mono);
            font-size: clamp(0.95rem, 1.2vw, 1.15rem);
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
            background: rgba(6, 182, 212, 0.18);
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
            padding: 9px 18px;
            border-radius: 10px;
            font-family: var(--font-display);
            font-size: clamp(0.9rem, 1.15vw, 1.08rem);
            font-weight: 750;
            cursor: pointer;
            transition: var(--transition-smooth);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }"""
    if lab_old in html:
        html = html.replace(lab_old, lab_new, 1)
        print("17. Updated .lab-text-input and .lab-btn.")

    # 18. Update .code-box-display
    code_box_old = """        .code-box-display {
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
        }"""
    code_box_new = """        .code-box-display {
            font-family: var(--font-mono);
            font-size: clamp(0.92rem, 1.18vw, 1.12rem);
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 10px 16px;
            color: var(--accent-cyan);
            word-break: break-all;
            min-height: 44px;
            display: flex;
            align-items: center;
        }"""
    if code_box_old in html:
        html = html.replace(code_box_old, code_box_new, 1)
        print("18. Updated .code-box-display.")

    # 19. Update Modal Grid typography
    modal_grid_old = """        .grid-modal-title {
            font-family: var(--font-display);
            font-size: 2rem;
            color: #FFFFFF;
        }"""
    modal_grid_new = """        .grid-modal-title {
            font-family: var(--font-display);
            font-size: clamp(1.8rem, 2.8vw, 2.4rem);
            color: #FFFFFF;
        }"""
    if modal_grid_old in html:
        html = html.replace(modal_grid_old, modal_grid_new, 1)
        print("19. Updated .grid-modal-title.")

    thumb_old = """        .grid-thumb-num {
            font-family: var(--font-mono);
            font-size: 0.78rem;
            color: var(--accent-cyan);
            font-weight: 700;
        }

        .grid-thumb-title {
            font-family: var(--font-display);
            font-size: 1rem;
            color: #FFFFFF;
            font-weight: 600;
            line-height: 1.25;
        }"""
    thumb_new = """        .grid-thumb-num {
            font-family: var(--font-mono);
            font-size: 0.88rem;
            color: var(--accent-cyan);
            font-weight: 700;
        }

        .grid-thumb-title {
            font-family: var(--font-display);
            font-size: 1.08rem;
            color: #FFFFFF;
            font-weight: 600;
            line-height: 1.3;
        }"""
    if thumb_old in html:
        html = html.replace(thumb_old, thumb_new, 1)
        print("20. Updated .grid-thumb-num and .grid-thumb-title.")

    # 21. Update Media Queries for Breakpoints (Desktop, Tablet, Mobile)
    mq_block_old = """        /* Large Desktop & 4K Displays (>= 1600px) */
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
        }"""
    mq_block_new = """        /* Large Desktop & 4K Displays (>= 1600px) */
        @media (min-width: 1600px) {
            .slide {
                padding: 3.2rem 6.5rem;
            }
            .slide-main-title {
                font-size: 3.8rem;
            }
            .hero-title {
                font-size: 5.6rem;
            }
            .card-title {
                font-size: 1.85rem;
            }
            .card-desc {
                font-size: 1.22rem;
            }
            .slide-subtitle {
                font-size: 1.6rem;
            }
            .checklist-label {
                font-size: 1.5rem;
            }
            .checklist-desc {
                font-size: 1.22rem;
            }
            .qa-q-header {
                font-size: 1.7rem;
            }
            .qa-answer-text {
                font-size: 1.3rem;
            }
            .quiz-prompt {
                font-size: 1.55rem;
            }
            .quiz-opt-btn {
                font-size: 1.22rem;
            }
            .pres-card {
                padding: 2rem 2.4rem;
            }
        }"""
    if mq_block_old in html:
        html = html.replace(mq_block_old, mq_block_new, 1)
        print("21. Updated Large Desktop (>= 1600px) typography.")

    # 22. Update Mobile Media Query (<= 768px) typography
    mq_mobile_old = """            .slide-tag {
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
            }"""
    mq_mobile_new = """            .slide-tag {
                font-size: 0.78rem;
                padding: 4px 10px;
            }
            .slide-breadcrumb {
                font-size: 0.84rem;
            }
            .slide-main-title {
                font-size: clamp(1.6rem, 6.2vw, 2.2rem);
                line-height: 1.2;
            }
            .slide-subtitle {
                font-size: clamp(0.96rem, 3.8vw, 1.15rem);
                line-height: 1.48;
            }
            .hero-title {
                font-size: clamp(2.1rem, 7.8vw, 2.9rem);
                line-height: 1.12;
                margin-bottom: 14px;
            }
            .card-title {
                font-size: 1.3rem;
            }
            .card-desc {
                font-size: 1rem;
                line-height: 1.55;
            }
            .checklist-label {
                font-size: 1.18rem;
            }
            .checklist-desc {
                font-size: 0.98rem;
            }
            .quiz-prompt {
                font-size: 1.18rem;
            }
            .quiz-opt-btn {
                font-size: 0.98rem;
                padding: 10px 14px;
            }
            .qa-q-header {
                font-size: 1.25rem;
            }
            .qa-answer-text {
                font-size: 1.02rem;
                line-height: 1.58;
            }"""
    if mq_mobile_old in html:
        html = html.replace(mq_mobile_old, mq_mobile_new, 1)
        print("22. Updated Mobile (<= 768px) typography.")

    # 23. Update Small Phones (<= 480px) typography
    mq_small_old = """            .slide-main-title {
                font-size: 1.35rem;
            }
            .hero-title {
                font-size: 1.65rem;
            }
            .badge-pill {
                font-size: 0.72rem;
                padding: 4px 10px;
            }"""
    mq_small_new = """            .slide-main-title {
                font-size: 1.5rem;
            }
            .hero-title {
                font-size: 1.95rem;
            }
            .badge-pill {
                font-size: 0.82rem;
                padding: 5px 12px;
            }
            .card-title {
                font-size: 1.22rem;
            }
            .card-desc {
                font-size: 0.95rem;
            }
            .slide-subtitle {
                font-size: 0.98rem;
            }"""
    if mq_small_old in html:
        html = html.replace(mq_small_old, mq_small_new, 1)
        print("23. Updated Small Phones (<= 480px) typography.")

    # 24. Upgrade in-body inline small font sizes across all slides
    # Find the position of <body> so we only edit slide content
    body_idx = html.find("<body>")
    head_part = html[:body_idx]
    body_part = html[body_idx:]

    # Map of inline font size upgrades in body:
    # 0.85rem -> 1.05rem
    # 0.8rem  -> 0.98rem
    # 0.78rem -> 0.95rem
    # 0.75rem -> 0.92rem
    # 0.72rem -> 0.9rem
    # 0.7rem  -> 0.88rem
    # 0.65rem -> 0.82rem
    # 0.82rem -> 1rem
    # ol/ul font-size: 0.9rem -> font-size: 1.08rem
    inline_replacements = [
        ('font-size: 0.85rem;', 'font-size: 1.05rem;'),
        ('font-size: 0.82rem;', 'font-size: 1rem;'),
        ('font-size: 0.8rem;', 'font-size: 0.98rem;'),
        ('font-size: 0.78rem;', 'font-size: 0.95rem;'),
        ('font-size: 0.75rem;', 'font-size: 0.92rem;'),
        ('font-size:0.75rem;', 'font-size: 0.92rem;'),
        ('font-size: 0.72rem;', 'font-size: 0.9rem;'),
        ('font-size: 0.7rem;', 'font-size: 0.88rem;'),
        ('font-size: 0.65rem;', 'font-size: 0.82rem;'),
        ('font-size: 0.9rem; color: #CBD5E1;', 'font-size: 1.08rem; color: #CBD5E1;'),
    ]

    for old_s, new_s in inline_replacements:
        count = body_part.count(old_s)
        if count > 0:
            body_part = body_part.replace(old_s, new_s)
            print(f"24. Replaced {count} instances of '{old_s}' with '{new_s}' in slide body.")

    html = head_part + body_part

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully updated typography across the entire presentation!")

if __name__ == "__main__":
    scale_typography()
