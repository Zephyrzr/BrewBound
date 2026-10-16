# 🧪 BrewBound

**Genre**: 2D Top-Down RPG & Turn-Based Elemental Battle  
**Engine**: Python 3.13 + Pygame 2.6  
**Style UI**: Sandbox(Beveled Blue Panels, Cyan Frames, Blocky Hotbar, Yellow Quantities)  

---

## 🌟 Fitur Baru di Versi Ini

### 1. 🎨 UI Bergaya Sandbox
* **Dialog Box Khas Game Sandbox(stardewvalley)**: Latar biru laut bergradasi gelap (`#0e3b6e` ke `#071f3d`), border cyan timbul (`#3fa2e6` dan highlight `#7ad0ff`), rivet sekrup sudut, dan tombol 3D bevel (Biru, Hijau, Merah).
* **Hotbar Ransel Kotak Khas GT**: Slot bahan kotak dengan efek kedalaman bayangan dan indikator kuantitas angka kuning (`#ffeb3b`) berbayang hitam di pojok kanan bawah.
* **Bar HP Arcade**: Tampilan bar HP bergaya arcade dengan persentase dan bar khusus ungu/emas untuk para Lord.

---

### 2. 🏃 Sistem Peluang Berhasil / Gagal Kabur (Flee Chance)
Senjata alkemis adalah racikan ramuan, namun ketika terdesak, pemain dapat mencoba melarikan diri dengan perhitungan peluang dinamis:

* **Musuh Biasa (Slime, Kelelawar, Katak)**: Dasar peluang kabur **65%**.
* **Efek Taktis**: Jika musuh terkena **Lumpur Pekat** (*Stun*) atau **Abu Kebutaan** (*Blind*), peluang kabur melonjak menjadi **85%**!
* **Boss Style LORD**: Peluang dasar kabur hanya **20%** (*"Sang Lord mengunci arena pertarungan!"*).
* **Konsekuensi Gagal Kabur**: Jika lemparan dadu gagal (`Roll > Chance`), **giliran pemain hangus** dan musuh **langsung melancarkan serangan gratis** ke arah pemain!

---

### 3. 👑 Boss Style LORD
Para boss area kini berwujud penguasa bermahkota megah dengan julukan para **LORD**:

1. **Area 1: LORD POHON PURBA: DVALIN**  
   * *Gelar*: Penguasa Hutan Gelap Purba  
   * *HP*: 120 | *Lemah*: 🔥 **Api**  
   * *Kutipan*: *"Hutan ini milikku! Nyala apimu takkan mampu menembus akar purbaku!"*
2. **Area 2: LORD GOLEM KRISTAL: BALTOR**  
   * *Gelar*: Kaisar Inti Kristal Abadi  
   * *HP*: 170 | *Lemah*: 💧 **Air**  
   * *Kutipan*: *"Tubuhku ditempa dari ribuan permata mineral! Air kalian hanya membasahi kulitku!"*
3. **Area 3: HIGH LORD RATU KABUT: VESPERA (FINAL BOSS)**  
   * *Gelar*: Ratu Tertinggi Kabut Kematian  
   * *HP*: 250 | *Lemah*: 🔥 **Api** dan 🪨 **Batu**  
   * *Kutipan*: *"Beraninya seorang murid fana menantang Yang Mulia! Seluruh desa akan tenggelam dalam kabutku!"*

#### ⚠️ Mekanisme Mode Amarah (Enraged Phase)
Bila HP sang Lord turun hingga **50% ke bawah**:
* Sang Lord memicu **MODE AMARAH SANG LORD** (*Enraged State*).
* Raungan boss (*Boss Roar*) bergema dan aura merah berapi menyelimuti tubuhnya.
* Daya serang sang Lord melonjak sebesar **+30%**!

---

## 🎮 Kontrol Permainan

| Tombol | Fungsi |
| :--- | :--- |
| **W, A, S, D** / **Panah** | Berjalan menjelajah desa dan peta area |
| **E** / **Spasi** | Ambil bahan panen / Interaksi kasur, peti, dan gerbang altar Lord |
| **1, 2, 3, 4** | Memilih bahan ke kuali racik (`1: Api`, `2: Air`, `3: Daun`, `4: Batu`) |
| **Spasi / Enter** | Racik ramuan dan serang musuh |
| **Esc** | Mencoba kabur dari pertarungan (Memperhitungkan % peluang) |
| **C** | Membersihkan slot kuali racik |
| **B** | Membuka / menutup Buku Resep |

---

## 🚀 Cara Menjalankan Game Pygame
Jalankan script `main.py` dari direktori proyek.

## 🌐 Menjalankan di Web dengan Pygbag

1. Pasang Pygbag dengan `py -m pip install pygbag`.
2. Buka terminal di direktori proyek, lalu jalankan `py -m pygbag --disable-sound-format-error --cdn https://pygame-web.github.io/archives/0.9/ .`.
3. Pygbag akan membuka game di browser lokal. Untuk membuat hasil build web statis, jalankan `py -m pygbag --disable-sound-format-error --cdn https://pygame-web.github.io/archives/0.9/ --build .`.
4. Unggah isi folder `build/web` ke layanan hosting statis.

File `main.py` menjalankan game sebagai loop `asyncio` agar browser tetap responsif. Emoji dirender dengan font Noto Emoji yang disertakan di `assets/fonts` agar terlihat pada browser tanpa mengandalkan font sistem. Build memakai arsip CDN Pygbag 0.9 agar dependensi browser filesystem tersedia. Musik menggunakan `assets/bgm.ogg` karena format OGG didukung Pygbag; file MP3 sumber tetap disimpan. Semua aset game harus tetap berada di dalam direktori proyek supaya ikut disertakan dalam build. Musik latar mulai diputar setelah pemain menekan Mulai, sesuai kebijakan autoplay browser.
