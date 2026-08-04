# 1. Classificador de comentários tóxicos
# Entrada: texto (comentário)
# Saída: tóxico ou não tóxico

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input

# ===================================
#  Modelo 1: Regressão Logística
# ===================================
print("\n\n--- Modelo 1: Regressão Logística ---\n")

def baixar_arquivoToxico():
    Comentarios = pd.read_csv(r"C:\Users\ruanb\Downloads\Estudos\Code\Ml_Dl\Toxic_Comments.csv")  # Lendo o arquivo CSV com os comentários tóxicos (certifique-se de usar o caminho correto para o seu arquivo)
    return Comentarios

df = baixar_arquivoToxico()                         
x = df['comentario']   # entrada (texto)
y = df['toxico']       # saída (rótulo)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

vectorizer = CountVectorizer(ngram_range=(1,2))
x_train = vectorizer.fit_transform(x_train) # fit transform → ele vai aprender o vocabulário dos comentários de treino e transformar os textos em vetores numéricos (matriz esparsa)
x_test = vectorizer.transform(x_test) # transform → ele vai usar o mesmo vocabulário aprendido no treino para transformar os comentários de teste em vetores numéricos (matriz esparsa)

modelo = LogisticRegression()
modelo.fit(x_train, y_train)

y_pred = modelo.predict(x_test)
acuracia = accuracy_score(y_test, y_pred)
print(f"Acurácia do Modelo de Regressão Logística: {acuracia * 100:.2f}%")


testes = [
    "você é um idiota",
    "eu te odeio",
    "você é incrível",
    "eu gosto de você",
    "você é um lixo"
]

testes_transformados = vectorizer.transform(testes)
previsoes = modelo.predict(testes_transformados)

for comentario, previsao in zip(testes, previsoes):
    label = "Tóxico" if previsao == 1 else "Não Tóxico"
    print(f"Comentário: '{comentario}' → {label}")


# ===================================
#  Modelo 2: Rede Neural Simples        
# ===================================

print("\n\n--- Modelo 2: Rede Neural Simples ---\n")

# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
# vectorizer = CountVectorizer()
# x_train = vectorizer.fit_transform(x_train) 
# x_test = vectorizer.transform(x_test)


x_train_nn = x_train.toarray()
x_test_nn = x_test.toarray()

model_nn = Sequential([
    Input(shape=(x_train_nn.shape[1],)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])
model_nn.compile(
    loss='binary_crossentropy',
    optimizer='adam', 
    metrics=['accuracy']
)

model_nn.fit(
    x_train_nn, y_train, 
    epochs=30, 
    batch_size=8,
    verbose=1
)

loss, accuracy = model_nn.evaluate(x_test_nn, y_test, verbose=0)
print(f"Acurácia do Modelo de Rede Neural: {accuracy * 100:.2f}%")

testes = [
    "você é incrível mesmo",
    "isso está horrível",
    "não ficou tão ruim",
    "eu odiei isso",
    "ótimo resultado"
]
testes_transformados = vectorizer.transform(testes).toarray()
previsoes_nn = model_nn.predict(testes_transformados)

for comentario, previsao in zip(testes, previsoes_nn):
    label = "Tóxico" if previsao[0] >= 0.5 else "Não Tóxico"
    print(f"Comentário: '{comentario}' → {label}")




