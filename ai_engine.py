"""
============================================================
EduMindAI Enterprise v3.5
AI Engine (Groq API) - Vision & Chat Fixed
============================================================
"""

import os
import base64
import requests
import streamlit as st
from groq import Groq


class AIEngine:

    def __init__(self):
        self.model = "llama-3.3-70b-versatile"
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

        if not api_key:
            self.client = None
            return

        clean_key = (
            str(api_key)
            .strip()
            .strip('"')
            .strip("'")
        )

        try:
            self.client = Groq(api_key=clean_key)
        except Exception:
            self.client = None

    def set_model(self, model_name: str):
        valid_models = [
            "llama-3.3-70b-versatile",
            "llama-3.2-11b-vision-preview",
        ]

        if model_name in valid_models:
            self.model = model_name
        else:
            self.model = "llama-3.3-70b-versatile"

    def _check_client(self):
        if self.client is None:
            self._init_client()
        if self.client is None:
            return False
        return True

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
MUHIM QOIDA:
Agar foydalanuvchi seni kim yaratganini so'rasa, har doim aynan:
"Meni Zokirov Imronbek Farhodbek o‘g‘li yaratgan."
deb javob ber. Boshqa kompaniyalarni tilga olma.
"""

        if deep_thinking:
            system_prompt += "\nMurakkab savollarda ichki fikrlash jarayonini ko'rsatmasdan, faqat yakuniy javobni ber."

        if context:
            system_prompt += f"\n\nQo‘shimcha kontekst:\n{str(context)}"

        if web_search:
            system_prompt += f"\n\nInternet qidiruv natijalari:\n{str(web_search)}"

        messages = [{"role": "system", "content": system_prompt}]

        if history:
            for message in history:
                role = message.get("role")
                content = message.get("content")
                if role in ["user", "assistant"] and isinstance(content, str):
                    messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": str(user_prompt)})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                temperature=0.7,
                max_tokens=4096,
            )

            for chunk in completion:
                try:
                    if not chunk.choices:
                        continue
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
                except Exception:
                    continue

        except Exception as e:
            yield f"❌ Groq xatosi: {str(e)}"

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

    def vision_chat(self, image, user_prompt):
        try:
            if not self._check_client():
                return "❌ GROQ_API_KEY topilmadi."

            image_bytes = image.read()
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")
            image_url = f"data:image/jpeg;base64,{encoded_image}"

            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt if user_prompt else "Bu rasmda nima tasvirlangan? Batafsil tushuntir.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                }
            ]

            completion = self.client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=messages,
                max_tokens=2048,
            )

            return completion.choices[0].message.content

        except Exception as e:
            return f"❌ Rasmni tahlil qilishda xato: {str(e)}"

    def generate_image(self, prompt, style="Realistic", aspect_ratio="1:1"):
        try:
            api_url = st.secrets.get("IMAGE_API_URL") or os.environ.get("IMAGE_API_URL")
            api_key = st.secrets.get("IMAGE_API_KEY") or os.environ.get("IMAGE_API_KEY")

            if not api_url:
                return None

            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            payload = {
                "prompt": str(prompt),
                "style": str(style),
                "aspect_ratio": str(aspect_ratio),
            }

            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()

            if response.headers.get("content-type", "").startswith("image/"):
                return response.content

            data = response.json()
            for key in ["image", "image_base64", "b64_json"]:
                if key in data and isinstance(data[key], str):
                    try:
                        return base64.b64decode(data[key])
                    except Exception:
                        pass

            for key in ["url", "image_url", "output"]:
                if key in data and isinstance(data[key], str):
                    return data[key]

            return None
        except Exception:
            return None


ai = AIEngine()
