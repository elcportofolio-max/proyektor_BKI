import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Jadwal Proyektor FKIP UNTIKA",
    page_icon="📽️",
    layout="wide"
)

# Custom CSS untuk tampilan profesional Program Studi
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        height: 3.5em;
        width: 100%;
        font-weight: bold;
        font-size: 18px;
    }
    .main-header {
        color: #1E3A8A;
        text-align: center;
        font-family: 'Arial';
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA JADWAL (KNOWLEDGE BASE) ---
# Seluruh data dari PDF telah dimasukkan sebagai basis pengetahuan AI
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

# --- 3. LOGIKA AI (GEMINI 2.5 FLASH) ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")

# Inisialisasi Judul Utama
st.markdown("<h1 class='main-header'>📽️ Sistem Jadwal Proyektor</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Program Studi Bahasa Dan Kebudayaan Inggris - FKIP UNTIKA Luwuk</h5>", unsafe_allow_html=True)
st.divider()

# Daftar Dosen untuk Menu
dosen_list = sorted(list(set([
    "Anitha Thalib Mbau", "Siti Rachmi", "Nurlaela", "Nadya Septiani Rahman", 
    "Nurul Pratiwi", "Siti Medyanti Pawata", "Sukma Widya Sasmi Sabbu", 
    "Srilidiawati Epa", "Anita Thalib Mbau"
])))

# --- 4. ANTARMUKA PENCARIAN ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Cari Berdasarkan Tanggal**")
    date_val = st.number_input("Masukkan Tanggal Mei 2026 (0 = Semua):", 0, 31, 0)
with col2:
    st.markdown("**Cari Berdasarkan Dosen**")
    lect_val = st.selectbox("Pilih Nama Dosen:", ["-- Abaikan --"] + dosen_list)

# Eksekusi Pencarian
if st.button("🔍 TEMUKAN JADWAL"):
    if not api_key:
        st.error("API Key belum dikonfigurasi di Secrets.")
    elif date_val == 0 and lect_val == "-- Abaikan --":
        st.warning("Mohon tentukan Tanggal atau Nama Dosen untuk mencari.")
    else:
        try:
            # Konfigurasi model sesuai temuan user yang sukses
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')

            # Logika Filter Query
            if date_val != 0 and lect_val == "-- Abaikan --":
                query = f"Tampilkan semua jadwal proyektor pada tanggal {date_val} Mei 2026."
            elif date_val == 0 and lect_val != "-- Abaikan --":
                query = f"Daftar jadwal proyektor untuk dosen {lect_val} selama bulan Mei 2026."
            else:
                query = f"Cek jadwal dosen {lect_val} pada tanggal {date_val} Mei 2026."

            prompt = f"""
            Gunakan data jadwal ini:
            {SCHEDULE_DATA}

            Instruksi: {query}
            
            Sajikan dalam TABEL Markdown (Tanggal, Jam, Mata Kuliah, Dosen).
            Jika tidak ditemukan, beritahu bahwa jadwal kosong untuk kriteria tersebut.
            Gunakan Bahasa Indonesia yang sopan.
            """

            with st.spinner("AI sedang memproses informasi..."):
                response = model.generate_content(prompt)
                st.divider()
                st.subheader("📍 Hasil Pencarian Jadwal")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Terjadi kendala teknis: {e}")

# --- 5. FOOTER ---
st.divider()
st.markdown("<p style='text-align: center; color: grey;'>© 2026 Program Studi Bahasa Dan Kebudayaan Inggris - Universitas Tompotika Luwuk</p>", unsafe_allow_html=True)
