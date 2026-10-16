"""
Sistem Pertarungan Turn-Based (Battle System)
"""

import pygame
import random
import math
from constants import (
    GT_DIALOG_BG, GT_DIALOG_BG_DARK, GT_BORDER_OUTER, GT_BORDER_CYAN,
    GT_BORDER_HIGHLIGHT, GT_BORDER_SHADOW, GT_SLOT_BG, GT_SLOT_BORDER,
    GT_SLOT_SELECTED, COLOR_TEXT_WHITE, COLOR_TEXT_YELLOW, COLOR_TEXT_MUTED,
    COLOR_TEXT_GOLD, COLOR_TEXT_RED, COLOR_TEXT_GREEN, COLOR_TEXT_CYAN,
    COLOR_FIRE, COLOR_WATER, COLOR_LEAF, COLOR_STONE,
    ELEMENT_COLORS, ELEMENT_NAMES, ELEMENT_SYMBOLS
)
from recipes import racik_ramuan, hitung_damage
from ui import Button, HealthBar, FloatingText, draw_gt_dialog
from audio import audio
from sprites import StardewSpriteCache

# Database Musuh & Boss Gaya LORD
ENEMIES_DATA = {
    "slime": {
        "nama": "Slime Lumut",
        "area": 1,
        "hp": 35,
        "lemah": ["api"],
        "atk": 9,
        "is_boss": False,
        "drop": ["daun", "air"],
        "deskripsi": "Makhluk berlendir dari hutan berkabut. Sangat mudah terbakar."
    },
    "pohon_tua": {
        "nama": "LORD POHON PURBA: DVALIN",
        "area": 1,
        "hp": 120,
        "lemah": ["api"],
        "atk": 16,
        "is_boss": True,
        "lord_title": "Penguasa Hutan Gelap Purba",
        "intro_quote": "Hutan ini milikku! Nyala apimu takkan mampu menembus akar purbaku!",
        "drop": ["daun", "api", "batu"],
        "deskripsi": "Lord pepohonan kuno bermahkota duri emas. Menyerap energi gelap kabut."
    },
    "kelelawar": {
        "nama": "Kelelawar Batu",
        "area": 2,
        "hp": 50,
        "lemah": ["air"],
        "atk": 13,
        "is_boss": False,
        "drop": ["batu", "air"],
        "deskripsi": "Kelelawar bersayap mineral tajam. Rapuh terhadap erosi air murni."
    },
    "golem": {
        "nama": "LORD GOLEM KRISTAL: BALTOR",
        "area": 2,
        "hp": 170,
        "lemah": ["air"],
        "atk": 20,
        "is_boss": True,
        "lord_title": "Kaisar Inti Kristal Abadi",
        "intro_quote": "Tubuhku ditempa dari ribuan permata mineral! Air kalian hanya membasahi kulitku!",
        "drop": ["batu", "batu", "air"],
        "deskripsi": "Overlord raksasa berbaju zirah kristal runik bercahaya ungu kramat."
    },
    "katak": {
        "nama": "Katak Racun",
        "area": 3,
        "hp": 65,
        "lemah": ["api", "batu"],
        "atk": 16,
        "is_boss": False,
        "drop": ["daun", "batu"],
        "deskripsi": "Amfibi rawa bertaring racun asam ungu pekat."
    },
    "ratu_kabut": {
        "nama": "HIGH LORD RATU KABUT: VESPERA",
        "area": 3,
        "hp": 250,
        "lemah": ["api", "batu"],
        "atk": 24,
        "is_boss": True,
        "lord_title": "Ratu Tertinggi Kabut Kematian",
        "intro_quote": "Beraninya seorang murid fana menantang Yang Mulia! Seluruh desa akan tenggelam dalam kabutku!",
        "drop": ["api", "air", "daun", "batu"],
        "deskripsi": "Penguasa sejati kabut kutukan berkubah mahkota intan hitam dan mantel kegelapan."
    }
}

class BattleManager:
    def __init__(self, player, enemy_key: str):
        self.player = player
        self.enemy_key = enemy_key
        data = ENEMIES_DATA[enemy_key].copy()
        from entities import Enemy
        self.enemy = Enemy(data)

        # Health bar bergaya Growtopia (Boss memiliki Bar Khusus)
        if self.enemy.is_boss:
            self.enemy_hp_bar = HealthBar((580, 80, 270, 24), self.enemy.max_hp, self.enemy.hp, is_boss=True)
        else:
            self.enemy_hp_bar = HealthBar((620, 85, 230, 22), self.enemy.max_hp, self.enemy.hp)
            
        self.player_hp_bar = HealthBar((110, 85, 230, 22), player.max_hp, player.hp)

        # Slot Kuali Racik
        self.slot1 = None
        self.slot2 = None

        # State Pertarungan
        # "PLAYER_TURN", "BREWING", "ENEMY_TURN", "VICTORY", "DEFEAT", "FLED"
        self.state = "PLAYER_TURN"
        self.turn_timer = 0
        self.battle_log = f"[SISTEM] Memulai pertempuran melawan {self.enemy.nama}!"
        self.log_color = COLOR_TEXT_YELLOW

        # Efek Visual & Animasi
        self.floating_texts = []
        self.shake_screen = 0
        self.anim_tick = 0
        self.enemy_flash = 0
        self.player_flash = 0

        # Mekanisme Lord Boss: Mode Amarah (Enraged Phase saat HP <= 50%)
        self.is_enraged = False
        if self.enemy.is_boss:
            audio.play("boss_roar")
            self.battle_log = f"[LORD] {data.get('intro_quote', '')}"
            self.log_color = COLOR_TEXT_RED

        # Buff Pemain
        self.player_shield_turns = 0
        self.player_regen_turns = 0
        self.player_regen_val = 0

        # Drop loot & resep baru
        self.loot_result = []
        self.new_recipe_unlocked = None

        self._init_buttons()

    def calculate_flee_chance(self) -> int:
        """
        Menghitung peluang (%) berhasil kabur:
        - Musuh biasa: dasar 65%
        - Jika musuh terkena Stun (Lumpur) atau Buta (Abu): +20% bonus kabur (85%)
        - Boss (Lord): dasar hanya 20% (arena terkunci aura Lord!)
        """
        if self.enemy.is_boss:
            base_chance = 20
        else:
            base_chance = 65

        if self.enemy.stunned_turns > 0 or self.enemy.blind_turns > 0:
            base_chance += 20

        return max(5, min(95, base_chance))

    def _init_buttons(self):
        # 4 Tombol Elemen di Panel Kanan sesuai Mockup Resmi
        # Api, Air, Daun, Batu menggunakan ukuran kotak 48x48
        btn_size = 50
        spacing = 10
        btn_start_x = 645
        btn_y = 398

        self.btn_elements = {}
        elements = ["api", "air", "daun", "batu"]
        shortcuts = ["1", "2", "3", "4"]

        for i, elem in enumerate(elements):
            x = btn_start_x + i * (btn_size + spacing)
            self.btn_elements[elem] = Button(
                (x, btn_y, btn_size, btn_size),
                "",
                callback=lambda e=elem: self.select_ingredient(e),
                color_theme="blue",
                shortcut=shortcuts[i]
            )

        # Tombol Aksi Racik, Batal, Kabur
        self.btn_brew = Button(
            (368, 466, 175, 42),
            "✨ Racik Ramuan",
            callback=self.execute_player_attack,
            color_theme="green",
            shortcut="[Spasi]"
        )

        self.btn_clear = Button(
            (555, 466, 95, 42),
            "Batal",
            callback=self.clear_slots,
            color_theme="blue",
            shortcut="[C]"
        )

        flee_chance = self.calculate_flee_chance()
        self.btn_flee = Button(
            (660, 466, 115, 42),
            f"🏃 Kabur ({flee_chance}%)",
            callback=self.attempt_flee,
            color_theme="red",
            shortcut="[Esc]"
        )

    def select_ingredient(self, elem: str):
        if self.state != "PLAYER_TURN":
            return

        needed = 1
        if self.slot1 == elem:
            needed += 1
        if self.player.bag.get(elem, 0) < needed:
            audio.play("click")
            self.add_floating_text("Bahan di Tas Habis!", (self.player_hp_bar.rect.centerx, 260), COLOR_TEXT_RED)
            return

        audio.play("select")
        if self.slot1 is None:
            self.slot1 = elem
        elif self.slot2 is None:
            self.slot2 = elem
        else:
            self.slot2 = elem

    def clear_slots(self):
        self.slot1 = None
        self.slot2 = None

    def attempt_flee(self):
        """
        Sistem Chance Kabur:
        Jika Berhasil -> Kembali ke desa tanpa penalti.
        Jika Gagal -> Giliran pemain terbuang, musuh langsung membalas menyerang!
        """
        if self.state != "PLAYER_TURN":
            return

        chance = self.calculate_flee_chance()
        roll = random.randint(1, 100)

        if roll <= chance:
            # BERHASIL KABUR!
            audio.play("flee_success")
            self.battle_log = f"[KABUR] 💨 Berhasil Kabur! ({roll}% <= {chance}%) Kamu lolos dari {self.enemy.nama}!"
            self.log_color = COLOR_TEXT_GREEN
            self.add_floating_text("BERHASIL KABUR!", (300, 240), COLOR_TEXT_GREEN, size=28)
            self.state = "FLED"
        else:
            # GAGAL KABUR!
            audio.play("flee_fail")
            self.battle_log = f"[ALERT] ❌ Gagal Kabur! ({roll}% > {chance}%) {self.enemy.nama} menghadang jalanmu!"
            self.log_color = COLOR_TEXT_RED
            self.add_floating_text("GAGAL KABUR!", (220, 220), COLOR_TEXT_RED, size=28)
            self.clear_slots()

            # Penalti: Giliran pemain hangus, langsung giliran musuh menyerang!
            self.state = "ENEMY_TURN"
            self.turn_timer = 45

    def get_current_recipe_preview(self):
        if self.slot1 and self.slot2:
            return racik_ramuan(self.slot1, self.slot2)
        return None

    def execute_player_attack(self):
        if self.state != "PLAYER_TURN":
            return
        if not self.slot1 or not self.slot2:
            self.add_floating_text("Pilih 2 Bahan Dulu!", (480, 420), COLOR_TEXT_YELLOW)
            return

        self.player.remove_from_bag(self.slot1, 1)
        self.player.remove_from_bag(self.slot2, 1)

        ramuan = racik_ramuan(self.slot1, self.slot2)
        kombinasi = ramuan["kombinasi"]

        if kombinasi not in self.player.unlocked_recipes:
            self.player.unlocked_recipes.add(kombinasi)
            self.new_recipe_unlocked = ramuan["nama"]

        self.state = "BREWING"
        self.turn_timer = 35
        audio.play("brew")

        if ramuan["tipe"] == "serangan":
            dmg, is_super = hitung_damage(ramuan, {"lemah": self.enemy.lemah})
            self.enemy.hp = max(0, self.enemy.hp - dmg)
            self.enemy_hp_bar.set_hp(self.enemy.hp)
            self.enemy_flash = 12
            self.shake_screen = 9 if is_super else 5

            if is_super:
                audio.play("crit")
                self.add_floating_text(f"SUPER EFEKTIF! -{dmg}", (680, 200), COLOR_TEXT_YELLOW, size=30)
                self.battle_log = f"[CRIT] 💥 {ramuan['nama']} SANGAT EFEKTIF! {dmg} damage menghantam {self.enemy.nama}!"
                self.log_color = COLOR_TEXT_YELLOW
            else:
                audio.play("hit")
                self.add_floating_text(f"-{dmg}", (720, 220), COLOR_TEXT_RED, size=24)
                self.battle_log = f"[SERANG] {ramuan['nama']} menghasilkan {dmg} damage ke musuh."
                self.log_color = COLOR_TEXT_WHITE

            if ramuan.get("efek_status"):
                self.enemy.apply_status(ramuan["efek_status"])

        elif ramuan["tipe"] == "pemulihan":
            heal_val = ramuan.get("heal", 20)
            self.player.hp = min(self.player.max_hp, self.player.hp + heal_val)
            self.player_hp_bar.set_hp(self.player.hp)
            self.player_flash = 10
            audio.play("heal")
            self.add_floating_text(f"+{heal_val} HP", (160, 220), COLOR_TEXT_GREEN, size=26)
            self.battle_log = f"[HEAL] 🌿 Kamu meminum {ramuan['nama']}! Pulih +{heal_val} HP."
            self.log_color = COLOR_TEXT_GREEN

            if ramuan.get("efek_status") and ramuan["efek_status"]["tipe"] == "regen":
                self.player_regen_turns = ramuan["efek_status"]["durasi"]
                self.player_regen_val = ramuan["efek_status"]["nilai"]

        elif ramuan["tipe"] == "bertahan":
            if ramuan.get("efek_status") and ramuan["efek_status"]["tipe"] == "shield":
                self.player_shield_turns = ramuan["efek_status"]["durasi"]
                audio.play("select")
                self.add_floating_text("PERISAI BATU AKTIF!", (160, 220), COLOR_TEXT_CYAN, size=24)
                self.battle_log = f"[BUFF] 🛡️ {ramuan['nama']} melapisi tubuhmu! Pertahanan naik 50%."
                self.log_color = COLOR_TEXT_CYAN

        # Cek apakah Lord Boss memasuki Mode Amarah (Enraged)
        if self.enemy.is_boss and not self.is_enraged and self.enemy.hp <= (self.enemy.max_hp * 0.5):
            self.is_enraged = True
            self.enemy.atk = int(self.enemy.atk * 1.3)  # +30% attack
            audio.play("boss_roar")
            self.add_floating_text("⚠️ AMARAH SANG LORD!", (680, 160), COLOR_TEXT_RED, size=28)
            self.battle_log = f"[ENRAGE] ⚠️ SANG LORD MEMASUKI MODE AMARAH! Serangannya meningkat drastis!"
            self.log_color = COLOR_TEXT_RED

        self.clear_slots()

    def execute_enemy_turn(self):
        if self.enemy.hp <= 0:
            self._handle_victory()
            return

        # 1. Burn tick
        if self.enemy.burn_turns > 0:
            self.enemy.burn_turns -= 1
            burn_dmg = self.enemy.burn_dmg
            self.enemy.hp = max(0, self.enemy.hp - burn_dmg)
            self.enemy_hp_bar.set_hp(self.enemy.hp)
            audio.play("hit")
            self.add_floating_text(f"🔥 -{burn_dmg}", (720, 200), COLOR_FIRE, size=22)
            if self.enemy.hp <= 0:
                self._handle_victory()
                return

        # 2. Stun tick
        if self.enemy.stunned_turns > 0:
            self.enemy.stunned_turns -= 1
            self.battle_log = f"[STATUS] 🫧 {self.enemy.nama} terjerat lumpur dan MELEWATKAN gilirannya!"
            self.log_color = COLOR_TEXT_CYAN
            self.state = "PLAYER_TURN"
            self._start_player_turn_buffs()
            return

        # 3. Blind tick
        if self.enemy.blind_turns > 0:
            self.enemy.blind_turns -= 1
            if random.random() < 0.5:
                self.battle_log = f"[STATUS] 💨 Serangan {self.enemy.nama} MELESET karena terhalang abu!"
                self.log_color = COLOR_TEXT_CYAN
                self.state = "PLAYER_TURN"
                self._start_player_turn_buffs()
                return

        # 4. Serangan Musuh
        dmg = self.enemy.atk
        if self.enemy.atk_debuff_turns > 0:
            self.enemy.atk_debuff_turns -= 1
            dmg = max(1, dmg - self.enemy.atk_debuff)

        if self.player_shield_turns > 0:
            dmg = int(dmg * 0.5)

        self.player.hp = max(0, self.player.hp - dmg)
        self.player_hp_bar.set_hp(self.player.hp)
        self.player_flash = 12
        self.shake_screen = 7
        audio.play("hit")
        self.add_floating_text(f"-{dmg} HP", (180, 230), COLOR_TEXT_RED, size=26)

        shield_note = " (Tertahan Perisai)" if self.player_shield_turns > 0 else ""
        enrage_note = " [AMARAH SANG LORD]" if self.is_enraged else ""
        self.battle_log = f"[MUSUH] ⚔️ {self.enemy.nama}{enrage_note} membalas! Kamu terkena {dmg} damage{shield_note}."
        self.log_color = COLOR_TEXT_RED

        if self.player_shield_turns > 0:
            self.player_shield_turns -= 1

        if self.player.hp <= 0:
            self.state = "DEFEAT"
            audio.play("defeat")
            return

        self.state = "PLAYER_TURN"
        self._start_player_turn_buffs()

    def _start_player_turn_buffs(self):
        if self.player_regen_turns > 0:
            self.player_regen_turns -= 1
            self.player.hp = min(self.player.max_hp, self.player.hp + self.player_regen_val)
            self.player_hp_bar.set_hp(self.player.hp)
            self.add_floating_text(f"+{self.player_regen_val} HP", (160, 200), COLOR_TEXT_GREEN, size=20)

    def _handle_victory(self):
        self.state = "VICTORY"
        audio.play("victory")
        self.loot_result = []

        for item in self.enemy.drop:
            if self.player.can_carry():
                self.player.add_to_bag(item, 1)
                self.loot_result.append(f"+1 {ELEMENT_NAMES.get(item, item)}")
            else:
                self.loot_result.append(f"Tas Penuh! (Gagal ambil {item})")

        if self.enemy.is_boss:
            _boss_unlock = {
                "pohon_tua": ("Pohon Tua", 2),
                "golem":     ("Golem Kristal", 3),
                "ratu_kabut": ("Ratu Kabut", None),
            }
            if self.enemy_key in _boss_unlock:
                defeat_key, unlock_area = _boss_unlock[self.enemy_key]
                self.player.bosses_defeated[defeat_key] = True
                if unlock_area and unlock_area not in self.player.unlocked_areas:
                    self.player.unlocked_areas.append(unlock_area)

        self.battle_log = f"[MENANG] 🎉 Berhasil menundukkan {self.enemy.nama}!"
        self.log_color = COLOR_TEXT_GREEN

    def add_floating_text(self, text, pos, color, size=24):
        self.floating_texts.append(FloatingText(text, pos, color, size))

    @staticmethod
    def _blit_with_flash(surface, sprite, pos, flash: int):
        """Blit sprite, dan tambahkan overlay putih jika flash > 0."""
        surface.blit(sprite, pos)
        if flash > 0:
            overlay = sprite.copy()
            overlay.fill((255, 255, 255, 180), special_flags=pygame.BLEND_ADD)
            surface.blit(overlay, pos)

    def update(self):
        self.anim_tick += 0.06
        self.player_hp_bar.update()
        self.enemy_hp_bar.update()

        if self.shake_screen > 0:
            self.shake_screen -= 1

        if self.enemy_flash > 0:
            self.enemy_flash -= 1
        if self.player_flash > 0:
            self.player_flash -= 1

        for ft in list(self.floating_texts):
            ft.update()
            if ft.is_dead:
                self.floating_texts.remove(ft)

        if self.state == "BREWING":
            self.turn_timer -= 1
            if self.turn_timer <= 0:
                self.state = "ENEMY_TURN"
                self.turn_timer = 45

        elif self.state == "ENEMY_TURN":
            self.turn_timer -= 1
            if self.turn_timer <= 0:
                self.execute_enemy_turn()

    def handle_event(self, event):
        if self.state == "PLAYER_TURN":
            for btn in self.btn_elements.values():
                btn.handle_event(event)

            self.btn_brew.handle_event(event)
            self.btn_clear.handle_event(event)
            self.btn_flee.handle_event(event)

            if event.type == pygame.KEYDOWN:
                _elem_keys = {pygame.K_1: "api", pygame.K_2: "air", pygame.K_3: "daun", pygame.K_4: "batu"}
                if event.key in _elem_keys:
                    self.select_ingredient(_elem_keys[event.key])
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.execute_player_attack()
                elif event.key == pygame.K_c:
                    self.clear_slots()
                elif event.key == pygame.K_ESCAPE:
                    self.attempt_flee()

        elif self.state in ("VICTORY", "DEFEAT", "FLED"):
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                return "END_BATTLE"
            if event.type == pygame.MOUSEBUTTONDOWN:
                return "END_BATTLE"

        return None

    def draw(self, surface, fonts):
        f_title = fonts["large"]
        f_reg = fonts["regular"]
        f_sm = fonts["small"]

        shake_x = random.randint(-self.shake_screen, self.shake_screen) if self.shake_screen > 0 else 0
        shake_y = random.randint(-self.shake_screen, self.shake_screen) if self.shake_screen > 0 else 0

        # Background Langit & Frame Utama Arena
        surface.fill((18, 22, 32))
        dialog_rect = pygame.Rect(30 + shake_x, 15 + shake_y, 900, 610)

        # Latar arena: gradien langit senja + tanah rumput — dibuat programatik
        # (tidak load file foto agar tidak ada UI ganda dari gambar)
        arena_bg = pygame.Surface((dialog_rect.width, 350))
        # Langit: gradien gelap ke ungu malam
        for row in range(200):
            t = row / 200
            r = int(40 + t * 30)
            g = int(45 + t * 55)
            b = int(70 + t * 55)
            pygame.draw.line(arena_bg, (r, g, b), (0, row), (dialog_rect.width, row))
        # Tanah + rumput
        pygame.draw.rect(arena_bg, (55, 100, 45), (0, 200, dialog_rect.width, 70))
        pygame.draw.rect(arena_bg, (40, 80, 32), (0, 258, dialog_rect.width, 12))
        pygame.draw.rect(arena_bg, (60, 45, 20), (0, 270, dialog_rect.width, 80))
        # Pohon dekoratif kiri
        pygame.draw.rect(arena_bg, (50, 35, 18), (60, 130, 22, 90))
        pygame.draw.circle(arena_bg, (30, 80, 35), (71, 120), 50)
        pygame.draw.circle(arena_bg, (35, 90, 40), (55, 135), 38)
        # Pohon dekoratif kanan
        pygame.draw.rect(arena_bg, (50, 35, 18), (820, 130, 22, 90))
        pygame.draw.circle(arena_bg, (30, 80, 35), (831, 120), 50)
        pygame.draw.circle(arena_bg, (35, 90, 40), (850, 135), 40)
        # Bulan / bintang kecil di atas
        pygame.draw.circle(arena_bg, (240, 230, 180), (810, 40), 18)
        for sx, sy in [(120, 25), (300, 15), (500, 35), (680, 20), (750, 55)]:
            pygame.draw.circle(arena_bg, (255, 255, 200), (sx, sy), 2)
        surface.blit(arena_bg, (dialog_rect.x, dialog_rect.y))

        # Bingkai kayu di sekeliling arena
        pygame.draw.rect(surface, (110, 65, 35), dialog_rect, width=4, border_radius=6)
        pygame.draw.rect(surface, (45, 25, 12), dialog_rect, width=2, border_radius=6)

        # ── KARTU INFO PEMAIN (KIRI ATAS) ──────────────────────────────────
        p_card = pygame.Rect(55 + shake_x, 30 + shake_y, 290, 80)
        pygame.draw.rect(surface, (40, 26, 18), p_card, border_radius=6)
        pygame.draw.rect(surface, (135, 85, 45), p_card, width=2, border_radius=6)

        # Potret Murid Alkemis (Kotak Hijau Khas Mockup)
        port_rect = pygame.Rect(p_card.x + 8, p_card.y + 12, 40, 40)
        pygame.draw.rect(surface, (25, 60, 25), port_rect, border_radius=4)
        pygame.draw.rect(surface, (95, 195, 85), port_rect, width=2, border_radius=4)
        p_port = StardewSpriteCache.get_portrait("player")
        if p_port:
            surface.blit(pygame.transform.scale(p_port, (36, 36)), (port_rect.x + 2, port_rect.y + 2))

        t_player = f_reg.render("Murid Alkemis (Kamu)", True, (245, 230, 200))
        surface.blit(t_player, (p_card.x + 56, p_card.y + 10))
        self.player_hp_bar.rect.topleft = (p_card.x + 56, p_card.y + 36)
        self.player_hp_bar.draw(surface, f_sm, "HP:")

        if self.player_shield_turns > 0:
            b_surf = f_sm.render(f"🛡️ Perisai Batu ({self.player_shield_turns})", True, COLOR_TEXT_CYAN)
            surface.blit(b_surf, (p_card.x + 56, p_card.y + 58))

        # ── KARTU INFO MUSUH / BOS (KANAN ATAS) ────────────────────────────
        e_card_w = 340 if self.enemy.is_boss else 300
        e_card = pygame.Rect(dialog_rect.right - e_card_w - 25 + shake_x, 30 + shake_y, e_card_w, 80)
        pygame.draw.rect(surface, (40, 22, 22) if self.enemy.is_boss else (40, 26, 18), e_card, border_radius=6)
        pygame.draw.rect(surface, (180, 50, 50) if self.enemy.is_boss else (135, 85, 45), e_card, width=2, border_radius=6)

        # Potret Musuh / Bos
        e_port_rect = pygame.Rect(e_card.right - 48, e_card.y + 12, 40, 40)
        pygame.draw.rect(surface, (30, 20, 25), e_port_rect, border_radius=4)
        pygame.draw.rect(surface, (180, 60, 60) if self.enemy.is_boss else (95, 195, 85), e_port_rect, width=2, border_radius=4)
        e_port = StardewSpriteCache.get_portrait(self.enemy.nama)
        if e_port:
            surface.blit(pygame.transform.scale(e_port, (36, 36)), (e_port_rect.x + 2, e_port_rect.y + 2))

        enemy_title = self.enemy.nama + (" (Bos Utama)" if self.enemy.is_boss else " (Musuh)")
        t_enemy = f_reg.render(enemy_title, True, COLOR_TEXT_RED if self.enemy.is_boss else (245, 230, 200))
        surface.blit(t_enemy, (e_card.x + 12, e_card.y + 10))
        self.enemy_hp_bar.rect.topleft = (e_card.x + 12, e_card.y + 36)
        self.enemy_hp_bar.draw(surface, f_sm, "HP:")

        weak_str = "Lemah: " + ", ".join([f"{ELEMENT_SYMBOLS.get(e, '')} {e.capitalize()}" for e in self.enemy.lemah])
        w_surf = f_sm.render(weak_str, True, COLOR_TEXT_GOLD)
        surface.blit(w_surf, (e_card.x + 12, e_card.y + 58))

        # ── SPRITE PEMAIN DI ARENA (TENGAH KIRI) ───────────────────────────
        px, py = 230 + shake_x, 280 + int(math.sin(self.anim_tick * 2) * 3)
        # Bayangan kaki di rumput tanah
        pygame.draw.ellipse(surface, (25, 40, 20, 140), (px - 32, py + 12, 64, 16))

        # Pilih pose Murid Alkemis berdasarkan giliran/aksi
        if self.state == "BREWING":
            p_action = "battle_fire"
        elif self.state == "VICTORY":
            p_action = "battle_victory"
        else:
            p_action = "battle_potion"

        p_raw = StardewSpriteCache.get_student_sprite(action=p_action)
        if p_raw:
            p_scale = 1.6
            p_sprite = pygame.transform.scale(p_raw, (int(p_raw.get_width() * p_scale), int(p_raw.get_height() * p_scale)))
            pw, ph = p_sprite.get_size()
            self._blit_with_flash(surface, p_sprite, (px - pw // 2, py - ph + 16), self.player_flash)

        # ── SPRITE MUSUH / BOS DI ARENA (TENGAH KANAN) ─────────────────────
        ex, ey = 700 + shake_x, 260 + int(math.sin(self.anim_tick * 2.2) * 4)
        pygame.draw.ellipse(surface, (25, 40, 20, 140), (ex - 45, ey + 24, 90, 20))

        if self.enemy.is_boss:
            # Bos Ratu Kabut Terkutuk
            boss_act = "cast" if self.state == "ENEMY_TURN" else "idle"
            e_sprite = StardewSpriteCache.get_boss_sprite(action=boss_act, scale=2.0)
            if not e_sprite:
                e_sprite = StardewSpriteCache.get_boss_sprite("idle", scale=2.0)
            
            # Efek kristal & kabut saat menyerang
            if self.state == "ENEMY_TURN":
                duri = StardewSpriteCache.get_boss_fx("duri", scale=1.5)
                if duri:
                    surface.blit(duri, (px - 20, py - 30))
                kabut = StardewSpriteCache.get_boss_fx("kabut", scale=1.5)
                if kabut:
                    surface.blit(kabut, (ex - 80, ey - 20))
        else:
            # Monster Biasa — lookup langsung dari enemy_key
            _sprite_map = {
                "slime":    ("slime", 2.0),
                "kelelawar": ("bat", 1.7),
                "katak":    ("slime", 2.0),
            }
            key_s, scale_s = _sprite_map.get(self.enemy_key, ("tree", 1.7))
            e_sprite = StardewSpriteCache.get_enemy_sprite(key_s, scale=scale_s)

        if e_sprite:
            ew, eh = e_sprite.get_size()
            self._blit_with_flash(surface, e_sprite, (ex - ew // 2, ey - eh + 28), self.enemy_flash)
        else:
            # Fallback
            pygame.draw.circle(surface, (60, 180, 80), (ex, ey), 34)

        # Status Efek Teks pada Musuh
        status_icons = []
        if self.enemy.burn_turns > 0:
            status_icons.append(f"🔥 Terbakar ({self.enemy.burn_turns})")
        if self.enemy.stunned_turns > 0:
            status_icons.append("🫧 Lumpur")
        if self.enemy.blind_turns > 0:
            status_icons.append("💨 Buta")
        if self.is_enraged:
            status_icons.append("⚠️ AMARAH")
        if status_icons:
            st_text = " | ".join(status_icons)
            st_surf = f_sm.render(st_text, True, COLOR_TEXT_YELLOW)
            surface.blit(st_surf, (ex - st_surf.get_width() // 2, ey - 105))

        # ── PANEL BAWAH: DUA PANEL KAYU KLASIK RPG (BAHAN & PILIH BAHAN) ───
        # 1. Panel Kiri (Bahan) — Sesuai Referensi Resmi Battle UI
        panel_mat = pygame.Rect(55, 365, 275, 245)
        pygame.draw.rect(surface, (36, 22, 14), panel_mat, border_radius=6)
        pygame.draw.rect(surface, (125, 75, 40), panel_mat, width=3, border_radius=6)
        pygame.draw.rect(surface, (60, 35, 18), panel_mat.inflate(-4, -4), width=1, border_radius=5)

        # Header "Bahan:" — left-aligned sesuai referensi
        t_bahan = f_reg.render("Bahan:", True, (245, 220, 175))
        surface.blit(t_bahan, (panel_mat.x + 16, panel_mat.y + 12))

        # Garis pemisah header
        pygame.draw.line(surface, (90, 55, 30), (panel_mat.x + 12, panel_mat.y + 36), (panel_mat.right - 12, panel_mat.y + 36), 1)

        # Daftar bahan — emoji + teks, left-aligned sesuai referensi
        # Layout: 2 kolom baris pertama, lalu 1 item per baris
        pad_left = panel_mat.x + 16
        items_start_y = panel_mat.y + 48
        row_height = 40
        col2_offset = 130  # offset kolom kedua dari pad_left

        materials = [
            ("air",  "Air",  (130, 200, 255)),
            ("api",  "Api",  (255, 140, 80)),
            ("daun", "Daun", (130, 240, 130)),
            ("batu", "Batu", (200, 200, 210)),
        ]

        for i, (elem, label, color) in enumerate(materials):
            ix = pad_left + (i % 2) * col2_offset
            iy = items_start_y + (i // 2) * row_height
            emoji = ELEMENT_SYMBOLS.get(elem, "")
            qty = self.player.bag.get(elem, 0)
            txt = f_reg.render(f"{emoji} {label} x{qty}", True, color)
            surface.blit(txt, (ix, iy))

        # Info Kapasitas Ransel — bottom-left sesuai referensi
        bag_sub = f_sm.render(f"Kapasitas: {self.player.total_bag_items}/10 Item", True, (190, 160, 120))
        surface.blit(bag_sub, (panel_mat.x + 16, panel_mat.bottom - 28))

        # 2. Panel Kanan (Pilih Bahan 1 & 2 + Log Hasil Racikan)
        panel_act = pygame.Rect(345, 365, 560, 245)
        pygame.draw.rect(surface, (36, 22, 14), panel_act, border_radius=6)
        pygame.draw.rect(surface, (125, 75, 40), panel_act, width=3, border_radius=6)
        pygame.draw.rect(surface, (60, 35, 18), panel_act.inflate(-4, -4), width=1, border_radius=5)

        # Header Pilih bahan 1 > & Pilih bahan 2 >
        lbl_s1 = f_reg.render("Pilih bahan 1 >", True, (245, 220, 175))
        surface.blit(lbl_s1, (panel_act.x + 20, panel_act.y + 12))

        lbl_s2 = f_reg.render("Pilih bahan 2 >", True, (245, 220, 175))
        surface.blit(lbl_s2, (panel_act.x + 160, panel_act.y + 12))

        # Tampilan Slot 1 & Slot 2
        s1_box = pygame.Rect(panel_act.x + 20, panel_act.y + 42, 54, 54)
        pygame.draw.rect(surface, (20, 12, 8), s1_box, border_radius=4)
        pygame.draw.rect(surface, (230, 190, 80) if self.slot1 else (90, 55, 30), s1_box, width=2, border_radius=4)
        if self.slot1:
            sym1 = ELEMENT_SYMBOLS.get(self.slot1, "")
            t_s1 = f_title.render(sym1, True, (255, 255, 255))
            surface.blit(t_s1, t_s1.get_rect(center=s1_box.center))

        s2_box = pygame.Rect(panel_act.x + 160, panel_act.y + 42, 54, 54)
        pygame.draw.rect(surface, (20, 12, 8), s2_box, border_radius=4)
        pygame.draw.rect(surface, (230, 190, 80) if self.slot2 else (90, 55, 30), s2_box, width=2, border_radius=4)
        if self.slot2:
            sym2 = ELEMENT_SYMBOLS.get(self.slot2, "")
            t_s2 = f_title.render(sym2, True, (255, 255, 255))
            surface.blit(t_s2, t_s2.get_rect(center=s2_box.center))

        # 4 Tombol Bahan (🔥, 💧, 🌿, 🪨) di Kanan
        for elem, btn in self.btn_elements.items():
            btn.draw(surface, f_reg, f_sm)
            # Render emoji di tengah tombol
            sym = ELEMENT_SYMBOLS.get(elem, "")
            t_elem = f_title.render(sym, True, (255, 255, 255))
            surface.blit(t_elem, t_elem.get_rect(center=btn.rect.center))
            # Border highlight jika dipilih
            if self.slot1 == elem or self.slot2 == elem:
                pygame.draw.rect(surface, (255, 230, 80), btn.rect, width=3, border_radius=4)

        # Tombol Aksi: Racik, Batal, Kabur
        flee_pct = self.calculate_flee_chance()
        self.btn_flee.text = f"🏃 Kabur ({flee_pct}%)"
        self.btn_brew.draw(surface, f_reg, f_sm)
        self.btn_clear.draw(surface, f_reg, f_sm)
        self.btn_flee.draw(surface, f_reg, f_sm)

        # Kotak Log Aksi / Hasil Ramuan di Bawah
        log_panel = pygame.Rect(panel_act.x + 14, panel_act.y + 160, panel_act.width - 28, 70)
        pygame.draw.rect(surface, (24, 15, 10), log_panel, border_radius=4)
        pygame.draw.rect(surface, (90, 55, 25), log_panel, width=1, border_radius=4)

        log_text = f"➔ {self.battle_log}"
        log_s = f_sm.render(log_text, True, self.log_color)
        surface.blit(log_s, (log_panel.x + 12, log_panel.centery - log_s.get_height() // 2))

        # Tampilkan efek ledakan api resmi jika terjadi serangan
        if "damage" in self.battle_log or self.state == "BREWING":
            exp_fx = StardewSpriteCache.get_explosion_fx()
            if exp_fx:
                surface.blit(exp_fx, (log_panel.right - 58, log_panel.centery - 22))

        # Gambar Teks Melayang
        for ft in self.floating_texts:
            ft.draw(surface, f_title if ft.size > 24 else f_reg)

        # Modal Kemenangan / Kekalahan / Kabur
        if self.state in ("VICTORY", "DEFEAT", "FLED"):
            overlay = pygame.Surface((960, 640), pygame.SRCALPHA)
            overlay.fill((5, 15, 30, 210))
            surface.blit(overlay, (0, 0))

            m_box = pygame.Rect(260, 160, 440, 290)
            draw_gt_dialog(surface, m_box)

            if self.state == "VICTORY":
                t_head = f_title.render("🎉 KEMENANGAN AKBAR!", True, GT_SLOT_SELECTED)
                surface.blit(t_head, (m_box.centerx - t_head.get_width() // 2, m_box.y + 20))
                t_sub = f_reg.render(f"{self.enemy.nama} berhasil ditundukkan!", True, COLOR_TEXT_WHITE)
                surface.blit(t_sub, (m_box.centerx - t_sub.get_width() // 2, m_box.y + 65))

                y_loot = m_box.y + 110
                l_head = f_sm.render("Hadiah Bahan Didapatkan:", True, COLOR_TEXT_GREEN)
                surface.blit(l_head, (m_box.centerx - l_head.get_width() // 2, y_loot))

                loot_str = ", ".join(self.loot_result) if self.loot_result else "Ransel Penuh!"
                loot_surf = f_reg.render(loot_str, True, COLOR_TEXT_YELLOW)
                surface.blit(loot_surf, (m_box.centerx - loot_surf.get_width() // 2, y_loot + 25))

                if self.new_recipe_unlocked:
                    rec_surf = f_sm.render(f"✨ Resep Baru Terbuka: {self.new_recipe_unlocked}!", True, GT_SLOT_SELECTED)
                    surface.blit(rec_surf, (m_box.centerx - rec_surf.get_width() // 2, y_loot + 55))

            elif self.state == "DEFEAT":
                t_head = f_title.render("💀 KAMU PINGSAN!", True, COLOR_TEXT_RED)
                surface.blit(t_head, (m_box.centerx - t_head.get_width() // 2, m_box.y + 20))
                t_sub = f_reg.render("HP kamu habis! Diselamatkan warga ke desa.", True, COLOR_TEXT_WHITE)
                surface.blit(t_sub, (m_box.centerx - t_sub.get_width() // 2, m_box.y + 70))
                t_pen = f_sm.render("Separuh bahan di ranselmu tercecer.", True, COLOR_TEXT_MUTED)
                surface.blit(t_pen, (m_box.centerx - t_pen.get_width() // 2, m_box.y + 110))

            elif self.state == "FLED":
                t_head = f_title.render("💨 BERHASIL MELARIKAN DIRI", True, COLOR_TEXT_CYAN)
                surface.blit(t_head, (m_box.centerx - t_head.get_width() // 2, m_box.y + 25))
                t_sub = f_reg.render("Kamu meloloskan diri kembali ke jalur aman!", True, COLOR_TEXT_WHITE)
                surface.blit(t_sub, (m_box.centerx - t_sub.get_width() // 2, m_box.y + 80))

            t_cont = f_reg.render("[ Tekan ENTER atau SPASI untuk Lanjut ]", True, GT_SLOT_SELECTED)
            surface.blit(t_cont, (m_box.centerx - t_cont.get_width() // 2, m_box.bottom - 45))
