from langchain_ollama import OllamaLLM

model = OllamaLLM(model="gemma4:latest")

response = model.invoke("Olá!")

print(response)