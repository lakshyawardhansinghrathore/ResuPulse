"""
skill_validation.py — Premium dark-theme skill validation with badge tags.
All styling uses inline styles only.
"""
from typing import Any, Dict

import streamlit as st

_TAG_VALIDATED = (
    "display:inline-flex;align-items:center;gap:0.3rem;"
    "padding:0.3rem 0.75rem;margin:0.2rem;border-radius:9999px;"
    "font-size:0.85rem;font-weight:500;"
    "background:rgba(52,211,153,0.12);color:#34d399;"
    "border:1px solid rgba(52,211,153,0.3);"
)

_TAG_UNVALIDATED = (
    "display:inline-flex;align-items:center;gap:0.3rem;"
    "padding:0.3rem 0.75rem;margin:0.2rem;border-radius:9999px;"
    "font-size:0.85rem;font-weight:500;"
    "background:rgba(248,113,113,0.12);color:#f87171;"
    "border:1px solid rgba(248,113,113,0.3);"
)

_LABEL_STYLE = (
    "font-size:0.8rem;font-weight:600;color:#64748b;"
    "text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.6rem;"
)


def display_skill_validation(analysis: Dict[str, Any]) -> None:
    details     = analysis.get("skill_validation_details") or {}
    validated   = details.get("validated",   [])
    unvalidated = details.get("unvalidated", [])
    total       = details.get("total", len(validated) + len(unvalidated))
    pct         = details.get("validation_pct", 0.0)

    st.markdown("### \u2705 Skill Validation")

    if total == 0:
        st.markdown(
            '<div style="text-align:center;padding:2.5rem 2rem;color:#64748b;">'
            '<div style="font-size:3rem;margin-bottom:0.75rem;opacity:0.4;">\U0001f50d</div>'
            '<div style="font-size:1.1rem;font-weight:600;color:#94a3b8;margin-bottom:0.4rem;">No Skills Detected</div>'
            '<div style="font-size:0.85rem;max-width:280px;margin:0 auto;">Add a clear Skills section to your resume.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    # Metric row
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Skills", total)
    c2.metric("Validated", len(validated))
    c3.metric("Validation %", f"{pct:.0f}%")

    st.progress(min(max(pct / 100.0, 0.0), 1.0))
    st.markdown("")

    # Skill tag clouds
    col_val, col_unval = st.columns(2)

    with col_val:
        if validated:
            st.markdown('<div style="' + _LABEL_STYLE + '">\u2705 Validated (' + str(len(validated)) + ')</div>',
                        unsafe_allow_html=True)
            tags = ""
            for entry in validated:
                skill      = entry.get("skill", "?") if isinstance(entry, dict) else str(entry)
                similarity = entry.get("similarity") if isinstance(entry, dict) else None
                sim_suffix = f" {similarity*100:.0f}%" if isinstance(similarity, (int, float)) else ""
                tags += '<span style="' + _TAG_VALIDATED + '">\u2713 ' + skill + sim_suffix + '</span>'
            st.markdown('<div style="display:flex;flex-wrap:wrap;gap:0.3rem;">' + tags + '</div>',
                        unsafe_allow_html=True)
        else:
            st.warning("No validated skills")

    with col_unval:
        if unvalidated:
            st.markdown('<div style="' + _LABEL_STYLE + '">\u26a0\ufe0f Unvalidated (' + str(len(unvalidated)) + ')</div>',
                        unsafe_allow_html=True)
            st.caption("Listed but not demonstrated in projects or experience.")
            tags = "".join(
                '<span style="' + _TAG_UNVALIDATED + '">! ' + skill + '</span>'
                for skill in unvalidated
            )
            st.markdown('<div style="display:flex;flex-wrap:wrap;gap:0.3rem;">' + tags + '</div>',
                        unsafe_allow_html=True)
        else:
            st.success("All skills validated! \U0001f389")
