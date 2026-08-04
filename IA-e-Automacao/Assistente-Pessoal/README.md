<p align="center">
  <img src="./assets/assistant-header.svg" width="100%" alt="Assistente Pessoal com IA — voz, automação e Groq">
</p>

<p align="center">
  <strong>Assistente pessoal em Python com comandos de voz, síntese de fala, automações e respostas geradas por IA.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Groq-7C3AED?style=for-the-badge" alt="Groq">
  <img src="https://img.shields.io/badge/SpeechRecognition-0891B2?style=for-the-badge" alt="SpeechRecognition">
  <img src="https://img.shields.io/badge/YouTube%20API-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube API">
  <img src="https://img.shields.io/badge/Status-Protótipo%20funcional-F59E0B?style=for-the-badge" alt="Status">
</p>

<p align="center">
  <a href="../../README.md">← Voltar ao catálogo de projetos</a>
</p>

## Visão geral

O **Assistente Pessoal** foi desenvolvido para receber comandos por voz, responder com áudio, abrir sites e programas, consultar inteligência artificial e manter um histórico local das conversas.

A estrutura modular separa reconhecimento de voz, síntese de fala, comandos, integração com IA e persistência, facilitando a criação de novas automações sem concentrar toda a lógica no arquivo principal.

## Principais funcionalidades

| Recurso | Descrição |
|---|---|
| Reconhecimento de voz | Captura comandos falados pelo microfone |
| Síntese de fala | Converte respostas em áudio |
| Comandos locais | Abre sites, programas e executa ações comuns |
| Integração com IA | Gera respostas por meio da API da Groq |
| Busca de vídeos | Consulta a YouTube Data API quando configurada |
| Histórico | Mantém as conversas em JSON no ambiente local |
| Tratamento de falhas | Evita que erros pontuais de microfone ou API encerrem o programa |
| Segurança | Carrega chaves por variáveis de ambiente |

## Arquitetura do projeto

```text
Microfone
   │
   ▼
Reconhecimento de voz
   │
   ├── comando local ──► sistema operacional / navegador
   │
   └── pergunta ───────► Groq API
                           │
                           ▼
                    resposta textual
                           │
                           ├── histórico JSON
                           └── síntese de fala
```

## Estrutura de pastas

```text
Assistente-Pessoal/
├── Config/
│   └── configurações e variáveis do projeto
├── Core/
│   └── voz, comandos, IA e histórico
├── data/
│   └── dados locais gerados durante o uso
├── assets/
│   └── assistant-header.svg
├── main.py
├── .env.example
├── requirements.txt
└── README.md
```

## Como executar localmente

### 1. Clonar o catálogo

```bash
git clone https://github.com/Ruanrabello/Projects.git
cd Projects/IA-e-Automacao/Assistente-Pessoal
```

### 2. Criar o ambiente

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

Configure as chaves necessárias no `.env`:

```env
GROQ_API_KEY=sua_chave_groq
YOUTUBE_API_KEY=sua_chave_youtube_opcional
```

### 3. Iniciar o assistente

```bash
python main.py
```

## Requisitos de uso

- Microfone funcional.
- Saída de áudio configurada.
- Chave válida da Groq.
- Windows para os comandos locais atualmente implementados.

## Segurança e privacidade

- O arquivo `.env` não deve ser versionado.
- O histórico pessoal fica fora do Git.
- As respostas e comandos locais devem ser revisados antes de ampliar permissões do sistema.
- Chaves antigas que tenham aparecido em commits precisam ser substituídas no provedor correspondente.

## Limitações atuais

- Alguns comandos dependem de caminhos e programas instalados no Windows.
- O histórico ainda não possui sincronização com banco ou nuvem.
- O reconhecimento de voz depende da qualidade do microfone e do ambiente.
- O projeto ainda não possui testes automatizados.

## Roadmap

- [x] Implementar comandos de voz.
- [x] Integrar respostas com IA.
- [x] Adicionar síntese de fala e histórico local.
- [x] Tratar falhas de microfone e API.
- [ ] Criar testes automatizados.
- [ ] Tornar comandos independentes do sistema operacional.
- [ ] Adicionar interface visual.
- [ ] Organizar comandos como plugins.
- [ ] Adicionar armazenamento opcional em banco de dados.

## Licença

Distribuído sob a [licença MIT](../../LICENSE).

## Autor

**Ruan Rabello** — estudante de Engenharia da Computação com foco em Back-end, Dados, IA e Automação.

[LinkedIn](https://www.linkedin.com/in/ruan-rabello-da-silva-9032b5274/) · [Portfólio](https://ruanportifolio.lovable.app) · [GitHub](https://github.com/Ruanrabello)
