import streamlit as st
import os

st.set_page_config(page_title="Diagnosa Sistem", layout="centered")

# Cek keberadaan file requirements di server
st.write("### 🛠 Diagnosa Deployment")
if os.path.exists("requirements.txt"):
    st.success("✅ File requirements.txt ditemukan di server.")
    with open("requirements.txt", "r") as f:
        st.code(f.read(), language="text")
else:
    st.error("❌ File requirements.txt TIDAK DITEMUKAN di folder utama server!")

# Cek Library
try:
    import google.generativeai as genai
    st.success("✅ Library 'google-generativeai' berhasil terinstal!")
except ImportError:
    st.error("❌ Library 'google-generativeai' BELUM TERINSTAL.")
    st.info("Saran: Pastikan nama file di GitHub adalah 'requirements.txt' (pakai 's') dan berada di root folder.")
    st.stop()

# --- Jika Berhasil, Lanjutkan ke Aplikasi Utama ---
st.balloons()
st.title("📽️ Jadwal Proyektor UNTIKA")
# ... (masukkan sisa kode aplikasi Anda di sini) ...
