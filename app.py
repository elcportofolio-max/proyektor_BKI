if st.button("🔍 CARI JADWAL SEKARANG"):
    if not api_key:
        st.error("Sistem Error: API Key tidak ditemukan.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # --- SOLUSI KUOTA: PRIORITASKAN GEMINI 1.5 FLASH ---
            # Kita kunci ke 1.5-flash karena kuota gratisnya 1.500/hari
            # jauh lebih banyak daripada versi 2.x yang hanya 20/hari.
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Query Logic
            if date_val != 0 and lect_val == "-- Abaikan Nama Dosen --":
                query = f"Tampilkan semua jadwal proyektor pada tanggal {date_val} Mei 2026."
            elif date_val == 0 and lect_val != "-- Abaikan Nama Dosen --":
                query = f"Tampilkan semua jadwal untuk dosen '{lect_val}' selama Mei 2026."
            else:
                query = f"Tampilkan jadwal dosen '{lect_val}' pada tanggal {date_val} Mei 2026."

            prompt = f"Data:\n{SCHEDULE_DATA}\n\nPerintah: {query}\nSajikan dalam TABEL Markdown (Tanggal, Hari, Jam, Mata Kuliah)."

            with st.spinner("AI sedang memproses jadwal..."):
                response = model.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
                
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ Kuota harian habis. Mohon tunggu beberapa saat atau hubungi Admin IT untuk ganti API Key.")
            else:
                st.error(f"Terjadi kesalahan: {e}")
