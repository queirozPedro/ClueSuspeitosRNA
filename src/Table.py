from Scene import *

def gerar_string_tabela(tabela):

    cartas = [
        "01 - Castical       ", "02 - Corda          ", "03 - Faca           ", "04 - Revolver       ",
        "05 - Cozinha        ", "06 - Hall           ", "07 - Sala de Estar  ", "08 - Sala de Jantar ",
        "09 - Spa            ", "10 - Green          ", "11 - Mustard        ", "12 - Peacock        ",
        "13 - Plum           ", "14 - Scarlet        ", "15 - White          "
    ]

    string = ''

    for i in range(15):
        string += f'|{cartas[i] }|'
        for j in range(4):
            if tabela[j][i] == 1 or tabela[j][i] == 0:
                string += ' '+ str(tabela[j][i])+ " |"
            else:
                string += str(tabela[j][i])+ " |"
                        
        string += '\n'
    return(string)

def gerar_string_tabela_detalhada(tabela, chance, crime):

    cartas = [
        "01 - Castical       ", "02 - Corda          ", "03 - Faca           ", "04 - Revolver       ",
        "05 - Cozinha        ", "06 - Hall           ", "07 - Sala de Estar  ", "08 - Sala de Jantar ",
        "09 - Spa            ", "10 - Green          ", "11 - Mustard        ", "12 - Peacock        ",
        "13 - Plum           ", "14 - Scarlet        ", "15 - White          "
    ]

    string = f'\nCrime: {crime}\nChance de corromper o  1: {chance[0]}\nChance de corromper o -1: {chance[1]}\n\n'

    for i in range(15):
        string += f'|{cartas[i] }|'
        for j in range(4):
            if tabela[j][i] == 1 or tabela[j][i] == 0:
                string += ' '+ str(tabela[j][i])+ " |"
            else:
                string += str(tabela[j][i])+ " |"
                        
        string += '\n'
    return(string)

