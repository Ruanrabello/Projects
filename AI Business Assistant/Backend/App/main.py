from fastapi import FastAPI

from routers import chat
from routers import documentos
from routers import relatorios

from database.models.Conversa import Conversa
from database.models.Documentos import Documento
from database.models.Mensagem import Mensagem
from database.models.Usuario import Usuario

from database.database import Base, engine

app = FastAPI(
    title="AI Business Assistant API"
)

Base.metadata.create_all(bind=engine)


app.include_router(chat.router)

app.include_router(documentos.router)

app.include_router(relatorios.router)


@app.get("/")
def home():
    return {
        "message": "API funcionando corretamente"
    }


