"""Sistem rekomendasi berbasis aturan (knowledge-based).

Setiap anjing mulai dari skor 100, lalu dikurangi kalau cirinya tidak cocok
dengan kondisi calon adopter. Hasil diurutkan dari skor tertinggi.
"""

WAKTU_KE_LEVEL = {"sedikit": 1, "sedang": 2, "banyak": 3}

PILIHAN = {
    "rumah": {
        "apt": "Apartemen atau kos",
        "rumah": "Rumah tanpa halaman",
        "halaman": "Rumah dengan halaman",
    },
    "waktu": {
        "sedikit": "Kurang dari 1 jam",
        "sedang": "1 sampai 3 jam",
        "banyak": "Lebih dari 3 jam",
    },
    "anak": {"ya": "Ada", "tidak": "Tidak ada"},
    "pengalaman": {"baru": "Ini yang pertama", "pernah": "Sudah pernah"},
}


def hitung_skor(anjing, jawaban):
    """Kembalikan (skor, alasan_cocok, catatan) untuk satu anjing."""
    skor = 100
    cocok = []
    catatan = []

    ukuran = anjing["ukuran_angka"]  # 1 kecil, 2 sedang, 3 besar
    energi = anjing["energi"]  # 1 rendah, 2 sedang, 3 tinggi

    # 1. Tempat tinggal
    if jawaban["rumah"] == "apt":
        if ukuran == 3:
            skor -= 30
            catatan.append("badannya besar untuk ruangan sempit")
        elif ukuran == 1:
            cocok.append("ukurannya pas untuk ruangan kecil")
    if energi == 3:
        if jawaban["rumah"] == "halaman":
            cocok.append("ada halaman untuk menyalurkan energinya")
        else:
            skor -= 12
            catatan.append("butuh ruang gerak lebih")

    # 2. Waktu luang dibandingkan tingkat energi
    selisih = abs(energi - WAKTU_KE_LEVEL[jawaban["waktu"]])
    if selisih == 0:
        cocok.append("tingkat energinya sesuai dengan waktu luangmu")
    else:
        skor -= 15 * selisih
        if energi > WAKTU_KE_LEVEL[jawaban["waktu"]]:
            catatan.append("butuh waktu main lebih banyak dari yang kamu punya")
        else:
            catatan.append("lebih santai dari ritme harianmu")

    # 3. Anak kecil
    if jawaban["anak"] == "ya":
        if anjing["ramah_anak"] == "Ya":
            cocok.append("ramah dengan anak kecil")
        elif anjing["ramah_anak"] == "Tidak":
            skor -= 35
            catatan.append("belum terbiasa dengan anak kecil")
        else:
            skor -= 10
            catatan.append("tanyakan ke shelter apakah cocok dengan anak kecil")

    # 4. Pengalaman memelihara
    if jawaban["pengalaman"] == "baru":
        if energi == 3 or ukuran == 3:
            skor -= 8
            catatan.append("lebih mudah untuk pemilik berpengalaman")
        else:
            cocok.append("mudah diurus untuk pemula")

    return max(5, min(98, skor)), cocok, catatan


def rekomendasikan(daftar_anjing, jawaban, jumlah=6):
    """Hitung skor semua anjing dan ambil yang tertinggi.

    Kalau skornya sama, anjing yang diprediksi lebih lama diadopsi (hasil regresi)
    ditaruh di depan, supaya anjing yang lama menunggu ikut mendapat kesempatan.
    """
    hasil = []
    for anjing in daftar_anjing:
        skor, cocok, catatan = hitung_skor(anjing, jawaban)
        hasil.append({**anjing, "skor": skor, "alasan": cocok[:2], "catatan": catatan[:2]})
    hasil.sort(key=lambda a: (a["skor"], a["prediksi_speed"]), reverse=True)
    return hasil[:jumlah]
