```python
import os
import base64
from io import BytesIO

from openai import OpenAI
from PIL import Image


# ==============================
# CONFIG
# ==============================

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError(
        "OPENAI_API_KEY topilmadi. "
        "Environment variable yoki Streamlit Secrets orqali API key qo'ying."
    )

client = OpenAI(api_key=API_KEY)


# ==============================
# IMAGE GENERATOR
# ==============================

def generate_image(
    prompt: str,
    size: str = "1024x1024",
):
    """
    Text prompt orqali rasm yaratadi.

    Args:
        prompt: Rasm uchun tavsif
        size: 1024x1024, 1536x1024 yoki 1024x1536

    Returns:
        PIL.Image.Image
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt bo'sh bo'lishi mumkin emas.")

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt.strip(),
        size=size,
    )

    image_base64 = response.data[0].b64_json

    image_bytes = base64.b64decode(image_base64)

    image = Image.open(BytesIO(image_bytes))

    return image


# ==============================
# SAVE IMAGE
# ==============================

def save_image(image, filename="generated_image.png"):
    """
    Yaratilgan PIL rasmini faylga saqlaydi.
    """

    image.save(filename)

    return filename


# ==============================
# IMAGE GENERATOR HELPER
# ==============================

def create_image(
    prompt: str,
    size: str = "1024x1024",
    filename: str = "generated_image.png",
):
    """
    Rasm yaratadi va faylga saqlaydi.
    """

    image = generate_image(
        prompt=prompt,
        size=size,
    )

    path = save_image(
        image,
        filename,
    )

    return image, path
```
