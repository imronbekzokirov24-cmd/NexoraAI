import streamlit as st

# Sahifa sozlamalari
st.set_page_config(
    page_title="NexoraAI - Super Platforma", page_icon="🤖", layout="wide"
)

# Sarlavha
st.title("🤖 NexoraAI — Barchasi birida sun'iy intellekt")
st.write(
    "Siz istagan barcha sun'iy intellekt xizmatlari bitta joyda! Kerakli"
    " bo'limni tanlang."
)

# Yon panel (Sidebar) menyusi
menu = st.sidebar.selectbox(
    "Bo'limni tanlang:",
    [
        "🧠 Aqlli suhbat",
        "🌍 Tarjima qilish",
        "💡 G‘oyalar berish",
        "💻 Kod yozish",
    ],
)

# 1. Aqlli suhbat moduli
if menu == "🧠 Aqlli suhbat":
  st.header("🧠 Aqlli suhbat bilan muloqot")
  savol = st.text_input("Menga biror savol bering:")
  if st.button("Javob olish"):
    if savol:
      # Hozircha oddiy mantiq, keyinchalik buni API bilan ulaymiz
      st.success(
          f"NexoraAI javobi: Siz '{savol}' deb yordam so'radingiz. Tez orada"
          " to'liq sun'iy intellekt javobi ulanadi!"
      )
    else:
      st.warning("Iltimos, savol kiriting.")

# 2. Tarjima qilish moduli
elif menu == "🌍 Tarjima qilish":
  st.header("🌍 Matnni tarjima qilish")
  matn = st.text_area("Tarjima qilinadigan matnni kiriting:")
  til = st.selectbox(
      "Qaysi tilga tarjima qilamiz?", ["Ingliz tili", "Rus tili", "O'zbek tili"]
  )
  if st.button("Tarjima qilish"):
    st.info(
        f"('{matn}') matni tez orada {til}ga tarjima qilinadigan qilib"
        " sozlanadi."
    )

# 3. G'oyalar berish moduli
elif menu == "💡 G‘oyalar berish":
  st.header("💡 Loyoya yoki mavzu uchun g'oyalar")
  mavzu = st.text_input("Qaysi mavzuda g'oya kerak?")
  if st.button("G'oya topish"):
    st.write(
        f"'{mavzu}' bo'yicha eng zo'r g'oyalar ro'yxati tez orada bu yerda"
        " chiqadi!"
    )

# 4. Kod yozish moduli
elif menu == "💻 Kod yozish":
  st.header("💻 Kod yozish va tahlil qilish")
  dastur_tili = st.selectbox("Dasturlash tilini tanlang:", ["Python", "JavaScript", "C++"])
  vazifa = st.text_area("Qanday dastur kerakligini yozing:")
  if st.button("Kod generatsiya qilish"):
    st.code(
        f"# {dastur_tili} tilida '{vazifa}' uchun namuna kod\nprint('Salom,"
        " NexoraAI!')",
        language="python",
    )

# Pastki izoh
st.sidebar.markdown("---")
st.sidebar.info("NexoraAI v1.0 | Muallif: Imronbek")
