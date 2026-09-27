import os
import io
import requests
import streamlit as st
from PIL import Image


# ==========================================================
# POLLINATIONS API KEY
# ==========================================================

def get_api_key():
    # 1. Streamlit Cloud Secrets
    try:
        key = st.secrets.get("POLLINATIONS_API_KEY")

        if key:
            return str(key).strip()
    except Exception:
        pass

    # 2. Local environment variable
    key = os.getenv("POLLINATIONS_API_KEY")

    if key:
        return key.strip()

    return None


# ==========================================================
# IMAGE GENERATOR
# ==========================================================

def generate_image(
    prompt,
    size="1024x1024",
    quality="high"
):
    if not prompt or not prompt.strip():
        raise ValueError("Rasm uchun prompt yozing.")

    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "POLLINATIONS_API_KEY topilmadi.\n\n"
            "Streamlit Cloud → Manage app → Settings → Secrets "
            "ichiga POLLINATIONS_API_KEY qo‘shing."
        )

    # ------------------------------------------------------
    # Image size
    # ------------------------------------------------------

    sizes = {
        "1024x1024": (1024, 1024),
        "1536x1024": (1536, 1024),
        "1024x1536": (1024, 1536),
    }

    width, height = sizes.get(
        size,
        (1024, 1024)
    )

    # ------------------------------------------------------
    # Pollinations image URL
    # ------------------------------------------------------

    encoded_prompt = requests.utils.quote(
        prompt.strip()
    )

    url = (
        f"https://gen.pollinations.ai/image/"
        f"{encoded_prompt}"
    )

    # ------------------------------------------------------
    # Parameters
    # ------------------------------------------------------

    params = {
        "model": "flux",
        "width": width,
        "height": height,
        "nologo": "true",
    }

    # ------------------------------------------------------
    # Authentication
    # ------------------------------------------------------

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "image/*",
    }

    # ------------------------------------------------------
    # Request
    # ------------------------------------------------------

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=180
        )
    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Rasm yaratish vaqti tugadi. "
            "Qaytadan urinib ko‘ring."
        )

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Pollinations serveriga ulanishda xato:\n{e}"
        )

    # ------------------------------------------------------
    # API error
    # ------------------------------------------------------

    if response.status_code != 200:

        error_text = response.text[:1500]

        raise RuntimeError(
            f"Pollinations API xatosi: "
            f"{response.status_code}\n\n"
            f"{error_text}"
        )

    # ------------------------------------------------------
    # Convert response → PIL Image
    # ------------------------------------------------------

    try:
        image = Image.open(
            io.BytesIO(response.content)
        )

        image.load()

    except Exception:
        raise RuntimeError(
            "API rasm o‘rniga noto‘g‘ri ma'lumot qaytardi."
        )

    return image


# ==========================================================
# SAVE IMAGE
# ==========================================================

def save_image(
    image,
    filename="nexora_generated.png"
):
    image.save(
        filename,
        format="PNG"
    )

    return filename
