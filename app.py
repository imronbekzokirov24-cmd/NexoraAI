"""
============================================================
EduMindAI
Clean White UI + Chat History
============================================================
"""

import uuid
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
# WHITE UI STYLE
# ==========================================================

st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    background: #ffffff !important;
}

.stApp {
    background: #ffffff !important;
    color: #17233c !important;
}

[data-testid="stHeader"] {
    background: #ffffff !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

.main .block-container {
    max-width: 1250px;
    padding-top: 35px;
    padding-left: 45px;
    padding-right: 45px;
    padding-bottom: 100px;
}


/* ========================================================
   SIDEBAR
   ======================================================== */

[data-testid="stSidebar"] {
    background: #f8fbff !important;
    border-right: 1px solid #e5ebf5;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 25px;
}


/* LOGO */

.logo-box {
    padding: 5px 5px 25px 5px;
}

.logo-title {
    font-size: 27px;
    font-weight: 750;
    color: #17233c;
}

.logo-subtitle {
    font-size: 14px;
    color: #8a98ad;
    margin-top: 2px;
}


/* SIDEBAR SECTION */

.sidebar-title {
    font-size: 11px;
    font-weight: 800;
    color: #6b7a90;
    letter-spacing: 1.5px;
    margin-top: 12px;
    margin-bottom: 12px;
    text-transform: uppercase;
}


/* CHAT HISTORY */

.history-title {
    font-size: 11px;
    font-weight: 800;
    color: #6b7a90;
    letter-spacing: 1.5px;
    margin-top: 5px;
    margin-bottom: 12px;
    text-transform: uppercase;
}

.history-empty {
    color: #9aa7ba;
    font-size: 14px;
    padding: 10px 5px;
}


/* SIDEBAR BUTTONS */

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: #334155 !important;
    border-radius: 11px !important;
    padding: 11px 13px !important;
    margin-bottom: 4px;
    font-size: 14px;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #eef5ff !important;
    border-color: #dce9fb !important;
    color: #2563eb !important;
}


/* MODEL */

[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #ffffff !important;
    border: 1px solid #dce5f0 !important;
    border-radius: 11px !important;
}


/* TOGGLES */

[data-testid="stSidebar"] label {
    color: #334155 !important;
}


/* DIVIDER */

[data-testid="stSidebar"] hr {
    border-color: #e5ebf5 !important;
}


/* ========================================================
   TOP AREA
   ======================================================== */

.top-area {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0 25px 0;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    width: 43px;
    height: 43px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #eef5ff;
    color: #2563eb;
    font-size: 23px;
    font-weight: 700;
}

.brand-name {
    font-size: 24px;
    font-weight: 750;
    color: #17233c;
}

.brand-subtitle {
    color: #8a98ad;
    font-size: 13px;
}


/* ========================================================
   CHAT MESSAGES
   ======================================================== */

[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e2e9f3 !important;
    border-radius: 16px !important;
    padding: 17px 20px !important;
    margin-bottom: 14px !important;
    box-shadow: 0 3px 12px rgba(30, 60, 100, 0.04);
}


/* USER */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: #f7faff !important;
}


/* ASSISTANT */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: #ffffff !important;
}


/* TEXT */

[data-testid="stChatMessage"] p {
    color: #334155 !important;
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
    box-shadow: 0 4px 16px rgba(30, 60, 100, 0.06) !important;
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
    padding: 15px;
    margin-bottom: 10px;
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
   BUTTONS
   ======================================================== */

.stButton > button {
    background: #ffffff !important;
    border: 1px solid #dce5f0 !important;
    color: #334155 !important;
    border-radius: 11px !important;
}

.stButton > button:hover {
    background: #f5f9ff !important;
    border-color: #bcd4f7 !important;
    color: #2563eb !important;
}


/* ========================================================
   WELCOME
   ======================================================== */

.welcome {
    text-align: center;
    padding: 100px 20px 70px 20px;
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
    font-size: 34px;
    font-weight: 800;
}

.welcome h1 {
    color: #17233c !important;
    font-size: 35px;
    margin-top: 18px;
}

.welcome p {
    color: #8795aa;
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


/* ========================================================
   MOBILE
   ======================================================== */

@media (max-width: 768px) {

    .main .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .welcome {
        padding-top: 60px;
    }

}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# SESSION STATE
# ==========================================================

defaults = {
    "messages": [],
    "chat_titles": [],
    "active_image": None,
    "total_prompts": 0,
    "selected_model": "openai/gpt-oss-120b",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    # ------------------------------------------------------
    # LOGO
    # ------------------------------------------------------

    st.markdown("""
    <div class="logo-box">
        <div class="logo-title">🧠 EduMindAI</div>
        <div class="logo-subtitle">
            Your AI Study Assistant
        </div>
    </div>
    """, unsafe_allow_html=True)


    # ------------------------------------------------------
    # CHAT HISTORY
    # ------------------------------------------------------

    st.markdown(
        '<div class="history-title">CHATLAR</div>',
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
            reversed(st.session_state.chat_titles)
        ):

            real_index = (
                len(st.session_state.chat_titles)
                - 1
                - i
            )

            if st.button(
                "💬 " + title,
                key=f"chat_title_{real_index}",
                use_container_width=True,
            ):
                st.session_state.selected_chat = real_index


    st.markdown("---")


    # ------------------------------------------------------
    # GROQ MODEL
    # ------------------------------------------------------

    st.markdown(
        '<div class="sidebar-title">GROQ MODEL</div>',
        unsafe_allow_html=True,
    )

    model = st.selectbox(
        "Model",
        [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.session_state.selected_model = model

    ai.set_model(model)


    st.markdown("---")


    # ------------------------------------------------------
    # SETTINGS
    # ------------------------------------------------------

    st.markdown(
        '<div class="sidebar-title">SETTINGS</div>',
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
    # STATISTICS
    # ------------------------------------------------------

    st.markdown(
        '<div class="sidebar-title">STATISTICS</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-title">💬 Savollar</div>
            <div class="stat-number">
                {st.session_state.total_prompts}
            </div>
        </div>

        <div class="stat-card">
            <div class="stat-title">💬 Chatlar</div>
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

        st.rerun()


    # ------------------------------------------------------
    # CLEAR
    # ------------------------------------------------------

    if st.button(
        "🗑️ Chatni tozalash",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.active_image = None
        st.session_state.chat_titles = []
        st.session_state.total_prompts = 0

        st.rerun()


# ==========================================================
# TOP BAR
# ==========================================================

st.markdown("""
<div class="top-area">

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

        <h1>
            EduMindAI
        </h1>

        <p>
            Groq yordamida savol bering,
            rasm tahlil qiling va AI bilan suhbatlashing.
        </p>

    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# IMAGE UPLOAD
# ==========================================================

uploaded_image = st.file_uploader(
    "🖼️ Rasm yuklash",
    type=[
        "png",
        "jpg",
        "jpeg",
        "webp",
    ],
    label_visibility="collapsed",
    key="image_uploader",
)

if uploaded_image is not None:

    st.session_state.active_image = uploaded_image

    st.image(
        uploaded_image,
        caption="Yuklangan rasm",
        width=350,
    )


# ==========================================================
# DISPLAY CHAT
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

    image = message.get(
        "image",
        None,
    )

    with st.chat_message(role):

        if image is not None:

            try:

                st.image(
                    image,
                    width=350,
                )

            except Exception:
                pass

        st.markdown(content)


# ==========================================================
# CHAT INPUT
# ==========================================================

prompt = st.chat_input(
    "Groq bilan xabar yozing..."
)


# ==========================================================
# PROCESS MESSAGE
# ==========================================================

if prompt:

    st.session_state.total_prompts += 1


    # ------------------------------------------------------
    # CHAT TITLE
    # ------------------------------------------------------

    chat_title = prompt.strip()

    if len(chat_title) > 28:

        chat_title = (
            chat_title[:28]
            + "..."
        )


    if not st.session_state.messages:

        st.session_state.chat_titles.append(
            chat_title
        )


    # ------------------------------------------------------
    # CURRENT IMAGE
    # ------------------------------------------------------

    current_image = (
        st.session_state.active_image
    )


    # ------------------------------------------------------
    # USER MESSAGE
    # ------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
            "image": current_image,
        }
    )


    with st.chat_message("user"):

        if current_image is not None:

            st.image(
                current_image,
                width=350,
            )

        st.markdown(prompt)


    # ------------------------------------------------------
    # ASSISTANT
    # ------------------------------------------------------

    with st.chat_message("assistant"):

        placeholder = st.empty()

        response = ""


        # ==================================================
        # VISION
        # ==================================================

        if current_image is not None:

            with st.spinner(
                "🖼️ Rasm tahlil qilinmoqda..."
            ):

                try:

                    response = ai.vision_chat(
                        image=current_image,
                        user_prompt=prompt,
                    )

                except Exception as e:

                    response = (
                        "❌ Rasmni tahlil qilishda xato: "
                        + str(e)
                    )

            placeholder.markdown(
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

            with st.spinner(
                "🤖 EduMindAI javob bermoqda..."
            ):

                try:

                    for chunk in ai.stream_chat(
                        user_prompt=prompt,
                        history=history,
                        context="",
                        web_search="",
                        deep_thinking=deep_thinking,
                    ):

                        if chunk is not None:

                            response += str(chunk)

                            placeholder.markdown(
                                response + "▌"
                            )

                except Exception as e:

                    response = (
                        "❌ AI xatosi: "
                        + str(e)
                    )

            placeholder.markdown(
                response
            )


    # ======================================================
    # SAVE ASSISTANT
    # ======================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "image": None,
        }
    )
