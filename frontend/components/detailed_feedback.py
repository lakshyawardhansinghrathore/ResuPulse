"""
detailed_feedback.py — Premium dark-theme issue cards with severity grouping.
All styling uses inline styles only.
"""
from typing import Any, Dict, List

import streamlit as st

from frontend.components._helpers import get_severity_style


SEVERITY_ORDER = ["critical", "high", "medium", "low"]

_SEVERITY_COLORS = {
    "critical": ("#f87171", "rgba(248,113,113,0.05)", "rgba(248,113,113,0.15)"),
    "high":     ("#fbbf24", "rgba(251,191,36,0.05)",  "rgba(251,191,36,0.15)"),
    "medium":   ("#60a5fa", "rgba(96,165,250,0.05)",  "rgba(96,165,250,0.15)"),
    "low":      ("#34d399", "rgba(52,211,153,0.05)",   "rgba(52,211,153,0.15)"),
}

_SEVERITY_BADGE = {
    "critical": ("\U0001f534 Critical", "#f87171", "rgba(248,113,113,0.15)", "rgba(248,113,113,0.25)"),
    "high":     ("\U0001f7e0 High",     "#fbbf24", "rgba(251,191,36,0.15)",  "rgba(251,191,36,0.25)"),
    "medium":   ("\U0001f535 Medium",   "#60a5fa", "rgba(96,165,250,0.15)",  "rgba(96,165,250,0.25)"),
    "low":      ("\U0001f7e2 Low",      "#34d399", "rgba(52,211,153,0.15)",  "rgba(52,211,153,0.25)"),
}

_DETAIL_ITEM = (
    "display:flex;gap:0.85rem;align-items:flex-start;"
    "padding:0.75rem 1rem;border-radius:10px;"
    "background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);"
    "margin-bottom:0.5rem;"
)


def _group_by_severity(issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {level: [] for level in SEVERITY_ORDER}
    for issue in issues:
        level = (issue.get("severity_level") or "low").lower()
        grouped.setdefault(level, []).append(issue)
    return grouped


def _render_issue(issue: Dict[str, Any]) -> None:
    sev_level   = (issue.get("severity_level") or "low").lower()
    accent, card_bg, card_border = _SEVERITY_COLORS.get(sev_level, _SEVERITY_COLORS["low"])
    badge_label, badge_color, badge_bg, badge_bdr = _SEVERITY_BADGE.get(sev_level, _SEVERITY_BADGE["low"])

    title       = issue.get("issue_title", "Untitled issue")
    impact      = (issue.get("ats_impact") or "").lower()
    explanation = issue.get("explanation", "")
    where       = issue.get("where_it_appears", "")
    how_to_fix  = issue.get("how_to_fix", "")
    action_items = issue.get("action_items") or []
    example     = issue.get("example_improvement", "")

    # Card header
    st.markdown(
        '<div style="background:' + card_bg + ';border-radius:12px;border:1px solid ' + card_border + ';'
        'padding:1rem 1.25rem;margin-bottom:0.6rem;border-left:3px solid ' + accent + ';">'
        '<div style="display:flex;align-items:center;justify-content:space-between;gap:0.75rem;flex-wrap:wrap;">'
        '<div style="font-size:0.9375rem;font-weight:600;color:#f1f5f9;">' + title + '</div>'
        '<span style="display:inline-flex;align-items:center;padding:0.2rem 0.65rem;border-radius:9999px;'
        'font-size:0.7rem;font-weight:600;background:' + badge_bg + ';border:1px solid ' + badge_bdr + ';'
        'color:' + badge_color + ';">' + badge_label + '</span>'
        '</div>'
        + (('<div style="font-size:0.7rem;color:#64748b;font-weight:500;letter-spacing:0.04em;'
            'text-transform:uppercase;margin-top:0.3rem;">ATS Impact: '
            '<span style="color:' + accent + ';font-weight:600;">' + impact + '</span></div>')
           if impact else '')
        + '</div>',
        unsafe_allow_html=True,
    )

    with st.expander("\U0001f4cb View Details", expanded=False):
        if explanation:
            st.markdown(
                '<div style="' + _DETAIL_ITEM + '">'
                '<span style="font-size:1rem;flex-shrink:0;">\U0001f4a1</span>'
                '<div style="font-size:0.85rem;color:#94a3b8;line-height:1.5;">'
                '<strong style="color:#f1f5f9;">What\'s happening:</strong> ' + explanation + '</div></div>',
                unsafe_allow_html=True,
            )
        if where:
            st.markdown(
                '<div style="' + _DETAIL_ITEM + '">'
                '<span style="font-size:1rem;flex-shrink:0;">\U0001f4cd</span>'
                '<div style="font-size:0.85rem;color:#94a3b8;line-height:1.5;">'
                '<strong style="color:#f1f5f9;">Where it appears:</strong> ' + where + '</div></div>',
                unsafe_allow_html=True,
            )
        if how_to_fix:
            st.markdown(
                '<div style="' + _DETAIL_ITEM + '">'
                '<span style="font-size:1rem;flex-shrink:0;">\U0001f527</span>'
                '<div style="font-size:0.85rem;color:#94a3b8;line-height:1.5;">'
                '<strong style="color:#f1f5f9;">How to fix:</strong> ' + how_to_fix + '</div></div>',
                unsafe_allow_html=True,
            )
        if action_items:
            st.markdown(
                '<div style="font-size:0.8rem;font-weight:600;color:#64748b;'
                'text-transform:uppercase;letter-spacing:0.06em;margin:0.5rem 0 0.4rem;">Action Items</div>',
                unsafe_allow_html=True,
            )
            for item in action_items:
                st.markdown(
                    '<div style="' + _DETAIL_ITEM + '">'
                    '<span style="font-size:1rem;flex-shrink:0;">\u2713</span>'
                    '<div style="font-size:0.85rem;color:#94a3b8;line-height:1.5;">' + item + '</div></div>',
                    unsafe_allow_html=True,
                )
        if example:
            st.markdown("**\u2728 Example Improvement:**")
            st.code(example, language="text")


def display_detailed_feedback(analysis: Dict[str, Any]) -> None:
    issues = analysis.get("detailed_feedback") or []
    if not issues:
        return

    st.markdown("### \U0001f50d Detailed Feedback")
    st.caption(str(len(issues)) + " issue(s) flagged \u2014 grouped by severity. Click any card to expand.")

    grouped = _group_by_severity(issues)
    for level in SEVERITY_ORDER:
        items = grouped.get(level, [])
        if not items:
            continue

        badge_label, badge_color, badge_bg, badge_bdr = _SEVERITY_BADGE.get(level, _SEVERITY_BADGE["low"])
        st.markdown(
            '<div style="display:flex;align-items:center;gap:0.6rem;margin:1.25rem 0 0.6rem;">'
            '<span style="display:inline-flex;align-items:center;padding:0.2rem 0.65rem;border-radius:9999px;'
            'font-size:0.7rem;font-weight:600;background:' + badge_bg + ';border:1px solid ' + badge_bdr + ';'
            'color:' + badge_color + ';">' + badge_label + '</span>'
            '<span style="font-size:0.8rem;color:#64748b;font-weight:500;">'
            + str(len(items)) + ' issue(s)</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        for issue in items:
            _render_issue(issue)
