import streamlit as st
import torch

from diffusers import AutoPipelineForText2Image


MODEL_ID = "stabilityai/sd-turbo"


@st.cache_resource
def load_model():

    if torch.cuda.is_available():

        device = "cuda"
        dtype = torch.float16

    else:

        device = "cpu"
        dtype = torch.float32

    pipe = AutoPipelineForText2Image.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
    )

    pipe = pipe.to(device)

    return pipe, device


def generate_image(
    prompt,
    size="1024x1024",
    quality="high",
):

    if not prompt or not prompt.strip():
        raise ValueError(
            "Rasm uchun prompt yozing."
        )

    pipe, device = load_model()

    sizes = {
        "1024x1024": (512, 512),
        "1536x1024": (512, 384),
        "1024x1536": (384, 512),
    }

    width, height = sizes.get(
        size,
        (512, 512)
    )

    with torch.inference_mode():

        result = pipe(
            prompt=prompt,
            width=width,
            height=height,
            num_inference_steps=4,
            guidance_scale=0.0,
        )

    if not result.images:
        raise ValueError(
            "AI rasm yaratmadi."
        )

    return result.images[0]


def save_image(
    image,
    filename="generated_image.png",
):

    image.save(
        filename,
        format="PNG",
    )

    return filename
