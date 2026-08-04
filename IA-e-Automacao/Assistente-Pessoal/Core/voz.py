import logging
from functools import lru_cache

import pyttsx4
import speech_recognition as sr

from Config.keys import VOICE_RATE, VOICE_VOLUME, WAKE_WORDS


logger = logging.getLogger(__name__)
recognizer = sr.Recognizer()


@lru_cache(maxsize=1)
def _get_synthesizer():
    """Inicializa o sintetizador apenas quando a primeira resposta for falada."""
    try:
        synthesizer = pyttsx4.init("sapi5")
        synthesizer.setProperty("rate", VOICE_RATE)
        synthesizer.setProperty("volume", max(0.0, min(1.0, VOICE_VOLUME)))

        voices = synthesizer.getProperty("voices") or []
        if voices:
            synthesizer.setProperty("voice", voices[0].id)

        return synthesizer
    except Exception:
        logger.exception("Não foi possível inicializar o sintetizador de voz.")
        return None


def falar_texto(texto: str) -> bool:
    """Converte texto em áudio. Retorna False quando o áudio não está disponível."""
    mensagem = str(texto or "").strip()
    if not mensagem:
        return False

    synthesizer = _get_synthesizer()
    if synthesizer is None:
        print(mensagem)
        return False

    try:
        synthesizer.say(mensagem)
        synthesizer.runAndWait()
        return True
    except Exception:
        logger.exception("Falha ao reproduzir a resposta por voz.")
        print(mensagem)
        return False


def _extract_command(text: str) -> str:
    normalized_text = text.strip().lower()

    for wake_word in WAKE_WORDS:
        if normalized_text == wake_word:
            return ""

        prefix = f"{wake_word} "
        if normalized_text.startswith(prefix):
            return normalized_text[len(prefix):].strip()

    return ""


def ouvir_microfone(timeout: float = 5, phrase_time_limit: float = 12) -> str:
    """Escuta uma frase e retorna apenas comandos iniciados por uma wake word."""
    try:
        with sr.Microphone() as microphone:
            print("🎤 Ouvindo...")
            recognizer.adjust_for_ambient_noise(microphone, duration=0.6)
            audio = recognizer.listen(
                microphone,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )
    except sr.WaitTimeoutError:
        return ""
    except (OSError, AttributeError) as error:
        raise RuntimeError("Microfone indisponível ou não configurado.") from error

    try:
        recognized_text = recognizer.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as error:
        raise RuntimeError(
            "O serviço de reconhecimento de voz não está disponível."
        ) from error

    command = _extract_command(recognized_text)
    if command:
        print(f"Você disse: {command}")

    return command
