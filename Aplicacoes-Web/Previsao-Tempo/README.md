<p align="center">
  <img src="./assets/weather-header.svg" width="100%" alt="Previsão do Tempo — FastAPI, JavaScript e OpenWeather">
</p>

<p align="center">
  <strong>Aplicação full stack para consultar condições meteorológicas em tempo real.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=111" alt="JavaScript">
  <img src="https://img.shields.io/badge/OpenWeather-2563EB?style=for-the-badge" alt="OpenWeather">
  <img src="https://img.shields.io/badge/Status-Funcional-16A34A?style=for-the-badge" alt="Status funcional">
</p>

<p align="center">
  <a href="../../README.md">← Voltar ao catálogo de projetos</a>
</p>

## Visão geral

O **Previsão do Tempo** combina uma API em FastAPI com uma interface web responsiva. O usuário informa uma cidade e recebe temperatura, sensação térmica, umidade, vento, pressão atmosférica e uma descrição das condições atuais.

O projeto demonstra consumo seguro de API externa, validação de entrada, tratamento de erros, timeout, CORS e integração entre front-end e back-end.

## Principais funcionalidades

| Recurso | Descrição |
|---|---|
| Consulta por cidade | Busca as condições meteorológicas atuais |
| Cards navegáveis | Organiza os dados em uma interface interativa |
| Imagens temáticas | Adapta o visual ao tipo de informação exibida |
| Validação | Verifica o nome da cidade antes da consulta |
| Timeout | Cancela requisições demoradas no navegador e na API |
| Tratamento de erros | Diferencia cidade inexistente, chave inválida e falha externa |
| Health check | Informa se a API está disponível e configurada |
| Reset de interface | Limpa a busca e devolve o foco ao campo de cidade |

## Arquitetura do projeto

```text
Navegador
   │ GET /weather/{city}
   ▼
HTML + CSS + JavaScript
   ▼
FastAPI
   │ HTTPS
   ▼
OpenWeatherMap
```

## Estrutura de pastas

```text
Previsao-Tempo/
├── Backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── Frontend/
│   ├── img/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── package.json
├── assets/
│   └── weather-header.svg
├── .gitignore
└── README.md
```

## Como executar localmente

### 1. Clonar o catálogo

```bash
git clone https://github.com/Ruanrabello/Projects.git
cd Projects/Aplicacoes-Web/Previsao-Tempo
```

### 2. Preparar o back-end

```bash
cd Backend
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

Configure a chave no arquivo `.env`:

```env
API_KEY=sua_chave_openweather
```

Inicie a API:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

A documentação estará em `http://127.0.0.1:8000/docs`.

### 3. Iniciar o front-end

Em outro terminal:

```bash
cd Frontend
python -m http.server 3000
```

Acesse `http://localhost:3000`.

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/weather/{city}` | Retorna as condições atuais da cidade |
| GET | `/health` | Verifica a API e informa se a chave está configurada |

## Segurança e confiabilidade

- A chave da OpenWeather permanece fora do código.
- A API não realiza consultas externas sem configuração válida.
- O CORS é limitado aos servidores locais usados pelo projeto.
- Requisições externas e consultas do navegador possuem timeout.
- Respostas inválidas e falhas do serviço externo são tratadas.

## Limitações atuais

- Exibe somente as condições atuais.
- O endereço da API usa `localhost` por padrão.
- Ainda não possui testes automatizados.
- Não possui screenshot real versionado no momento.

## Roadmap

- [x] Corrigir tratamento de cidades inexistentes.
- [x] Validar ausência ou rejeição da API key.
- [x] Implementar timeout real no front-end.
- [x] Corrigir navegação, reset e botão “Ver Tudo”.
- [x] Organizar o projeto em `Backend` e `Frontend`.
- [ ] Adicionar screenshot ou GIF da interface.
- [ ] Adicionar previsão de cinco dias.
- [ ] Adicionar geolocalização.
- [ ] Criar testes automatizados.
- [ ] Preparar configuração para deploy.

## Licença

Distribuído sob a [licença MIT](../../LICENSE).

## Autor

**Ruan Rabello** — estudante de Engenharia da Computação com foco em Back-end, Dados, IA e Automação.

[LinkedIn](https://www.linkedin.com/in/ruan-rabello-da-silva-9032b5274/) · [Portfólio](https://ruanportifolio.lovable.app) · [GitHub](https://github.com/Ruanrabello)
