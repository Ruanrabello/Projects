import logging
import os
from contextlib import asynccontextmanager
from decimal import Decimal, ROUND_HALF_UP

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, Float, Integer, String, create_engine, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker


load_dotenv()
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não configurada. Copie .env.example para .env.")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,https://calculadora-cashback-w34p.vercel.app",
    ).split(",")
    if origin.strip()
]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class ConsultaSQL(Base):
    __tablename__ = "cashback"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True, nullable=False)
    tipo_cliente = Column(String, index=True, nullable=False)
    valor_compra = Column(Float, nullable=False)
    valor_cashback = Column(Float, nullable=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API de Cashback",
    description="Calcula cashback, aplica cupons e mantém um histórico limitado por cliente.",
    version="1.1.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class DadosEntrada(BaseModel):
    tipo_cliente: str
    valor_compra: float = Field(gt=0, le=10_000_000)
    cupom: float = Field(ge=0, le=100)

    @field_validator("tipo_cliente")
    @classmethod
    def validar_tipo_cliente(cls, value: str) -> str:
        normalized_value = value.strip().lower()
        if normalized_value not in {"normal", "vip"}:
            raise ValueError("tipo_cliente deve ser 'normal' ou 'vip'")
        return normalized_value


class CashbackResponse(BaseModel):
    valor_final: float
    cashback: float


class HistoricoItem(BaseModel):
    tipo_cliente: str
    valor_compra: float
    valor_cashback: float


class HistoricoResponse(BaseModel):
    historico: list[HistoricoItem]


def calcular_valores(tipo_cliente: str, valor_compra: float, cupom: float) -> tuple[float, float]:
    purchase = Decimal(str(valor_compra))
    discount = Decimal(str(cupom)) / Decimal("100")
    final_value = purchase * (Decimal("1") - discount)
    percentage = Decimal("0.10") if final_value >= Decimal("500") else Decimal("0.05")
    cashback = final_value * percentage

    if tipo_cliente == "vip":
        cashback *= Decimal("1.10")

    money = Decimal("0.01")
    return (
        float(final_value.quantize(money, rounding=ROUND_HALF_UP)),
        float(cashback.quantize(money, rounding=ROUND_HALF_UP)),
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip()
    return request.client.host if request.client else "unknown"


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception as error:
        logger.exception("Falha no health check do banco de dados.")
        raise HTTPException(status_code=503, detail="Banco de dados indisponível") from error

    return {"status": "ok", "database": "connected"}


@app.post("/calcular-cashback", response_model=CashbackResponse)
def calcular_cashback(
    dados: DadosEntrada,
    request: Request,
    db: Session = Depends(get_db),
):
    valor_final, cashback = calcular_valores(
        dados.tipo_cliente,
        dados.valor_compra,
        dados.cupom,
    )

    consulta = ConsultaSQL(
        ip=get_client_ip(request),
        tipo_cliente=dados.tipo_cliente,
        valor_compra=dados.valor_compra,
        valor_cashback=cashback,
    )
    db.add(consulta)

    try:
        db.commit()
    except Exception as error:
        db.rollback()
        logger.exception("Falha ao salvar o cálculo de cashback.")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível salvar o cálculo.",
        ) from error

    return CashbackResponse(valor_final=valor_final, cashback=cashback)


@app.get("/historico", response_model=HistoricoResponse)
def historico(request: Request, db: Session = Depends(get_db)):
    consultas = (
        db.query(ConsultaSQL)
        .filter(ConsultaSQL.ip == get_client_ip(request))
        .order_by(ConsultaSQL.id.desc())
        .limit(10)
        .all()
    )

    return HistoricoResponse(
        historico=[
            HistoricoItem(
                tipo_cliente=item.tipo_cliente,
                valor_compra=item.valor_compra,
                valor_cashback=item.valor_cashback,
            )
            for item in consultas
        ]
    )
