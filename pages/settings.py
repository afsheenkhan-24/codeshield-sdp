import streamlit as st
from utils.supabase_client import get_supabase_client

ROLES = [
    "Platform Engineer",
    "Security Analyst",
    "Analyst Designer",
    "Project Manager",
    "Tester",
]


def Settings():
    st.header("Settings")
    st.caption("Manage your account and preferences")
    st.markdown("---")
    st.subheader("User profile")

    user = st.session_state.get("user")

    if user:
        metadata = user.user_metadata or {}
        default_name = metadata.get("full_name", "")
        default_email = user.email or ""
        default_role = metadata.get("role", ROLES[0])
    else:
        default_name = ""
        default_email = ""
        default_role = ROLES[0]

    if default_role not in ROLES:
        default_role = ROLES[0]

    with st.form("profile_form"):
        full_name = st.text_input(
            "Full name",
            value=default_name,
            placeholder="e.g. Jane Smith",
        )
        st.text_input(
            "Email address",
            value=default_email,
            disabled=True,
            help="Email cannot be changed here.",
        )
        role = st.selectbox(
            "Role",
            options=ROLES,
            index=ROLES.index(default_role),
        )
        submitted = st.form_submit_button("Save profile")

    if submitted:
        if not full_name.strip():
            st.warning("Full name cannot be empty.")
        else:
            try:
                supabase = get_supabase_client()
                supabase.auth.update_user({
                    "data": {
                        "full_name": full_name.strip(),
                        "role": role,
                    }
                })
                if "profile" not in st.session_state:
                    st.session_state.profile = {}
                st.session_state.profile["full_name"] = full_name.strip()
                st.session_state.profile["role"] = role
                st.session_state.profile["email"] = default_email
                st.success("Profile saved.")
            except Exception as e:
                st.error(f"Failed to save profile: {e}")
