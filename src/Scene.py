from Table import *
import numpy as np

'''
    Geração de jogos em tabelas para estudo do Jogo Clue Card
    Para representar as 15 cartas do jogo, serão usados os números de 1 a 15, 
    onde cada um representa, respectivamente:
    
    1 -> Castiçal
    2 -> Corda
    3 -> Faca
    4 -> Revólver

    5 -> Cozinha
    6 -> Hall
    7 -> Sala de Estar
    8 -> Sala de Jantar
    9 -> Spa

    10 -> Green
    11 -> Mustard
    12 -> Peacock
    13 -> Plum
    14 -> Scarlet
    15 -> White
'''


def gerar_crime():
    '''
    Método que gera o crime.
    '''
    arma = np.random.randint(1, 5)
    lugar = np.random.randint(5, 10)
    suspeito = np.random.randint(10, 16)
    crime = np.array([arma, lugar, suspeito])
    return crime


def gerar_evidencias(crime):
    # Cria um array de números de 1 a 15
    pistas = np.arange(1, 16)
    
    # Vou remover os valores do crime do array de evidencias
    # A mascara vai ser um array que vai armazenar os elementos de pista que não estiverem em crime
    mascara = ~np.isin(pistas, crime)
    evidencias = pistas[mascara]
    return evidencias


def gerar_jogadores(evidencias):
    '''
    Vai receber um array com as evidencias e distribuir elas entre os jogadores
    Retorna uma matriz (array de array) de jogadorse 'jogadores[]' e suas cartas 'jogadores[][]'
    '''
    jogadores = []

    for i in range(4):
        jogador = np.random.choice(evidencias, size=3, replace=False)
        evidencias = evidencias[~np.isin(evidencias, jogador)]
        jogador.sort()
        jogadores.append(jogador)

    jogadores = np.array(jogadores)

    return jogadores


def gerar_tabela(jogadores):
    tabela_aux = []

    for i in range(4):
        tabela_jogador_np = np.arange(1, 16)
        mascara = np.isin(tabela_jogador_np, jogadores[i])
        tabela_jogador_np[mascara] = 1
        tabela_jogador_np[~mascara] = -1
        tabela_jogador = tabela_jogador_np.tolist()
        tabela_aux.append(tabela_jogador)

    tabela = np.array(tabela_aux)

    return tabela.tolist()

def corromper_tabela(tabela, chance):
    '''
    Método que corrompe uma tabela. Recebe a tabela junto as chances de corromper o 
    número 1 e o -1. Retorna a tabela corrompida. 
    '''
    for i in range(15):
        for j in range(1,4):
            if tabela[j][i] == 1:
                if np.random.randint(0, 100) < chance[0]:
                    tabela[j][i] = 0
            elif tabela[j][i] == -1:
                if np.random.randint(0, 100) < chance[1]:
                    tabela[j][i] = 0
    return tabela;

def criar_cenario(chance):
    '''
    O método criar_cenario, cria o cenario do crime e retorna o array do crime e a tabela já corrompida.
    '''
    crime = gerar_crime()
    return crime, corromper_tabela(gerar_tabela(gerar_jogadores(gerar_evidencias(crime))), chance)