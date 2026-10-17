"""
Manajer Game Utama (Game Engine)
"""

import pygame
import math
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GT_DIALOG_BG, GT_DIALOG_BG_DARK,
    GT_BORDER_CYAN, GT_SLOT_BG, GT_SLOT_BORDER, GT_SLOT_SELECTED,
    COLOR_TEXT_WHITE, COLOR_TEXT_YELLOW, COLOR_TEXT_MUTED, COLOR_TEXT_GOLD,
    COLOR_TEXT_RED, COLOR_TEXT_GREEN, COLOR_TEXT_CYAN, ELEMENT_COLORS,
    ELEMENT_NAMES, ELEMENT_SYMBOLS, MAX_BAG_CAPACITY, STATE_MENU, STATE_EXPLORE,
    STATE_BATTLE, STATE_RECIPE_BOOK, STATE_STORAGE, STATE_VICTORY
)
from entities import Player
from world import WorldMap
from battle import BattleManager
from recipes import RECIPES
from ui import ToastNotification, draw_gt_dialog, Button
from audio import audio
from sprites import StardewSpriteCache

class GameManager:
    def __init__(self):
        self.state = STATE_MENU
        self.player = Player(480, 320)
        self.current_area_id = 0
        self.world_map = WorldMap(self.current_area_id)
        self.battle_manager = None
        self.encounter_enemy = None
        self.toast = ToastNotification()

        self.current_prompt = ""
        self.storage_selected_elem = "api"

        # Tombol Main Menu Resmi
        self.btn_menu_start = Button(
            ((SCREEN_WIDTH - 250) // 2, 330, 250, 42),
            "▶ Mulai Petualangan",
            callback=self.start_game,
            color_theme="green",
            shortcut="[Enter]"
        )
        self.btn_menu_exit = Button(
            ((SCREEN_WIDTH - 250) // 2, 385, 250, 42),
            "✖ Keluar Game",
            callback=self.quit_game,
            color_theme="red",
            shortcut="[Esc]"
        )

        self.toast.show("[SISTEM] Selamat datang di Brewbound!", COLOR_TEXT_YELLOW, 220)
        self._modal_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self._modal_overlay.fill((5, 15, 30, 210))

    def start_game(self):
        audio.play("select")
        self.state = STATE_EXPLORE
        self.toast.show("[PANDUAN] Jelajahi desa untuk kumpulkan bahan!", COLOR_TEXT_CYAN, 200)

    def quit_game(self):
        import sys
        pygame.quit()
        sys.exit()


    def change_area(self, area_id: int):
        self.current_area_id = area_id
        self.world_map = WorldMap(area_id)
        if area_id == 0:
            self.player.x = 820
            self.player.y = 320
        else:
            self.player.x = 90
            self.player.y = 320
        self.toast.show(f"[LOKASI] Memasuki {self.world_map.title}", COLOR_TEXT_CYAN, 120)

    def start_battle(self, enemy_key: str):
        audio.play("select")
        self.battle_manager = BattleManager(self.player, enemy_key)
        self.state = STATE_BATTLE

    def handle_interaction(self):
        px, py = self.player.x, self.player.y

        # 1. Cek Titik Panen
        for hp in self.world_map.harvest_points:
            dist = math.hypot(hp.x - px, hp.y - py)
            if dist < 42 and hp.active:
                if self.player.can_carry():
                    elem = hp.harvest()
                    self.player.add_to_bag(elem, 1)
                    self.toast.show(f"+1 {ELEMENT_NAMES[elem]} ({ELEMENT_SYMBOLS[elem]}) didapatkan!", ELEMENT_COLORS[elem], 100)
                else:
                    self.toast.show("[RANSEL PENUH] Maksimal 10 bahan! Simpan di peti desa!", COLOR_TEXT_RED, 130)
                return

        # 2. Cek Objek Interaktif Peta
        for obj in self.world_map.interactables:
            r = obj["rect"]
            p_rect = pygame.Rect(px - 20, py - 20, 40, 40)
            if r.colliderect(p_rect.inflate(32, 32)):
                t = obj["type"]
                if t == "BED":
                    self.player.rest_in_village()
                    self.toast.show("[PULIH] Kamu beristirahat di kasur empuk. HP 100% pulih!", COLOR_TEXT_GREEN, 150)
                elif t == "STORAGE":
                    self.state = STATE_STORAGE
                    audio.play("select")
                elif t == "NPC_MENTOR":
                    self.toast.show("Guru Zephyr: 'Hati-hati, para Lord akan mengamuk saat HP-nya di bawah 50%!'", COLOR_TEXT_YELLOW, 200)
                elif t == "PORTAL_FOREST":
                    self.change_area(1)
                elif t == "PORTAL_VILLAGE":
                    self.change_area(0)
                elif t == "BOSS_FOREST":
                    self.start_battle("pohon_tua")
                elif t == "BOSS_CAVE":
                    self.start_battle("golem")
                elif t == "BOSS_SWAMP":
                    self.start_battle("ratu_kabut")
                return

    def update(self):
        self.toast.update()

        if self.state == STATE_EXPLORE:
            dx, dy = 0, 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy += 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += 1

            screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.player.move(dx, dy, self.world_map.colliders, screen_rect)
            self.world_map.update()

            self.current_prompt = ""
            px, py = self.player.x, self.player.y

            for hp in self.world_map.harvest_points:
                if hp.active and math.hypot(hp.x - px, hp.y - py) < 42:
                    self.current_prompt = f"[E] Ambil {ELEMENT_NAMES[hp.elemen]}"
                    break

            if not self.current_prompt:
                p_rect = pygame.Rect(px - 20, py - 20, 40, 40)
                for obj in self.world_map.interactables:
                    if obj["rect"].colliderect(p_rect.inflate(32, 32)):
                        self.current_prompt = f"[E] {obj['label']}"
                        break

            # Cek kontak dengan musuh berkeliaran
            for e in list(self.world_map.enemies):
                dist = math.hypot(e["x"] - px, e["y"] - py)
                if dist < (self.player.radius + e["radius"] + 8):
                    self.start_battle(e["key"])
                    self.encounter_enemy = e
                    break

        elif self.state == STATE_BATTLE:
            if self.battle_manager:
                self.battle_manager.update()

    def handle_event(self, event):
        if self.state == STATE_MENU:
            self.btn_menu_start.handle_event(event)
            self.btn_menu_exit.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_game()
                elif event.key == pygame.K_ESCAPE:
                    self.quit_game()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b and self.state in (STATE_EXPLORE, STATE_RECIPE_BOOK):
                self.state = STATE_RECIPE_BOOK if self.state == STATE_EXPLORE else STATE_EXPLORE
                audio.play("select")
                return

        if self.state == STATE_EXPLORE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e or event.key == pygame.K_SPACE:
                    self.handle_interaction()

        elif self.state == STATE_BATTLE:
            res = self.battle_manager.handle_event(event)
            if res == "END_BATTLE":
                if self.battle_manager.state == "VICTORY":
                    if self.encounter_enemy in self.world_map.enemies:
                        self.world_map.enemies.remove(self.encounter_enemy)
                    if self.player.bosses_defeated.get("Ratu Kabut", False):
                        self.state = STATE_VICTORY
                    else:
                        self.state = STATE_EXPLORE
                elif self.battle_manager.state == "DEFEAT":
                    lost = self.player.faint_penalty()
                    self.change_area(0)
                    self.player.x = 340
                    self.player.y = 260
                    self.state = STATE_EXPLORE
                    lost_msg = ", ".join(lost) if lost else "tidak ada"
                    self.toast.show(f"[PINGSAN] Kembali ke desa. Bahan tercecer: {lost_msg}.", COLOR_TEXT_RED, 220)
                elif self.battle_manager.state == "FLED":
                    if self.encounter_enemy in self.world_map.enemies:
                        enemy_x = self.encounter_enemy["x"]
                        enemy_y = self.encounter_enemy["y"]
                        dx = self.player.x - enemy_x
                        dy = self.player.y - enemy_y
                        distance = math.hypot(dx, dy)
                        if distance == 0:
                            dx, dy, distance = -1, 0, 1
                        escape_distance = self.player.radius + self.encounter_enemy["radius"] + 32
                        self.player.x = max(
                            self.player.radius,
                            min(SCREEN_WIDTH - self.player.radius, enemy_x + dx / distance * escape_distance)
                        )
                        self.player.y = max(
                            self.player.radius + 56,
                            min(SCREEN_HEIGHT - self.player.radius - 20, enemy_y + dy / distance * escape_distance)
                        )
                    self.state = STATE_EXPLORE
                    self.toast.show("[KABUR] Kamu berhasil meloloskan diri ke tempat aman!", COLOR_TEXT_GREEN, 150)
                else:
                    self.state = STATE_EXPLORE
                self.encounter_enemy = None
                self.battle_manager = None

        elif self.state == STATE_STORAGE:
            if event.type == pygame.KEYDOWN:
                _elem_keys = {pygame.K_1: "api", pygame.K_2: "air", pygame.K_3: "daun", pygame.K_4: "batu"}
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    self.state = STATE_EXPLORE
                    audio.play("click")
                elif event.key in _elem_keys:
                    self.storage_selected_elem = _elem_keys[event.key]
                elif event.key == pygame.K_RIGHT:
                    elem = self.storage_selected_elem
                    if self.player.storage.get(elem, 0) > 0 and self.player.can_carry():
                        self.player.storage[elem] -= 1
                        self.player.bag[elem] = self.player.bag.get(elem, 0) + 1
                        audio.play("select")
                elif event.key == pygame.K_LEFT:
                    elem = self.storage_selected_elem
                    if self.player.bag.get(elem, 0) > 0:
                        self.player.bag[elem] -= 1
                        self.player.storage[elem] = self.player.storage.get(elem, 0) + 1
                        audio.play("select")

        elif self.state == STATE_RECIPE_BOOK:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                    self.state = STATE_EXPLORE
                    audio.play("click")

        elif self.state == STATE_VICTORY:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                self.player.bosses_defeated["Ratu Kabut"] = False
                self.change_area(0)
                self.state = STATE_EXPLORE

    def draw(self, surface, fonts):
        f_reg = fonts["regular"]

        if self.state == STATE_MENU:
            self._draw_main_menu(surface, fonts)

        elif self.state == STATE_EXPLORE:
            self.world_map.draw(surface, fonts)
            self.player.draw(surface)

            if self.current_prompt:
                p_surf = f_reg.render(self.current_prompt, True, GT_SLOT_SELECTED)
                bx = (SCREEN_WIDTH - p_surf.get_width()) // 2
                by = 545
                p_rect = pygame.Rect(bx - 14, by - 6, p_surf.get_width() + 28, p_surf.get_height() + 12)
                draw_gt_dialog(surface, p_rect)
                surface.blit(p_surf, (bx, by))

            self._draw_hud(surface, fonts)

        elif self.state == STATE_BATTLE:
            if self.battle_manager:
                self.battle_manager.draw(surface, fonts)

        elif self.state == STATE_STORAGE:
            self._draw_storage_modal(surface, fonts)

        elif self.state == STATE_RECIPE_BOOK:
            self._draw_recipe_book_modal(surface, fonts)

        elif self.state == STATE_VICTORY:
            self._draw_victory_screen(surface, fonts)

        self.toast.draw(surface, f_reg)

    def _draw_main_menu(self, surface, fonts):
        f_title = fonts["large"]
        f_reg = fonts["regular"]
        f_sm = fonts["small"]

        # Menu dirender mandiri agar aset menu lama tidak menumpuk di belakang UI.
        surface.fill((23, 42, 34))
        pygame.draw.rect(surface, (31, 55, 42), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        pygame.draw.line(surface, (76, 105, 62), (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)

        # Kotak Judul Programatik (TIDAK menggunakan foto asset yang sudah mengandung tombol)
        bx = (SCREEN_WIDTH - 460) // 2
        by = 80
        m_rect = pygame.Rect(bx, by, 460, 150)
        # Bayangan kotak
        shadow = pygame.Rect(bx + 4, by + 4, 460, 150)
        pygame.draw.rect(surface, (8, 5, 3), shadow, border_radius=10)
        # Panel kayu utama
        pygame.draw.rect(surface, (35, 22, 12), m_rect, border_radius=10)
        pygame.draw.rect(surface, (140, 90, 40), m_rect, width=3, border_radius=10)
        pygame.draw.rect(surface, (80, 50, 22), m_rect.inflate(-6, -6), width=1, border_radius=9)
        # Dekorasi garis tengah
        sep_y = m_rect.y + 95
        pygame.draw.line(surface, (140, 90, 40), (m_rect.x + 20, sep_y), (m_rect.right - 20, sep_y), 1)
        # Teks judul besar
        t1 = f_title.render("BREWBOUND", True, (255, 215, 60))
        t2 = f_reg.render("Alkemis Desa — Selamatkan Desa dari Kabut Kutukan!", True, (245, 230, 160))
        surface.blit(t1, (m_rect.centerx - t1.get_width() // 2, m_rect.y + 22))
        surface.blit(t2, (m_rect.centerx - t2.get_width() // 2, m_rect.y + 60))
        # Ikon ramuan dekoratif kiri kanan
        deco_color = (140, 90, 40)
        for dx in [m_rect.x + 14, m_rect.right - 22]:
            pygame.draw.circle(surface, deco_color, (dx, m_rect.y + 14), 5)

        # Tombol Aksi Mulai & Keluar — satu-satunya tombol (tidak ada gambar yang tumpang tindih)
        self.btn_menu_start.draw(surface, f_reg, f_sm)
        self.btn_menu_exit.draw(surface, f_reg, f_sm)

        # Petunjuk Singkat
        guide = f_sm.render("[Panah/WASD] Jalan  |  [E] Interaksi  |  [B] Buku Resep", True, (200, 180, 140))
        surface.blit(guide, (SCREEN_WIDTH // 2 - guide.get_width() // 2, 470))

        # Credit kanan bawah
        credit = f_sm.render("Created by Razi & Musa", True, (160, 150, 130))
        surface.blit(credit, (SCREEN_WIDTH - credit.get_width() - 16, SCREEN_HEIGHT - credit.get_height() - 12))

    def _draw_hud(self, surface, fonts):
        f_reg = fonts["regular"]
        f_sm = fonts["small"]

        # Bar Panel Atas Bergaya Growtopia Chat Window
        hud_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 56)
        pygame.draw.rect(surface, GT_DIALOG_BG, hud_rect)
        pygame.draw.rect(surface, GT_DIALOG_BG_DARK, (4, 4, SCREEN_WIDTH - 8, 48))
        pygame.draw.line(surface, GT_BORDER_CYAN, (0, 55), (SCREEN_WIDTH, 55), 2)

        # Nama Lokasi
        t_loc = f_reg.render(self.world_map.title, True, GT_SLOT_SELECTED)
        surface.blit(t_loc, (16, 16))

        # Bar HP Pemain
        hp_text = f_sm.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, COLOR_TEXT_WHITE)
        surface.blit(hp_text, (260, 18))
        hp_bar_rect = pygame.Rect(340, 18, 110, 18)
        pygame.draw.rect(surface, (10, 20, 35), hp_bar_rect, border_radius=4)
        hp_ratio = self.player.hp / self.player.max_hp
        fill_w = int(hp_bar_rect.width * hp_ratio)
        if fill_w > 0:
            pygame.draw.rect(surface, COLOR_TEXT_GREEN, (hp_bar_rect.x, hp_bar_rect.y, fill_w, hp_bar_rect.height), border_radius=4)
        pygame.draw.rect(surface, GT_BORDER_CYAN, hp_bar_rect, width=1, border_radius=4)

        # Hotbar Ransel Bahan (Emoji langsung)
        elements = ("api", "air", "daun", "batu")
        bag_groups = []
        for elem in elements:
            emoji_sym = ELEMENT_SYMBOLS.get(elem, "")
            emoji_surf = f_reg.render(emoji_sym, True, (255, 255, 255))
            count_surf = f_sm.render(str(self.player.bag.get(elem, 0)), True, COLOR_TEXT_YELLOW)
            group_width = emoji_surf.get_width() + 4 + count_surf.get_width()
            bag_groups.append((emoji_surf, count_surf, group_width))

        bag_gap = 10
        bag_width = sum(group[2] for group in bag_groups) + bag_gap * (len(bag_groups) - 1)
        bag_x = 465 + (155 - bag_width) // 2
        for emoji_surf, count_surf, group_width in bag_groups:
            surface.blit(emoji_surf, (bag_x, 14))
            surface.blit(count_surf, (bag_x + emoji_surf.get_width() + 4, 18))
            bag_x += group_width + bag_gap

        cap_color = COLOR_TEXT_RED if self.player.total_bag_items >= MAX_BAG_CAPACITY else COLOR_TEXT_CYAN
        t_cap = f_sm.render(f"[{self.player.total_bag_items}/10]", True, cap_color)
        surface.blit(t_cap, (625, 18))

        # Shortcut Buku Resep
        t_keys = f_sm.render("[B] Resep", True, GT_SLOT_SELECTED)
        surface.blit(t_keys, (840, 18))

    def _draw_storage_modal(self, surface, fonts):
        surface.blit(self._modal_overlay, (0, 0))

        box = pygame.Rect(180, 80, 600, 480)
        draw_gt_dialog(surface, box, title="STORAGE")

        f_title = fonts["large"]
        f_reg = fonts["regular"]
        f_sm = fonts["small"]

        title = f_title.render("📦 Peti Bahan Alkemis Desa", True, GT_SLOT_SELECTED)
        surface.blit(title, (box.centerx - title.get_width() // 2, box.y + 16))

        sub = f_sm.render("Kelola bahan antara Ransel (Maks 10) dan Peti Desa (Tanpa Batas)", True, COLOR_TEXT_MUTED)
        surface.blit(sub, (box.centerx - sub.get_width() // 2, box.y + 52))

        y_content = box.y + 90
        elements = ["api", "air", "daun", "batu"]
        elem_keys = ["1", "2", "3", "4"]

        for i, elem in enumerate(elements):
            row_y = y_content + i * 68
            is_sel = (self.storage_selected_elem == elem)

            row_rect = pygame.Rect(box.x + 30, row_y, box.width - 60, 54)
            bg_col = (20, 55, 105) if is_sel else (10, 32, 64)
            pygame.draw.rect(surface, bg_col, row_rect, border_radius=6)
            b_border = GT_SLOT_SELECTED if is_sel else GT_BORDER_CYAN
            pygame.draw.rect(surface, b_border, row_rect, width=2, border_radius=6)

            t_elem = f_reg.render(f"[{elem_keys[i]}] {ELEMENT_SYMBOLS[elem]} {ELEMENT_NAMES[elem]}", True, ELEMENT_COLORS[elem])
            surface.blit(t_elem, (row_rect.x + 14, row_rect.centery - t_elem.get_height() // 2))

            bag_qty = self.player.bag.get(elem, 0)
            t_bag = f_reg.render(f"Ransel: {bag_qty}", True, COLOR_TEXT_WHITE)
            surface.blit(t_bag, (row_rect.x + 230, row_rect.centery - t_bag.get_height() // 2))

            arrow = f_sm.render("⬅ [Panah Kiri] Simpan | Ambil [Panah Kanan] ➔", True, COLOR_TEXT_MUTED)
            surface.blit(arrow, (row_rect.x + 300, row_rect.centery - arrow.get_height() // 2))

            sto_qty = self.player.storage.get(elem, 0)
            t_sto = f_reg.render(f"Peti: {sto_qty}", True, GT_SLOT_SELECTED)
            surface.blit(t_sto, (row_rect.right - 85, row_rect.centery - t_sto.get_height() // 2))

        guide = f_sm.render("Pilih baris: [1-4] | Ambil: [➔] | Simpan: [⬅] | Tutup: [ESC / E]", True, GT_SLOT_SELECTED)
        surface.blit(guide, (box.centerx - guide.get_width() // 2, box.bottom - 38))

    def _draw_recipe_book_modal(self, surface, fonts):
        surface.blit(self._modal_overlay, (0, 0))

        box = pygame.Rect(100, 45, 760, 550)
        draw_gt_dialog(surface, box, title="RECIPES")

        f_title = fonts["large"]
        f_reg = fonts["regular"]
        f_sm = fonts["small"]

        title = f_title.render("📖 Buku Catatan Resep", True, GT_SLOT_SELECTED)
        surface.blit(title, (box.centerx - title.get_width() // 2, box.y + 14))

        sub = f_sm.render(f"Terbuka: {len(self.player.unlocked_recipes)} / 10 Resep Ramuan", True, COLOR_TEXT_CYAN)
        surface.blit(sub, (box.centerx - sub.get_width() // 2, box.y + 46))

        start_y = box.y + 75
        all_combinations = list(RECIPES.keys())

        for i, comb in enumerate(all_combinations):
            col_idx = i // 5
            row_idx = i % 5
            c_x = box.x + 25 + col_idx * 360
            c_y = start_y + row_idx * 82
            item_box = pygame.Rect(c_x, c_y, 345, 74)

            is_known = comb in self.player.unlocked_recipes
            recipe_data = RECIPES[comb]

            pygame.draw.rect(surface, (10, 32, 64), item_box, border_radius=6)
            pygame.draw.rect(surface, GT_BORDER_CYAN if is_known else (30, 60, 100), item_box, width=1, border_radius=6)

            if is_known:
                e1, e2 = comb
                comb_str = f"{ELEMENT_SYMBOLS.get(e1, '')} {e1.capitalize()} + {ELEMENT_SYMBOLS.get(e2, '')} {e2.capitalize()}"
                t_comb = f_sm.render(comb_str, True, GT_SLOT_SELECTED)
                surface.blit(t_comb, (item_box.x + 10, item_box.y + 6))

                t_name = f_reg.render(f"{recipe_data['icon']} {recipe_data['nama']}", True, COLOR_TEXT_WHITE)
                surface.blit(t_name, (item_box.x + 10, item_box.y + 25))

                t_desc = f_sm.render(recipe_data["deskripsi"][:40] + "...", True, COLOR_TEXT_MUTED)
                surface.blit(t_desc, (item_box.x + 10, item_box.y + 50))
            else:
                t_lock = f_reg.render("🔒 Resep Belum Terbuka", True, (120, 140, 160))
                surface.blit(t_lock, (item_box.x + 15, item_box.y + 16))
                t_hint = f_sm.render("Eksperimen dengan kombinasi baru di pertempuran!", True, (90, 110, 130))
                surface.blit(t_hint, (item_box.x + 15, item_box.y + 42))

        close_txt = f_reg.render("[ Tekan B atau ESC untuk Menutup ]", True, GT_SLOT_SELECTED)
        surface.blit(close_txt, (box.centerx - close_txt.get_width() // 2, box.bottom - 36))

    def _draw_victory_screen(self, surface, fonts):
        surface.fill((10, 25, 45))
        f_title = fonts["large"]
        f_reg = fonts["regular"]

        box = pygame.Rect(180, 90, 600, 460)
        draw_gt_dialog(surface, box, title="VICTORY")

        t1 = f_title.render("✨ SELURUH LORD TELAH TUMBANG! ✨", True, GT_SLOT_SELECTED)
        surface.blit(t1, (box.centerx - t1.get_width() // 2, box.y + 35))

        story1 = f_reg.render("Kabut kutukan ungu telah tersapu dari angkasa.", True, COLOR_TEXT_WHITE)
        story2 = f_reg.render("High Lord Vespera mengakui kehebatan ramuanmu.", True, COLOR_TEXT_WHITE)
        story3 = f_reg.render("Matahari kembali menyinari seluruh desa!", True, COLOR_TEXT_GREEN)

        surface.blit(story1, (box.centerx - story1.get_width() // 2, box.y + 115))
        surface.blit(story2, (box.centerx - story2.get_width() // 2, box.y + 150))
        surface.blit(story3, (box.centerx - story3.get_width() // 2, box.y + 185))

        t_title_alchemist = f_title.render("🏅 Gelar: GRAND MASTER ALKEMIS DUNIA", True, COLOR_TEXT_CYAN)
        surface.blit(t_title_alchemist, (box.centerx - t_title_alchemist.get_width() // 2, box.y + 265))

        t_end = f_reg.render("[ Tekan ENTER untuk Kembali ke Desa ]", True, GT_SLOT_SELECTED)
        surface.blit(t_end, (box.centerx - t_end.get_width() // 2, box.bottom - 48))
