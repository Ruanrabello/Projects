"""
Sistema de conquistas desbloqueáveis.
"""
import json

from settings import ACHIEVEMENTS_FILE, SAVES_DIR


ACHIEVEMENT_DEFS = {
    "first_blood": {"name": "Primeiro Sangue", "desc": "Elimine seu primeiro inimigo"},
    "floor_3": {"name": "Explorador", "desc": "Alcance o andar 3"},
    "floor_5": {"name": "Profundo", "desc": "Alcance o andar 5"},
    "boss_slayer": {"name": "Caçador de Boss", "desc": "Derrote um boss"},
    "no_damage_floor": {"name": "Fantasma", "desc": "Complete um andar sem levar dano"},
    "collector": {"name": "Colecionador", "desc": "Colete 10 power-ups"},
    "level_5": {"name": "Veterano", "desc": "Alcance nível 5"},
    "score_5000": {"name": "Lenda Neon", "desc": "Pontue 5000+ em uma partida"},
}


class AchievementManager:
    def __init__(self):
        self.unlocked: set[str] = set()
        self._session_stats = {
            "kills": 0,
            "powerups": 0,
            "floor_damage_taken": 0,
            "max_level": 1,
        }
        self._load()

    def _load(self):
        SAVES_DIR.mkdir(parents=True, exist_ok=True)
        if ACHIEVEMENTS_FILE.exists():
            try:
                with open(ACHIEVEMENTS_FILE, "r", encoding="utf-8") as f:
                    self.unlocked = set(json.load(f))
            except (json.JSONDecodeError, OSError):
                self.unlocked = set()

    def _persist(self):
        with open(ACHIEVEMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted(self.unlocked), f, indent=2)

    def unlock(self, key: str) -> bool:
        if key in ACHIEVEMENT_DEFS and key not in self.unlocked:
            self.unlocked.add(key)
            self._persist()
            return True
        return False

    def check_runtime(self, score: int, floor: int, level: int, boss_killed: bool):
        newly = []
        s = self._session_stats
        if s["kills"] >= 1 and self.unlock("first_blood"):
            newly.append("first_blood")
        if floor >= 3 and self.unlock("floor_3"):
            newly.append("floor_3")
        if floor >= 5 and self.unlock("floor_5"):
            newly.append("floor_5")
        if boss_killed and self.unlock("boss_slayer"):
            newly.append("boss_slayer")
        if s["floor_damage_taken"] == 0 and floor > 1 and self.unlock("no_damage_floor"):
            newly.append("no_damage_floor")
        if s["powerups"] >= 10 and self.unlock("collector"):
            newly.append("collector")
        if level >= 5 and self.unlock("level_5"):
            newly.append("level_5")
        if score >= 5000 and self.unlock("score_5000"):
            newly.append("score_5000")
        return [ACHIEVEMENT_DEFS[k] for k in newly]

    def on_kill(self):
        self._session_stats["kills"] += 1

    def on_powerup(self):
        self._session_stats["powerups"] += 1

    def on_damage(self):
        self._session_stats["floor_damage_taken"] += 1

    def on_boss_kill(self):
        self._session_stats["boss"] = True

    def new_floor(self):
        self._session_stats["floor_damage_taken"] = 0
