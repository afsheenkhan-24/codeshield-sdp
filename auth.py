import streamlit as st
from utils.supabase_client import get_supabase_client


def run_auth() -> bool:

    # Already authenticated this session
    if st.session_state.get("user"):
        return True

    supabase = get_supabase_client()

    
    col1, col2 = st.columns([0.13, 0.87])
    with col1:
        st.image('logo.jpeg', width=200)
    with col2:
        st.title("CodeShield Tech Solutions")
        st.caption("Technical Debt and Security Scanner")
    # st.markdown("---")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    # ---- Login ----
    with tab_login:
        st.subheader("Sign in to your account")

        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Sign in", key="btn_login"):
            if not login_email or not login_password:
                st.warning("Please enter your email and password.")
            else:
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": login_email,
                        "password": login_password,
                    })
                    user = response.user
                    if user:
                        st.session_state["user"] = user
                        # Pre-populate profile with name from Supabase metadata
                        full_name = user.user_metadata.get("full_name", "")
                        email = user.user_metadata.get("email", "")
                        if "profile" not in st.session_state:
                            st.session_state["profile"] = {}
                        st.session_state["profile"]["full_name"] = full_name
                        st.session_state["profile"]["email"] = email
                        st.session_state["profile"]["role"] = "Platform Engineer"
                        st.rerun()
                    else:
                        st.error("Sign in failed. Please check your credentials.")
                except Exception as e:
                    st.error(f"Sign in error: {e}")

    # ---- Register ----
    with tab_register:
        st.subheader("Create an account")

        reg_name = st.text_input("Full name", key="reg_name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input(
            "Password",
            type="password",
            key="reg_password",
            help="Minimum 6 characters.",
        )
        reg_password_confirm = st.text_input(
            "Confirm password",
            type="password",
            key="reg_password_confirm",
        )

        if st.button("Create account", key="btn_register"):
            if not reg_name or not reg_email or not reg_password:
                st.warning("Please fill in all fields.")
            elif reg_password != reg_password_confirm:
                st.error("Passwords do not match.")
            elif len(reg_password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                try:
                    response = supabase.auth.sign_up({
                        "email": reg_email,
                        "password": reg_password,
                        "options": {
                            "data": {"full_name": reg_name}
                        },
                    })
                    user = response.user
                    if user:
                        st.success(
                            f"Account created for **{reg_name}**! "
                            "Please check your email to confirm your account, then sign in."
                        )
                    else:
                        st.error("Registration failed. Please try again.")
                except Exception as e:
                    st.error(f"Registration error: {e}")

    return False


def sign_out():
    """Sign the current user out and clear session state."""
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state.pop("user", None)
    st.session_state.pop("profile", None)
    st.rerun()