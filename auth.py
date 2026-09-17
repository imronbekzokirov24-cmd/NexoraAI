"""
============================================================
EduMindAI Enterprise
Google Authentication
============================================================
"""

import secrets
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

        if "user_email" not in st.session_state:
            st.session_state.user_email = ""

        if "user_picture" not in st.session_state:
            st.session_state.user_picture = ""

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
    # GOOGLE LOGIN
    # ======================================================

    def google_login(self):

        try:

            st.login("google")

        except Exception as e:

            st.error(
                f"Google Login xatosi: {e}"
            )

    # ======================================================
    # GOOGLE USERNI DATABASEGA ULASH
    # ======================================================

    def sync_google_user(self):

        try:

            if not st.user.is_logged_in:
                return False

        except Exception:

            return False

        # ----------------------------------------------
        # GOOGLE DATA
        # ----------------------------------------------

        email = getattr(
            st.user,
            "email",
            ""
        )

        name = getattr(
            st.user,
            "name",
            ""
        )

        picture = getattr(
            st.user,
            "picture",
            ""
        )

        sub = getattr(
            st.user,
            "sub",
            ""
        )

        if not email:

            return False

        # ----------------------------------------------
        # USERNAME
        # ----------------------------------------------

        if name:

            username = str(name).strip()

        else:

            username = email.split("@")[0]

        # Database username unique bo‘lishi kerak.

        username = username.replace(
            " ",
            "_"
        )

        if not username:

            username = "google_user"


        # ----------------------------------------------
        # MAVJUD USER
        # ----------------------------------------------

        existing_user = (
            db.get_user_by_username(
                username
            )
        )

        # ----------------------------------------------
        # YANGI USER
        # ----------------------------------------------

        if not existing_user:

            # Google user uchun tasodifiy ichki
            # password yaratamiz.
            #
            # Bu password Google account passwordi emas.

            random_password = (
                secrets.token_urlsafe(32)
            )

            created = db.create_user(
                username=username,
                password=self.hash_password(
                    random_password
                ),
                email=email,
            )

            if created:

                existing_user = (
                    db.get_user_by_username(
                        username
                    )
                )

        # ----------------------------------------------
        # USER TOPILMAGAN BO‘LSA
        # ----------------------------------------------

        if not existing_user:

            # Username conflict bo‘lishi mumkin.
            # Email asosida yana bir username qilamiz.

            safe_username = (
                "google_"
                + email.split("@")[0]
            )

            safe_username = safe_username.replace(
                " ",
                "_"
            )

            existing_user = (
                db.get_user_by_username(
                    safe_username
                )
            )

            if not existing_user:

                random_password = (
                    secrets.token_urlsafe(32)
                )

                db.create_user(
                    username=safe_username,
                    password=self.hash_password(
                        random_password
                    ),
                    email=email,
                )

                existing_user = (
                    db.get_user_by_username(
                        safe_username
                    )
                )

            username = safe_username

        # ----------------------------------------------
        # SESSION
        # ----------------------------------------------

        st.session_state.logged_in = True

        st.session_state.user_id = (
            existing_user["id"]
        )

        st.session_state.username = (
            existing_user["username"]
        )

        st.session_state.user_email = email

        st.session_state.user_picture = picture

        st.session_state.plan = (
            existing_user.get(
                "plan",
                "Free"
            )
        )

        st.session_state.google_sub = sub

        return True

    # ======================================================
    # CHECK LOGIN
    # ======================================================

    def is_logged_in(self):

        try:

            return bool(
                st.user.is_logged_in
            )

        except Exception:

            return False

    # ======================================================
    # LOGOUT
    # ======================================================

    def logout(self):

        # Local sessionni tozalash

        st.session_state.logged_in = False

        st.session_state.user_id = None

        st.session_state.username = ""

        st.session_state.user_email = ""

        st.session_state.user_picture = ""

        st.session_state.plan = "Free"

        st.session_state.messages = []

        # Google/Streamlit logout

        try:

            st.logout()

        except Exception:

            st.rerun()

    # ======================================================
    # LOGIN PAGE
    # ======================================================

    def show_login_page(self):

        st.markdown(
            """
            <div style="
                text-align:center;
                padding-top:80px;
                padding-bottom:30px;
            ">

                <h1>🧠 EduMindAI</h1>

                <p style="font-size:20px;">
                    AI Learning Assistant
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🔐 Accountga kirish"
        )

        st.write(
            "EduMindAI'dan foydalanish uchun "
            "Google account orqali kiring."
        )

        st.write("")

        if st.button(
            "🌐 Continue with Google",
            use_container_width=True,
            type="primary",
        ):

            self.google_login()

        st.write("")

        st.caption(
            "Google orqali xavfsiz kirish."
        )


# ==========================================================
# GLOBAL AUTH INSTANCE
# ==========================================================

auth = Auth()
