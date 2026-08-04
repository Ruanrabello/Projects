<p align="center">
  <img src="./assets/projects-header.svg" width="100%" alt="Projects — catálogo de aplicações, IA, dados e games">
</p>

<p align="center">
  <strong>Catálogo de projetos completos, protótipos funcionais e estudos aplicados.</strong>
</p>

<p align="center">
  <a href="https://github.com/Ruanrabello/Projects/actions/workflows/quality.yml"><img src="https://github.com/Ruanrabello/Projects/actions/workflows/quality.yml/badge.svg" alt="Repository Quality"></a>
  <img src="https://img.shields.io/badge/Licença-MIT-16A34A?style=flat-square" alt="Licença MIT">
  <img src="https://img.shields.io/badge/Documentação-Padronizada-2563EB?style=flat-square" alt="Documentação padronizada">
</p>

<p align="center">
  <a href="./Aplicacoes-Web"><img src="https://img.shields.io/badge/Aplicações%20Web-2563EB?style=for-the-badge" alt="Aplicações Web"></a>
  <a href="./IA-e-Automacao"><img src="https://img.shields.io/badge/IA%20e%20Automação-7C3AED?style=for-the-badge" alt="IA e Automação"></a>
  <a href="./Machine-Learning"><img src="https://img.shields.io/badge/Machine%20Learning-16A34A?style=for-the-badge" alt="Machine Learning"></a>
  <a href="./Games"><img src="https://img.shields.io/badge/Games-DC2626?style=for-the-badge" alt="Games"></a>
</p>

## Sobre o repositório

O **Projects** reúne projetos menores e médios em um catálogo organizado pelo tipo de solução. Uma aplicação permanece inteira na mesma pasta, com interface, API, regras de negócio, persistência e integrações documentadas em conjunto.

Projetos maiores e independentes permanecem em repositórios próprios.

## Projetos principais

| Projeto | Entrega | Tecnologias | Status |
|---|---|---|---|
| [Enterprise AI Assistant](https://github.com/Ruanrabello/enterprise-ai-assistant) | Plataforma full stack de IA corporativa com histórico, configuração de provedores e evolução para RAG | FastAPI, React, PostgreSQL, Ollama, Gemini e Grok | Projeto principal em evolução |
| [Excel VBA Projects](https://github.com/Ruanrabello/Excel-vba-projects) | Automações para relatórios, tratamento de dados, PDFs e integração com Outlook | Excel e VBA | Repositório dedicado |

## Navegação por categorias

| Categoria | Foco | Projetos | Acesso |
|---|---|---|---|
| 🌐 Aplicações Web | Produtos full stack, APIs e integrações | Previsão do Tempo, Calculadora de Cashback | [Abrir](./Aplicacoes-Web) |
| 🤖 IA e Automação | Voz, comandos, APIs e tarefas automatizadas | Assistente Pessoal | [Abrir](./IA-e-Automacao) |
| 📊 Machine Learning | Classificação, redes neurais e IA local | Machine Learning & IA | [Abrir](./Machine-Learning) |
| 🎮 Games | Sistemas interativos e arquitetura de jogos | Neon Depths — Game Ball | [Abrir](./Games) |

## Catálogo interno

| Projeto | Descrição | Tecnologias | Status |
|---|---|---|---|
| [Previsão do Tempo](./Aplicacoes-Web/Previsao-Tempo) | Consulta meteorológica com interface responsiva, API própria e integração externa | FastAPI, HTML, CSS, JavaScript e OpenWeatherMap | Funcional e revisado |
| [Calculadora de Cashback](./Aplicacoes-Web/Calculadora-Cashback) | Regras de cashback, cupons, persistência, histórico e configuração por ambiente | FastAPI, SQLAlchemy, PostgreSQL, HTML, CSS e JavaScript | Funcional e revisado |
| [Assistente Pessoal](./IA-e-Automacao/Assistente-Pessoal) | Voz, comandos locais, consulta à IA, busca de vídeos e histórico persistente | Python, Groq, SpeechRecognition e YouTube Data API | Protótipo funcional e revisado |
| [Machine Learning & IA](./Machine-Learning/Machine-Learning-IA) | Classificação, redes neurais, comparação de modelos e agentes locais | Python, Scikit-learn, TensorFlow, LangChain e Ollama | Estudos reproduzíveis |
| [Neon Depths — Game Ball](./Games/Game-Ball) | Roguelike com geração procedural, combate, progressão, áudio e salvamento | Python e Pygame | Funcional e revisado |

## Estrutura

```text
Projects/
├── .github/workflows/
│   └── quality.yml
├── Aplicacoes-Web/
│   ├── Previsao-Tempo/
│   └── Calculadora-Cashback/
├── IA-e-Automacao/
│   └── Assistente-Pessoal/
├── Machine-Learning/
│   └── Machine-Learning-IA/
├── Games/
│   └── Game-Ball/
├── assets/
├── .gitignore
├── README.md
└── LICENSE
```

## Padrão de documentação

Cada projeto relevante possui banner próprio, tecnologias utilizadas, visão geral, funcionalidades, arquitetura, estrutura de pastas, execução local, roadmap, licença e autor. Os READMEs das categorias também funcionam como páginas de navegação técnica, e não apenas como índices de diretório.

As pastas `assets` permanecem versionadas porque armazenam os recursos usados pelos READMEs. Removê-las quebraria banners e imagens.

## Qualidade aplicada

- Configurações sensíveis por variáveis de ambiente.
- Dados pessoais, históricos e saves locais fora do Git.
- Tratamento de falhas de rede, banco, áudio, microfone e serviços externos.
- Código organizado por responsabilidade e com pontos de entrada explícitos.
- Exemplos de Machine Learning com seeds, funções e execução reproduzível.
- GitHub Actions para validar sintaxe Python, links internos e padrões comuns de credenciais.

## Próximas melhorias

- [ ] Adicionar testes unitários para as regras de cashback.
- [ ] Adicionar testes para colisões e geração procedural do Neon Depths.
- [ ] Adicionar screenshot atual do Previsão do Tempo.
- [ ] Adicionar screenshot ou GIF real do Neon Depths.
- [ ] Criar nova captura da interface redesenhada da Calculadora de Cashback.

## Autor

**Ruan Rabello** — estudante de Engenharia da Computação com foco em Back-end, Dados, IA e Automação.

[LinkedIn](https://www.linkedin.com/in/ruan-rabello-da-silva-9032b5274/) · [Portfólio](https://ruanportifolio.lovable.app) · [GitHub](https://github.com/Ruanrabello)

## Licença

Distribuído sob a [licença MIT](./LICENSE).
