"""
============================================================
EduMindAI Enterprise v3.5 (Free Edition)
Main Application
============================================================
"""

import uuid
import streamlit as st
from streamlit_mic_recorder import mic_recorder

from config import *
from database import db
from ai_engine import ai
from search import search
from speech import speech
from vision import vision
from pdf_reader import pdf_reader
from style import style
from export_utils import exporter
from data_analyzer import analyzer
from url_scraper import scraper


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="EduMindAI Enterprise",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

style.load()


# ==========================================================
# SESSION STATE
# ==========================================================

defaults = {
    "logged_in": False,
    "user_email": "",
    "user_id": str(uuid.uuid4()),
    "plan": "Free",
    "messages": [],
    "active_image": None,
    "document_text": "",
    "data_summary": "",
    "url_text": "",
    "prefilled_prompt": "",
    "total_prompts": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# TITLE
# ==========================================================

st.title("🧠 EduMindAI Enterprise v3.5")

st.caption(
    "AI Chat • Multilingual • Code Interpreter • Vision • "
    "PDF/Excel • Web Scraper • Deep Reasoning"
)

st.divider()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("⚙️ EduMindAI Control Center")
    st.markdown("---")

    # ACCOUNT
    st.subheader("👤 Account")

    if not st.session_state.logged_in:

        st.write("Tizimga kirish uchun email va parolingizni kiriting:")

        email_input = st.text_input(
            "Email:",
            placeholder="example@gmail.com",
        )

        password_input = st.text_input(
            "Parol:",
            type="password",
            placeholder="******",
        )

        if st.button("🔑 Sign In", use_container_width=True):

            if email_input and "@" in email_input:

                st.session_state.logged_in = True
                st.session_state.user_email = email_input

                st.success("Muvaffaqiyatli kirdingiz!")
                st.rerun()

            else:
                st.error("Iltimos, to'g'ri email manzilini kiriting!")

    else:

        st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Tarif:** {st.session_state.plan}")

        if st.button("🚪 Sign Out", use_container_width=True):

            st.session_state.logged_in = False
            st.session_state.user_email = ""

            st.rerun()

    st.markdown("---")

    # USAGE
    st.subheader("📊 Usage Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Xabarlar",
            len(st.session_state.messages),
        )

    with col2:
        st.metric(
            "So'rovlar",
            st.session_state.total_prompts,
        )

    st.markdown("---")

    # LANGUAGE
    st.subheader("🌐 Language Settings")

    app_language = st.selectbox(
        "Muloqot tili (Language):",
        [
            "O'zbekcha",
            "English",
            "Русский",
        ],
        index=0,
    )

    st.markdown("---")

    # AI SETTINGS
    st.subheader("🤖 AI Settings")

    ai_model = st.selectbox(
        "AI Model",
        [
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
        ],
        index=0,
    )

    ai.set_model(ai_model)

    st.markdown("---")

    # FEATURES
    st.subheader("⚡ Features")

    enable_web = st.toggle(
        "🌐 Internet Search",
        value=True,
    )

    enable_memory = st.toggle(
        "🧠 Conversation Memory",
        value=True,
    )

    enable_tts = st.toggle(
        "🔊 Voice Response",
        value=False,
    )

    voice_gender = "Ayol"

    if enable_tts:

        voice_gender = st.radio(
            "Ovoz turi:",
            [
                "Ayol",
                "Erkak",
            ],
            horizontal=True,
        )

    enable_img_gen = st.toggle(
        "🎨 Image Generation",
        value=False,
    )

    enable_deep_think = st.toggle(
        "🔬 Deep Thinking Mode",
        value=False,
    )

    img_style = "Realistic"
    img_aspect = "1:1"

    if enable_img_gen:

        st.markdown("---")
        st.subheader("🎨 Image Settings")

        img_style = st.selectbox(
            "Uslub (Style):",
            [
                "Realistic",
                "Anime",
                "3D Render",
                "Cyberpunk",
                "Oil Painting",
                "Digital Art",
            ],
        )

        img_aspect = st.selectbox(
            "O'lcham (Aspect Ratio):",
            [
                "1:1",
                "16:9",
                "9:16",
            ],
        )

    st.markdown("---")

    # PROMPT TEMPLATES
    try:

        from prompt_templates import templates

        template_prefix = templates.render_templates()

        if template_prefix:

            st.session_state.prefilled_prompt = template_prefix

            st.success(
                "Shablon tanlandi! Matningizni kiriting."
            )

    except Exception:
        pass

    st.markdown("---")

    # URL SCRAPER
    st.subheader("🔗 Web Page / Link Analyzer")

    web_url = st.text_input(
        "Veb-sayt havolasi (https://...)"
    )

    if web_url:

        with st.spinner("🔗 Sayt tahlil qilinmoqda..."):

            try:

                st.session_state.url_text = scraper.scrape_url(
                    web_url
                )

                if st.session_state.url_text:
                    st.success("Veb-sayt matni yuklandi!")

            except Exception as e:
                st.error(f"URL xatosi: {e}")

    st.markdown("---")

    # VOICE INPUT
    st.subheader("🎙️ Voice Input")

    try:

        audio_record = mic_recorder(
            start_prompt="🔴 Ovoz yozish",
            stop_prompt="⬛ To'xtatish",
            key="recorder",
        )

    except Exception as e:

        audio_record = None
        st.warning(f"Voice input ishlamadi: {e}")

    st.markdown("---")

    # EXPORT CHAT
    st.subheader("📥 Export Chat")

    if st.session_state.messages:

        try:

            docx_data = exporter.to_docx(
                st.session_state.messages
            )

            st.download_button(
                label="📄 Word (.docx)",
                data=docx_data,
                file_name="edumind_chat.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Word export xatosi: {e}")

        try:

            pdf_data = exporter.to_pdf(
                st.session_state.messages
            )

            st.download_button(
                label="📕 PDF (.pdf)",
                data=bytes(pdf_data),
                file_name="edumind_chat.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception:
            pass

    else:

        st.caption("Chatda xabarlar yo'q.")

    st.markdown("---")

    # DOCUMENT UPLOAD
    st.subheader("📄 Upload Document")

    uploaded_files = st.file_uploader(
        "PDF / TXT fayllar",
        type=[
            "pdf",
            "txt",
        ],
        accept_multiple_files=True,
    )

    if uploaded_files:

        try:

            st.session_state.document_text = pdf_reader.read_multiple(
                uploaded_files
            )

            st.success("Hujjatlar yuklandi.")

        except Exception as e:
            st.error(f"Hujjat xatosi: {e}")

    st.markdown("---")

    # EXCEL / CSV
    st.subheader("📊 Upload Data (Excel/CSV)")

    data_file = st.file_uploader(
        "Excel / CSV fayl",
        type=[
            "csv",
            "xlsx",
            "xls",
        ],
    )

    if data_file:

        try:

            df = analyzer.read_file(data_file)

            if df is not None:

                st.session_state.data_summary = (
                    analyzer.analyze_and_display(df)
                )

        except Exception as e:
            st.error(f"Data xatosi: {e}")

    st.markdown("---")

    # IMAGE UPLOAD
    st.subheader("🖼️ Upload Image")

    uploaded_image_file = st.file_uploader(
        "Rasm yuklash",
        type=[
            "png",
            "jpg",
            "jpeg",
        ],
        key="img_input",
    )

    if uploaded_image_file is not None:

        st.session_state.active_image = uploaded_image_file

        st.image(
            uploaded_image_file,
            caption="Kiritilgan rasm",
            use_container_width=True,
        )

    st.markdown("---")

    # CLEAR CHAT
    if st.button(
        "🗑 Clear Chat & History",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.active_image = None
        st.session_state.document_text = ""
        st.session_state.data_summary = ""
        st.session_state.url_text = ""
        st.session_state.prefilled_prompt = ""
        st.session_state.total_prompts = 0

        st.rerun()


# ==========================================================
# CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message.get("image") is not None:

            st.image(
                message["image"],
                use_container_width=True,
            )

        st.markdown(
            message.get("content", "")
        )


# ==========================================================
# CHAT INPUT
# ==========================================================

text_prompt = st.chat_input(
    "EduMindAI bilan suhbatni boshlang..."
)

prompt = None

if text_prompt:

    prompt = text_prompt

elif audio_record and "bytes" in audio_record:

    st.audio(
        audio_record["bytes"],
        format="audio/wav",
    )

    prompt = (
        "Ovozli xabar qabul qilindi. "
        "Ushbu xabarga mos javob ber."
    )


# ==========================================================
# PROCESS PROMPT
# ==========================================================

if prompt:

    st.session_state.total_prompts += 1

    lang_instruction = (
        "\n\n"
        "[SYSTEM INSTRUCTION: "
        f"Javobni {app_language} tilda bering.]"
    )

    if st.session_state.prefilled_prompt:

        prompt = (
            st.session_state.prefilled_prompt
            + "\n\n"
            + prompt
        )

        st.session_state.prefilled_prompt = ""

    prompt_with_lang = (
        prompt
        + lang_instruction
    )

    current_img = st.session_state.active_image

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
            "image": current_img,
        }
    )

    with st.chat_message("user"):

        if current_img is not None:

            st.image(
                current_img,
                use_container_width=True,
            )

        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()
        response = ""

        # IMAGE GENERATION
        if enable_img_gen:

            try:

                generated_image = ai.generate_image(
                    prompt=prompt,
                    style=img_style,
                    aspect_ratio=img_aspect,
                )

                if generated_image is not None:

                    response = "🎨 Rasm yaratildi."

                    placeholder.markdown(response)

                    try:
                        st.image(
                            generated_image,
                            use_container_width=True,
                        )
                    except Exception:
                        pass

                else:

                    response = (
                        "🎨 Rasm yaratish uchun "
                        "IMAGE_API_URL va IMAGE_API_KEY "
                        "sozlamalarini tekshiring."
                    )

                    placeholder.markdown(response)

            except Exception as e:

                response = f"❌ Image generation xatosi: {e}"
                placeholder.error(response)

        # VISION
        elif current_img is not None:

            with st.spinner(
                "🖼️ AI rasmni ko'rib tahlil qilmoqda..."
            ):

                try:

                    response = ai.vision_chat(
                        image=current_img,
                        user_prompt=prompt_with_lang,
                    )

                except Exception as e:

                    response = f"❌ Vision xatosi: {e}"

            placeholder.markdown(response)

            st.session_state.active_image = None

        # TEXT CHAT
        else:

            web_context = ""

            if enable_web:

                with st.spinner(
                    "🌐 Internetdan qidirilmoqda..."
                ):

                    try:

                        web_context = search.search_context(
                            prompt
                        )

                    except Exception as e:

                        web_context = (
                            f"Web search xatosi: {e}"
                        )

            full_context = (
                st.session_state.document_text
            )

            if st.session_state.data_summary:

                full_context += (
                    "\n\n"
                    "[EXCEL/CSV DATA SUMMARY]:\n"
                    + st.session_state.data_summary
                )

            if st.session_state.url_text:

                full_context += (
                    "\n\n"
                    "[WEBPAGE URL CONTENT]:\n"
                    + st.session_state.url_text
                )

            history = (
                st.session_state.messages
                if enable_memory
                else None
            )

            with st.spinner(
                "🤖 EduMindAI javob bermoqda..."
            ):

                try:

                    for chunk in ai.stream_chat(
                        user_prompt=prompt_with_lang,
                        history=history,
                        context=full_context,
                        web_search=web_context,
                        deep_thinking=enable_deep_think,
                    ):

                        if chunk is not None:

                            response += str(chunk)

                            placeholder.markdown(
                                response + "▌"
                            )

                except Exception as e:

                    response = f"❌ AI xatosi: {e}"

            placeholder.markdown(response)

        # TEXT TO SPEECH
        if enable_tts and response and not enable_img_gen:

            try:

                audio = speech.quick(response)

                if audio:
                    st.audio(audio)

            except Exception as e:
                st.warning(
                    f"Voice response xatosi: {e}"
                )

    # SAVE ASSISTANT MESSAGE
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "image": None,
        }
    )
