"""Versão 1: chamada simples a um modelo local do Ollama."""

import os

from langchain_ollama import OllamaLLM


MODEL_NAME = os.getenv("OLLAMA_MODEL", "gemma4:latest")


def main() -> None:
    model = OllamaLLM(model=MODEL_NAME)

    try:
        response = model.invoke("Olá! Apresente-se em uma frase.")
    except Exception as error:
        raise RuntimeError(
            "Não foi possível consultar o Ollama. Verifique se o serviço e o modelo estão disponíveis."
        ) from error

    print(response)


if __name__ == "__main__":
    main()
