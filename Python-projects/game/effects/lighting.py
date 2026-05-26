"""
Overlay de iluminação simples — escuridão com clarão no jogador.
"""
import pygame


class LightingSystem:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.darkness = pygame.Surface((width, height), pygame.SRCALPHA)
        self._build_darkness()

    def _build_darkness(self):
        self.darkness.fill((0, 0, 0, 200))

    def render(self, surface: pygame.Surface, light_positions: list[tuple],
               camera_offset: pygame.Vector2, ambient: int = 200):
        overlay = self.darkness.copy()
        overlay.fill((0, 0, 0, ambient))
        for wx, wy, radius in light_positions:
            sx = int(wx - camera_offset.x)
            sy = int(wy - camera_offset.y)
            for r in range(radius, 0, -8):
                alpha = int(180 * (1 - r / radius))
                pygame.draw.circle(overlay, (0, 0, 0, max(0, ambient - alpha)),
                                   (sx, sy), r)
        surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
