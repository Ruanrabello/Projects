"""
Áudio procedural — gera SFX e música sem arquivos externos.
"""
import array
import math
import pygame

from settings import MASTER_VOLUME, MUSIC_VOLUME, SFX_VOLUME


def _make_tone(freq: float, duration: float, volume: float = 0.3,
               sample_rate: int = 22050, wave: str = "sine") -> pygame.mixer.Sound:
    n_samples = int(sample_rate * duration)
    buf = array.array("h")
    amp = int(32767 * volume)
    for i in range(n_samples):
        t = i / sample_rate
        if wave == "sine":
            v = math.sin(2 * math.pi * freq * t)
        elif wave == "square":
            v = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        elif wave == "saw":
            v = 2 * (t * freq % 1) - 1
        else:
            v = math.sin(2 * math.pi * freq * t * 2)
        env = min(1.0, (n_samples - i) / (n_samples * 0.3))
        buf.append(int(v * amp * env))
    return pygame.mixer.Sound(buffer=buf)


class AudioManager:
    def __init__(self):
        self.master = MASTER_VOLUME
        self.music_vol = MUSIC_VOLUME
        self.sfx_vol = SFX_VOLUME
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._music_playing = False

    def init(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        self._build_sfx()

    def _build_sfx(self):
        self._sounds = {
            "shoot": _make_tone(880, 0.06, 0.2, wave="square"),
            "hit": _make_tone(200, 0.1, 0.35, wave="saw"),
            "enemy_hit": _make_tone(150, 0.08, 0.25),
            "kill": _make_tone(440, 0.15, 0.3),
            "pickup": _make_tone(660, 0.12, 0.25),
            "dash": _make_tone(300, 0.1, 0.2, wave="square"),
            "hurt": _make_tone(100, 0.2, 0.4),
            "level_up": _make_tone(523, 0.25, 0.35),
            "boss": _make_tone(80, 0.4, 0.45),
            "ui": _make_tone(520, 0.05, 0.15),
            "game_over": _make_tone(110, 0.5, 0.4),
        }

    def play(self, name: str):
        snd = self._sounds.get(name)
        if snd:
            snd.set_volume(self.sfx_vol * self.master)
            snd.play()

    def play_music(self):
        if self._music_playing:
            return
        # Loop de tons baixos simulando ambiente
        self._music_playing = True
        pygame.mixer.music.set_volume(self.music_vol * self.master)
        # Usa tom longo como drone de fundo
        drone = _make_tone(55, 3.0, 0.08)
        # pygame.mixer.music precisa de arquivo; usamos canal dedicado
        ch = pygame.mixer.find_channel(True)
        if ch:
            drone.set_volume(self.music_vol * self.master * 0.5)
            ch.play(drone, loops=-1)

    def stop_music(self):
        pygame.mixer.stop()
        self._music_playing = False

    def set_volumes(self, master=None, music=None, sfx=None):
        if master is not None:
            self.master = master
        if music is not None:
            self.music_vol = music
        if sfx is not None:
            self.sfx_vol = sfx
