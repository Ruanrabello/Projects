from sqlalchemy.orm import Session

from database.models.Conversa import Conversa



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
