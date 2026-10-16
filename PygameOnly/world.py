"""Sistem Dunia & Penjelajahan (World Map)"""

import pygame
import math
from constants import GT_BORDER_CYAN, GT_SLOT_SELECTED
from entities import HarvestPoint
from sprites import StardewSpriteCache

class WorldMap:
    def __init__(self, area_id=0):
        self.area_id = area_id  # 0: Desa Kebun Stardew, 1: Hutan, 2: Gua, 3: Rawa
        self.width = 960
        self.height = 640
        self.colliders = []
        self.harvest_points = []
        self.enemies = []
        self.interactables = []
        self.title = ""
        self.anim_tick = 0

        self._build_area(area_id)

    def _build_area(self, area_id):
        self.colliders.clear()
        self.harvest_points.clear()
        self.enemies.clear()
        self.interactables.clear()

        # Batas layar peta
        self.colliders.append(pygame.Rect(0, 0, 960, 56))
        self.colliders.append(pygame.Rect(0, 600, 960, 40))
        self.colliders.append(pygame.Rect(0, 56, 20, 584))
        self.colliders.append(pygame.Rect(940, 56, 20, 584))

        if area_id == 0:
            # ===============================================================
            # DESA ALKEMIS: REKREASI LENGKAP STARDEW VALLEY FARM (SESUAI FOTO)
            # ===============================================================
            self.title = "🌾 Pedesaan"

            # 1. Farmhouse Kayu (Posisi Tengah Atas Sesuai Foto)
            # Ukuran sprite: 260 x 190, ditempatkan di (280, 50)
            house_collider = pygame.Rect(310, 110, 200, 120)
            self.colliders.append(house_collider)

            # Teras Rumah (Kasur / Tempat Istirahat HP)
            self.interactables.append({
                "rect": pygame.Rect(380, 200, 70, 40),
                "type": "BED",
                "label": "Teras Rumah (Tidur & Pulihkan HP Penuh)"
            })

            # 2. Peti Pengiriman Kayu (Shipping Bin) di Kanan Rumah (Sesuai Foto)
            bin_collider = pygame.Rect(645, 135, 58, 48)
            self.colliders.append(bin_collider)
            self.interactables.append({
                "rect": bin_collider,
                "type": "STORAGE",
                "label": "Peti Pengiriman Bahan (Buka Ransel & Peti)"
            })

            # 3. Sumur Batu Khas Stardew Valley di Kanan Tengah (Sesuai Foto)
            well_collider = pygame.Rect(690, 410, 80, 75)
            self.colliders.append(well_collider)
            self.interactables.append({
                "rect": well_collider,
                "type": "WELL",
                "label": "Sumur Batu Alami (Ambil Air Embun)"
            })

            # 4. NPC Guru Zephyr di dekat Kotak Lebah
            self.interactables.append({
                "rect": pygame.Rect(230, 185, 45, 45),
                "type": "NPC_MENTOR",
                "label": "Guru Zephyr: 'Rawat kebun dan racik ramuan untuk tundukkan para Lord!'"
            })

            # 5. Pagar Kayu Pembatas Kebun (Sesuai Foto)
            # Pagar kiri
            self.colliders.append(pygame.Rect(95, 200, 16, 380))
            # Pagar bawah
            self.colliders.append(pygame.Rect(95, 580, 760, 16))

            # 6. Gerbang Menuju Hutan (Kanan Jalan Tanah)
            self.interactables.append({
                "rect": pygame.Rect(875, 230, 65, 140),
                "type": "PORTAL_FOREST",
                "label": "Gerbang Menuju Hutan Berkabut ➔"
            })

            # 7. Petak Ladang Tanaman Panen (Tilled Soil Beds Sesuai Foto):
            # Petak Kiri Atas: Herba Hijau Daun (Trellis & Kale)
            self.harvest_points.append(HarvestPoint(210, 310, "daun", "Herba Kacang Rambat"))
            self.harvest_points.append(HarvestPoint(270, 310, "daun", "Herba Kacang Rambat"))
            self.harvest_points.append(HarvestPoint(210, 420, "daun", "Herba Tunas Hijau"))
            self.harvest_points.append(HarvestPoint(270, 420, "daun", "Herba Tunas Hijau"))

            # Petak Tengah: Kubis Hijau (Daun) & Strawberry Merah (Api)
            self.harvest_points.append(HarvestPoint(440, 310, "daun", "Kol Kebun Segar"))
            self.harvest_points.append(HarvestPoint(490, 310, "daun", "Kol Kebun Segar"))
            self.harvest_points.append(HarvestPoint(440, 450, "api", "Cabai Bara Pedas"))
            self.harvest_points.append(HarvestPoint(490, 450, "api", "Cabai Bara Pedas"))

            # Petak Kanan: Strawberry Rimbun (Api) & Geode Mineral (Batu)
            self.harvest_points.append(HarvestPoint(580, 310, "api", "Strawberry Bara"))
            self.harvest_points.append(HarvestPoint(620, 310, "api", "Strawberry Bara"))
            self.harvest_points.append(HarvestPoint(580, 450, "batu", "Batu Mineral Geode"))
            self.harvest_points.append(HarvestPoint(620, 450, "batu", "Kristal Ungu Kebun"))

            # Titik Air di Sumur Batu
            self.harvest_points.append(HarvestPoint(730, 500, "air", "Mata Air Sumur Batu"))

        elif area_id == 1:
            # AREA 1: HUTAN BERKABUT
            self.title = "🌲 Area 1: Hutan Berkabut"

            self.interactables.append({
                "rect": pygame.Rect(20, 250, 55, 130),
                "type": "PORTAL_VILLAGE",
                "label": "⬅ Kembali ke Kebun Desa"
            })

            trees = [
                pygame.Rect(170, 90, 90, 100),
                pygame.Rect(430, 120, 90, 90),
                pygame.Rect(290, 370, 110, 90),
                pygame.Rect(590, 350, 100, 100),
                pygame.Rect(230, 480, 90, 70),
            ]
            self.colliders.extend(trees)

            self.harvest_points.append(HarvestPoint(260, 230, "daun", "Herba Hutan"))
            self.harvest_points.append(HarvestPoint(520, 480, "daun", "Lumut Hijau"))
            self.harvest_points.append(HarvestPoint(380, 220, "air", "Mata Air Hutan"))
            self.harvest_points.append(HarvestPoint(730, 180, "api", "Bunga Bara Hutan"))
            self.harvest_points.append(HarvestPoint(480, 310, "batu", "Batu Runik Lumut"))

            self.enemies.append({"key": "slime", "x": 420, "y": 270, "radius": 18})
            self.enemies.append({"key": "slime", "x": 640, "y": 210, "radius": 18})

            self.interactables.append({
                "rect": pygame.Rect(810, 220, 100, 170),
                "type": "BOSS_FOREST",
                "label": "👑 Gerbang Takhta: LORD DVALIN (BOSS)"
            })

        elif area_id == 2:
            # AREA 2: GUA KRISTAL
            self.title = "💎 Area 2: Gua Kristal"

            self.interactables.append({
                "rect": pygame.Rect(20, 250, 55, 130),
                "type": "PORTAL_VILLAGE",
                "label": "⬅ Kembali ke Kebun Desa"
            })

            rocks = [
                pygame.Rect(170, 110, 100, 90),
                pygame.Rect(350, 140, 130, 70),
                pygame.Rect(270, 370, 90, 110),
                pygame.Rect(570, 330, 100, 90),
                pygame.Rect(630, 120, 90, 90)
            ]
            self.colliders.extend(rocks)

            self.harvest_points.append(HarvestPoint(250, 310, "batu", "Geode Mineral"))
            self.harvest_points.append(HarvestPoint(450, 410, "batu", "Kristal Amethyst"))
            self.harvest_points.append(HarvestPoint(410, 110, "air", "Stalaktit Gua"))
            self.harvest_points.append(HarvestPoint(670, 440, "air", "Embun Murni"))
            self.harvest_points.append(HarvestPoint(510, 230, "api", "Bara Geotermal"))

            self.enemies.append({"key": "kelelawar", "x": 470, "y": 250, "radius": 18})
            self.enemies.append({"key": "kelelawar", "x": 710, "y": 290, "radius": 18})

            self.interactables.append({
                "rect": pygame.Rect(810, 220, 100, 170),
                "type": "BOSS_CAVE",
                "label": "👑 Inti Kristal: LORD BALTOR (BOSS)"
            })

        elif area_id == 3:
            # AREA 3: RAWA BERACUN
            self.title = "☠️ Area 3: Rawa Beracun"

            self.interactables.append({
                "rect": pygame.Rect(20, 250, 55, 130),
                "type": "PORTAL_VILLAGE",
                "label": "⬅ Kembali ke Kebun Desa"
            })

            swamps = [
                pygame.Rect(210, 110, 110, 100),
                pygame.Rect(430, 140, 100, 90),
                pygame.Rect(330, 380, 120, 90),
                pygame.Rect(610, 360, 100, 100),
            ]
            self.colliders.extend(swamps)

            self.harvest_points.append(HarvestPoint(270, 310, "api", "Bara Rawa Ungu"))
            self.harvest_points.append(HarvestPoint(530, 450, "batu", "Fosil Rawa"))
            self.harvest_points.append(HarvestPoint(450, 290, "daun", "Herba Asam"))
            self.harvest_points.append(HarvestPoint(670, 190, "air", "Embun Rawa"))

            self.enemies.append({"key": "katak", "x": 470, "y": 240, "radius": 18})
            self.enemies.append({"key": "katak", "x": 660, "y": 310, "radius": 18})

            self.interactables.append({
                "rect": pygame.Rect(805, 215, 110, 180),
                "type": "BOSS_SWAMP",
                "label": "👑 Takhta Kabut: HIGH LORD VESPERA (FINAL BOSS)"
            })

    def update(self):
        self.anim_tick += 0.05
        for hp in self.harvest_points:
            hp.update()

    def draw(self, surface, fonts):
        if self.area_id == 0:
            # =========================================================================
            # RENDER AUTENTIK STARDEW VALLEY FARM (PERSIS FOTO REFERENSI PENGGUNA)
            # =========================================================================
            
            # 1. Rumput Hijau Segar Stardew Valley (#6db533)
            surface.fill((109, 181, 51))

            # Tekstur Rumput Berbintik Dithering Lembut Khas Stardew
            for gx in range(0, self.width, 32):
                for gy in range(56, self.height, 32):
                    if (gx + gy) % 64 == 0:
                        pygame.draw.rect(surface, (98, 168, 44), (gx, gy, 8, 4))
                    elif (gx + gy) % 48 == 0:
                        pygame.draw.rect(surface, (120, 195, 58), (gx + 12, gy + 8, 6, 3))


            # 2. Jalan Tanah Kuning-Keemasan Natural (Dirt Path #dead5f)
            # Jalur utama: dari gerbang kanan ke tengah peta, lalu ke teras rumah
            # Jalur 1 – horizontal dari gerbang kanan ke pusat
            path_polys = [
                # Jalan horizontal sepanjang tepi kanan, dari gerbang ke tengah
                [(840, 225), (960, 225), (960, 375), (840, 375)],
                # Jalan melengkung dari tengah kanan ke arah bawah rumah
                [(420, 215), (840, 215), (840, 300), (580, 300), (500, 340), (420, 340)],
                # Jalan dari teras rumah (bawah) ke jalur utama
                [(420, 215), (500, 215), (500, 570), (420, 570)],
            ]
            for p in path_polys:
                pygame.draw.polygon(surface, (222, 173, 95), p)
                pygame.draw.polygon(surface, (198, 150, 78), p, width=2)

            # Kerikil-kerikil kecil di jalan tanah (Sesuai Foto)
            pebbles = [
                (230, 285), (320, 275), (460, 280), (540, 280), (650, 290), (780, 310),
                (390, 380), (430, 490), (600, 490), (740, 260), (820, 330)
            ]
            for px, py in pebbles:
                pygame.draw.circle(surface, (160, 115, 60), (px, py), 2)
                pygame.draw.circle(surface, (240, 205, 140), (px + 1, py), 1)

            # Bunga-Bunga Liar dan Semanggi di Rumput (Sesuai Foto)
            wildflowers = [
                (55, 160, (255, 255, 255)), (75, 240, (245, 140, 190)), (130, 95, (100, 170, 255)),
                (290, 75, (255, 220, 80)), (610, 85, (255, 255, 255)), (820, 140, (245, 140, 190)),
                (860, 520, (100, 170, 255)), (710, 560, (255, 220, 80)), (320, 560, (255, 255, 255))
            ]
            for fx, fy, fcol in wildflowers:
                pygame.draw.circle(surface, fcol, (fx, fy), 3)
                pygame.draw.circle(surface, (255, 240, 100), (fx, fy), 1)

            # 3. Pagar Kayu Patok Berpalang (Wooden Post & Rail Fence Sesuai Foto)
            # Pagar vertikal kiri
            for fy in range(200, 580, 26):
                pygame.draw.rect(surface, (155, 100, 52), (92, fy, 14, 26), border_radius=3)
                pygame.draw.rect(surface, (95, 55, 25), (92, fy, 14, 26), width=1, border_radius=3)
            pygame.draw.line(surface, (170, 115, 60), (99, 205), (99, 580), 3)
            pygame.draw.line(surface, (110, 65, 30), (101, 205), (101, 580), 1)

            # Pagar horizontal bawah
            for fx in range(95, 840, 26):
                pygame.draw.rect(surface, (155, 100, 52), (fx, 574, 14, 26), border_radius=3)
                pygame.draw.rect(surface, (95, 55, 25), (fx, 574, 14, 26), width=1, border_radius=3)
            pygame.draw.line(surface, (170, 115, 60), (95, 582), (835, 582), 3)

            # Semak Belukar Bunga Berdaun Rapat di Tepi Pagar (Sesuai Foto)
            for by in range(210, 570, 36):
                pygame.draw.circle(surface, (45, 140, 60), (82, by), 12)
                pygame.draw.circle(surface, (70, 185, 85), (80, by - 2), 8)
                pygame.draw.circle(surface, (255, 140, 180), (82, by - 1), 3)

            # 4. Kotak Sarang Lebah (Beehives) di Samping Rumah (Sesuai Foto)
            beehive_img = StardewSpriteCache.get_beehive()
            for bi in range(5):
                surface.blit(beehive_img, (120 + bi * 32, 110))

            # 5. Pohon Oak Rimbun di Kiri Atas (Sesuai Foto)
            tree_oak = StardewSpriteCache.get_tree(is_cherry=False)
            surface.blit(tree_oak, (25, 45))

            # 6. Pohon Sakura Merah Muda (Cherry Blossom Tree) di Kanan Bawah (Sesuai Foto)
            tree_cherry = StardewSpriteCache.get_tree(is_cherry=True)
            surface.blit(tree_cherry, (840, 380))

            # Kelopak Bunga Sakura Jatuh di Tanah
            petal_drops = [(810, 480), (835, 510), (880, 530), (840, 550), (790, 530)]
            for px, py in petal_drops:
                pygame.draw.ellipse(surface, (245, 160, 195), (px, py, 6, 4))

            # 7. Tunggul Pohon (Tree Stump) Khas Stardew di Kanan Bawah (Sesuai Foto)
            stump_cx, stump_cy = 730, 550
            pygame.draw.ellipse(surface, (120, 75, 40), (stump_cx - 24, stump_cy - 12, 48, 28))
            pygame.draw.ellipse(surface, (195, 145, 95), (stump_cx - 18, stump_cy - 9, 36, 20))
            pygame.draw.line(surface, (90, 50, 20), (stump_cx - 6, stump_cy - 2), (stump_cx + 8, stump_cy - 2), 2)
            # Tunas akar
            pygame.draw.line(surface, (90, 50, 20), (stump_cx - 16, stump_cy + 8), (stump_cx - 24, stump_cy + 14), 3)
            pygame.draw.line(surface, (90, 50, 20), (stump_cx + 16, stump_cy + 8), (stump_cx + 24, stump_cy + 14), 3)

            # 8. Orang-orangan Sawah (Scarecrow) di Tengah Kebun (Sesuai Foto)
            scarecrow_img = StardewSpriteCache.get_scarecrow()
            surface.blit(scarecrow_img, (360, 365))

            # 9. Rumah Kayu Alkemis (Farmhouse Sprite Lengkap Sesuai Foto)
            house_img = StardewSpriteCache.get_farmhouse()
            surface.blit(house_img, (280, 35))

            # 10. Peti Pengiriman Kayu (Shipping Bin) di Samping Tangga Rumah
            bin_img = StardewSpriteCache.get_shipping_bin()
            surface.blit(bin_img, (645, 135))

            # Tong Sampah Logam di Samping Peti Pengiriman (Sesuai Foto)
            trash_rect = pygame.Rect(620, 145, 18, 26)
            pygame.draw.rect(surface, (140, 145, 150), trash_rect, border_radius=2)
            pygame.draw.rect(surface, (80, 85, 90), trash_rect, width=1, border_radius=2)
            pygame.draw.ellipse(surface, (160, 165, 170), (trash_rect.left - 2, trash_rect.top - 3, trash_rect.width + 4, 7))

            # 11. Sumur Batu Megah Beratap Genteng (Stone Well Sprite Sesuai Foto)
            well_img = StardewSpriteCache.get_stone_well()
            surface.blit(well_img, (685, 395))

            # 12. NPC Guru Zephyr dengan sprite baru dari referensi pengguna
            zephyr_sprite = StardewSpriteCache.get_zephyr_sprite()
            if zephyr_sprite:
                surface.blit(zephyr_sprite, zephyr_sprite.get_rect(midbottom=(252, 226)))
            # Label nama melayang di atas sprite
            if fonts:
                name_surf = fonts["small"].render("Guru Zephyr", True, (200, 100, 255))
                surface.blit(name_surf, (252 - name_surf.get_width() // 2, 92))

        else:
            # Area Liar: Hutan, Gua, atau Rawa
            theme_color = (20, 48, 32) if self.area_id == 1 else ((18, 32, 58) if self.area_id == 2 else (35, 18, 48))
            surface.fill(theme_color)

            tile_size = 48
            for x in range(0, self.width, tile_size):
                pygame.draw.line(surface, tuple(min(255, c + 14) for c in theme_color), (x, 56), (x, self.height))
            for y in range(56, self.height, tile_size):
                pygame.draw.line(surface, tuple(min(255, c + 14) for c in theme_color), (0, y), (self.width, y))

            for c in self.colliders[4:]:
                if self.area_id == 1:
                    pygame.draw.rect(surface, (90, 55, 30), (c.centerx - 12, c.centery, 24, c.height // 2))
                    pygame.draw.rect(surface, (35, 130, 50), (c.left, c.top, c.width, c.height // 2 + 10), border_radius=8)
                elif self.area_id == 2:
                    pts = [(c.centerx, c.top), (c.right, c.centery), (c.right - 14, c.bottom), (c.left + 14, c.bottom), (c.left, c.centery)]
                    pygame.draw.polygon(surface, (95, 90, 160), pts)
                    pygame.draw.polygon(surface, GT_BORDER_CYAN, pts, width=2)
                else:
                    pygame.draw.ellipse(surface, (55, 20, 65), c)
                    pygame.draw.ellipse(surface, (110, 45, 130), c, width=2)

        # Gambar Titik Panen Ladang Tanaman (Crops)
        for hp in self.harvest_points:
            hp.draw(surface)

        # Gambar Portal & Altar Lord
        for obj in self.interactables:
            r = obj["rect"]
            t = obj["type"]

            if "PORTAL" in t:
                col = (60, 210, 95) if "FOREST" in t else GT_BORDER_CYAN
                pygame.draw.rect(surface, (12, 35, 70), r, border_radius=8)
                pygame.draw.rect(surface, col, r, width=3, border_radius=8)
                arr = fonts["large"].render("➔" if "FOREST" in t else "⬅", True, col)
                surface.blit(arr, (r.centerx - arr.get_width() // 2, r.centery - arr.get_height() // 2))
            elif "BOSS" in t:
                pygame.draw.rect(surface, (35, 12, 45), r, border_radius=10)
                pygame.draw.rect(surface, (240, 45, 45), r, width=3, border_radius=10)
                title = fonts["small"].render("BOSS", True, GT_SLOT_SELECTED)
                surface.blit(title, title.get_rect(center=(r.centerx, r.top + 18)))

                boss_sprite = StardewSpriteCache.get_boss_sprite("idle", scale=0.65)
                if boss_sprite:
                    sprite_rect = boss_sprite.get_rect(center=(r.centerx, r.top + 82))
                    surface.blit(boss_sprite, sprite_rect)

                boss_names = {
                    "BOSS_FOREST": "DVALIN",
                    "BOSS_CAVE": "BALTOR",
                    "BOSS_SWAMP": "VESPERA",
                }
                boss_name = fonts["small"].render(boss_names.get(t, "LORD"), True, GT_SLOT_SELECTED)
                surface.blit(boss_name, boss_name.get_rect(center=(r.centerx, r.bottom - 17)))

        # Musuh berkeliaran
        for e in self.enemies:
            cx, cy = int(e["x"]), int(e["y"])
            bob = int(math.sin(self.anim_tick + cx) * 3)
            sprite_key = {"slime": "slime", "kelelawar": "bat"}.get(e["key"])
            scale = 0.85 if sprite_key == "slime" else 0.7
            enemy_sprite = (
                StardewSpriteCache.get_enemy_sprite(sprite_key, scale=scale)
                if sprite_key else None
            )

            pygame.draw.ellipse(
                surface, (20, 45, 15, 120),
                (cx - e["radius"], cy + e["radius"] - 4, e["radius"] * 2, 8)
            )
            if enemy_sprite:
                sprite_rect = enemy_sprite.get_rect(center=(cx, cy + bob))
                surface.blit(enemy_sprite, sprite_rect)
            else:
                col = (60, 180, 80) if e["key"] == "slime" else (
                    (150, 130, 180) if e["key"] == "kelelawar" else (180, 80, 180)
                )
                pygame.draw.circle(surface, col, (cx, cy + bob), e["radius"])
                pygame.draw.circle(surface, (255, 40, 40), (cx - 4, cy + bob - 2), 3)
                pygame.draw.circle(surface, (255, 40, 40), (cx + 4, cy + bob - 2), 3)
            em = fonts["small"].render("⚔️", True, (255, 255, 255))
            surface.blit(em, (cx - em.get_width() // 2, cy + bob - e["radius"] - 16))
