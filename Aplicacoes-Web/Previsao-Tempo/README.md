<p align="center">
  <img src="./assets/weather-header.svg" width="100%" alt="Previsão do Tempo — FastAPI, JavaScript e OpenWeather">
</p>

<p align="center">
  <strong>Aplicação full stack para consultar condições meteorológicas em tempo real.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=111" alt="JavaScript">
  <img src="https://img.shields.io/badge/OpenWeather-2563EB?style=for-the-badge" alt="OpenWeather">
  <img src="https://img.shields.io/badge/Status-Funcional-16A34A?style=for-the-badge" alt="Status funcional">
</p>

## Sobre

O **Previsão do Tempo** combina uma API em FastAPI com uma interface web responsiva. O usuário informa uma cidade e recebe temperatura, sensação térmica, umidade, vento, pressão e descrição das condições atuais.

O projeto demonstra consumo seguro de API externa, validação de entrada, tratamento de erros, timeout, CORS e integração entre front-end e back-end.

## Funcionalidades

- Busca de condições meteorológicas por cidade.
- Validação de nomes antes do envio.
- Exibição em cards navegáveis.
- Imagens de fundo adaptadas ao tipo de informação.
- Loader e mensagens de erro em português.
- Timeout no navegador para evitar requisições travadas.
- Endpoint de saúde e indicação de configuração da API.
- Tratamento específico para cidade inexistente, chave inválida e falha externa.

## Arquitetura

```text
Navegador
   │
   ▼
HTML + CSS + JavaScript
   │ GET /weather/{city}
   ▼
FastAPI
   │ HTTPS
   ▼
OpenWeatherMap
```

## Estrutura

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

## Como executar

### 1. Back-end

```bash
cd Backend
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Preencha a chave da OpenWeather no arquivo `.env`:

```env
API_KEY=sua_chave_openweather
```

Inicie o Uvicorn:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Documentação interativa:

```text
http://127.0.0.1:8000/docs
```

### 2. Front-end

```bash
cd Frontend
python -m http.server 3000
```

Acesse:

```text
http://localhost:3000
```

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/weather/{city}` | Retorna as condições atuais da cidade |
| GET | `/health` | Verifica a API e informa se a chave está configurada |

## Segurança e confiabilidade

- A chave da OpenWeather fica fora do código, em variável de ambiente.
- A API não inicia consultas externas sem configuração válida.
- CORS está limitado aos servidores locais usados no projeto.
- Requisições externas têm timeout.
- O front-end cancela consultas demoradas.
- Respostas não JSON e erros do serviço externo são tratados.

## Limitações atuais

- Exibe somente as condições atuais.
- O endereço da API usa `localhost` por padrão.
- Ainda não há testes automatizados.

## Roadmap

- [x] Corrigir tratamento de cidades inexistentes.
- [x] Validar ausência ou rejeição da API key.
- [x] Implementar timeout real no front-end.
- [x] Corrigir o botão “Ver Tudo”.
- [x] Renomear `Frontend copy` para `Frontend`.
- [x] Mover para `Aplicacoes-Web/Previsao-Tempo`.
- [ ] Adicionar previsão de cinco dias.
- [ ] Adicionar geolocalização.
- [ ] Criar testes automatizados.
- [ ] Preparar configuração para deploy.

## Autor

**Ruan Rabello** — estudante de Engenharia da Computação com foco em Back-end, Dados, IA e Automação.

[LinkedIn](https://www.linkedin.com/in/ruan-rabello-da-silva-9032b5274/) · [Portfólio](https://ruanportifolio.lovable.app) · [GitHub](https://github.com/Ruanrabello)

## Licença

Projeto educacional distribuído como parte do repositório `Projects`.
