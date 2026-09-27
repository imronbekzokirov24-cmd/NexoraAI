```python
import os
import streamlit as st

# ==========================================================
# OPENAI IMAGE API KEY
# ==========================================================

# Streamlit Secrets'dan OPENAI_API_KEY olish
try:
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    pass


from ai_engine import ai
from image_generator import generate_image


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

    col1, col2, col3 = st.columns([1, 2, 1])

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
    box-shadow: 0 3px 12px rgba(30, 60, 100, 0.04);
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
   IMAGE GENERATOR
   ======================================================== */

.image-generator-box {
    background: #ffffff;
    border: 1px solid #e2e9f3;
    border-radius: 20px;
    padding: 25px;
    margin-top: 10px;
    box-shadow: 0 5px 20px rgba(30, 60, 100, 0.05);
}

.image-title {
    color: #17233c;
    font-size: 28px;
    font-weight: 750;
}

.image-subtitle {
    color: #8997aa;
    font-size: 14px;
    margin-bottom: 20px;
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

if "generated_images" not in st.session_state:
    st.session_state.generated_images = []


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("""
    <div class="logo-title">
        🧠 EduMindAI
    </div>

    <div class="logo-subtitle">
        Your AI Study Assistant
    </div>
    """, unsafe_allow_html=True)


    # CHAT HISTORY

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
            reversed(st.session_state.chat_titles)
        ):

            real_index = (
                len(st.session_state.chat_titles)
                - 1
                - i
            )

            if st.button(
                "💬 " + title,
                key=f"history_{real_index}",
                use_container_width=True,
            ):

                st.session_state.selected_chat = real_index


    st.markdown("---")


    # IMAGE GENERATOR BUTTON

    st.markdown(
        '<div class="sidebar-title">AI TOOLS</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "🖼️ AI Image Generator",
        use_container_width=True,
    ):
        st.session_state.page = "image"
        st.rerun()


    if st.button(
        "💬 AI Chat",
        use_container_width=True,
    ):
        st.session_state.page = "chat"
        st.rerun()


    st.markdown("---")


    # MODEL

    st.markdown(
        '<div class="sidebar-title">GROQ MODEL</div>',
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

    ai.set_model(selected_model)


    st.markdown("---")


    # SETTINGS

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


    # USER

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


    # STATISTICS

    st.markdown(
        '<div class="sidebar-title">STATISTICS</div>',
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

        <div class="stat-card">

            <div class="stat-title">
                🖼️ Yaratilgan rasmlar
            </div>

            <div class="stat-number">
                {len(st.session_state.generated_images)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown("---")


    # NEW CHAT

    if st.button(
        "➕ Yangi chat",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.active_image = None
        st.session_state.pasted_image = None
        st.session_state.page = "chat"

        st.rerun()


    # CLEAR

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
# DEFAULT PAGE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "chat"


# ==========================================================
# IMAGE GENERATOR PAGE
# ==========================================================

if st.session_state.page == "image":

    st.markdown("""
    <div class="brand">

        <div class="brand-icon">
            🎨
        </div>

        <div>

            <div class="brand-name">
                AI Image Generator
            </div>

            <div class="brand-subtitle">
                Turn your ideas into high-quality images
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    <div class="image-generator-box">

        <div class="image-title">
            🖼️ Create an image
        </div>

        <div class="image-subtitle">
            Rasmni qanday xohlayotganingizni batafsil yozing.
        </div>

    </div>
    """, unsafe_allow_html=True)


    image_prompt = st.text_area(
        "Prompt",
        placeholder=(
            "Masalan: A futuristic city at night, "
            "cinematic lighting, realistic architecture, "
            "rainy streets, ultra detailed, 4K..."
        ),
        height=150,
        key="image_prompt",
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        image_size = st.selectbox(
            "📐 O‘lcham",
            [
                "1024x1024",
                "1536x1024",
                "1024x1536",
            ],
        )


    with col2:

        image_quality = st.selectbox(
            "✨ Sifat",
            [
                "high",
                "medium",
                "low",
            ],
            index=0,
        )


    with col3:

        image_style = st.selectbox(
            "🎨 Uslub",
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


    # STYLE PROMPT

    style_text = ""

    if image_style == "Photorealistic":
        style_text = (
            "photorealistic, natural lighting, realistic textures, "
            "high detail, professional photography"
        )

    elif image_style == "Cinematic":
        style_text = (
            "cinematic composition, dramatic lighting, "
            "film still, atmospheric, professional color grading"
        )

    elif image_style == "Anime":
        style_text = (
            "high quality anime art, detailed character design, "
            "beautiful background, polished illustration"
        )

    elif image_style == "3D Render":
        style_text = (
            "high quality 3D render, realistic materials, "
            "detailed environment, studio quality"
        )

    elif image_style == "Digital Art":
        style_text = (
            "professional digital artwork, detailed composition, "
            "polished digital painting"
        )

    elif image_style == "Fantasy":
        style_text = (
            "epic fantasy artwork, magical atmosphere, "
            "detailed environment, cinematic lighting"
        )

    elif image_style == "Minimalist":
        style_text = (
            "clean minimalist design, simple composition, "
            "balanced spacing, elegant visual style"
        )


    st.markdown("### 📝 Prompt")


    if st.button(
        "✨ CREATE IMAGE",
        type="primary",
        use_container_width=True,
    ):

        if not image_prompt.strip():

            st.warning(
                "Avval rasm qanday bo‘lishini yozing."
            )

        else:

            final_prompt = image_prompt.strip()

            if style_text:
                final_prompt += ", " + style_text


            try:

                with st.spinner(
                    "🎨 AI rasm yaratmoqda..."
                ):

                    image = generate_image(
                        prompt=final_prompt,
                        size=image_size,
                        quality=image_quality,
                    )


                st.session_state.generated_images.append(
                    {
                        "prompt": image_prompt,
                        "image": image,
                    }
                )

                st.session_state.active_image = image


                st.success(
                    "✅ Rasm muvaffaqiyatli yaratildi!"
                )


                st.image(
                    image,
                    use_container_width=True,
                )


                image_bytes = None

                try:

                    from io import BytesIO

                    buffer = BytesIO()

                    image.save(
                        buffer,
                        format="PNG",
                    )

                    image_bytes = buffer.getvalue()

                except Exception:
                    pass


                if image_bytes:

                    st.download_button(
                        "⬇️ Rasmni yuklab olish",
                        data=image_bytes,
                        file_name="edumindai_generated.png",
                        mime="image/png",
                        use_container_width=True,
                    )


            except Exception as e:

                st.error(
                    "❌ Rasm yaratishda xatolik yuz berdi."
                )

                st.code(
                    str(e)
                )


    # IMAGE HISTORY

    if st.session_state.generated_images:

        st.markdown("---")

        st.markdown("### 🖼️ Image History")


        for index, item in enumerate(
            reversed(st.session_state.generated_images)
        ):

            with st.expander(
                f"🎨 {item['prompt'][:70]}"
            ):

                st.image(
                    item["image"],
                    use_container_width=True,
                )


    st.stop()


# ==========================================================
# CHAT PAGE
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

chat_submission = st.chat_input(
    "Xabaringizni yozing yoki rasmni Ctrl+V qiling...",
    accept_file=True,
    file_type=[
        "png",
        "jpg",
        "jpeg",
        "webp",
        "pdf",
        "txt",
        "csv",
        "json",
    ],
    key="groq_chat_input",
)


prompt = ""
uploaded_chat_file = None


if chat_submission is not None:

    prompt = chat_submission.text.strip()

    if chat_submission.files:

        uploaded_chat_file = chat_submission.files[0]


# ==========================================================
# SEND MESSAGE
# ==========================================================

if prompt or uploaded_chat_file:

    st.session_state.total_prompts += 1


    # FILE / IMAGE

    current_image = None
    uploaded_file_type = ""


    if uploaded_chat_file is not None:

        uploaded_file_type = (
            uploaded_chat_file.type or ""
        )


        if uploaded_file_type.startswith("image/"):

            current_image = uploaded_chat_file


    # TITLE

    title = prompt.strip()


    if not title and uploaded_chat_file is not None:

        title = "📎 " + uploaded_chat_file.name


    if not title:

        title = "Yangi chat"


    if len(title) > 30:

        title = title[:30] + "..."


    if not st.session_state.messages:

        st.session_state.chat_titles.append(
            title
        )


    # USER MESSAGE

    user_content = prompt


    if not user_content and uploaded_chat_file is not None:

        if current_image:

            user_content = "📷 Rasm yuborildi"

        else:

            user_content = (
                f"📎 {uploaded_chat_file.name}"
            )


    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_content,
            "image": current_image,
        }
    )


    with st.chat_message("user"):

        if current_image:

            st.image(
                current_image,
                width=350,
            )


        if prompt:

            st.markdown(prompt)

        elif uploaded_chat_file is not None:

            st.markdown(
                f"📎 **{uploaded_chat_file.name}**"
            )


    # ======================================================
    # AI
    # ======================================================

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        response = ""


        # VISION

        if current_image:

            vision_prompt = (
                prompt
                if prompt
                else "Bu rasmni batafsil tahlil qil."
            )


            with st.spinner(
                "🖼️ Rasm tahlil qilinmoqda..."
            ):

                response = ai.vision_chat(
                    image=current_image,
                    user_prompt=vision_prompt,
                )


            response_placeholder.markdown(
                response
            )


        # OTHER FILE

        elif uploaded_chat_file is not None:

            response = (
                f"📎 **{uploaded_chat_file.name}** "
                "fayli qabul qilindi. "
                "Hozircha bu chat oynasida rasm "
                "tahlili faol."
            )


            response_placeholder.markdown(
                response
            )


        # NORMAL CHAT

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


    # SAVE

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "image": None,
        }
    )
```
