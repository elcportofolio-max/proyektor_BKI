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

# --- 3. ANTARMUKA UTAMA ---
st.title("📽️ Sistem Informasi Jadwal Proyektor")
st.markdown("##### Program Studi Bahasa Dan Kebudayaan Inggris - FKIP UNTIKA Luwuk")

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
            
            # --- SOLUSI KRUSIAL: PAKSA MODEL STABIL ---
            # Kita coba 'gemini-1.5-flash-latest' karena kuotanya 1.500 per hari
            model_name = "gemini-1.5-flash-latest"
            model = genai.GenerativeModel(model_name)

            query = f"Cari jadwal Mei 2026 untuk tanggal {date_val} dan dosen {lect_val}."

            prompt = f"Data:\n{SCHEDULE_DATA}\n\nInstruksi: {query}\nSajikan dalam tabel Markdown (Tanggal, Jam, Matakuliah, Dosen)."

            with st.spinner(f"AI sedang memproses..."):
                response = model.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
                
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ Kuota harian model baru habis (Limit 20). Silakan tunggu 24 jam atau buat API Key baru dengan akun Google lain.")
            elif "404" in str(e):
                # Jika 'latest' gagal, coba nama standar
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e2:
                    st.error(f"Gagal memanggil model AI: {e2}")
            else:
                st.error(f"Terjadi kesalahan: {e}")

st.divider()
st.caption("© 2026 Prodi Bahasa Dan Kebudayaan Inggris - UNTIKA Luwuk")
