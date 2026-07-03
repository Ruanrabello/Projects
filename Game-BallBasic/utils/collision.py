"""
Resolução de colisão eixo a eixo — evita atravessar paredes e cantos.
"""
import pygame

from settings import TILE_SIZE


def make_hitbox(pos: pygame.Vector2, size: tuple[int, int]) -> pygame.Rect:
    w, h = size
    rect = pygame.Rect(0, 0, w, h)
    rect.center = (int(pos.x), int(pos.y))
    return rect


def _resolve_wall_overlap(pos: pygame.Vector2, hitbox_size: tuple[int, int],
                          walls: list[pygame.Rect], max_passes: int = 8) -> pygame.Vector2:
    """Empurra entidade para fora de paredes (múltiplas passadas para cantos)."""
    w, h = hitbox_size
    half_w, half_h = w // 2, h // 2
    pos = pygame.Vector2(pos)

    for _ in range(max_passes):
        box = make_hitbox(pos, hitbox_size)
        hit_any = False
        for wall in walls:
            if not box.colliderect(wall):
                continue
            hit_any = True
            overlap_left = box.right - wall.left
            overlap_right = wall.right - box.left
            overlap_top = box.bottom - wall.top
            overlap_bottom = wall.bottom - box.top
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
            if min_overlap == overlap_left:
                pos.x = wall.left - half_w - 1
            elif min_overlap == overlap_right:
                pos.x = wall.right + half_w + 1
            elif min_overlap == overlap_top:
                pos.y = wall.top - half_h - 1
            else:
                pos.y = wall.bottom + half_h + 1
            box = make_hitbox(pos, hitbox_size)
        if not hit_any:
            break
    return pos


def move_with_wall_collision(
    pos: pygame.Vector2,
    hitbox_size: tuple[int, int],
    delta: pygame.Vector2,
    walls: list[pygame.Rect],
    map_bounds: pygame.Rect | None = None,
) -> pygame.Vector2:
    """Move posição com slide nas paredes (não usa o rect do sprite rotacionado)."""
    pos = pygame.Vector2(pos)
    w, h = hitbox_size
    half_w, half_h = w // 2, h // 2

    if delta.x != 0:
        pos.x += delta.x
        pos = _resolve_wall_overlap(pos, hitbox_size, walls)

    if delta.y != 0:
        pos.y += delta.y
        pos = _resolve_wall_overlap(pos, hitbox_size, walls)

    if map_bounds is not None:
        pos.x = max(map_bounds.left + half_w + 1,
                    min(pos.x, map_bounds.right - half_w - 1))
        pos.y = max(map_bounds.top + half_h + 1,
                    min(pos.y, map_bounds.bottom - half_h - 1))

    return pos


def clamp_to_walkable(pos: pygame.Vector2, hitbox_size: tuple[int, int],
                      walls: list[pygame.Rect],
                      map_bounds: pygame.Rect | None = None) -> pygame.Vector2:
    """Garante que spawn não nasça dentro de parede."""
    pos = _resolve_wall_overlap(pos, hitbox_size, walls)
    if map_bounds is not None:
        w, h = hitbox_size
        half_w, half_h = w // 2, h // 2
        pos.x = max(map_bounds.left + half_w + 1,
                    min(pos.x, map_bounds.right - half_w - 1))
        pos.y = max(map_bounds.top + half_h + 1,
                    min(pos.y, map_bounds.bottom - half_h - 1))
    return pos
