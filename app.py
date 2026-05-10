import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Sistem Proyektor FKIP UNTIKA",
    page_icon="📽️",
    layout="centered"
)

# --- DATA JADWAL (Knowledge Base) ---
SCHEDULE_DATA = """
JADWAL PENGGUNAAN PROYEKTOR MEI 2026 - PRODI BAHASA INGGRIS UNTIKA:
- 04 Mei (Monday): 07.30–10.00: Academic Reading (Anitha Thalib Mbau); 10.15–11.50: Language Learning Theories (Siti Rachmi); 12.30–15.00: Academic Writing Proficiency (Nurlaela); 15.15–16.55: Data Literacy (Nadya Septiani Rahman)
... (dst sesuai data sebelumnya) ...
"""

LECTURERS = ["Anitha Thalib Mbau", "Siti Rachmi", "Nurlaela", "Nadya Septiani Rahman", "Nurul Pratiwi", "Siti Medyanti Pawata", "Sukma Widya Sasmi Sabbu", "Srilidiawati Epa"]

# --- PENANGANAN API KEY ---
# Aplikasi akan mencoba mencari di 'Secrets' Streamlit terlebih dahulu, 
# jika tidak ada baru meminta input manual di sidebar.
api_key = st.sidebar.text_input("Google API Key:", type="password")
if not api_key:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]

# --- KONTEN UTAMA ---
st.title("📽️ Sistem Jadwal Proyektor")
st.write("Cari jadwal berdasarkan **Tanggal** atau **Nama Dosen**.")

col1, col2 = st.columns(2)
with col1:
    date_input = st.number_input("📅 Tanggal (Mei 2026):", 0, 31, 0)
with col2:
    lecturer_input = st.selectbox("👤 Nama Dosen:", ["-- Cari Semua Dosen --"] + sorted(list(set(LECTURERS))))

if st.button("🔍 TEMUKAN JADWAL"):
    if not api_key:
        st.error("Silakan masukkan API Key di sidebar atau konfigurasi Secrets!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            # Logika pencarian fleksibel
            if date_input != 0 and lecturer_input == "-- Cari Semua Dosen --":
                msg = f"Tampilkan semua jadwal proyektor pada tanggal {date_input} Mei 2026."
            elif date_input == 0 and lecturer_input != "-- Cari Semua Dosen --":
                msg = f"Tampilkan semua jadwal proyektor untuk dosen '{lecturer_input}' selama bulan Mei 2026."
            else:
                msg = f"Tampilkan jadwal proyektor untuk dosen '{lecturer_input}' pada tanggal {date_input} Mei 2026."

            prompt = f"Data:\n{SCHEDULE_DATA}\n\nTugas: {msg}\nSajikan dalam tabel Markdown (Tanggal, Jam, Matakuliah, Dosen)."

            with st.spinner("AI sedang memproses..."):
                response = model.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
