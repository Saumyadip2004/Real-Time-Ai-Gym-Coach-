import streamlit as st
from services.persistence.exercise_repository import get_or_create_user


def render_login_wall():
    # 1. If already logged in, skip login UI and return True
    if "username" in st.session_state and st.session_state["username"]:
        return True

    # 2. Render Login Form
    st.title("🏋️ AI Real-time GYM Trainer")
    st.markdown("### Welcome! Please enter a username to start.")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Name (unique)", placeholder="unique name e.g. princekhunt")
        # CHANGED: use_container_width=True replaces width="stretch"
        submit_button = st.form_submit_button("Start Session", use_container_width=True)

    # 3. Handle Form Submission
    if submit_button:
        if not username.strip():
            st.error("Name cannot be empty.")
            return False

        user=get_or_create_user(username)

        st.session_state["username"] = user["username"]
        st.session_state["user_id"] = user["id"]
        st.rerun()

    return False