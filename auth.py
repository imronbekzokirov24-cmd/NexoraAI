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
        self.init_session()

    # ======================================================
    # SESSION
    # ======================================================

    def init_session(self):

        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        if "user_id" not in st.session_state:
            st.session_state.user_id = None

        if "username" not in st.session_state:
            st.session_state.username = ""

        if "email" not in st.session_state:
            st.session_state.email = ""

        if "plan" not in st.session_state:
            st.session_state.plan = "Free"

    # ======================================================
    # PASSWORD HASH
    # ======================================================

    def hash_password(self, password):

        return hashlib.sha256(
            str(password).encode("utf-8")
        ).hexdigest()

    # ======================================================
    # REGISTER
    # ======================================================

    def register(
        self,
        username,
        email,
        password
    ):

        username = str(username).strip()
        email = str(email).strip()
        password = str(password)

        if not username:
            return False, "Username kiriting."

        if not email:
            return False, "Email kiriting."

        if not password:
            return False, "Password kiriting."

        if len(username) < 3:
            return False, "Username kamida 3 ta belgidan iborat bo‘lsin."

        if len(password) < 6:
            return False, "Password kamida 6 ta belgidan iborat bo‘lsin."

        password_hash = self.hash_password(password)

        try:

            created = db.create_user(
                username=username,
                password=password_hash,
                email=email
            )

            if created:

                return (
                    True,
                    "Account muvaffaqiyatli yaratildi."
                )

            return (
                False,
                "Bu username allaqachon mavjud."
            )

        except Exception as e:

            return (
                False,
                f"Register xatosi: {e}"
            )

    # ======================================================
    # LOGIN
    # ======================================================

    def login(
        self,
        username,
        password
    ):

        username = str(username).strip()
        password = str(password)

        if not username:
            return False, "Username kiriting."

        if not password:
            return False, "Password kiriting."

        password_hash = self.hash_password(password)

        try:

            user = db.authenticate_user(
                username=username,
                password=password_hash
            )

            if not user:

                return (
                    False,
                    "Username yoki password noto‘g‘ri."
                )

            # ==============================================
            # SESSION
            # ==============================================

            st.session_state.logged_in = True

            st.session_state.user_id = user["id"]

            st.session_state.username = user["username"]

            st.session_state.email = user.get(
                "email",
                ""
            )

            st.session_state.plan = user.get(
                "plan",
                "Free"
            )

            return True, "Login muvaffaqiyatli."

        except Exception as e:

            return (
                False,
                f"Login xatosi: {e}"
            )

    # ======================================================
    # LOGOUT
    # ======================================================

    def logout(self):

        st.session_state.logged_in = False

        st.session_state.user_id = None

        st.session_state.username = ""

        st.session_state.email = ""

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
    # CURRENT USER
    # ======================================================

    def current_user(self):

        user_id = st.session_state.get(
            "user_id"
        )

        if not user_id:
            return None

        return db.get_user(user_id)

    # ======================================================
    # AUTH PAGE
    # ======================================================

    def show_auth_page(self):

        st.markdown(
            """
            <div style="
                text-align:center;
                padding:35px 10px 20px 10px;
            ">

                <h1>🧠 EduMindAI</h1>

                <p>
                    AI Learning Assistant
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        login_tab, register_tab = st.tabs(
            [
                "🔐 Login",
                "📝 Register"
            ]
        )

        # ==================================================
        # LOGIN
        # ==================================================

        with login_tab:

            st.subheader("Welcome back!")

            login_username = st.text_input(
                "Username",
                key="auth_login_username"
            )

            login_password = st.text_input(
                "Password",
                type="password",
                key="auth_login_password"
            )

            login_button = st.button(
                "🔐 Login",
                use_container_width=True,
                key="auth_login_button"
            )

            if login_button:

                success, message = self.login(
                    login_username,
                    login_password
                )

                if success:

                    st.success(message)

                    st.rerun()

                else:

                    st.error(message)

        # ==================================================
        # REGISTER
        # ==================================================

        with register_tab:

            st.subheader("Create your account")

            register_username = st.text_input(
                "Username",
                key="auth_register_username"
            )

            register_email = st.text_input(
                "Email",
                key="auth_register_email"
            )

            register_password = st.text_input(
                "Password",
                type="password",
                key="auth_register_password"
            )

            register_confirm = st.text_input(
                "Confirm Password",
                type="password",
                key="auth_register_confirm"
            )

            register_button = st.button(
                "📝 Create Account",
                use_container_width=True,
                key="auth_register_button"
            )

            if register_button:

                if register_password != register_confirm:

                    st.error(
                        "Passwordlar bir xil emas."
                    )

                else:

                    success, message = self.register(
                        register_username,
                        register_email,
                        register_password
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
