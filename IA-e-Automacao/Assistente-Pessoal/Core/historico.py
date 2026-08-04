import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_PATH = BASE_DIR / "data" / "Historico.json"
HISTORY_LIMIT = 50
VALID_ROLES = {"user", "assistant"}


def _is_valid_message(item: object) -> bool:
    return (
        isinstance(item, dict)
        and item.get("role") in VALID_ROLES
        and isinstance(item.get("content"), str)
        and bool(item["content"].strip())
    )


def carregar_historico() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []

    try:
        with HISTORY_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return [item for item in data if _is_valid_message(item)][-HISTORY_LIMIT:]


def salvar_historico(historico: list[dict]) -> None:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = HISTORY_PATH.with_suffix(".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(historico[-HISTORY_LIMIT:], file, ensure_ascii=False, indent=2)
        temporary_path.replace(HISTORY_PATH)
    except OSError as error:
        temporary_path.unlink(missing_ok=True)
        raise RuntimeError("Não foi possível salvar o histórico local.") from error


def adicionar_mensagem(historico: list[dict], role: str, content: str) -> list[dict]:
    normalized_content = str(content or "").strip()

    if role not in VALID_ROLES:
        raise ValueError(f"Papel de mensagem inválido: {role}")

    if not normalized_content:
        return historico

    historico.append({"role": role, "content": normalized_content})
    del historico[:-HISTORY_LIMIT]
    salvar_historico(historico)
    return historico


def limpar_historico() -> None:
    try:
        HISTORY_PATH.unlink(missing_ok=True)
    except OSError as error:
        raise RuntimeError("Não foi possível limpar o histórico local.") from error
