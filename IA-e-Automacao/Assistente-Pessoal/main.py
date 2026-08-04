import logging

from Core.comandos import interpretar_comando
from Core.historico import adicionar_mensagem, carregar_historico
from Core.ia import chamar_ia
from Core.voz import falar_texto, ouvir_microfone


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

EXIT_COMMANDS = {"parar", "encerrar", "finalizar", "sair"}


def executar_assistente() -> None:
    historico = carregar_historico()
    print("Assistente iniciado. Use uma wake word e diga 'parar' para finalizar.")

    while True:
        try:
            comando = ouvir_microfone()
        except RuntimeError as error:
            logger.warning("Entrada de voz indisponível: %s", error)
            falar_texto(str(error))
            continue
        except KeyboardInterrupt:
            print("\nEncerrando o assistente.")
            break

        if not comando:
            continue

        comando_normalizado = comando.casefold().strip()
        if comando_normalizado in EXIT_COMMANDS:
            falar_texto("Encerrando o assistente. Foi um prazer ajudar.")
            break

        try:
            resposta_comando = interpretar_comando(comando)
        except Exception:
            logger.exception("Falha inesperada ao interpretar um comando local.")
            resposta_comando = "Não consegui executar esse comando."

        if resposta_comando:
            falar_texto(resposta_comando)
            continue

        try:
            resposta_ia = chamar_ia(comando, historico)
        except RuntimeError as error:
            logger.warning("Integração com IA indisponível: %s", error)
            falar_texto(str(error))
            continue

        try:
            adicionar_mensagem(historico, "user", comando)
            adicionar_mensagem(historico, "assistant", resposta_ia)
        except RuntimeError as error:
            logger.warning("Não foi possível persistir o histórico: %s", error)

        falar_texto(resposta_ia)


if __name__ == "__main__":
    executar_assistente()
