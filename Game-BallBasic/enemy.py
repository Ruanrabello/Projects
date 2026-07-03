"""
Inimigos com IA: perseguição, ataque, desvio e tipos variados.
"""
import math
import random
import pygame

from settings import (
    ENEMY_ATTACK_RANGE, ENEMY_DETECT_RANGE, ENEMY_DODGE_CHANCE,
    DIFFICULTY_HP_SCALE, DIFFICULTY_DMG_SCALE,
    ENEMY_HITBOX, BOSS_HITBOX,
)
from bullet import Bullet
from utils.sprites import create_enemy_sprite
from utils.collision import (
    move_with_wall_collision, make_hitbox, clamp_to_walkable, _resolve_wall_overlap,
)


ENEMY_TYPES = {
    "grunt": {"hp": 40, "speed": 110, "damage": 12, "score": 100, "attack_cd": 1.2},
    "runner": {"hp": 25, "speed": 200, "damage": 8, "score": 120, "attack_cd": 0.9},
    "tank": {"hp": 90, "speed": 70, "damage": 22, "score": 200, "attack_cd": 1.8},
    "boss": {"hp": 400, "speed": 85, "damage": 30, "score": 1000, "attack_cd": 0.7},
}


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, enemy_type: str = "grunt", floor: int = 1):
        super().__init__()
        self.enemy_type = enemy_type
        stats = ENEMY_TYPES.get(enemy_type, ENEMY_TYPES["grunt"]).copy()
        scale = DIFFICULTY_HP_SCALE ** (floor - 1)
        self.max_hp = stats["hp"] * scale
        self.hp = self.max_hp
        self.speed = stats["speed"]
        self.damage = stats["damage"] * (DIFFICULTY_DMG_SCALE ** (floor - 1))
        self.score_value = int(stats["score"] * (1 + floor * 0.1))
        self.attack_cooldown = stats["attack_cd"]
        self.attack_timer = random.uniform(0, self.attack_cooldown)

        self.pos = pygame.Vector2(x, y)
        self.anim_frame = 0
        self.anim_timer = 0.0
        self.state = "idle"  # idle, chase, attack, dodge
        self.dodge_timer = 0.0
        self.dodge_dir = pygame.Vector2(0, 0)
        self.hit_flash = 0.0
        self.is_boss = enemy_type == "boss"
        self.map_bounds: pygame.Rect | None = None
        self.walls_cache: list[pygame.Rect] = []

        self._refresh_sprite()

    def place_at(self, pos: pygame.Vector2, walls: list[pygame.Rect],
                 map_bounds: pygame.Rect | None):
        """Define posição inicial sem sobrepor paredes."""
        self.walls_cache = walls
        self.map_bounds = map_bounds
        self.pos = clamp_to_walkable(pos, self.hitbox_size, walls, map_bounds)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    @property
    def hitbox_size(self) -> tuple[int, int]:
        return BOSS_HITBOX if self.is_boss else ENEMY_HITBOX

    @property
    def hitbox(self) -> pygame.Rect:
        return make_hitbox(self.pos, self.hitbox_size)

    def _refresh_sprite(self):
        self.image = create_enemy_sprite(self.enemy_type, self.anim_frame)
        if self.hit_flash > 0:
            flash = self.image.copy()
            flash.fill((255, 200, 200), special_flags=pygame.BLEND_RGB_ADD)
            self.image = flash
        size = 72 if self.is_boss else 44
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def update(self, dt: float, player_pos: pygame.Vector2, walls: list[pygame.Rect],
               bullets_group, audio, floor: int = 1):
        self.walls_cache = walls
        if self.hit_flash > 0:
            self.hit_flash -= dt

        to_player = player_pos - self.pos
        dist = to_player.length()

        if self.dodge_timer > 0:
            self.dodge_timer -= dt
            self._move(self.dodge_dir * 280 * dt, walls)
            self.state = "dodge"
        elif dist < ENEMY_DETECT_RANGE and dist > 0:
            if dist < ENEMY_ATTACK_RANGE:
                self.state = "attack"
                self.attack_timer -= dt
                if self.attack_timer <= 0:
                    self._melee_attack(player_pos, audio)
                    self.attack_timer = self.attack_cooldown
                    if random.random() < 0.25 and self.enemy_type == "runner":
                        direction = Bullet(self.pos, to_player.normalize(),
                                           self.damage * 0.6, "enemy", speed=320)
                        bullets_group.add(direction)
            else:
                self.state = "chase"
                move = to_player.normalize() * self.speed * dt
                # Desvio lateral ocasional
                if random.random() < ENEMY_DODGE_CHANCE * dt * 3:
                    self.dodge_dir = to_player.normalize().rotate(90 * random.choice([-1, 1]))
                    self.dodge_timer = 0.25
                else:
                    self._move(move, walls)
        else:
            self.state = "idle"

        self.anim_timer += dt
        if self.anim_timer > 0.15:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4
        # Corrige qualquer sobreposição residual (ex.: empurrão entre inimigos)
        if walls:
            self.pos = _resolve_wall_overlap(self.pos, self.hitbox_size, walls)
        self._refresh_sprite()
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def _move(self, delta: pygame.Vector2, walls: list[pygame.Rect]):
        self.pos = move_with_wall_collision(
            self.pos, self.hitbox_size, delta, walls, self.map_bounds,
        )

    def _melee_attack(self, player_pos: pygame.Vector2, audio):
        audio.play("hit")

    def take_damage(self, amount: float, particles, audio) -> bool:
        self.hp -= amount
        self.hit_flash = 0.12
        particles.emit_hit(self.pos)
        audio.play("enemy_hit")
        return self.hp <= 0

    def try_dodge_bullet(self, bullet_pos: pygame.Vector2):
        if self.dodge_timer > 0:
            return
        if random.random() < ENEMY_DODGE_CHANCE * 0.5:
            away = (self.pos - bullet_pos)
            if away.length_squared() > 0:
                self.dodge_dir = away.normalize()
                self.dodge_timer = 0.2


class EnemyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def alive_count(self) -> int:
        return len(self.sprites())


def pick_enemy_type(floor: int, force_boss: bool = False) -> str:
    if force_boss:
        return "boss"
    roll = random.random()
    if floor >= 4 and roll < 0.15:
        return "tank"
    if floor >= 2 and roll < 0.35:
        return "runner"
    return "grunt"
