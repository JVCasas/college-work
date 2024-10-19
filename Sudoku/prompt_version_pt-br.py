import random

######## CLASSES ########

class sudoku:#Classe que gera um sudoku
    
    def __init__(self, dificuldade):
        self.dificuldade = dificuldade #Variável que recebe um valor de um a três para definir uma dificuldade do jogo a ser gerado sendo por padrão a dificuldade fácil
        self.jogoCompleto = self.geraSudokuCompleto() #Variável que recebe uma tabela completa (gabarito)
        self.puzzle = self.geraPuzzleSudoku(self.jogoCompleto, self.dificuldade) #Variável que recebe um jogo a partir da tabela completa

    def geraSudokuCompleto(self):#Função que cria uma tabela de sudoku completa (já resolvida)
        grade = [[0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]]#Matriz base para ser formatada 
        referenciaOpcoes = [1,2,3,4,5,6,7,8,9]#Referencia lista de números a serem inseridos em cada
        opcoes = referenciaOpcoes[:]

        def insereNumeroAleatorio(matriz, referencia, opc, linha=0, coluna=0):#Função que vai substituir os 0s da matriz por um número aleatório até finalizar a criação de uma tabela de sudoku completa valida
            
            if coluna >= 9:
                linha += 1
                coluna = 0
                opc = referencia[:]

            if linha >= 9:
                return False
            else:
                if self.validezOpcoes(linha, coluna, opc, matriz):
                    opcoesValidas = []
                    for n in opc:
                        if self.verificaNumero(n, linha, coluna, matriz):
                            opcoesValidas.append(n)
                    while self.verificaIncompletude(matriz):
                        if not opcoesValidas:
                            return True
                        else:
                            numero = random.choice(opcoesValidas)
                            matriz[linha][coluna] = numero
                            opc.remove(numero)
                            if insereNumeroAleatorio(matriz, referencia, opc, linha, coluna +1):
                                opcoesValidas.remove(numero)
                                opc.append(numero)
                                opc.sort()
                                matriz[linha][coluna] = 0
                    return False
                else:
                    return True

        insereNumeroAleatorio(grade, referenciaOpcoes, opcoes)

        return grade
    
    def geraPuzzleSudoku(self, matriz, dificuldade = 1):#Função que recebe uma tabela completa de sudoku e apaga números aleatórios de forma a gerar um jogo de sudoku de acordo com uma dificuldade informada.
        copiaResolucao = [linha[:] for linha in matriz]
        
        if dificuldade == 1:
            numerosRemovidos = random.choice(range(31,46))
        elif dificuldade == 2:
            numerosRemovidos = random.choice(range(46,61))
        else:
            numerosRemovidos = random.choice(range(61,76))


        def achaSolucao(matriz, linha = 0, coluna = 0, contador = 0):#Função que procura o número de soluções possíveis de um quebra-cabeça
            if coluna >= 9:
                linha += 1
                coluna = 0
            
            if linha >= 9:
                contador +=1
                return contador
            else:
                if matriz[linha][coluna] == 0:
                    for n in range(1,10):
                        if self.verificaNumero(n, linha, coluna, matriz):
                            matriz[linha][coluna] = n
                            contador += achaSolucao(matriz, linha, coluna + 1)
                    matriz[linha][coluna] = 0
                    return contador
                else:
                    contador += achaSolucao(matriz, linha, coluna + 1)
                    return contador
        
        while numerosRemovidos > 0:
            linha = random.choice(range(0,8))
            coluna = random.choice(range(0,8))
            resgate = copiaResolucao[linha][coluna]
            copiaResolucao[linha][coluna] = 0
            if achaSolucao(copiaResolucao) != 1:
                copiaResolucao[linha][coluna] = resgate
            else:
                numerosRemovidos -= 1
        
        return copiaResolucao

    @staticmethod
    def verificaIncompletude(matriz):#Função que verifica se a tabela esta totalmente preenchida
        for l in matriz:
            if 0 in l:
                return True
        return False

    @staticmethod
    def verificaLinha(numero, linha, matriz):#Função que verifica se um numero não esta inserido na linha
        if numero in matriz[linha]:
            return False
        else:
            return True

    @staticmethod
    def verificaColuna(numero, coluna, matriz):#Função que verifica se um numero não esta inserido na coluna
        col = []
        for lin in matriz:
            col.append(lin[coluna])
        if numero in col:
            return False
        return True

    @staticmethod
    def verificaSubMatriz(numero, linha, coluna, matriz):#Função que verifica se um numero não esta inserido no quadrante 3x3
        submatriz = []
        if linha < 3:
            if coluna < 3:
                for n in range(0,3):
                    submatriz.append(matriz[n][0:3])
            elif coluna < 6:
                for n in range(0,3):
                    submatriz.append(matriz[n][3:6])
            else:
                for n in range(0,3):
                    submatriz.append(matriz[n][6:9])
        elif linha < 6:
            if coluna < 3:
                for n in range(3,6):
                    submatriz.append(matriz[n][0:3])
            elif coluna < 6:
                for n in range(3,6):
                    submatriz.append(matriz[n][3:6])
            else:
                for n in range(3,6):
                    submatriz.append(matriz[n][6:9])
        else:
            if coluna < 3:
                for n in range(6,9):
                    submatriz.append(matriz[n][0:3])
            elif coluna < 6:
                for n in range(6,9):
                    submatriz.append(matriz[n][3:6])
            else:
                for n in range(6,9):
                    submatriz.append(matriz[n][6:9])
        
        if numero in (submatriz[0] + submatriz[1] + submatriz[2]):
            return False
        else:
            return True
    
    def verificaNumero(self, numero, linha, coluna, matriz):#Função que verifica se o número pode ser inserido na posição a ser preenchida
        if self.verificaLinha(numero, linha, matriz):
            if self.verificaColuna(numero, coluna, matriz):
                if self.verificaSubMatriz(numero, linha, coluna, matriz):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def validezOpcoes(self, linha, coluna, opcoes, matriz):#Função que verifica se há opções validas de números para serem inseridos na grade.
        if opcoes == []:
            return False
        
        for item in opcoes:
            if self.verificaNumero(item, linha, coluna, matriz):
                return True
            
class jogo:#Classe Responsavel por gerar uma partida e genrenciar as principais funcionalidades dela
    def __init__(self):
        self.nivel = self.menuDificuldade()
        self.game = sudoku(dificuldade = self.nivel)
        self.gabarito = self.game.jogoCompleto
        self.puzzle = self.game.puzzle
    
    @staticmethod
    def escreveSudoku(matriz):#Função que exibe a tabela de Sudoku formatada
        for l in range(0,9):
            if l == 3 or l == 6:
                    print('-' * 29)

            for n in range(0,9):
                
                if n == 3 or n == 6:
                    print('|', end = '')

                if matriz[l][n] == 0:
                    print(' . ', end = '')
                else:
                    print(f' {matriz[l][n]} ', end = '')
            print('')

    @staticmethod
    def menuDificuldade():#Função que exibe um menu de seleção de dificuldade
        print('Selecione uma dificuldade:\n[1] - Fácil\n[2] - Intermediário\n[3] - Díficil')
        while True:
            dificuldade = input('Dificuldade? -> ')
            if not dificuldade.isnumeric():
                print('Favor digite APENAS UM ÚNICO NÚMERO VALIDO!')
            else:
                dificuldade = int(dificuldade)
                if dificuldade in [1, 2, 3]:
                    return dificuldade
                else:
                    print('Favor digite APENAS UM ÚNICO NÚMERO VALIDO!')

    @staticmethod
    def selecaoNumerica(mensagemInput, inicio, fim):#Função que exibe um submenu que retorna um numero digitado pelo usuário que estaja dentro de um intervalo determinado.
        while True:
                valor = input(mensagemInput)
                if not valor.isnumeric():
                    print('Favor digite APENAS UM ÚNICO NÚMERO VALIDO!')
                else:
                    valor = int(valor)
                    if valor in range(inicio, fim):
                        return valor

    def menuPartida(self):#Função que exibe um menu de partida e que persiste até a finalização da mesma
        resposta = self.gabarito
        puzzle = self.puzzle
        copiaPuzzle = [linha[:] for linha in puzzle]

        while not puzzle == resposta:
            self.escreveSudoku(puzzle)
            linha = self.selecaoNumerica('Digite uma linha de 1 a 9: ', 1, 10) - 1
            coluna = self.selecaoNumerica('Digite uma coluna de 1 a 9: ', 1, 10) - 1
            if copiaPuzzle[linha][coluna] == 0:
                numero = self.selecaoNumerica('Digite um número de 1 a 9 (Digite 0 para apagar): ', 0, 10)
                if self.game.verificaNumero(numero, linha, coluna, puzzle):
                    puzzle[linha][coluna] = numero
                else:
                    print('O número não pode ser inserido nesta casa.')
            else:
                print('Não é possivel selecionar casas predefinidas!')
        print('Tabela Concluida!')
        self.escreveSudoku(resposta)

######## FUNÇÕES ########

def menuContinue():#Função de menu que pergunta ao final de cada partida se um novo jogo deve ser gerado.
    while True:
        entrada = input('Deseja continuar? [S/N] \n')
        if entrada not in ['S', 's', 'N', 'n']:
            print('Entrada Invalida!')
        else:
            if entrada in ['s', 'S']:
                return True
            else:
                return False

######## PROGRAMA ########

print(""" ________   __     __  _______    _________   __   ___   __     __ \n|  ______| |  |   | | |   __  \\  |   ____  | |  | /  /  |  |   | | \n|  |_____  |  |   | | |  |   \\ \\ |  |    | | |  |/  /   |  |   | | \n|______  | |  |   | | |  |   / / |  |    | | |   _  \\   |  |   | | \n_______| | |  |___| | |  |__/ /  |  |____| | |  | \\  \\  |  |___| | \n|________| |________| |______/   |_________| |__|  \\__\\ |________| \n""")
input('Pressione Enter para iniciar um novo jogo.')

continuacao = True

while continuacao:
    partida = jogo()
    partida.menuPartida()
    continuacao = menuContinue()