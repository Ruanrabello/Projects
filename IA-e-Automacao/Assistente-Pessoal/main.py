from Core.comandos import interpretar_comando
from Core.historico import adicionar_mensagem, carregar_historico
from Core.ia import chamar_ia
from Core.voz import falar_texto, ouvir_microfone


def executar_assistente() -> None:
    historico = carregar_historico()

    print("Assistente iniciado. Diga 'parar' ou 'encerrar' para finalizar.")

    while True:
        try:
            comando = ouvir_microfone()
        except Exception as erro:
            print(f"Erro ao acessar o microfone: {erro}")
            falar_texto("Não consegui acessar o microfone. Tente novamente.")
            continue

        if not comando or not comando.strip():
            continue

        comando = comando.strip()
        comando_normalizado = comando.lower()

        if "parar" in comando_normalizado or "encerrar" in comando_normalizado:
            falar_texto("Encerrando o assistente. Foi um prazer ajudar.")
            break

        try:
            resposta_comando = interpretar_comando(comando)
        except Exception as erro:
            print(f"Erro ao interpretar comando: {erro}")
            resposta_comando = None

        if resposta_comando:
            falar_texto(resposta_comando)
            continue

        try:
            resposta_ia = chamar_ia(comando, historico)
        except RuntimeError as erro:
            resposta_ia = str(erro)
            print(resposta_ia)

        adicionar_mensagem(historico, "user", comando)
        adicionar_mensagem(historico, "assistant", resposta_ia)
        falar_texto(resposta_ia)


if __name__ == "__main__":
    executar_assistente()
