"""
Sistem Audio & Musik (Audio & BGM Manager)
"""

import io
import math
import struct
import wave
import os
import pygame

class SoundManager:
    def __init__(self):
        self.enabled = False
        self.music_enabled = True
        self.sounds = {}
        self.bgm_path = os.path.join(os.path.dirname(__file__), "assets", "bgm.mp3")

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            self.enabled = True
            self._generate_all_sfx()
            self.start_bgm()
        except Exception as e:
            print(f"[SoundManager] Inisialisasi audio/mixer: {e}")
            self.enabled = False

    def start_bgm(self):
        """Memutar musik latar belakang MP3 yang disediakan user secara looping"""
        if not self.enabled or not self.music_enabled:
            return
        try:
            if os.path.exists(self.bgm_path):
                pygame.mixer.music.load(self.bgm_path)
                pygame.mixer.music.set_volume(0.55)
                pygame.mixer.music.play(-1)  # Looping tanpa henti
                print(f"[SoundManager] Memutar BGM: {self.bgm_path}")
            else:
                print(f"[SoundManager] File BGM tidak ditemukan di {self.bgm_path}")
        except Exception as e:
            print(f"[SoundManager] Gagal memutar BGM: {e}")

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        if not self.enabled:
            return self.music_enabled
        try:
            if self.music_enabled:
                pygame.mixer.music.unpause()
                if not pygame.mixer.music.get_busy():
                    self.start_bgm()
            else:
                pygame.mixer.music.pause()
        except Exception as e:
            print(f"[SoundManager] Toggle musik error: {e}")
        return self.music_enabled

    def _generate_wav(self, duration_s: float, sample_func) -> pygame.mixer.Sound:
        sample_rate = 22050
        num_samples = int(sample_rate * duration_s)
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sample_rate)
            samples = []
            for i in range(num_samples):
                t = i / sample_rate
                val = sample_func(t, i, num_samples)
                val = max(-1.0, min(1.0, val))
                samples.append(int(val * 32767 * 0.45))
            w.writeframes(struct.pack(f'<{len(samples)}h', *samples))
        buf.seek(0)
        return pygame.mixer.Sound(buf)

    def _generate_all_sfx(self):
        # 1. Click blip (Growtopia UI button pop)
        def click_wave(t, i, n):
            env = 1.0 - (i / n)
            return math.sin(2 * math.pi * 750 * t) * env
        self.sounds["click"] = self._generate_wav(0.05, click_wave)

        # 2. Select slot
        def select_wave(t, i, n):
            freq = 520 + 350 * (i / n)
            env = 1.0 - (i / n) ** 0.5
            return math.sin(2 * math.pi * freq * t) * env
        self.sounds["select"] = self._generate_wav(0.07, select_wave)

        # 3. Brew cauldron bubble
        def brew_wave(t, i, n):
            freq = 320 + 600 * math.sin(2 * math.pi * 14 * t) + 180 * (i / n)
            env = math.sin(math.pi * (i / n))
            return (0.7 * math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)) * env
        self.sounds["brew"] = self._generate_wav(0.32, brew_wave)

        # 4. Hit / Damage Attack (punch / block break)
        def hit_wave(t, i, n):
            env = (1.0 - (i / n)) ** 2
            freq = max(60, 240 - 500 * t)
            sub = math.sin(2 * math.pi * freq * t)
            noise = (math.sin(i * 12.9898) % 1.0) * 0.35
            return (sub * 0.65 + noise) * env
        self.sounds["hit"] = self._generate_wav(0.18, hit_wave)

        # 5. Super Effective Crit
        def crit_wave(t, i, n):
            env = (1.0 - (i / n)) ** 1.3
            freq = 950 if t < 0.08 else (1350 if t < 0.16 else 1900)
            return (0.7 * math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(2 * math.pi * (freq * 1.5) * t)) * env
        self.sounds["crit"] = self._generate_wav(0.3, crit_wave)

        # 6. Heal (Growtopia/Stardew sparkling chime)
        def heal_wave(t, i, n):
            env = math.sin(math.pi * (i / n))
            notes = [523.25, 659.25, 783.99, 1046.50]
            step = min(3, int(t * 11))
            return math.sin(2 * math.pi * notes[step] * t) * env
        self.sounds["heal"] = self._generate_wav(0.36, heal_wave)

        # 7. Harvest item (Stardew crop pluck pop)
        def harvest_wave(t, i, n):
            env = 1.0 - (i / n)
            freq = 700 + (400 if i > n // 2 else 0)
            return math.sin(2 * math.pi * freq * t) * env
        self.sounds["harvest"] = self._generate_wav(0.12, harvest_wave)

        # 8. Victory Fanfare
        def victory_wave(t, i, n):
            env = min(1.0, 1.2 - (i / n))
            notes = [440, 554, 659, 880]
            step = min(3, int(t / 0.14))
            return math.sin(2 * math.pi * notes[step] * t) * env
        self.sounds["victory"] = self._generate_wav(0.6, victory_wave)

        # 9. Defeat / Faint
        def defeat_wave(t, i, n):
            env = 1.0 - (i / n)
            freq = max(100, 440 - 320 * t)
            return math.sin(2 * math.pi * freq * t) * env
        self.sounds["defeat"] = self._generate_wav(0.48, defeat_wave)

        # 10. Flee Success
        def flee_success_wave(t, i, n):
            env = math.sin(math.pi * (i / n))
            freq = 300 + 700 * (i / n)
            return math.sin(2 * math.pi * freq * t) * env
        self.sounds["flee_success"] = self._generate_wav(0.25, flee_success_wave)

        # 11. Flee Fail
        def flee_fail_wave(t, i, n):
            env = 1.0 - (i / n)
            freq = 150 if (int(t * 30) % 2 == 0) else 110
            return (0.7 * math.sin(2 * math.pi * freq * t) + 0.3 * ((math.sin(i * 7.7) % 1.0))) * env
        self.sounds["flee_fail"] = self._generate_wav(0.35, flee_fail_wave)

        # 12. Lord Boss Roar
        def boss_roar_wave(t, i, n):
            env = min(1.0, math.sin(math.pi * (i / n) ** 0.6))
            freq = 80 + 40 * math.sin(2 * math.pi * 8 * t)
            noise = (math.sin(i * 15.345) % 1.0) * 0.4
            return (math.sin(2 * math.pi * freq * t) * 0.6 + noise) * env
        self.sounds["boss_roar"] = self._generate_wav(0.65, boss_roar_wave)

    def play(self, name: str):
        if not self.enabled:
            return
        snd = self.sounds.get(name)
        if snd:
            snd.play()

audio = SoundManager()
