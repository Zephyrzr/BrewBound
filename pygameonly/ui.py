"""
Komponen Antarmuka Pengguna (UI) Khas Gaya Sandbox
"""

import pygame
from constants import (
    GT_DIALOG_BG, GT_DIALOG_BG_DARK, GT_BORDER_OUTER, GT_BORDER_CYAN,
    GT_BORDER_HIGHLIGHT, GT_BORDER_SHADOW, GT_BTN_BLUE, GT_BTN_BLUE_LIGHT,
    GT_BTN_BLUE_DARK, GT_BTN_GREEN, GT_BTN_GREEN_LIGHT, GT_BTN_GREEN_DARK,
    GT_BTN_RED, GT_BTN_RED_LIGHT, GT_BTN_RED_DARK, GT_SLOT_BG, GT_SLOT_BORDER,
    GT_SLOT_SELECTED, COLOR_TEXT_WHITE, COLOR_TEXT_YELLOW, COLOR_TEXT_MUTED,
    COLOR_TEXT_GOLD, COLOR_TEXT_RED, COLOR_TEXT_GREEN, COLOR_TEXT_CYAN,
    COLOR_HP_GREEN, COLOR_HP_RED, COLOR_HP_BG
)
from audio import audio

def draw_gt_dialog(surface, rect, title=""):
    """
    Menggambar kotak dialog khas Growtopia:
    - Latar biru laut bergradasi gelap
    - Border ganda cyan terang dengan efek 3D bevel
    - Header judul dengan aksen garis emas/kuning
    """
    r = pygame.Rect(rect)

    # 1. Bayangan luar hitam
    shadow_rect = r.inflate(4, 4)
    pygame.draw.rect(surface, GT_BORDER_OUTER, shadow_rect, border_radius=10)

    # 2. Latar Belakang Dialog Khas GT
    pygame.draw.rect(surface, GT_DIALOG_BG, r, border_radius=8)

    # Latar dalam bergradasi gelap (inset panel)
    inner_rect = r.inflate(-10, -10)
    pygame.draw.rect(surface, GT_DIALOG_BG_DARK, inner_rect, border_radius=6)

    # 3. Border Cyan Ganda dengan Efek Bevel 3D
    pygame.draw.rect(surface, GT_BORDER_CYAN, r, width=3, border_radius=8)
    
    # Highlight sudut atas & kiri (Cyan Terang)
    pygame.draw.line(surface, GT_BORDER_HIGHLIGHT, (r.left + 6, r.top + 2), (r.right - 6, r.top + 2), 2)
    pygame.draw.line(surface, GT_BORDER_HIGHLIGHT, (r.left + 2, r.top + 6), (r.left + 2, r.bottom - 6), 2)

    # Shadow sudut bawah & kanan (Biru Tua)
    pygame.draw.line(surface, GT_BORDER_SHADOW, (r.left + 6, r.bottom - 3), (r.right - 6, r.bottom - 3), 2)
    pygame.draw.line(surface, GT_BORDER_SHADOW, (r.right - 3, r.top + 6), (r.right - 3, r.bottom - 6), 2)

    # 4. Rivet / Sekrup Sudut Khas Game Sandbox
    corners = [
        (r.left + 8, r.top + 8),
        (r.right - 9, r.top + 8),
        (r.left + 8, r.bottom - 9),
        (r.right - 9, r.bottom - 9)
    ]
    for cx, cy in corners:
        pygame.draw.circle(surface, (20, 60, 110), (cx, cy), 3)
        pygame.draw.circle(surface, (140, 220, 255), (cx - 1, cy - 1), 1)

    # 5. Header Judul
    if title:
        pygame.draw.line(surface, GT_BORDER_CYAN, (r.left + 15, r.top + 38), (r.right - 15, r.top + 38), 2)

def draw_shadowed_text(surface, font, text, pos, color, shadow_offset=1):
    """Render teks dengan bayangan hitam pixel — menggantikan pola render ganda yang berulang."""
    shadow = font.render(text, True, (0, 0, 0))
    surf = font.render(text, True, color)
    surface.blit(shadow, (pos[0] + shadow_offset, pos[1] + shadow_offset))
    surface.blit(surf, pos)

class Button:
    """Tombol bergaya 3D Bevel Growtopia dengan feedback tactile (atas terang, bawah gelap)"""
    def __init__(self, rect, text, callback=None, color_theme="blue", text_color=COLOR_TEXT_WHITE, shortcut=""):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.color_theme = color_theme  # "blue", "green", "red", "wood"
        self.text_color = text_color
        self.shortcut = shortcut
        self.is_hovered = False
        self.is_pressed = False
        self.is_disabled = False

    def handle_event(self, event):
        if self.is_disabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                audio.play("click")
                if self.callback:
                    self.callback()
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False
        return False

    def draw(self, surface, font, small_font=None):
        r = self.rect.copy()
        if self.is_pressed:
            r.y += 2  # Efek tombol tertekan ke bawah

        # Tentukan palet warna bevel 3D
        if self.is_disabled:
            base_col = (45, 55, 70)
            light_col = (70, 80, 95)
            dark_col = (25, 30, 40)
            txt_col = (110, 125, 140)
        elif self.color_theme == "green":
            base_col = GT_BTN_GREEN if not self.is_hovered else (60, 180, 75)
            light_col = GT_BTN_GREEN_LIGHT
            dark_col = GT_BTN_GREEN_DARK
            txt_col = COLOR_TEXT_WHITE
        elif self.color_theme == "red":
            base_col = GT_BTN_RED if not self.is_hovered else (215, 60, 60)
            light_col = GT_BTN_RED_LIGHT
            dark_col = GT_BTN_RED_DARK
            txt_col = COLOR_TEXT_WHITE
        else:
            base_col = GT_BTN_BLUE if not self.is_hovered else (40, 120, 215)
            light_col = GT_BTN_BLUE_LIGHT
            dark_col = GT_BTN_BLUE_DARK
            txt_col = COLOR_TEXT_YELLOW if self.is_hovered else COLOR_TEXT_WHITE

        # Latar tombol
        pygame.draw.rect(surface, base_col, r, border_radius=6)

        # Border Bevel 3D Khas Growtopia (Highlight atas-kiri, Shadow bawah-kanan)
        pygame.draw.line(surface, light_col, (r.left + 2, r.top + 2), (r.right - 2, r.top + 2), 2)
        pygame.draw.line(surface, light_col, (r.left + 2, r.top + 2), (r.left + 2, r.bottom - 2), 2)

        pygame.draw.line(surface, dark_col, (r.left + 2, r.bottom - 2), (r.right - 2, r.bottom - 2), 3)
        pygame.draw.line(surface, dark_col, (r.right - 2, r.top + 2), (r.right - 2, r.bottom - 2), 3)

        # Garis tepi luar hitam
        pygame.draw.rect(surface, GT_BORDER_OUTER, r, width=1, border_radius=6)

        # Teks tombol dengan bayangan hitam pixel
        shadow_surf = font.render(self.text, True, (0, 0, 0))
        txt_surf = font.render(self.text, True, txt_col)
        t_rect = txt_surf.get_rect(center=r.center)
        surface.blit(shadow_surf, (t_rect.x + 1, t_rect.y + 1))
        surface.blit(txt_surf, t_rect)

        # Shortcut key badge
        if self.shortcut and small_font:
            sc_surf = small_font.render(self.shortcut, True, COLOR_TEXT_YELLOW if self.is_hovered else COLOR_TEXT_MUTED)
            surface.blit(sc_surf, (r.right - sc_surf.get_width() - 6, r.y + 3))


class HealthBar:
    """Bar HP bergaya arcade Growtopia dengan segmen dan persentase"""
    def __init__(self, rect, max_hp, current_hp=None, is_boss=False):
        self.rect = pygame.Rect(rect)
        self.max_hp = max_hp
        self.current_hp = current_hp if current_hp is not None else max_hp
        self.display_hp = float(self.current_hp)
        self.is_boss = is_boss

    def set_hp(self, hp):
        self.current_hp = max(0, min(self.max_hp, hp))

    def update(self):
        diff = self.current_hp - self.display_hp
        if abs(diff) < 0.2:
            self.display_hp = float(self.current_hp)
        else:
            self.display_hp += diff * 0.18

    def draw(self, surface, font, label=""):
        r = self.rect

        # Bayangan luar
        pygame.draw.rect(surface, GT_BORDER_OUTER, r.inflate(4, 4), border_radius=6)
        pygame.draw.rect(surface, COLOR_HP_BG, r, border_radius=5)

        # Isi bar
        ratio = max(0.0, min(1.0, self.display_hp / self.max_hp if self.max_hp > 0 else 0))
        fill_width = int((r.width - 4) * ratio)
        if fill_width > 0:
            fill_rect = pygame.Rect(r.x + 2, r.y + 2, fill_width, r.height - 4)
            # Warna HP: Hijau jika sehat, Merah/Oranye jika sekarat. Boss berwarna Ungu/Merah Darah
            if self.is_boss:
                col = (190, 40, 220) if ratio > 0.5 else (230, 45, 45)
            else:
                col = COLOR_HP_GREEN if ratio > 0.4 else ((240, 160, 40) if ratio > 0.2 else COLOR_HP_RED)
            pygame.draw.rect(surface, col, fill_rect, border_radius=4)

            # Highlight glossy atas bar
            pygame.draw.line(surface, (255, 255, 255, 120), (fill_rect.left, fill_rect.top + 1), (fill_rect.right, fill_rect.top + 1), 1)

        # Border luar Cyan / Emas
        border_col = GT_SLOT_SELECTED if self.is_boss else GT_BORDER_CYAN
        pygame.draw.rect(surface, border_col, r, width=2, border_radius=5)

        # Teks HP
        text = f"{label} {int(self.current_hp)}/{self.max_hp}".strip()
        t_shadow = font.render(text, True, (0, 0, 0))
        t_surf = font.render(text, True, COLOR_TEXT_WHITE)
        t_rect = t_surf.get_rect(center=r.center)
        surface.blit(t_shadow, (t_rect.x + 1, t_rect.y + 1))
        surface.blit(t_surf, t_rect)

class FloatingText:
    """Teks melayang bergaya pop-up kartun Growtopia"""
    def __init__(self, text, pos, color=COLOR_TEXT_YELLOW, size=24, duration=48):
        self.text = text
        self.x, self.y = pos
        self.color = color
        self.size = size
        self.duration = duration
        self.age = 0
        self.is_dead = False

    def update(self):
        self.age += 1
        self.y -= 1.3
        if self.age >= self.duration:
            self.is_dead = True

    def draw(self, surface, font):
        t_shadow = font.render(self.text, True, (0, 0, 0))
        t_surf = font.render(self.text, True, self.color)
        surface.blit(t_shadow, (int(self.x) + 2, int(self.y) + 2))
        surface.blit(t_surf, (int(self.x), int(self.y)))

class ToastNotification:
    """Pemberitahuan bar gaya Growtopia Chat Banner"""
    def __init__(self):
        self.message = ""
        self.timer = 0
        self.color = COLOR_TEXT_GREEN

    def show(self, msg, color=COLOR_TEXT_GREEN, duration=160):
        self.message = msg
        self.timer = duration
        self.color = color

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def draw(self, surface, font):
        if self.timer <= 0 or not self.message:
            return
        surf = font.render(self.message, True, self.color)
        shadow = font.render(self.message, True, (0, 0, 0))

        box_w = surf.get_width() + 32
        box_h = surf.get_height() + 16
        box_x = (surface.get_width() - box_w) // 2
        box_y = 18

        r = pygame.Rect(box_x, box_y, box_w, box_h)
        draw_gt_dialog(surface, r)
        surface.blit(shadow, (box_x + 17, box_y + 9))
        surface.blit(surf, (box_x + 16, box_y + 8))
