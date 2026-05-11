import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Jadwal Proyektor UNTIKA", layout="wide")

# --- 2. DATA JADWAL (KNOWLEDGE BASE) ---
SCHEDULE_DATA = """
JADWAL PENGGUNAAN PROYEKTOR MEI 2026 - FKIP UNTIKA LUWUK:
- 04 Mei (Monday): 07.30–10.00: Academic Reading (Anitha Thalib Mbau); 10.15–11.50: Language Learning Theories (Siti Rachmi); 12.30–15.00: Academic Writing Proficiency (Nurlaela); 15.15–16.55: Data Literacy (Nadya Septiani Rahman)
... (Sertakan seluruh data Mei Anda di sini agar AI tetap punya basis data) ...
"""

# --- 3. LOGIKA API KEY ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")

st.title("📽️ Sistem Jadwal Proyektor")
st.markdown("### Program Studi Bahasa Dan Kebudayaan Inggris - FKIP UNTIKA Luwuk")

# Diagnosa Model yang Tersedia
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Mencari semua model yang bisa digunakan untuk generateContent
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if models:
            st.sidebar.success(f"✅ API Key Aktif. Model tersedia: {len(models)}")
            # Pilih model secara cerdas (prioritas flash)
            selected_model = next((m for m in models if "flash" in m), models[0])
        else:
            st.sidebar.error("❌ API Key ini tidak memiliki akses ke model AI manapun.")
            st.stop()
    except Exception as e:
        st.sidebar.error(f"❌ Error Koneksi: {e}")
        st.stop()
else:
    st.sidebar.warning("⚠️ Harap masukkan API Key di Secrets Streamlit.")
    st.stop()

# --- 4. TAMPILAN PENCARIAN ---
col1, col2 = st.columns(2)
with col1:
    date_val = st.number_input("📅 Tanggal (Mei 2026):", 0, 31, 0)
with col2:
    lecturers = sorted(list(set(["Anitha Thalib Mbau", "Siti Rachmi", "Nurlaela", "Nadya Septiani Rahman", "Nurul Pratiwi", "Siti Medyanti Pawata", "Sukma Widya Sasmi Sabbu", "Srilidiawati Epa", "Anita Thalib Mbau"])))
    lect_val = st.selectbox("👤 Pilih Nama Dosen:", ["-- Abaikan --"] + lecturers)

if st.button("🔍 CARI JADWAL SEKARANG"):
    try:
        model = genai.GenerativeModel(selected_model)
        
        if date_val != 0 and lect_val == "-- Abaikan --":
            query = f"Tampilkan semua jadwal proyektor pada tanggal {date_val} Mei 2026."
        elif date_val == 0 and lect_val != "-- Abaikan --":
            query = f"Tampilkan semua jadwal dosen '{lect_val}' selama bulan Mei 2026."
        else:
            query = f"Tampilkan jadwal dosen '{lect_val}' pada tanggal {date_val} Mei 2026."

        prompt = f"Gunakan data ini:\n{SCHEDULE_DATA}\n\nInstruksi: {query}\nSajikan dalam TABEL Markdown (Tanggal, Jam, Matakuliah, Dosen)."

        with st.spinner(f"AI ({selected_model}) sedang memproses..."):
            response = model.generate_content(prompt)
            st.divider()
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses: {e}")

st.divider()
st.caption("© 2026 FKIP Universitas Tompotika Luwuk")
