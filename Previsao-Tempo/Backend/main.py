import logging
import os
import re

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

API_KEY = os.getenv("API_KEY", "").strip()
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
REQUEST_TIMEOUT_SECONDS = 10

logger = logging.getLogger("weather_api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="API de Previsão do Tempo", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def validate_city(city: str) -> str:
    normalized_city = city.strip()

    if len(normalized_city) < 2 or len(normalized_city) > 50:
        raise HTTPException(
            status_code=400,
            detail="O nome da cidade deve ter entre 2 e 50 caracteres.",
        )

    if not re.fullmatch(r"[a-zA-ZÀ-ÿ\s\-']+", normalized_city):
        raise HTTPException(
            status_code=400,
            detail="Use apenas letras, espaços, hífens e apóstrofos.",
        )

    return normalized_city


def ensure_api_key() -> None:
    if not API_KEY:
        logger.error("A variável de ambiente API_KEY não foi configurada.")
        raise HTTPException(
            status_code=503,
            detail="O serviço de clima não está configurado.",
        )


def get_weather(city: str) -> dict:
    ensure_api_key()
    normalized_city = validate_city(city)

    parameters = {
        "q": normalized_city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br",
    }

    try:
        response = requests.get(
            OPENWEATHER_URL,
            params=parameters,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Cidade não encontrada.")

        if response.status_code in {401, 403}:
            logger.error("A OpenWeatherMap rejeitou a chave configurada.")
            raise HTTPException(
                status_code=503,
                detail="O serviço de clima está temporariamente indisponível.",
            )

        response.raise_for_status()
        data = response.json()

        return {
            "Cidade": data["name"],
            "País": data["sys"]["country"],
            "Temperatura": data["main"]["temp"],
            "Descrição": data["weather"][0]["description"],
            "Umidade": data["main"]["humidity"],
            "Sensação Térmica": data["main"]["feels_like"],
            "Velocidade do Vento": data["wind"]["speed"],
            "Pressão": data["main"]["pressure"],
        }

    except HTTPException:
        raise
    except requests.Timeout as error:
        logger.warning("Timeout ao buscar clima para %s: %s", normalized_city, error)
        raise HTTPException(
            status_code=504,
            detail="O serviço de previsão demorou demais para responder.",
        ) from error
    except requests.ConnectionError as error:
        logger.warning("Falha de conexão ao buscar clima para %s: %s", normalized_city, error)
        raise HTTPException(
            status_code=503,
            detail="Não foi possível conectar ao serviço de previsão.",
        ) from error
    except (requests.RequestException, KeyError, TypeError, ValueError) as error:
        logger.exception("Erro inesperado ao buscar clima para %s", normalized_city)
        raise HTTPException(
            status_code=502,
            detail="O serviço de previsão retornou uma resposta inválida.",
        ) from error


@app.get("/weather/{city}")
def weather(city: str) -> dict:
    return get_weather(city)


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "weather_service_configured": bool(API_KEY),
    }
