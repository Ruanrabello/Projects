import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split      # Para dividir os dados em treino e teste
from sklearn.preprocessing import StandardScaler          # Para padronizar os dados (muito importante para Regressão Logística)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score                # Para avaliar a acurácia do modelo(Mede o desempenho → acurácia (acertos))
from sklearn.datasets import load_iris                    # Para carregar um dataset de exemplo (Iris)

def baixar_arquivoIris():
    # 1. Carregar o dataset Iris
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)     # Criando um DataFrame com as features
    df['species'] = iris.target                                       # Adicionando a coluna de rótulos (tipos de flores)
    return df, iris

df, iris = baixar_arquivoIris()                          # Carregando tabela inteira pra variável df
x = df.drop('species', axis=1).values              # Removendo a coluna de species para criar a matriz de features (medidas das flores(essas sao as informacoes que vamos usar para treinar o modelo)
y = df['species'].values                           # Separando os rótulos (tipos de flores(que é o que queremos prever))

# 2. Dividir Treino e Teste (20% para teste)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)           # Dividindo os dados em treino e teste (20% para teste, 80% para treino) ( test_size=0.2 → 20% dos dados para teste, random_state=42 → para garantir que a divisão seja a mesma toda vez que rodarmos o código)

# 3. Padronizar os dados, colocando tudo na mesma escala, se nao o modelo pode ter dificuldade para aprender (pois algumas features podem ter valores muito maiores que outras, o que pode confundir o modelo)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 4. Criar o modelo
modelo = LogisticRegression()

# 5. Treinar o modelo com os dados de treino (X_train e y_train), ele vai aprender a relacionar as medidas das flores (X_train) com os tipos de flores (y_train)
modelo.fit(X_train, y_train)

# 6. Fazer previsões com os dados de teste, recebdo as medidas das flores de teste (X_test) e tentando prever os tipos de flores (y_test)
previsoes = modelo.predict(X_test)

# 7. Ver o quão bom o modelo foi, ele vai comparar as previsões (previsoes) com os rótulos reais (y_test) e calcular a acurácia (quantos acertos o modelo teve)
acuracia = accuracy_score(y_test, previsoes)
print(f"Acurácia do Modelo: {acuracia * 100:.2f}%")


#! --------------------------------------------------------------------------------------- 

# --- TESTE COM DADOS NOVOS ---
# Digamos que achamos uma flor com essas medidas:
nova_flor = np.array([[5.1, 3.5, 1.4, 0.2]]) # cada valor e referente a uma medida da flor (comprimento da sépala, largura da sépala, comprimento da pétala, largura da pétala)
nova_flor_escaneada = scaler.transform(nova_flor) # Não esqueça de padronizar!

resultado = modelo.predict(nova_flor_escaneada)
nome_da_flor = iris.target_names[resultado]

print(f"A flor que encontramos é uma: {nome_da_flor}")