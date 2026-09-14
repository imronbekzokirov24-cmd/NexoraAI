import os
import base64
import streamlit as st
from groq import Groq


class AIEngine:

    def __init__(self):
        # Hozirgi Groq modeli
        self.model = "openai/gpt-oss-20b"

        self.client = None

        self._init_client()

    # =========================================================
    # GROQ API
    # =========================================================

    def _init_client(self):

        api_key = None

        try:
            if "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]

            elif "GROQ_API_KEY" in os.environ:
                api_key = os.environ["GROQ_API_KEY"]

        except Exception:
            pass

        if api_key:

            clean_key = (
                str(api_key)
                .strip()
                .strip('"')
                .strip("'")
            )

            self.client = Groq(
                api_key=clean_key
            )

    # =========================================================
    # MODEL TANLASH
    # =========================================================

    def set_model(self, model_name: str):

        valid_models = [
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
        ]

        if model_name in valid_models:
            self.model = model_name

        else:
            self.model = "openai/gpt-oss-20b"

    # =========================================================
    # STREAM CHAT
    # =========================================================

    def stream_chat(
        self,
        user_prompt: str,
        history=None,
        context: str = "",
        web_search: str = "",
        deep_thinking: bool = False
    ):

        if self.client is None:
            self._init_client()

        if self.client is None:

            yield (
                "❌ GROQ_API_KEY topilmadi. "
                "Streamlit Secrets bo‘limini tekshiring."
            )

            return

        system_prompt = """
Siz EduMindAI Enterprise v3.5 sun'iy intellekt assistentisiz.

Foydalanuvchiga aniq, foydali va tushunarli javob bering.

Foydalanuvchi qaysi tilda yozsa,
shu tilda javob bering.

Kod so‘ralsa, to‘liq va ishlaydigan kod yozing.

Savollarga imkon qadar aniq javob bering.
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # -----------------------------------------------------
        # CHAT HISTORY
        # -----------------------------------------------------

        if history:

            for message in history:

                if message.get("role") in [
                    "user",
                    "assistant"
                ]:

                    content = message.get(
                        "content",
                        ""
                    )

                    if content:

                        messages.append(
                            {
                                "role": message["role"],
                                "content": str(content)
                            }
                        )

        # -----------------------------------------------------
        # USER PROMPT
        # -----------------------------------------------------

        full_user_prompt = user_prompt

        if context:

            full_user_prompt += (
                "\n\nQo‘shimcha hujjat/data:\n"
                + str(context)
            )

        if web_search:

            full_user_prompt += (
                "\n\nInternet qidiruv natijalari:\n"
                + str(web_search)
            )

        messages.append(
            {
                "role": "user",
                "content": full_user_prompt
            }
        )

        # -----------------------------------------------------
        # GROQ REQUEST
        # -----------------------------------------------------

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )

            for chunk in response:

                if not chunk.choices:
                    continue

                content = chunk.choices[0].delta.content

                if content:
                    yield content

        except Exception as e:

            yield (
                "❌ Groq xatosi: "
                + str(e)
            )

    # =========================================================
    # ODDIY CHAT
    # =========================================================

    def chat(
        self,
        user_prompt: str,
        history=None,
        context: str = "",
        web_search: str = "",
        deep_thinking: bool = False
    ):

        answer = ""

        for chunk in self.stream_chat(
            user_prompt=user_prompt,
            history=history,
            context=context,
            web_search=web_search,
            deep_thinking=deep_thinking
        ):

            answer += str(chunk)

        return answer

    # =========================================================
    # 🎨 RASM YARATISH
    # =========================================================

    def generate_image(
        self,
        prompt: str,
        style: str = "Realistic",
        aspect_ratio: str = "1:1"
    ):

        try:

            # OpenAI kutubxonasini shu yerda import qilamiz
            from openai import OpenAI

        except ImportError:

            return (
                "❌ OpenAI kutubxonasi o‘rnatilmagan. "
                "requirements.txt fayliga openai qo‘shing."
            )

        # -----------------------------------------------------
        # OPENAI API KEY
        # -----------------------------------------------------

        api_key = None

        try:

            if "OPENAI_API_KEY" in st.secrets:

                api_key = st.secrets[
                    "OPENAI_API_KEY"
                ]

            elif "OPENAI_API_KEY" in os.environ:

                api_key = os.environ[
                    "OPENAI_API_KEY"
                ]

        except Exception:
            pass

        if not api_key:

            return (
                "❌ OPENAI_API_KEY topilmadi.\n\n"
                "Streamlit Secrets bo‘limiga "
                "OPENAI_API_KEY qo‘shing."
            )

        clean_key = (
            str(api_key)
            .strip()
            .strip('"')
            .strip("'")
        )

        # -----------------------------------------------------
        # OPENAI CLIENT
        # -----------------------------------------------------

        try:

            image_client = OpenAI(
                api_key=clean_key
            )

        except Exception as e:

            return (
                "❌ OpenAI client xatosi: "
                + str(e)
            )

        # -----------------------------------------------------
        # PROMPT
        # -----------------------------------------------------

        full_prompt = f"""
Create a high-quality image based on this description:

{prompt}

Visual style:
{style}

Aspect ratio requested:
{aspect_ratio}

Make the image detailed, clean, professional,
visually attractive and well composed.
"""

        # -----------------------------------------------------
        # IMAGE GENERATION
        # -----------------------------------------------------

        try:

            result = image_client.images.generate(
                model="gpt-image-2",
                prompt=full_prompt
            )

            if not result.data:

                return "❌ Rasm yaratilmadi."

            image_data = result.data[0].b64_json

            if not image_data:

                return "❌ Rasm ma'lumoti olinmadi."

            image_bytes = base64.b64decode(
                image_data
            )

            return image_bytes

        except Exception as e:

            return (
                "❌ Rasm yaratishda xato: "
                + str(e)
            )

    # =========================================================
    # 👁 VISION
    # =========================================================

    def vision_chat(
        self,
        image,
        user_prompt: str
    ):

        if self.client is None:
            self._init_client()

        if self.client is None:

            return (
                "❌ GROQ_API_KEY topilmadi."
            )

        try:

            # Rasmni bytes ko‘rinishiga o'tkazish
            if hasattr(image, "read"):

                image_bytes = image.read()

            else:

                image_bytes = image

            encoded_image = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url":
                                "data:image/png;base64,"
                                + encoded_image
                            }
                        }
                    ]
                }
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            return response.choices[0].message.content

        except Exception as e:

            return (
                "❌ Rasmni tahlil qilishda xato: "
                + str(e)
            )


# =============================================================
# GLOBAL AI ENGINE
# =============================================================

ai = AIEngine()
