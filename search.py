import streamlit as str
from duckduckgo_search import DDGS


class SearchEngine:

    def search_context(self, query: str, max_results: int = 3) -> str:
        """Internetdan qidiruv amalga oshirib, matnli kontekst qaytaradi"""
        try:
            context_accumulator = ""
            
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                
                if not results:
                    return "Internetdan hech qanday ma'lumot topilmadi."
                
                for index, result in enumerate(results, 1):
                    title = result.get("title", "Sarlavha yo'q")
                    body = result.get("body", "Ma'lumot mavjud emas")
                    href = result.get("href", "")
                    
                    context_accumulator += (
                        f"Natija {index}:\n"
                        f"Mavzu: {title}\n"
                        f"Matn: {body}\n"
                        f"Havola: {href}\n\n"
                    )
            
            return context_accumulator.strip()

        except Exception as e:
            return f"Internetdan qidirishda xatolik yuz berdi: {str(e)}"


# Global instansiya
search = SearchEngine()
