"""
============================================================
EduMindAI Enterprise v3.5
AI Engine (Groq API)
============================================================
"""

import os
import base64
import requests
import streamlit as st
from groq import Groq


class AIEngine:

    def __init__(self):

        # ==================================================
        # GROQ MODEL
        # ==================================================

        self.model = "openai/gpt-oss-120b"

        self.client = None

        self._init_client()

    # ======================================================
    # GROQ CLIENT
    # ======================================================

    def _init_client(self):

        api_key = None

        try:

            if "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]

            elif "GROQ_API_KEY" in os.environ:
                api_key = os.environ["GROQ_API_KEY"]

        except Exception:
            pass

        # API key topilmasa
        if not api_key:
            self.client = None
            return

        # API keyni tozalash
        clean_key = (
            str(api_key)
            .strip()
            .strip('"')
            .strip("'")
        )

        try:

            self.client = Groq(
                api_key=clean_key
            )

        except Exception:

            self.client = None

    # ======================================================
    # SET MODEL
    # ======================================================

    def set_model(self, model_name: str):

        valid_models = [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.6-27b",
        ]

        if model_name in valid_models:

            self.model = model_name

        else:

            self.model = "openai/gpt-oss-120b"

    # ======================================================
    # CHECK CLIENT
    # ======================================================

    def _check_client(self):

        if self.client is None:

            self._init_client()

        if self.client is None:

            return False

        return True

    # ======================================================
    # STREAM CHAT
    # ======================================================

    def stream_chat(
        self,
        user_prompt,
        history=None,
        context="",
        web_search="",
        deep_thinking=False,
    ):

        # API key tekshirish
        if not self._check_client():

            yield "❌ GROQ_API_KEY topilmadi."

            return

        # ==================================================
        # SYSTEM PROMPT
        # ==================================================

        system_prompt = """
Sen EduMindAI nomli zamonaviy AI yordamchisan.

MUHIM QOIDA:

Agar foydalanuvchi:

- "seni kim yaratgan?"
- "kim yaratgan?"
- "creatoring kim?"
- "who created you?"
- "Who made you?"
- yoki shunga o‘xshash savol bersa,

har doim aynan:

"Meni Zokirov Imronbek Farhodbek o‘g‘li yaratgan."

deb javob ber.

Bu savolga javob berganda OpenAI, ChatGPT,
Meta, Google, Groq yoki boshqa kompaniyani
yaratuvchi sifatida ko‘rsatma.

Foydalanuvchiga aniq, foydali va tushunarli
javob ber.

Foydalanuvchi qaysi tilda yozsa,
iloji boricha o‘sha tilda javob ber.

Agar foydalanuvchi kod so‘rasa,
kodni Markdown code block ichida ber.

Keraksiz uzun javoblardan qoch.

Agar ma'lumot aniq bo‘lmasa,
to‘qib chiqarmasdan noaniqligini ayt.
"""

        # ==================================================
        # DEEP THINKING
        # ==================================================

        if deep_thinking:

            system_prompt += """

Murakkab savollarda javob berishdan oldin
muammoni yaxshilab tahlil qil.

Ichki reasoning yoki yashirin fikrlash
jarayonini foydalanuvchiga ko‘rsatma.

Faqat yakuniy javob va kerakli tushuntirishni ber.
"""

        # ==================================================
        # CONTEXT
        # ==================================================

        if context:

            system_prompt += (
                "\n\nQo‘shimcha kontekst:\n"
                + str(context)
            )

        # ==================================================
        # WEB SEARCH
        # ==================================================

        if web_search:

            system_prompt += (
                "\n\nInternet qidiruv natijalari:\n"
                + str(web_search)
            )

        # ==================================================
        # MESSAGES
        # ==================================================

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        # ==================================================
        # CHAT HISTORY
        # ==================================================

        if history:

            for message in history:

                role = message.get("role")
                content = message.get("content")

                if role not in [
                    "user",
                    "assistant"
                ]:
                    continue

                if isinstance(content, str):

                    messages.append(
                        {
                            "role": role,
                            "content": content,
                        }
                    )

        # ==================================================
        # CURRENT USER MESSAGE
        # ==================================================

        messages.append(
            {
                "role": "user",
                "content": str(user_prompt),
            }
        )

        # ==================================================
        # GROQ API REQUEST
        # ==================================================

        try:

            completion = self.client.chat.completions.create(

                model=self.model,

                messages=messages,

                stream=True,

                temperature=0.7,

                max_tokens=4096,
            )

            # ==================================================
            # STREAM RESPONSE
            # ==================================================

            for chunk in completion:

                try:

                    if not chunk.choices:
                        continue

                    content = (
                        chunk.choices[0]
                        .delta
                        .content
                    )

                    if content:

                        yield content

                except Exception:

                    continue

        except Exception as e:

            yield f"❌ Groq xatosi: {str(e)}"

    # ======================================================
    # NORMAL CHAT
    # ======================================================

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

    # ======================================================
    # VISION / IMAGE CHAT
    # ======================================================

    def vision_chat(
        self,
        image,
        user_prompt,
    ):

        try:

            if not self._check_client():

                return "❌ GROQ_API_KEY topilmadi."

            # Hozircha rasmni alohida vision modelga
            # yubormasdan foydalanuvchi savolini qayta ishlaymiz.

            prompt = f"""
Foydalanuvchi rasm yukladi.

Foydalanuvchining savoli:
{user_prompt}

Rasm asosida javob berish kerak.
Agar rasm mazmunini ko‘rish imkoniyati bo‘lmasa,
buni ochiq ayt.
"""

            return self.chat(
                user_prompt=prompt
            )

        except Exception as e:

            return (
                "❌ Rasmni tahlil qilishda xato: "
                + str(e)
            )

    # ======================================================
    # IMAGE GENERATION
    # ======================================================

    def generate_image(
        self,
        prompt,
        style="Realistic",
        aspect_ratio="1:1",
    ):

        try:

            api_url = None
            api_key = None

            # ==================================================
            # STREAMLIT SECRETS
            # ==================================================

            try:

                if "IMAGE_API_URL" in st.secrets:

                    api_url = st.secrets[
                        "IMAGE_API_URL"
                    ]

                if "IMAGE_API_KEY" in st.secrets:

                    api_key = st.secrets[
                        "IMAGE_API_KEY"
                    ]

            except Exception:

                pass

            # ==================================================
            # ENVIRONMENT VARIABLES
            # ==================================================

            if not api_url:

                api_url = os.environ.get(
                    "IMAGE_API_URL"
                )

            if not api_key:

                api_key = os.environ.get(
                    "IMAGE_API_KEY"
                )

            # ==================================================
            # API URL BO‘LMASA
            # ==================================================

            if not api_url:

                return None

            # ==================================================
            # HEADERS
            # ==================================================

            headers = {
                "Content-Type": "application/json"
            }

            if api_key:

                headers["Authorization"] = (
                    f"Bearer {api_key}"
                )

            # ==================================================
            # PAYLOAD
            # ==================================================

            payload = {

                "prompt": str(prompt),

                "style": str(style),

                "aspect_ratio": str(
                    aspect_ratio
                ),
            }

            # ==================================================
            # REQUEST
            # ==================================================

            response = requests.post(

                api_url,

                headers=headers,

                json=payload,

                timeout=120,
            )

            response.raise_for_status()

            # ==================================================
            # DIRECT IMAGE
            # ==================================================

            content_type = response.headers.get(
                "content-type",
                ""
            )

            if content_type.startswith("image/"):

                return response.content

            # ==================================================
            # JSON RESPONSE
            # ==================================================

            data = response.json()

            # ==================================================
            # BASE64 IMAGE
            # ==================================================

            for key in [
                "image",
                "image_base64",
                "b64_json",
            ]:

                if key in data:

                    value = data[key]

                    if isinstance(value, str):

                        try:

                            return base64.b64decode(
                                value
                            )

                        except Exception:

                            pass

            # ==================================================
            # IMAGE URL
            # ==================================================

            for key in [
                "url",
                "image_url",
                "output",
            ]:

                if key in data:

                    value = data[key]

                    if isinstance(value, str):

                        return value

            return None

        except Exception:

            return None


# ==========================================================
# GLOBAL AI INSTANCE
# ==========================================================

ai = AIEngine()
