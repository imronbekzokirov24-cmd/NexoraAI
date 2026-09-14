import os
import base64
import requests
import streamlit as st
from groq import Groq


class AIEngine:

    def __init__(self):
        self.model = "openai/gpt-oss-20b"
        self.client = None
        self._init_client()

    # =====================================================
    # GROQ
    # =====================================================

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

    # =====================================================
    # MODEL
    # =====================================================

    def set_model(self, model_name: str):

        valid_models = [
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b"
        ]

        if model_name in valid_models:
            self.model = model_name
        else:
            self.model = "openai/gpt-oss-20b"

    # =====================================================
    # CHAT
    # =====================================================

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
            yield "❌ GROQ_API_KEY topilmadi."
            return

        system_prompt = """
Siz EduMindAI Enterprise v3.5
sun'iy intellekt assistentisiz.

Foydalanuvchiga aniq, foydali
va tushunarli javob bering.

Foydalanuvchi qaysi tilda yozsa,
shu tilda javob bering.

Kod so'ralsa, ishlaydigan kod yozing.
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

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

                        messages.append({
                            "role": message["role"],
                            "content": str(content)
                        })

        full_prompt = user_prompt

        if context:

            full_prompt += (
                "\n\nQo'shimcha ma'lumot:\n"
                + str(context)
            )

        if web_search:

            full_prompt += (
                "\n\nInternet natijalari:\n"
                + str(web_search)
            )

        messages.append({
            "role": "user",
            "content": full_prompt
        })

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

    # =====================================================
    # CHAT
    # =====================================================

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
            user_prompt,
            history,
            context,
            web_search,
            deep_thinking
        ):

            answer += str(chunk)

        return answer

    # =====================================================
    # IMAGE GENERATION
    # =====================================================

    def generate_image(
        self,
        prompt: str,
        style: str = "Realistic",
        aspect_ratio: str = "1:1"
    ):

        # OpenAI API ishlatilmaydi.
        #
        # Hozircha rasm yaratish o'chirilgan.
        # Bu yerga keyinchalik local/free
        # image model ulash mumkin.

        return (
            "🎨 Rasm yaratish moduli hozircha "
            "o'chirilgan. OpenAI API ishlatilmaydi."
        )

    # =====================================================
    # VISION
    # =====================================================

    def vision_chat(
        self,
        image,
        user_prompt: str
    ):

        if self.client is None:
            self._init_client()

        if self.client is None:
            return "❌ GROQ_API_KEY topilmadi."

        try:

            if hasattr(image, "read"):
                image_bytes = image.read()
            else:
                image_bytes = image

            encoded = base64.b64encode(
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
                                + encoded
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


ai = AIEngine()
