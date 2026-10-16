"""
Sistem Resep dan Kombinasi Elemen
"""

# Resep ramuan lengkap (Kunci berupa tuple yang sudah diurutkan secara alfabetis)
RECIPES = {
    ("api", "api"): {
        "nama": "Bom Api",
        "elemen": "api",
        "damage": 28,
        "heal": 0,
        "deskripsi": "Ledakan api konsentrasi tinggi. Memberi damage api besar.",
        "tipe": "serangan",
        "efek_status": None,
        "icon": "💥"
    },
    ("air", "daun"): {
        "nama": "Tonik Hijau",
        "elemen": "daun",
        "damage": 0,
        "heal": 28,
        "deskripsi": "Cairan herba segar beraroma mint. Memulihkan 28 HP seketika.",
        "tipe": "pemulihan",
        "efek_status": None,
        "icon": "🧪"
    },
    ("air", "api"): {
        "nama": "Uap Panas",
        "elemen": "api",
        "damage": 18,
        "heal": 0,
        "deskripsi": "Semburan uap mendidih. Menghasilkan damage dan melemahkan serangan musuh sebesar 4 poin (2 giliran).",
        "tipe": "serangan",
        "efek_status": {"tipe": "atk_down", "nilai": 4, "durasi": 2},
        "icon": "♨️"
    },
    ("batu", "daun"): {
        "nama": "Kulit Batu",
        "elemen": "batu",
        "damage": 0,
        "heal": 0,
        "deskripsi": "Lapisan lumut dan batu keras melindungi tubuh. Mengurangi damage musuh sebesar 50% selama 2 giliran.",
        "tipe": "bertahan",
        "efek_status": {"tipe": "shield", "nilai": 0.5, "durasi": 2},
        "icon": "🛡️"
    },
    ("api", "batu"): {
        "nama": "Lava Pijar",
        "elemen": "api",
        "damage": 18,
        "heal": 0,
        "deskripsi": "Magma cair yang membara. Memberi 18 damage dan efek Terbakar (8 damage/giliran selama 2 giliran).",
        "tipe": "serangan",
        "efek_status": {"tipe": "burn", "damage": 8, "durasi": 2},
        "icon": "🌋"
    },
    ("air", "batu"): {
        "nama": "Lumpur Pekat",
        "elemen": "air",
        "damage": 12,
        "heal": 0,
        "deskripsi": "Lumpur tebal yang menjerat musuh. Memberi 12 damage dan membuat musuh MELEWATKAN 1 giliran (Stun).",
        "tipe": "serangan",
        "efek_status": {"tipe": "stun", "durasi": 1},
        "icon": "🫧"
    },
    ("air", "air"): {
        "nama": "Gelombang Murni",
        "elemen": "air",
        "damage": 22,
        "heal": 0,
        "deskripsi": "Arus air deras bertekanan tinggi. Memberikan damage berelemen air murni.",
        "tipe": "serangan",
        "efek_status": None,
        "icon": "🌊"
    },
    ("daun", "daun"): {
        "nama": "Akar Penyembuh",
        "elemen": "daun",
        "damage": 0,
        "heal": 16,
        "deskripsi": "Sari akar hutan. Memulihkan 16 HP dan memberi regenerasi +6 HP tiap giliran selama 2 giliran.",
        "tipe": "pemulihan",
        "efek_status": {"tipe": "regen", "nilai": 6, "durasi": 2},
        "icon": "🌱"
    },
    ("batu", "batu"): {
        "nama": "Longsor Mini",
        "elemen": "batu",
        "damage": 24,
        "heal": 0,
        "deskripsi": "Hantaman batu-batu berat yang dijatuhkan dari atas. Damage fisik bumi yang kuat.",
        "tipe": "serangan",
        "efek_status": None,
        "icon": "🪨"
    },
    ("api", "daun"): {
        "nama": "Abu Kebutaan",
        "elemen": "api",
        "damage": 16,
        "heal": 0,
        "deskripsi": "Asap dan debu herba terbakar. Memberi 16 damage dan membutakan musuh (akurasi musuh turun drastis selama 1 giliran).",
        "tipe": "serangan",
        "efek_status": {"tipe": "blind", "durasi": 1},
        "icon": "💨"
    }
}

def racik_ramuan(bahan1: str, bahan2: str) -> dict:
    """
    Menggabungkan dua bahan dasar menjadi ramuan.
    Urutan bahan tidak masalah karena otomatis diurutkan secara alfabetis.
    """
    kombinasi = tuple(sorted([bahan1.lower(), bahan2.lower()]))
    if kombinasi in RECIPES:
        resep = RECIPES[kombinasi].copy()
        resep["kombinasi"] = kombinasi
        return resep
    return {
        "nama": "Ramuan Gagal",
        "elemen": "netral",
        "damage": 5,
        "heal": 0,
        "deskripsi": "Campuran tidak stabil dan meledak kecil di wajahmu.",
        "tipe": "serangan",
        "efek_status": None,
        "kombinasi": kombinasi,
        "icon": "💨"
    }

def hitung_damage(ramuan: dict, musuh: dict) -> tuple[int, bool]:
    """
    Menghitung damage akhir berdasarkan kelemahan elemen musuh.
    Mengembalikan (damage_akhir, is_super_efektif).
    """
    base_dmg = ramuan.get("damage", 0)
    if base_dmg <= 0:
        return 0, False

    elemen_ramuan = ramuan.get("elemen", "")
    kelemahan_musuh = musuh.get("lemah", [])
    if isinstance(kelemahan_musuh, str):
        kelemahan_musuh = [kelemahan_musuh]

    if elemen_ramuan in kelemahan_musuh:
        damage_akhir = int(base_dmg * 1.6)
        return damage_akhir, True
    
    return base_dmg, False
