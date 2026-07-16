from sqlalchemy.orm import Session

from database.models.Conversa import Conversa

from database.models.Mensagem import Mensagem

from services.gemma4_latest import gerar_resposta_ia



def criar_conversa(
    db: Session,
    titulo: str,
    usuario_id: int
):
    conversa = Conversa(
        titulo=titulo,
        usuario_id=usuario_id
    )

    db.add(conversa)

    db.commit()

    db.refresh(conversa)

    return conversa



def listar_conversas(db: Session, usuario_id: int):
    return (
        db.query(Conversa)
        .filter(Conversa.usuario_id == usuario_id)
        .all()
    )

# -----------------------------------------------------------

def listar_mensagens(db:Session, conversa_id: int):
    return (
        db.query(Mensagem)
        .filter(Mensagem.conversa_id == conversa_id)
        .all()
    )


def criar_mensagem(
        db: Session,
        conversa_id: int,
        usuario: str,
        texto: str
):
    # salva mensagem do usuário
    mensagem = Mensagem(
        conversa_id = conversa_id,
        usuario = usuario,
        texto = texto
    )

    db.add(mensagem)
    db.commit()
    db.refresh(mensagem)

    try:
        resposta = gerar_resposta_ia(texto)
    except Exception as e:
        resposta = "Desculpe, não consegui gerar uma resposta agora. Tente novamente."
        print(f"Erro ao gerar resposta da IA: {e}")

    # gera resposta da IA
    resposta = gerar_resposta_ia(texto)

    # salva resposta da IA
    mensagem_ai = Mensagem(
        conversa_id = conversa_id,
        usuario = 'ai',
        texto = resposta
    )

    db.add(mensagem_ai)
    db.commit()
    db.refresh(mensagem_ai)

    return mensagem
