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

    # ------------------------------------------------------
    # TEXT MODELS
    # ------------------------------------------------------

    DEFAULT_MODEL = "openai/gpt-oss-120b"

    VALID_MODELS = [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
    ]

    # Groq vision modellari
    VISION_MODELS = [
        "qwen/qwen3.6-27b",
        "qwen/qwen3.8-27b",
    ]

    def __init__(self):

        self.model = self.DEFAULT_MODEL
        self.client = None
        self.available_models = []

        self._init_client()
        self._load_available_models()

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

        # Agar key "..." ko ichiga olib qolgan bo'lsa
        api_key = api_key.strip('"').strip("'")

        try:
            self.client = Groq(
                api_key=api_key
            )

        except Exception:
            self.client = None

    # ------------------------------------------------------
    # LOAD AVAILABLE MODELS
    # ------------------------------------------------------

    def _load_available_models(self):

        self.available_models = []

        if self.client is None:
            return

        try:

            models = self.client.models.list()

            for model in models.data:

                model_id = getattr(
                    model,
                    "id",
                    None
                )

                if model_id:
                    self.available_models.append(
                        model_id
                    )

        except Exception:

            self.available_models = []

    # ------------------------------------------------------
    # FIND VISION MODEL
    # ------------------------------------------------------

    def _get_vision_model(self):

        # Avval API orqali ko'ringan modellardan qidiramiz
        if self.available_models:

            for model in self.VISION_MODELS:

                if model in self.available_models:
                    return model

        # Model list ishlamasa, birinchi zamonaviy
        # vision modelni sinab ko'ramiz
        return self.VISION_MODELS[0]

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

        # --------------------------------------------------
        # CHAT HISTORY
        # --------------------------------------------------

        if history:

            for message in history:

                role = message.get("role")
                content = message.get("content")

                if role in (
                    "user",
                    "assistant"
                ):

                    if isinstance(
                        content,
                        str
                    ):

                        messages.append(
                            {
                                "role": role,
                                "content": content,
                            }
                        )

        # --------------------------------------------------
        # CURRENT USER MESSAGE
        # --------------------------------------------------

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

            # --------------------------------------------------
            # REASONING
            # --------------------------------------------------

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

            return (
                "❌ GROQ_API_KEY topilmadi."
            )

        try:

            # ----------------------------------------------
            # IMAGE POSITION
            # ----------------------------------------------

            try:
                image.seek(0)
            except Exception:
                pass

            image_bytes = image.read()

            if not image_bytes:

                return (
                    "❌ Rasmni o'qib bo'lmadi."
                )

            # ----------------------------------------------
            # MIME TYPE
            # ----------------------------------------------

            mime_type = getattr(
                image,
                "type",
                None,
            )

            if mime_type not in (
                "image/jpeg",
                "image/png",
                "image/webp",
            ):

                mime_type = "image/jpeg"

            # ----------------------------------------------
            # BASE64
            # ----------------------------------------------

            encoded_image = (
                base64
                .b64encode(image_bytes)
                .decode("utf-8")
            )

            image_url = (
                f"data:{mime_type};base64,"
                f"{encoded_image}"
            )

            # ----------------------------------------------
            # PROMPT
            # ----------------------------------------------

            text_prompt = (
                user_prompt
                if user_prompt
                else
                "Bu rasmni batafsil tahlil qil."
            )

            # ----------------------------------------------
            # MESSAGES
            # ----------------------------------------------

            messages = [

                {
                    "role": "system",
                    "content": (
                        "Sen EduMindAI vision "
                        "yordamchisisan. "
                        "Rasmni diqqat bilan tahlil qil. "
                        "Rasmdagi obyektlar, matnlar, "
                        "diagrammalar va kodlarni "
                        "tushuntir. "
                        "Asosan o'zbek tilida javob ber."
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

            # ----------------------------------------------
            # AVAILABLE VISION MODEL
            # ----------------------------------------------

            vision_model = self._get_vision_model()

            # ----------------------------------------------
            # API REQUEST
            # ----------------------------------------------

            completion = (
                self.client
                .chat
                .completions
                .create(
                    model=vision_model,
                    messages=messages,
                    max_completion_tokens=4096,
                    temperature=0.4,
                )
            )

            # ----------------------------------------------
            # RESPONSE
            # ----------------------------------------------

            if not completion.choices:

                return (
                    "❌ Vision javobi bo'sh."
                )

            content = (
                completion
                .choices[0]
                .message
                .content
            )

            if content:

                return content

            return (
                "❌ Rasm bo'yicha javob olinmadi."
            )

        except Exception as e:

            error_text = str(e)

            # ----------------------------------------------
            # MODEL ACCESS ERROR
            # ----------------------------------------------

            if (
                "model_not_found"
                in error_text.lower()
                or
                "does not exist"
                in error_text.lower()
                or
                "do not have access"
                in error_text.lower()
            ):

                return (
                    "❌ Vision modelga kirish imkoni yo'q.\n\n"
                    f"Tanlangan model: `{self._get_vision_model()}`\n\n"
                    "Groq API key'ingiz uchun vision model "
                    "mavjudligini tekshiring."
                )

            # ----------------------------------------------
            # IMAGE SIZE ERROR
            # ----------------------------------------------

            if "20MB" in error_text:

                return (
                    "❌ Rasm juda katta.\n\n"
                    "Groq Vision uchun rasm "
                    "20 MB dan kichik bo'lishi kerak."
                )

            # ----------------------------------------------
            # OTHER ERROR
            # ----------------------------------------------

            return (
                "❌ Vision xatosi:\n\n"
                + error_text
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

        # Groq orqali image generation ishlatilmaydi.

        return None


# ----------------------------------------------------------
# GLOBAL AI ENGINE
# ----------------------------------------------------------

ai = AIEngine()
