from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier

from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt
from matplotlib_venn.layout.venn3 import DefaultLayoutAlgorithm

from Scene import *
from save_to_file import *
from Table import *

def gerar_dados(dados, chance):
    '''
    Função responsável por gerar a base de dados usada no treino.
    Recebe a quantidade de dados que devem ser gerados, a chance do
    número 1 ser corrompido e a chance do número -1 ser corrompido.
    Retorna X seguido de y para cada tipo de carta.
    '''
    # Os itens nomeados com X serão as tabelas com 0, 1 e -1 referentes aos jogadores.
    itens_X = [[],[],[]]
    # Os itens nomeados com y serão as respostas dos crimes.
    itens_y = [[],[],[]]

    # Base de dados
    for _ in range(dados):
        # Vou criar o crime e a tabela
        crime, tabela = criar_cenario(chance)
        # Distribuir o crime em seu respectivos y
        itens_y[0].append(crime[0])
        itens_y[1].append(crime[1])
        itens_y[2].append(crime[2])

        # Divide um array para cada tipo de carta
        # Um array com as informações de armas
        tabela_aux = []
        for i in range(4):
            for j in range(4):
                tabela_aux.append(tabela[i][j])
        itens_X[0].append(tabela_aux)
        # Um array com as informações de lugares
        tabela_aux = []
        for i in range(4):
            for j in range(4,9):
                tabela_aux.append(tabela[i][j])
        itens_X[1].append(tabela_aux)
        # Um array com as informações de suspeitos
        tabela_aux = []
        for i in range(4):
            for j in range(9,15):
                tabela_aux.append(tabela[i][j])
        itens_X[2].append(tabela_aux)

    return (itens_X, itens_y)


def definir_param_grid():
    '''
    Função que retorna os param_grid de arma, lugar e suspeito
    '''

    """
    Os param_grid são dicionários de diferentes combinações que 
    deseja testar no modelo.
    """
    param_grid = []
    # param_grid_arma -> 0
    # param_grid_lugar -> 1
    # param_grid_suspeito -> 2
    param_grid.append({
        'hidden_layer_sizes': [(16, 8), (8, 4), (8,), (4,)], 
        'activation': ['identity', 'logistic'],
        'solver': ['adam'],
        'learning_rate': ['constant', 'adaptive'],
    })
    param_grid.append({
        'hidden_layer_sizes': [(20, 10), (10, 5), (10,), (5,)], 
        'activation': ['identity', 'logistic'],
        'solver': ['adam'],
        'learning_rate': ['constant', 'adaptive'],
    })
    param_grid.append({
        'hidden_layer_sizes': [(24, 12), (12, 6), (12,), (6,)],
        'activation': ['identity', 'logistic'],
        'solver': ['adam'],
        'learning_rate': ['constant', 'adaptive'],
    })
    return (param_grid)


def definir_grid_search(clf, param_grid):
    '''
    Define os grid_search
    '''
    grid_search = []
    grid_search.append(GridSearchCV(estimator=clf[0], param_grid=param_grid[0], n_jobs=-1, cv=3))
    grid_search.append(GridSearchCV(estimator=clf[1], param_grid=param_grid[1], n_jobs=-1, cv=3))
    grid_search.append(GridSearchCV(estimator=clf[2], param_grid=param_grid[2], n_jobs=-1, cv=3))

    return(grid_search)


def print_resultados(dados, testes, chance, resultados):
    '''
    Recebe os dados do treino e exibe um relátorio geral
    '''
    string = [
        f"\nCom um total de {dados} dados de jogos\n",
        f"Para um total de {testes} testes automáticos e aleatórios\n",
        f"Com chance de {chance[0]}% de Corromper o 1\n",
        f"Com chance de {chance[1]}% de Corromer o -1\n",
        f"Resultado\n",
        f"Acertou tudo: {resultados[0]} ou {(resultados[0]/testes)*100:.2f}%\n",
        f"Acertou apenas a Arma: {resultados[1]} ou {(resultados[1]/testes)*100:.2f}%\n",
        f"Acertou apenas o Lugar: {resultados[2]} ou {(resultados[2]/testes)*100:.2f}%\n",
        f"Acertou apenas o Suspeito: {resultados[3]} ou {(resultados[3]/testes)*100:.2f}%\n",
        f"Acertou apenas a Arma e o Lugar: {resultados[4]} ou {(resultados[4]/testes)*100:.2f}%\n",
        f"Acertou apenas o Lugar e o Suspeito: {resultados[5]} ou {(resultados[5]/testes)*100:.2f}%\n",
        f"Acertou apenas o Suspeito e a Arma: {resultados[6]} ou {(resultados[6]/testes)*100:.2f}%\n",
        f"Errou tudo: {resultados[7]} ou {(resultados[7]/testes)*100:.2f}%\n"
    ]
    print("".join(string))


def gerar_diagrama_venn(dados, testes, chance, resultados):
    '''
    Função que gera um diagrama de Venn com base nas informações do treino
    '''

    subsets = [
            round((resultados[1]/testes)*100, 2), 
            round((resultados[2]/testes)*100, 2), 
            round((resultados[4]/testes)*100, 2), 
            round((resultados[3]/testes)*100, 2),
            round((resultados[6]/testes)*100, 2), 
            round((resultados[5]/testes)*100, 2),
            round((resultados[0]/testes)*100, 2)
    ]

    venn3(subsets=subsets, 
        set_labels=("Arma", "Lugar", "Suspeito"),
        set_colors=("orange", "blue", "red"),
        layout_algorithm=DefaultLayoutAlgorithm(fixed_subset_sizes=(1,1,1,1,1,1,1)))
    
    venn3_circles(subsets=(subsets), layout_algorithm=DefaultLayoutAlgorithm(fixed_subset_sizes=(1,1,1,1,1,1,1)))
    
    plt.title(f"Resultado do treino (em %)")
    string = [
        f"Total de dados: {dados}\n",
        f"Total de testes: {testes}\n",
        f"Corrupção de 1 e -1: {chance[0]}%, {chance[1]}%",
    ]
    plt.text(-1, -0.8, "".join(string), fontsize=10)
    plt.text(0.5, -0.5, f"Erros: {round((resultados[7]/testes)*100, 2)}", fontsize=12)
    plt.savefig(f'{dados}_dados_e_{testes}_testes_{chance[0]}%_para_1_e_{chance[1]}%_para_-1')
    plt.clf()


def realizar_testes(testes, chance, grid_search):
    '''
    Função que faz os testes e retorna os resultados
    '''

    resultados = [0, 0, 0, 0, 0, 0, 0, 0]
    """
    resultados[0] os que acertaram tudo (acertos)
    resultados[1] os que acertaram apenas arma (acertos_arma)
    resultados[2] os que acertaram apenas lugar (acertos_lugar)
    resultados[3] os que acertaram apenas suspeito (acertos_suspeito)
    resultados[4] os que acertaram apenas arma e lugar (acertos_arma_lugar)
    resultados[5] os que acertaram apenas lugar e suspeito (acertos_lugar_suspeito)
    resultados[6] os que acertaram apenas suspeito e arma (acertos_suspeito_arma)
    resultados[7] os que erraram tudo (erros)
    """
    
    # Realiza os testes
    for _ in range(testes):
        crime, tabela = criar_cenario(chance)

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

        palpite_arma = (grid_search[0].predict([tabela_arma]))
        palpite_lugar = (grid_search[1].predict([tabela_lugar]))
        palpite_suspeito = (grid_search[2].predict([tabela_suspeito]))

        if crime[0] == palpite_arma: # Arma
            if crime[1] == palpite_lugar: # Arma e Lugar
                if crime[2] == palpite_suspeito: # Arma, lugar e suspeito
                    resultados[0] += 1
                else:
                    resultados[4] += 1
            elif crime[2] == palpite_suspeito: # Arma e suspeito
                resultados[6] += 1
            else:
                resultados[1] += 1
        elif crime[1] == palpite_lugar: # Lugar
            if crime[2] == palpite_suspeito: # Lugar e suspeito
                resultados[5] += 1
            else:
                resultados[2] += 1
        elif crime[2] == palpite_suspeito: # Suspeito
            resultados[3] += 1
        else:
            resultados[7] += 1

    return (resultados)


def mostrar_parametros(grid_search):
    '''
    Recebe os grid_search e retorna um relatório com as melhores combinações de parâmetros para esse treino
    '''
    melhores_parametros = [
        f"{grid_search[0].best_params_}\n",
        f"{grid_search[1].best_params_}\n",
        f"{grid_search[2].best_params_}"
    ]
    return melhores_parametros


def treinar(dados, testes, chance):
    '''
    Função que faz os treinamentos e testes com base nas chances de corromper 1 e -1.
    Recebe a quantidade de dados, a qualidade de testes que serão feitos com base
    neles, e as chances de corromper 1 e -1.
    Retorna um array de resultados e uma string com informações sobre melhores 
    combinações de parâmetros.
    '''
    # Definir os modelos
    clf = []
    # clf_arma -> 0
    # clf_lugar -> 1
    # clf_suspeito -> 2
    for _ in range(3):
        clf.append(MLPClassifier(max_iter=1000000000))

    # Definir os param_grid
    param_grid = definir_param_grid()
    
    # Definir os grid_search
    grid_search = definir_grid_search(clf, param_grid)
    
    # Gerar os Dados do treino
    X_train, y_train = gerar_dados(dados, chance)

    # Realizar os Ajustes
    grid_search[0].fit(X_train[0], y_train[0])
    print("\nAjustou a Arma")
    grid_search[1].fit(X_train[1], y_train[1])
    print("Ajustou o Lugar")
    grid_search[2].fit(X_train[2], y_train[2]) 
    print("Ajustou o Suspeito\n")

    # Coleta as melhores combinações de parâmetros para cada tipo de carta
    melhores_parametros = mostrar_parametros(grid_search)

    # Faz os testes
    resultados = realizar_testes(testes, chance, grid_search)
    
    # Retorna os resultados dos testes e os melhores parametros para cada tipo carta 
    return resultados, melhores_parametros 


def treinar_uma_vez():
    '''
    Coleta as informações e inicia um treino 
    '''
    # Coleta os caracteristicas do treino
    print(f"\n\nCaracteristicas do Treino Unico")
    dados = int(input("Quantidade de Dados do Treinamento: "))
    testes = int(input("Quantidade de Testes: "))
    print(f"Informações adicionais")
    chance = [0, 0]
    chance[0] = int(input("Chance de Corromper o 1: "))
    chance[1] = int(input("Chance de Corromper o -1: "))

    # Faz os treinos e retorna os resultados
    resultados, melhores_parametros = treinar(dados, testes, chance)
    # Exibe quais os melhores parâmetros neste treino
    print("".join(melhores_parametros))
    # Exibe o resultado no terminal
    print_resultados(dados, testes, chance, resultados)
    # Gera diagrama de Venn com base no resultado
    gerar_diagrama_venn(dados, testes, chance, resultados)


def treinar_100_vezes():
    '''
    Coleta as informações e inicia 100 treinos, onde a corrupção dos treinos começa
    em um e vai até 100
    '''
    # Coleta os caracteristicas do treino
    print("\n\nTreinar 100 vezes")
    dados = int(input("Quantidade de dados para cada treinamento: "))
    testes = int(input("Quantidade de testes para cada treinamento: "))
    intervalo_analise = int(input("Intervalo entre as analises: "))
    
    param_cont = [
        [0, 0, 0, 0, 0, 0],   
        [0, 0, 0, 0, 0, 0],   
        [0, 0, 0, 0, 0, 0]   
    ]    
    marco = 0
    # 'hidden_layer_sizes': [(16, 8), (8, 4), (8,), (4,)], 
    # 'activation': ['identity', 'logistic'],
    # 'solver': ['adam', 'lbfgs'],
    # 'learning_rate': ['constant', 'adaptive'],

    for i in range(1, 101):
        resultados, melhores_parametros = treinar(dados, testes, [i, i])
        for j in range(3):
            if 'identity' in melhores_parametros[j]:
                param_cont[j][0] += 1
            if 'logistic' in melhores_parametros[j]:
                param_cont[j][1] += 1
            if 'adam' in melhores_parametros[j]:
                param_cont[j][2] += 1
            if 'lbfgs' in melhores_parametros[j]:
                param_cont[j][3] += 1
            if 'constant' in melhores_parametros[j]:
                param_cont[j][4] += 1
            if 'adaptive' in melhores_parametros[j]:
                param_cont[j][5] += 1
            
        if i%intervalo_analise == 0:
            string = f"\nNo intervalo de {marco if marco != 0 else 1} até {i} ocorreram:\n"
            for j in range(3):
                string_aux = [
                    f"\nPara Arma:\n",
                    f"Activation identity: {param_cont[j][0]}\n",
                    f"Activation logistic: {param_cont[j][1]}\n",
                    f"Solver adam: {param_cont[j][2]}\n",
                    f"Solver lbfgs: {param_cont[j][3]}\n",
                    f"Learning_rate constant: {param_cont[j][4]}\n",
                    f"Learning_rate adaptive: {param_cont[j][5]}\n"    
                ]
                string += ''.join(string_aux)
            print("".join(string))
            for i in range(len(param_cont)):
                param_cont[i] = [0] * len(param_cont[i])  
            marco += intervalo_analise


def main():
    opcoes = {
        "1": ("Treinar uma vez", treinar_uma_vez),
        "2": ("Treinar 100 vezes", treinar_100_vezes),
        "3": ("Gerar tabelas TXT", gerar_tabelas_txt),
        "4": ("Gerar tabelas LaTeX", gerar_tabelas_tex),
    }

    print("\n=== Clue Suspeitos RNA ===")
    for chave, (nome, _) in opcoes.items():
        print(f"{chave}. {nome}")

    escolha = input("\nEscolha uma opção: ").strip()

    if escolha in opcoes:
        opcoes[escolha][1]()
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()