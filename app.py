import streamlit as st
import os

# --- 1. PROTEKSI IMPORT ---
try:
    import google.generativeai as genai
    AI_READY = True
except ImportError:
    AI_READY = False

# --- 2. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Jadwal Proyektor FKIP UNTIKA", page_icon="📽️")

# --- 3. DATA JADWAL LENGKAP ---
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

# --- 4. LOGIKA UTAMA ---
st.title("📽️ Sistem Jadwal Proyektor")
st.write("Cari jadwal bulan Mei 2026")

# Ambil API Key dari Secrets
api_key = st.secrets.get("GOOGLE_API_KEY", "")

with st.sidebar:
    st.header("🔑 Status AI")
    if api_key:
        st.success("API Terpasang")
    else:
        st.warning("API Key belum diatur di Secrets")
        api_key = st.text_input("Masukan API Key Manual:", type="password")

if not AI_READY:
    st.error("Library AI belum terinstal sempurna. Mohon tunggu beberapa saat.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    date_val = st.number_input("📅 Tanggal (Mei 2026):", 0, 31, 0)
with col2:
    lecturers = sorted(list(set(["Anitha Thalib Mbau", "Siti Rachmi", "Nurlaela", "Nadya Septiani Rahman", "Nurul Pratiwi", "Siti Medyanti Pawata", "Sukma Widya Sasmi Sabbu", "Srilidiawati Epa", "Anita Thalib Mbau"])))
    lect_val = st.selectbox("👤 Pilih Nama Dosen:", ["-- Abaikan --"] + lecturers)

if st.button("🔍 CARI JADWAL SEKARANG"):
    if not api_key:
        st.error("API Key kosong!")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- BAGIAN SMART AUTO-DETECT MODEL ---
            # AI akan mencari model apa saja yang tersedia di akun Anda
            with st.spinner("Mendeteksi model AI yang aktif di akun Anda..."):
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                if not available_models:
                    st.error("Tidak ada model AI yang aktif pada API Key ini.")
                    st.stop()
                
                # Pilih model terbaik yang tersedia (mencari flash atau pro)
                # Jika ada gemini-2.0, gemini-1.5, atau gemini-pro, dia akan pilih salah satu.
                selected_model_name = available_models[0] # Ambil yang pertama tersedia
                model = genai.GenerativeModel(selected_model_name)
                st.caption(f"Menggunakan Model: {selected_model_name}")

            # Persiapan Query
            if date_val != 0 and lect_val == "-- Abaikan --":
                query = f"Tampilkan semua jadwal pada tanggal {date_val} Mei 2026."
            elif date_val == 0 and lect_val != "-- Abaikan --":
                query = f"Tampilkan semua jadwal untuk dosen '{lect_val}' selama Mei 2026."
            else:
                query = f"Tampilkan jadwal dosen '{lect_val}' pada tanggal {date_val} Mei 2026."

            prompt = f"Gunakan data ini:\n{SCHEDULE_DATA}\n\nInstruksi: {query}\nSajikan dalam TABEL Markdown yang rapi."

            with st.spinner("AI sedang menyusun tabel jadwal..."):
                response = model.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan AI: {e}")

st.divider()
st.caption("© 2026 Prodi Bahasa Dan Kebudayaan Inggris - UNTIKA Luwuk")
