# 📊 Machine Learning & IA

Laboratório de estudos aplicados em classificação, processamento de texto, redes neurais e agentes locais com Ollama.

## Projetos incluídos

| Área | Arquivos | Objetivo |
|---|---|---|
| Agentes locais | `Agentes/` | Evolução de um agente conversacional com histórico e prompt de sistema |
| Classificação Iris | `Modelos/Ml_iris.py` | Treinar uma regressão logística para classificar flores |
| Spam | `Modelos/NB_RN.py` | Comparar Naive Bayes e rede neural em classificação de texto |
| Toxicidade | `Modelos/RN_RL.py` | Comparar regressão logística e rede neural em comentários tóxicos |

## Tecnologias

Python, Pandas, NumPy, Scikit-learn, TensorFlow, LangChain e Ollama.

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Para os agentes, mantenha o Ollama em execução e instale um modelo compatível. Os scripts de modelos podem ser executados individualmente, por exemplo:

```bash
python Modelos/Ml_iris.py
python Modelos/RN_RL.py
```

## Estrutura

```text
Machine-Learning-IA/
├── Agentes/
├── Modelos/
│   ├── Bases/
│   ├── Ml_iris.py
│   ├── NB_RN.py
│   └── RN_RL.py
├── requirements.txt
└── README.md
```

## Status

Projeto educacional em evolução. Os exemplos foram mantidos separados para mostrar a progressão dos estudos e facilitar testes individuais.

## Autor

**Ruan Rabello**
