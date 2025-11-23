# app.py
"""
Arab Royal Palace + King's Palace Style
Ultra-Luxury Qur'an Reader UI
- Royal velvet-black fabric background
- Golden palace borders
- Shimmering gold glow
- Elegant Arabic font (Amiri)
- Deep royal red (maroon) palace shadows
- Glass gold panels
"""

import streamlit as st
from pathlib import Path
import json
import requests

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Luxury Qur'an", layout="wide")

# --------------------------------------------------
# CSS — Royal Palace + Kings Palace Mix
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri&display=swap');

/* FULL APP BACKGROUND — Velvet Royal Palace */
.stApp {
    background-image: url('https://i.imgur.com/Zn8F0iW.jpeg'); /* Royal black velvet fabric */
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    font-family: 'Amiri', serif;
    color: #FFD700;
}

/* GOLDEN GLASS PANEL */
.glass-box {
    background: rgba(0, 0, 0, 0.55);
    padding: 28px;
    border-radius: 18px;
    border: 2px solid #ffcc33;
    box-shadow:
        0 0 20px rgba(255, 215, 0, 0.4),
        inset 0 0 15px rgba(255, 215, 0, 0.15);
    backdrop-filter: blur(12px);
}

/* SURAH HEADER GOLD BAR */
.surah-header {
    background: linear-gradient(90deg, #8b0000, #d4af37, #8b0000);
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    color: #000;
}

/* ARABIC TEXT */
.arabic-text {
    font-size: 34px;
    line-height: 2.2;
    direction: rtl;
    text-align: right;
    color: #ffdd55;
    text-shadow: 0px 0px 8px rgba(255, 200, 80, 0.5);
}

/* AYAH NUMBER BADGE */
.ayah-number {
    background: #d4af37;
    color: black;
    padding: 5px 12px;
    font-weight: bold;
    border-radius: 10px;
    margin-left: 8px;
    font-size: 15px;
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.6);
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(90deg, #d4af37, #8b0000, #d4af37);
    color: black;
    border-radius: 10px;
    padding: 8px 15px;
    font-weight: bold;
    border: 2px solid #d4af37;
    box-shadow: 0 0 12px rgba(255, 215, 0, 0.7);
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Auto-Download Qur'an JSON if Missing
# --------------------------------------------------
QURAN_JSON = 'quran-uthmani.json'
API = 'https://api.alquran.cloud/v1/quran/uthmani'

if not Path(QURAN_JSON).exists():
    with st.spinner('Downloading Qur\'an...'):
        try:
            r = requests.get(API)
            r.raise_for_status()
            data = r.json()['data']['surahs']
            with open(QURAN_JSON, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            st.success('Download complete!')
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

# --------------------------------------------------
# Load Qur'an
# --------------------------------------------------
@st.cache_data
def load():
    return json.load(open(QURAN_JSON, 'r', encoding='utf-8'))

SURAHS = load()

# --------------------------------------------------
# Layout (Royal Right Side Display)
# --------------------------------------------------
left, right = st.columns([1, 2])

# LEFT SIDE — Controls
with left:
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.header("👑 Royal Qur'an Menu")

    surah_list = [f"{s['number']:03d} — {s['englishName']} ({len(s['ayahs'])} Ayat)" for s in SURAHS]
    sel = st.selectbox("Select Surah", surah_list)
    surah_num = int(sel.split('—')[0])

    mode = st.radio("Mode", ["Full Surah", "Single Ayah"])
    if mode == "Single Ayah":
        ayah_num = st.number_input("Ayah Number", min_value=1,
                                   max_value=len(SURAHS[surah_num - 1]['ayahs']), value=1)
    else:
        ayah_num = None

    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT SIDE — Royal Display
with right:
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)

    s = SURAHS[surah_num - 1]
    st.markdown(f"<div class='surah-header'>سورة {s['name']} — {s['englishName']}</div>", unsafe_allow_html=True)

    if ayah_num:
        ay = s['ayahs'][ayah_num - 1]
        st.markdown(f"<span class='ayah-number'>{ayah_num}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='arabic-text'>{ay['text']}</div>", unsafe_allow_html=True)

    else:
        for ay in s['ayahs']:
            st.markdown(f"<span class='ayah-number'>{ay['numberInSurah']}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='arabic-text'>{ay['text']}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
