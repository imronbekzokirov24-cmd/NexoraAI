```python
"""
============================================================
EduMindAI Enterprise v3.8
AI Engine — GROQ ONLY
Chat • Reasoning • Vision
============================================================
"""

import os
import base64
import streamlit as st

from groq import Groq


class AIEngine:

    # ======================================================
    # MODELS
    # ======================================================

    DEFAULT_MODEL = "openai/gpt-oss-120b"

    VALID_MODELS = [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
    ]

    VISION_MODEL = "qwen/qwen3.6-27b"


    # ======================================================
    # INIT
    # ======================================================

    def __init__(self):

        self.model = self.DEFAULT_MODEL
        self.client = None

        self._init_client()


    # ======================================================
    # GROQ CLIENT
    # ======================================================

    def _init_client(self):

        api_key = None

        # Streamlit secrets
        try:

            if "GROQ_API_KEY" in st.secrets:

                api_key = st.secrets[
                    "GROQ_API_KEY"
                ]

        except Exception:
            pass


        # Windows environment
        if not api_key:

            api_key = os.environ.get(
                "GROQ_API_KEY"
            )


        # API key yo'q
        if not api_key:

            self.client = None
            return


        # Tozalash
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

        if model_name in self.VALID_MODELS:

            self.model = model_name

        else:

            self.model = self.DEFAULT_MODEL


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
    # SYSTEM PROMPT
    # ======================================================

    def _system_prompt(
        self,
        context="",
        web_search="",
        deep_thinking=False,
    ):

        system_prompt = """
Sen EduMindAI nomli zamonaviy AI
yordamchisisan.

Foydalanuvchiga aniq, foydali va
tushunarli javob ber.

Asosan o'zbek tilida javob ber,
lekin foydalanuvchi boshqa tilda
yozsa, o'sha tilda javob ber.

Kod so'ralganda to'liq va ishlaydigan
kod yoz.

Matematik masalalarda yechimni
bosqichma-bosqich tushuntir.

Agar foydalanuvchi seni kim yaratganini
so'rasa, aynan quyidagicha javob ber:

"Meni Zokirov Imronbek Farhodbek o‘g‘li yaratgan."

Boshqa AI kompaniyalari yoki
AI provayderlari haqida keraksiz
ma'lumot bermagin.
"""


        if deep_thinking:

            system_prompt += """

Murakkab savollarda reasoning
imkoniyatidan foydalan.

Foydalanuvchiga ichki reasoning
jarayonini ko'rsatma.

Faqat aniq va foydali yakuniy
javobni ber.
"""


        if context:

            system_prompt += (
                "\n\nQo'shimcha kontekst:\n"
                + str(context)
            )


        if web_search:

            system_prompt += (
                "\n\nQidiruv natijalari:\n"
                + str(web_search)
            )


        return system_prompt


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

        if not self._check_client():

            yield (
                "❌ GROQ_API_KEY topilmadi.\n\n"
                "Streamlit Secrets yoki "
                "Windows Environment Variables "
                "ichiga GROQ_API_KEY qo‘shing."
            )

            return


        # SYSTEM
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


        # HISTORY
        if history:

            for message in history:

                role = message.get(
                    "role"
                )

                content = message.get(
                    "content"
                )


                if (
                    role in [
                        "user",
                        "assistant",
                    ]
                    and isinstance(
                        content,
                        str
                    )
                ):

                    messages.append(
                        {
                            "role": role,
                            "content": content,
                        }
                    )


        # USER MESSAGE
        messages.append(
            {
                "role": "user",
                "content": str(
                    user_prompt
                ),
            }
        )


        # ==================================================
        # GROQ REQUEST
        # ==================================================

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

                request[
                    "reasoning_effort"
                ] = "medium"

                request[
                    "include_reasoning"
                ] = False


            completion = (
                self.client
                .chat
                .completions
                .create(
                    **request
                )
            )


            # STREAM
            for chunk in completion:

                try:

                    if not chunk.choices:
                        continue


                    delta = (
                        chunk.choices[0]
                        .delta
                    )


                    content = getattr(
                        delta,
                        "content",
                        None
                    )


                    if content:

                        yield content


                except Exception:

                    continue


        except Exception as e:

            yield (
                "❌ Groq xatosi:\n\n"
                + str(e)
            )


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
    # VISION
    # ======================================================

    def vision_chat(
        self,
        image,
        user_prompt,
    ):

        try:

            if not self._check_client():

                return (
                    "❌ GROQ_API_KEY topilmadi."
                )


            # ----------------------------------------------
            # FILE POINTERNI BOSHIga QAYTARISH
            # ----------------------------------------------

            try:

                image.seek(0)

            except Exception:
                pass


            # ----------------------------------------------
            # IMAGE BYTES
            # ----------------------------------------------

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
                "image/jpeg"
            )


            if mime_type not in [
                "image/jpeg",
                "image/png",
                "image/webp",
            ]:

                mime_type = "image/jpeg"


            # ----------------------------------------------
            # BASE64
            # ----------------------------------------------

            encoded_image = (
                base64
                .b64encode(
                    image_bytes
                )
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
            # VISION MESSAGE
            # ----------------------------------------------

            messages = [

                {
                    "role": "system",
                    "content": """
Sen EduMindAI vision yordamchisisan.

Rasmni diqqat bilan tahlil qil.

Ko'rinadigan obyektlar,
matnlar, diagrammalar,
kodlar va boshqa muhim
elementlarni tushuntir.

Agar rasmda matn bo'lsa,
uni o'qib, savolga mos
ravishda tushuntir.
""",
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
                                "url": image_url
                            },
                        },

                    ],
                },

            ]


            # ----------------------------------------------
            # GROQ VISION REQUEST
            # ----------------------------------------------

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


            # ----------------------------------------------
            # RESPONSE
            # ----------------------------------------------

            if (
                not completion.choices
            ):

                return (
                    "❌ Vision javobi bo'sh."
                )


            content = (
                completion
                .choices[0]
                .message
                .content
            )


            return (
                content
                if content
                else
                "❌ Rasm bo'yicha javob olinmadi."
            )


        except Exception as e:

            return (
                "❌ Rasmni Groq Vision orqali "
                "tahlil qilishda xato:\n\n"
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

        # Groq hozir ushbu engine orqali
        # image generation endpoint bermaydi.
        #
        # Shuning uchun boshqa image API
        # chaqirilmaydi.

        return None


# ==========================================================
# GLOBAL AI ENGINE
# ==========================================================

ai = AIEngine()
```
