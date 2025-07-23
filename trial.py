import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os
import tempfile
import re
from datetime import datetime
import base64

# --- Page Setup ---
st.set_page_config(page_title="Even-Odd Multilingual Analyzer", layout="centered")

# --- Sidebar UI ---
st.sidebar.markdown("🎨 **Customize Appearance**")

# Language Selector (moved to sidebar)
language = st.sidebar.selectbox("🌐 Choose a language", [
    "English: en", "French: fr", "Spanish: es", "Dutch: de", "Italian: it", "Sweden: sw", "Japanese: ja", "Korean: ko", "Chineese: zh-cn", "Russian: ru", "Arabian: ar", "Portugese: pt"
])

# Translator & Translation Helper
translator = Translator()
def t(text):
    if language == "en":
        return text
    try:
        return translator.translate(text, dest=language).text
    except:
        return text

# Font Customization
font_size = st.sidebar.slider(t("Font Size"), 12, 60, 24)
text_colors = ['Red', 'Blue', 'Green', 'Purple', 'Orange', 'Yellow', 'Cyan', 'Magenta', 'Black', 'White']
text_color = st.sidebar.selectbox(t("Text Color"), text_colors, index=text_colors.index("Black"))
font_styles = ['Arial', 'Comic Sans MS', 'Courier New', 'Georgia', 'Impact', 'Tahoma', 'Times New Roman', 'Verdana']
font_family = st.sidebar.selectbox(t("Font Style"), font_styles)

# Voice Toggle
enable_voice = st.sidebar.checkbox(t("Enable Voice"), value=True)

# --- Music Playback ---
music_file = "ambient.mp3"
try:
    if os.path.exists(music_file):
        with open(music_file, "rb") as f:
            base64_music = base64.b64encode(f.read()).decode()
        music_html = f"""
        <audio autoplay loop>
        <source src="data:audio/mp3;base64,{base64_music}" type="audio/mp3">
        </audio>
        """
        st.markdown(music_html, unsafe_allow_html=True)
except Exception as e:
    st.warning(t("Ambient music couldn't be loaded."))

# --- Greeting Header ---
hour = datetime.now().hour
if hour < 12:
    greet = t("Good Morning")
elif hour < 18:
    greet = t("Good Afternoon")
else:
    greet = t("Good Evening")

st.markdown(f"<h1 style='text-align:center; color:{text_color.lower()}; font-family:{font_family}; font-size:{font_size + 10}px;'>🔢 {t('Even-Odd Multilingual Analyzer')}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{text_color.lower()}; font-family:{font_family}; font-size:{font_size}px;'>{greet} 👋</p>", unsafe_allow_html=True)

# --- Inputs ---
name = st.text_input(t("Enter your name:"))
number = st.text_input(t("Enter a number:"))

# --- Input Validation ---
if name:
    if name.isnumeric() or re.search(r'\d', name):
        st.error(t("Name must not contain numbers."))
        st.stop()

if number and not number.isnumeric():
    st.error(t("Number must be numeric."))
    st.stop()

# --- Analyze Button ---
if st.button("🔍 " + t("Analyze")):
    if name and number:
        num = int(number)
        result = t("even 🔵") if num % 2 == 0 else t("odd 🔺")
        result_text = f"{name}, {number} {t('is')} {result}"

        translated = translator.translate(result_text, dest=language).text
        st.markdown(f"<h3 style='color:{text_color.lower()}; font-family:{font_family}; font-size:{font_size}px;'>{translated}</h3>", unsafe_allow_html=True)

        # Voice
        if enable_voice:
            try:
                tts = gTTS(translated, lang=language)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts_path = fp.name
                    tts.save(tts_path)

                with open(tts_path, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
                
                os.remove(tts_path)
            except Exception as e:
                st.error(f"{t('Voice playback failed')}: {e}")

        st.balloons()

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color:{text_color.lower()}; font-family:{font_family}; font-size:{font_size - 4}px;'>{t('Made with ❤️ by Victor Ronaldinho')}</p>", unsafe_allow_html=True)
