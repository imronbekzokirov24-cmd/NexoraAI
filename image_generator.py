import os
import base64
from io import BytesIO

import streamlit as st
from openai import OpenAI
from PIL import Image


def get_openai_api_key():
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass

    return os.getenv("OPENAI_API_KEY")


def generate_image(
    prompt,
    size="1024x1024",
    quality="high",
):
    api_key = get_openai_api_key()

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY topilmadi. "
            "Streamlit Secrets ichiga OPENAI_API_KEY qo‘shing."
        )

    client = OpenAI(api_key=api_key)

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=size,
        quality=quality,
    )

    if not response.data:
        raise ValueError(
            "OpenAI API rasm qaytarmadi."
        )

    image_data = response.data[0].b64_json

    if not image_data:
        raise ValueError(
            "API'dan rasm ma'lumoti kelmadi."
        )

    image_bytes = base64.b64decode(image_data)

    image = Image.open(
        BytesIO(image_bytes)
    )

    return image


def save_image(
    image,
    filename="generated_image.png",
):
    image.save(
        filename,
        format="PNG",
    )

    return filename
