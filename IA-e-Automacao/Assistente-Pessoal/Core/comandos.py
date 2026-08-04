import logging
import os
import subprocess
import time
import webbrowser
from datetime import datetime
from functools import lru_cache

import pyautogui
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Config.keys import YOUTUBE_API_KEY


logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_youtube_client():
    """Cria o cliente somente quando uma busca de vídeo é solicitada."""
    if not YOUTUBE_API_KEY:
        raise RuntimeError(
            "A busca de vídeos não está configurada. Defina YOUTUBE_API_KEY no arquivo .env."
        )

    return build(
        "youtube",
        "v3",
        developerKey=YOUTUBE_API_KEY,
        cache_discovery=False,
    )


def abrir_youtube() -> str:
    webbrowser.open("https://www.youtube.com/")
    return "Abrindo YouTube."


def pausar_video() -> str:
    pyautogui.press("k")
    return "Reprodução pausada ou retomada."


def fechar_aba_atual() -> None:
    pyautogui.hotkey("ctrl", "w")


def abrir_google() -> str:
    webbrowser.open("https://www.google.com.br/")
    return "Abrindo Google."


def dizer_hora() -> str:
    agora = datetime.now().strftime("%H:%M")
    return f"Agora são {agora}."


def abrir_calculadora() -> str:
    if os.name != "nt":
        return "O comando da calculadora está disponível apenas no Windows."

    try:
        subprocess.Popen(["calc.exe"])
    except OSError:
        logger.exception("Não foi possível abrir a calculadora do Windows.")
        return "Não consegui abrir a calculadora."

    return "Abrindo calculadora."


def buscar_video(termo: str) -> str | None:
    consulta = termo.strip()
    if not consulta:
        return None

    try:
        resposta = (
            _get_youtube_client()
            .search()
            .list(
                q=consulta,
                part="snippet",
                maxResults=1,
                type="video",
            )
            .execute()
        )
    except RuntimeError:
        raise
    except HttpError as error:
        logger.warning("A YouTube Data API rejeitou a consulta: %s", error)
        raise RuntimeError(
            "A busca de vídeos está temporariamente indisponível."
        ) from error
    except Exception as error:
        logger.exception("Falha inesperada ao buscar vídeo.")
        raise RuntimeError(
            "Não foi possível concluir a busca de vídeos."
        ) from error

    items = resposta.get("items", [])
    if not items:
        return None

    video_id = items[0].get("id", {}).get("videoId")
    if not video_id:
        return None

    return f"https://www.youtube.com/watch?v={video_id}"


def abrir_video(termo: str, fechar_anterior: bool = False) -> str:
    try:
        url = buscar_video(termo)
    except RuntimeError as error:
        return str(error)

    if not url:
        return "Não encontrei um vídeo para esse termo."

    if fechar_anterior:
        fechar_aba_atual()
        time.sleep(0.3)

    webbrowser.open(url)
    return f"Reproduzindo {termo} no YouTube."


def interpretar_comando(texto: str) -> str | None:
    comando = texto.strip().lower()
    if not comando:
        return None

    for palavra in ("tocar", "ouvir", "reproduzir"):
        prefixo = f"{palavra} "
        if comando.startswith(prefixo):
            termo_busca = comando[len(prefixo):].strip()
            return abrir_video(termo_busca) if termo_busca else "Qual música você quer ouvir?"

    if "youtube" in comando:
        return abrir_youtube()
    if "google" in comando:
        return abrir_google()
    if "pausar" in comando or "despausar" in comando:
        return pausar_video()
    if "hora" in comando:
        return dizer_hora()
    if "calculadora" in comando:
        return abrir_calculadora()

    return None
