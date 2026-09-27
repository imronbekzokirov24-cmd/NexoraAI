# image_generator.py

import os
import base64
from io import BytesIO

from openai import OpenAI
from PIL import Image


# ==========================================================
# CONFIG
# ==========================================================

def get_api_key():
    """
    OPENAI_API_KEY ni avval environment variable'dan,
    keyin Streamlit Secrets'dan olishga harakat qiladi.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        return api_key

    try:
        import streamlit as st

        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]

    except Exception:
        pass

    return None


API_KEY = get_api_key()


if not API_KEY:
    raise ValueError(
        "OPENAI_API_KEY topilmadi.\n\n"
        "Streamlit Secrets yoki environment variable "
        "orqali OPENAI_API_KEY qo'shing."
    )


# ==========================================================
# OPENAI CLIENT
# ==========================================================

client = OpenAI(
    api_key=API_KEY
)


# ==========================================================
# SETTINGS
# ==========================================================

IMAGE_MODEL = "gpt-image-2"

VALID_SIZES = [
    "1024x1024",
    "1536x1024",
    "1024x1536",
]

VALID_QUALITIES = [
    "low",
    "medium",
    "high",
]


# ==========================================================
# GENERATE IMAGE
# ==========================================================

def generate_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "high",
):
    """
    Text prompt orqali AI rasm yaratadi.

    Args:
        prompt: Rasm tavsifi
        size: 1024x1024 / 1536x1024 / 1024x1536
        quality: low / medium / high

    Returns:
        PIL.Image.Image
    """

    # ------------------------------------------------------
    # PROMPT CHECK
    # ------------------------------------------------------

    if not prompt:
        raise ValueError(
            "Prompt bo'sh bo'lishi mumkin emas."
        )

    prompt = prompt.strip()

    if not prompt:
        raise ValueError(
            "Prompt bo'sh bo'lishi mumkin emas."
        )


    # ------------------------------------------------------
    # SIZE CHECK
    # ------------------------------------------------------

    if size not in VALID_SIZES:
        size = "1024x1024"


    # ------------------------------------------------------
    # QUALITY CHECK
    # ------------------------------------------------------

    if quality not in VALID_QUALITIES:
        quality = "high"


    # ------------------------------------------------------
    # API REQUEST
    # ------------------------------------------------------

    response = client.images.generate(
        model=IMAGE_MODEL,
        prompt=prompt,
        size=size,
        quality=quality,
    )


    # ------------------------------------------------------
    # RESPONSE CHECK
    # ------------------------------------------------------

    if not response.data:
        raise RuntimeError(
            "Image API hech qanday rasm qaytarmadi."
        )


    image_data = response.data[0]


    # ------------------------------------------------------
    # BASE64
    # ------------------------------------------------------

    if not getattr(image_data, "b64_json", None):
        raise RuntimeError(
            "Image API'dan b64_json olinmadi."
        )


    image_base64 = image_data.b64_json


    # ------------------------------------------------------
    # DECODE
    # ------------------------------------------------------

    try:

        image_bytes = base64.b64decode(
            image_base64
        )

    except Exception as e:

        raise RuntimeError(
            f"Rasm ma'lumotlarini decode qilishda xato: {e}"
        )


    # ------------------------------------------------------
    # PIL IMAGE
    # ------------------------------------------------------

    try:

        image = Image.open(
            BytesIO(image_bytes)
        )

        image.load()

    except Exception as e:

        raise RuntimeError(
            f"Rasmni ochishda xato: {e}"
        )


    return image


# ==========================================================
# SAVE IMAGE
# ==========================================================

def save_image(
    image,
    filename: str = "generated_image.png",
):
    """
    PIL Image'ni PNG faylga saqlaydi.
    """

    if image is None:
        raise ValueError(
            "Saqlash uchun image berilmagan."
        )


    image.save(
        filename,
        format="PNG",
    )


    return filename


# ==========================================================
# CREATE + SAVE
# ==========================================================

def create_image(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "high",
    filename: str = "generated_image.png",
):
    """
    Rasm yaratadi va PNG sifatida saqlaydi.

    Returns:
        image, filename
    """

    image = generate_image(
        prompt=prompt,
        size=size,
        quality=quality,
    )


    path = save_image(
        image=image,
        filename=filename,
    )


    return image, path


# ==========================================================
# SIMPLE TEST
# ==========================================================

if __name__ == "__main__":

    test_prompt = (
        "A futuristic city at night, "
        "cinematic lighting, rainy streets, "
        "beautiful skyscrapers, ultra detailed"
    )


    print("🎨 Rasm yaratilmoqda...")


    image, path = create_image(
        prompt=test_prompt,
        size="1024x1024",
        quality="high",
        filename="test_generated_image.png",
    )


    print(
        f"✅ Rasm tayyor: {path}"
    )
