import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Jadwal Proyektor UNTIKA Luwuk",
    page_icon="📽️",
    layout="centered"
)

# --- 2. DATA JADWAL LENGKAP (KNOWLEDGE BASE) ---
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

# Daftar Dosen untuk Menu Dropdown
LECTURERS = sorted(list(set([
    "Anitha Thalib Mbau", "Siti Rachmi", "Nurlaela", "Nadya Septiani Rahman", 
    "Nurul Pratiwi", "Siti Medyanti Pawata", "Sukma Widya Sasmi Sabbu", 
    "Srilidiawati Epa", "Anita Thalib Mbau"
])))

# --- 3. LOGIKA API KEY ---
# Mengambil dari Streamlit Secrets atau Sidebar
api_key_env = st.secrets.get("GOOGLE_API_KEY", "")
api_key_side = st.sidebar.text_input("Ganti API Key (Jika perlu):", value=api_key_env, type="password")
final_api_key = api_key_side if api_key_side else api_key_env

with st.sidebar:
    if final_api_key:
        st.success("✅ API Key Terpasang")
    else:
        st.error("❌ API Key Belum Ada")
    st.info("Model: Gemini 1.5 Flash")

# --- 4. TAMPILAN UTAMA ---
st.title("📽️ Cek Jadwal Proyektor")
st.markdown("Pusat Informasi Penggunaan In Focus - **FKIP UNTIKA Luwuk**")

# Input Pencarian
col1, col2 = st.columns(2)
with col1:
    date_input = st.number_input("📅 Pilih Tanggal (Mei 2026):", 0, 31, 0, help="Isi 0 jika ingin mencari semua tanggal.")
with col2:
    lect_input = st.selectbox("👤 Pilih Nama Dosen:", ["-- Abaikan Nama Dosen --"] + LECTURERS)

# Tombol Eksekusi
if st.button("🔍 TEMUKAN JADWAL"):
    if not final_api_key:
        st.error("Silakan masukkan API Key terlebih dahulu!")
    elif date_input == 0 and lect_input == "-- Abaikan Nama Dosen --":
        st.warning("Mohon isi minimal satu kriteria pencarian (Tanggal atau Dosen).")
    else:
        try:
            # Konfigurasi AI
            genai.configure(api_key=final_api_key)
            # Menggunakan 1.5-flash karena 2.5-flash belum rilis resmi
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Membuat logika pencarian
            if date_input != 0 and lect_input == "-- Abaikan Nama Dosen --":
                search_query = f"Daftar jadwal proyektor pada tanggal {date_input} Mei 2026."
            elif date_input == 0 and lect_input != "-- Abaikan Nama Dosen --":
                search_query = f"Semua jadwal penggunaan proyektor untuk dosen {lect_input} selama Mei 2026."
            else:
                search_query = f"Jadwal dosen {lect_input} khusus pada tanggal {date_input} Mei 2026."

            prompt = f"""
            Gunakan data jadwal ini sebagai referensi tunggal:
            {SCHEDULE_DATA}

            Perintah: {search_query}
            
            Aturan Jawaban:
            1. Jika ada, sajikan dalam TABEL Markdown: Tanggal | Jam | Matakuliah | Dosen.
            2. Jika tidak ada jadwal, beritahu dengan sopan bahwa jadwal tidak ditemukan.
            3. Gunakan Bahasa Indonesia yang formal.
            """

            with st.spinner("Mencari data di jadwal resmi..."):
                response = model.generate_content(prompt)
                st.divider()
                st.subheader("📍 Hasil Pencarian")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan teknis: {e}")

# --- 5. FOOTER ---
st.divider()
st.caption("© 2026 Prodi Bahasa Dan Kebudayaan Inggris - Universitas Tompotika Luwuk")
