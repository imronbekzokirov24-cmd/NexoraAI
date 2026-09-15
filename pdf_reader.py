"""
============================================================
EduMindAI Enterprise v3.0
PDF Reader Engine (PyMuPDF)
============================================================
"""

import fitz  # PyMuPDF


class PDFReader:

    def __init__(self):
        pass

    # =====================================================
    # READ PDF
    # =====================================================

    def read_pdf(self, file) -> str:
        try:
            if hasattr(file, "seek"):
                file.seek(0)
            document = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page in document:
                text += page.get_text()
            document.close()
            return text
        except Exception:
            return ""

    # =====================================================
    # READ TXT
    # =====================================================

    def read_txt(self, file) -> str:
        try:
            if hasattr(file, "seek"):
                file.seek(0)
            return file.read().decode("utf-8", errors="ignore")
        except Exception:
            return ""

    # =====================================================
    # READ MULTIPLE FILES
    # =====================================================

    def read_multiple(self, files) -> str:
        if not files:
            return ""

        text = ""
        for file in files:
            extension = self.file_type(file)
            if extension == "pdf":
                text += f"\n--- [FAYL: {file.name}] ---\n" + self.read_pdf(file)
            elif extension == "txt":
                text += f"\n--- [FAYL: {file.name}] ---\n" + self.read_txt(file)
            text += "\n\n"

        return text.strip()

    # =====================================================
    # FILE TYPE
    # =====================================================

    def file_type(self, file) -> str:
        return file.name.split(".")[-1].lower()

    # =====================================================
    # FILE COUNT / PAGES
    # =====================================================

    def count_pages(self, file) -> int:
        try:
            if hasattr(file, "seek"):
                file.seek(0)
            document = fitz.open(stream=file.read(), filetype="pdf")
            pages = len(document)
            document.close()
            return pages
        except Exception:
            return 0

    # =====================================================
    # CHECK SUPPORT
    # =====================================================

    def is_supported(self, filename: str) -> bool:
        extension = filename.split(".")[-1].lower()
        return extension in ["pdf", "txt"]


# =====================================================
# PDF OBJECT INSTANCE
# =====================================================

pdf_reader = PDFReader()
