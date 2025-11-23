# app.py
"""
Luxury Black & Gold Streamlit Qur'an Reader with Auto-Download
Features:
 - Auto-download Qur'an JSON if missing
 - Elegant black background with gold text
 - Glassmorphism panels
 - Beautiful Arabic font (Amiri)
 - Single Ayah / Full Surah view
"""
from pathlib import Path
import json
import streamlit as st
from typing import List, Dict
import requests

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Qur'an Reader", layout="wide")

# -------------------------
# CSS Styling - Black & Gold Theme
# -------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri&display=swap');
        body {
            background-color: #000000;
            color: #FFD700;
            font-family: 'Amiri', serif;
        }
        .glass-box {
            background: rgba(0, 0, 0, 0.5);
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 4px 25px rgba(0,0,0,0.8);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid #FFD700;
        }
        .arabic-text {
            font-family: 'Amiri', serif;
            font-size: 32px;
            line-height: 2.0;
            direction: rtl;
            text-align: right;
            color: #FFD700;
        }
        .ayah-number {
            background: #FFD700;
            color: #000000;
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 14px;
            margin-left: 6px;
        }
        .stButton>button {
            background-color: #FFD700;
            color: #000000;
            border-radius: 12px;
            padding: 6px 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Auto-download Qur'an JSON if missing
# -------------------------
QURAN_JSON = 'quran-uthmani.json'
API_BASE = 'https://api.alquran.cloud/v1/quran/uthmani'

if not Path(QURAN_JSON).exists():
    with st.spinner('Qur\'an not found. Downloading automatically...'):
        try:
            resp = requests.get(API_BASE)
            resp.raise_for_status()
            data = resp.json().get('data', {}).get('surahs', [])
            with open(QURAN_JSON, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            st.success('Download complete!')
        except Exception as e:
            st.error(f'Failed to download Qur\'an: {e}')
            st.stop()

# -------------------------
# Load Qur'an
# -------------------------
@st.cache_data
def load_quran():
    with open(QURAN_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

SURAHS = load_quran()

# -------------------------
# UI Layout
# -------------------------
left, right = st.columns([1, 2])

with left:
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.header("📖 قرآن مجید")
    surah_info = [f"{s['number']:03d} — {s.get('englishName','')} ({len(s['ayahs'])} Ayat)" for s in SURAHS]
    surah_sel = st.selectbox("Select Surah / سورہ منتخب کریں", surah_info)
    surah_number = int(surah_sel.split('—')[0])
    choice = st.radio("View", ["Full Surah", "Single Ayah"])
    if choice == "Single Ayah":
        ayah_num = st.number_input("Ayah number", min_value=1, max_value=len(SURAHS[surah_number-1]['ayahs']), value=1)
    else:
        ayah_num = None
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    surah = SURAHS[surah_number-1]
    st.subheader(f"Surah {surah['number']}: {surah['englishName']}")
    st.write("---")

    if ayah_num:
        ay = surah['ayahs'][ayah_num - 1]
        st.markdown(f"<span class='ayah-number'>{ayah_num}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='arabic-text'>{ay['text']}</div>", unsafe_allow_html=True)
    else:
        for ay in surah['ayahs']:
            st.markdown(f"<span class='ayah-number'>{ay['numberInSurah']}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='arabic-text'>{ay['text']}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
