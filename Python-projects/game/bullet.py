"""
Projéteis do jogador e inimigos.
"""
import pygame

from settings import BULLET_SPEED, TILE_SIZE
from utils.sprites import create_bullet_sprite


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2,
                 damage: float, owner: str = "player", speed: float = BULLET_SPEED):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.direction = direction.normalize() if direction.length_squared() > 0 else pygame.Vector2(1, 0)
        self.damage = damage
        self.owner = owner
        self.speed = speed
        self.lifetime = 2.0
        self.image = create_bullet_sprite()
        if owner == "enemy":
            self.image = pygame.transform.scale(self.image, (14, 14))
            self.image.fill((255, 80, 80), special_flags=pygame.BLEND_RGB_MULT)
        self.rect = self.image.get_rect(center=(int(pos.x), int(pos.y)))

    def update(self, dt: float, walls: list[pygame.Rect]):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
        self.pos += self.direction * self.speed * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        for wall in walls:
            if self.rect.colliderect(wall):
                self.kill()
                return

    @property
    def world_pos(self) -> pygame.Vector2:
        return self.pos


class BulletGroup(pygame.sprite.Group):
    def update_all(self, dt: float, walls: list[pygame.Rect]):
        for bullet in self.sprites():
            bullet.update(dt, walls)
