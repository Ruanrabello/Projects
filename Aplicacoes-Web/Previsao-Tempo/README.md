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

O **Previsão do Tempo** combina uma API em FastAPI com uma interface responsiva. A consulta retorna cidade, país, temperatura, sensação térmica, umidade, vento, pressão e descrição das condições atuais.

A interface foi revisada para corrigir estilos inválidos, melhorar contraste e acessibilidade, manter o botão de reset dentro do painel e substituir o antigo alerta de “Ver Tudo” por um resumo em `dialog`.

## Principais funcionalidades

| Recurso | Descrição |
|---|---|
| Consulta por cidade | Busca as condições meteorológicas atuais |
| Cards navegáveis | Permite avançar, voltar ou selecionar cada detalhe |
| Imagens temáticas | Usa fundos existentes conforme temperatura e condição |
| Resumo completo | Exibe todos os dados em uma janela de diálogo |
| Validação | Aplica as mesmas regras no navegador e na API |
| Timeout | Cancela requisições demoradas no front-end e back-end |
| Tratamento de erros | Diferencia cidade inexistente, chave inválida e falha externa |
| Acessibilidade | Labels, estados de carregamento e navegação por teclado |

## Arquitetura

```text
Navegador
   │ GET /weather/{city}
   ▼
HTML + CSS + JavaScript
   ▼
FastAPI
   │ HTTPS + timeout
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

## Como executar localmente

```bash
git clone https://github.com/Ruanrabello/Projects.git
cd Projects/Aplicacoes-Web/Previsao-Tempo/Backend
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

Configure:

```env
API_KEY=sua_chave_openweather
```

Inicie a API:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Em outro terminal:

```bash
cd ../Frontend
python -m http.server 3000
```

Acesse `http://localhost:3000`.

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/weather/{city}` | Retorna as condições atuais da cidade |
| GET | `/health` | Informa se a API e a chave externa estão configuradas |

## Segurança e confiabilidade

- A chave da OpenWeather fica fora do código.
- A API não consulta o serviço externo sem configuração válida.
- O CORS é limitado aos ambientes locais documentados.
- Respostas não JSON, dados numéricos inválidos e falhas externas são tratados.
- O front-end só usa imagens que existem dentro do projeto.

## Limitações atuais

- Exibe apenas as condições atuais.
- A URL padrão do back-end é local.
- Ainda não possui testes automatizados nem deploy documentado.
- Uma captura real da interface redesenhada ainda precisa ser adicionada.

## Roadmap

- [x] Corrigir tratamento de cidades inexistentes e chave inválida.
- [x] Implementar timeout e validação nas duas camadas.
- [x] Redesenhar a interface e corrigir CSS inválido.
- [x] Substituir o alerta por um resumo acessível.
- [ ] Adicionar screenshot ou GIF da interface atual.
- [ ] Adicionar previsão de cinco dias e geolocalização.
- [ ] Criar testes automatizados.
- [ ] Preparar configuração para deploy.

## Licença

Distribuído sob a [licença MIT](../../LICENSE).

## Autor

**Ruan Rabello** — estudante de Engenharia da Computação com foco em Back-end, Dados, IA e Automação.

[LinkedIn](https://www.linkedin.com/in/ruan-rabello-da-silva-9032b5274/) · [Portfólio](https://ruanportifolio.lovable.app) · [GitHub](https://github.com/Ruanrabello)
