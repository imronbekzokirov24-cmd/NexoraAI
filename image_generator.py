import streamlit as st
import torch

from diffusers import AutoPipelineForText2Image


MODEL_ID = "stabilityai/sd-turbo"


@st.cache_resource
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    pipe = AutoPipelineForText2Image.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    )

    pipe = pipe.to(device)

    return pipe, device


def generate_image(
    prompt,
    size="1024x1024",
    quality="high",
):
    if not prompt or not prompt.strip():
        raise ValueError("Rasm uchun prompt yozing.")

    pipe, device = load_model()

    sizes = {
        "1024x1024": (1024, 1024),
        "1536x1024": (1536, 1024),
        "1024x1536": (1024, 1536),
    }

    width, height = sizes.get(
        size,
        (512, 512)
    )

    # SD-Turbo uchun kichikroq resolution ancha tezroq
    width = min(width, 512)
    height = min(height, 512)

    with torch.inference_mode():

        result = pipe(
            prompt=prompt,
            num_inference_steps=4,
            guidance_scale=0.0,
            width=width,
            height=height,
        )

    image = result.images[0]

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
