"""Versão 3: agente local com persona e histórico limitado."""

import os

from langchain_ollama import OllamaLLM


MODEL_NAME = os.getenv("OLLAMA_MODEL", "gemma4:latest")
MAX_INTERACTIONS = 10
EXIT_COMMANDS = {"sair", "encerrar", "parar"}
SYSTEM_PROMPT = (
    "Você é um professor especialista em Python e programação. "
    "Responda de forma simples, didática e com exemplos curtos quando necessário."
)


def build_prompt(history: list[tuple[str, str]], question: str) -> str:
    lines = [f"Instruções: {SYSTEM_PROMPT}", "", "Conversa:"]

    for user_message, assistant_message in history[-MAX_INTERACTIONS:]:
        lines.append(f"Aluno: {user_message}")
        lines.append(f"Professor: {assistant_message}")

    lines.append(f"Aluno: {question}")
    lines.append("Professor:")
    return "\n".join(lines)


def main() -> None:
    model = OllamaLLM(model=MODEL_NAME)
    history: list[tuple[str, str]] = []

    print("Professor de Python iniciado. Digite 'sair' para encerrar.")

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
