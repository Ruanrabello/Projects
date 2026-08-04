"""Versão 2: conversa local com histórico limitado."""

import os

from langchain_ollama import OllamaLLM


MODEL_NAME = os.getenv("OLLAMA_MODEL", "gemma4:latest")
MAX_INTERACTIONS = 10
EXIT_COMMANDS = {"sair", "encerrar", "parar"}


def build_prompt(history: list[tuple[str, str]], question: str) -> str:
    lines = ["Conversa anterior:"]
    for user_message, assistant_message in history[-MAX_INTERACTIONS:]:
        lines.append(f"Usuário: {user_message}")
        lines.append(f"Assistente: {assistant_message}")

    lines.append(f"Usuário: {question}")
    lines.append("Assistente:")
    return "\n".join(lines)


def main() -> None:
    model = OllamaLLM(model=MODEL_NAME)
    history: list[tuple[str, str]] = []

    print("Agente iniciado. Digite 'sair' para encerrar.")

    while True:
        try:
            question = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nConversa encerrada.")
            break

        if not question:
            continue
        if question.casefold() in EXIT_COMMANDS:
            break

        try:
            response = str(model.invoke(build_prompt(history, question))).strip()
        except Exception as error:
            print("IA: Não foi possível consultar o Ollama.")
            print(f"Detalhe técnico: {error}")
            continue

        print("IA:", response)
        history.append((question, response))
        del history[:-MAX_INTERACTIONS]


if __name__ == "__main__":
    main()
