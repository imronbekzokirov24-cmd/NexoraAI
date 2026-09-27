import os
import io
import requests
import streamlit as st
from PIL import Image


def get_api_key():
    try:
        if "POLLINATIONS_API_KEY" in st.secrets:
            return st.secrets["POLLINATIONS_API_KEY"]
    except Exception:
        pass

    return os.getenv("POLLINATIONS_API_KEY")


def generate_image(
    prompt,
    size="1024x1024",
    quality="high"
):
    if not prompt or not prompt.strip():
        raise ValueError("Prompt yozing.")

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "POLLINATIONS_API_KEY topilmadi. "
            "Streamlit Secrets ga API key qo‘shing."
        )

    sizes = {
        "1024x1024": (1024, 1024),
        "1536x1024": (1536, 1024),
        "1024x1536": (1024, 1536),
    }

    width, height = sizes.get(size, (1024, 1024))

    url = "https://gen.pollinations.ai/image/" + requests.utils.quote(
        prompt.strip()
    )

    params = {
        "model": "flux",
        "width": width,
        "height": height,
        "nologo": "true",
    }

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=180
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Image API xatosi: {response.status_code}\n"
            f"{response.text[:1000]}"
        )

    image = Image.open(io.BytesIO(response.content))
    return image


def save_image(image, filename="nexora_generated.png"):
    image.save(filename, format="PNG")
    return filename
