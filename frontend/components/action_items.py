"""
action_items.py — Premium dark-theme action items sorted by urgency.
All styling uses inline styles only.
"""
from typing import Any, Dict, List, Tuple

import streamlit as st


SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}

_ICON = {"critical": "\U0001f534", "high": "\U0001f7e0", "medium": "\U0001f7e1", "low": "\U0001f7e2"}

_BADGE_STYLES = {
    "critical": ("color:#f87171;background:rgba(248,113,113,0.15);border:1px solid rgba(248,113,113,0.25);"),
    "high":     ("color:#fbbf24;background:rgba(251,191,36,0.15);border:1px solid rgba(251,191,36,0.25);"),
    "medium":   ("color:#60a5fa;background:rgba(96,165,250,0.15);border:1px solid rgba(96,165,250,0.25);"),
    "low":      ("color:#34d399;background:rgba(52,211,153,0.15);border:1px solid rgba(52,211,153,0.25);"),
}

_ITEM_STYLE = (
    "display:flex;gap:0.85rem;align-items:flex-start;"
    "padding:0.85rem 1rem;border-radius:10px;"
    "background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);"
    "margin-bottom:0.6rem;"
)


def _collect_action_items(analysis: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    items: List[Tuple[str, str, str]] = []
    for issue in analysis.get("detailed_feedback") or []:
        level = (issue.get("severity_level") or "low").lower()
        title = issue.get("issue_title", "")
        for action in issue.get("action_items") or []:
            items.append((level, title, action))
    if not items:
        for suggestion in analysis.get("suggestions") or []:
            items.append(("medium", "General", suggestion))
    items.sort(key=lambda row: SEVERITY_RANK.get(row[0], 99))
    return items


def display_action_items(analysis: Dict[str, Any]) -> None:
    items = _collect_action_items(analysis)
    if not items:
        return

    st.markdown("### \u26a1 Action Items")
    st.caption("Concrete steps to improve your score, sorted by urgency.")

    for level, source, action in items:
        icon = _ICON.get(level, "\U0001f7e2")
        badge_style = _BADGE_STYLES.get(level, _BADGE_STYLES["low"])
        source_badge = ""
        if source:
            short = source[:30]
            source_badge = (
                '<span style="display:inline-flex;padding:0.15rem 0.5rem;border-radius:9999px;'
                'font-size:0.65rem;font-weight:600;margin-left:0.4rem;' + badge_style + '">'
                + short + '</span>'
            )
        st.markdown(
            '<div style="' + _ITEM_STYLE + '">'
            '<span style="font-size:1.1rem;flex-shrink:0;margin-top:0.1rem;">' + icon + '</span>'
            '<div style="font-size:0.85rem;color:#94a3b8;line-height:1.5;">' + action + source_badge + '</div>'
            '</div>',
            unsafe_allow_html=True,
        )
