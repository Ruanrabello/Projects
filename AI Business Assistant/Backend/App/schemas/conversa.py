from pydantic import BaseModel


class ConversaCreate(BaseModel):
    titulo: str


class ConversaResponse(BaseModel):
    id: int
    titulo: str
    usuario_id: int

    class Config:
        from_attributes = True
