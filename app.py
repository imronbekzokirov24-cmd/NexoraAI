"""
============================================================
EduMindAI Enterprise v3.6
Google Login + AI Chat + Database + PDF AI (Fixed)
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
    page_title="EduMindAI Enterprise",
    page_icon="🧠",
    layout="wide",
)


# ==========================================================
# SESSION DEFAULTS
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
    "pdf_context": "",  # PDF matnini xotirada doimiy saqlash uchun
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# GOOGLE LOGIN CHECK
# ==========================================================

google_logged_in = auth.is_logged_in()


# ==========================================================
# LOGIN
# ==========================================================

if not google_logged_in:
    auth.show_login_page()
    st.stop()


# ==========================================================
# SYNC GOOGLE USER
# ==========================================================

if not st.session_state.logged_in:
    success = auth.sync_google_user()
    if not success:
        st.error("Google account ma'lumotlarini olishda xato.")
        st.stop()


# ==========================================================
# LOAD CHAT HISTORY
# ==========================================================

if not st.session_state.history_loaded:
    try:
        saved_chats = db.load_chat(st.session_state.user_id)
        st.session_state.messages = []
        for message in saved_chats:
            st.session_state.messages.append(
                {
                    "role": message["role"],
                    "content": message["content"],
                }
            )
        st.session_state.history_loaded = True
    except Exception as e:
        st.session_state.history_loaded = True
        st.warning(f"Chat history yuklanmadi: {e}")


# ==========================================================
# HEADER
# ==========================================================

col1, col2 = st.columns([5, 1])

with col1:
    st.title("🧠 EduMindAI Enterprise")
    st.caption("AI Chat • Multilingual • Code • Reasoning • Database • PDF")

with col2:
    if st.session_state.user_picture:
        st.image(st.session_state.user_picture, width=55)

st.divider()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.title("⚙️ EduMindAI")
    st.markdown("---")

    # ======================================================
    # ACCOUNT
    # ======================================================
    st.subheader("👤 Account")
    st.write(f"**{st.session_state.username}**")
    st.caption(st.session_state.user_email)
    st.write(f"Plan: **{st.session_state.plan}**")

    if st.button("🚪 Google'dan chiqish", use_container_width=True):
        auth.logout()

    st.markdown("---")

    # ======================================================
    # PDF UPLOADER (TUZATILGAN VA BARQAROR QISM)
    # ======================================================
    st.subheader("📄 PDF AI")
    uploaded_file = st.file_uploader("O'qish uchun PDF tanlang", type=["pdf"])
    
    if uploaded_file is not None:
        # Fayl yangi yuklanganda yoki o'zgarganda o'qiymiz
        try:
            reader = PdfReader(uploaded_file)
            text_data = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_data += text + "\n"
            
            # Matnni session_state ga yozamiz, shunda o'chib ketmaydi
            st.session_state.pdf_context = text_data
            st.success(f"PDF o'qildi! ({len(reader.pages)} sahifa)")
            
            try:
                db.increase_pdfs(st.session_state.user_id)
            except Exception:
                pass
                
        except Exception as e:
            st.error(f"PDF o'qishda xatolik: {e}")

    # Agar PDF yuklangan bo'lsa holatini ko'rsatib turish
    if st.session_state.pdf_context:
        st.info("✅ PDF xotirada saqlangan va AI ga ulab qo'yilgan.")

    st.markdown("---")

    # ======================================================
    # AI MODEL
    # ======================================================
    st.subheader("🤖 AI Model")
    model = st.selectbox(
        "Model:",
        ["llama-3.3-70b-versatile"],
    )
    ai.set_model(model)

    # ======================================================
    # SETTINGS
    # ======================================================
    st.subheader("⚡ Settings")
    deep_thinking = st.toggle("🔬 Deep Thinking", value=False)
    memory_enabled = st.toggle("🧠 Chat Memory", value=True)

    st.markdown("---")

    # ======================================================
    # STATISTICS
    # ======================================================
    st.subheader("📊 Statistics")
    try:
        stats = db.get_statistics(st.session_state.user_id)
    except Exception:
        stats = {"questions": 0, "pdfs": 0, "images": 0}

    st.metric("💬 Savollar", stats.get("questions", 0))
    st.metric("📄 PDF", stats.get("pdfs", 0))
    st.metric("🖼️ Images", stats.get("images", 0))

    st.markdown("---")

    # ======================================================
    # CLEAR HISTORY
    # ======================================================
    if st.button("🗑️ Clear Chat", use_container_width=True):
        try:
            db.clear_chat(st.session_state.user_id)
        except Exception:
            pass
        st.session_state.messages = []
        st.session_state.pdf_context = ""  # PDF kontekstini ham tozalaymiz
        st.rerun()


# ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:
    role = message.get("role", "assistant")
    content = message.get("content", "")
    with st.chat_message(role):
        st.markdown(content)


# ==========================================================
# CHAT INPUT
# ==========================================================

prompt = st.chat_input("EduMindAI bilan suhbatni boshlang yoki PDF haqida so'rang...")


# ==========================================================
# PROCESS MESSAGE
# ==========================================================

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        db.save_chat(st.session_state.user_id, "user", prompt)
        db.increase_questions(st.session_state.user_id)
    except Exception:
        pass

    with st.chat_message("assistant"):
        response_box = st.empty()
        response = ""

        if memory_enabled:
            history = st.session_state.messages[:-1]
        else:
            history = None

        # PDF matnini doimiy xotiradan olib AI ga uzatamiz
        final_context = st.session_state.get("pdf_context", "")

        try:
            for chunk in ai.stream_chat(
                user_prompt=prompt,
                history=history,
                context=final_context,  # PDF matni shu yerga boradi
                web_search="",
                deep_thinking=deep_thinking,
            ):
                response += str(chunk)
                response_box.markdown(response + "▌")

            response_box.markdown(response)

        except Exception as e:
            response = f"❌ AI xatosi: {e}"
            response_box.error(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
    try:
        db.save_chat(st.session_state.user_id, "assistant", response)
    except Exception:
        pass
