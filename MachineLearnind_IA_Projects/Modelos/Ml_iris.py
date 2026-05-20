import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris

# 1. Carregar os dados
iris = load_iris()
X = iris.data  # Características: tamanho da pétala, etc.
y = iris.target # O que queremos prever: o tipo da flor

# 2. Dividir Treino e Teste (20% para teste)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Padronizar os dados (Opcional mas recomendado para Regressão Logística)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 4. Criar o modelo
# Usamos LogisticRegression para CLASSIFICAR as flores
modelo = LogisticRegression()

# 5. Treinar o modelo
modelo.fit(X_train, y_train)

# 6. Fazer previsões com os dados de teste
previsoes = modelo.predict(X_test)

# 7. Ver o quão bom o modelo foi
acuracia = accuracy_score(y_test, previsoes)
print(f"Acurácia do Modelo: {acuracia * 100:.2f}%")

# --- TESTE COM DADOS NOVOS ---
# Digamos que achamos uma flor com essas medidas:
nova_flor = np.array([[5.1, 3.5, 1.4, 0.2]])
nova_flor_escaneada = scaler.transform(nova_flor) # Não esqueça de padronizar!

resultado = modelo.predict(nova_flor_escaneada)
nome_da_flor = iris.target_names[resultado]

print(f"A flor que encontramos é uma: {nome_da_flor}")