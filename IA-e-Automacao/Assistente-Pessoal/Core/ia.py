import logging
from functools import lru_cache

from groq import Groq

from Config.keys import GROQ_API_KEY, GROQ_MODEL
from Core.Personalidade import SYSTEM_PROMPT


logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _criar_cliente() -> Groq:
    if not GROQ_API_KEY:
        raise RuntimeError(
            "A integração com IA não está configurada. Defina GROQ_API_KEY no arquivo .env."
        )

    return Groq(api_key=GROQ_API_KEY)


def chamar_ia(mensagem: str, historico: list[dict] | None = None) -> str:
    """Envia a mensagem atual e um histórico limitado para a API da Groq."""
    conteudo = mensagem.strip()
    if not conteudo:
        return "Não consegui identificar uma mensagem para enviar à IA."

    mensagens_para_api = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *(historico or []),
        {"role": "user", "content": conteudo},
    ]

    try:
        resposta = _criar_cliente().chat.completions.create(
            model=GROQ_MODEL,
            messages=mensagens_para_api,
        )
    except RuntimeError:
        raise
    except Exception as error:
        logger.exception("Falha ao consultar a API da Groq.")
        raise RuntimeError(
            "Não foi possível consultar a IA neste momento. Tente novamente mais tarde."
        ) from error

    if not resposta.choices:
        return "A IA não retornou uma resposta. Tente novamente."

    texto = resposta.choices[0].message.content
    if not texto or not texto.strip():
        return "A IA respondeu sem conteúdo. Tente novamente."

    return texto.strip()
