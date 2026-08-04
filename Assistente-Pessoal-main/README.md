<p align="center">
  <img src="./assets/assistant-header.svg" width="100%" alt="Assistente Pessoal com IA — voz, automação e Groq">
</p>

<p align="center">
  <strong>Assistente pessoal em Python com comandos de voz, síntese de fala, automações e respostas geradas por IA.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Groq-8B5CF6?style=flat-square" alt="Groq">
  <img src="https://img.shields.io/badge/Voice-Automation-0891B2?style=flat-square" alt="Voice Automation">
  <img src="https://img.shields.io/badge/Status-Protótipo%20funcional-F59E0B?style=flat-square" alt="Status">
</p>

## Sobre o projeto

O **Assistente Pessoal** foi desenvolvido para executar comandos por voz, abrir sites e programas, responder perguntas com inteligência artificial e manter um histórico local das conversas.

O projeto combina reconhecimento de voz, síntese de fala, integração com a API da Groq e automações locais em uma estrutura modular, facilitando a evolução de novos comandos.

## Funcionalidades

| Recurso | Descrição |
|---|---|
| Reconhecimento de voz | Captura comandos falados pelo microfone |
| Síntese de voz | Responde ao usuário com áudio |
| Comandos locais | Abre sites, programas e executa ações comuns |
| Integração com IA | Utiliza a Groq para respostas mais naturais |
| Busca de vídeos | Pode consultar a YouTube Data API |
| Histórico | Armazena conversas localmente em JSON |

## Tecnologias

- Python 3.10+
- Groq API
- YouTube Data API
- Reconhecimento e síntese de voz
- Variáveis de ambiente com `python-dotenv`
- Persistência local em JSON

## Estrutura

```text
Assistente-Pessoal-main/
├── main.py                # Ponto de entrada
├── Core/                  # Voz, comandos, IA e histórico
├── Config/                # Configurações do projeto
├── data/                  # Histórico e dados locais
├── assets/                # Identidade visual da documentação
├── .env.example           # Modelo seguro de variáveis
├── requirements.txt       # Dependências Python
└── README.md
```

## Instalação

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

Copie o arquivo de exemplo:

```powershell
copy .env.example .env
```

Preencha apenas no arquivo local as chaves necessárias, como a chave da Groq e, opcionalmente, a chave da YouTube Data API.

## Execução

```bash
python main.py
```

## Requisitos de uso

- Microfone funcional.
- Saída de áudio configurada.
- Windows para os comandos locais atualmente implementados.
- Chave válida da Groq.

## Limitações atuais

- Alguns comandos dependem de caminhos e programas instalados no Windows.
- O histórico é local e ainda não possui sincronização.
- O reconhecimento de voz pode variar conforme ruído e qualidade do microfone.
- O projeto ainda não possui testes automatizados.

## Roadmap

- [x] Comandos de voz
- [x] Respostas com IA
- [x] Síntese de fala
- [x] Histórico local
- [ ] Padronizar tratamento de erros
- [ ] Criar testes automatizados
- [ ] Tornar os comandos independentes do sistema operacional
- [ ] Adicionar interface visual
- [ ] Organizar comandos por plugins

## Segurança

- Nunca publique o arquivo `.env`.
- Mantenha chaves de API apenas em variáveis de ambiente.
- Revise comandos que abrem programas ou executam ações locais antes de utilizá-los.

## Autor

**Ruan Rabello**

[LinkedIn](https://www.linkedin.com/in/ruan-rabello-da-silva-9032b5274/) · [Portfólio](https://ruanportifolio.lovable.app) · [GitHub](https://github.com/Ruanrabello)
