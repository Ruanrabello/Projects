# Este é um exemplo simples de um agente de conversação usando o modelo "gemma4:latest" da Ollama. O agente mantém um histórico de mensagens para fornecer contexto à IA durante a conversa.

from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage

model = OllamaLLM(model="gemma4:latest")

historico = []

while True:
    pergunta = input("Você: ")                                  # Solicita a entrada do usuário para a pergunta

    historico.append(HumanMessage(content=pergunta))            # Adiciona a pergunta do usuário ao histórico como uma mensagem humana

    resposta = model.invoke(historico)                          # Envia o histórico completo para o modelo e obtém a resposta da IA

    print("IA:", resposta)                                      # Exibe a resposta da IA para o usuário

    historico.append(AIMessage(content=resposta))               # Adiciona a resposta da IA ao histórico como uma mensagem de IA, para que o contexto seja mantido nas próximas interações