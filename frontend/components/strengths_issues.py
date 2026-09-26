"""
strengths_issues.py — Premium dark-theme strengths & critical issues.
All styling uses inline styles only.
"""
from typing import Any, Dict, List
import streamlit as st

_ITEM_STYLE = (
    "display:flex;gap:0.85rem;align-items:flex-start;"
    "padding:0.85rem 1rem;border-radius:10px;"
    "background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);"
    "margin-bottom:0.6rem;"
)


def display_strengths(strengths: List[str]) -> None:
    st.markdown("### \U0001f4aa Strengths")
    if not strengths:
        st.markdown(
            '<div style="text-align:center;padding:2.5rem 2rem;color:#64748b;">'
            '<div style="font-size:3rem;margin-bottom:0.75rem;opacity:0.4;">\U0001f331</div>'
            '<div style="font-size:1.1rem;font-weight:600;color:#94a3b8;margin-bottom:0.4rem;">Keep Improving</div>'
            '<div style="font-size:0.85rem;max-width:280px;margin:0 auto;">Optimize your resume further to unlock detected strengths.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    for item in strengths:
        st.markdown(
            '<div style="' + _ITEM_STYLE + '">'
            '<span style="font-size:1.1rem;flex-shrink:0;">\u2705</span>'
            '<div style="font-size:0.875rem;color:#94a3b8;line-height:1.5;">' + item + '</div>'
            '</div>',
            unsafe_allow_html=True,
        )


def display_critical_issues(analysis: Dict[str, Any]) -> None:
    critical = analysis.get("critical_issues") or []
    summary  = analysis.get("issues_summary") or []

    if not critical and not summary:
        st.markdown(
            '<div style="display:flex;gap:0.75rem;align-items:flex-start;'
            'padding:0.9rem 1.1rem;border-radius:10px;margin:0.75rem 0;font-size:0.875rem;'
            'border-left:3px solid #34d399;background:rgba(52,211,153,0.12);color:#94a3b8;">'
            '<span>\U0001f389</span>'
            '<div><strong style="color:#f1f5f9;">No Critical Issues Found!</strong><br>'
            'Your resume doesn\u2019t have any urgent problems. Nice work!</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown("### \U0001f6a8 Critical Issues")
    st.markdown(
        '<div style="display:flex;gap:0.75rem;align-items:flex-start;'
        'padding:0.9rem 1.1rem;border-radius:10px;margin:0.75rem 0;font-size:0.875rem;'
        'border-left:3px solid #f87171;background:rgba(248,113,113,0.12);color:#94a3b8;">'
        '<span>\u26a0\ufe0f</span>'
        '<div><strong style="color:#f1f5f9;">Address these first</strong> for the greatest improvement in your ATS score.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    for item in critical:
        st.markdown(
            '<div style="' + _ITEM_STYLE + '">'
            '<span style="font-size:1.1rem;flex-shrink:0;">\U0001f534</span>'
            '<div style="font-size:0.875rem;color:#94a3b8;line-height:1.5;">' + item + '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    extra = [s for s in summary if s not in critical]
    if extra:
        with st.expander("\U0001f4cb Additional Flagged Items", expanded=False):
            for item in extra:
                st.markdown(
                    '<div style="' + _ITEM_STYLE + '">'
                    '<span style="font-size:1.1rem;flex-shrink:0;">\U0001f7e0</span>'
                    '<div style="font-size:0.875rem;color:#94a3b8;line-height:1.5;">' + item + '</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
