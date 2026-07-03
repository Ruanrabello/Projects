import os
import re
import logging
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="API de Previsão do Tempo", version="1.0.0")

load_dotenv()
API_KEY = os.getenv("API_KEY")

logger = logging.getLogger("weather_api")
logger.setLevel(logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_methods=["*"],
    allow_headers=["*"]
)


def validate_city(city: str) -> bool:
    if not city or len(city) < 2 or len(city) > 50:             # Verifica se a cidade é nula ou tem um comprimento inválido
        return False

    if not re.match(r"^[a-zA-ZÀ-ÿ\s\-]+$", city):               # Permite apenas letras, hífens e espaços
        return False

    return True


def get_weather(city: str):

    if not validate_city(city):
        logger.warning(f"Nome de cidade inválido: {city}")                              # Registra um aviso no log sobre o nome da cidade inválido → Para você (desenvolvedor)
        raise HTTPException(status_code=400, detail="Nome de cidade inválido")          # Retorna um erro HTTP 400 com a mensagem → Para o usuário/cliente da API

    try:                                                        # Tente executar este código. Se ocorrer algum erro, vá para um dos blocos except
        url = "https://api.openweathermap.org/data/2.5/weather"
        parameters = {
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "pt_br"
        }

        response = requests.get(url, params=parameters, timeout=10)
        response.raise_for_status()                                                                     # Verifica se a resposta foi bem-sucedida (status code 200-299)
        data = response.json()
        return {
            "Cidade": data["name"],
            "País": data["sys"]["country"],
            "Temperatura": data["main"]["temp"],
            "Descrição": data["weather"][0]["description"],
            "Umidade": data["main"]["humidity"],
            "Sensação Térmica": data["main"]["feels_like"],
            "Velocidade do Vento": data["wind"]["speed"],
            "Pressão": data["main"]["pressure"]
        }

    except requests.exceptions.Timeout:                                                                 # Se a requisição exceder o timeout, registre o erro e retorne um erro HTTP 504

        logger.error(f"Timeout ao buscar clima para {city}")                                            # Registra o erro de timeout no log(terminal ou arquivo de log) → Para você (desenvolvedor)
        raise HTTPException(status_code=504, detail="Serviço de previsão indisponível (timeout)")       # Retorna um erro HTTP 504  com a mensagem→ Para o usuário/cliente da API

    except requests.exceptions.ConnectionError:                                                         # Se ocorrer um erro de conexão, registre o erro e retorne um erro HTTP 503

        logger.error(f"Erro de conexão ao buscar clima para {city}")                                    # Registra o erro de conexão no log(terminal ou arquivo de log) → Para você (desenvolvedor)
        raise HTTPException(status_code=503, detail="Serviço de previsão indisponível")                 # Retorna um erro HTTP 504  com a mensagem → Para o usuário/cliente da API

    except requests.exceptions.RequestException as e:                                                   # Para outros erros relacionados à requisição, registre o erro e retorne um erro HTTP 500

        logger.error(f"Erro ao buscar clima para {city}: {e}")                                          # Registra o erro genérico no log(terminal ou arquivo de log) → Para você (desenvolvedor)
        raise HTTPException(status_code=500, detail="Erro ao buscar previsão do tempo")                 # Retorna um erro HTTP 500 com a mensagem → Para o usuário/cliente da API


@app.get("/weather/{city}")
def weather(city: str):
    return get_weather(city)


@app.get("/health")
def health_check():
    return {"status": "ok"}

