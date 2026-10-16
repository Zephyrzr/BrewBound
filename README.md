# 🧪 BrewBound

**Genre**: 2D Top-Down RPG & Turn-Based Elemental Battle  
**Engine**: Python 3.13 + Pygame 2.6 + Pygbag
**Style UI**: Sandbox(Beveled Blue Panels, Cyan Frames, Blocky Hotbar, Yellow Quantities)  

---

## 🌟 Fitur

### 1. 🎨 UI
* **Dialog Box Khas Game Sandbox**
* **Hotbar Ransel Kotak**
* **Bar HP Arcade**

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
