"""Foto ilustrasi dari Dog CEO (https://dog.ceo/dog-api/).

Dataset PetFinder versi ringkas tidak menyertakan foto. Supaya katalog tidak
kosong, setiap anjing diberi FOTO ILUSTRASI sesuai rasnya:
1. Ras diambil dari kolom Breed1.
2. Kalau Breed1 = "Mixed Breed", dicari nama ras di deskripsi
   (misalnya "poodle mix" atau "a lab cross").
3. Kalau tetap tidak ketemu, dipakai foto anjing bertipe "anjing kampung"
   (dingo, kelpie, basenji) yang mirip anjing campuran pada umumnya.

Hanya foto dari Stanford Dogs Dataset (nama file diawali "n0") yang dipakai,
karena foto kiriman pengguna di Dog CEO tidak selalu bisa dimuat.

Daftar nama file foto per ras disimpan di data/dog_ceo_images.json, jadi
aplikasi tidak perlu memanggil API setiap kali halaman dibuka. Browser
langsung memuat gambar dari images.dog.ceo.
"""
import json
import re
from pathlib import Path

ALAMAT_GAMBAR = "https://images.dog.ceo/breeds/{folder}/{file}"

# Nama ras di dataset -> folder ras di Dog CEO
RAS_KE_FOLDER = {
    "Shih Tzu": ["shihtzu"],
    "Poodle": ["poodle-toy", "poodle-miniature", "poodle-standard"],
    "Labrador Retriever": ["labrador"],
    "Yellow Labrador Retriever": ["labrador"],
    "Black Labrador Retriever": ["labrador"],
    "Chocolate Labrador Retriever": ["labrador"],
    "Golden Retriever": ["retriever-golden"],
    "Retriever": ["retriever-golden", "retriever-flatcoated", "retriever-curly"],
    "Terrier": ["terrier-fox", "terrier-border", "terrier-cairn", "terrier-australian"],
    "German Shepherd Dog": ["german-shepherd"],
    "Shepherd": ["german-shepherd"],
    "Beagle": ["beagle"],
    "Spitz": ["samoyed"],
    "Rottweiler": ["rottweiler"],
    "Schnauzer": ["schnauzer", "schnauzer-miniature"],
    "Jack Russell Terrier": ["terrier-fox"],
    "Jack Russell Terrier (Parson Russell Terrier)": ["terrier-fox"],
    "Miniature Pinscher": ["pinscher-miniature"],
    "German Pinscher": ["pinscher-miniature"],
    "Doberman Pinscher": ["doberman"],
    "Cocker Spaniel": ["spaniel-cocker"],
    "English Cocker Spaniel": ["spaniel-cocker"],
    "Husky": ["husky"],
    "Siberian Husky": ["husky"],
        "Chihuahua": ["chihuahua"],
    "Silky Terrier": ["terrier-silky"],
    "Belgian Shepherd Malinois": ["malinois"],
        "Pomeranian": ["pomeranian"],
    "Pug": ["pug"],
    "Border Collie": ["collie-border"],
    "Collie": ["collie"],
    "Maltese": ["maltese"],
    "Pekingese": ["pekinese"],
    "Pit Bull Terrier": ["terrier-american"],
    "American Staffordshire Terrier": ["terrier-american"],
    "Corgi": ["pembroke"],
        "Basset Hound": ["hound-basset"],
    "Hound": ["hound-english", "hound-walker"],
    "Bullmastiff": ["mastiff-bull"],
    "Boxer": ["boxer"],
    "West Highland White Terrier Westie": ["terrier-westhighland"],
    "Basenji": ["basenji"],
    "English Bulldog": ["bulldog-french"],
    "French Bulldog": ["bulldog-french"],
    "Yorkshire Terrier Yorkie": ["terrier-yorkshire"],
    "Boston Terrier": ["bulldog-boston"],
    "Australian Terrier": ["terrier-australian"],
    "Australian Kelpie": ["kelpie"],
    "Toy Fox Terrier": ["terrier-toy"],
    "Great Dane": ["dane-great"],
    "Saint Bernard": ["stbernard"],
    "Weimaraner": ["weimaraner"],
}

# Ras yang tidak ada fotonya di Dog CEO
RAS_TANPA_FOTO = {"Dalmatian", "Dachshund", "Shar Pei"}

# Dipakai untuk anjing campuran yang rasnya tidak disebut
FOLDER_CAMPURAN = ["dingo", "kelpie", "basenji"]

# Kata di deskripsi -> folder (dipakai untuk anjing "Mixed Breed")
KATA_RAS = [
    (r"shih ?tzu", ["shihtzu"]),
    (r"poodle", ["poodle-toy", "poodle-miniature"]),
    (r"golden retriever|golden", ["retriever-golden"]),
    (r"labrador|\blab\b", ["labrador"]),
    (r"husky", ["husky"]),
    (r"german shepherd|\bgsd\b", ["german-shepherd"]),
    (r"beagle", ["beagle"]),
    (r"rottweiler", ["rottweiler"]),
        (r"chihuahua", ["chihuahua"]),
    (r"pomeranian", ["pomeranian"]),
    (r"schnauzer", ["schnauzer-miniature"]),
    (r"spitz", ["samoyed"]),
        (r"maltese", ["maltese"]),
    (r"corgi", ["pembroke"]),
    (r"doberman", ["doberman"]),
    (r"collie", ["collie-border"]),
    (r"\bpug\b", ["pug"]),
    (r"terrier", ["terrier-fox", "terrier-border"]),
]
KATA_RAS = [(re.compile(pola), folder) for pola, folder in KATA_RAS]

with open(Path(__file__).resolve().parent / "data" / "dog_ceo_images.json", encoding="utf-8") as f:
    DAFTAR_FOTO = json.load(f)


def pilih_folder(ras, deskripsi):
    """Tentukan folder ras Dog CEO untuk satu anjing.

    Ras yang tidak punya foto (misalnya Dalmatian, Dachshund, Shar Pei) tidak
    diberi foto ilustrasi, jadi kartunya menampilkan ikon anjing.
    """
    if ras in RAS_KE_FOLDER:
        return RAS_KE_FOLDER[ras]
    if ras in RAS_TANPA_FOTO:
        return []
    teks = str(deskripsi).lower()
    for pola, folder in KATA_RAS:
        if pola.search(teks):
            return folder
    return FOLDER_CAMPURAN


def foto_ilustrasi(anjing_id, ras, deskripsi):
    """Kembalikan alamat foto ilustrasi. Foto yang sama selalu dipilih untuk ID yang sama."""
    kandidat = [
        (folder, file)
        for folder in pilih_folder(ras, deskripsi)
        for file in DAFTAR_FOTO.get(folder, [])
    ]
    if not kandidat:
        return None
    folder, file = kandidat[anjing_id % len(kandidat)]
    return ALAMAT_GAMBAR.format(folder=folder, file=file)
