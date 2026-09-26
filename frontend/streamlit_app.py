import streamlit as st
import sys
from pathlib import Path

# Put the repo root on sys.path so `from frontend.views import ...` resolves
# regardless of the directory streamlit was launched from.
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure page
st.set_page_config(
    page_title="ResuPulse \u2014 AI ATS Scorer",
    page_icon="\u26a1",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auth state. Populated by Supabase sign-in / sign-up / OAuth.
# All four are None when signed out, all four are set when signed in.
for key, default in [
    ("access_token", None),
    ("refresh_token", None),
    ("user_id", None),       # Supabase auth user id (uuid); also used by api_client
    ("user_email", None),
    ("auth_error", None),
    ("auth_info", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# If we just came back from Google OAuth, Supabase appends `?code=<authcode>`
# to the redirect URL. Exchange it for a session before rendering anything.
if (
    not st.session_state.access_token
    and "code" in st.query_params
):
    from frontend.services import supabase_client
    result = supabase_client.exchange_code_for_session(st.query_params["code"])

    # Always clear the ?code= param so a refresh doesn't try to re-exchange.
    st.query_params.clear()
    if "error" in result:
        st.session_state.auth_error = f"Google sign-in failed: {result['error']}"
    else:
        st.session_state.access_token  = result["access_token"]
        st.session_state.refresh_token = result["refresh_token"]
        st.session_state.user_id       = result["user_id"]
        st.session_state.user_email    = result["email"]
        st.rerun()

# Load custom CSS
def load_css():
    try:
        css_path = Path(__file__).parent / 'assets' / 'styles.css'
        with open(css_path, 'r', encoding='utf-8') as f:
            return '<style>' + f.read() + '</style>'
    except FileNotFoundError:
        return ''

st.markdown(load_css(), unsafe_allow_html=True)

# Initialize session state for view management
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'landing'

# ------------------------------------------------------------------ #
#  Sidebar                                                             #
# ------------------------------------------------------------------ #
with st.sidebar:
    # Brand logo / wordmark
    st.markdown("""
    <div style="padding: 0.5rem 0 1.25rem; border-bottom: 1px solid rgba(255,255,255,0.07); margin-bottom: 1rem;">
        <div style="font-size: 1.5rem; font-weight: 900; letter-spacing: -0.03em;
                    background: linear-gradient(135deg, #f1f5f9, #a78bfa);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    background-clip: text;">
            \u26a1 ResuPulse
        </div>
        <div style="font-size: 0.7rem; color: #64748b; letter-spacing: 0.06em;
                    text-transform: uppercase; font-weight: 600; margin-top: 0.15rem;">
            AI-Powered ATS Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Navigation")

    nav_items = [
        ("\U0001f3e0  Home",       'landing'),
        ("\u26a1  ATS Scorer",     'scorer'),
        ("\U0001f4ca  History",    'history'),
        ("\U0001f4da  Resources",  'resources'),
    ]
    for label, view in nav_items:
        is_active = st.session_state.current_view == view
        if is_active:
            # Highlight active item with indigo pill
            st.markdown(
                "<div style='background:rgba(99,102,241,0.15);"
                " border:1px solid rgba(99,102,241,0.3);"
                " border-radius:10px; padding:0.55rem 0.9rem; color:#a78bfa;"
                " font-size:0.9375rem; font-weight:600; margin-bottom:4px;'>"
                + label + "</div>",
                unsafe_allow_html=True,
            )
        else:
            if st.button(label, use_container_width=True, key="nav_" + view):
                st.session_state.current_view = view
                st.rerun()

    st.markdown("---")
    st.markdown("### \U0001f464 Account")

    from frontend.services import supabase_client

    if st.session_state.access_token:
        # Signed-in: show email pill + sign-out
        user_email = st.session_state.user_email or ""
        st.markdown(
            "<div style='font-size:0.75rem; color:#64748b; margin-bottom:0.25rem;'>Signed in as</div>"
            "<div style='font-size:0.875rem; color:#a78bfa; font-weight:600;"
            " margin-bottom:0.75rem; word-break:break-all;'>"
            + user_email + "</div>",
            unsafe_allow_html=True,
        )
        if st.button("Sign out", use_container_width=True):
            supabase_client.sign_out()
            for k in ("access_token", "refresh_token", "user_id", "user_email"):
                st.session_state[k] = None
            st.rerun()
    else:
        # Signed-out: tabs for sign-in / sign-up + Google OAuth
        if st.session_state.auth_error:
            st.error(st.session_state.auth_error)
            st.session_state.auth_error = None
        if st.session_state.auth_info:
            st.info(st.session_state.auth_info)
            st.session_state.auth_info = None

        tab_in, tab_up = st.tabs(["Sign in", "Sign up"])

        with tab_in:
            with st.form("signin_form", clear_on_submit=False):
                email    = st.text_input("Email", key="signin_email")
                password = st.text_input("Password", type="password", key="signin_pw")
                submitted = st.form_submit_button("Sign in", use_container_width=True)
            if submitted:
                result = supabase_client.sign_in_with_password(email, password)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                else:
                    st.session_state.access_token  = result["access_token"]
                    st.session_state.refresh_token = result["refresh_token"]
                    st.session_state.user_id       = result["user_id"]
                    st.session_state.user_email    = result["email"]
                st.rerun()

        with tab_up:
            with st.form("signup_form", clear_on_submit=False):
                email_up    = st.text_input("Email", key="signup_email")
                password_up = st.text_input("Password (min 6 chars)", type="password", key="signup_pw")
                submitted_up = st.form_submit_button("Create account", use_container_width=True)
            if submitted_up:
                result = supabase_client.sign_up_with_password(email_up, password_up)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                elif result.get("pending_confirmation"):
                    st.session_state.auth_info = (
                        "Check your inbox \u2014 confirmation email sent to " + result["email"] + "."
                    )
                else:
                    st.session_state.access_token  = result["access_token"]
                    st.session_state.refresh_token = result["refresh_token"]
                    st.session_state.user_id       = result["user_id"]
                    st.session_state.user_email    = result["email"]
                st.rerun()

        st.markdown(
            "<div style='text-align:center; margin:0.6rem 0; font-size:0.75rem; color:#64748b;'>or</div>",
            unsafe_allow_html=True,
        )

        oauth = supabase_client.google_oauth_url()
        if "error" in oauth:
            st.caption("Google sign-in unavailable: " + oauth["error"])
        else:
            st.link_button(
                "\U0001f511  Continue with Google",
                url=oauth["url"],
                use_container_width=True,
            )

# ------------------------------------------------------------------ #
#  Main content — render based on current view                         #
# ------------------------------------------------------------------ #
if st.session_state.current_view == 'landing':
    from frontend.views import landing
    landing.render()

elif st.session_state.current_view == 'scorer':
    from frontend.views import scorer
    scorer.render()

elif st.session_state.current_view == 'history':
    from frontend.views import history
    history.render()

elif st.session_state.current_view == 'resources':
    from frontend.views import resources
    resources.render()
