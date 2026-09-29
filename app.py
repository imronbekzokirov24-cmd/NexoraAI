import io
import streamlit as st
import ai_engine as ai


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="NexoraAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# IMAGE GENERATOR IMPORT
# ==========================================================

IMAGE_GENERATOR_AVAILABLE = False
IMAGE_GENERATOR_ERROR = None
generate_image = None

try:
    from image_generator import generate_image
    IMAGE_GENERATOR_AVAILABLE = True

except Exception as e:
    generate_image = None
    IMAGE_GENERATOR_ERROR = str(e)


# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "image_history" not in st.session_state:
    st.session_state.image_history = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "openai/gpt-oss-120b"

if "page" not in st.session_state:
    st.session_state.page = "Chat"

if "deep_thinking" not in st.session_state:
    st.session_state.deep_thinking = False


# ==========================================================
# SET DEFAULT MODEL
# ==========================================================

try:
    ai.set_model(st.session_state.selected_model)
except Exception:
    pass


# ==========================================================
# CSS
# ==========================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1200px;
    }

    .nexora-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .nexora-subtitle {
        color: #777;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .creator {
        text-align: center;
        color: #888;
        font-size: 13px;
        margin-top: 50px;
        padding: 20px;
    }

    .history-card {
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e5e5e5;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;">
            <h1>🤖 NexoraAI</h1>
            <p>AI Assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ------------------------------------------------------
    # NAVIGATION
    # ------------------------------------------------------

    if st.button(
        "💬 Chat",
        use_container_width=True,
    ):
        st.session_state.page = "Chat"
        st.rerun()

    if st.button(
        "🎨 AI Image Generator",
        use_container_width=True,
    ):
        st.session_state.page = "Image Generator"
        st.rerun()

    if st.button(
        "🕘 Chat History",
        use_container_width=True,
    ):
        st.session_state.page = "History"
        st.rerun()

    st.divider()

    # ------------------------------------------------------
    # MODEL
    # ------------------------------------------------------

    st.markdown("### Model")

    model = st.selectbox(
        "Select model",
        [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
        ],
        index=(
            0
            if st.session_state.selected_model
            == "openai/gpt-oss-120b"
            else 1
        ),
        label_visibility="collapsed",
    )

    if model != st.session_state.selected_model:

        st.session_state.selected_model = model

        try:
            ai.set_model(model)
        except Exception:
            pass

    # ------------------------------------------------------
    # DEEP THINKING
    # ------------------------------------------------------

    st.session_state.deep_thinking = st.toggle(
        "Deep Thinking",
        value=st.session_state.deep_thinking,
    )

    st.divider()

    # ------------------------------------------------------
    # NEW CHAT
    # ------------------------------------------------------

    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.page = "Chat"

        st.rerun()

    st.divider()

    # ------------------------------------------------------
    # APP INFO
    # ------------------------------------------------------

    st.markdown("### NexoraAI")

    st.caption("AI Assistant")
    st.caption("No login required")


# ==========================================================
# CHAT PAGE
# ==========================================================

if st.session_state.page == "Chat":

    st.markdown(
        '<div class="nexora-title">NexoraAI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="nexora-subtitle">AI Assistant</div>',
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------
    # DISPLAY MESSAGES
    # ------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            content = message.get(
                "content",
                ""
            )

            if content:
                st.markdown(content)

            if message.get("image") is not None:

                st.image(
                    message["image"],
                    use_container_width=True,
                )

    # ------------------------------------------------------
    # CHAT INPUT
    # ------------------------------------------------------

    user_input = st.chat_input(
        "Message NexoraAI...",
        accept_file=True,
        file_type=[
            "png",
            "jpg",
            "jpeg",
            "webp",
            "pdf",
            "txt",
            "csv",
            "docx",
        ],
    )

    if user_input:

        # ==================================================
        # GET TEXT
        # ==================================================

        prompt = user_input.text or ""

        # ==================================================
        # GET FILE
        # ==================================================

        uploaded_file = None

        try:
            uploaded_file = user_input.files
        except Exception:
            uploaded_file = None

        # ==================================================
        # IF FILE LIST
        # ==================================================

        if isinstance(uploaded_file, list):

            if len(uploaded_file) > 0:
                uploaded_file = uploaded_file[0]
            else:
                uploaded_file = None

        # ==================================================
        # USER MESSAGE
        # ==================================================

        if prompt:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            with st.chat_message("user"):
                st.markdown(prompt)

        # ==================================================
        # FILE / IMAGE
        # ==================================================

        file_data = None

        if uploaded_file is not None:

            try:

                file_name = getattr(
                    uploaded_file,
                    "name",
                    "",
                )

                file_type = getattr(
                    uploaded_file,
                    "type",
                    "",
                )

                file_data = uploaded_file

                # ------------------------------------------
                # IMAGE
                # ------------------------------------------

                if (
                    file_type
                    and file_type.startswith("image/")
                ):

                    image_bytes = uploaded_file.getvalue()

                    st.session_state.messages.append(
                        {
                            "role": "user",
                            "content": f"📎 {file_name}",
                            "image": image_bytes,
                        }
                    )

                    with st.chat_message("user"):

                        st.markdown(
                            f"📎 **{file_name}**"
                        )

                        st.image(
                            image_bytes,
                            use_container_width=True,
                        )

                # ------------------------------------------
                # OTHER FILE
                # ------------------------------------------

                else:

                    st.session_state.messages.append(
                        {
                            "role": "user",
                            "content": f"📎 {file_name}",
                        }
                    )

                    with st.chat_message("user"):

                        st.markdown(
                            f"📎 **{file_name}**"
                        )

            except Exception as e:

                st.warning(
                    f"Faylni o‘qishda xato: {e}"
                )

        # ==================================================
        # AI RESPONSE
        # ==================================================

        if prompt or file_data:

            with st.chat_message("assistant"):

                try:

                    # ======================================
                    # IMAGE VISION
                    # ======================================

                    if (
                        file_data is not None
                        and getattr(
                            file_data,
                            "type",
                            "",
                        ).startswith("image/")
                    ):

                        image_bytes = (
                            file_data.getvalue()
                        )

                        response = ai.vision_chat(
                            user_prompt=(
                                prompt
                                if prompt
                                else
                                "Analyze this image."
                            ),
                            image_bytes=image_bytes,
                        )

                        if response is None:

                            response = (
                                "AI javob qaytarmadi."
                            )

                        st.markdown(response)

                    # ======================================
                    # NORMAL CHAT
                    # ======================================

                    else:

                        response = st.write_stream(
                            ai.stream_chat(
                                user_prompt=prompt,
                                history=(
                                    st.session_state.messages[:-1]
                                ),
                                context="",
                                web_search="",
                                deep_thinking=(
                                    st.session_state
                                    .deep_thinking
                                ),
                            )
                        )

                        if response is None:

                            response = (
                                "AI javob qaytarmadi."
                            )

                    # ======================================
                    # SAVE RESPONSE
                    # ======================================

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response,
                        }
                    )

                except Exception as e:

                    error_message = (
                        f"❌ AI xatosi:\n\n{e}"
                    )

                    st.error(
                        error_message
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                        }
                    )


# ==========================================================
# IMAGE GENERATOR PAGE
# ==========================================================

elif st.session_state.page == "Image Generator":

    st.markdown(
        '<div class="nexora-title">AI Image Generator</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="nexora-subtitle">'
        "Describe an image and let AI create it."
        "</div>",
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------
    # GENERATOR STATUS
    # ------------------------------------------------------

    if not IMAGE_GENERATOR_AVAILABLE:

        st.error(
            "❌ Image generator yuklanmadi."
        )

        if IMAGE_GENERATOR_ERROR:

            st.code(
                IMAGE_GENERATOR_ERROR
            )

        st.info(
            "image_generator.py fayli va "
            "requirements.txt ni tekshiring."
        )

    else:

        # --------------------------------------------------
        # PROMPT
        # --------------------------------------------------

        prompt = st.text_area(
            "Describe your image",
            placeholder=(
                "A futuristic city at night, "
                "cinematic lighting, realistic, 4K..."
            ),
            height=140,
        )

        # --------------------------------------------------
        # SETTINGS
        # --------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            size = st.selectbox(
                "Image size",
                [
                    "1024x1024",
                    "1536x1024",
                    "1024x1536",
                ],
            )

        with col2:

            quality = st.selectbox(
                "Quality",
                [
                    "high",
                    "medium",
                    "low",
                ],
            )

        # --------------------------------------------------
        # GENERATE
        # --------------------------------------------------

        if st.button(
            "🎨 Generate Image",
            use_container_width=True,
            type="primary",
        ):

            if not prompt.strip():

                st.warning(
                    "Avval rasm uchun prompt yozing."
                )

            else:

                with st.spinner(
                    "AI rasm yaratmoqda..."
                ):

                    try:

                        image = generate_image(
                            prompt=prompt,
                            size=size,
                            quality=quality,
                        )

                        if image is None:

                            raise ValueError(
                                "AI rasm qaytarmadi."
                            )

                        # ----------------------------------
                        # HISTORY
                        # ----------------------------------

                        st.session_state.image_history.append(
                            {
                                "prompt": prompt,
                                "image": image,
                            }
                        )

                        # ----------------------------------
                        # SHOW IMAGE
                        # ----------------------------------

                        st.success(
                            "Rasm tayyor! 🎉"
                        )

                        st.image(
                            image,
                            caption=prompt,
                            use_container_width=True,
                        )

                        # ----------------------------------
                        # DOWNLOAD
                        # ----------------------------------

                        buffer = io.BytesIO()

                        image.save(
                            buffer,
                            format="PNG",
                        )

                        st.download_button(
                            label="⬇️ Download Image",
                            data=buffer.getvalue(),
                            file_name=(
                                "nexora_generated.png"
                            ),
                            mime="image/png",
                            use_container_width=True,
                        )

                    except Exception as e:

                        st.error(
                            "❌ Image generation xatosi:"
                        )

                        st.code(
                            str(e)
                        )

        # --------------------------------------------------
        # IMAGE HISTORY
        # --------------------------------------------------

        if st.session_state.image_history:

            st.divider()

            st.markdown(
                "### 🕘 Generated Images"
            )

            for index, item in enumerate(
                reversed(
                    st.session_state.image_history
                )
            ):

                with st.expander(
                    f"Image "
                    f"{len(st.session_state.image_history) - index}"
                ):

                    st.write(
                        item["prompt"]
                    )

                    st.image(
                        item["image"],
                        use_container_width=True,
                    )

                    buffer = io.BytesIO()

                    item["image"].save(
                        buffer,
                        format="PNG",
                    )

                    st.download_button(
                        "⬇️ Download",
                        data=buffer.getvalue(),
                        file_name=(
                            f"nexora_image_{index + 1}.png"
                        ),
                        mime="image/png",
                        key=f"download_image_{index}",
                    )


# ==========================================================
# CHAT HISTORY PAGE
# ==========================================================

elif st.session_state.page == "History":

    st.markdown(
        '<div class="nexora-title">Chat History</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="nexora-subtitle">'
        "Your recent conversations"
        "</div>",
        unsafe_allow_html=True,
    )

    if not st.session_state.messages:

        st.info(
            "Hozircha chat tarixi bo‘sh."
        )

    else:

        # User messages
        user_messages = [
            message
            for message in st.session_state.messages
            if message["role"] == "user"
        ]

        if not user_messages:

            st.info(
                "Hozircha chat tarixi bo‘sh."
            )

        else:

            for index, message in enumerate(
                reversed(user_messages)
            ):

                text = message.get(
                    "content",
                    "New Chat",
                )

                if len(text) > 80:

                    text = (
                        text[:80]
                        + "..."
                    )

                st.markdown(
                    f"""
                    <div class="history-card">
                        <b>💬 {text}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="creator">
        Zokirov Imronbek Farhodbek o‘g‘li yaratgan
        <br>
        <b>NexoraAI</b>
    </div>
    """,
    unsafe_allow_html=True,
)
