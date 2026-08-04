"""Áudio procedural para efeitos e trilha ambiente."""

import array
import logging
import math

import pygame

from settings import MASTER_VOLUME, MUSIC_VOLUME, SFX_VOLUME


logger = logging.getLogger(__name__)
SAMPLE_RATE = 22050


def _clamp_volume(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _make_tone(
    frequency: float,
    duration: float,
    volume: float = 0.3,
    sample_rate: int = SAMPLE_RATE,
    wave: str = "sine",
) -> pygame.mixer.Sound:
    sample_count = max(1, int(sample_rate * duration))
    buffer = array.array("h")
    amplitude = int(32767 * _clamp_volume(volume))

    for index in range(sample_count):
        time = index / sample_rate

        if wave == "square":
            value = 1.0 if math.sin(2 * math.pi * frequency * time) >= 0 else -1.0
        elif wave == "saw":
            value = 2 * (time * frequency % 1) - 1
        else:
            value = math.sin(2 * math.pi * frequency * time)

        remaining_ratio = (sample_count - index) / sample_count
        envelope = min(1.0, remaining_ratio / 0.3)
        buffer.append(int(value * amplitude * envelope))

    return pygame.mixer.Sound(buffer=buffer)


class AudioManager:
    def __init__(self):
        self.master = _clamp_volume(MASTER_VOLUME)
        self.music_vol = _clamp_volume(MUSIC_VOLUME)
        self.sfx_vol = _clamp_volume(SFX_VOLUME)
        self.enabled = False
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._music_channel: pygame.mixer.Channel | None = None
        self._music_sound: pygame.mixer.Sound | None = None

    def init(self) -> bool:
        """Inicializa o áudio sem impedir o jogo de abrir quando não há dispositivo."""
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(
                    frequency=SAMPLE_RATE,
                    size=-16,
                    channels=1,
                    buffer=512,
                )
            self._build_sfx()
            self.enabled = True
        except pygame.error:
            logger.warning("Áudio indisponível. O jogo continuará sem som.", exc_info=True)
            self.enabled = False

        return self.enabled

    def _build_sfx(self) -> None:
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

    def play(self, name: str) -> None:
        if not self.enabled:
            return

        sound = self._sounds.get(name)
        if sound is None:
            return

        sound.set_volume(_clamp_volume(self.sfx_vol * self.master))
        sound.play()

    def play_music(self) -> None:
        if not self.enabled or self._music_channel?.get_busy():
            return

        self._music_sound = _make_tone(55, 3.0, 0.08)
        self._music_sound.set_volume(_clamp_volume(self.music_vol * self.master * 0.5))
        self._music_channel = pygame.mixer.find_channel(True)

        if self._music_channel is not None:
            self._music_channel.play(self._music_sound, loops=-1)

    def stop_music(self) -> None:
        if self._music_channel is not None:
            self._music_channel.stop()
        self._music_channel = None
        self._music_sound = None

    def set_volumes(self, master=None, music=None, sfx=None) -> None:
        if master is not None:
            self.master = _clamp_volume(master)
        if music is not None:
            self.music_vol = _clamp_volume(music)
        if sfx is not None:
            self.sfx_vol = _clamp_volume(sfx)

        if self._music_sound is not None:
            self._music_sound.set_volume(_clamp_volume(self.music_vol * self.master * 0.5))
