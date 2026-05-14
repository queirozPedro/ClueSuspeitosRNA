from Scene import *
from Table import *

def gerar_tabelas_txt():
    '''
    Método que gera as tabelas em txt
    '''
    
    print("Caracteristicas do Arquivo Txt")
    
    quant_tabelas = int(input("Quantidade de Tabelas: "))
    chance = [0, 0]
    chance[0] = int(input("Probabilidade de 1 ser corrompido(0 a 100): "))
    chance[1] = int(input("Probabilidade de -1 ser corrompido(0 a 100): "))
    nome_arquivo = f'{quant_tabelas}_jogos_com_{chance[0]}%_para_1_e_{chance[1]}%_para_-1.txt'

    cartas = [
        "Castical(01)", "Corda(02)", "Faca(03)", "Revolver(04)",
        "Cozinha(05)", "Hall(06)", "Sala de Estar(07)", "Sala de Jantar(08)",
        "Spa(09)", "Green(10)", "Mustard(11)", "Peacock(12)",
        "Plum(13)", "Scarlet(14)", "White(15)"
    ]

    with open(nome_arquivo, 'w') as arquivo:
        for i in range(quant_tabelas):

            crime = gerar_crime()
            evidencias = gerar_evidencias(crime)
            jogadores = gerar_jogadores(evidencias)
            tabela = corromper_tabela(gerar_tabela(jogadores), chance)

            linhas = [
                f'Jogo {i+1} de {quant_tabelas}\n',
                f'{chance[0]}% de chance de corromper o 1\n',
                f'{chance[1]}% de chance de corromper o -1\n\n',
                f'Crime: {cartas[crime[0]-1]}, {cartas[crime[1]-1]}, {cartas[crime[2]-1]}\n',
                f'Jogador 0: {cartas[jogadores[0][0]-1]}, {cartas[jogadores[0][1]-1]}, {cartas[jogadores[0][2]-1]}\n',
                f'Jogador 1: {cartas[jogadores[1][0]-1]}, {cartas[jogadores[1][1]-1]}, {cartas[jogadores[1][2]-1]}\n',
                f'Jogador 2: {cartas[jogadores[2][0]-1]}, {cartas[jogadores[2][1]-1]}, {cartas[jogadores[2][2]-1]}\n',
                f'Jogador 3: {cartas[jogadores[3][0]-1]}, {cartas[jogadores[3][1]-1]}, {cartas[jogadores[3][2]-1]}\n\n',
                f'Tabela Corrompida \n',
                gerar_string_tabela(tabela),
                '\n\n\n'
            ]

            arquivo.writelines(linhas)
    print("Arquivo Gerado com Sucesso")


def gerar_tabelas_tex():
    '''
    Método que gera as tabelas em LaTex
    '''
    print("Caracteristicas do Arquivo LaTex")
    
    quant_tabelas = int(input("Quantidade de Tabelas: "))
    chance = [0, 0]
    chance[0] = int(input("Probabilidade de 1 ser corrompido(0 a 100): "))
    chance[1] = int(input("Probabilidade de -1 ser corrompido(0 a 100): "))
    nome_arquivo = f'{quant_tabelas}_jogos_com_{chance[0]}%_para_1_e_{chance[1]}%_para_-1.tex'

    with open(nome_arquivo, 'w') as arquivo:
        
        texto = [
            r'\documentclass{article}',
            r'\usepackage{graphicx} % Required for inserting images',
            r'\usepackage[portuguese]{babel}',
            r'\usepackage[utf8]{inputenc}',
            r'\usepackage[T1]{fontenc}',
            r'\begin{document}',
            r'\title{Teste de Corrupcao de Dados}'
        ]

        for n in range(quant_tabelas):
            crime = gerar_crime()
            evidencias = gerar_evidencias(crime)
            jogadores = gerar_jogadores(evidencias)
            tabela = corromper_tabela(gerar_tabela(jogadores), chance)

            cartas = [
                "01 - Castical", "02 - Corda", "03 - Faca", "04 - Revolver",
                "05 - Cozinha", "06 - Hall", "07 - Sala de Estar", "08 - Sala de Jantar",
                "09 - Spa", "10 - Green", "11 - Mustard", "12 - Peacock",
                "13 - Plum", "14 - Scarlet", "15 - White"
            ]

            linha = r'\section{Jogo '+ str(n+1)+ ' de ' + str(quant_tabelas) +'}'

            texto.append(linha)

            texto.extend([
                r'\begin{table}[!htb]',
                r'\begin{tabular}{|l|l|l|l|l|}',
                r'\hline',
                r'Cartas & Jogador 0 & Jogador 1 & Jogador 2 & Jogador 3 \\ \hline'
            ])

            for i in range(15):
                linha = cartas[i]
                for j in range(4):
                    linha += f' & {tabela[j][i]}'
                linha += r' \\ \hline'
                texto.append(linha)

            texto.extend([
                r'\end{tabular}',
                r'\end{table}',
                '\\ \\'
            ])

        texto.append(r'\end{document}')

        arquivo.writelines('\n'.join(texto))

def gerar_jogo_arquivo():
    crime = gerar_crime()
    evidencias = gerar_evidencias(crime)
    jogadores = gerar_jogadores(evidencias)
    tabela = gerar_tabela(jogadores)
    
    linhas = [
        f'Caracteristicas do Jogo'
        f'Crime: {crime}\n'
        f'Evidencias: {evidencias}\n'
        f'Jogadores:\n{jogadores}\n\n'
    ]

    tabela_arma = []
    for i in range(4):
        for j in range(4):
            tabela_arma.append(tabela[i][j])

    tabela_lugar = []
    for i in range(4):
        for j in range(4,9):
            tabela_lugar.append(tabela[i][j])

    tabela_suspeito = []
    for i in range(4):
        for j in range(9,15):
            tabela_suspeito.append(tabela[i][j])

    with open ('arquivo.txt', 'w') as arquivo:
        linhas.extend([
            f'Tabela\n{tabela}\nTamanho: {len(tabela)} por {len(tabela[0])}\n\n',
            f'Tabela Arma\n{tabela_arma}\nTamanho: {len(tabela_arma)}\n\n',
            f'Tabela Lugar\n{tabela_lugar}\nTamanho: {len(tabela_lugar)}\n\n',
            f'Tabela Suspeito\n{tabela_suspeito}\nTamanho: {len(tabela_suspeito)}\n\n'
        ])
        arquivo.writelines(linhas) 
