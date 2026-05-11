import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Jadwal Proyektor FKIP UNTIKA",
    page_icon="📽️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

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

# --- 3. ANTARMUKA UTAMA ---
st.title("📽️ Sistem Informasi Jadwal Proyektor")
st.markdown("##### Program Studi Bahasa Dan Kebudayaan Inggris - FKIP UNTIKA Luwuk")
st.divider()

# Ambil API Key dari Secrets
api_key = st.secrets.get("GOOGLE_API_KEY", "")

# Input Pencarian
col1, col2 = st.columns(2)
with col1:
    date_val = st.number_input("📅 Tanggal (0 = Lihat Semua):", 0, 31, 0)
with col2:
    dosen_list = sorted(list(set([
        "Anitha Thalib Mbau", "Siti Rachmi", "Nurlaela", "Nadya Septiani Rahman", 
        "Nurul Pratiwi", "Siti Medyanti Pawata", "Sukma Widya Sasmi Sabbu", 
        "Srilidiawati Epa", "Anita Thalib Mbau"
    ])))
    lect_val = st.selectbox("👤 Pilih Nama Dosen:", ["-- Abaikan Nama Dosen --"] + dosen_list)

if st.button("🔍 CARI JADWAL SEKARANG"):
    if not api_key:
        st.error("API Key belum diatur di Secrets Streamlit.")
    elif date_val == 0 and lect_val == "-- Abaikan Nama Dosen --":
        st.warning("Mohon tentukan Tanggal atau Nama Dosen.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # PAKSA MENGGUNAKAN 1.5 FLASH (KOTA 1.500/HARI)
            # Ini akan menghindari error 429 Limit 20/hari
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Query Logic
            if date_val != 0 and lect_val == "-- Abaikan Nama Dosen --":
                query = f"Tampilkan semua jadwal proyektor pada tanggal {date_val} Mei 2026."
            elif date_val == 0 and lect_val != "-- Abaikan Nama Dosen --":
                query = f"Daftar jadwal proyektor untuk dosen {lect_val} selama bulan Mei 2026."
            else:
                query = f"Cek jadwal dosen {lect_val} pada tanggal {date_val} Mei 2026."

            prompt = f"Gunakan data ini:\n{SCHEDULE_DATA}\n\nPerintah: {query}\nSajikan dalam TABEL Markdown (Tanggal, Jam, Mata Kuliah, Dosen)."

            with st.spinner("AI sedang memproses..."):
                response = model.generate_content(prompt)
                st.subheader("📍 Hasil Pencarian Jadwal")
                st.markdown(response.text)
                
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ Kuota harian model ini habis (Limit 20). Mohon ganti model ke Gemini 1.5 Flash di kode Python.")
            else:
                st.error(f"Terjadi kesalahan: {e}")

# Footer
st.divider()
st.markdown("<p style='text-align: center; color: grey;'>© 2026 Program Studi Bahasa Dan Kebudayaan Inggris - Universitas Tompotika Luwuk</p>", unsafe_allow_html=True)
