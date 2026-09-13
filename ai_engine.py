import base64
import os
import streamlit as st
from google import genai
from google.genai import types


class AIEngine:

    def __init__(self):
        # Gemini 2.5 modeli (bepul va tezkor)
        self.model = "gemini-2.5-flash"

        try:
            # Secrets yoki OS muhitidan kalitni olish
            api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get(
                "GEMINI_API_KEY"
            )
            if api_key:
                self.client = genai.Client(api_key=api_key)
            else:
                self.client = None
        except Exception:
            self.client = None

    def set_model(self, model_name: str):
        self.model = model_name

    def stream_chat(
        self,
        user_prompt: str,
        history=None,
        context: str = "",
        web_search: str = "",
        deep_thinking: bool = False,
    ):
        if self.client is None:
            yield "❌ GEMINI_API_KEY topilmadi. Streamlit Secrets bo‘limini tekshiring."
            return

        system_prompt = """
Siz EduMindAI Enterprise sun'iy intellekt assistentisiz.
Foydalanuvchiga aniq, foydali va tushunarli javob bering.
Foydalanuvchi qaysi tilda yozsa, shu tilda javob bering.
Kod so‘ralsa, kodni markdown code block ichida yozing.
"""

        if deep_thinking:
            system_prompt += """
Masalani diqqat bilan tahlil qiling va yakuniy javobni
aniq va tushunarli qilib bering.
"""

        # Promptga kontekst va web-search natijalarini qo'shish
        full_user_prompt = user_prompt
        if context:
            full_user_prompt += f"\n\nQo‘shimcha hujjat/data:\n{context}"
        if web_search:
            full_user_prompt += f"\n\nInternet qidiruv natijalari:\n{web_search}"

        # Gemini formatiga mos chat tarixini shakllantirish
        contents = []
        if history:
            for message in history:
                role = message.get("role")
                content = message.get("content", "")
                if role == "user":
                    contents.append(
                        types.Content(
                            role="user", parts=[types.Part.from_text(text=str(content))]
                        )
                    )
                elif role == "assistant":
                    contents.append(
                        types.Content(
                            role="model", parts=[types.Part.from_text(text=str(content))]
                        )
                    )

        contents.append(
            types.Content(
                role="user", parts=[types.Part.from_text(text=full_user_prompt)]
            )
        )

        try:
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
            )

            # Streaming orqali javob olish
            response = self.client.models.generate_content_stream(
                model=self.model, contents=contents, config=config
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            yield f"❌ Gemini xatosi: {str(e)}"

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
        if self.client is None:
            return None

        try:
            full_prompt = f"{prompt}. Style: {style}. High quality, detailed."

            # Imagen 3 modeli orqali rasm yaratish
            result = self.client.models.generate_images(
                model="imagen-3.0-generate-002",
                prompt=full_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio=aspect_ratio,
                    output_mime_type="image/png",
                ),
            )

            for generated_image in result.generated_images:
                encoded = base64.b64encode(generated_image.image.image_bytes).decode(
                    "utf-8"
                )
                return f"data:image/png;base64,{encoded}"

            return None
        except Exception:
            return None

    def vision_chat(self, image, user_prompt: str):
        if self.client is None:
            return "❌ GEMINI_API_KEY topilmadi."

        try:
            if hasattr(image, "getvalue"):
                image_bytes = image.getvalue()
            else:
                image_bytes = image.read()

            image_part = types.Part.from_bytes(
                data=image_bytes, mime_type="image/jpeg"
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=[image_part, user_prompt],
                config=types.GenerateContentConfig(
                    system_instruction="Siz rasmni tahlil qiluvchi AI assistentisiz."
                ),
            )

            return response.text

        except Exception as e:
            return f"❌ Rasmni tahlil qilishda xatolik: {str(e)}"


ai = AIEngine()
