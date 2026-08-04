import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não configurada. Copie .env.example para .env.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

app = FastAPI(title="API de Cashback", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://calculadora-cashback-w34p.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ConsultaSQL(Base):
    __tablename__ = "cashback"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True, nullable=False)
    tipo_cliente = Column(String, index=True, nullable=False)
    valor_compra = Column(Float, nullable=False)
    valor_cashback = Column(Float, nullable=False)


Base.metadata.create_all(bind=engine)


class DadosEntrada(BaseModel):
    tipo_cliente: str = Field(pattern="^(normal|vip)$")
    valor_compra: float = Field(gt=0)
    cupom: float = Field(ge=0, le=100)


def calcular_valor_cashback(tipo_cliente: str, valor_compra: float, cupom: float) -> float:
    preco_final = valor_compra * (1 - cupom / 100)
    percentual = 0.10 if preco_final >= 500 else 0.05
    cashback = preco_final * percentual
    if tipo_cliente.lower() == "vip":
        cashback *= 1.10
    return round(cashback, 2)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/calcular-cashback")
def calcular_cashback(dados: DadosEntrada, request: Request, db: Session = Depends(get_db)):
    ip_cliente = request.client.host if request.client else "127.0.0.1"
    cashback = calcular_valor_cashback(
        dados.tipo_cliente,
        dados.valor_compra,
        dados.cupom,
    )

    consulta = ConsultaSQL(
        ip=ip_cliente,
        tipo_cliente=dados.tipo_cliente,
        valor_compra=dados.valor_compra,
        valor_cashback=cashback,
    )
    db.add(consulta)
    try:
        db.commit()
    except Exception as erro:
        db.rollback()
        raise HTTPException(status_code=500, detail="Não foi possível salvar o cálculo") from erro

    return {"cashback": cashback}


@app.get("/historico")
def historico(request: Request, db: Session = Depends(get_db)):
    ip_cliente = request.client.host if request.client else "127.0.0.1"
    consultas = (
        db.query(ConsultaSQL)
        .filter(ConsultaSQL.ip == ip_cliente)
        .order_by(ConsultaSQL.id.desc())
        .limit(10)
        .all()
    )

    return {
        "historico": [
            {
                "tipo_cliente": item.tipo_cliente,
                "valor_compra": item.valor_compra,
                "valor_cashback": item.valor_cashback,
            }
            for item in consultas
        ]
    }
