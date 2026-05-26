"""
Jogador: movimento, combate, dash, XP e power-ups.
"""
import math
import pygame

from settings import (
    PLAYER_SPEED, PLAYER_MAX_HP, PLAYER_MAX_ENERGY, ENERGY_REGEN,
    FIRE_RATE, DASH_COST, DASH_SPEED, DASH_DURATION, INVINCIBILITY_TIME,
    BULLET_DAMAGE, XP_PER_KILL, XP_LEVEL_BASE, XP_LEVEL_SCALE,
    POWERUP_DURATION, PLAYER_HITBOX,
)
from bullet import Bullet
from utils.sprites import create_player_frames
from utils.collision import move_with_wall_collision, _resolve_wall_overlap


class Player(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.frames = create_player_frames()
        self.anim_index = 0
        self.anim_timer = 0.0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(int(x), int(y)))

        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.energy = PLAYER_MAX_ENERGY
        self.max_energy = PLAYER_MAX_ENERGY
        self.speed = PLAYER_SPEED
        self.base_damage = BULLET_DAMAGE
        self.damage_mult = 1.0
        self.speed_mult = 1.0
        self.shield = 0.0

        self.level = 1
        self.xp = 0
        self.xp_to_next = XP_LEVEL_BASE
        self.score = 0
        self.kills = 0

        self.fire_cooldown = 0.0
        self.dash_timer = 0.0
        self.dash_cooldown = 0.0
        self.invincible = 0.0
        self.facing = pygame.Vector2(1, 0)

        self.powerups: dict[str, float] = {}
        self.map_bounds: pygame.Rect | None = None

    @property
    def hitbox(self) -> pygame.Rect:
        from utils.collision import make_hitbox
        return make_hitbox(self.pos, PLAYER_HITBOX)

    @property
    def damage(self) -> float:
        mult = self.damage_mult
        if "damage" in self.powerups:
            mult *= 1.5
        return self.base_damage * mult

    @property
    def move_speed(self) -> float:
        spd = self.speed * self.speed_mult
        if "speed" in self.powerups:
            spd *= 1.35
        return spd

    def update(self, dt: float, move_dir: pygame.Vector2, aim_dir: pygame.Vector2,
               walls: list[pygame.Rect], want_shoot: bool, want_dash: bool,
               bullets_group, particles, audio):
        # Power-up timers
        expired = [k for k, t in self.powerups.items() if t <= 0]
        for k in expired:
            del self.powerups[k]
        for k in list(self.powerups):
            self.powerups[k] -= dt

        if aim_dir.length_squared() > 0:
            self.facing = aim_dir

        # Dash
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
        if self.dash_timer > 0:
            self.dash_timer -= dt
            move = self.facing * DASH_SPEED * dt
            self._move(move, walls)
            self.invincible = max(self.invincible, 0.05)
        elif move_dir.length_squared() > 0:
            self._move(move_dir * self.move_speed * dt, walls)
            self.anim_timer += dt
            if self.anim_timer > 0.12:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(self.frames)

        self.energy = min(self.max_energy, self.energy + ENERGY_REGEN * dt)
        if self.invincible > 0:
            self.invincible -= dt

        self.fire_cooldown = max(0, self.fire_cooldown - dt)

        if want_dash and self.dash_timer <= 0 and self.dash_cooldown <= 0:
            if self.energy >= DASH_COST:
                self.energy -= DASH_COST
                self.dash_timer = DASH_DURATION
                self.dash_cooldown = 0.5
                self.invincible = DASH_DURATION
                particles.emit_dash(self.pos)
                audio.play("dash")

        if want_shoot and self.fire_cooldown <= 0 and self.energy >= 5:
            self.fire_cooldown = FIRE_RATE
            self.energy -= 5
            spread = 0.04 if self.level < 5 else 0.02
            direction = self.facing.rotate(math.degrees(spread * (math.sin(self.anim_index) - 0.5)))
            bullet = Bullet(self.pos + direction * 20, direction, self.damage, "player")
            bullets_group.add(bullet)
            audio.play("shoot")

        # Animação / sprite
        self.image = self.frames[self.anim_index]
        if self.invincible > 0 and int(self.invincible * 20) % 2 == 0:
            self.image = self.image.copy()
            self.image.set_alpha(140)
        if walls:
            self.pos = _resolve_wall_overlap(self.pos, PLAYER_HITBOX, walls)

        angle = math.degrees(math.atan2(self.facing.y, self.facing.x)) + 90
        self.image = pygame.transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def _move(self, delta: pygame.Vector2, walls: list[pygame.Rect]):
        self.pos = move_with_wall_collision(
            self.pos, PLAYER_HITBOX, delta, walls, self.map_bounds,
        )

    def take_damage(self, amount: float, audio) -> bool:
        if self.invincible > 0 or self.shield > 0:
            if self.shield > 0:
                self.shield = max(0, self.shield - amount)
            return False
        self.hp -= amount
        self.invincible = INVINCIBILITY_TIME
        audio.play("hurt")
        return self.hp <= 0

    def heal(self, amount: float):
        self.hp = min(self.max_hp, self.hp + amount)

    def add_xp(self, amount: int, audio=None) -> bool:
        """Retorna True se subiu de nível."""
        self.xp += amount
        leveled = False
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(XP_LEVEL_BASE * (XP_LEVEL_SCALE ** (self.level - 1)))
            self.max_hp += 10
            self.hp = min(self.max_hp, self.hp + 20)
            self.base_damage += 3
            leveled = True
            if audio:
                audio.play("level_up")
        return leveled

    def on_kill(self, xp_bonus: int = XP_PER_KILL, audio=None):
        self.kills += 1
        self.score += xp_bonus
        self.add_xp(xp_bonus, audio)

    def apply_powerup(self, ptype: str, audio, particles):
        audio.play("pickup")
        particles.emit_pickup(self.pos)
        if ptype == "health":
            self.heal(35)
        elif ptype == "energy":
            self.energy = self.max_energy
        elif ptype in ("damage", "speed", "shield"):
            self.powerups[ptype] = POWERUP_DURATION
            if ptype == "shield":
                self.shield = 50

    @property
    def center(self) -> pygame.Vector2:
        return self.pos
