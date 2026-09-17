"""
EduMindAI Enterprise
AI Engine - GROQ ONLY
Chat + Reasoning + Vision
"""

import os
import base64
import streamlit as st
from groq import Groq


class AIEngine:

    DEFAULT_MODEL = "openai/gpt-oss-120b"

    VALID_MODELS = [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
    ]

    VISION_MODEL = "qwen/qwen3.6-27b"

    def __init__(self):
        self.model = self.DEFAULT_MODEL
        self.client = None
        self._init_client()

    # ------------------------------------------------------
    # GROQ CLIENT
    # ------------------------------------------------------

    def _init_client(self):

        api_key = None

        # Streamlit Cloud Secrets
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            api_key = None

        # Windows environment variable
        if not api_key:
            api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            self.client = None
            return

        api_key = str(api_key).strip()

        api_key = api_key.strip('"').strip("'")

        try:
            self.client = Groq(api_key=api_key)
        except Exception:
            self.client = None

    # ------------------------------------------------------
    # MODEL
    # ------------------------------------------------------

    def set_model(self, model_name):

        if model_name in self.VALID_MODELS:
            self.model = model_name
        else:
            self.model = self.DEFAULT_MODEL

    # ------------------------------------------------------
    # CHECK CLIENT
    # ------------------------------------------------------

    def _check_client(self):

        if self.client is None:
            self._init_client()

        return self.client is not None

    # ------------------------------------------------------
    # SYSTEM PROMPT
    # ------------------------------------------------------

    def _system_prompt(
        self,
        context="",
        web_search="",
        deep_thinking=False,
    ):

        prompt = """
Sen EduMindAI nomli zamonaviy AI yordamchisisan.

Foydalanuvchiga aniq, foydali va tushunarli
javob ber.

Asosan o'zbek tilida javob ber.
Agar foydalanuvchi boshqa tilda yozsa,
o'sha tilda javob ber.

Kod so'ralganda to'liq va ishlaydigan kod yoz.

Matematik masalalarda yechimni bosqichma-bosqich
tushuntir.

Agar foydalanuvchi seni kim yaratganini so'rasa,
quyidagicha javob ber:

"Meni Zokirov Imronbek Farhodbek o‘g‘li yaratgan."
"""

        if deep_thinking:
            prompt += """

Murakkab savollarni chuqur tahlil qil.
Ichki reasoning jarayonini foydalanuvchiga
ko'rsatma.
Faqat yakuniy foydali javobni ber.
"""

        if context:
            prompt += (
                "\n\nQo'shimcha kontekst:\n"
                + str(context)
            )

        if web_search:
            prompt += (
                "\n\nQidiruv natijalari:\n"
                + str(web_search)
            )

        return prompt

    # ------------------------------------------------------
    # STREAM CHAT
    # ------------------------------------------------------

    def stream_chat(
        self,
        user_prompt,
        history=None,
        context="",
        web_search="",
        deep_thinking=False,
    ):

        if not self._check_client():

            yield (
                "❌ GROQ_API_KEY topilmadi.\n\n"
                "Streamlit Secrets ichiga "
                "GROQ_API_KEY qo'shing."
            )

            return

        system_prompt = self._system_prompt(
            context=context,
            web_search=web_search,
            deep_thinking=deep_thinking,
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        # Chat history
        if history:

            for message in history:

                role = message.get("role")
                content = message.get("content")

                if role in ("user", "assistant"):

                    if isinstance(content, str):

                        messages.append(
                            {
                                "role": role,
                                "content": content,
                            }
                        )

        # Current user message
        messages.append(
            {
                "role": "user",
                "content": str(user_prompt),
            }
        )

        try:

            request = {
                "model": self.model,
                "messages": messages,
                "stream": True,
                "temperature": 0.7,
                "max_tokens": 4096,
            }

            # Reasoning
            if deep_thinking:

                request["reasoning_effort"] = "medium"
                request["include_reasoning"] = False

            completion = (
                self.client
                .chat
                .completions
                .create(**request)
            )

            for chunk in completion:

                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta

                content = getattr(
                    delta,
                    "content",
                    None,
                )

                if content:
                    yield content

        except Exception as e:

            yield (
                "❌ Groq xatosi:\n\n"
                + str(e)
            )

    # ------------------------------------------------------
    # NORMAL CHAT
    # ------------------------------------------------------

    def chat(
        self,
        user_prompt,
        history=None,
        context="",
        web_search="",
        deep_thinking=False,
    ):

        result = ""

        for chunk in self.stream_chat(
            user_prompt=user_prompt,
            history=history,
            context=context,
            web_search=web_search,
            deep_thinking=deep_thinking,
        ):

            result += str(chunk)

        return result

    # ------------------------------------------------------
    # VISION
    # ------------------------------------------------------

    def vision_chat(
        self,
        image,
        user_prompt,
    ):

        if not self._check_client():

            return "❌ GROQ_API_KEY topilmadi."

        try:

            # File boshiga qaytish
            try:
                image.seek(0)
            except Exception:
                pass

            image_bytes = image.read()

            if not image_bytes:
                return "❌ Rasmni o'qib bo'lmadi."

            mime_type = getattr(
                image,
                "type",
                "image/jpeg",
            )

            if mime_type not in (
                "image/jpeg",
                "image/png",
                "image/webp",
            ):

                mime_type = "image/jpeg"

            encoded_image = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            image_url = (
                f"data:{mime_type};base64,"
                f"{encoded_image}"
            )

            text_prompt = (
                user_prompt
                if user_prompt
                else "Bu rasmni batafsil tahlil qil."
            )

            messages = [
                {
                    "role": "system",
                    "content": (
                        "Sen EduMindAI vision yordamchisisan. "
                        "Rasmni diqqat bilan tahlil qil. "
                        "Rasmdagi obyektlar, matnlar, "
                        "diagrammalar va kodlarni tushuntir."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text_prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                },
            ]

            completion = (
                self.client
                .chat
                .completions
                .create(
                    model=self.VISION_MODEL,
                    messages=messages,
                    max_tokens=4096,
                    temperature=0.4,
                )
            )

            if not completion.choices:
                return "❌ Vision javobi bo'sh."

            content = (
                completion
                .choices[0]
                .message
                .content
            )

            if content:
                return content

            return "❌ Rasm bo'yicha javob olinmadi."

        except Exception as e:

            return (
                "❌ Vision xatosi:\n\n"
                + str(e)
            )

    # ------------------------------------------------------
    # IMAGE GENERATION
    # ------------------------------------------------------

    def generate_image(
        self,
        prompt,
        style="Realistic",
        aspect_ratio="1:1",
    ):

        # Bu engine orqali image generation
        # ishlatilmaydi.

        return None


# ----------------------------------------------------------
# GLOBAL AI ENGINE
# ----------------------------------------------------------

ai = AIEngine()
