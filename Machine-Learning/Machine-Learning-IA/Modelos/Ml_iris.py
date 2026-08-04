"""Classificação do dataset Iris com uma pipeline de regressão logística."""

import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42


def criar_modelo() -> Pipeline:
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(max_iter=500, random_state=RANDOM_STATE),
            ),
        ]
    )


def main() -> None:
    iris = load_iris()
    features_train, features_test, target_train, target_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=iris.target,
    )

    model = criar_modelo()
    model.fit(features_train, target_train)

    predictions = model.predict(features_test)
    accuracy = accuracy_score(target_test, predictions)

    print(f"Acurácia: {accuracy:.2%}")
    print(
        classification_report(
            target_test,
            predictions,
            target_names=iris.target_names,
            zero_division=0,
        )
    )

    new_flower = np.array([[5.1, 3.5, 1.4, 0.2]])
    predicted_class = int(model.predict(new_flower)[0])
    print(f"Nova amostra: {iris.target_names[predicted_class]}")


if __name__ == "__main__":
    main()
