# =========================================
# 📌 IMPORTAÇÕES
# =========================================
import random           # Gerar emails aleatórios(ou textos aleatórios)
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer         # Para transformar texto em números (vetorização)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB                       # Modelo de Naive Bayes para classificação de texto
from sklearn.metrics import accuracy_score  

from tensorflow.keras.models import Sequential                      #! Para criar a estrutura da rede neural
from tensorflow.keras.layers import Dense                           #! Camada densa (fully connected) para a rede neural

# =========================================
# 🔹 Modelo 1 — NAIVE BAYES
# =========================================

print("\n========== NAIVE BAYES ==========\n")                      #  Lista de frases simulando emails reais

emails = [                                              
    "Compre e ganhe um desconto",
    "Reunião na segunda-feira",
    "Parabéns, você ganhou um prêmio em dinheiro!",
    "Clique aqui e saiba mais sobre nossa promoção",
    "Relatório mensal da empresa",
    "Fotos da viagem em anexo",

    "Oferta imperdível, compre agora",
    "Você foi selecionado para ganhar prêmio",
    "Promoção válida só hoje",
    "Ganhe dinheiro rápido",
    "Oportunidade única agora",

    "Segue relatório atualizado",
    "Vamos marcar reunião",
    "Confirmação de presença",
    "Atualização do projeto enviada",
    "Convite para evento técnico"
]

labels = [                                                              # 1 para SPAM, 0 para NÃO SPAM, cada valor é referente ao email correspondente na lista de emails porem linha a linha, ou seja, o primeiro email "Compre e ganhe um desconto" é classificado como SPAM (1), o segundo email "Reunião na segunda-feira" é classificado como NÃO SPAM (0) e assim por diante.
    1, 0, 1, 1, 0, 0,
    1, 1, 1, 1, 1,
    0, 0, 0, 0, 0
]

# Vetorização
vectorizer_nb = CountVectorizer()                   #! Para transformar os emails em uma matriz de contagem de palavras (vetorização)
X = vectorizer_nb.fit_transform(emails)             #! Transformando os emails em uma matriz de contagem de palavras (vetorização)  

# Divisão
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.3, random_state=42
)

# Modelo
model_nb = MultinomialNB()                          # Criando o modelo de Naive Bayes para classificação de texto
model_nb.fit(X_train, y_train)                      # Treinando o modelo com os dados de treino (X_train e y_train), ele vai aprender a relacionar as palavras dos emails (X_train) com as classificações de SPAM ou NÃO SPAM (y_train)

# Avaliação
y_pred = model_nb.predict(X_test)                       # Fazendo previsões com os dados de teste (X_test), ele vai tentar prever se os emails de teste são SPAM ou NÃO SPAM (y_test) e comparar com as classificações reais (y_test) para calcular a acurácia do modelo
accuracy_nb = accuracy_score(y_test, y_pred)            # Calculando a acurácia do modelo, ou seja, quantos acertos o modelo teve ao tentar classificar os emails de teste como SPAM ou NÃO SPAM (y_test) e comparando com as previsões do modelo (y_pred)

print(f"Acurácia Naive Bayes: {accuracy_nb * 100:.2f}%")

# Novos testes de emails para ver se o modelo classifica corretamente como SPAM ou NÃO SPAM
testes_nb = [
    "Ganhe dinheiro fácil agora",
    "Reunião sobre o projeto amanhã",
    "Promoção exclusiva",
    "Envio do relatório em anexo"
]

testes_vec_nb = vectorizer_nb.transform(testes_nb)  # Transformando os novos emails de teste em uma matriz de contagem de palavras (vetorização) usando o mesmo vectorizer que foi usado para treinar o modelo, para garantir que as palavras sejam representadas da mesma forma (mesmas colunas na matriz) e o modelo possa fazer previsões corretas com base no que ele aprendeu durante o treinamento.
previsoes_nb = model_nb.predict(testes_vec_nb)      # Fazendo previsões com os novos emails de teste (testes_vec_nb), ele vai tentar prever se esses novos emails são SPAM ou NÃO SPAM e comparar com as classificações reais (que sabemos que são SPAM ou NÃO SPAM) para ver se o modelo está acertando ou errando.

for email, pred in zip(testes_nb, previsoes_nb):
    print(f"\nEmail: {email}")
    print(f"Classificação: {'SPAM' if pred == 1 else 'NÃO SPAM'}")














# =========================================
# 🔹 Modelo 2 — REDE NEURAL
# =========================================

print("\n========== REDE NEURAL ==========\n")

spam_keywords = [
    "ganhe", "promoção", "desconto", "oferta", "dinheiro",
    "clique", "urgente", "agora", "imperdível", "prêmio"
]

ham_keywords = [
    "reunião", "relatório", "projeto", "agenda", "empresa",
    "documento", "atualização", "anexo", "cronograma", "equipe"
]

def gerar_email(lista):                                 # Gerar um email aleatório usando palavras de uma lista (spam_keywords ou ham_keywords), o tamanho do email é aleatório entre 5 e 10 palavras(k=tamanho), e as palavras são escolhidas aleatoriamente da lista fornecida.  " ".join(...) junta essas palavras em uma única string separada por espaços, formando o email gerado. A função random.choices(lista, k=tamanho) escolhe k palavras aleatórias da lista fornecida, e " ".join(...) junta essas palavras em uma única string separada por espaços, formando o email gerado.
    tamanho = random.randint(5, 10)
    return " ".join(random.choices(lista, k=tamanho))   # Gerar um email aleatório usando palavras de uma lista (spam_keywords ou ham_keywords), o tamanho do email é aleatório entre 5 e 10 palavras, e as palavras são escolhidas aleatoriamente da lista fornecida. A função random.choices(lista, k=tamanho) escolhe k palavras aleatórias da lista fornecida, e " ".join(...) junta essas palavras em uma única string separada por espaços, formando o email gerado.        

emails = [] # Lista para armazenar os emails gerados
labels = [] # Lista para armazenar as classificações dos emails gerados (1 para SPAM, 0 para NÃO SPAM)

# 50 spam
for _ in range(50):        # Gerar 50 emails de SPAM usando as palavras da lista spam_keywords e classificá-los como 1 (SPAM)
    emails.append(gerar_email(spam_keywords))   # Gerar um email aleatório usando as palavras da lista spam_keywords e classificá-lo como 1 (SPAM)
    labels.append(1)    # Classificando os emails gerados como 1 (SPAM)

# 50 não spam
for _ in range(50):        # Gerar 50 emails de NÃO SPAM usando as palavras da lista ham_keywords e classificá-los como 0 (NÃO SPAM)
    emails.append(gerar_email(ham_keywords))    # Gerar um email aleatório usando as palavras da lista ham_keywords e classificá-lo como 0 (NÃO SPAM)
    labels.append(0)        # Classificando os emails gerados como 0 (NÃO SPAM)

# Embaralhar
dados = list(zip(emails, labels))  # Criar uma lista de tuplas onde cada tupla contém um email e sua classificação correspondente (SPAM ou NÃO SPAM), para facilitar o embaralhamento dos dados.
random.shuffle(dados)              # Embaralhar a lista de tuplas (dados) para garantir que os emails de SPAM e NÃO SPAM estejam misturados, o que é importante para o treinamento do modelo, para evitar que ele aprenda padrões específicos de ordem dos dados.
emails, labels = zip(*dados)       # Descompactar a lista de tuplas (dados) de volta em duas listas separadas: uma para os emails e outra para as classificações (labels), para que possamos usar essas listas para treinar o modelo de rede neural.

# Vetorização
vectorizer_nn = CountVectorizer()   # transforma palavras em uma “tabela de contagem”, pq a ia nao entende texto, ele vai criar uma matriz
X = vectorizer_nn.fit_transform(emails).toarray() # transforma os emails em uma matriz de contagem de palavras (vetorização) usando o CountVectorizer, onde cada linha representa um email e cada coluna representa uma palavra do vocabulário, e o valor em cada célula é a contagem de quantas vezes aquela palavra aparece naquele email. O método fit_transform(emails) ajusta o vectorizer ao conjunto de emails e transforma os emails em uma matriz de contagem de palavras, e o método toarray() converte essa matriz esparsa em um array denso do NumPy, que é mais fácil de manipular para treinar a rede neural.
y = np.array(labels)

# Divisão
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Modelo
model_nn = Sequential()                                           # Criando um modelo sequencial para a rede neural, onde as camadas são empilhadas uma após a outra. O modelo sequencial é uma maneira simples de construir uma rede neural, onde cada camada tem exatamente uma entrada e uma saída, e as camadas são conectadas em sequência. Isso é adequado para a maioria dos casos de uso de redes neurais, especialmente para tarefas de classificação como esta.
model_nn.add(Dense(16, input_dim=X.shape[1], activation='relu'))  # Adicionando a primeira camada densa (fully connected) com 16 neurônios, onde input_dim=X.shape[1] especifica o número de entradas para a camada (que é igual ao número de colunas na matriz de contagem de palavras, ou seja, o tamanho do vocabulário), e activation='relu' especifica a função de ativação ReLU (Rectified Linear Unit) para introduzir não linearidade na rede neural, o que ajuda a rede a aprender padrões mais complexos nos dados.
model_nn.add(Dense(8, activation='relu'))                         # Adicionando a segunda camada densa com 8 neurônios e função de ativação ReLU, para permitir que a rede neural aprenda representações mais abstratas dos dados após a primeira camada.
model_nn.add(Dense(1, activation='sigmoid'))                      # Adicionando a camada de saída com 1 neurônio e função de ativação sigmoid, que é apropriada para tarefas de classificação binária (SPAM ou NÃO SPAM), pois a função sigmoid retorna um valor entre 0 e 1, representando a probabilidade de um email ser classificado como SPAM (1) ou NÃO SPAM (0).

# Compilar

model_nn.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Treinar
model_nn.fit(X_train, y_train, epochs=10, batch_size=4, verbose=1)

# Avaliar
loss, accuracy_nn = model_nn.evaluate(X_test, y_test)
print(f"\nAcurácia Rede Neural: {accuracy_nn * 100:.2f}%")

# Teste
testes_nn = [
    "ganhe dinheiro agora",
    "reunião de equipe amanhã",
    "oferta imperdível clique agora",
    "envio do relatório atualizado",
    "REUNIAO DE DINHEIRO AGORA"
]

testes_vec_nn = vectorizer_nn.transform(testes_nn).toarray()
previsoes_nn = model_nn.predict(testes_vec_nn)

for email, pred in zip(testes_nn, previsoes_nn):
    print(f"\nEmail: {email}")
    print(f"Classificação: {'SPAM' if pred > 0.5 else 'NÃO SPAM'}")