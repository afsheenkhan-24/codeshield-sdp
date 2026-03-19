import streamlit as st


def Settings():
    st.header("Settings")
    st.caption("Manage your account and preferences")

    st.markdown("---")

    # ---- User Profile ----
    st.subheader("User profile")

    # Load saved values from session state (persists during the session)
    if "profile" not in st.session_state:
        st.session_state.profile = {
            "full_name": "",
            "email": "",
            "role": "Platform Engineer",
        }

    with st.form("profile_form"):
        full_name = st.text_input(
            "Full name",
            value=st.session_state.profile["full_name"],
            placeholder="e.g. Jane Smith",
        )
        email = st.text_input(
            "Email address",
            value=st.session_state.profile["email"],
            placeholder="e.g. jane@example.com",
        )
        role = st.selectbox(
            "Role",
            options=[
                "Platform Engineer",
                "Security Analyst",
                "Analyst Designer",
                "Project Manager",
                "Tester",
            ],
            index=[
                "Platform Engineer",
                "Security Analyst",
                "Analyst Designer",
                "Project Manager",
                "Tester",
            ].index(st.session_state.profile["role"]),
        )

        saved = st.form_submit_button("Save profile")
        if saved:
            st.session_state.profile["full_name"] = full_name
            st.session_state.profile["email"] = email
            st.session_state.profile["role"] = role
            st.success("Profile saved.")

    '''st.markdown("---")

    # ---- Appearance -----
    st.subheader("Appearance")

    if "theme" not in st.session_state:
        st.session_state.theme = "Light"

    chosen = st.radio(
        "Theme",
        options=["Light", "Dark"],
        index=0 if st.session_state.theme == "Light" else 1,
        horizontal=True,
    )

    if chosen != st.session_state.theme:
        st.session_state.theme = chosen

        # Write the chosen theme to .streamlit/config.toml at runtime
        theme_config = (
            '[theme]\nbase="light"\n'
            if chosen == "Light"
            else '[theme]\nbase="dark"\n'
        )
        try:
            import os
            os.makedirs(".streamlit", exist_ok=True)
            with open(".streamlit/config.toml", "w") as f:
                f.write(theme_config)
            st.success(f"{chosen} mode applied. Reloading...")
            st.rerun()
        except Exception as e:
            st.warning(f"Could not write theme config: {e}")'''