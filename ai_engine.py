import os
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

        if api_key:
            clean_key = str(api_key).strip().strip('"').strip("'")
            self.client = Groq(api_key=clean_key)

    def set_model(self, model_name: str):
        valid_models = [
            "llama-3.3-70b-versatile",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
        ]
        if model_name in valid_models:
            self.model = model_name
        else:
            self.model = "llama-3.3-70b-versatile"

    def stream_chat(
        self,
        user_prompt: str,
        history=None,
        context: str = "",
        web_search: str = "",
        deep_thinking: bool = False,
    ):
        if self.client is None:
            self._init_client()

        if self.client is None:
            yield "❌ GROQ_API_KEY topilmadi. Streamlit Secrets bo‘limini tekshiring."
            return

        system_prompt = """
Siz EduMindAI Enterprise sun'iy intellekt assistentisiz.
Foydalanuvchiga aniq, foydali va tushunarli javob bering.
Foydalanuvchi qaysi tilda yozsa, shu tilda javob bering.
Kod so‘ralsa, kodni markdown code block ichida yozing.
"""

        messages = [{"role": "system", "content": system_prompt}]

        if history:
            for message in history:
                if message.get("role") in ["user", "assistant"]:
                    content = message.get("content", "")
                    if content:
                        messages.append(
                            {"role": message["role"], "content": str(content)}
                        )

        full_user_prompt = user_prompt
        if context:
            full_user_prompt += f"\n\nQo‘shimcha hujjat/data:\n{context}"
        if web_search:
            full_user_prompt += f"\n\nInternet qidiruv natijalari:\n{web_search}"

        messages.append({"role": "user", "content": full_user_prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, stream=True
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"❌ Groq xatosi: {str(e)}"

    def chat(
        self,
        user_prompt: str,
        history=None,
        context: str = "",
        web_search: str = "",
        deep_thinking: bool = False,
    ):
        answer = ""
        for chunk in self.stream_chat(
            user_prompt=user_prompt,
            history=history,
            context=context,
            web_search=web_search,
            deep_thinking=deep_thinking,
        ):
            answer += str(chunk)
        return answer

    def generate_image(
        self, prompt: str, style: str = "Realistic", aspect_ratio: str = "1:1"
    ):
        return "⚠️ Rasm generatsiyasi Groq matn modelida mavjud emas."

    def vision_chat(self, image, user_prompt: str):
        return "⚠️ Rasmni tahlil qilish imkoniyati Groq matn modelida mavjud emas."


ai = AIEngine()
