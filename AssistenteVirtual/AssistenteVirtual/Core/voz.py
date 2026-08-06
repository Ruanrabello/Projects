import pyttsx4                                          #? Importa biblioteca para sintese de voz
import speech_recognition as sr                         #? Importa biblioteca que converte oque eu falo em texto
import time                                             #? importa biblioteca com funcoes relacionadas ao tempo

# Inicializadores
reconhecedor = sr.Recognizer()          #! Objeto que gerencia a captura/interpretacão de áudio 
sintetizador = pyttsx4.init('sapi5')                    #? Inicializa o engine do pyttsx4 e escolhe o driver sapi5
sintetizador.setProperty('rate', 220)                   #? Ajusta a velocidade de fala (palavras por minuto).
sintetizador.setProperty('volume', 1.0)                 #? Define o volume da fala; 1.0

voices = sintetizador.getProperty('voices')             #? Recupera a lista de vozes disponíveis do engine
sintetizador.setProperty('voice', voices[0].id)         #? Define a voz a ser usada; aqui usa a primeira voz disponível


def falar_texto(texto):                                       #? Converte texto em voz
    texto = (f"Senhor, {texto}")                              #? (adiciona no início) a string "Senhor, " ao texto recebido
    if not texto.strip():                                     #? Verifica se texto está vazio ou contém só espaços(strip() remover espaços em branco nas extremidades). Se estiver vazio, vai evitar tentar falar algo.)
        return
    try:
        time.sleep(1)                                         #? Pausa de 1 segundo antes de falar  
        sintetizador.say(texto)                               #? Faz o computador falar.
        sintetizador.runAndWait()                             #? Bloqueante: espera terminar de falar
    except Exception as e:
        print(f"❌ Erro ao falar: {e}")                       #? Captura qualquer exceção que ocorra dentro do try (por exemplo, problema com driver de áudio)


def ouvir_microfone():                                        #?  Ouvindo o microfone e retornando texto transcrito
    with sr.Microphone() as mic:                              #?  Cria um objeto que representa o dispositivo de microfone do seu computador. as mic significa: dê o nome mic a esse objeto do microfone.
        print("🎤 Ouvindo...")
        reconhecedor.adjust_for_ambient_noise(mic, duration=1)          #? Ajusta o ruído
        audio = reconhecedor.listen(mic)                                #? grava até detectar silêncio

    try:
        texto = reconhecedor.recognize_google(audio, language="pt-BR")      #? Usa o sistema de voz do Google grátis para converter áudio → texto
        print(f"Você disse: {texto}")

        wake_word = "jarvis"                                                #? palavra de ativação
        
        if texto.lower().startswith(wake_word):                             #? Verifica se o texto transcrito, em letras minúsculas, começa com a wake word
            return texto[len(wake_word):].strip()                           #? Remove o nome antes de mandar pra IA, Retorna a parte do texto após a wake word: usa slicing para pular os primeiros caracteres
        else:
            print("Aguardando palavra de ativação")
            return ""
    except:
        print("❌ Não entendi.")
        return ""
   
