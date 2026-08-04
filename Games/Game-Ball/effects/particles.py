"""
Sistema de partículas para impactos, mortes e coletas.
"""
import random
import pygame

from settings import COLOR_NEON_CYAN, COLOR_NEON_PINK, COLOR_NEON_YELLOW
from utils.sprites import create_particle_surface


class Particle:
    __slots__ = ("pos", "vel", "life", "max_life", "surf", "gravity")

    def __init__(self, pos, vel, life, surf, gravity=0.0):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.life = life
        self.max_life = life
        self.surf = surf
        self.gravity = gravity

    def update(self, dt: float) -> bool:
        self.life -= dt
        if self.life <= 0:
            return False
        self.vel.y += self.gravity * dt
        self.pos += self.vel * dt
        return True

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2):
        alpha = max(0, min(255, int(255 * (self.life / self.max_life))))
        s = self.surf.copy()
        s.set_alpha(alpha)
        surface.blit(s, (int(self.pos.x - camera_offset.x - s.get_width() / 2),
                         int(self.pos.y - camera_offset.y - s.get_height() / 2)))


class ParticleSystem:
    def __init__(self):
        self.particles: list[Particle] = []

    def emit_burst(self, pos: pygame.Vector2, color: tuple, count: int = 12,
                   speed: float = 180, size: int = 8):
        for _ in range(count):
            angle = random.uniform(0, 360)
            spd = random.uniform(speed * 0.3, speed)
            vel = pygame.Vector2(spd, 0).rotate(angle)
            life = random.uniform(0.25, 0.7)
            surf = create_particle_surface(random.randint(size - 2, size + 2), color)
            self.particles.append(Particle(pos, vel, life, surf, gravity=120))

    def emit_hit(self, pos: pygame.Vector2, color=COLOR_NEON_PINK):
        self.emit_burst(pos, color, count=8, speed=140, size=6)

    def emit_death(self, pos: pygame.Vector2, color=COLOR_NEON_YELLOW):
        self.emit_burst(pos, color, count=20, speed=220, size=10)

    def emit_pickup(self, pos: pygame.Vector2):
        self.emit_burst(pos, COLOR_NEON_CYAN, count=10, speed=100, size=5)

    def emit_dash(self, pos: pygame.Vector2):
        for _ in range(6):
            vel = pygame.Vector2(random.uniform(-80, 80), random.uniform(-80, 80))
            surf = create_particle_surface(5, COLOR_NEON_CYAN)
            self.particles.append(Particle(pos, vel, 0.3, surf))

    def update(self, dt: float):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2):
        for p in self.particles:
            p.draw(surface, camera_offset)
