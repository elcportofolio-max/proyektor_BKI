import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Jadwal Proyektor FKIP UNTIKA",
    page_icon="📽️",
    layout="wide"
)

# --- 2. DATA JADWAL (KNOWLEDGE BASE) ---
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

# --- 3. LOGIKA UTAMA ---
api_key = st.secrets.get("GOOGLE_API_KEY", "")

st.title("📽️ Jadwal Penggunaan Proyektor")
st.markdown("### Program Studi Bahasa Dan Kebudayaan Inggris - FKIP UNTIKA Luwuk")

# Input Pencarian
col1, col2 = st.columns(2)
with col1:
    date_val = st.number_input("📅 Masukkan Tanggal (Mei 2026):", 0, 31, 0)
with col2:
    lecturers = sorted(list(set([
        "Anitha Thalib Mbau", "Siti Rachmi", "Nurlaela", "Nadya Septiani Rahman", 
        "Nurul Pratiwi", "Siti Medyanti Pawata", "Sukma Widya Sasmi Sabbu", 
        "Srilidiawati Epa", "Anita Thalib Mbau"
    ])))
    lect_val = st.selectbox("👤 Pilih Nama Dosen:", ["-- Abaikan Nama Dosen --"] + lecturers)

if st.button("🔍 CARI JADWAL SEKARANG"):
    if not api_key:
        st.error("API Key tidak ditemukan di Secrets Streamlit.")
    elif date_val == 0 and lect_val == "-- Abaikan Nama Dosen --":
        st.warning("Mohon isi tanggal atau pilih nama dosen.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- SOLUSI 404: AUTO-TRY MULTIPLE MODELS ---
            model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-1.5-pro']
            model = None
            
            for name in model_names:
                try:
                    test_model = genai.GenerativeModel(name)
                    # Coba tes singkat apakah model merespon
                    test_model.generate_content("test", generation_config={"max_output_tokens": 1})
                    model = test_model
                    break # Berhenti jika berhasil
                except:
                    continue
            
            if model is None:
                st.error("❌ Tidak ada model Gemini yang merespon. Pastikan API Key Anda aktif di Google AI Studio.")
                st.stop()

            # Logika Filter Query
            if date_val != 0 and lect_val == "-- Abaikan Nama Dosen --":
                query = f"Tampilkan semua jadwal proyektor pada tanggal {date_val} Mei 2026."
            elif date_val == 0 and lect_val != "-- Abaikan Nama Dosen --":
                query = f"Tampilkan semua jadwal dosen '{lect_val}' selama bulan Mei 2026."
            else:
                query = f"Tampilkan jadwal dosen '{lect_val}' pada tanggal {date_val} Mei 2026."

            prompt = f"Gunakan data ini:\n{SCHEDULE_DATA}\n\nInstruksi: {query}\nSajikan dalam TABEL Markdown (Tanggal, Jam, Matakuliah, Dosen)."

            with st.spinner("AI sedang memproses jadwal..."):
                response = model.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# Footer
st.divider()
st.markdown("<p style='text-align: center;'>© 2026 Prodi Bahasa Dan Kebudayaan Inggris - Universitas Tompotika Luwuk</p>", unsafe_allow_html=True)
