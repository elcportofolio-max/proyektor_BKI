if st.button("🔍 CARI JADWAL"):
    if not api_key:
        st.error("API Key kosong. Silakan masukkan kunci di sidebar.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- STRATEGI CADANGAN MODEL ---
            # 1. Coba Flash Latest (Paling Cepat)
            # 2. Jika gagal, coba Pro (Paling Pintar)
            try:
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                st.write("⏱️ Menggunakan Model: Flash Latest")
            except:
                model = genai.GenerativeModel('gemini-pro')
                st.write("🧠 Menggunakan Model: Gemini Pro")
            
            # Logika Prompt
            if date_val != 0 and lect_val == "-- Abaikan --":
                query = f"Tampilkan semua jadwal proyektor pada tanggal {date_val} Mei 2026."
            elif date_val == 0 and lect_val != "-- Abaikan --":
                query = f"Tampilkan semua jadwal untuk dosen '{lect_val}' selama Mei 2026."
            else:
                query = f"Tampilkan jadwal dosen '{lect_val}' pada tanggal {date_val} Mei 2026."

            prompt = f"""
            Data Jadwal Resmi:
            {SCHEDULE_DATA}

            Instruksi: {query}
            Tampilkan dalam format tabel Markdown (Tanggal, Jam, Matakuliah, Dosen).
            Jika tidak ada jadwal, tulis: 'Mohon maaf, tidak ada jadwal untuk kriteria tersebut.'
            """

            with st.spinner("AI sedang menganalisis jadwal..."):
                response = model.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan AI: {e}")
