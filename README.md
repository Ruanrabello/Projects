<p align="center">
  <img src="./assets/projects-header.svg" width="100%" alt="Projects — catálogo de aplicações, IA, dados e games">
</p>

<p align="center">
  <strong>Catálogo de projetos completos, protótipos funcionais e estudos aplicados.</strong>
</p>

<p align="center">
  <a href="./Aplicacoes-Web"><img src="https://img.shields.io/badge/Aplicações%20Web-2563EB?style=for-the-badge" alt="Aplicações Web"></a>
  <a href="./IA-e-Automacao"><img src="https://img.shields.io/badge/IA%20e%20Automação-7C3AED?style=for-the-badge" alt="IA e Automação"></a>
  <a href="./Dados-e-Machine-Learning"><img src="https://img.shields.io/badge/Dados%20e%20ML-16A34A?style=for-the-badge" alt="Dados e Machine Learning"></a>
  <a href="./Games"><img src="https://img.shields.io/badge/Games-DC2626?style=for-the-badge" alt="Games"></a>
</p>

## Sobre o repositório

O **Projects** reúne projetos menores e médios em um único catálogo profissional. A organização é feita pelo **tipo de solução**, e não por camadas como front-end e back-end, porque uma mesma aplicação pode conter interface, API, banco de dados e integrações.

Projetos grandes e independentes permanecem em repositórios próprios.

## Projetos principais

| Projeto | Descrição | Tecnologias | Status |
|---|---|---|---|
| [Enterprise AI Assistant](https://github.com/Ruanrabello/enterprise-ai-assistant) | Plataforma full stack de IA corporativa com histórico, configuração de modelos e base para RAG | FastAPI, React, PostgreSQL, Ollama, Gemini e Grok | Projeto principal |
| [Excel VBA Projects](https://github.com/Ruanrabello/Excel-vba-projects) | Automações para relatórios, tratamento de dados, PDFs e integração com Outlook | Excel e VBA | Repositório dedicado |

## Navegação por categorias

| Categoria | Identidade | Projetos | Acesso |
|---|---|---|---|
| 🌐 Aplicações Web | Azul e ciano | Previsão do Tempo, Calculadora de Cashback | [Abrir](./Aplicacoes-Web) |
| 🤖 IA e Automação | Roxo e laranja | Assistente Pessoal | [Abrir](./IA-e-Automacao) |
| 📊 Dados e Machine Learning | Verde e roxo | Machine Learning & IA | [Abrir](./Dados-e-Machine-Learning) |
| 🎮 Games | Vermelho e rosa neon | Neon Depths — Game Ball | [Abrir](./Games) |

## Catálogo interno

### 🌐 Aplicações Web

| Projeto | Descrição | Tecnologias | Status |
|---|---|---|---|
| [Previsão do Tempo](./Aplicacoes-Web/Previsao-Tempo) | Aplicação full stack para consultar dados meteorológicos, com interface responsiva, API própria e integração externa | FastAPI, HTML, CSS, JavaScript e OpenWeatherMap | Funcional e revisado |
| [Calculadora de Cashback](./Aplicacoes-Web/Calculadora-Cashback) | Aplicação full stack para cálculo de cashback, cupons e histórico de consultas | FastAPI, SQLAlchemy, PostgreSQL, HTML e JavaScript | Funcional e revisado |

### 🤖 IA e Automação

| Projeto | Descrição | Tecnologias | Status |
|---|---|---|---|
| [Assistente Pessoal](./IA-e-Automacao/Assistente-Pessoal) | Assistente por voz que executa comandos locais, consulta IA, pesquisa vídeos e mantém histórico | Python, Groq, SpeechRecognition e YouTube Data API | Protótipo funcional e revisado |

### 📊 Dados e Machine Learning

| Projeto | Descrição | Tecnologias | Status |
|---|---|---|---|
| [Machine Learning & IA](./Dados-e-Machine-Learning/Machine-Learning-IA) | Laboratório com agentes locais, classificação, redes neurais e comparação entre modelos | Python, Pandas, NumPy, Scikit-learn, TensorFlow, LangChain e Ollama | Estudos aplicados |

### 🎮 Games

| Projeto | Descrição | Tecnologias | Status |
|---|---|---|---|
| [Neon Depths — Game Ball](./Games/Game-Ball) | Roguelike cyberpunk com geração procedural, inimigos, chefes, power-ups, conquistas e salvamento | Python e Pygame | Funcional |

## Estrutura atual

```text
Projects/
├── Aplicacoes-Web/
│   ├── Previsao-Tempo/
│   └── Calculadora-Cashback/
├── IA-e-Automacao/
│   └── Assistente-Pessoal/
├── Dados-e-Machine-Learning/
│   └── Machine-Learning-IA/
├── Games/
│   └── Game-Ball/
├── assets/
├── README.md
└── LICENSE
```

## Padrão de nomes

- Sem sufixos como `-main`, `Basic` ou `copy`.
- Palavras separadas por hífen.
- Nomes curtos, descritivos e consistentes.
- Cada pasta representa uma solução completa, não apenas uma camada técnica.

## Boas práticas aplicadas

- Dependências, ambientes virtuais, caches, builds e bancos locais não são versionados.
- Chaves e credenciais são fornecidas por variáveis de ambiente.
- Dados pessoais e históricos locais ficam fora do Git.
- Cada projeto relevante possui descrição, tecnologias, status e instruções próprias.
- Projetos grandes recebem um repositório dedicado.

## Progresso da organização

- [x] Remover arquivos gerados e dependências versionadas
- [x] Separar o Enterprise AI Assistant
- [x] Criar identidade visual e descrições
- [x] Substituir categorias de camada por categorias de soluções completas
- [x] Migrar e renomear fisicamente todas as pastas
- [x] Revisar Assistente Pessoal
- [x] Revisar Previsão do Tempo
- [x] Revisar Calculadora de Cashback
- [x] Revisar Machine Learning & IA
- [x] Revisar Game Ball
- [ ] Adicionar screenshots ou GIFs aos projetos com interface

## Autor

**Ruan Rabello** — estudante de Engenharia da Computação com foco em Back-end, Dados, IA e Automação.

[LinkedIn](https://www.linkedin.com/in/ruan-rabello-da-silva-9032b5274/) · [Portfólio](https://ruanportifolio.lovable.app) · [GitHub](https://github.com/Ruanrabello)

## Licença

Distribuído sob a [licença MIT](./LICENSE).
