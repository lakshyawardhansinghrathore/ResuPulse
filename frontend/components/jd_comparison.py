"""
jd_comparison.py — Premium dark-theme JD match display.
All styling uses inline styles only.
"""
from typing import Any, Dict, Optional

import streamlit as st

_BADGE_SUCCESS = (
    "display:inline-flex;align-items:center;padding:0.2rem 0.65rem;margin:0.2rem;"
    "border-radius:9999px;font-size:0.75rem;font-weight:600;"
    "background:rgba(52,211,153,0.12);color:#34d399;border:1px solid rgba(52,211,153,0.25);"
)

_BADGE_DANGER = (
    "display:inline-flex;align-items:center;padding:0.2rem 0.65rem;margin:0.2rem;"
    "border-radius:9999px;font-size:0.75rem;font-weight:600;"
    "background:rgba(248,113,113,0.12);color:#f87171;border:1px solid rgba(248,113,113,0.25);"
)

_METRIC_BOX = (
    "background:rgba(22,25,41,0.7);border:1px solid rgba(99,102,241,0.18);"
    "border-radius:12px;padding:1.25rem;text-align:center;"
    "backdrop-filter:blur(16px);margin-bottom:0.75rem;"
)

_ITEM_STYLE = (
    "display:flex;gap:0.85rem;align-items:flex-start;"
    "padding:0.75rem 1rem;border-radius:10px;"
    "background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);"
    "margin-bottom:0.5rem;"
)


def display_jd_comparison(jd_comparison: Optional[Dict[str, Any]]) -> None:
    if not jd_comparison:
        return

    st.markdown("### \U0001f3af Job Description Match")

    match_pct = float(jd_comparison.get("match_percentage", 0))
    semantic  = float(jd_comparison.get("semantic_similarity", 0))
    matched   = jd_comparison.get("matched_keywords", []) or []
    missing   = jd_comparison.get("missing_keywords",  []) or []
    gap       = jd_comparison.get("skills_gap",         []) or []

    pct_color = "#34d399" if match_pct >= 70 else "#fbbf24" if match_pct >= 50 else "#f87171"
    sem_color = "#34d399" if semantic >= 0.7 else "#fbbf24" if semantic >= 0.5 else "#f87171"

    m1, m2 = st.columns(2)
    with m1:
        st.markdown(
            '<div style="' + _METRIC_BOX + '">'
            '<div style="font-size:0.75rem;font-weight:600;color:#64748b;text-transform:uppercase;'
            'letter-spacing:0.08em;margin-bottom:0.35rem;">Match Percentage</div>'
            '<div style="font-size:3rem;font-weight:900;color:' + pct_color + ';'
            'letter-spacing:-0.03em;line-height:1;">' + f'{match_pct:.0f}%' + '</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.progress(min(max(match_pct / 100.0, 0.0), 1.0))

    with m2:
        st.markdown(
            '<div style="' + _METRIC_BOX + '">'
            '<div style="font-size:0.75rem;font-weight:600;color:#64748b;text-transform:uppercase;'
            'letter-spacing:0.08em;margin-bottom:0.35rem;">Semantic Similarity</div>'
            '<div style="font-size:3rem;font-weight:900;color:' + sem_color + ';'
            'letter-spacing:-0.03em;line-height:1;">' + f'{semantic * 100:.0f}%' + '</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.progress(min(max(semantic, 0.0), 1.0))

    st.markdown("")
    kw_l, kw_r = st.columns(2)

    with kw_l:
        st.markdown(
            '<div style="font-size:0.8rem;font-weight:600;color:#64748b;'
            'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.6rem;">'
            '\u2705 Matched Keywords</div>',
            unsafe_allow_html=True,
        )
        if matched:
            tags = "".join('<span style="' + _BADGE_SUCCESS + '">' + kw + '</span>' for kw in matched[:15])
            st.markdown('<div style="display:flex;flex-wrap:wrap;gap:0.3rem;">' + tags + '</div>',
                        unsafe_allow_html=True)
        else:
            st.caption("No keywords matched yet")

    with kw_r:
        st.markdown(
            '<div style="font-size:0.8rem;font-weight:600;color:#64748b;'
            'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.6rem;">'
            '\u274c Missing Keywords</div>',
            unsafe_allow_html=True,
        )
        if missing:
            tags = "".join('<span style="' + _BADGE_DANGER + '">' + kw + '</span>' for kw in missing[:10])
            st.markdown('<div style="display:flex;flex-wrap:wrap;gap:0.3rem;">' + tags + '</div>',
                        unsafe_allow_html=True)
        else:
            st.success("All key terms present! \U0001f389")

    if gap:
        st.markdown("")
        st.markdown(
            '<div style="font-size:0.8rem;font-weight:600;color:#64748b;'
            'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.6rem;">'
            '\U0001f4ca Skills Gap Areas</div>',
            unsafe_allow_html=True,
        )
        for skill in gap[:10]:
            st.markdown(
                '<div style="' + _ITEM_STYLE + '">'
                '<span style="font-size:1rem;flex-shrink:0;">\U0001f4cc</span>'
                '<div style="font-size:0.85rem;color:#94a3b8;line-height:1.5;">' + skill + '</div>'
                '</div>',
                unsafe_allow_html=True,
            )
