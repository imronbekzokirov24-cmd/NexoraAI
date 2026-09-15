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
            clean_key = str(api_key).strip().strip('"').strip("'")

            try:
                self.client = Groq(api_key=clean_key)
            except Exception:
                self.client = None

    def set_model(self, model_name: str):
        valid_models = [
            "openai/gpt-oss-20b",
            "openai/gpt-oss-120b"
        ]

        if model_name in valid_models:
            self.model = model_name
        else:
            self.model = "openai/gpt-oss-20b"

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
                if message.get("role") in ["user", "assistant"]:
                    content = message.get("content", "")

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

        if deep_thinking:
            full_prompt += (
                "\n\nJavobni chuqur tahlil qilib,"
                " bosqichma-bosqich tekshirib bering."
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
            yield "❌ Groq xatosi: " + str(e)

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

    def generate_image(
        self,
        prompt: str,
        style: str = "Realistic",
        aspect_ratio: str = "1:1"
    ):
        api_url = None
        api_key = None

        try:
            if "IMAGE_API_URL" in st.secrets:
                api_url = st.secrets["IMAGE_API_URL"]

            if "IMAGE_API_KEY" in st.secrets:
                api_key = st.secrets["IMAGE_API_KEY"]

        except Exception:
            pass

        if not api_url:
            api_url = os.environ.get("IMAGE_API_URL")

        if not api_key:
            api_key = os.environ.get("IMAGE_API_KEY")

        if not api_url:
            return (
                "❌ IMAGE_API_URL sozlanmagan.\n\n"
                "Rasm generator API manzilini ulash kerak."
            )

        final_prompt = (
            f"{prompt}\n\n"
            f"Style: {style}\n"
            f"Aspect ratio: {aspect_ratio}\n"
            "High quality, detailed, professional "
            "AI generated image."
        )

        headers = {
            "Content-Type": "application/json"
        }

        if api_key:
            headers["Authorization"] = "Bearer " + str(api_key)

        payload = {
            "prompt": final_prompt,
            "style": style,
            "aspect_ratio": aspect_ratio
        }

        try:
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=180
            )

            if response.status_code != 200:
                return (
                    "❌ Image API xatosi: "
                    f"{response.status_code}\n\n"
                    + response.text[:1000]
                )

            content_type = (
                response.headers
                .get("content-type", "")
                .lower()
            )

            if content_type.startswith("image/"):
                return response.content

            try:
                data = response.json()
            except Exception:
                return "❌ Image API noto'g'ri javob qaytardi."

            image_base64 = None

            if isinstance(data, dict):
                image_base64 = data.get("image")

                if not image_base64:
                    image_base64 = data.get("image_base64")

                if not image_base64:
                    image_base64 = data.get("b64_json")

            if image_base64:
                try:
                    if "," in image_base64:
                        image_base64 = image_base64.split(",", 1)[1]

                    return base64.b64decode(image_base64)

                except Exception as e:
                    return (
                        "❌ Base64 rasmni o'qishda xato: "
                        + str(e)
                    )

            image_url = None

            if isinstance(data, dict):
                image_url = data.get("url")

                if not image_url:
                    image_url = data.get("image_url")

                if not image_url:
                    image_url = data.get("output")

            if image_url:
                try:
                    image_response = requests.get(
                        image_url,
                        timeout=120
                    )

                    if image_response.status_code == 200:
                        return image_response.content

                except Exception as e:
                    return (
                        "❌ Rasm URL'dan yuklanmadi: "
                        + str(e)
                    )

            return "❌ Image API javobida rasm topilmadi."

        except requests.exceptions.Timeout:
            return (
                "❌ Rasm yaratish vaqti tugadi. "
                "Qayta urinib ko'ring."
            )

        except requests.exceptions.ConnectionError:
            return (
                "❌ Image API bilan bog'lanib bo'lmadi."
            )

        except Exception as e:
            return "❌ Rasm yaratishda xato: " + str(e)

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
