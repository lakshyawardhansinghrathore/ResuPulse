"""
score_display.py — Premium dark-theme score gauge and breakdown bars.
All styling uses inline styles (Streamlit strips class= attributes).
"""
from typing import Any, Dict
import streamlit as st
from frontend.components._helpers import get_score_color, get_score_emoji


# Component max scores match backend/core/config.py SCORE_WEIGHTS.
COMPONENTS = [
    ("Formatting",        "formatting",        20, "\U0001f4dd"),
    ("Keywords & Skills", "keywords",          25, "\U0001f511"),
    ("Content Quality",   "content",           25, "\U0001f4c4"),
    ("Skill Validation",  "skill_validation",  15, "\u2705"),
    ("ATS Compatibility", "ats_compatibility", 15, "\U0001f916"),
]


def _bar_color(pct: float) -> str:
    if pct >= 0.8:
        return "linear-gradient(90deg,#059669,#34d399)"
    if pct >= 0.6:
        return "linear-gradient(90deg,#d97706,#fbbf24)"
    return "linear-gradient(90deg,#dc2626,#f87171)"


def _score_info(score: float):
    if score >= 80:
        return "\u2705 Excellent", "#34d399", "rgba(52,211,153,0.15)", "rgba(52,211,153,0.35)"
    if score >= 60:
        return "\u26a0\ufe0f Needs Work", "#fbbf24", "rgba(251,191,36,0.15)", "rgba(251,191,36,0.35)"
    return "\u274c Needs Improvement", "#f87171", "rgba(248,113,113,0.15)", "rgba(248,113,113,0.35)"


def _svg_gauge(score: float) -> str:
    r = 74
    cx = cy = 90
    stroke_w = 10
    circ = 2 * 3.14159 * r
    offset = circ * (1 - score / 100)
    _, color, _, _ = _score_info(score)
    uid = int(score * 10)

    return (
        f'<svg width="180" height="180" viewBox="0 0 180 180">'
        f'<defs><filter id="g{uid}"><feGaussianBlur stdDeviation="4" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="{stroke_w}" stroke-linecap="round"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke_w}" '
        f'stroke-linecap="round" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}" '
        f'transform="rotate(-90 {cx} {cy})" filter="url(#g{uid})" '
        f'style="transition:stroke-dashoffset 1s cubic-bezier(0.4,0,0.2,1);"/>'
        f'<text x="{cx}" y="{cy - 8}" text-anchor="middle" font-family="Inter,sans-serif" '
        f'font-size="36" font-weight="900" fill="{color}" letter-spacing="-2">{score:.0f}</text>'
        f'<text x="{cx}" y="{cy + 18}" text-anchor="middle" font-family="Inter,sans-serif" '
        f'font-size="12" font-weight="600" fill="rgba(255,255,255,0.35)" letter-spacing="1">/ 100</text>'
        f'</svg>'
    )


def display_overall_score(analysis: Dict[str, Any]) -> None:
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    interpretation = analysis.get("interpretation", "")
    badge_label, color, bg, border = _score_info(score)
    emoji = get_score_emoji(score)
    svg = _svg_gauge(score)

    st.markdown("## \U0001f4ca Analysis Results")
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        interp_html = ""
        if interpretation:
            interp_html = (
                '<div style="font-size:0.85rem;color:#94a3b8;text-align:center;'
                'margin-top:0.6rem;max-width:320px;line-height:1.5;">'
                + interpretation + '</div>'
            )
        st.markdown(
            '<div style="display:flex;flex-direction:column;align-items:center;padding:2rem;'
            'background:rgba(22,25,41,0.7);border:1px solid rgba(99,102,241,0.18);'
            'border-radius:24px;backdrop-filter:blur(16px);box-shadow:0 20px 48px rgba(0,0,0,0.6);">'
            '<div style="font-size:0.8rem;font-weight:600;text-transform:uppercase;'
            'letter-spacing:0.1em;color:#64748b;margin-bottom:1rem;">Overall ATS Score</div>'
            + svg +
            '<div style="display:inline-flex;align-items:center;gap:0.4rem;padding:0.35rem 1rem;'
            'border-radius:9999px;font-size:0.85rem;font-weight:600;margin-top:0.75rem;'
            'background:' + bg + ';border:1px solid ' + border + ';color:' + color + ';">'
            + emoji + ' ' + badge_label + '</div>'
            + interp_html +
            '</div>',
            unsafe_allow_html=True,
        )


def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    component_scores = analysis.get("component_scores") or {}
    st.markdown("### \U0001f4c8 Score Breakdown")

    left, right = st.columns(2)
    for i, (label, key, max_score, icon) in enumerate(COMPONENTS):
        value = float(component_scores.get(key, 0))
        pct = value / max_score if max_score else 0
        pct_pct = round(pct * 100, 1)
        bar_bg = _bar_color(pct)
        val_color = "#34d399" if pct >= 0.8 else "#fbbf24" if pct >= 0.6 else "#f87171"

        col = left if i % 2 == 0 else right
        with col:
            st.markdown(
                '<div style="margin-bottom:1rem;">'
                '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem;">'
                '<span style="font-size:0.85rem;font-weight:600;color:#94a3b8;">'
                + icon + ' ' + label + '</span>'
                '<span style="font-size:0.85rem;font-weight:700;color:' + val_color + ';">'
                + f'{value:.0f}' + '<span style="color:#64748b;font-weight:400;">/' + str(max_score) + '</span></span>'
                '</div>'
                '<div style="height:8px;background:rgba(255,255,255,0.06);border-radius:9999px;overflow:hidden;">'
                '<div style="height:100%;border-radius:9999px;width:' + str(pct_pct) + '%;'
                'background:' + bar_bg + ';transition:width 0.8s cubic-bezier(0.4,0,0.2,1);"></div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )
