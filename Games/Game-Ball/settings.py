"""
Configurações globais do Neon Depths.
Centraliza constantes, caminhos e presets gráficos.
"""
from pathlib import Path

# ── Caminhos ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
SOUNDS_DIR = BASE_DIR / "sounds"
SAVES_DIR = BASE_DIR / "saves"
EFFECTS_DIR = BASE_DIR / "effects"

for folder in (ASSETS_DIR, SOUNDS_DIR, SAVES_DIR):
    folder.mkdir(parents=True, exist_ok=True)

# ── Janela ────────────────────────────────────────────────────────────────
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Neon Depths"
GAME_VERSION = "1.0.0"

# ── Cores (paleta neon cyberpunk) ─────────────────────────────────────────
COLOR_BG = (12, 10, 28)
COLOR_FLOOR = (22, 18, 42)
COLOR_WALL = (45, 35, 75)
COLOR_NEON_CYAN = (0, 255, 220)
COLOR_NEON_PINK = (255, 60, 160)
COLOR_NEON_PURPLE = (160, 80, 255)
COLOR_NEON_YELLOW = (255, 220, 60)
COLOR_NEON_GREEN = (60, 255, 120)
COLOR_WHITE = (240, 240, 255)
COLOR_DARK = (8, 6, 18)
COLOR_HUD_BG = (20, 16, 40, 180)
COLOR_DAMAGE = (255, 80, 80)
COLOR_HEAL = (80, 255, 140)
COLOR_XP = (120, 200, 255)

# ── Gameplay ──────────────────────────────────────────────────────────────
TILE_SIZE = 48
PLAYER_HITBOX = (26, 26)
ENEMY_HITBOX = (30, 30)
BOSS_HITBOX = (50, 50)
MAP_WIDTH = 40
MAP_HEIGHT = 30
PLAYER_SPEED = 280
PLAYER_MAX_HP = 100
PLAYER_MAX_ENERGY = 100
ENERGY_REGEN = 18
BULLET_SPEED = 520
BULLET_DAMAGE = 22
FIRE_RATE = 0.14
DASH_COST = 25
DASH_SPEED = 600
DASH_DURATION = 0.18
INVINCIBILITY_TIME = 0.6
XP_PER_KILL = 25
XP_LEVEL_BASE = 80
XP_LEVEL_SCALE = 1.35

# ── Inimigos ──────────────────────────────────────────────────────────────
ENEMY_SPAWN_INTERVAL = 2.8
ENEMY_SPAWN_MIN = 0.8
ENEMY_MAX_ON_SCREEN = 18
ENEMY_ATTACK_RANGE = 55
ENEMY_DETECT_RANGE = 420
ENEMY_DODGE_CHANCE = 0.35

# ── Fases ─────────────────────────────────────────────────────────────────
FLOORS_PER_ACT = 3
BOSS_FLOOR_INTERVAL = 3
DIFFICULTY_HP_SCALE = 1.12
DIFFICULTY_DMG_SCALE = 1.08
DIFFICULTY_SPAWN_SCALE = 0.92

# ── Câmera ───────────────────────────────────────────────────────────────
CAMERA_LERP = 8.0
SHAKE_DECAY = 4.5
SHAKE_MAX = 14

# ── Áudio ─────────────────────────────────────────────────────────────────
MASTER_VOLUME = 0.7
MUSIC_VOLUME = 0.45
SFX_VOLUME = 0.8

# ── Save / Leaderboard ────────────────────────────────────────────────────
SAVE_FILE = SAVES_DIR / "save.json"
LEADERBOARD_FILE = SAVES_DIR / "leaderboard.json"
ACHIEVEMENTS_FILE = SAVES_DIR / "achievements.json"
MAX_LEADERBOARD = 10

# ── Estados do jogo ───────────────────────────────────────────────────────
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_SETTINGS = "settings"
STATE_TRANSITION = "transition"

# ── Transições ────────────────────────────────────────────────────────────
TRANSITION_DURATION = 0.55
FADE_COLOR = (8, 6, 20)

# ── Power-ups ─────────────────────────────────────────────────────────────
POWERUP_TYPES = ("health", "energy", "damage", "speed", "shield")
POWERUP_DURATION = 8.0

# ── Controles ─────────────────────────────────────────────────────────────
KEY_BINDINGS = {
    "up": ("w", "up"),
    "down": ("s", "down"),
    "left": ("a", "left"),
    "right": ("d", "right"),
    "dash": ("space",),
    "pause": ("escape", "p"),
    "shoot": ("mouse",),
}
