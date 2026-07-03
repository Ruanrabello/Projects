# Assistente Pessoal

Assistente pessoal com reconhecimento de voz, síntese de voz e integração com IA via Groq.

## Funcionalidades

- Escuta comandos por voz
- Responde com voz sintetizada
- Abre sites e programas comuns
- Consulta a IA para respostas mais naturais
- Mantém histórico de conversas

## Requisitos

- Python 3.10+
- Microfone e áudio compatível com Windows
- Chave de API da Groq
- Opcionalmente, chave da YouTube Data API para buscas de vídeo

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd Assistente-Pessoal
   ```
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Preencha as chaves de API

## Execução

```bash
python main.py
```

## Estrutura do projeto

- `main.py`: ponto de entrada do assistente
- `Core/`: módulos de voz, comandos, IA e histórico
- `Config/`: configuração e chaves
- `data/`: arquivos de dados do projeto

## Observações

- O histórico de conversas é salvo localmente em `data/Historico.json`
- Evite compartilhar chaves de API ou arquivos `.env` publicamente

