"""
============================================================
EduMindAI Enterprise v3.7 - Full Fixed & Updated
Google Login + AI Chat + Database + PDF/File Uploader
============================================================
"""

from auth import auth
from database import db
from ai_engine import ai
from pypdf import PdfReader
import streamlit as st

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
    "pdf_context": "",  # PDF matnini xotirada saqlash uchun
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

  # Account
  st.subheader("👤 Account")
  st.write(f"**{st.session_state.username}**")
  st.caption(st.session_state.user_email)
  st.write(f"Plan: **{st.session_state.plan}**")

  if st.button("🚪 Google'dan chiqish", use_container_width=True):
    auth.logout()

  st.markdown("---")

  # PDF UPLOADER (Sidebar)
  st.subheader("📄 PDF AI")
  uploaded_file = st.file_uploader("O'qish uchun PDF tanlang", type=["pdf"])

  if uploaded_file is not None:
    try:
      reader = PdfReader(uploaded_file)
      text_data = ""
      for page in reader.pages:
        text = page.extract_text()
        if text:
          text_data += text + "\n"

      st.session_state.pdf_context = text_data
      st.success(f"PDF o'qildi! ({len(reader.pages)} sahifa)")

      try:
        db.increase_pdfs(st.session_state.user_id)
      except Exception:
        pass

    except Exception as e:
      st.error(f"PDF o'qishda xatolik: {e}")

  if st.session_state.pdf_context:
    st.info("✅ PDF xotirada saqlangan va AIning diqqat markazida.")

  st.markdown("---")

  # AI MODEL
  st.subheader("🤖 AI Model")
  model = st.selectbox(
      "Model:",
      ["llama-3.3-70b-versatile"],
  )
  ai.set_model(model)

  # SETTINGS
  st.subheader("⚡ Settings")
  deep_thinking = st.toggle("🔬 Deep Thinking", value=False)
  memory_enabled = st.toggle("🧠 Chat Memory", value=True)

  st.markdown("---")

  # STATISTICS
  st.subheader("📊 Statistics")
  try:
    stats = db.get_statistics(st.session_state.user_id)
  except Exception:
    stats = {"questions": 0, "pdfs": 0, "images": 0}

  st.metric("💬 Savollar", stats.get("questions", 0))
  st.metric("📄 PDF", stats.get("pdfs", 0))
  st.metric("🖼️ Images", stats.get("images", 0))

  st.markdown("---")

  # CLEAR HISTORY
  if st.button("🗑️ Clear Chat", use_container_width=True):
    try:
      db.clear_chat(st.session_state.user_id)
    except Exception:
      pass
    st.session_state.messages = []
    st.session_state.pdf_context = ""
    st.rerun()


# ==========================================================
# CHAT HISTORY DISPLAY
# ==========================================================

for message in st.session_state.messages:
  role = message.get("role", "assistant")
  content = message.get("content", "")
  file_obj = message.get("file", None)

  with st.chat_message(role):
    st.markdown(content)
    if file_obj is not None:
      try:
        if hasattr(file_obj, "type") and file_obj.type in [
            "image/png",
            "image/jpeg",
            "image/jpg",
        ]:
          st.image(file_obj, width=250)
      except Exception:
        pass


# ==========================================================
# CHAT INPUT & FILE UPLOADER (Gemini uslubidagi pastki qism)
# ==========================================================

col_file, col_input = st.columns([0.08, 0.92])

with col_file:
  uploaded_chat_file = st.file_uploader(
      "➕",
      type=["png", "jpg", "jpeg", "mp4", "pdf", "xlsx"],
      label_visibility="collapsed",
      key="chat_file_uploader",
  )

with col_input:
  prompt = st.chat_input(
      "EduMindAI bilan suhbatni boshlang yoki rasm/fayl yuboring..."
  )


# ==========================================================
# PROCESS MESSAGE
# ==========================================================

if prompt or uploaded_chat_file:
  user_content = prompt if prompt else "Fayl yuborildi."
  pdf_text = st.session_state.get("pdf_context", "")

  if pdf_text:
    ai_prompt = f"Quyidagi PDF hujjati matni asosida javob ber:\n\n{pdf_text}\n\nFoydalanuvchi savoli: {user_content}"
  else:
    ai_prompt = user_content

  # Sessiyaga qo'shish
  st.session_state.messages.append(
      {
          "role": "user",
          "content": user_content,
          "file": uploaded_chat_file,
      }
  )

  # Ekranga chiqarish
  with st.chat_message("user"):
    st.markdown(user_content)
    if uploaded_chat_file is not None:
      try:
        if uploaded_chat_file.type in ["image/png", "image/jpeg", "image/jpg"]:
          st.image(uploaded_chat_file, width=250)
        elif uploaded_chat_file.type == "video/mp4":
          st.video(uploaded_chat_file)
        else:
          st.write(f"📁 Yuklangan fayl: {uploaded_chat_file.name}")
      except Exception:
        pass

  try:
    db.save_chat(st.session_state.user_id, "user", user_content)
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

    try:
      for chunk in ai.stream_chat(
          user_prompt=ai_prompt,
          history=history,
          context="",
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
