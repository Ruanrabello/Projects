"""
Menus: principal, pause, game over, configurações e transições.
"""
import math
import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_NEON_CYAN,
    COLOR_NEON_PINK, COLOR_NEON_PURPLE, FADE_COLOR, TRANSITION_DURATION,
    TITLE, GAME_VERSION,
)
from utils.leaderboard import Leaderboard
from utils.achievements import ACHIEVEMENT_DEFS


class Transition:
    def __init__(self):
        self.active = False
        self.timer = 0.0
        self.direction = 1  # 1 = fade out, -1 = fade in
        self.callback = None

    def start(self, callback=None):
        self.active = True
        self.timer = 0.0
        self.direction = 1
        self.callback = callback

    def update(self, dt: float) -> bool:
        if not self.active:
            return False
        self.timer += dt
        if self.timer >= TRANSITION_DURATION:
            if self.direction == 1:
                if self.callback:
                    self.callback()
                self.direction = -1
                self.timer = 0.0
            else:
                self.active = False
                return False
        return True

    def draw(self, surface: pygame.Surface):
        if not self.active:
            return
        t = min(1.0, self.timer / TRANSITION_DURATION)
        if self.direction == -1:
            t = 1.0 - t
        alpha = int(255 * t)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(FADE_COLOR)
        overlay.set_alpha(alpha)
        surface.blit(overlay, (0, 0))

    @property
    def blocking(self) -> bool:
        return self.active and self.timer < TRANSITION_DURATION and self.direction == 1


class MenuManager:
    def __init__(self, save_data: dict):
        self.save_data = save_data
        self.font_title = pygame.font.SysFont("consolas", 64, bold=True)
        self.font_sub = pygame.font.SysFont("consolas", 22)
        self.font_item = pygame.font.SysFont("consolas", 28)
        self.font_sm = pygame.font.SysFont("consolas", 18)
        self.selected = 0
        self.bg_offset = 0.0
        self.transition = Transition()
        self.settings_selection = 0
        self.player_name = "NEON"
        self.show_leaderboard = False
        self.show_achievements = False

    def update_bg(self, dt: float):
        self.bg_offset += dt * 30

    def draw_animated_bg(self, surface: pygame.Surface, bg_surface: pygame.Surface):
        surface.blit(bg_surface, (0, 0))
        # Linhas neon animadas
        for i in range(8):
            y = int((self.bg_offset + i * 90) % SCREEN_HEIGHT)
            alpha = 40 + int(20 * math.sin(self.bg_offset * 0.02 + i))
            color = (*COLOR_NEON_PURPLE[:3],)
            pygame.draw.line(surface, (*COLOR_NEON_CYAN[:2], min(255, color[2] + 80)),
                             (0, y), (SCREEN_WIDTH, y + 40), 1)

    def draw_main_menu(self, surface: pygame.Surface):
        title = self.font_title.render(TITLE, True, COLOR_NEON_CYAN)
        glow = self.font_title.render(TITLE, True, COLOR_NEON_PINK)
        surface.blit(glow, (SCREEN_WIDTH // 2 - title.get_width() // 2 + 3, 103))
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        sub = self.font_sub.render("Roguelike Dungeon Crawler", True, COLOR_WHITE)
        surface.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, 175))

        items = ["JOGAR", "LEADERBOARD", "CONQUISTAS", "CONFIGURAÇÕES", "SAIR"]
        for i, item in enumerate(items):
            color = COLOR_NEON_CYAN if i == self.selected else (120, 120, 150)
            prefix = "> " if i == self.selected else "  "
            txt = self.font_item.render(prefix + item, True, color)
            surface.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 280 + i * 48))

        hint = self.font_sm.render(
            f"W/S ou ↑↓ — Enter — Gamepad  |  Recorde: {self.save_data.get('high_score', 0)}",
            True, (150, 150, 170))
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))
        ver = self.font_sm.render(f"v{GAME_VERSION}", True, (80, 80, 100))
        surface.blit(ver, (16, SCREEN_HEIGHT - 30))

    def draw_pause(self, surface: pygame.Surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))
        title = self.font_title.render("PAUSE", True, COLOR_NEON_CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        items = ["CONTINUAR", "CONFIGURAÇÕES", "MENU PRINCIPAL"]
        for i, item in enumerate(items):
            color = COLOR_NEON_CYAN if i == self.selected else (120, 120, 150)
            txt = self.font_item.render(("> " if i == self.selected else "  ") + item, True, color)
            surface.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 340 + i * 48))

    def draw_game_over(self, surface: pygame.Surface, score: int, floor: int, kills: int,
                       is_high: bool):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((40, 0, 20, 200))
        surface.blit(overlay, (0, 0))
        title = self.font_title.render("GAME OVER", True, COLOR_NEON_PINK)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 140))

        stats = [
            f"Pontuação: {score}",
            f"Andar: {floor}",
            f"Eliminações: {kills}",
        ]
        for i, s in enumerate(stats):
            txt = self.font_item.render(s, True, COLOR_WHITE)
            surface.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 260 + i * 40))

        if is_high:
            hs = self.font_sub.render("NOVO RECORDE!", True, COLOR_NEON_CYAN)
            surface.blit(hs, (SCREEN_WIDTH // 2 - hs.get_width() // 2, 400))

        hint = self.font_sm.render("Enter — Menu  |  R — Reiniciar", True, (150, 150, 170))
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 80))

    def draw_settings(self, surface: pygame.Surface, settings: dict):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        title = self.font_title.render("CONFIGURAÇÕES", True, COLOR_NEON_CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        rows = [
            ("Volume Master", f"{settings.get('master_volume', 0.7):.1f}", "master_volume"),
            ("Volume Música", f"{settings.get('music_volume', 0.45):.1f}", "music_volume"),
            ("Volume SFX", f"{settings.get('sfx_volume', 0.8):.1f}", "sfx_volume"),
            ("Tela Cheia", "SIM" if settings.get("fullscreen") else "NÃO", "fullscreen"),
            ("Partículas", "SIM" if settings.get("particles", True) else "NÃO", "particles"),
            ("Screen Shake", "SIM" if settings.get("screen_shake", True) else "NÃO", "screen_shake"),
            ("VOLTAR", "", "back"),
        ]
        for i, (label, val, _) in enumerate(rows):
            color = COLOR_NEON_CYAN if i == self.settings_selection else (120, 120, 150)
            txt = self.font_item.render(
                f"{'>' if i == self.settings_selection else ' '} {label}: {val}", True, color)
            surface.blit(txt, (SCREEN_WIDTH // 2 - 220, 200 + i * 42))

        hint = self.font_sm.render(
            "← → ou Enter alternar tela cheia  |  F11 atalho  |  Esc voltar", True, (150, 150, 170))
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60))

    def draw_leaderboard(self, surface: pygame.Surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        title = self.font_title.render("LEADERBOARD", True, COLOR_NEON_CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 60))
        entries = Leaderboard.load()
        if not entries:
            txt = self.font_sub.render("Nenhuma pontuação ainda.", True, COLOR_WHITE)
            surface.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 300))
        for i, e in enumerate(entries):
            line = f"{i+1}. {e['name']} — {e['score']} (andar {e['floor']})"
            txt = self.font_item.render(line, True, COLOR_WHITE if i > 0 else COLOR_NEON_CYAN)
            surface.blit(txt, (SCREEN_WIDTH // 2 - 280, 160 + i * 38))
        hint = self.font_sm.render("Esc — Voltar", True, (150, 150, 170))
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))

    def draw_achievements(self, surface: pygame.Surface, unlocked: set):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        title = self.font_title.render("CONQUISTAS", True, COLOR_NEON_CYAN)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))
        for i, (key, ach) in enumerate(ACHIEVEMENT_DEFS.items()):
            done = key in unlocked
            color = COLOR_NEON_CYAN if done else (80, 80, 100)
            mark = "✓" if done else "○"
            txt = self.font_sm.render(f"{mark} {ach['name']}: {ach['desc']}", True, color)
            surface.blit(txt, (80, 120 + i * 28))
        hint = self.font_sm.render("Esc — Voltar", True, (150, 150, 170))
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))

    def handle_menu_input(self, event, max_items: int) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % max_items
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % max_items
            elif event.key == pygame.K_RETURN:
                return "confirm"
        if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
            return "confirm"
        return None
