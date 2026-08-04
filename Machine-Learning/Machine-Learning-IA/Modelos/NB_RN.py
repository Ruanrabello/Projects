"""Compara Naive Bayes e rede neural em uma classificação didática de spam."""

import random

import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input


RANDOM_STATE = 42
random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)
tf.random.set_seed(RANDOM_STATE)

SPAM_KEYWORDS = [
    "ganhe", "promoção", "desconto", "oferta", "dinheiro",
    "clique", "urgente", "agora", "imperdível", "prêmio",
]
HAM_KEYWORDS = [
    "reunião", "relatório", "projeto", "agenda", "empresa",
    "documento", "atualização", "anexo", "cronograma", "equipe",
]

TEST_MESSAGES = [
    "ganhe dinheiro agora",
    "reunião de equipe amanhã",
    "oferta imperdível clique agora",
    "envio do relatório atualizado",
]


def class_name(value: int | bool) -> str:
    return "SPAM" if int(value) == 1 else "NÃO SPAM"


def run_naive_bayes() -> None:
    messages = [
        "Compre e ganhe um desconto",
        "Reunião na segunda-feira",
        "Parabéns, você ganhou um prêmio em dinheiro",
        "Clique aqui e saiba mais sobre nossa promoção",
        "Relatório mensal da empresa",
        "Fotos da viagem em anexo",
        "Oferta imperdível compre agora",
        "Você foi selecionado para ganhar prêmio",
        "Promoção válida só hoje",
        "Ganhe dinheiro rápido",
        "Oportunidade única agora",
        "Segue relatório atualizado",
        "Vamos marcar reunião",
        "Confirmação de presença",
        "Atualização do projeto enviada",
        "Convite para evento técnico",
    ]
    labels = np.array([1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0])

    vectorizer = CountVectorizer(ngram_range=(1, 2))
    features = vectorizer.fit_transform(messages)
    features_train, features_test, labels_train, labels_test = train_test_split(
        features,
        labels,
        test_size=0.3,
        random_state=RANDOM_STATE,
        stratify=labels,
    )

    model = MultinomialNB()
    model.fit(features_train, labels_train)
    predictions = model.predict(features_test)

    print("\n========== NAIVE BAYES ==========\n")
    print(f"Acurácia: {accuracy_score(labels_test, predictions):.2%}")
    print(classification_report(labels_test, predictions, zero_division=0))

    test_features = vectorizer.transform(TEST_MESSAGES)
    for message, prediction in zip(TEST_MESSAGES, model.predict(test_features)):
        print(f"{class_name(prediction):10} | {message}")


def generate_message(words: list[str]) -> str:
    size = random.randint(5, 10)
    return " ".join(random.choices(words, k=size))


def create_synthetic_dataset(samples_per_class: int = 150) -> tuple[list[str], np.ndarray]:
    dataset = [
        (generate_message(SPAM_KEYWORDS), 1)
        for _ in range(samples_per_class)
    ] + [
        (generate_message(HAM_KEYWORDS), 0)
        for _ in range(samples_per_class)
    ]
    random.shuffle(dataset)

    messages, labels = zip(*dataset)
    return list(messages), np.asarray(labels, dtype=np.float32)


def create_neural_network(input_size: int) -> Sequential:
    model = Sequential(
        [
            Input(shape=(input_size,)),
            Dense(16, activation="relu"),
            Dense(8, activation="relu"),
            Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(
        loss="binary_crossentropy",
        optimizer="adam",
        metrics=["accuracy"],
    )
    return model


def run_neural_network() -> None:
    messages, labels = create_synthetic_dataset()
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(messages).toarray().astype(np.float32)

    features_train, features_test, labels_train, labels_test = train_test_split(
        features,
        labels,
        test_size=0.3,
        random_state=RANDOM_STATE,
        stratify=labels,
    )

    model = create_neural_network(features.shape[1])
    model.fit(
        features_train,
        labels_train,
        epochs=12,
        batch_size=16,
        validation_split=0.15,
        verbose=0,
    )
    _, accuracy = model.evaluate(features_test, labels_test, verbose=0)

    print("\n========== REDE NEURAL ==========\n")
    print(f"Acurácia: {accuracy:.2%}")

    test_features = vectorizer.transform(TEST_MESSAGES).toarray().astype(np.float32)
    probabilities = model.predict(test_features, verbose=0).reshape(-1)

    for message, probability in zip(TEST_MESSAGES, probabilities):
        prediction = probability >= 0.5
        print(f"{class_name(prediction):10} | {probability:.2%} | {message}")


def main() -> None:
    run_naive_bayes()
    run_neural_network()


if __name__ == "__main__":
    main()
