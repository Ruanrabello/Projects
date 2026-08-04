import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "").strip()

WAKE_WORDS = tuple(
    word.strip().lower()
    for word in os.getenv("WAKE_WORDS", "jarvis,jarbas,jarvi").split(",")
    if word.strip()
)

VOICE_RATE = int(os.getenv("VOICE_RATE", "200"))
VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", "1.0"))
