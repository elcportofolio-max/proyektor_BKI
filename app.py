import streamlit as st
import google.generativeai as genai

# --- CONFIG ---
st.set_page_config(page_title="Proyektor UNTIKA", layout="centered")

# --- DATA JADWAL (Hanya cuplikan, pastikan versi Anda lengkap) ---
SCHEDULE_DATA = """
JADWAL PENGGUNAAN PROYEKTOR MEI 2026:
- 04 Mei (Monday): 07.30–10.00: Academic Reading (Anitha Thalib Mbau); 10.15–11.50: Language Learning Theories (Siti Rachmi); 12.30–15.00: Academic Writing Proficiency (Nurlaela); 15.15–16.55: Data Literacy (Nadya Septiani Rahman)
... (Sertakan seluruh data Mei Anda di sini) ...
"""

# --- AMBIL API KEY ---
# Kode ini akan memprioritaskan Secrets, jika kosong baru minta di sidebar
api_key = st.secrets.get("GOOGLE_API_KEY", "")

with st.sidebar:
    st.header("🔑 Koneksi AI")
    if api_key:
        st.success("API Key Terdeteksi di Secrets")
        # Opsi untuk menimpa jika ingin tes manual
        manual_key = st.text_input("Ganti Key Manual (Kosongkan jika pakai Secrets):", type="password")
        if manual_key:
            api_key = manual_key
    else:
        st.error("API Key Belum Diatur di Secrets!")
        api_key = st.text_input("Masukkan API Key Anda:", type="password")

# --- UI UTAMA ---
st.title("📽️ Jadwal Proyektor FKIP UNTIKA")
st.write("Sistem Informasi Penggunaan Media Pembelajaran")

col1, col2 = st.columns(2)
with col1:
    date_val = st.number_input("📅 Tanggal (Mei 2026):", 0, 31, 0)
with col2:
    lecturer_val = st.selectbox("👤 Pilih Dosen:", ["-- Abaikan --", "Anitha Thalib Mbau", "Siti Rachmi", "Nurlaela", "Nadya Septiani Rahman", "Nurul Pratiwi", "Siti Medyanti Pawata", "Sukma Widya Sasmi Sabbu", "Srilidiawati Epa"])

if st.button("🔍 CARI JADWAL"):
    if not api_key:
        st.error("Gagal: API Key tidak ditemukan. Masukkan kunci di sidebar atau Secrets!")
    else:
        try:
            # Konfigurasi AI
            genai.configure(api_key=api_key)
            
            # GUNAKAN 'gemini-1.5-flash' (MODEL PALING STABIL SAAT INI)
            # Hindari string '2.5' karena server sering menolak jika belum rilis publik penuh
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Prompt Logika
            query = f"Tampilkan jadwal Mei 2026 untuk tanggal {date_val} dan dosen {lecturer_val}."
            if date_val == 0: query = f"Tampilkan semua jadwal dosen {lecturer_val} selama Mei 2026."
            if lecturer_val == "-- Abaikan --": query = f"Tampilkan semua jadwal pada tanggal {date_val} Mei 2026."

            prompt = f"Gunakan data ini sebagai basis:\n{SCHEDULE_DATA}\n\nPerintah: {query}\nSajikan dalam tabel Markdown yang rapi."

            with st.spinner("AI sedang memproses data..."):
                response = model.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
            st.info("Tips: Jika muncul error 400, berarti API Key Anda sudah tidak berlaku atau salah ketik. Buatlah Key baru di Google AI Studio.")
