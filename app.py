"""
============================================================
EduMindAI Enterprise v3.8
Groq Only • Modern Dark UI • Chat History • PDF • Vision
============================================================
"""

import streamlit as st
from pypdf import PdfReader

from database import db
from auth import auth
from ai_engine import ai


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="EduMindAI • Groq",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# DARK UI
# ==========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(110, 70, 255, 0.16),
            transparent 30%
        ),
        radial-gradient(
            circle at 10% 90%,
            rgba(60, 40, 150, 0.10),
            transparent 30%
        ),
        #070b17;
    color: #f5f5ff;
}

.block-container {
    max-width: 1500px;
    padding-top: 1rem;
    padding-bottom: 5rem;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #080c19 0%,
            #0b1021 55%,
            #080b16 100%
        );

    border-right: 1px solid rgba(130, 90, 255, 0.20);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}


/* BRAND */

.brand {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 8px 5px 18px 5px;
}

.brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #ff3b30,
        #ff684f
    );

    color: white;
    font-size: 22px;
    font-weight: 900;

    box-shadow:
        0 8px 30px rgba(255, 60, 45, 0.25);
}

.brand-name {
    font-size: 21px;
    font-weight: 800;
}

.brand-name span {
    color: #9b7cff;
}


/* TOP BAR */

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 12px 17px;
    margin-bottom: 18px;

    border-radius: 15px;

    background:
        linear-gradient(
            90deg,
            rgba(15, 20, 42, 0.97),
            rgba(22, 18, 53, 0.96)
        );

    border: 1px solid rgba(130, 90, 255, 0.20);
}

.groq-title {
    display: flex;
    align-items: center;
    gap: 11px;

    font-size: 19px;
    font-weight: 750;
}

.groq-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #ff3b30,
        #ff684f
    );

    color: white;
    font-size: 19px;
    font-weight: 900;
}

.fast-text {
    color: #858ba8;
    font-size: 13px;
}


/* HISTORY */

.history-title {
    color: #858ba8;
    font-size: 11px;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: 1px;

    margin-top: 14px;
    margin-bottom: 8px;
}

.history-item {
    padding: 9px 11px;
    margin: 3px 0;

    border-radius: 9px;

    color: #c7cadc;
    font-size: 13px;
}

.history-item:hover {
    background: rgba(110, 80, 255, 0.12);
    color: white;
}


/* ACCOUNT */

.account-card {
    padding: 13px;

    border-radius: 13px;

    background:
        linear-gradient(
            135deg,
            rgba(25, 29, 59, 0.95),
            rgba(12, 16, 33, 0.95)
        );

    border: 1px solid rgba(130, 90, 255, 0.16);
}

.account-name {
    font-size: 14px;
    font-weight: 700;
}

.account-email {
    color: #858ba8;
    font-size: 11px;
    margin-top: 3px;
}

.account-plan {
    color: #a78bfa;
    font-size: 12px;
    margin-top: 7px;
}


/* WELCOME */

.welcome {
    text-align: center;
    padding: 75px 20px 35px 20px;
}

.welcome-icon {
    width: 72px;
    height: 72px;

    margin: auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            #ff3b30,
            #ff684f
        );

    color: white;
    font-size: 33px;
    font-weight: 900;

    box-shadow:
        0 15px 50px rgba(255, 60, 40, 0.25);
}

.welcome h1 {
    font-size: 38px;
    margin-top: 18px;
    margin-bottom: 7px;
}

.welcome p {
    color: #858ba8;
}


/* CHAT */

div[data-testid="stChatMessage"] {
    border-radius: 15px;
}


/* INPUT */

div[data-testid="stChatInput"] {
    border-radius: 17px !important;

    background:
        linear-gradient(
            135deg,
            #11162d,
            #171431
        ) !important;

    border: 1px solid
        rgba(130, 90, 255, 0.30) !important;

    box-shadow:
        0 10px 40px rgba(0, 0, 0, 0.25);
}

div[data-testid="stChatInput"] textarea {
    color: white !important;
}


/* BUTTONS */

.stButton > button {
    border-radius: 10px !important;

    background:
        linear-gradient(
            135deg,
            #171b38,
            #10152a
        ) !important;

    color: #dddff1 !important;

    border: 1px solid
        rgba(130, 90, 255, 0.20) !important;

    transition: 0.2s;
}

.stButton > button:hover {
    border-color: #7659ff !important;

    box-shadow:
        0 0 20px rgba(118, 89, 255, 0.18);
}


/* SELECTBOX */

div[data-baseweb="select"] > div {
    background: #11162d !important;
    border-color: rgba(130, 90, 255, 0.25) !important;
    border-radius: 10px !important;
}


/* METRIC */

[data-testid="stMetric"] {
    background: rgba(17, 22, 45, 0.70);

    border: 1px solid
        rgba(130, 90, 255, 0.14);

    padding: 10px;
    border-radius: 12px;
}


/* FILE */

[data-testid="stFileUploader"] {
    background: rgba(13, 17, 35, 0.75);
    border-radius: 12px;
}


/* SCROLLBAR */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #080b17;
}

::-webkit-scrollbar-thumb {
    background: #29234e;
    border-radius: 10px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# SESSION STATE
# ==========================================================

defaults = {
    "logged_in": False,
    "user_id": None,
    "username": "",
    "user_email": "",
    "user_picture": "",
    "plan": "Free",
    "messages": [],
    "history_loaded": False,
    "pdf_context": "",
    "selected_model": "openai/gpt-oss-120b",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# LOGIN
# ==========================================================

google_logged_in = auth.is_logged_in()

if not google_logged_in:
    auth.show_login_page()
    st.stop()


if not st.session_state.logged_in:
    success = auth.sync_google_user()

    if not success:
        st.error("Google account ma'lumotlarini olishda xato.")
        st.stop()


# ==========================================================
# LOAD HISTORY
# ==========================================================

if not st.session_state.history_loaded:

    try:
        saved_chats = db.load_chat(
            st.session_state.user_id
        )

        st.session_state.messages = []

        for message in saved_chats:
            st.session_state.messages.append(
                {
                    "role": message["role"],
                    "content": message["content"],
                }
            )

        st.session_state.history_loaded = True

    except Exception:
        st.session_state.history_loaded = True


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">G</div>
            <div class="brand-name">
                Edu<span>MindAI</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # NEW CHAT

    if st.button(
        "＋  Yangi chat",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.pdf_context = ""

        st.rerun()


    # HISTORY

    st.markdown(
        '<div class="history-title">Chatlar</div>',
        unsafe_allow_html=True,
    )

    user_messages = [
        message
        for message in st.session_state.messages
        if message.get("role") == "user"
    ]


    if user_messages:

        for message in user_messages[-15:]:

            title = str(
                message.get("content", "")
            ).replace("\n", " ").strip()

            if not title:
                title = "Yangi chat"

            if len(title) > 42:
                title = title[:42] + "..."

            st.markdown(
                f"""
                <div class="history-item">
                    💬 {title}
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.markdown(
            """
            <div class="history-item">
                💬 Hozircha chat yo‘q
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.markdown("---")


    # ACCOUNT

    st.markdown(
        '<div class="history-title">Account</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="account-card">

            <div class="account-name">
                👤 {st.session_state.username}
            </div>

            <div class="account-email">
                {st.session_state.user_email}
            </div>

            <div class="account-plan">
                Plan: {st.session_state.plan}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.write("")


    if st.button(
        "🚪 Google'dan chiqish",
        use_container_width=True,
    ):
        auth.logout()


    st.markdown("---")


    # PDF

    st.markdown(
        '<div class="history-title">PDF AI</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "PDF tanlang",
        type=["pdf"],
        label_visibility="collapsed",
    )


    if uploaded_file is not None:

        try:

            reader = PdfReader(uploaded_file)

            text_data = ""

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    text_data += text + "\n"

            st.session_state.pdf_context = text_data

            st.success(
                f"PDF o‘qildi • {len(reader.pages)} sahifa"
            )

            try:
                db.increase_pdfs(
                    st.session_state.user_id
                )
            except Exception:
                pass

        except Exception as e:

            st.error(
                f"PDF o‘qishda xato: {e}"
            )


    if st.session_state.pdf_context:
        st.info("✅ PDF xotirada")


    st.markdown("---")


    # GROQ MODEL

    st.markdown(
        '<div class="history-title">Groq Model</div>',
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


    # SETTINGS

    st.markdown(
        '<div class="history-title">Settings</div>',
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


    # STATISTICS

    st.markdown(
        '<div class="history-title">Statistics</div>',
        unsafe_allow_html=True,
    )

    try:

        stats = db.get_statistics(
            st.session_state.user_id
        )

    except Exception:

        stats = {
            "questions": 0,
            "pdfs": 0,
            "images": 0,
        }


    st.metric(
        "💬 Savollar",
        stats.get("questions", 0),
    )

    st.metric(
        "📄 PDF",
        stats.get("pdfs", 0),
    )

    st.metric(
        "🖼️ Images",
        stats.get("images", 0),
    )


    st.markdown("---")


    if st.button(
        "🗑️ Chatni tozalash",
        use_container_width=True,
    ):

        try:
            db.clear_chat(
                st.session_state.user_id
            )
        except Exception:
            pass

        st.session_state.messages = []
        st.session_state.pdf_context = ""

        st.rerun()


# ==========================================================
# TOP BAR
# ==========================================================

st.markdown(
    """
    <div class="topbar">

        <div class="groq-title">

            <div class="groq-icon">
                G
            </div>

            <div>
                Groq
            </div>

        </div>

        <div class="fast-text">
            ⚡ Fast AI
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# WELCOME
# ==========================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome">

            <div class="welcome-icon">
                G
            </div>

            <h1>
                EduMindAI
            </h1>

            <p>
                Groq yordamida savol bering,
                PDF yuklang yoki rasm tahlil qiling.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# CHAT HISTORY DISPLAY
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

    file_obj = message.get(
        "file",
        None,
    )


    with st.chat_message(role):

        st.markdown(content)


        if file_obj is not None:

            try:

                file_type = getattr(
                    file_obj,
                    "type",
                    "",
                )


                if file_type in [
                    "image/png",
                    "image/jpeg",
                    "image/jpg",
                ]:

                    st.image(
                        file_obj,
                        width=350,
                    )


                elif file_type == "video/mp4":

                    st.video(file_obj)


            except Exception:
                pass


# ==========================================================
# CHAT FILE UPLOAD
# ==========================================================

uploaded_chat_file = st.file_uploader(
    "📎 Fayl",
    type=[
        "png",
        "jpg",
        "jpeg",
        "mp4",
        "pdf",
        "xlsx",
    ],
    label_visibility="collapsed",
    key="chat_file_uploader",
)


# ==========================================================
# CHAT INPUT
# ==========================================================

prompt = st.chat_input(
    "Groq bilan xabar yozing..."
)


# ==========================================================
# PROCESS MESSAGE
# ==========================================================

if prompt or uploaded_chat_file:

    user_content = (
        prompt
        if prompt
        else "Fayl yuborildi."
    )


    # PDF CONTEXT

    pdf_text = st.session_state.get(
        "pdf_context",
        "",
    )


    if pdf_text:

        ai_prompt = f"""
Quyidagi PDF hujjatidan foydalanib,
foydalanuvchi savoliga javob ber.

PDF HUJJATI:
{pdf_text}

FOYDALANUVCHI SAVOLI:
{user_content}
"""

    else:

        ai_prompt = user_content


    # SAVE USER MESSAGE

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_content,
            "file": uploaded_chat_file,
        }
    )


    # DISPLAY USER

    with st.chat_message("user"):

        st.markdown(user_content)


        if uploaded_chat_file is not None:

            try:

                file_type = uploaded_chat_file.type


                if file_type in [
                    "image/png",
                    "image/jpeg",
                    "image/jpg",
                ]:

                    st.image(
                        uploaded_chat_file,
                        width=350,
                    )


                elif file_type == "video/mp4":

                    st.video(
                        uploaded_chat_file
                    )


                else:

                    st.write(
                        f"📁 {uploaded_chat_file.name}"
                    )

            except Exception:
                pass


    # DATABASE

    try:

        db.save_chat(
            st.session_state.user_id,
            "user",
            user_content,
        )

        db.increase_questions(
            st.session_state.user_id
        )

    except Exception:
        pass


    # ASSISTANT

    with st.chat_message("assistant"):

        response_box = st.empty()

        response = ""


        if memory_enabled:

            history = (
                st.session_state.messages[:-1]
            )

        else:

            history = None


        try:

            # ==========================================
            # IMAGE → GROQ VISION
            # ==========================================

            if (
                uploaded_chat_file is not None
                and uploaded_chat_file.type
                in [
                    "image/png",
                    "image/jpeg",
                    "image/jpg",
                ]
            ):

                response = ai.vision_chat(
                    image=uploaded_chat_file,
                    user_prompt=(
                        prompt
                        if prompt
                        else
                        "Bu rasmni batafsil tahlil qil."
                    ),
                )

                response_box.markdown(
                    response
                )


            # ==========================================
            # NORMAL GROQ CHAT
            # ==========================================

            else:

                for chunk in ai.stream_chat(
                    user_prompt=ai_prompt,
                    history=history,
                    context="",
                    web_search="",
                    deep_thinking=deep_thinking,
                ):

                    response += str(chunk)

                    response_box.markdown(
                        response + "▌"
                    )


                response_box.markdown(
                    response
                )


        except Exception as e:

            response = (
                "❌ Groq xatosi:\n\n"
                + str(e)
            )

            response_box.error(
                response
            )


    # SAVE ASSISTANT

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


    try:

        db.save_chat(
            st.session_state.user_id,
            "assistant",
            response,
        )

    except Exception:
        pass
