<p align="center">
  <img src="./assets/machine-learning-header.svg" width="100%" alt="Machine Learning e Inteligência Artificial — Scikit-learn, TensorFlow e Ollama">
</p>

<p align="center">
  <strong>Laboratório de classificação, processamento de texto, redes neurais e agentes locais com IA.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge" alt="LangChain">
  <img src="https://img.shields.io/badge/Ollama-111111?style=for-the-badge" alt="Ollama">
</p>

<p align="center">
  <a href="../../README.md">← Voltar ao catálogo de projetos</a>
</p>

## Visão geral

O **Machine Learning & IA** reúne experimentos independentes com modelos clássicos, redes neurais e agentes locais. Os scripts usam funções, pontos de entrada explícitos e seeds para tornar a execução mais previsível e evitar treinamento acidental durante uma importação.

## Projetos incluídos

| Área | Arquivo | Objetivo |
|---|---|---|
| Agente básico | `Agentes/App_v1.py` | Fazer uma chamada simples ao Ollama |
| Agente com histórico | `Agentes/App_v2.py` | Manter contexto limitado e permitir encerramento controlado |
| Agente com persona | `Agentes/App_v3.py` | Aplicar instruções de sistema e histórico limitado |
| Classificação Iris | `Modelos/Ml_iris.py` | Usar pipeline de padronização e regressão logística |
| Detecção de spam | `Modelos/NB_RN.py` | Comparar Naive Bayes e rede neural com seeds fixas |
| Toxicidade | `Modelos/RN_RL.py` | Comparar regressão logística e rede neural usando dataset interno |

## Práticas aplicadas

- Divisão estratificada entre treino e teste.
- Pipelines para evitar inconsistência no pré-processamento.
- Seeds em Python, NumPy e TensorFlow.
- Relatórios de classificação e previsões de exemplo.
- Datasets carregados por caminhos relativos ao projeto.
- Agentes com histórico limitado e comando de saída.
- Modelo do Ollama configurável pela variável `OLLAMA_MODEL`.

## Arquitetura dos experimentos

```text
Dataset
   │
   ▼
Validação e preparação
   │
   ▼
Treino / teste estratificado
   │
   ▼
Modelo clássico ou rede neural
   │
   ▼
Métricas e inferência
```

```text
Prompt + histórico limitado
            │
            ▼
       LangChain
            │
            ▼
 Ollama + modelo configurável
```

## Estrutura

```text
Machine-Learning-IA/
├── Agentes/
│   ├── App_v1.py
│   ├── App_v2.py
│   └── App_v3.py
├── Modelos/
│   ├── Bases/
│   │   ├── Toxic_Comments.csv
│   │   └── iris.csv
│   ├── Ml_iris.py
│   ├── NB_RN.py
│   └── RN_RL.py
├── assets/
│   └── machine-learning-header.svg
├── requirements.txt
└── README.md
```

## Como executar localmente

```bash
git clone https://github.com/Ruanrabello/Projects.git
cd Projects/Machine-Learning/Machine-Learning-IA
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

No Linux ou macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Execute os modelos:

```bash
python Modelos/Ml_iris.py
python Modelos/NB_RN.py
python Modelos/RN_RL.py
```

Para os agentes, mantenha o Ollama ativo:

```bash
ollama pull gemma4:latest
```

Opcionalmente defina outro modelo:

```powershell
$env:OLLAMA_MODEL="qwen3:8b"
python Agentes/App_v3.py
```

## Limitações atuais

- Os datasets são pequenos e educacionais.
- Os resultados não representam modelos prontos para produção.
- Treino, avaliação e inferência ainda permanecem no mesmo arquivo em alguns exemplos.
- Ainda não há persistência de modelos treinados ou rastreamento de experimentos.

## Roadmap

- [x] Usar caminhos relativos e pontos de entrada explícitos.
- [x] Adicionar seeds e divisão estratificada.
- [x] Limitar histórico e permitir encerramento dos agentes.
- [ ] Separar treino, avaliação e inferência em módulos.
- [ ] Adicionar matrizes de confusão e visualizações.
- [ ] Persistir modelos e métricas.
- [ ] Adicionar testes automatizados.

## Licença

Distribuído sob a [licença MIT](../../LICENSE).

## Autor

**Ruan Rabello** — estudante de Engenharia da Computação com foco em Back-end, Dados, IA e Automação.

[LinkedIn](https://www.linkedin.com/in/ruan-rabello-da-silva-9032b5274/) · [Portfólio](https://ruanportifolio.lovable.app) · [GitHub](https://github.com/Ruanrabello)
