# PawMatch: Aplikasi Web Rekomendasi Adopsi Anjing

PawMatch adalah aplikasi web berbasis Flask yang menghubungkan shelter dengan calon adopter anjing. Calon adopter mendapat rekomendasi anjing yang cocok dengan kondisi rumah dan waktu luangnya, sedangkan shelter mendapat analisis data untuk memprioritaskan promosi.

Proyek akhir mata kuliah Aplikasi Web.

## Fitur

- [x] Katalog anjing dengan label kelompok (clustering K-Means)
- [x] Cek kecocokan: rekomendasi anjing berdasarkan kondisi calon adopter
- [ ] Form pengajuan adopsi (disimpan ke SQLite)
- [ ] Chatbot rule-based untuk pertanyaan seputar adopsi
- [ ] Halaman admin: tambah anjing, kelola pengajuan, hasil analisis
- [ ] Prediksi lama adopsi (regresi linear, model sudah dilatih)
- [ ] Analisis sentimen deskripsi (VADER) dan tweet (InSet)

## Dataset

PetFinder.my Adoption Prediction, versi ringkas dari TensorFlow (`data/petfinder-mini.csv`).

- 11.537 profil adopsi hewan dari Malaysia, 6.601 di antaranya anjing
- Kolom: umur, ras, jenis kelamin, warna, ukuran, panjang bulu, vaksin, steril, kesehatan, biaya, deskripsi, jumlah foto, kecepatan adopsi (0–4)

Foto di katalog adalah **foto ilustrasi** dari [Dog CEO](https://dog.ceo/dog-api/) sesuai ras (dataset ringkas tidak menyertakan foto). Nama anjing diambil dari deskripsi kalau disebutkan.

Sumber:
- https://www.kaggle.com/c/petfinder-adoption-prediction
- https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers
- Foto ilustrasi: https://dog.ceo/dog-api/ (gambar dari Stanford Dogs Dataset dan kontributor)

## Struktur folder

```
pawmatch/
├── data/          dataset mentah dan hasil olahan
├── notebooks/     notebook cleaning, clustering, regresi, sentimen
├── models/        model hasil training (.joblib)
├── templates/     halaman HTML Flask
├── static/        CSS dan JavaScript
├── app.py         aplikasi Flask
├── rekomendasi.py logika skor kecocokan
├── foto.py        foto ilustrasi per ras dari Dog CEO
└── requirements.txt
```

## Menjalankan

Jalankan notebook 1 sampai 3 secara berurutan terlebih dahulu (menghasilkan `data/dogs_app.csv` dan model di `models/`), lalu:

```
python -m pip install -r requirements.txt
python app.py
```

## Progres

| Tahap | Isi | Status |
|---|---|---|
| 1 | Struktur proyek dan dataset | Selesai |
| 2 | Cleaning data (`notebooks/1_cleaning.ipynb`) | Selesai |
| 3 | Clustering (`notebooks/2_clustering.ipynb`) dan regresi (`notebooks/3_regresi.ipynb`) | Selesai |
| 4 | Flask: katalog, detail anjing, dan cek kecocokan | Selesai |
| 5 | SQLite dan pengajuan adopsi | Belum |
| 6 | Chatbot | Belum |
| 7 | Halaman admin dan sentimen | Belum |
| 8 | Crawling tweet dan FAQ | Belum |
