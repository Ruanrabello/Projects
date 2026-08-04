"""
Leaderboard local em JSON.
"""
import json
from datetime import datetime

from settings import LEADERBOARD_FILE, MAX_LEADERBOARD, SAVES_DIR


class Leaderboard:
    @classmethod
    def load(cls) -> list[dict]:
        SAVES_DIR.mkdir(parents=True, exist_ok=True)
        if LEADERBOARD_FILE.exists():
            try:
                with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return []

    @classmethod
    def add_entry(cls, name: str, score: int, floor: int):
        entries = cls.load()
        entries.append({
            "name": name[:12],
            "score": score,
            "floor": floor,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        entries.sort(key=lambda e: e["score"], reverse=True)
        entries = entries[:MAX_LEADERBOARD]
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        return entries

    @classmethod
    def is_high_score(cls, score: int) -> bool:
        entries = cls.load()
        if len(entries) < MAX_LEADERBOARD:
            return True
        return score > entries[-1]["score"] if entries else True
