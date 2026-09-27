import os
import streamlit as st
from huggingface_hub import InferenceClient


def get_hf_token():
    # Streamlit Secrets
    try:
        if "HF_TOKEN" in st.secrets:
            return st.secrets["HF_TOKEN"]
    except Exception:
        pass

    # Environment variable
    return os.getenv("HF_TOKEN")


def generate_image(
    prompt,
    size="1024x1024",
    quality="high",
):
    token = get_hf_token()

    if not token:
        raise ValueError(
            "HF_TOKEN topilmadi. "
            "Streamlit Secrets ichiga HF_TOKEN qo‘shing."
        )

    client = InferenceClient(
        provider="auto",
        api_key=token,
    )

    # Sizning app.py dagi size qiymatini width/height ga aylantiramiz
    sizes = {
        "1024x1024": (1024, 1024),
        "1536x1024": (1536, 1024),
        "1024x1536": (1024, 1536),
    }

    width, height = sizes.get(
        size,
        (1024, 1024)
    )

    image = client.text_to_image(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell",
        width=width,
        height=height,
    )

    if image is None:
        raise ValueError(
            "Hugging Face rasm qaytarmadi."
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
