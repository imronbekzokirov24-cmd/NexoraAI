"""
============================================================
EduMindAI Enterprise
Authentication System
============================================================
"""

import hashlib
import streamlit as st
from database import db


class Auth:

    def __init__(self):
        self._init_session()

    # ======================================================
    # SESSION
    # ======================================================

    def _init_session(self):

        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        if "user_id" not in st.session_state:
            st.session_state.user_id = None

        if "username" not in st.session_state:
            st.session_state.username = "Guest"

        if "plan" not in st.session_state:
            st.session_state.plan = "Free"

    # ======================================================
    # PASSWORD HASH
    # ======================================================

    def hash_password(self, password):

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    # ======================================================
    # REGISTER
    # ======================================================

    def register(self, username, password):

        username = username.strip()

        if not username:
            return False, "Username kiriting."

        if not password:
            return False, "Password kiriting."

        if len(username) < 3:
            return False, "Username kamida 3 ta belgidan iborat bo‘lsin."

        if len(password) < 6:
            return False, "Password kamida 6 ta belgidan iborat bo‘lsin."

        try:

            password_hash = self.hash_password(password)

            result = db.create_user(
                username,
                password_hash
            )

            if result:

                return True, "Account muvaffaqiyatli yaratildi."

            return False, "Bu username allaqachon mavjud."

        except Exception as e:

            return False, f"Register xatosi: {e}"

    # ======================================================
    # LOGIN
    # ======================================================

    def login(self, username, password):

        username = username.strip()

        if not username or not password:

            return False, "Username va password kiriting."

        try:

            password_hash = self.hash_password(password)

            user = db.authenticate_user(
                username,
                password_hash
            )

            if not user:

                return False, "Username yoki password noto‘g‘ri."

            st.session_state.logged_in = True

            st.session_state.user_id = user["id"]

            st.session_state.username = user["username"]

            st.session_state.plan = user.get(
                "plan",
                "Free"
            )

            return True, "Login muvaffaqiyatli."

        except Exception as e:

            return False, f"Login xatosi: {e}"

    # ======================================================
    # LOGOUT
    # ======================================================

    def logout(self):

        st.session_state.logged_in = False

        st.session_state.user_id = None

        st.session_state.username = "Guest"

        st.session_state.plan = "Free"

        st.session_state.messages = []

        st.rerun()

    # ======================================================
    # CHECK LOGIN
    # ======================================================

    def is_logged_in(self):

        return st.session_state.get(
            "logged_in",
            False
        )

    # ======================================================
    # LOGIN PAGE
    # ======================================================

    def show_auth_page(self):

        st.markdown(
            """
            <div style="
                max-width:600px;
                margin:auto;
                text-align:center;
                padding-top:40px;
            ">

            <h1>🧠 EduMindAI</h1>

            <p>
            AI Learning Assistant
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        tab1, tab2 = st.tabs(
            [
                "🔐 Login",
                "📝 Register"
            ]
        )

        # ==================================================
        # LOGIN
        # ==================================================

        with tab1:

            st.subheader("Welcome back!")

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button(
                "🔐 Login",
                use_container_width=True
            ):

                success, message = self.login(
                    username,
                    password
                )

                if success:

                    st.success(message)

                    st.rerun()

                else:

                    st.error(message)

        # ==================================================
        # REGISTER
        # ==================================================

        with tab2:

            st.subheader("Create your account")

            username = st.text_input(
                "Username",
                key="register_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="register_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="register_confirm_password"
            )

            if st.button(
                "📝 Create Account",
                use_container_width=True
            ):

                if password != confirm_password:

                    st.error(
                        "Passwordlar bir xil emas."
                    )

                else:

                    success, message = self.register(
                        username,
                        password
                    )

                    if success:

                        st.success(message)

                        st.info(
                            "Endi Login bo‘limidan kiring."
                        )

                    else:

                        st.error(message)


# ==========================================================
# GLOBAL AUTH INSTANCE
# ==========================================================

auth = Auth()
