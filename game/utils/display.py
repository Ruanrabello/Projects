"""
Gerenciador de tela — suporta ultrawide (ex.: 2560×1080) com letterbox.
O jogo renderiza sempre em 1280×720 e escala para o monitor.
"""
import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG, TITLE


class DisplayManager:
    def __init__(self, game_width: int = SCREEN_WIDTH, game_height: int = SCREEN_HEIGHT):
        self.game_w = game_width
        self.game_h = game_height
        self.surface = pygame.Surface((game_width, game_height))
        self.window: pygame.Surface | None = None
        self.fullscreen = False
        self.scale_rect = pygame.Rect(0, 0, game_width, game_height)
        self.window_size = (game_width, game_height)

    def apply_mode(self, fullscreen: bool):
        self.fullscreen = fullscreen
        if fullscreen:
            info = pygame.display.Info()
            w, h = info.current_w, info.current_h
            # Fallback para ultrawide comum se o SDL não reportar tamanho
            if w < 640 or h < 480:
                w, h = 2560, 1080
            try:
                self.window = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
            except pygame.error:
                self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            w, h = self.window.get_size()
        else:
            self.window = pygame.display.set_mode(
                (self.game_w, self.game_h),
                pygame.RESIZABLE,
            )
            w, h = self.window.get_size()

        self.window_size = (w, h)
        self._calc_scale(w, h)
        pygame.display.set_caption(TITLE)

    def _calc_scale(self, window_w: int, window_h: int):
        """Escala mantendo 16:9 — em 21:9 ficam barras pretas nas laterais."""
        scale = min(window_w / self.game_w, window_h / self.game_h)
        sw = max(1, int(self.game_w * scale))
        sh = max(1, int(self.game_h * scale))
        x = (window_w - sw) // 2
        y = (window_h - sh) // 2
        self.scale_rect = pygame.Rect(x, y, sw, sh)

    def screen_to_game(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Converte coordenada do mouse na janela → coordenada do jogo (1280×720)."""
        mx, my = pos
        sr = self.scale_rect
        if sr.width <= 0 or sr.height <= 0:
            return mx, my
        if not sr.collidepoint(mx, my):
            mx = max(sr.left, min(mx, sr.right - 1))
            my = max(sr.top, min(my, sr.bottom - 1))
        gx = (mx - sr.x) * self.game_w / sr.width
        gy = (my - sr.y) * self.game_h / sr.height
        return int(gx), int(gy)

    def present(self):
        if self.window is None:
            return
        win_w, win_h = self.window.get_size()
        if (win_w, win_h) != self.window_size:
            self.window_size = (win_w, win_h)
            self._calc_scale(win_w, win_h)

        scaled = pygame.transform.smoothscale(self.surface, self.scale_rect.size)
        self.window.fill(COLOR_BG)
        self.window.blit(scaled, self.scale_rect.topleft)
        pygame.display.flip()
