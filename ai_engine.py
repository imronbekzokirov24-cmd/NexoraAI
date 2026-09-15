import os
import base64
import requests
import streamlit as st
from groq import Groq


class AIEngine:

    def __init__(self):
        self.vision_model = "llama-3.2-90b-vision-preview"
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

        if not api_key:
            self.client = None
            return

        clean_key = str(api_key).strip()
        clean_key = clean_key.strip('"')
        clean_key = clean_key.strip("'")

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
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b",
        ]

        if model_name in valid_models:
            self.model = model_name
        else:
            self.model = "openai/gpt-oss-20b"

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

        if not self._check_client():
            yield "❌ GROQ_API_KEY topilmadi."
            return

        system_prompt = """
Sen EduMindAI nomli zamonaviy AI yordamchisan.

MUHIM QOIDA: Agar sizni kim yaratgan deb so'rashsa, har doim quyidagicha javob bering:
"Meni 2012-yil 20-oktyabr tug`ilgan Imronbek Zokirov yaratgan."
Hech qachon OpenAI yoki boshqa kompaniya yaratganini aytmang.

Foydalanuvchiga aniq, foydali va tushunarli javob ber.

Foydalanuvchi qaysi tilda yozsa,
iloji boricha o‘sha tilda javob ber.

Agar foydalanuvchi kod so‘rasa,
kodni Markdown code block ichida ber.

Keraksiz uzun javoblardan qoch.
"""

        if deep_thinking:
            system_prompt += """
Murakkab savollarda javobni berishdan oldin
muammoni yaxshilab tahlil qil.
Lekin foydalanuvchiga ichki reasoning yoki
yashirin fikrlash jarayonini ko‘rsatma.
"""

        if context:
            system_prompt += (
                "\n\nQo‘shimcha kontekst:\n"
                + str(context)
            )

        if web_search:
            system_prompt += (
                "\n\nInternet qidiruv natijalari:\n"
                + str(web_search)
            )

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        # ==================================================
        # HISTORY
        # ==================================================

        if history:

            for message in history:

                role = message.get("role")
                content = message.get("content")

                if role not in [
                    "user",
                    "assistant",
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
        # USER MESSAGE
        # ==================================================

        messages.append(
            {
                "role": "user",
                "content": str(user_prompt),
            }
        )

        try:

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                temperature=0.7,
            )

            for chunk in completion:

                try:

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

            yield f"❌ Groq xatosi: {e}"

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

            if hasattr(image, "seek"):
                image.seek(0)

            image_bytes = image.read()

            if not image_bytes:
                return "❌ Rasm ma'lumotlari topilmadi."

            encoded_image = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            mime_type = "image/jpeg"

            image_type = getattr(
                image,
                "type",
                None,
            )

            if image_type:

                if image_type in [
                    "image/png",
                    "image/jpeg",
                    "image/webp",
                ]:
                    mime_type = image_type

            completion = self.client.chat.completions.create(

                model=self.vision_model,

                messages=[
                    {
                        "role": "user",

                        "content": [

                            {
                                "type": "text",
                                "text": str(user_prompt),
                            },

                            {
                                "type": "image_url",

                                "image_url": {
                                    "url": (
                                        f"data:{mime_type};base64,"
                                        f"{encoded_image}"
                                    )
                                },
                            },

                        ],
                    }
                ],

                temperature=0.7,

                max_completion_tokens=1024,

            )

            result = (
                completion
                .choices[0]
                .message
                .content
            )

            if result:
                return result

            return "❌ AI rasmga javob qaytarmadi."

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

            if not api_url:
                api_url = os.environ.get(
                    "IMAGE_API_URL"
                )

            if not api_key:
                api_key = os.environ.get(
                    "IMAGE_API_KEY"
                )

            if not api_url:

                return None

            headers = {}

            if api_key:

                headers["Authorization"] = (
                    f"Bearer {api_key}"
                )

            headers["Content-Type"] = (
                "application/json"
            )

            payload = {

                "prompt": str(prompt),

                "style": str(style),

                "aspect_ratio": str(
                    aspect_ratio
                ),

            }

            response = requests.post(

                api_url,

                headers=headers,

                json=payload,

                timeout=120,

            )

            response.raise_for_status()

            content_type = response.headers.get(
                "content-type",
                "",
            )

            if content_type.startswith(
                "image/"
            ):

                return response.content

            data = response.json()

            for key in [
                "image",
                "image_base64",
                "b64_json",
            ]:

                if key in data:

                    value = data[key]

                    if isinstance(
                        value,
                        str,
                    ):

                        return base64.b64decode(
                            value
                        )

            for key in [
                "url",
                "image_url",
                "output",
            ]:

                if key in data:

                    value = data[key]

                    if isinstance(
                        value,
                        str,
                    ):

                        return value

            return None

        except requests.exceptions.Timeout:

            return None

        except requests.exceptions.RequestException:

            return None

        except Exception:

            return None


# ==========================================================
# GLOBAL AI INSTANCE
# ==========================================================

ai = AIEngine()
