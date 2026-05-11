import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Jadwal Proyektor FKIP UNTIKA",
    page_icon="📽️",
    layout="wide"
)

# --- 2. DATA JADWAL MEI 2026 ---
SCHEDULE_DATA = """
JADWAL PENGGUNAAN PROYEKTOR MEI 2026 - FKIP UNTIKA LUWUK:
- 04 Mei (Monday): 07.30–10.00: Academic Reading (Anitha Thalib Mbau); 10.15–11.50: Language Learning Theories (Siti Rachmi); 12.30–15.00: Academic Writing Proficiency (Nurlaela); 15.15–16.55: Data Literacy (Nadya Septiani Rahman)
- 05 Mei (Tuesday): 07.30–10.00: English Translation (Nurul Pratiwi); 10.15–11.50: Technology-enhanced Language Instruction (Siti Medyanti Pawata); 12.30–15.00: Creative Writing (Nurul Pratiwi); 15.15–16.55: British/American Literature (Nadya Septiani Rahman)
- 06 Mei (Wednesday): 07.30–10.00: Data Literacy (Nadya Septiani Rahman); 10.15–11.50: Indonesian for Foreign Speakers (Siti Rachmi); 12.30–15.00: English Semantics and Pragmatics (Nurul Pratiwi); 15.15–16.55: Academic Reading Proficiency (Anitha Thalib Mbau)
- 07 Mei (Thursday): 07.30–10.00: Academic Speaking Proficiency (Siti Medyanti Pawata); 10.15–11.50: Paragraph Writing (Siti Medyanti Pawata); 12.30–15.00: Intermediate English Grammar (Sukma Widya Sasmi Sabbu); 15.15–16.55: Intermediate English Grammar (Sukma Widya Sasmi Sabbu)
- 08 Mei (Friday): 07.30–10.00: British/American Culture (Srilidiawati Epa); 10.15–11.50: English Semantics and Pragmatics (Nurul Pratiwi); 12.30–15.00: English Poetry and Prose (Nadya Septiani); 15.15–16.55: English Phonetics and Phonology (Siti Rachmi)
- 11 Mei (Monday): 07.30–10.00: British/American Culture (Siti Medyanti Pawata); 10.15–11.50: English Popular Culture (Srilidiawati Epa); 12.30–15.00: Language Learning Theories (Siti Rachmi); 15.15–16.55: Oral Communication Skills (Anitha Thalib Mbau)
- 12 Mei (Tuesday): 07.30–10.00: Contextual English Words (Srilidiawati Epa); 10.15–11.50: British/American Literature (Nadya Septiani Rahman); 12.30–15.00: Creative Writing (Nurul Pratiwi); 15.15–16.55: Second Language Acquisition (Sukma Widya Sasmi Sabbu)
- 13 Mei (Wednesday): 07.30–10.00: Academic Reading (Anitha Thalib Mbau); 10.15–11.50: English Poetry and Prose (Nadya Septiani Rahman); 12.30–15.00: English Semantics and Pragmatics (Nurul Pratiwi); 15.15–16.55: Second Language Acquisition (Sukma Widya Sasmi Sabbu)
- 18 Mei (Monday): 07.30–10.00: British/American Culture (Srilidiawati Epa); 10.15–11.50: Paragraph Writing (Siti Medyanti Pawata); 12.30–15.00: Academic Writing Proficiency (Nurlaela); 15.15–16.55: Academic Listening Proficiency (Sukma Widya Sasmi Sabbu)
- 19 Mei (Tuesday): 07.30–10.00: Oral Communication Skills (Anitha Thalib Mbau); 10.15–11.50: Contextual English Words (Srilidiawati Epa); 12.30–15.00: Creative Writing (Nurul Pratiwi); 15.15–16.55: Literary and Cultural Studies (Srilidiawati Epa)
- 20 Mei (Wednesday): 07.30–10.00: Data Literacy (Nadya Septiani Rahman); 10.15–11.50: Indonesian for Foreign Speakers (Siti Rachmi); 12.30–15.00: English Semantics and Pragmatics (Nurul Pratiwi); 15.15–16.55: Academic Reading Proficiency (Anitha Thalib Mbau)
- 21 Mei (Thursday): 07.30–10.00: Scientific Reading (Anitha Thalib Mbau); 10.15–11.50: English Translation (Nurul Pratiwi); 12.30–15.00: Research Methods on Language and Culture (Nurlaela); 15.15–16.55: Intermediate English Grammar (Sukma Widya Sasmi Sabbu)
- 22 Mei (Friday): 07.30–10.00: British/American Culture (Srilidiawati Epa); 10.15–11.50: Scientific Reading (Anita Thalib Mbau); 12.30–15.00: English Poetry and Prose (Nadya Septiani); 15.15–16.55: English Phonetics and Phonology (Siti Rachmi)
- 25 Mei (Monday): 07.30–10.00: Academic Reading (Anitha Thalib Mbau); 10.15–11.50: Language Learning Theories (Siti Rachmi); 12.30–15.00: Language Learning Theories (Siti Rachmi); 15.15–16.55: Data Literacy (Nadya Septiani)
- 26 Mei (Tuesday): 07.30–10.00: English Translation (Nurul Pratiwi); 10.15–11.50: Technology-enhanced Language Instruction (Siti Medyanti Pawata); 12.30–15.00: Creative Writing (Nurul Pratiwi); 15.15–16.55: British/American Literature (Nadya Septiani Rahman)
- 29 Mei (Friday): 07.30–10.00: British/American Culture (Srilidiawati Epa); 10.15–11.50: Film Studies (Nadya Septiani Rahman); 12.30–15.00: English Poetry and Prose (Nadya Septiani); 15.15–16.55: English Phonetics and Phonology (Siti Rachmi)
"""

# --- 3. DETEKSI MODEL ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")

st.title("📽️ Sistem Informasi Jadwal Proyektor")
st.markdown("##### FKIP UNTIKA Luwuk")

available_models = []
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Ambil daftar model yang bisa digunakan untuk teks
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Filter: Hapus model internal/robotics/preview yang bermasalah
        valid_models = [m for m in available_models if "robotics" not in m and "preview" not in m]
        
        # Cari model flash (prioritas 1.5)
        default_model = next((m for m in valid_models if "1.5" in m and "flash" in m), None)
        if not default_model:
            default_model = next((m for m in valid_models if "flash" in m), valid_models[0] if valid_models else None)
    except Exception as e:
        st.error(f"Koneksi API Gagal: {e}")
        st.stop()
else:
    st.error("API Key belum diatur di Secrets Streamlit.")
    st.stop()

# Tampilkan Pilihan Model di Sidebar jika ingin ganti manual
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    selected_model = st.selectbox("Model yang Digunakan:", available_models, index=available_models.index(default_model) if default_model in available_models else 0)
    st.info("Pilih model lain jika model saat ini memberikan error 404.")

# --- 4. ANTARMUKA PENCARIAN ---
col1, col2 = st.columns(2)
with col1:
    date_val = st.number_input("📅 Tanggal (Mei 2026):", 0, 31, 0)
with col2:
    dosen_list = sorted(list(set(["Anitha Thalib Mbau", "Siti Rachmi", "Nurlaela", "Nadya Septiani Rahman", "Nurul Pratiwi", "Siti Medyanti Pawata", "Sukma Widya Sasmi Sabbu", "Srilidiawati Epa", "Anita Thalib Mbau"])))
    lect_val = st.selectbox("👤 Pilih Nama Dosen:", ["-- Abaikan --"] + dosen_list)

if st.button("🔍 CARI JADWAL SEKARANG"):
    try:
        model = genai.GenerativeModel(selected_model)
        
        # Penentuan Query
        if date_val != 0 and lect_val == "-- Abaikan --":
            query = f"Daftar jadwal proyektor tanggal {date_val} Mei 2026."
        elif date_val == 0 and lect_val != "-- Abaikan --":
            query = f"Daftar semua jadwal untuk dosen {lect_val} selama bulan Mei 2026."
        else:
            query = f"Jadwal dosen {lect_val} pada tanggal {date_val} Mei 2026."

        prompt = f"Data Basis:\n{SCHEDULE_DATA}\n\nPerintah: {query}\nSajikan dalam TABEL Markdown yang rapi."

        with st.spinner(f"Memproses menggunakan {selected_model}..."):
            response = model.generate_content(prompt)
            st.divider()
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"Kesalahan: {e}")
        st.info("Coba ganti model di menu sebelah kiri (sidebar) dan klik cari lagi.")

st.divider()
st.caption("© 2026 Prodi Bahasa Dan Kebudayaan Inggris - UNTIKA Luwuk")
