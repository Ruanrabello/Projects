"""
Persistência de progresso em JSON.
"""
import json
from datetime import datetime
from pathlib import Path

from settings import SAVE_FILE, SAVES_DIR


class SaveSystem:
    @staticmethod
    def default_data() -> dict:
        return {
            "high_score": 0,
            "total_kills": 0,
            "best_floor": 1,
            "unlocked_achievements": [],
            "settings": {
                "master_volume": 0.7,
                "music_volume": 0.45,
                "sfx_volume": 0.8,
                "fullscreen": False,
                "particles": True,
                "screen_shake": True,
            },
            "last_played": None,
        }

    @classmethod
    def load(cls) -> dict:
        SAVES_DIR.mkdir(parents=True, exist_ok=True)
        if SAVE_FILE.exists():
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                base = cls.default_data()
                base.update(data)
                return base
            except (json.JSONDecodeError, OSError):
                pass
        return cls.default_data()

    @classmethod
    def save(cls, data: dict):
        SAVES_DIR.mkdir(parents=True, exist_ok=True)
        data["last_played"] = datetime.now().isoformat()
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def update_run(cls, score: int, floor: int, kills: int):
        data = cls.load()
        data["high_score"] = max(data["high_score"], score)
        data["best_floor"] = max(data["best_floor"], floor)
        data["total_kills"] = data.get("total_kills", 0) + kills
        cls.save(data)
        return data
