"""
HUD moderno, notificações e overlays de feedback.
"""
import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_NEON_CYAN,
    COLOR_NEON_PINK, COLOR_NEON_YELLOW, COLOR_DAMAGE, COLOR_HEAL, COLOR_XP,
)


class UI:
    def __init__(self):
        pygame.font.init()
        self.font_sm = pygame.font.SysFont("consolas", 16)
        self.font_md = pygame.font.SysFont("consolas", 22, bold=True)
        self.font_lg = pygame.font.SysFont("consolas", 36, bold=True)
        self.font_title = pygame.font.SysFont("consolas", 52, bold=True)
        self.notifications: list[dict] = []
        self.damage_numbers: list[dict] = []
        self.achievement_popup: dict | None = None
        self.achievement_timer = 0.0

    def notify(self, text: str, color=COLOR_NEON_CYAN, duration: float = 2.5):
        self.notifications.append({"text": text, "color": color, "time": duration})

    def show_achievement(self, ach: dict):
        self.achievement_popup = ach
        self.achievement_timer = 3.5

    def add_damage_number(self, pos: tuple, amount: float, color=COLOR_DAMAGE):
        self.damage_numbers.append({
            "pos": pygame.Vector2(pos),
            "text": str(int(amount)),
            "color": color,
            "life": 0.8,
            "vy": -60,
        })

    def update(self, dt: float):
        for n in self.notifications:
            n["time"] -= dt
        self.notifications = [n for n in self.notifications if n["time"] > 0]

        for d in self.damage_numbers:
            d["life"] -= dt
            d["pos"].y += d["vy"] * dt
        self.damage_numbers = [d for d in self.damage_numbers if d["life"] > 0]

        if self.achievement_timer > 0:
            self.achievement_timer -= dt
            if self.achievement_timer <= 0:
                self.achievement_popup = None

    def draw_bar(self, surface, x, y, w, h, value, max_val, color, label=""):
        pygame.draw.rect(surface, (30, 25, 50), (x, y, w, h), border_radius=4)
        fill = int(w * max(0, min(1, value / max_val)) if max_val else 0)
        if fill > 0:
            pygame.draw.rect(surface, color, (x, y, fill, h), border_radius=4)
        pygame.draw.rect(surface, (80, 70, 120), (x, y, w, h), 1, border_radius=4)
        if label:
            txt = self.font_sm.render(label, True, COLOR_WHITE)
            surface.blit(txt, (x + 6, y + h // 2 - txt.get_height() // 2))

    def draw_hud(self, surface, player, floor: int, enemies_left: int):
        panel = pygame.Surface((280, 110), pygame.SRCALPHA)
        panel.fill((20, 16, 40, 200))
        surface.blit(panel, (16, 16))

        self.draw_bar(surface, 28, 28, 240, 18, player.hp, player.max_hp, COLOR_DAMAGE, "HP")
        self.draw_bar(surface, 28, 54, 240, 14, player.energy, player.max_energy, COLOR_NEON_CYAN, "NRG")
        xp_w = int(240 * player.xp / max(1, player.xp_to_next))
        pygame.draw.rect(surface, (30, 25, 50), (28, 78, 240, 10), border_radius=3)
        pygame.draw.rect(surface, COLOR_XP, (28, 78, xp_w, 10), border_radius=3)

        info = self.font_sm.render(
            f"NV{player.level}  ANDAR {floor}  INIM {enemies_left}  PTS {player.score}",
            True, COLOR_WHITE)
        surface.blit(info, (16, 132))

        # Power-ups ativos
        px = SCREEN_WIDTH - 160
        for i, (ptype, timer) in enumerate(player.powerups.items()):
            txt = self.font_sm.render(f"{ptype.upper()} {timer:.1f}s", True, COLOR_NEON_PINK)
            surface.blit(txt, (px, 16 + i * 22))

    def draw_damage_numbers(self, surface, camera_offset):
        for d in self.damage_numbers:
            alpha = int(255 * (d["life"] / 0.8))
            txt = self.font_md.render(d["text"], True, d["color"])
            txt.set_alpha(alpha)
            pos = (int(d["pos"].x - camera_offset.x), int(d["pos"].y - camera_offset.y))
            surface.blit(txt, pos)

    def draw_notifications(self, surface):
        y = SCREEN_HEIGHT - 80
        for n in self.notifications:
            txt = self.font_md.render(n["text"], True, n["color"])
            surface.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, y))
            y -= 30

    def draw_achievement_popup(self, surface):
        if not self.achievement_popup:
            return
        ach = self.achievement_popup
        box = pygame.Surface((400, 70), pygame.SRCALPHA)
        box.fill((40, 20, 60, 230))
        pygame.draw.rect(box, COLOR_NEON_YELLOW, box.get_rect(), 2, border_radius=8)
        t1 = self.font_md.render("CONQUISTA!", True, COLOR_NEON_YELLOW)
        t2 = self.font_sm.render(f"{ach['name']} — {ach['desc']}", True, COLOR_WHITE)
        box.blit(t1, (16, 10))
        box.blit(t2, (16, 38))
        surface.blit(box, (SCREEN_WIDTH // 2 - 200, 60))
