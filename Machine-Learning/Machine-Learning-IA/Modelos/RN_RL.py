"""Compara regressão logística e rede neural na classificação de toxicidade."""

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "Bases" / "Toxic_Comments.csv"
RANDOM_STATE = 42


def carregar_dados() -> pd.DataFrame:
    """Carrega o dataset versionado dentro do próprio projeto."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset não encontrado em: {DATASET_PATH}. "
            "Confirme se a pasta Modelos/Bases foi clonada corretamente."
        )

    dados = pd.read_csv(DATASET_PATH)
    colunas_obrigatorias = {"comentario", "toxico"}
    if not colunas_obrigatorias.issubset(dados.columns):
        raise ValueError(
            "O dataset precisa conter as colunas 'comentario' e 'toxico'."
        )

    return dados.dropna(subset=["comentario", "toxico"])


def preparar_dados(dados: pd.DataFrame):
    textos = dados["comentario"].astype(str)
    rotulos = dados["toxico"].astype(int)

    x_treino_texto, x_teste_texto, y_treino, y_teste = train_test_split(
        textos,
        rotulos,
        test_size=0.30,
        random_state=RANDOM_STATE,
        stratify=rotulos,
    )

    vetorizador = CountVectorizer(ngram_range=(1, 2))
    x_treino = vetorizador.fit_transform(x_treino_texto)
    x_teste = vetorizador.transform(x_teste_texto)

    return vetorizador, x_treino, x_teste, y_treino, y_teste


def executar_regressao_logistica(
    vetorizador,
    x_treino,
    x_teste,
    y_treino,
    y_teste,
) -> None:
    print("\n--- Modelo 1: Regressão Logística ---\n")

    modelo = LogisticRegression(max_iter=1_000, random_state=RANDOM_STATE)
    modelo.fit(x_treino, y_treino)

    previsoes = modelo.predict(x_teste)
    acuracia = accuracy_score(y_teste, previsoes)
    print(f"Acurácia: {acuracia * 100:.2f}%")

    exemplos = [
        "você é um idiota",
        "eu te odeio",
        "você é incrível",
        "eu gosto de você",
        "você é um lixo",
    ]
    exemplos_vetorizados = vetorizador.transform(exemplos)

    for comentario, previsao in zip(
        exemplos,
        modelo.predict(exemplos_vetorizados),
    ):
        classe = "Tóxico" if previsao == 1 else "Não tóxico"
        print(f"Comentário: {comentario!r} → {classe}")


def executar_rede_neural(
    vetorizador,
    x_treino,
    x_teste,
    y_treino,
    y_teste,
) -> None:
    print("\n--- Modelo 2: Rede Neural Simples ---\n")

    x_treino_denso = x_treino.toarray()
    x_teste_denso = x_teste.toarray()

    modelo = Sequential(
        [
            Input(shape=(x_treino_denso.shape[1],)),
            Dense(32, activation="relu"),
            Dense(16, activation="relu"),
            Dense(1, activation="sigmoid"),
        ]
    )
    modelo.compile(
        loss="binary_crossentropy",
        optimizer="adam",
        metrics=["accuracy"],
    )
    modelo.fit(
        x_treino_denso,
        y_treino,
        epochs=30,
        batch_size=8,
        verbose=1,
    )

    _, acuracia = modelo.evaluate(x_teste_denso, y_teste, verbose=0)
    print(f"Acurácia: {acuracia * 100:.2f}%")

    exemplos = [
        "você é incrível mesmo",
        "isso está horrível",
        "não ficou tão ruim",
        "eu odiei isso",
        "ótimo resultado",
    ]
    exemplos_vetorizados = vetorizador.transform(exemplos).toarray()
    previsoes = modelo.predict(exemplos_vetorizados, verbose=0)

    for comentario, previsao in zip(exemplos, previsoes):
        classe = "Tóxico" if previsao[0] >= 0.5 else "Não tóxico"
        print(f"Comentário: {comentario!r} → {classe}")


def main() -> None:
    dados = carregar_dados()
    vetorizador, x_treino, x_teste, y_treino, y_teste = preparar_dados(dados)

    executar_regressao_logistica(
        vetorizador,
        x_treino,
        x_teste,
        y_treino,
        y_teste,
    )
    executar_rede_neural(
        vetorizador,
        x_treino,
        x_teste,
        y_treino,
        y_teste,
    )


if __name__ == "__main__":
    main()
