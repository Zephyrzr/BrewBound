import pygame
import math
from constants import PLAYER_MAX_HP, MAX_BAG_CAPACITY, GT_SLOT_SELECTED
from audio import audio
from sprites import StardewSpriteCache


class Player:
    def __init__(self, x=480, y=320):
        self.x = x
        self.y = y
        self.radius = 16
        self.speed = 3.6
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp

        # Tas ransel bawaan (Maksimal 10 item)
        self.bag = {
            "api": 3,
            "air": 2,
            "daun": 3,
            "batu": 2
        }

        # Peti Penyimpanan di Desa (Kapasitas Tak Terbatas)
        self.storage = {
            "api": 5,
            "air": 5,
            "daun": 5,
            "batu": 5
        }

        # Resep yang sudah diketahui pemain
        self.unlocked_recipes = {
            ("api", "api"),
            ("air", "daun"),
            ("air", "api"),
            ("batu", "daun")
        }

        self.unlocked_areas = [1]
        self.bosses_defeated = {
            "Pohon Tua": False,
            "Golem Kristal": False,
            "Ratu Kabut": False
        }

        self.walk_frame = 0
        self.facing_right = True
        self.facing = "down"
        self.is_moving = False

    @property
    def total_bag_items(self):
        return sum(self.bag.values())

    def can_carry(self, qty=1):
        return (self.total_bag_items + qty) <= MAX_BAG_CAPACITY

    def add_to_bag(self, item_name, qty=1):
        if not self.can_carry(qty):
            return False
        self.bag[item_name] = self.bag.get(item_name, 0) + qty
        return True

    def remove_from_bag(self, item_name, qty=1):
        if self.bag.get(item_name, 0) >= qty:
            self.bag[item_name] -= qty
            return True
        return False

    def rest_in_village(self):
        self.hp = self.max_hp
        audio.play("heal")

    def faint_penalty(self):
        self.hp = self.max_hp
        lost_items = []
        for elem in list(self.bag.keys()):
            lost = self.bag[elem] // 2
            if lost > 0:
                self.bag[elem] -= lost
                lost_items.append(f"{lost} {elem.capitalize()}")
        return lost_items

    def move(self, dx, dy, colliders, screen_rect):
        self.is_moving = False
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        if dx != 0 and abs(dx) >= abs(dy):
            if dx > 0:
                self.facing = "right"
                self.facing_right = True
            elif dx < 0:
                self.facing = "left"
                self.facing_right = False
        elif dy != 0:
            if dy > 0:
                self.facing = "down"
            elif dy < 0:
                self.facing = "up"

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        new_x = max(self.radius, min(screen_rect.width - self.radius, new_x))
        new_y = max(self.radius + 56, min(screen_rect.height - self.radius - 20, new_y))

        player_rect = pygame.Rect(new_x - self.radius, new_y - self.radius, self.radius * 2, self.radius * 2)
        collision = False
        for c in colliders:
            if player_rect.colliderect(c):
                collision = True
                break

        if not collision:
            self.x = new_x
            self.y = new_y
            if dx != 0 or dy != 0:
                self.is_moving = True
                self.walk_frame += 0.125

    def draw(self, surface):
        """
        Menggambar Karakter Murid Alkemis (Autentik dari Lembar Aset Resmi Pengguna):
        Rambut cokelat, kacamata, jubah abu-abu/hitam list emas, tas selempang.
        """
        cx, cy = int(self.x), int(self.y)
        bob = int(math.sin(self.walk_frame * 1.5) * 2) if self.is_moving else 0

        # Bayangan kaki di tanah
        pygame.draw.ellipse(surface, (20, 45, 20, 120), (cx - 16, cy + 12, 32, 9))

        action = "walk" if self.is_moving else "idle"
        sprite = StardewSpriteCache.get_student_sprite(action=action, direction=self.facing, walk_frame=self.walk_frame)
        if sprite:
            sw, sh = sprite.get_size()
            surface.blit(sprite, (cx - sw // 2, cy - sh + 14 + bob))


class Enemy:
    def __init__(self, data: dict, x=0, y=0):
        self.nama = data["nama"]
        self.area = data.get("area", 1)
        self.max_hp = data["hp"]
        self.hp = self.max_hp
        self.lemah = data["lemah"]
        self.atk = data.get("atk", 10)
        self.is_boss = data.get("is_boss", False)
        self.drop = data.get("drop", ["daun"])
        self.deskripsi = data.get("deskripsi", "")

        self.burn_turns = 0
        self.burn_dmg = 0
        self.stunned_turns = 0
        self.atk_debuff = 0
        self.atk_debuff_turns = 0
        self.blind_turns = 0

        self.x = x
        self.y = y
        self.radius = 24 if self.is_boss else 18
        self.float_tick = 0

    def apply_status(self, efek: dict):
        if not efek:
            return
        t = efek.get("tipe")
        if t == "burn":
            self.burn_turns = efek.get("durasi", 2)
            self.burn_dmg = efek.get("damage", 8)
        elif t == "stun":
            self.stunned_turns = efek.get("durasi", 1)
        elif t == "atk_down":
            self.atk_debuff = efek.get("nilai", 4)
            self.atk_debuff_turns = efek.get("durasi", 2)
        elif t == "blind":
            self.blind_turns = efek.get("durasi", 1)


class HarvestPoint:
    """Titik Panen Bergaya Tanaman Ladang Stardew Valley (Sesuai Foto Referensi)"""
    def __init__(self, x, y, elemen, item_name):
        self.x = x
        self.y = y
        self.elemen = elemen
        self.item_name = item_name
        self.radius = 16
        self.active = True
        self.respawn_timer = 0
        self.pulse = 0

    def update(self):
        self.pulse += 0.05
        if not self.active:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.active = True

    def harvest(self):
        if self.active:
            self.active = False
            self.respawn_timer = 450
            audio.play("harvest")
            return self.elemen
        return None

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)

        # 1. Petak Tanah Bajak Cangkul (Tilled Soil Bed - Stardew Hex #8f5832)
        soil_w, soil_h = 36, 26
        soil_rect = pygame.Rect(cx - soil_w // 2, cy - soil_h // 2 + 2, soil_w, soil_h)
        pygame.draw.rect(surface, (143, 88, 50), soil_rect, border_radius=4)
        pygame.draw.rect(surface, (95, 54, 25), soil_rect, width=2, border_radius=4)
        # Garis alur cangkul basah
        pygame.draw.line(surface, (110, 65, 35), (soil_rect.left + 4, soil_rect.centery - 3), (soil_rect.right - 4, soil_rect.centery - 3), 1)
        pygame.draw.line(surface, (110, 65, 35), (soil_rect.left + 4, soil_rect.centery + 4), (soil_rect.right - 4, soil_rect.centery + 4), 1)

        if not self.active:
            # Tunas kecil hijau baru dipanen
            pygame.draw.circle(surface, (80, 150, 65), (cx, cy + 2), 3)
            return

        # 2. Tanaman Matang Siap Panen (Sesuai Foto Stardew Valley)
        bob = int(math.sin(self.pulse) * 1.8)

        if self.elemen == "daun":
            # Tanaman Kale/Cabbage Berdaun Biru-Hijau Lebat (Sesuai Petak Kiri Foto)
            pygame.draw.circle(surface, (35, 110, 65), (cx, cy - 2 + bob), 10)
            pygame.draw.circle(surface, (55, 165, 95), (cx - 4, cy - 5 + bob), 6)
            pygame.draw.circle(surface, (55, 165, 95), (cx + 4, cy - 5 + bob), 6)
            pygame.draw.circle(surface, (85, 215, 125), (cx, cy - 4 + bob), 5)
            pygame.draw.circle(surface, (160, 245, 185), (cx, cy - 4 + bob), 2)

        elif self.elemen == "api":
            # Tanaman Strawberry / Cabai Merah Rimbun (Sesuai Petak Tengah Foto)
            # Ranting daun hijau
            pygame.draw.circle(surface, (40, 130, 50), (cx, cy - 4 + bob), 9)
            pygame.draw.circle(surface, (65, 185, 75), (cx, cy - 6 + bob), 6)
            # Buah cabai/strawberry merah matang dengan biji kuning
            berries = [(cx - 4, cy - 3 + bob), (cx + 4, cy - 3 + bob), (cx, cy + 2 + bob)]
            for bx, by in berries:
                pygame.draw.circle(surface, (225, 40, 30), (bx, by), 4)
                pygame.draw.circle(surface, (255, 110, 95), (bx - 1, by - 1), 2)
                pygame.draw.circle(surface, (255, 230, 80), (bx, by), 1)

        elif self.elemen == "air":
            # Mata Air Embun / Gentong Air Keramik
            pygame.draw.circle(surface, (45, 125, 185), (cx, cy - 2 + bob), 9)
            pygame.draw.circle(surface, (70, 185, 245), (cx, cy - 3 + bob), 7)
            pygame.draw.circle(surface, (220, 245, 255), (cx - 2, cy - 5 + bob), 3)

        elif self.elemen == "batu":
            # Batu Mineral Geode Ungu/Amethyst (Sesuai Petak Tambang)
            pts = [
                (cx, cy - 9 + bob),
                (cx + 8, cy - 2 + bob),
                (cx + 6, cy + 6 + bob),
                (cx - 6, cy + 6 + bob),
                (cx - 8, cy - 2 + bob)
            ]
            pygame.draw.polygon(surface, (135, 95, 185), pts)
            pygame.draw.polygon(surface, (185, 145, 240), pts, width=2)
            pygame.draw.circle(surface, (255, 255, 255), (cx - 2, cy - 3 + bob), 2)
