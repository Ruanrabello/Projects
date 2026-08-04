"""Persistência segura do progresso local em JSON."""

import json
import logging
from datetime import datetime

from settings import SAVE_FILE, SAVES_DIR


logger = logging.getLogger(__name__)


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
        defaults = cls.default_data()

        if not SAVE_FILE.exists():
            return defaults

        try:
            with SAVE_FILE.open("r", encoding="utf-8") as file:
                saved_data = json.load(file)
        except (json.JSONDecodeError, OSError):
            logger.warning("Save inválido ou inacessível. Usando valores padrão.", exc_info=True)
            return defaults

        if not isinstance(saved_data, dict):
            return defaults

        merged_data = {**defaults, **saved_data}
        saved_settings = saved_data.get("settings", {})
        if isinstance(saved_settings, dict):
            merged_data["settings"] = {
                **defaults["settings"],
                **saved_settings,
            }
        else:
            merged_data["settings"] = defaults["settings"]

        return merged_data

    @classmethod
    def save(cls, data: dict) -> None:
        SAVES_DIR.mkdir(parents=True, exist_ok=True)
        data["last_played"] = datetime.now().isoformat(timespec="seconds")
        temporary_file = SAVE_FILE.with_suffix(".tmp")

        try:
            with temporary_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            temporary_file.replace(SAVE_FILE)
        except OSError:
            temporary_file.unlink(missing_ok=True)
            logger.exception("Não foi possível salvar o progresso.")

    @classmethod
    def update_run(cls, score: int, floor: int, kills: int) -> dict:
        data = cls.load()
        data["high_score"] = max(int(data.get("high_score", 0)), int(score))
        data["best_floor"] = max(int(data.get("best_floor", 1)), int(floor))
        data["total_kills"] = int(data.get("total_kills", 0)) + max(0, int(kills))
        cls.save(data)
        return data
