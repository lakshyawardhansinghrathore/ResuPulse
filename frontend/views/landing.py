import streamlit as st


def render():
    """Premium dark landing page for ResuPulse — uses only inline styles."""

    # ------------------------------------------------------------------ #
    #  Hero Section                                                        #
    # ------------------------------------------------------------------ #
    st.markdown(
        '<div style="position:relative;text-align:center;padding:3.5rem 2rem 3rem;'
        'border-radius:20px;overflow:hidden;margin-bottom:2rem;'
        'background:linear-gradient(135deg,rgba(99,102,241,0.15),rgba(139,92,246,0.10),rgba(167,139,250,0.08));'
        'border:1px solid rgba(99,102,241,0.18);backdrop-filter:blur(20px);'
        'box-shadow:0 25px 60px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.07);">'
        #  Badge
        '<div style="display:inline-block;background:rgba(99,102,241,0.15);'
        'border:1px solid rgba(99,102,241,0.35);color:#818cf8;font-size:0.85rem;'
        'font-weight:600;letter-spacing:0.06em;text-transform:uppercase;'
        'padding:0.3rem 1rem;border-radius:9999px;margin-bottom:1.25rem;">'
        '\u2726 AI-Powered ATS Intelligence</div>'
        #  Title
        '<div style="font-size:clamp(2rem,5vw,3.2rem);font-weight:900;letter-spacing:-0.03em;'
        'line-height:1.1;margin-bottom:1rem;'
        'background:linear-gradient(135deg,#f1f5f9,#a78bfa 50%,#818cf8);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">'
        'Know Why Your Resume<br>Gets Rejected \u2014 Before It Does</div>'
        #  Subtitle
        '<div style="font-size:1.1rem;color:#94a3b8;max-width:560px;margin:0 auto 2rem;'
        'line-height:1.6;font-weight:400;">'
        'Upload your resume and get an instant, deeply detailed ATS score powered by '
        'LLM parsing, semantic skill validation, and hybrid JD matching.</div>'
        #  Stats strip
        '<div style="display:flex;justify-content:center;gap:2.5rem;flex-wrap:wrap;">'
        '<div style="text-align:center;"><span style="font-size:1.75rem;font-weight:800;color:#818cf8;display:block;line-height:1;">5</span>'
        '<span style="font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;font-weight:500;">Score Dimensions</span></div>'
        '<div style="text-align:center;"><span style="font-size:1.75rem;font-weight:800;color:#818cf8;display:block;line-height:1;">4x</span>'
        '<span style="font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;font-weight:500;">LLM Fallback Chain</span></div>'
        '<div style="text-align:center;"><span style="font-size:1.75rem;font-weight:800;color:#818cf8;display:block;line-height:1;">100%</span>'
        '<span style="font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;font-weight:500;">Private &amp; Secure</span></div>'
        '<div style="text-align:center;"><span style="font-size:1.75rem;font-weight:800;color:#818cf8;display:block;line-height:1;">PDF</span>'
        '<span style="font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;font-weight:500;">Export Ready</span></div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # CTA button
    _, mid, _ = st.columns([1.2, 1, 1.2])
    with mid:
        if st.button("\U0001f680 Analyze My Resume", use_container_width=True, type="primary"):
            st.session_state.current_view = 'scorer'
            st.rerun()

    st.markdown("")

    # ------------------------------------------------------------------ #
    #  Features Section Title                                              #
    # ------------------------------------------------------------------ #
    st.markdown("## \u2728 What Makes ResuPulse Different")
    st.caption("Not just keyword counting \u2014 we go three layers deep.")

    # ------------------------------------------------------------------ #
    #  Feature Cards — using st.columns + inline-styled divs              #
    # ------------------------------------------------------------------ #
    CARD_STYLE = (
        "background:rgba(22,25,41,0.7);"
        "border:1px solid rgba(99,102,241,0.18);"
        "border-radius:16px;padding:1.5rem 1.25rem;"
        "backdrop-filter:blur(16px);"
        "min-height:200px;"
        "border-top:2px solid rgba(99,102,241,0.3);"
    )

    features = [
        ("\U0001f9e0", "Semantic Skill Validation",
         "Uses **sentence embeddings** to verify that skills you list are actually "
         "*demonstrated* in your projects. Listing \u201cPython\u201d without evidence won\u2019t pass."),
        ("\u26a1", "Groq LLM Parsing",
         "Llama 3.3 70B extracts structured data from raw resume text with a "
         "**4-model fallback chain** \u2014 zero failures even under rate limits."),
        ("\U0001f50d", "Hybrid JD Matching",
         "Combines **fuzzy string matching** (RapidFuzz, 80% threshold) "
         "with cosine similarity of dense embeddings for nuanced JD alignment."),
        ("\U0001f4ca", "5-Component Score",
         "100-point weighted composite across Formatting, Keywords, Content Quality, "
         "Skill Validation, and ATS Compatibility with penalties and bonuses."),
        ("\U0001f3af", "Actionable Diagnostics",
         "Not just a score \u2014 produces **before/after rewrite examples**, "
         "step-by-step action items, and severity-ranked issues."),
        ("\U0001f4d1", "PDF Export",
         "Generates a multi-section executive report via "
         "**Jinja2 + WeasyPrint** \u2014 shareable, printable, and professionally formatted."),
    ]

    # Row 1
    c1, c2, c3 = st.columns(3, gap="medium")
    for col, (icon, title, desc) in zip([c1, c2, c3], features[:3]):
        with col:
            st.markdown(
                '<div style="' + CARD_STYLE + '">'
                '<div style="font-size:2.2rem;margin-bottom:0.75rem;">' + icon + '</div>'
                '<div style="font-size:1rem;font-weight:700;color:#f1f5f9;margin-bottom:0.4rem;">' + title + '</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            st.markdown(desc)

    # Row 2
    c4, c5, c6 = st.columns(3, gap="medium")
    for col, (icon, title, desc) in zip([c4, c5, c6], features[3:]):
        with col:
            st.markdown(
                '<div style="' + CARD_STYLE + '">'
                '<div style="font-size:2.2rem;margin-bottom:0.75rem;">' + icon + '</div>'
                '<div style="font-size:1rem;font-weight:700;color:#f1f5f9;margin-bottom:0.4rem;">' + title + '</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            st.markdown(desc)

    # ------------------------------------------------------------------ #
    #  How It Works                                                        #
    # ------------------------------------------------------------------ #
    st.markdown("")
    st.markdown("## \U0001f680 How It Works")
    st.caption("Three steps from upload to actionable feedback.")

    STEP_STYLE = (
        "text-align:center;padding:1.5rem 1rem;"
        "background:rgba(22,25,41,0.7);"
        "border:1px solid rgba(255,255,255,0.07);"
        "border-radius:16px;backdrop-filter:blur(16px);"
    )
    NUM_STYLE = (
        "width:44px;height:44px;border-radius:50%;"
        "background:linear-gradient(135deg,#6366f1,#a78bfa);"
        "display:inline-flex;align-items:center;justify-content:center;"
        "font-weight:800;font-size:1.125rem;color:white;"
        "box-shadow:0 4px 15px rgba(99,102,241,0.4);margin-bottom:0.75rem;"
    )

    s1, arrow1, s2, arrow2, s3 = st.columns([1, 0.15, 1, 0.15, 1], gap="small")

    steps = [
        ("1", "Upload Resume", "PDF, DOC, or DOCX \u2014 up to 5 MB"),
        ("2", "AI Analysis",   "LLM parsing + semantic validation + JD matching"),
        ("3", "Get Results",   "Detailed score breakdown + actionable fixes + PDF"),
    ]
    step_cols = [s1, s2, s3]
    arrow_cols = [arrow1, arrow2]

    for i, (num, title, desc) in enumerate(steps):
        with step_cols[i]:
            st.markdown(
                '<div style="' + STEP_STYLE + '">'
                '<div style="' + NUM_STYLE + '">' + num + '</div>'
                '<div style="font-size:1rem;font-weight:600;color:#f1f5f9;margin-bottom:0.3rem;">' + title + '</div>'
                '<div style="font-size:0.85rem;color:#64748b;line-height:1.5;">' + desc + '</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        if i < 2:
            with arrow_cols[i]:
                st.markdown(
                    '<div style="display:flex;align-items:center;justify-content:center;'
                    'height:100%;color:#6366f1;font-size:1.5rem;padding-top:1.5rem;">'
                    '\u2192</div>',
                    unsafe_allow_html=True,
                )

    # ------------------------------------------------------------------ #
    #  Tech Stack                                                          #
    # ------------------------------------------------------------------ #
    st.markdown("")
    st.markdown(
        '<div style="display:flex;gap:0.75rem;align-items:flex-start;'
        'padding:0.9rem 1.1rem;border-radius:10px;margin:0.75rem 0;font-size:0.875rem;'
        'border-left:3px solid #60a5fa;background:rgba(96,165,250,0.12);color:#94a3b8;">'
        '<span>\u2699\ufe0f</span>'
        '<div><strong style="color:#f1f5f9;">Tech Stack:</strong> '
        'FastAPI \u00b7 Groq Llama 3.3 70B \u00b7 SentenceTransformers \u00b7 '
        'RapidFuzz \u00b7 spaCy \u00b7 Supabase Auth + PostgreSQL \u00b7 WeasyPrint \u00b7 Docker</div>'
        '</div>',
        unsafe_allow_html=True,
    )
