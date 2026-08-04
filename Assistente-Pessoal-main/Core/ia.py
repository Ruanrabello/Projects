from groq import Groq

from Config.keys import GROQ_API_KEY
from Core.Personalidade import SYSTEM_PROMPT


MODELO_PADRAO = "llama-3.1-8b-instant"


def _criar_cliente() -> Groq:
    if not GROQ_API_KEY or GROQ_API_KEY == "your-groq-api-key-here":
        raise RuntimeError(
            "A variável GROQ_API_KEY não foi configurada. "
            "Defina a chave no ambiente antes de iniciar o assistente."
        )

    return Groq(api_key=GROQ_API_KEY)


def chamar_ia(mensagem: str, historico: list[dict] | None = None) -> str:
    """Envia a mensagem atual e o histórico para a API da Groq."""
    if not mensagem or not mensagem.strip():
        return "Não consegui identificar uma mensagem para enviar à IA."

    mensagens_para_api = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *(historico or []),
        {"role": "user", "content": mensagem.strip()},
    ]

    try:
        resposta = _criar_cliente().chat.completions.create(
            model=MODELO_PADRAO,
            messages=mensagens_para_api,
        )
    except Exception as erro:
        raise RuntimeError(f"Não foi possível consultar a IA: {erro}") from erro

    texto = resposta.choices[0].message.content

    if not texto or not texto.strip():
        return "A IA respondeu sem conteúdo. Tente novamente."

    return texto.strip()
