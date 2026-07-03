"""
Geração procedural de sprites — não depende de arquivos externos.
"""
import math
import pygame

from settings import TILE_SIZE, COLOR_NEON_CYAN, COLOR_NEON_PINK, COLOR_NEON_PURPLE
from settings import COLOR_NEON_YELLOW, COLOR_NEON_GREEN, COLOR_WALL, COLOR_FLOOR


def _glow_circle(size: int, color: tuple, glow: int = 4) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    for r in range(size // 2, 0, -1):
        alpha = int(255 * (r / (size // 2)) ** 0.5)
        c = (*color[:3], min(255, alpha + glow * 10))
        pygame.draw.circle(surf, c, (cx, cy), r)
    return surf


def create_player_frames() -> list[pygame.Surface]:
    frames = []
    for i in range(4):
        s = pygame.Surface((40, 40), pygame.SRCALPHA)
        pulse = 1 + 0.08 * math.sin(i * math.pi / 2)
        body = (int(20 * pulse), int(28 * pulse))
        pygame.draw.polygon(s, COLOR_NEON_CYAN, [(20, 4), (36, 32), (20, 26), (4, 32)])
        pygame.draw.circle(s, (255, 255, 255), (20, 14), 4)
        pygame.draw.rect(s, COLOR_NEON_PURPLE, (14, 22, 12, 8), border_radius=3)
        frames.append(s)
    return frames


def create_enemy_sprite(enemy_type: str, frame: int = 0) -> pygame.Surface:
    palettes = {
        "grunt": COLOR_NEON_PINK,
        "runner": COLOR_NEON_YELLOW,
        "tank": COLOR_NEON_PURPLE,
        "boss": (255, 100, 50),
    }
    color = palettes.get(enemy_type, COLOR_NEON_PINK)
    size = 44 if enemy_type != "boss" else 72
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    wobble = int(3 * math.sin(frame * 1.5))
    pygame.draw.ellipse(s, color, (4, 8 + wobble, size - 8, size - 14))
    pygame.draw.circle(s, (255, 60, 80), (size // 3, size // 3), 5)
    pygame.draw.circle(s, (255, 60, 80), (2 * size // 3, size // 3), 5)
    if enemy_type == "tank":
        pygame.draw.rect(s, (*color[:2], min(255, color[2] + 40)), (2, size - 12, size - 4, 8), border_radius=2)
    if enemy_type == "boss":
        pygame.draw.polygon(s, COLOR_NEON_YELLOW, [(size // 2, 0), (size, 20), (size - 8, size // 2)])
        pygame.draw.polygon(s, COLOR_NEON_YELLOW, [(0, 20), (8, size // 2), (size // 2, 0)])
    return s


def create_bullet_sprite() -> pygame.Surface:
    return _glow_circle(12, COLOR_NEON_CYAN, glow=6)


def create_powerup_sprite(power_type: str) -> pygame.Surface:
    colors = {
        "health": (255, 80, 100),
        "energy": COLOR_NEON_CYAN,
        "damage": COLOR_NEON_PINK,
        "speed": COLOR_NEON_YELLOW,
        "shield": COLOR_NEON_GREEN,
    }
    return _glow_circle(28, colors.get(power_type, COLOR_NEON_CYAN))


def create_tile_surfaces() -> dict:
    floor = pygame.Surface((TILE_SIZE, TILE_SIZE))
    floor.fill(COLOR_FLOOR)
    for i in range(0, TILE_SIZE, 8):
        pygame.draw.line(floor, (30, 24, 55), (i, 0), (i, TILE_SIZE), 1)
        pygame.draw.line(floor, (30, 24, 55), (0, i), (TILE_SIZE, i), 1)

    wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
    wall.fill(COLOR_WALL)
    pygame.draw.rect(wall, (65, 50, 100), (2, 2, TILE_SIZE - 4, TILE_SIZE - 4), 2)
    pygame.draw.line(wall, (90, 70, 130), (0, 0), (TILE_SIZE, TILE_SIZE), 2)

    return {"floor": floor, "wall": wall}


def create_particle_surface(size: int, color: tuple) -> pygame.Surface:
    return _glow_circle(size, color)


def create_background_layer(w: int, h: int) -> pygame.Surface:
    """Camada de fundo animável com estrelas neon."""
    bg = pygame.Surface((w, h))
    bg.fill((8, 6, 22))
    import random
    rng = random.Random(42)
    for _ in range(120):
        x, y = rng.randint(0, w), rng.randint(0, h)
        c = rng.choice([(0, 180, 200, 80), (200, 50, 150, 60), (100, 60, 200, 70)])
        pygame.draw.circle(bg, c[:3], (x, y), rng.randint(1, 2))
    return bg
