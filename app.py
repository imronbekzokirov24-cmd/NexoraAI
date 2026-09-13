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

# 1. Aqlli suhbat moduli (Enter bosganda ishlaydigan chat interfeysi)
if menu == "🧠 Aqlli suhbat":
  st.header("🧠 Aqlli suhbat bilan muloqot")

  # Xabarlarni saqlash uchun state
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # Oldingi xabarlarni ekranga chiqarish
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # Enter bosilganda ishlaydigan input
  if savol := st.chat_input("Menga biror savol bering..."):
    # Foydalanuvchi xabarini qo'shish
    st.session_state.messages.append({"role": "user", "content": savol})
    with st.chat_message("user"):
      st.markdown(savol)

    # Bot javobi (Hozircha vaqtinchalik javob, keyin API ulanadi)
    bot_javobi = (
        f"NexoraAI javobi: Siz '{savol}' deb yordam so'radingiz. Tez orada"
        " to'liq sun'iy intellekt javobi ulanadi!"
    )
    st.session_state.messages.append({"role": "assistant", "content": bot_javobi})
    with st.chat_message("assistant"):
      st.markdown(bot_javobi)

# 2. Tarjima qilish moduli
elif menu == "🌍 Tarjima qilish":
  st.header("🌍 Matnni tarjima qilish")
  matn = st.text_area("Tarjima qilinadigan matnni kiriting:")
  til = st.selectbox(
      "Qaysi tilga tarjima qilamiz?", ["Ingliz tili", "Rus tili", "O'zbek tili"]
  )
  if st.button("Tarjima qilish"):
    if matn.strip():
      st.info(
          f"('{matn}') matni tez orada {til}ga tarjima qilinadigan qilib"
          " sozlanadi."
      )
    else:
      st.warning("Iltimos, tarjima uchun matn kiriting.")

# 3. G'oyalar berish moduli
elif menu == "💡 G‘oyalar berish":
  st.header("💡 Loyiha yoki mavzu uchun g'oyalar")
  mavzu = st.text_input("Qaysi mavzuda g'oya kerak?")
  if st.button("G'oya topish"):
    if mavzu.strip():
      st.write(
          f"'{mavzu}' bo'yicha eng zo'r g'oyalar ro'yxati tez orada bu yerda"
          " chiqadi!"
      )
    else:
      st.warning("Iltimos, mavzu kiriting.")

# 4. Kod yozish moduli
elif menu == "💻 Kod yozish":
  st.header("💻 Kod yozish va tahlil qilish")
  dastur_tili = st.selectbox(
      "Dasturlash tilini tanlang:", ["Python", "JavaScript", "C++"]
  )
  vazifa = st.text_area("Qanday dastur kerakligini yozing:")
  if st.button("Kod generatsiya qilish"):
    if vazifa.strip():
      st.code(
          f"# {dastur_tili} tilida '{vazifa}' uchun namuna kod\nprint('Salom,"
          " NexoraAI!')",
          language="python",
      )
    else:
      st.warning("Iltimos, vazifani yozing.")

# Pastki izoh
st.sidebar.markdown("---")
st.sidebar.info("NexoraAI v1.0 | Muallif: Imronbek")
