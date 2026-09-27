import streamlit as st
from image_generator import generate_image

st.set_page_config(
    page_title="NexoraAI Image Generator",
    page_icon="🎨",
    layout="centered"
)

st.title("🎨 NexoraAI Image Generator")
st.write("Prompt yozing va AI rasm yaratadi.")

prompt = st.text_area(
    "📝 Rasm qanday bo‘lsin?",
    placeholder="Masalan: futuristic city at night, neon lights, realistic, 4K"
)

size = st.selectbox(
    "📐 Rasm o‘lchami",
    [
        "1024x1024",
        "1536x1024",
        "1024x1536"
    ]
)

if st.button("🎨 Rasm yaratish", use_container_width=True):

    if not prompt.strip():
        st.warning("Avval prompt yozing.")
    else:
        with st.spinner("AI rasm yaratmoqda..."):
            try:
                image = generate_image(
                    prompt=prompt,
                    size=size
                )

                st.success("✅ Rasm tayyor!")

                st.image(
                    image,
                    caption=prompt,
                    use_container_width=True
                )

                # Download
                import io

                buffer = io.BytesIO()
                image.save(buffer, format="PNG")

                st.download_button(
                    "⬇️ Rasmni yuklab olish",
                    data=buffer.getvalue(),
                    file_name="nexora_generated.png",
                    mime="image/png",
                    use_container_width=True
                )

            except Exception as e:
                st.error("❌ Xatolik yuz berdi:")
                st.code(str(e))
