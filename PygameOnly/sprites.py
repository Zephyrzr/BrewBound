"""
Pembangkit Grafis Pixel Art Tingkat Tinggi (High-Fidelity Pixel Art Sprite Generator)
Tema: Autentik Stardew Valley (Sesuai Referensi Foto Pengguna)
Menghasilkan sprite Farmhouse Kayu, Sumur Batu, Petak Ladang, Tanaman Bahan,
Pohon Oak & Sakura, Kotak Pengiriman (Shipping Bin), dan Karakter Petani Alkemis.
"""

import pygame
import math

class StardewSpriteCache:
    _cache = {}

    @classmethod
    def get_farmhouse(cls):
        if "farmhouse" not in cls._cache:
            w, h = 260, 190
            surf = pygame.Surface((w, h), pygame.SRCALPHA)

            # Dinding Kayu Utama (Pine Plank Timber)
            wall_rect = pygame.Rect(30, 75, 200, 95)
            pygame.draw.rect(surf, (216, 155, 83), wall_rect)
            # Garis papan kayu vertikal/horizontal khas Stardew
            for y in range(wall_rect.top, wall_rect.bottom, 10):
                pygame.draw.line(surf, (179, 119, 55), (wall_rect.left, y), (wall_rect.right, y), 1)
            for x in range(wall_rect.left + 25, wall_rect.right, 30):
                pygame.draw.line(surf, (160, 100, 45), (x, wall_rect.top), (x, wall_rect.bottom), 1)
            pygame.draw.rect(surf, (126, 78, 30), wall_rect, width=2)

            # Tumpukan Kayu Bakar di Teras Kiri (Sesuai Foto)
            wood_rect = pygame.Rect(wall_rect.left + 6, wall_rect.top + 38, 48, 52)
            pygame.draw.rect(surf, (120, 75, 35), wood_rect, border_radius=2)
            for row in range(5):
                for col in range(4):
                    lx = wood_rect.left + 6 + col * 10
                    ly = wood_rect.top + 6 + row * 10
                    pygame.draw.circle(surf, (80, 45, 20), (lx, ly), 5)
                    pygame.draw.circle(surf, (215, 165, 110), (lx, ly), 4)
                    pygame.draw.circle(surf, (140, 90, 45), (lx, ly), 1)

            # Atap Genteng Merah Terakota Shingle (Overlap 3D Tiles)
            roof_poly = [
                (10, 85),
                (w - 10, 85),
                (wall_rect.centerx + 40, 12),
                (wall_rect.centerx - 40, 12)
            ]
            pygame.draw.polygon(surf, (191, 73, 45), roof_poly)
            # Pola baris genteng shingle dengan highlight dan shadow
            for ry in range(20, 85, 9):
                ratio = (ry - 12) / 73.0
                left_x = int(wall_rect.centerx - 40 - ratio * (wall_rect.centerx - 40 - 10))
                right_x = int(wall_rect.centerx + 40 + ratio * (w - 10 - wall_rect.centerx - 40))
                pygame.draw.line(surf, (225, 105, 75), (left_x, ry), (right_x, ry), 2)
                pygame.draw.line(surf, (136, 41, 20), (left_x, ry + 2), (right_x, ry + 2), 1)
                # Sambungan genteng
                for tx in range(left_x + 8, right_x - 8, 12):
                    pygame.draw.line(surf, (136, 41, 20), (tx, ry - 7), (tx, ry), 1)
            pygame.draw.polygon(surf, (100, 30, 15), roof_poly, width=3)

            # Jendela Loteng Segitiga Kecil (Attic Vent Window)
            attic_x, attic_y = wall_rect.centerx - 5, 42
            pygame.draw.circle(surf, (130, 80, 35), (attic_x, attic_y), 9)
            pygame.draw.circle(surf, (110, 195, 245), (attic_x, attic_y), 7)
            pygame.draw.line(surf, (90, 50, 20), (attic_x - 7, attic_y), (attic_x + 7, attic_y), 2)
            pygame.draw.line(surf, (90, 50, 20), (attic_x, attic_y - 7), (attic_x, attic_y + 7), 2)

            # Cerobong Asap Batu
            chimney = pygame.Rect(wall_rect.right - 45, 6, 24, 45)
            pygame.draw.rect(surf, (125, 128, 135), chimney)
            # Tekstur batu bata cerobong
            for cy in range(chimney.top, chimney.bottom, 8):
                pygame.draw.line(surf, (85, 88, 95), (chimney.left, cy), (chimney.right, cy), 1)
            pygame.draw.rect(surf, (70, 72, 78), chimney, width=2)
            pygame.draw.rect(surf, (60, 62, 68), (chimney.left - 2, chimney.top - 4, chimney.width + 4, 6))

            # Pintu Depan Kayu dengan Kusen & Gagang Emas
            door_rect = pygame.Rect(wall_rect.centerx - 12, wall_rect.bottom - 46, 26, 46)
            pygame.draw.rect(surf, (150, 88, 38), door_rect, border_radius=2)
            pygame.draw.rect(surf, (85, 45, 18), door_rect, width=2, border_radius=2)
            # Panel dalam pintu & kaca atas
            pygame.draw.rect(surf, (180, 220, 245), (door_rect.left + 5, door_rect.top + 6, 16, 14), border_radius=1)
            pygame.draw.circle(surf, (255, 215, 60), (door_rect.right - 5, door_rect.centery + 6), 3)

            # Jendela Kaca Biru dengan Kotak Bunga
            win_rect = pygame.Rect(wall_rect.centerx - 62, wall_rect.top + 32, 28, 28)
            pygame.draw.rect(surf, (120, 205, 250), win_rect)
            pygame.draw.rect(surf, (95, 55, 25), win_rect, width=2)
            pygame.draw.line(surf, (95, 55, 25), (win_rect.centerx, win_rect.top), (win_rect.centerx, win_rect.bottom), 2)
            pygame.draw.line(surf, (95, 55, 25), (win_rect.left, win_rect.centery), (win_rect.right, win_rect.centery), 2)
            # Kotak bunga planter di bawah jendela
            planter = pygame.Rect(win_rect.left - 3, win_rect.bottom, win_rect.width + 6, 9)
            pygame.draw.rect(surf, (140, 85, 45), planter, border_radius=2)
            # Bunga warna-warni (Pink, Kuning, Biru)
            flowers = [(win_rect.left + 2, (255, 105, 180)), (win_rect.left + 10, (255, 220, 60)), 
                       (win_rect.left + 18, (100, 160, 255)), (win_rect.left + 26, (255, 80, 80))]
            for fx, fcol in flowers:
                pygame.draw.circle(surf, fcol, (fx, win_rect.bottom + 2), 3)

            # Teras Kayu Depan (Porch Steps)
            porch_rect = pygame.Rect(wall_rect.left + 15, wall_rect.bottom, wall_rect.width - 30, 18)
            pygame.draw.rect(surf, (190, 130, 68), porch_rect)
            pygame.draw.rect(surf, (110, 65, 25), porch_rect, width=2)
            for step_y in range(porch_rect.top, porch_rect.bottom, 6):
                pygame.draw.line(surf, (150, 95, 45), (porch_rect.left, step_y), (porch_rect.right, step_y), 1)

            # Kotak Surat Kayu (Mailbox)
            mb_pole = pygame.Rect(wall_rect.right + 12, wall_rect.bottom - 12, 6, 26)
            pygame.draw.rect(surf, (110, 65, 30), mb_pole)
            mb_box = pygame.Rect(wall_rect.right + 6, wall_rect.bottom - 26, 18, 15)
            pygame.draw.rect(surf, (180, 60, 45), mb_box, border_radius=3)
            pygame.draw.rect(surf, (100, 30, 20), mb_box, width=1, border_radius=3)

            cls._cache["farmhouse"] = surf
        return cls._cache["farmhouse"]

    @classmethod
    def get_stone_well(cls):
        if "well" not in cls._cache:
            w, h = 90, 100
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            cx = w // 2

            # Badan Sumur Batu Bundar
            base_rect = pygame.Rect(cx - 36, 45, 72, 48)
            pygame.draw.ellipse(surf, (135, 138, 145), base_rect)
            # Lapisan batu bata melingkar
            for layer in range(4):
                ly = 52 + layer * 10
                pygame.draw.ellipse(surf, (110, 114, 122), (cx - 35, ly, 70, 12), width=1)
                for stone_x in range(cx - 30, cx + 30, 14):
                    pygame.draw.line(surf, (75, 78, 85), (stone_x, ly), (stone_x + 2, ly + 9), 1)
            pygame.draw.ellipse(surf, (65, 68, 75), base_rect, width=2)

            # Air Sumur Dalam (Pantulan Biru Mengkilap)
            water_rect = pygame.Rect(cx - 26, 52, 52, 22)
            pygame.draw.ellipse(surf, (35, 110, 175), water_rect)
            pygame.draw.ellipse(surf, (80, 180, 240), (cx - 18, 56, 36, 12))
            pygame.draw.ellipse(surf, (200, 235, 255), (cx - 10, 58, 20, 6))

            # Tiang Kayu Penopang Atap
            pygame.draw.rect(surf, (120, 75, 35), (cx - 32, 18, 6, 48))
            pygame.draw.rect(surf, (120, 75, 35), (cx + 26, 18, 6, 48))
            # Palang kayu atas
            pygame.draw.rect(surf, (100, 60, 25), (cx - 34, 18, 68, 6))

            # Tali & Katrol Timba
            pygame.draw.line(surf, (200, 180, 130), (cx, 22), (cx, 55), 2)
            # Ember timba kayu
            pygame.draw.rect(surf, (140, 85, 40), (cx - 6, 52, 12, 10), border_radius=1)
            pygame.draw.line(surf, (70, 70, 70), (cx - 6, 55), (cx + 6, 55), 1)

            # Atap Genteng Kayu Shingle Segitiga
            roof_pts = [(cx - 40, 24), (cx + 40, 24), (cx, 2)]
            pygame.draw.polygon(surf, (185, 65, 45), roof_pts)
            for sy in range(6, 24, 5):
                half_w = int(40 * (sy / 24.0))
                pygame.draw.line(surf, (220, 95, 70), (cx - half_w, sy), (cx + half_w, sy), 2)
                pygame.draw.line(surf, (120, 35, 20), (cx - half_w, sy + 1), (cx + half_w, sy + 1), 1)
            pygame.draw.polygon(surf, (90, 25, 15), roof_pts, width=2)

            cls._cache["well"] = surf
        return cls._cache["well"]

    @classmethod
    def get_shipping_bin(cls):
        """Peti Pengiriman Kayu Khas Stardew Valley (Wooden Shipping Bin)"""
        if "shipping_bin" not in cls._cache:
            w, h = 58, 48
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            # Kotak bawah
            box = pygame.Rect(4, 16, 50, 28)
            pygame.draw.rect(surf, (166, 106, 56), box, border_radius=3)
            for y in range(box.top + 6, box.bottom, 7):
                pygame.draw.line(surf, (120, 70, 30), (box.left, y), (box.right, y), 1)
            pygame.draw.rect(surf, (80, 45, 18), box, width=2, border_radius=3)

            # Tutup Lengkung Atas
            lid = pygame.Rect(2, 4, 54, 18)
            pygame.draw.ellipse(surf, (190, 125, 68), lid)
            pygame.draw.ellipse(surf, (95, 50, 20), lid, width=2)

            # Sabuk Besi Pengikat & Gembok Emas
            pygame.draw.line(surf, (75, 78, 85), (box.left + 12, box.top), (box.left + 12, box.bottom), 3)
            pygame.draw.line(surf, (75, 78, 85), (box.right - 12, box.top), (box.right - 12, box.bottom), 3)
            pygame.draw.rect(surf, (255, 215, 60), (box.centerx - 4, box.top - 2, 8, 8), border_radius=1)

            cls._cache["shipping_bin"] = surf
        return cls._cache["shipping_bin"]

    @classmethod
    def get_beehive(cls):
        """Kotak Lebah Khas Stardew Valley dengan Indikator Madu"""
        if "beehive" not in cls._cache:
            w, h = 32, 42
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            # Tiang bawah
            pygame.draw.rect(surf, (120, 75, 35), (14, 28, 4, 12))
            # Kotak madu
            pygame.draw.rect(surf, (215, 160, 85), (4, 10, 24, 20), border_radius=2)
            pygame.draw.rect(surf, (130, 80, 30), (4, 10, 24, 20), width=2, border_radius=2)
            # Pintu masuk lebah
            pygame.draw.rect(surf, (50, 30, 10), (12, 22, 8, 4))
            # Atap genteng kecil
            pygame.draw.polygon(surf, (175, 60, 40), [(2, 12), (30, 12), (16, 2)])
            pygame.draw.polygon(surf, (90, 25, 15), [(2, 12), (30, 12), (16, 2)], width=1)
            # Gelembung toples madu siap panen
            pygame.draw.circle(surf, (255, 255, 255), (16, 6), 6)
            pygame.draw.circle(surf, (255, 215, 60), (16, 6), 4)

            cls._cache["beehive"] = surf
        return cls._cache["beehive"]

    @classmethod
    def get_scarecrow(cls):
        """Orang-orangan Sawah Khas Stardew Valley (Scarecrow)"""
        if "scarecrow" not in cls._cache:
            w, h = 32, 48
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            # Tiang kayu
            pygame.draw.rect(surf, (120, 75, 35), (14, 24, 4, 24))
            # Baju biru
            pygame.draw.rect(surf, (45, 95, 165), (8, 16, 16, 14), border_radius=2)
            # Kepala labu / jerami
            pygame.draw.circle(surf, (240, 140, 40), (16, 11), 6)
            # Topi jerami petani
            pygame.draw.ellipse(surf, (220, 185, 90), (4, 4, 24, 8))
            pygame.draw.circle(surf, (190, 150, 60), (16, 5), 5)
            pygame.draw.line(surf, (180, 40, 30), (6, 7), (26, 7), 2)

            cls._cache["scarecrow"] = surf
        return cls._cache["scarecrow"]

    @classmethod
    def get_tree(cls, is_cherry=False):
        key = "tree_cherry" if is_cherry else "tree_oak"
        if key not in cls._cache:
            w, h = 100, 120
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            cx, cy = w // 2, 70

            # Batang Pohon Bertekstur Kayu dengan Akar
            trunk = pygame.Rect(cx - 10, cy + 10, 20, 42)
            pygame.draw.rect(surf, (110, 68, 38), trunk, border_radius=4)
            for tx in range(trunk.left + 3, trunk.right - 2, 5):
                pygame.draw.line(surf, (80, 45, 20), (tx, trunk.top), (tx, trunk.bottom), 1)
            # Akar mencengkeram tanah
            pygame.draw.polygon(surf, (90, 50, 25), [(cx - 14, h - 8), (cx - 6, cy + 35), (cx - 8, h - 8)])
            pygame.draw.polygon(surf, (90, 50, 25), [(cx + 14, h - 8), (cx + 6, cy + 35), (cx + 8, h - 8)])

            if is_cherry:
                # Daun Sakura Merah Muda Berlapis (Cherry Blossom)
                colors = [(225, 125, 165), (245, 160, 195), (255, 190, 220), (255, 225, 240)]
                clumps = [
                    (cx, cy - 25, 32), (cx - 22, cy - 12, 26), (cx + 22, cy - 12, 26),
                    (cx - 14, cy + 10, 24), (cx + 14, cy + 10, 24), (cx, cy, 28)
                ]
                for px, py, rad in clumps:
                    pygame.draw.circle(surf, colors[0], (px, py + 2), rad)
                    pygame.draw.circle(surf, colors[1], (px, py), rad - 2)
                    pygame.draw.circle(surf, colors[2], (px - 2, py - 3), rad - 6)
                    pygame.draw.circle(surf, colors[3], (px - 4, py - 6), rad - 12)
            else:
                # Daun Pohon Oak Hijau Lebat Berlapis (Sesuai Foto Stardew)
                c_dark = (35, 105, 45)
                c_mid = (55, 155, 60)
                c_light = (85, 200, 75)
                c_hi = (135, 235, 100)
                clumps = [
                    (cx, cy - 26, 34), (cx - 24, cy - 10, 28), (cx + 24, cy - 10, 28),
                    (cx - 16, cy + 12, 26), (cx + 16, cy + 12, 26), (cx, cy, 32)
                ]
                for px, py, rad in clumps:
                    pygame.draw.circle(surf, c_dark, (px, py + 3), rad)
                    pygame.draw.circle(surf, c_mid, (px, py), rad - 2)
                    pygame.draw.circle(surf, c_light, (px - 2, py - 4), rad - 7)
                    pygame.draw.circle(surf, c_hi, (px - 5, py - 7), rad - 14)

            cls._cache[key] = surf
        return cls._cache[key]


    # =========================================================================
    # ASET AUTENTIK DARI FOTO REFERENSI RESMI (RAMUAN TERAKHIR: ALKEMIS DESA)
    # =========================================================================

    @classmethod
    def load_png(cls, rel_path, colorkey=None):
        if rel_path not in cls._cache:
            import os
            full_path = os.path.join(os.path.dirname(__file__), rel_path)
            if os.path.exists(full_path):
                img = pygame.image.load(full_path)
                if colorkey is not None:
                    img.set_colorkey(colorkey)
                cls._cache[rel_path] = img
            else:
                return None
        return cls._cache[rel_path]

    @classmethod
    def get_student_sprite(cls, action="idle", direction="down", walk_frame=0):
        """
        Sprite Karakter Murid Alkemis (Sesuai Lembar Aset 4x4 Resmi):
        Rambut cokelat, kacamata bulat, jubah alkemis bergaris emas, tas selempang.
        """
        step = int(walk_frame) % 2
        key = f"student_{action}_{direction}_{step}"
        if key not in cls._cache:
            img = None
            if action == "battle_fire":
                img = cls.load_png("assets/player/player_attack_fire.png")
            elif action == "battle_victory":
                img = cls.load_png("assets/player/player_victory_1.png")
            elif action == "battle_potion":
                img = cls.load_png("assets/player/player_side_potion.png")
            elif action == "battle_cast":
                img = cls.load_png("assets/player/player_cast_point.png")
            elif direction == "up":
                if action == "walk":
                    img = cls.load_png("assets/player/player_back_idle.png" if step == 0 else "assets/player/player_back_walk_2.png")
                else:
                    img = cls.load_png("assets/player/player_back_idle.png")
            elif direction == "left":
                img = cls.load_png("assets/player/player_side_left.png")
            elif direction == "right":
                img = cls.load_png("assets/player/player_side_right.png")
                if img:
                    img = pygame.transform.flip(img, True, False)
            else:  # down / front
                if action == "walk":
                    img = cls.load_png("assets/player/player_walk_front_1.png" if step == 0 else "assets/player/player_walk_front_2.png")
                else:
                    img = cls.load_png("assets/player/player_idle_front.png")

            # Fallback: untuk arah "up" gunakan sprite belakang agar tidak flip ke depan
            if not img:
                if direction == "up":
                    img = cls.load_png("assets/player/player_back_idle.png")
                if not img:
                    img = cls.load_png("assets/player/player_idle_front.png")
            cls._cache[key] = img
        return cls._cache[key]

    @classmethod
    def _load_scaled(cls, cache_key: str, path: str, scale: float):
        """Helper: load PNG dan scale, dengan cache."""
        if cache_key not in cls._cache:
            base = cls.load_png(path)
            if base and scale != 1.0:
                cls._cache[cache_key] = pygame.transform.scale(
                    base, (int(base.get_width() * scale), int(base.get_height() * scale))
                )
            else:
                cls._cache[cache_key] = base
        return cls._cache[cache_key]

    @classmethod
    def get_enemy_sprite(cls, name_key, scale=1.0):
        """Sprite monster autentik dari lembar aset (Slime Lumut, Pohon Tua, Kelelawar Batu)"""
        k = name_key.lower()
        if "slime" in k:
            path = "assets/enemies/slime_transparent.png"
        elif "pohon" in k or "tree" in k:
            path = "assets/enemies/tree_transparent.png"
        elif "kelelawar" in k or "bat" in k:
            path = "assets/enemies/bat_transparent.png"
        elif "ratu" in k or "boss" in k or "kabut" in k:
            path = "assets/enemies/boss_idle_transparent.png"
        else:
            return None
        return cls._load_scaled(f"enemy_{name_key}_{scale}", path, scale)

    @classmethod
    def get_boss_sprite(cls, action="idle", scale=1.0):
        """Sprite Bos Ratu Kabut Terkutuk (Idle & Casting Pose)"""
        path = "assets/enemies/boss_cast_transparent.png" if action == "cast" else "assets/enemies/boss_idle_transparent.png"
        return cls._load_scaled(f"boss_ratu_{action}_{scale}", path, scale)

    @classmethod
    def get_boss_fx(cls, fx_name, scale=1.0):
        """Efek Jurus Bos: duri, kabut, simbol, teras"""
        return cls._load_scaled(f"boss_fx_{fx_name}_{scale}", f"assets/enemies/{fx_name}_transparent.png", scale)

    @classmethod
    def get_zephyr_sprite(cls, height=110):
        cache_key = f"zephyr_sprite_{height}"
        if cache_key not in cls._cache:
            sprite = cls.load_png("assets/npcs/guru_zephyr.png")
            if sprite:
                width = round(sprite.get_width() * height / sprite.get_height())
                cls._cache[cache_key] = pygame.transform.scale(sprite, (width, height))
            else:
                cls._cache[cache_key] = None
        return cls._cache[cache_key]

    @classmethod
    def get_portrait(cls, name_key):
        """Portrait profil karakter untuk HP Bar di Arena Pertarungan"""
        k = name_key.lower()
        if "player" in k or "elian" in k or "murid" in k:
            return cls.load_png("assets/player/player_portrait.png")
        elif "ratu" in k or "kabut" in k:
            return cls.load_png("assets/enemies/boss_ratu_kabut_portrait.png")
        else:
            return cls.load_png("assets/enemies/slime_portrait.png")

    @classmethod
    def get_explosion_fx(cls):
        return cls.load_png("assets/ui/fx_explosion.png")
