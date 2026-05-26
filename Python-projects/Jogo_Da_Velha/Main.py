from random import randrange
from time import sleep

Matriz = [
    [" 1 ", " 2 ", " 3 "], 
    [" 4 ", " 5 ", " 6 "], 
    [" 7 ", " 8 ", " 9 "]
]


def ImprimeMatriz():
    for i in range(3):
        for j in range(3):
            print(Matriz[i][j], end="")
        print()
    
def JogadaHumana():
    while True:
        try:
            
            Jogada = int(input("Digite o número da posição onde deseja jogar ou 0 para sair: "))

            if Jogada == 0:
                exit()

            if Jogada < 1 or Jogada > 9:
                print("Número inválido. Tente novamente.")
                continue

            Linha = (Jogada - 1) // 3                   # retorna o quociente sem a parte decimal. Ele é usado para calcular a linha, exemplo: se o usuário digitar 5, 5 - 1 = 4, 4 // 3 = 1 (linha 1)
 
            Coluna = (Jogada - 1) % 3                   # retorna o resto da divisão. Ele é usado para calcular a coluna, exemplo: se o usuário digitar 5, 5 - 1 = 4, 4 % 3 = 1 (sobra 1)

            if Matriz[Linha][Coluna] in [" X ", " O "]: # verifica se a posição já está ocupada por um "X" ou "O"
                print("Posição já ocupada. Tente novamente.")
                continue

            Matriz[Linha][Coluna] = " X "
            sleep(1)  # Pausa por 1 segundo para simular o tempo de resposta do jogador
        
            break

        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 9.")

def JogadaComputador():
    while True:
        jogada = randrange(1, 10) # gera um número aleatório entre 1 e 9

        Linha = (jogada - 1) // 3
        Coluna = (jogada - 1) % 3

        if Matriz[Linha][Coluna] not in [" X ", " O "]: # verifica se a posição não está ocupada por um "X" ou "O"
            Matriz[Linha][Coluna] = " O "
            sleep(1)  # Pausa por 1 segundo para simular pensamento do computador
            ImprimeMatriz()
            print(f"O computador jogou na posição {jogada}.")
            break

def VerificarVencedor():
    # Verificar linhas
    for i in range(3):
        if Matriz[i][0] == Matriz[i][1] == Matriz[i][2]:
            return Matriz[i][0].strip()  # Retorna "X" ou "O", o strip remove os espaços em branco para retornar apenas "X" ou "O"

    # Verificar colunas
    for j in range(3):
        if Matriz[0][j] == Matriz[1][j] == Matriz[2][j]:
            return Matriz[0][j].strip()  # Retorna "X" ou "O", o strip remove os espaços em branco para retornar apenas "X" ou "O"

    # Verificar diagonais
    if Matriz[0][0] == Matriz[1][1] == Matriz[2][2]:
        return Matriz[0][0].strip()  # Retorna "X" ou "O", o strip remove os espaços em branco para retornar apenas "X" ou "O"
    
    if Matriz[0][2] == Matriz[1][1] == Matriz[2][0]:
        return Matriz[0][2].strip()  # Retorna "X" ou "O", o strip remove os espaços em branco para retornar apenas "X" ou "O"

    return None  # Nenhum vencedor ainda

def VerificarEmpate():
    for i in range(3):
        for j in range(3):
            if Matriz[i][j] not in [" X ", " O "]: # Verifica se ainda existe alguma posição vazia
                return False  # Ainda há posições vazias, não é empate
    return True  # Todas as posições estão preenchidas, é empate

def ComeçarJogo():

    ImprimeMatriz()

    while True:
        JogadaHumana()

        vencedor = VerificarVencedor()
        if vencedor in ["X", "O"]:
            print(f"Parabéns! O jogador '{vencedor}' venceu!")
            break

        if VerificarEmpate():
            print("O jogo empatou!")
            break

        JogadaComputador()

        vencedor = VerificarVencedor()
        if vencedor in ["X", "O"]:
            print(f"O computador venceu! O jogador '{vencedor}' perdeu.")
            break

ComeçarJogo() 