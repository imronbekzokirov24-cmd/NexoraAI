from PIL import Image
import io


class VisionEngine:

    def prepare_image(self, uploaded_file):
        """Streamlit'dan kelgan rasm faylini PIL Image formatiga o'tkazish"""
        try:
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                return image
            return None
        except Exception as e:
            print(f"Rasm yuklash xatosi: {e}")
            return None


# Global instansiya
vision = VisionEngine()
