"""
Geração de masmorra, tiles, power-ups e spawn procedural.
"""
import math
import random
import pygame

from settings import (
    TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, COLOR_NEON_CYAN,
    POWERUP_TYPES, BOSS_FLOOR_INTERVAL,
)
from utils.sprites import create_tile_surfaces, create_powerup_sprite


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, power_type: str):
        super().__init__()
        self.power_type = power_type
        self.pos = pygame.Vector2(x, y)
        self.bob_timer = random.uniform(0, 6.28)
        self.image = create_powerup_sprite(power_type)
        self.base_image = self.image
        self.rect = self.image.get_rect(center=(int(x), int(y)))

    def update(self, dt: float):
        self.bob_timer += dt * 4
        offset = int(math.sin(self.bob_timer) * 4)
        self.image = self.base_image
        self.rect.center = (int(self.pos.x), int(self.pos.y + offset))


class GameMap:
    def __init__(self, floor: int = 1):
        self.floor = floor
        self.tiles: list[list[int]] = []
        self.walls: list[pygame.Rect] = []
        self.floor_rects: list[pygame.Rect] = []
        self.spawn_points: list[pygame.Vector2] = []
        self.powerups = pygame.sprite.Group()
        self.tile_surfaces = create_tile_surfaces()
        self.pixel_w = MAP_WIDTH * TILE_SIZE
        self.pixel_h = MAP_HEIGHT * TILE_SIZE
        self.exit_rect: pygame.Rect | None = None
        self._generate()

    def _generate(self):
        """Gera masmorra com salas conectadas por corredores."""
        self.tiles = [[1 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        rooms = []
        attempts = 0
        while len(rooms) < 6 + self.floor and attempts < 80:
            attempts += 1
            w = random.randint(5, 10)
            h = random.randint(5, 10)
            x = random.randint(1, MAP_WIDTH - w - 2)
            y = random.randint(1, MAP_HEIGHT - h - 2)
            new_room = pygame.Rect(x, y, w, h)
            if not any(new_room.colliderect(r) for r in rooms):
                rooms.append(new_room)
                for ty in range(y, y + h):
                    for tx in range(x, x + w):
                        self.tiles[ty][tx] = 0

        for i in range(1, len(rooms)):
            c1 = rooms[i - 1].center
            c2 = rooms[i].center
            self._carve_h_tunnel(c1[1], c2[1], c1[0], c2[0])
            self._carve_v_tunnel(c1[0], c2[0], c1[1], c2[1])

        self.walls.clear()
        self.floor_rects.clear()
        self.spawn_points.clear()

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.tiles[y][x] == 1:
                    self.walls.append(rect)
                else:
                    self.floor_rects.append(rect)
                    if random.random() < 0.02:
                        self.spawn_points.append(pygame.Vector2(
                            rect.centerx, rect.centery))

        if rooms:
            start = rooms[0].center
            self.player_spawn = pygame.Vector2(
                start[0] * TILE_SIZE + TILE_SIZE // 2,
                start[1] * TILE_SIZE + TILE_SIZE // 2,
            )
            end = rooms[-1].center
            ex, ey = end[0] * TILE_SIZE, end[1] * TILE_SIZE
            self.exit_rect = pygame.Rect(ex, ey, TILE_SIZE * 2, TILE_SIZE * 2)
            self.tiles[end[1]][end[0]] = 0
        else:
            self.player_spawn = pygame.Vector2(
                MAP_WIDTH * TILE_SIZE // 2, MAP_HEIGHT * TILE_SIZE // 2)

        self._spawn_powerups()
        if self.floor % BOSS_FLOOR_INTERVAL == 0:
            self.boss_room = rooms[-1] if rooms else None
        else:
            self.boss_room = None

    def _carve_h_tunnel(self, y1, y2, x1, x2):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= y < MAP_HEIGHT and 0 <= x1 < MAP_WIDTH:
                self.tiles[y][x1] = 0

    def _carve_v_tunnel(self, x1, x2, y1, y2):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= x < MAP_WIDTH and 0 <= y1 < MAP_HEIGHT:
                self.tiles[y1][x] = 0

    def _spawn_powerups(self):
        self.powerups.empty()
        floors = [r for r in self.floor_rects if r.colliderect(
            pygame.Rect(0, 0, self.pixel_w, self.pixel_h))]
        random.shuffle(floors)
        count = min(3 + self.floor // 2, 8)
        for rect in floors[:count * 3]:
            if len(self.powerups) >= count:
                break
            if random.random() < 0.15:
                ptype = random.choice(POWERUP_TYPES)
                pu = PowerUp(rect.centerx, rect.centery, ptype)
                self.powerups.add(pu)

    def get_spawn_position(self) -> pygame.Vector2:
        """Retorna posição em chão livre, longe de paredes."""
        if self.spawn_points:
            return random.choice(self.spawn_points)
        for _ in range(40):
            pos = pygame.Vector2(
                random.randint(TILE_SIZE * 2, self.pixel_w - TILE_SIZE * 3),
                random.randint(TILE_SIZE * 2, self.pixel_h - TILE_SIZE * 3),
            )
            test = pygame.Rect(0, 0, 28, 28)
            test.center = (int(pos.x), int(pos.y))
            if not any(test.colliderect(w) for w in self.walls):
                return pos
        return pygame.Vector2(self.player_spawn)

    def get_walkable_bounds(self) -> pygame.Rect:
        return pygame.Rect(
            TILE_SIZE, TILE_SIZE,
            self.pixel_w - TILE_SIZE * 2,
            self.pixel_h - TILE_SIZE * 2,
        )

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2,
             anim_offset: float = 0):
        """Desenha tiles visíveis com parallax leve no fundo."""
        view = pygame.Rect(
            int(camera_offset.x), int(camera_offset.y),
            surface.get_width(), surface.get_height())
        view.inflate_ip(TILE_SIZE * 2, TILE_SIZE * 2)

        for rect in self.floor_rects:
            if rect.colliderect(view):
                draw_rect = rect.move(-int(camera_offset.x), -int(camera_offset.y))
                surface.blit(self.tile_surfaces["floor"], draw_rect)

        for rect in self.walls:
            if rect.colliderect(view):
                draw_rect = rect.move(-int(camera_offset.x), -int(camera_offset.y))
                surface.blit(self.tile_surfaces["wall"], draw_rect)

        if self.exit_rect and self.exit_rect.colliderect(view):
            er = self.exit_rect.move(-int(camera_offset.x), -int(camera_offset.y))
            pulse = int(40 + 30 * math.sin(anim_offset * 3))
            portal = pygame.Surface((er.width, er.height), pygame.SRCALPHA)
            pygame.draw.rect(portal, (*COLOR_NEON_CYAN[:3], pulse), portal.get_rect(), border_radius=8)
            pygame.draw.rect(portal, COLOR_NEON_CYAN, portal.get_rect(), 2, border_radius=8)
            surface.blit(portal, er.topleft)

    def draw_powerups(self, surface, camera_offset, dt):
        for pu in self.powerups:
            pu.update(dt)
            draw_rect = pu.rect.move(-int(camera_offset.x), -int(camera_offset.y))
            surface.blit(pu.image, draw_rect)
