"""
Konstanta dan Pengaturan 
"""

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "Brewbound"

# --- PALET WARNA KHAS GROWTOPIA ---
# Dialog Utama Growtopia (Biru Laut Dalam dengan border Cyan Cerah)
GT_DIALOG_BG = (12, 50, 96)            # Biru khas popup Growtopia
GT_DIALOG_BG_DARK = (7, 29, 58)        # Bagian dalam gelap
GT_BORDER_OUTER = (3, 16, 33)          # Garis tepi luar paling gelap
GT_BORDER_CYAN = (65, 175, 245)        # Border cyan terang khas GT
GT_BORDER_HIGHLIGHT = (130, 215, 255)  # Sudut highlight berkilau
GT_BORDER_SHADOW = (18, 70, 130)       # Bayangan bevel bawah

# Tombol Bevel Growtopia (Gaya 3D timbul)
GT_BTN_BLUE = (25, 95, 175)
GT_BTN_BLUE_LIGHT = (50, 140, 235)
GT_BTN_BLUE_DARK = (12, 50, 105)

GT_BTN_GREEN = (45, 150, 55)
GT_BTN_GREEN_LIGHT = (75, 195, 85)
GT_BTN_GREEN_DARK = (22, 90, 30)

GT_BTN_RED = (185, 45, 45)
GT_BTN_RED_LIGHT = (230, 75, 75)
GT_BTN_RED_DARK = (110, 22, 22)

GT_SLOT_BG = (16, 35, 62)
GT_SLOT_BORDER = (40, 95, 160)
GT_SLOT_SELECTED = (255, 215, 0)       # Kuning keemasan saat slot aktif

# Warna Teks Chat & Dialog Growtopia
COLOR_TEXT_WHITE = (255, 255, 255)
COLOR_TEXT_YELLOW = (255, 235, 60)     # Kuning judul/sistem GT
COLOR_TEXT_MUTED = (170, 200, 230)     # Biru muda pudar
COLOR_TEXT_GOLD = (255, 205, 40)
COLOR_TEXT_RED = (255, 85, 85)
COLOR_TEXT_GREEN = (90, 245, 110)
COLOR_TEXT_CYAN = (80, 225, 255)

# Warna Elemen Bahan
COLOR_FIRE = (245, 85, 40)       # 🔥 Api
COLOR_WATER = (45, 175, 255)     # 💧 Air
COLOR_LEAF = (60, 215, 85)       # 🌿 Daun
COLOR_STONE = (180, 155, 125)    # 🪨 Batu

# Bar HP Growtopia Style
COLOR_HP_GREEN = (46, 204, 113)
COLOR_HP_RED = (231, 76, 60)
COLOR_HP_BG = (15, 22, 35)

# Simbol & Nama Elemen
ELEMENT_SYMBOLS = {
    "api": "🔥",
    "air": "💧",
    "daun": "🌿",
    "batu": "🪨"
}

ELEMENT_NAMES = {
    "api": "Bara Api",
    "air": "Embun Murni",
    "daun": "Herba Hijau",
    "batu": "Batu Runik"
}

ELEMENT_COLORS = {
    "api": COLOR_FIRE,
    "air": COLOR_WATER,
    "daun": COLOR_LEAF,
    "batu": COLOR_STONE
}

MAX_BAG_CAPACITY = 10
PLAYER_MAX_HP = 60

# Status State Game
STATE_MENU = "MENU"
STATE_EXPLORE = "EXPLORE"
STATE_BATTLE = "BATTLE"
STATE_RECIPE_BOOK = "RECIPE_BOOK"
STATE_STORAGE = "STORAGE"
STATE_VICTORY = "VICTORY"
