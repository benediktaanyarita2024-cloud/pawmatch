# PawMatch: Aplikasi Web Rekomendasi Adopsi Anjing

PawMatch adalah aplikasi web berbasis Flask yang menghubungkan shelter dengan calon adopter anjing. Calon adopter mendapat rekomendasi anjing yang cocok dengan kondisi rumah dan waktu luangnya, sedangkan shelter mendapat analisis data untuk memprioritaskan promosi.

Proyek akhir mata kuliah Aplikasi Web.

## Fitur

- [ ] Katalog anjing dengan label kelompok (clustering K-Means)
- [ ] Cek kecocokan: rekomendasi anjing berdasarkan kondisi calon adopter
- [ ] Form pengajuan adopsi (disimpan ke SQLite)
- [ ] Chatbot rule-based untuk pertanyaan seputar adopsi
- [ ] Halaman admin: tambah anjing, kelola pengajuan, hasil analisis
- [ ] Prediksi lama adopsi (regresi linear)
- [ ] Analisis sentimen deskripsi (VADER) dan tweet (InSet)

## Dataset

PetFinder.my Adoption Prediction, versi ringkas dari TensorFlow (`data/petfinder-mini.csv`).

- 11.537 profil adopsi hewan dari Malaysia, 6.601 di antaranya anjing
- Kolom: umur, ras, jenis kelamin, warna, ukuran, panjang bulu, vaksin, steril, kesehatan, biaya, deskripsi, jumlah foto, kecepatan adopsi (0–4)

Sumber:
- https://www.kaggle.com/c/petfinder-adoption-prediction
- https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers

## Struktur folder

```
pawmatch/
├── data/          dataset mentah dan hasil olahan
├── notebooks/     notebook cleaning, clustering, regresi, sentimen
├── models/        model hasil training (.joblib)
├── templates/     halaman HTML Flask
├── static/        CSS dan JavaScript
├── app.py         aplikasi Flask (menyusul)
└── requirements.txt
```

## Menjalankan

```
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python app.py
```

## Progres

| Tahap | Isi | Status |
|---|---|---|
| 1 | Struktur proyek dan dataset | Selesai |
| 2 | Cleaning data | Selesai |
| 3 | Clustering dan regresi | Belum |
| 4 | Flask: katalog dan cek kecocokan | Belum |
| 5 | SQLite dan pengajuan adopsi | Belum |
| 6 | Chatbot | Belum |
| 7 | Halaman admin dan sentimen | Belum |
| 8 | Crawling tweet dan FAQ | Belum |
