# app.py
"""
Enhanced Streamlit Qur'an Reader with Beautiful Background & Typography.
Features Added:
 - Elegant full-screen background (CSS)
 - Glassmorphism panels
 - Beautiful Arabic font (Amiri/MeQuran fallback)
 - Better spacing, colors, separators
 - Responsive layout
 - Smooth reading experience
"""
from pathlib import Path
import json
import streamlit as st
from typing import List, Dict
import io

# -------------------------
# Page Config with custom wide layout
# -------------------------
st.set_page_config(page_title="Qur'an Reader", layout="wide")

# -------------------------
# CUSTOM CSS (Background + Glass Effect + Fonts)
# -------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri&display=swap');
        body {
            background: url('https://images.unsplash.com/photo-1526401485004-2fda9f6d2f4a') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Amiri', serif;
        }
        .glass-box {
            background: rgba(255, 255, 255, 0.25);
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 4px 25px rgba(0,0,0,0.25);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }
        .arabic-text {
            font-family: 'Amiri', serif;
            font-size: 30px;
            line-height: 1.9;
            direction: rtl;
            text-align: right;
        }
        .ayah-number {
            background: rgba(0,0,0,0.4);
            color: white;
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 14px;
            margin-left: 6px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Load Qur'an Data
# -------------------------
@st.cache_data
def load_quran():
    try:
        import quran_module
        if hasattr(quran_module, "QURAN"):
            return quran_module.QURAN
        if hasattr(quran_module, "surahs"):
            return quran_module.surahs
    except:
        pass
    for p in Path('.').glob('quran-*.json'):
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
            if isinstance(data, dict) and 'surahs' in data:
                return data['surahs']
            if isinstance(data, list):
                return data
        except:
            continue
    return None

SURAHS = load_quran()
if SURAHS is None:
    st.error("⚠️ No Qur'an JSON or quran_module.py found. Please upload your file.")
    st.stop()

# -------------------------
# UI Layout with Glass Box Panels
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

    # Display Qur'an text
    if ayah_num:
        ay = surah['ayahs'][ayah_num - 1]
        st.markdown(f"<span class='ayah-number'>{ayah_num}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='arabic-text'>{ay['text']}</div>", unsafe_allow_html=True)
    else:
        for ay in surah['ayahs']:
            st.markdown(
                f"<span class='ayah-number'>{ay['numberInSurah']}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='arabic-text'>{ay['text']}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)
