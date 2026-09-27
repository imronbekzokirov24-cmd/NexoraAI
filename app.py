import os
import io
import base64
import streamlit as st

from PIL import Image

import ai_engine as ai

try:
    from image_generator import generate_image
    IMAGE_GENERATOR_AVAILABLE = True
except Exception:
    IMAGE_GENERATOR_AVAILABLE = False


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NexoraAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# LOAD SECRETS
# =========================================================

try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    pass


# =========================================================
# CUSTOM CSS
# =========================================================

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
    }

    .nexora-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .nexora-subtitle {
        color: #777;
        font-size: 15px;
        margin-bottom: 25px;
    }

    .creator {
        text-align: center;
        color: #888;
        font-size: 12px;
        margin-top: 30px;
    }

    .image-card {
        padding: 15px;
        border-radius: 18px;
        border: 1px solid #e5e5e5;
        background: #ffffff;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

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


# =========================================================
# AUTH
# =========================================================

try:
    is_logged_in = st.user.is_logged_in
except Exception:
    is_logged_in = False


if not is_logged_in:

    st.markdown(
        """
        <div style="text-align:center; margin-top:100px;">
            <div style="font-size:55px;">🤖</div>
            <div class="nexora-title">NexoraAI</div>
            <div class="nexora-subtitle">
                AI Assistant • Chat • Vision • Image Generation
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="text-align:center;">
            <p>Continue with your account to use NexoraAI.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button(
            "🔐 Sign in",
            use_container_width=True,
            type="primary",
        ):
            try:
                st.login("auth0")
            except Exception as e:
                st.error(f"Login xatosi: {e}")

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🤖 NexoraAI")

    st.caption("AI Assistant")

    st.divider()

    # -----------------------------------------------------
    # PAGE BUTTONS
    # -----------------------------------------------------

    if st.button(
        "💬 Chat",
        use_container_width=True,
    ):
        st.session_state.page = "Chat"
        st.rerun()

    if st.button(
        "🖼️ AI Image Generator",
        use_container_width=True,
    ):
        st.session_state.page = "Image Generator"
        st.rerun()

    if st.button(
        "📚 Chat History",
        use_container_width=True,
    ):
        st.session_state.page = "History"
        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # MODEL
    # -----------------------------------------------------

    st.markdown("### 🧠 Model")

    model_options = [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
    ]

    selected_model = st.selectbox(
        "Model",
        model_options,
        index=model_options.index(
            st.session_state.selected_model
        )
        if st.session_state.selected_model in model_options
        else 0,
    )

    st.session_state.selected_model = selected_model

    try:
        ai.set_model(selected_model)
    except Exception:
        pass

    # -----------------------------------------------------
    # DEEP THINKING
    # -----------------------------------------------------

    st.session_state.deep_thinking = st.toggle(
        "🧠 Deep Thinking",
        value=st.session_state.deep_thinking,
    )

    st.divider()

    # -----------------------------------------------------
    # NEW CHAT
    # -----------------------------------------------------

    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # USER
    # -----------------------------------------------------

    try:
        user_name = st.user.name
    except Exception:
        user_name = "User"

    try:
        user_email = st.user.email
    except Exception:
        user_email = ""

    st.markdown("### 👤 Account")

    st.write(user_name)

    if user_email:
        st.caption(user_email)

    if st.button(
        "🚪 Logout",
        use_container_width=True,
    ):
        try:
            st.logout()
        except Exception as e:
            st.error(f"Logout xatosi: {e}")

    st.markdown(
        """
        <div class="creator">
            Zokirov Imronbek Farhodbek o‘g‘li yaratgan
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# CHAT PAGE
# =========================================================

if st.session_state.page == "Chat":

    st.markdown(
        """
        <div class="nexora-title">NexoraAI</div>
        <div class="nexora-subtitle">
            Ask anything. Upload images. Generate ideas.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # DISPLAY CHAT HISTORY
    # -----------------------------------------------------

    for message in st.session_state.messages:

        role = message.get("role", "assistant")
        content = message.get("content", "")

        with st.chat_message(role):

            if content:
                st.markdown(content)

            if message.get("image") is not None:

                try:
                    st.image(
                        message["image"],
                        use_container_width=True,
                    )
                except Exception:
                    pass

            if message.get("file_name"):
                st.caption(
                    f"📎 {message['file_name']}"
                )

    # -----------------------------------------------------
    # CHAT INPUT
    # -----------------------------------------------------

    prompt = st.chat_input(
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

    if prompt:

        # -------------------------------------------------
        # GET TEXT
        # -------------------------------------------------

        try:
            user_text = prompt.text
        except Exception:
            user_text = str(prompt)

        user_text = user_text or ""

        # -------------------------------------------------
        # GET FILES
        # -------------------------------------------------

        try:
            uploaded_files = prompt.files
        except Exception:
            uploaded_files = []

        image_file = None
        other_file = None

        for uploaded_file in uploaded_files:

            file_type = uploaded_file.type or ""

            if file_type.startswith("image/"):
                image_file = uploaded_file
                break

            else:
                other_file = uploaded_file

        # -------------------------------------------------
        # USER MESSAGE
        # -------------------------------------------------

        display_text = user_text

        if image_file:
            if display_text:
                display_text += "\n\n📷 Image attached"
            else:
                display_text = "📷 Image attached"

        elif other_file:
            if display_text:
                display_text += (
                    f"\n\n📎 {other_file.name}"
                )
            else:
                display_text = (
                    f"📎 {other_file.name}"
                )

        if not display_text:
            display_text = "Please analyze the attached file."

        st.session_state.messages.append(
            {
                "role": "user",
                "content": display_text,
                "file_name": (
                    image_file.name
                    if image_file
                    else (
                        other_file.name
                        if other_file
                        else None
                    )
                ),
            }
        )

        # -------------------------------------------------
        # SHOW USER MESSAGE
        # -------------------------------------------------

        with st.chat_message("user"):

            st.markdown(display_text)

            if image_file:

                try:
                    st.image(
                        image_file,
                        use_container_width=True,
                    )
                except Exception:
                    pass

        # -------------------------------------------------
        # AI RESPONSE
        # -------------------------------------------------

        with st.chat_message("assistant"):

            try:

                # =========================================
                # VISION
                # =========================================

                if image_file:

                    image_bytes = image_file.getvalue()

                    try:

                        response = ai.vision_chat(
                            user_prompt=user_text
                            if user_text
                            else "Analyze this image.",
                            image_bytes=image_bytes,
                            history=st.session_state.messages,
                        )

                    except TypeError:

                        try:

                            response = ai.vision_chat(
                                user_text
                                if user_text
                                else "Analyze this image.",
                                image_bytes,
                            )

                        except Exception as vision_error:
                            raise vision_error

                # =========================================
                # NORMAL CHAT
                # =========================================

                else:

                    response = ai.stream_chat(
                        user_prompt=user_text,
                        history=st.session_state.messages,
                        deep_thinking=st.session_state.deep_thinking,
                    )

                # -----------------------------------------
                # HANDLE GENERATOR
                # -----------------------------------------

                if hasattr(response, "__iter__") and not isinstance(
                    response, str
                ):

                    full_response = ""

                    response_placeholder = st.empty()

                    try:

                        for chunk in response:

                            if chunk is None:
                                continue

                            chunk_text = str(chunk)

                            full_response += chunk_text

                            response_placeholder.markdown(
                                full_response
                            )

                    except TypeError:

                        full_response = str(response)

                        response_placeholder.markdown(
                            full_response
                        )

                else:

                    full_response = str(response)

                    st.markdown(full_response)

                # -----------------------------------------
                # SAVE RESPONSE
                # -----------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": full_response,
                    }
                )

            except Exception as e:

                error_text = (
                    f"❌ AI xatosi:\n\n"
                    f"`{str(e)}`"
                )

                st.error(error_text)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_text,
                    }
                )


# =========================================================
# IMAGE GENERATOR PAGE
# =========================================================

elif st.session_state.page == "Image Generator":

    st.markdown(
        """
        <div class="nexora-title">
            🖼️ AI Image Generator
        </div>

        <div class="nexora-subtitle">
            Describe an image and let AI create it.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not IMAGE_GENERATOR_AVAILABLE:

        st.error(
            "❌ image_generator.py topilmadi yoki import qilishda xato bo‘ldi."
        )

        st.info(
            "Loyihada image_generator.py fayli mavjudligini tekshiring."
        )

    else:

        # -------------------------------------------------
        # PROMPT
        # -------------------------------------------------

        image_prompt = st.text_area(
            "🎨 What do you want to create?",
            placeholder=(
                "Example: A futuristic city at night, "
                "neon lights, cinematic atmosphere, "
                "high detail"
            ),
            height=140,
        )

        # -------------------------------------------------
        # SETTINGS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            image_size = st.selectbox(
                "📐 Size",
                [
                    "1024x1024",
                    "1536x1024",
                    "1024x1536",
                ],
            )

        with col2:

            image_quality = st.selectbox(
                "✨ Quality",
                [
                    "high",
                    "medium",
                    "low",
                ],
            )

        with col3:

            image_style = st.selectbox(
                "🎨 Style",
                [
                    "Auto",
                    "Photorealistic",
                    "Cinematic",
                    "Anime",
                    "3D Render",
                    "Digital Art",
                    "Fantasy",
                    "Minimalist",
                ],
            )

        st.divider()

        # -------------------------------------------------
        # GENERATE BUTTON
        # -------------------------------------------------

        if st.button(
            "✨ Generate Image",
            type="primary",
            use_container_width=True,
        ):

            if not image_prompt.strip():

                st.warning(
                    "Avval rasm uchun prompt yozing."
                )

            else:

                final_prompt = image_prompt.strip()

                if image_style != "Auto":

                    final_prompt += (
                        f"\n\nStyle: {image_style}."
                    )

                try:

                    with st.spinner(
                        "🎨 AI rasm yaratyapti..."
                    ):

                        generated_image = generate_image(
                            prompt=final_prompt,
                            size=image_size,
                            quality=image_quality,
                        )

                    if generated_image is not None:

                        st.success(
                            "✅ Rasm tayyor!"
                        )

                        st.image(
                            generated_image,
                            use_container_width=True,
                        )

                        # ---------------------------------
                        # SAVE IMAGE HISTORY
                        # ---------------------------------

                        st.session_state.image_history.append(
                            {
                                "prompt": final_prompt,
                                "image": generated_image,
                            }
                        )

                        # ---------------------------------
                        # DOWNLOAD
                        # ---------------------------------

                        image_buffer = io.BytesIO()

                        generated_image.save(
                            image_buffer,
                            format="PNG",
                        )

                        image_buffer.seek(0)

                        st.download_button(
                            label="⬇️ Download PNG",
                            data=image_buffer.getvalue(),
                            file_name="nexoraai_generated.png",
                            mime="image/png",
                            use_container_width=True,
                        )

                    else:

                        st.error(
                            "❌ Rasm yaratilmadi."
                        )

                except Exception as e:

                    st.error(
                        "❌ Image generation xatosi:"
                    )

                    st.code(
                        str(e)
                    )

        # -------------------------------------------------
        # IMAGE HISTORY
        # -------------------------------------------------

        if st.session_state.image_history:

            st.divider()

            st.markdown("### 🕘 Generated Images")

            for index, item in enumerate(
                reversed(
                    st.session_state.image_history
                )
            ):

                with st.container():

                    st.markdown(
                        f"**Prompt:** {item['prompt']}"
                    )

                    st.image(
                        item["image"],
                        use_container_width=True,
                    )


# =========================================================
# HISTORY PAGE
# =========================================================

elif st.session_state.page == "History":

    st.markdown(
        """
        <div class="nexora-title">
            📚 Chat History
        </div>

        <div class="nexora-subtitle">
            Your current conversation history.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.messages:

        st.info(
            "Hozircha chat history bo‘sh."
        )

    else:

        for index, message in enumerate(
            st.session_state.messages
        ):

            role = message.get(
                "role",
                "assistant",
            )

            content = message.get(
                "content",
                "",
            )

            if role == "user":

                st.markdown(
                    f"**👤 You:** {content}"
                )

            else:

                st.markdown(
                    f"**🤖 NexoraAI:** {content}"
                )

            st.divider()

    if st.button(
        "🗑️ Clear History",
        use_container_width=True,
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="creator">
        NexoraAI • Chat • Vision • AI Image Generation
        <br>
        Zokirov Imronbek Farhodbek o‘g‘li yaratgan
    </div>
    """,
    unsafe_allow_html=True,
)
