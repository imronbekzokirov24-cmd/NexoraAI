"""
============================================================
EduMindAI Enterprise
App
Groq + Auth0 + Chat History + Clipboard Image
============================================================
"""

import base64
import streamlit as st

from ai_engine import ai


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="EduMindAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# AUTH0 LOGIN
# ==========================================================

if not st.user.is_logged_in:

    st.markdown("""
    <style>

    .stApp {
        background: #ffffff !important;
    }

    .login-box {
        max-width: 480px;
        margin: 120px auto 0 auto;
        text-align: center;
        padding: 45px 35px;
        border: 1px solid #e4eaf2;
        border-radius: 22px;
        background: #ffffff;
        box-shadow: 0 10px 35px rgba(30, 60, 100, 0.07);
    }

    .login-icon {
        width: 70px;
        height: 70px;
        border-radius: 20px;
        background: #eef5ff;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
        font-size: 34px;
    }

    .login-title {
        font-size: 32px;
        font-weight: 750;
        color: #17233c;
        margin-top: 18px;
    }

    .login-subtitle {
        color: #8996a9;
        font-size: 15px;
        margin-bottom: 25px;
    }

    </style>

    <div class="login-box">

        <div class="login-icon">
            🧠
        </div>

        <div class="login-title">
            EduMindAI
        </div>

        <div class="login-subtitle">
            Your AI Study Assistant
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align:center;'>"
        "<p style='color:#64748b;'>Akkauntingiz bilan kiring</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        if st.button(
            "🔐  Continue with Google / GitHub / Facebook / Email",
            use_container_width=True,
        ):

            st.login("auth0")

    st.stop()


# ==========================================================
# WHITE UI
# ==========================================================

st.markdown("""
<style>

html, body {
    background: #ffffff !important;
}

.stApp {
    background: #ffffff !important;
    color: #17233c !important;
}

[data-testid="stAppViewContainer"] {
    background: #ffffff !important;
}

[data-testid="stHeader"] {
    background: #ffffff !important;
}


/* ========================================================
   MAIN
   ======================================================== */

.main .block-container {

    max-width: 1250px;

    padding-top: 30px;
    padding-left: 45px;
    padding-right: 45px;
    padding-bottom: 100px;

}


/* ========================================================
   SIDEBAR
   ======================================================== */

[data-testid="stSidebar"] {

    background: #f8fbff !important;

    border-right: 1px solid #e4ebf4;

}

[data-testid="stSidebar"] > div:first-child {

    padding-top: 25px;

}


/* LOGO */

.logo-title {

    font-size: 27px;

    font-weight: 750;

    color: #17233c;

}

.logo-subtitle {

    font-size: 13px;

    color: #8997aa;

    margin-top: 3px;

    margin-bottom: 28px;

}


/* SECTION */

.sidebar-title {

    color: #718096;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.5px;

    margin-top: 10px;

    margin-bottom: 12px;

}


/* CHAT HISTORY */

.history-empty {

    color: #9aa7b8;

    font-size: 14px;

    padding: 8px 3px 15px 3px;

}


/* SIDEBAR BUTTON */

[data-testid="stSidebar"] .stButton > button {

    width: 100%;

    text-align: left;

    background: transparent !important;

    color: #334155 !important;

    border: 1px solid transparent !important;

    border-radius: 10px !important;

    padding: 10px 12px !important;

    margin-bottom: 3px;

}

[data-testid="stSidebar"] .stButton > button:hover {

    background: #eef5ff !important;

    border-color: #dbe8fa !important;

    color: #2563eb !important;

}


/* SELECTBOX */

[data-testid="stSidebar"] [data-baseweb="select"] {

    background: #ffffff !important;

}


/* ========================================================
   BRAND
   ======================================================== */

.brand {

    display: flex;

    align-items: center;

    gap: 12px;

    margin-bottom: 25px;

}

.brand-icon {

    width: 45px;

    height: 45px;

    border-radius: 14px;

    background: #eef5ff;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 23px;

}

.brand-name {

    font-size: 25px;

    font-weight: 750;

    color: #17233c;

}

.brand-subtitle {

    color: #8997aa;

    font-size: 13px;

}


/* ========================================================
   CHAT
   ======================================================== */

[data-testid="stChatMessage"] {

    background: #ffffff !important;

    border: 1px solid #e2e9f3 !important;

    border-radius: 16px !important;

    padding: 17px 20px !important;

    margin-bottom: 14px !important;

    box-shadow:
        0 3px 12px rgba(30, 60, 100, 0.04);

}


/* USER */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {

    background: #f7faff !important;

}


/* ========================================================
   CHAT INPUT
   ======================================================== */

[data-testid="stChatInput"] {

    background: #ffffff !important;

}

[data-testid="stChatInput"] > div {

    background: #ffffff !important;

    border: 1px solid #dce5f0 !important;

    border-radius: 16px !important;

    box-shadow:
        0 4px 16px rgba(30, 60, 100, 0.06) !important;

}

[data-testid="stChatInput"] textarea {

    background: #ffffff !important;

    color: #17233c !important;

}

[data-testid="stChatInput"] textarea::placeholder {

    color: #94a3b8 !important;

}


/* ========================================================
   UPLOAD
   ======================================================== */

[data-testid="stFileUploader"] {

    background: #ffffff !important;

    border: 1px solid #dfe7f2 !important;

    border-radius: 15px !important;

}


/* ========================================================
   STATISTICS
   ======================================================== */

.stat-card {

    background: #ffffff;

    border: 1px solid #e2e9f3;

    border-radius: 14px;

    padding: 14px;

    margin-bottom: 9px;

}

.stat-title {

    color: #7c8aa0;

    font-size: 13px;

}

.stat-number {

    color: #17233c;

    font-size: 25px;

    font-weight: 750;

}


/* ========================================================
   WELCOME
   ======================================================== */

.welcome {

    text-align: center;

    padding-top: 100px;

    padding-bottom: 60px;

}

.welcome-icon {

    width: 70px;

    height: 70px;

    border-radius: 20px;

    background: #eef5ff;

    color: #2563eb;

    display: flex;

    align-items: center;

    justify-content: center;

    margin: auto;

    font-size: 25px;

    font-weight: 800;

}

.welcome-title {

    color: #17233c;

    font-size: 35px;

    font-weight: 750;

    margin-top: 18px;

}

.welcome-text {

    color: #8997aa;

    font-size: 15px;

}


/* ========================================================
   SCROLLBAR
   ======================================================== */

::-webkit-scrollbar {

    width: 7px;

}

::-webkit-scrollbar-track {

    background: #ffffff;

}

::-webkit-scrollbar-thumb {

    background: #d9e2ee;

    border-radius: 10px;

}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_titles" not in st.session_state:
    st.session_state.chat_titles = []

if "total_prompts" not in st.session_state:
    st.session_state.total_prompts = 0

if "active_image" not in st.session_state:
    st.session_state.active_image = None

if "pasted_image" not in st.session_state:
    st.session_state.pasted_image = None


# ==========================================================
# CLIPBOARD PASTE LISTENER
# ==========================================================

st.markdown("""
<script>

document.addEventListener(
    "paste",
    async function(event) {

        const items =
            event.clipboardData.items;

        for (let i = 0; i < items.length; i++) {

            const item = items[i];

            if (item.type.startsWith("image/")) {

                const file = item.getAsFile();

                if (!file) {
                    continue;
                }

                const reader =
                    new FileReader();

                reader.onload = function(e) {

                    const imageData =
                        e.target.result;

                    const text =
                        document.querySelector(
                            'textarea'
                        );

                    if (text) {

                        text.value =
                            text.value;

                        text.dispatchEvent(
                            new Event(
                                'input',
                                {
                                    bubbles: true
                                }
                            )
                        );
                    }

                    window.parent.postMessage(
                        {
                            type:
                                "edumindai_pasted_image",

                            image:
                                imageData
                        },
                        "*"
                    );

                };

                reader.readAsDataURL(file);

            }

        }

    }
);

</script>
""", unsafe_allow_html=True)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    # ------------------------------------------------------
    # LOGO
    # ------------------------------------------------------

    st.markdown("""
    <div class="logo-title">
        🧠 EduMindAI
    </div>

    <div class="logo-subtitle">
        Your AI Study Assistant
    </div>
    """, unsafe_allow_html=True)


    # ------------------------------------------------------
    # CHAT HISTORY
    # ------------------------------------------------------

    st.markdown(
        '<div class="sidebar-title">CHATLAR</div>',
        unsafe_allow_html=True,
    )


    if not st.session_state.chat_titles:

        st.markdown(
            '<div class="history-empty">'
            'Hozircha chatlar yo‘q'
            '</div>',
            unsafe_allow_html=True,
        )

    else:

        for i, title in enumerate(
            reversed(
                st.session_state.chat_titles
            )
        ):

            real_index = (
                len(
                    st.session_state.chat_titles
                )
                - 1
                - i
            )

            if st.button(
                "💬 " + title,
                key=f"history_{real_index}",
                use_container_width=True,
            ):

                st.session_state.selected_chat = (
                    real_index
                )


    st.markdown("---")


    # ------------------------------------------------------
    # MODEL
    # ------------------------------------------------------

    st.markdown(
        '<div class="sidebar-title">'
        'GROQ MODEL'
        '</div>',
        unsafe_allow_html=True,
    )


    selected_model = st.selectbox(
        "Model",
        [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
        ],
        label_visibility="collapsed",
    )


    ai.set_model(
        selected_model
    )


    st.markdown("---")


    # ------------------------------------------------------
    # SETTINGS
    # ------------------------------------------------------

    st.markdown(
        '<div class="sidebar-title">'
        'SETTINGS'
        '</div>',
        unsafe_allow_html=True,
    )


    deep_thinking = st.toggle(
        "🔬 Deep Thinking",
        value=False,
    )


    memory_enabled = st.toggle(
        "🧠 Chat Memory",
        value=True,
    )


    st.markdown("---")


    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    user_name = "User"

    try:

        if st.user.name:
            user_name = st.user.name

        elif st.user.email:
            user_name = st.user.email

    except Exception:
        pass


    st.markdown(
        f"""
        <div class="sidebar-title">
            ACCOUNT
        </div>

        <div style="
            background:#ffffff;
            border:1px solid #e2e9f3;
            border-radius:14px;
            padding:13px;
            margin-bottom:10px;
        ">

            <div style="
                font-weight:700;
                color:#17233c;
            ">
                👤 {user_name}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    if st.button(
        "🚪 Log out",
        use_container_width=True,
    ):

        st.logout()


    st.markdown("---")


    # ------------------------------------------------------
    # STATISTICS
    # ------------------------------------------------------

    st.markdown(
        '<div class="sidebar-title">'
        'STATISTICS'
        '</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        f"""
        <div class="stat-card">

            <div class="stat-title">
                💬 Savollar
            </div>

            <div class="stat-number">
                {st.session_state.total_prompts}
            </div>

        </div>

        <div class="stat-card">

            <div class="stat-title">
                💬 Chatlar
            </div>

            <div class="stat-number">
                {len(st.session_state.chat_titles)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown("---")


    # ------------------------------------------------------
    # NEW CHAT
    # ------------------------------------------------------

    if st.button(
        "➕ Yangi chat",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.session_state.active_image = None

        st.session_state.pasted_image = None

        st.rerun()


    # ------------------------------------------------------
    # CLEAR
    # ------------------------------------------------------

    if st.button(
        "🗑️ Chatni tozalash",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.session_state.chat_titles = []

        st.session_state.active_image = None

        st.session_state.pasted_image = None

        st.session_state.total_prompts = 0

        st.rerun()


# ==========================================================
# TOP BAR
# ==========================================================

st.markdown("""
<div class="brand">

    <div class="brand-icon">
        🧠
    </div>

    <div>

        <div class="brand-name">
            EduMindAI
        </div>

        <div class="brand-subtitle">
            Your AI Study Assistant
        </div>

    </div>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# WELCOME
# ==========================================================

if not st.session_state.messages:

    st.markdown("""
    <div class="welcome">

        <div class="welcome-icon">
            AI
        </div>

        <div class="welcome-title">
            EduMindAI
        </div>

        <div class="welcome-text">
            Savolingizni yozing yoki
            rasm/fayl yuboring.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# FILE / IMAGE UPLOAD
# ==========================================================

uploaded_file = st.file_uploader(
    "📎 Rasm yoki fayl",
    type=[
        "png",
        "jpg",
        "jpeg",
        "webp",
        "pdf",
        "txt",
        "csv",
        "json",
    ],
    label_visibility="collapsed",
    key="main_file_uploader",
)


# ==========================================================
# PROCESS UPLOADED FILE
# ==========================================================

if uploaded_file is not None:

    file_type = uploaded_file.type or ""


    # ------------------------------------------------------
    # IMAGE
    # ------------------------------------------------------

    if file_type.startswith("image/"):

        st.session_state.active_image = (
            uploaded_file
        )

        st.image(
            uploaded_file,
            width=350,
            caption="Yuklangan rasm",
        )


    # ------------------------------------------------------
    # OTHER FILE
    # ------------------------------------------------------

    else:

        st.info(
            f"📎 Fayl tayyor: {uploaded_file.name}"
        )


# ==========================================================
# CHAT DISPLAY
# ==========================================================

for message in st.session_state.messages:

    role = message.get(
        "role",
        "assistant",
    )

    content = message.get(
        "content",
        "",
    )

    image_data = message.get(
        "image",
        None,
    )

    with st.chat_message(role):

        if image_data:

            try:

                st.image(
                    image_data,
                    width=350,
                )

            except Exception:
                pass

        st.markdown(content)


# ==========================================================
# CHAT INPUT
# ==========================================================

prompt = st.chat_input(
    "Xabaringizni yozing yoki Ctrl+V bilan rasm qo‘ying..."
)


# ==========================================================
# SEND MESSAGE
# ==========================================================

if prompt:

    st.session_state.total_prompts += 1


    # ------------------------------------------------------
    # TITLE
    # ------------------------------------------------------

    title = prompt.strip()

    if len(title) > 30:

        title = (
            title[:30]
            + "..."
        )


    if not st.session_state.messages:

        st.session_state.chat_titles.append(
            title
        )


    # ------------------------------------------------------
    # IMAGE
    # ------------------------------------------------------

    current_image = (
        st.session_state.active_image
    )


    # ------------------------------------------------------
    # USER
    # ------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
            "image": current_image,
        }
    )


    with st.chat_message("user"):

        if current_image:

            st.image(
                current_image,
                width=350,
            )

        st.markdown(prompt)


    # ------------------------------------------------------
    # AI
    # ------------------------------------------------------

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        response = ""


        # ==================================================
        # VISION
        # ==================================================

        if current_image:

            with st.spinner(
                "🖼️ Rasm tahlil qilinmoqda..."
            ):

                response = ai.vision_chat(
                    image=current_image,
                    user_prompt=prompt,
                )

            response_placeholder.markdown(
                response
            )


            st.session_state.active_image = None


        # ==================================================
        # NORMAL CHAT
        # ==================================================

        else:

            history = (
                st.session_state.messages
                if memory_enabled
                else None
            )


            for chunk in ai.stream_chat(
                user_prompt=prompt,
                history=history,
                context="",
                web_search="",
                deep_thinking=deep_thinking,
            ):

                response += str(chunk)

                response_placeholder.markdown(
                    response + "▌"
                )


            response_placeholder.markdown(
                response
            )


    # ------------------------------------------------------
    # SAVE
    # ------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "image": None,
        }
    )
