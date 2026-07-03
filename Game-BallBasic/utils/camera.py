"""
Câmera suave com shake e limites do mapa.
"""
import random
import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAMERA_LERP, SHAKE_DECAY, SHAKE_MAX


class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.shake_amount = 0.0
        self.shake_offset = pygame.Vector2(0, 0)
        self.map_pixel_w = 0
        self.map_pixel_h = 0

    def set_map_size(self, width: int, height: int):
        self.map_pixel_w = width
        self.map_pixel_h = height

    def shake(self, intensity: float = 6.0):
        self.shake_amount = min(SHAKE_MAX, self.shake_amount + intensity)

    def update(self, target_pos: pygame.Vector2, dt: float):
        # Segue o alvo com interpolação exponencial (frame-independent)
        t = 1 - pow(0.001, dt * CAMERA_LERP)
        self.x += (target_pos.x - SCREEN_WIDTH / 2 - self.x) * t
        self.y += (target_pos.y - SCREEN_HEIGHT / 2 - self.y) * t

        max_x = max(0, self.map_pixel_w - SCREEN_WIDTH)
        max_y = max(0, self.map_pixel_h - SCREEN_HEIGHT)
        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))

        if self.shake_amount > 0.1:
            self.shake_amount = max(0, self.shake_amount - SHAKE_DECAY * dt * 60)
            self.shake_offset = pygame.Vector2(
                random.uniform(-1, 1) * self.shake_amount,
                random.uniform(-1, 1) * self.shake_amount,
            )
        else:
            self.shake_amount = 0
            self.shake_offset.update(0, 0)

    @property
    def offset(self) -> pygame.Vector2:
        return pygame.Vector2(self.x, self.y) + self.shake_offset

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        off = self.offset
        return rect.move(-int(off.x), -int(off.y))

    def apply_pos(self, pos: pygame.Vector2) -> tuple[int, int]:
        off = self.offset
        return int(pos.x - off.x), int(pos.y - off.y)
