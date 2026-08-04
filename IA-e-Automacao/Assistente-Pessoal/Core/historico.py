import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_HISTORICO = BASE_DIR / "data" / "Historico.json"
LIMITE_MENSAGENS = 50


def carregar_historico() -> list[dict]:
    if not CAMINHO_HISTORICO.exists():
        return []

    try:
        with CAMINHO_HISTORICO.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        return []

    return dados if isinstance(dados, list) else []


def salvar_historico(historico: list[dict]) -> None:
    CAMINHO_HISTORICO.parent.mkdir(parents=True, exist_ok=True)

    with CAMINHO_HISTORICO.open("w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, ensure_ascii=False, indent=2)


def adicionar_mensagem(historico: list[dict], role: str, content: str) -> list[dict]:
    conteudo = content.strip()

    if not conteudo:
        return historico

    historico.append({"role": role, "content": conteudo})

    if len(historico) > LIMITE_MENSAGENS:
        del historico[:-LIMITE_MENSAGENS]

    salvar_historico(historico)
    return historico


def limpar_historico() -> None:
    try:
        CAMINHO_HISTORICO.unlink(missing_ok=True)
    except OSError as erro:
        raise RuntimeError(f"Não foi possível limpar o histórico: {erro}") from erro
