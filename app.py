"""Aplikasi web PawMatch (Flask).

Jalankan:
    python app.py
lalu buka http://127.0.0.1:5000
"""
import math
import re
from pathlib import Path

import pandas as pd
from flask import Flask, abort, render_template, request

from foto import foto_ilustrasi
from rekomendasi import PILIHAN, rekomendasikan

BASE_DIR = Path(__file__).resolve().parent
PER_HALAMAN = 24

app = Flask(__name__)


# Kata yang sering muncul di awal deskripsi tapi bukan nama anjing
BUKAN_NAMA = {
    "This", "He", "She", "It", "They", "We", "I", "My", "Our", "The", "Hi", "Hello",
    "Dear", "Please", "Puppy", "Puppies", "Dog", "Very", "Found", "Rescued", "Male",
    "Female", "Cute", "Friendly", "Lost", "Adopt", "For", "Looking", "Healthy",
    "Abandoned", "Stray", "Hey", "Good", "Mixed", "Black", "Brown", "White", "Local",
    "Just", "Pls", "Urgent", "Free", "Sweet", "Beautiful", "Active", "Playful", "Here",
    "There", "Mom", "Mother", "Sister", "Brother", "Not", "Name", "Adoption", "Fees",
}
POLA_AWAL = re.compile(
    r"^(?:Meet |Introducing |This is |Hi,? (?:I'?m|my name is) |Hello,? (?:I'?m|my name is) )?"
    r"([A-Z][a-z]{2,11})(?:\s+(?:is|was|has|loves|came|likes|had)\b|,)"
)
POLA_NAMA = re.compile(r"\b(?:name is|named|called)\s+([A-Z][a-z]{2,11})\b")


def ambil_nama(deskripsi):
    """Cari nama anjing di deskripsi, misalnya 'Peanut is a ...' atau 'named Ben'.

    Dataset tidak punya kolom nama, jadi nama diambil dari teks kalau ada.
    """
    teks = str(deskripsi).strip()
    for pola, cari in ((POLA_AWAL, POLA_AWAL.match), (POLA_NAMA, POLA_NAMA.search)):
        hasil = cari(teks)
        if hasil and hasil.group(1) not in BUKAN_NAMA:
            return hasil.group(1)
    return None


def muat_anjing():
    """Baca hasil notebook regresi. Profil berisi beberapa anjing tidak ditampilkan."""
    df = pd.read_csv(BASE_DIR / "data" / "dogs_app.csv")
    df = df[~df["grup"]].copy()
    nama = df["Description"].apply(ambil_nama)
    df["punya_nama"] = nama.notna()
    df["nama"] = nama.fillna("Anjing #" + df["anjing_id"].astype(str))
    df["umur_teks"] = df["Age"].apply(umur_ke_teks)
    df["ringkas"] = df["Description"].str.slice(0, 140) + "…"
    df["foto"] = [
        foto_ilustrasi(i, ras, teks)
        for i, ras, teks in zip(df["anjing_id"], df["Breed1"], df["Description"])
    ]
    # Anjing yang namanya diketahui ditampilkan lebih dulu di katalog
    return df.sort_values(["punya_nama", "anjing_id"], ascending=[False, True])


def umur_ke_teks(bulan):
    if bulan < 12:
        return f"{bulan} bln"
    tahun = bulan // 12
    return f"{tahun} thn"


ANJING = muat_anjing()
DAFTAR_ANJING = ANJING.to_dict(orient="records")
DAFTAR_CLUSTER = sorted(ANJING["cluster_label"].unique())
TERJEMAHAN = {
    "Small": "Kecil", "Medium": "Sedang", "Large": "Besar",
    "Short": "Pendek", "Long": "Panjang",
    "Yes": "Sudah", "No": "Belum", "Not Sure": "Belum diketahui",
    "Male": "Jantan", "Female": "Betina",
    "Healthy": "Sehat", "Minor Injury": "Luka ringan", "Serious Injury": "Luka serius",
}


@app.template_filter("id")
def ke_indonesia(teks):
    """Terjemahkan nilai kolom dataset ke Bahasa Indonesia untuk ditampilkan."""
    return TERJEMAHAN.get(teks, teks)


@app.route("/")
def beranda():
    ukuran = request.args.get("ukuran", "")
    kelompok = request.args.get("kelompok", "")
    halaman = max(request.args.get("halaman", 1, type=int), 1)

    data = ANJING
    if ukuran:
        data = data[data["MaturitySize"] == ukuran]
    if kelompok:
        data = data[data["cluster_label"] == kelompok]

    total_halaman = max(math.ceil(len(data) / PER_HALAMAN), 1)
    halaman = min(halaman, total_halaman)
    awal = (halaman - 1) * PER_HALAMAN
    anjing = data.iloc[awal:awal + PER_HALAMAN].to_dict(orient="records")

    return render_template(
        "index.html",
        anjing=anjing,
        jumlah=len(data),
        ukuran=ukuran,
        kelompok=kelompok,
        daftar_cluster=DAFTAR_CLUSTER,
        halaman=halaman,
        total_halaman=total_halaman,
    )


@app.route("/anjing/<int:anjing_id>")
def detail(anjing_id):
    baris = ANJING[ANJING["anjing_id"] == anjing_id]
    if baris.empty:
        abort(404)
    return render_template("detail.html", a=baris.iloc[0].to_dict())


@app.route("/cocok", methods=["GET", "POST"])
def cocok():
    if request.method == "GET":
        return render_template("cocok.html", pilihan=PILIHAN, jawaban={}, error=None)

    jawaban = {kunci: request.form.get(kunci, "") for kunci in PILIHAN}
    belum = [k for k, v in jawaban.items() if v not in PILIHAN[k]]
    if belum:
        return render_template(
            "cocok.html", pilihan=PILIHAN, jawaban=jawaban,
            error="Jawab keempat pertanyaan dulu, ya.",
        ), 400

    hasil = rekomendasikan(DAFTAR_ANJING, jawaban)
    ringkasan = {k: PILIHAN[k][v] for k, v in jawaban.items()}
    return render_template("hasil.html", hasil=hasil, ringkasan=ringkasan)


@app.errorhandler(404)
def tidak_ditemukan(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
