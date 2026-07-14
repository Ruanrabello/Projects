from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.conversa import ConversaCreate, ConversaResponse
from services.chatservice import criar_conversa, listar_conversas
from database.models import Conversa
from typing import List



router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.get("/conversas", response_model=List[ConversaResponse])

def listar_conversas_endpoint(db: Session = Depends(get_db)):
    return listar_conversas(db,usuario_id= 1)



@router.post( "/conversas", response_model=ConversaResponse)

def nova_conversa(
    conversa: ConversaCreate,
    db: Session = Depends(get_db)
):
    return criar_conversa(
        db=db,
        titulo=conversa.titulo,
        usuario_id=1                     #Porque ainda não temos login. mais pra frente mudara usuario_id = usuario_logado.id
    )
