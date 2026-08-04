<p align="center">
  <img src="./assets/cashback-header.svg" width="100%" alt="Calculadora de Cashback — FastAPI, PostgreSQL e JavaScript">
</p>

<p align="center">
  <strong>Aplicação full stack para calcular cashback, aplicar cupons e consultar o histórico de operações.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=111" alt="JavaScript">
</p>

<p align="center">
  <a href="../../README.md">← Voltar ao catálogo de projetos</a>
</p>

## Visão geral

A **Calculadora de Cashback** combina uma API em FastAPI, persistência com SQLAlchemy e uma interface web responsiva. O usuário informa o tipo de cliente, o valor da compra e o percentual de desconto; a aplicação calcula o cashback e registra a operação no banco de dados.

O projeto demonstra regras de negócio, validação de dados, integração entre front-end e back-end, persistência em PostgreSQL e tratamento de falhas de banco.

## Demonstração

- [Abrir aplicação web](https://calculadora-cashback-w34p.vercel.app)
- [Abrir documentação Swagger da API](https://calculadora-cashback-csom.onrender.com/docs)

## Principais funcionalidades

| Recurso | Descrição |
|---|---|
| Cálculo de cashback | Calcula o benefício sobre o valor final da compra |
| Clientes Normal e VIP | Aplica regras diferentes conforme o perfil selecionado |
| Cupons | Desconta o percentual informado antes de calcular o cashback |
| Histórico | Retorna as dez consultas mais recentes associadas ao IP |
| Persistência | Salva os cálculos por meio de SQLAlchemy |
| Validação | Rejeita valores, cupons e tipos de cliente inválidos |
| Health check | Expõe um endpoint simples para verificar a disponibilidade da API |

## Regras de negócio

- Cashback base de **5%**.
- Compras com valor final a partir de **R$ 500** recebem **10%**.
- Clientes VIP recebem **10% de bônus sobre o cashback calculado**.
- O cupom é aplicado antes do cálculo do benefício.

## Arquitetura

```text
Navegador
   │ POST /calcular-cashback
   │ GET  /historico
   ▼
HTML + JavaScript
   ▼
FastAPI + Pydantic
   ▼
SQLAlchemy
   ▼
PostgreSQL
```

## Estrutura de pastas

```text
Calculadora-Cashback/
├── assets/
│   └── cashback-header.svg
├── main.py
├── index.html
├── requirements.txt
├── .env.example
└── README.md
```

## Como executar localmente

### 1. Clonar o catálogo

```bash
git clone https://github.com/Ruanrabello/Projects.git
cd Projects/Aplicacoes-Web/Calculadora-Cashback
```

### 2. Preparar o ambiente Python

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

No Linux ou macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configure a conexão no arquivo `.env`:

```env
DATABASE_URL=postgresql://usuario:senha@host:5432/banco
```

### 3. Iniciar a API

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

A documentação estará em `http://127.0.0.1:8000/docs`.

### 4. Iniciar a interface

```bash
python -m http.server 3000
```

Acesse `http://localhost:3000`. Para usar a API local, altere temporariamente `API_URL` no `index.html` para `http://127.0.0.1:8000`.

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/health` | Verifica se a API está disponível |
| POST | `/calcular-cashback` | Calcula e salva o cashback |
| GET | `/historico` | Retorna as últimas consultas do cliente |

## Roadmap

- [x] Implementar cálculo para clientes Normal e VIP.
- [x] Adicionar cupons e histórico.
- [x] Proteger a conexão do banco com variável de ambiente.
- [x] Adicionar validações e tratamento de falhas.
- [ ] Separar HTML, CSS e JavaScript em arquivos próprios.
- [ ] Permitir configuração automática da URL da API.
- [ ] Adicionar testes unitários para as regras de negócio.
- [ ] Adicionar screenshot ou GIF da aplicação.

## Licença

Distribuído sob a [licença MIT](../../LICENSE).

## Autor

**Ruan Rabello** — estudante de Engenharia da Computação com foco em Back-end, Dados, IA e Automação.

[LinkedIn](https://www.linkedin.com/in/ruan-rabello-da-silva-9032b5274/) · [Portfólio](https://ruanportifolio.lovable.app) · [GitHub](https://github.com/Ruanrabello)
