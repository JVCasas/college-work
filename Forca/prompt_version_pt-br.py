import random
import unicodedata
import time
import os

def verificaArquivo(alvo):#Função que verifica a existencia do arquivo do banco de dados, caso exista ele busca por incongruencias que não necessariamente geram excessões. A função retorna dois valores, uma messagem de erro ou de sucesso no formato string e um valor boleano que é falso, caso haja alguma incongruencia na biblioteca ou ela seja inexistente, e verdadeiro caso tudo esteja nos conformes.
    validez = True
    menssagem = ''
    try:
        arquivoVazio = False
        hashtagSobresalente = False
        hashtagAusente = False
        caracterInvalido = False
        linhaVazia = False
        palavrasSemTema = False
        temaSemPalavras = False

        with open(alvo, 'r', encoding = 'utf-8') as arquivo:
            if os.path.getsize(alvo) == 0:
                    arquivoVazio = True
            for linha in arquivo:
                hashtags = 0
                if linha == '\n':
                    linhaVazia = True
                for n in linha:
                    if n == '#':
                        hashtags += 1
                    if not n.isalpha() and n not in '- #,' and n != '\n':
                        caracterInvalido = True
                if hashtags > 1:
                    hashtagSobresalente = True
                if hashtags < 1 and not linhaVazia:
                    hashtagAusente = True
                if hashtags == 1:
                    verificador = linha.split('#')
                    if verificador [0] == '':
                        palavrasSemTema = True
                    if verificador[1] == '' or verificador[1] == '\n':
                        temaSemPalavras = True
        
        if arquivoVazio:
            menssagem += 'Erro: Arquivo "Biblio.txt" vazio.\n'
            validez = False
        if hashtagSobresalente:
            menssagem += 'Erro: Divisor de tema x palavras exedente.\n'
            validez = False
        if hashtagAusente:
            menssagem += 'Erro: Divisor de tema x palavras ausente.\n'
            validez = False
        if caracterInvalido:
            menssagem += 'Erro: Caracter invalido na bliblioteca.\n'
            validez = False
        if linhaVazia:
            menssagem += 'Erro: Linha vazia na biblioteca.\n'
            validez = False
        if temaSemPalavras:
            menssagem += 'Erro: Tema sem palavras.\n'
            validez = False
        if palavrasSemTema:
            menssagem += 'Erro: Palavras sem tema.\n'
            validez = False
        if validez:
            menssagem += 'Biblioteca OK'
        
        return menssagem, validez
                             
    except FileNotFoundError:
        validez = False
        menssagem += 'Erro: Arquivo "Biblio.txt" não encontrado.\n'
        return menssagem, validez


class jogo:#Classe que contem os intrumentos e execução de uma partida.
    
    def __init__(self, desafio):
        self.desafio = desafio #Variável que recebe um objeto desafio.
        self.tentativas = 5 #variavel que regula as tentativas do usuário.
        self.forcas = ["---------\n|/      |\n|\n|\n|\n|\n|\n --", "---------\n|/      |\n|       O\n|\n|\n|\n|\n --", "---------\n|/      |\n|       O\n|       ^\n|\n|\n|\n --", "---------\n|/      |\n|       O\n|       ^\n|       | \n|\n|\n --", "---------\n|/      |\n|       O\n|       ^\n|     / | \\ \n|       ^\n|\n --", "---------\n|/      |\n|       O\n|       ^\n|     / | \\ \n|       ^\n|     /   \\ \n --"] #Variável que guarda os elementos visuais do desenho da forca.
        self.segredo = desafio.geraSombra() #Variável que recebe uma lista análoga á palavra com underlines substituindo os caracteres, que será exibido visualmente ao usuário como referencia. os undererlines são substituidos pelos exatos caracteres que representam na palavra original conforme os acertos, tambem serve como um comparador final para definir a vitória.
    
    def gameStart(self):#Função que executa o jogo e testa a quantidade de tentativas restante da partida e mostra todos os elementos visuais necessários da partida os atualizando a cada tentativa e exibindo uma mensagem de vitória ou derrota ao concluir a palavra ou esgotar as tentativas.
        while True:
            if self.tentativas == 5:
                print(self.forcas[0])
                print(f'Tema: {self.desafio.tema}')
                print(f'Total de letras: {self.desafio.tamanho}')
                self.escrevePalavra(self.segredo)
                letra = self.validaTentativa()
                self.tentativas += self.verificaLetra(letra, self.desafio, self.segredo)
            if self.tentativas == 4:
                print(self.forcas[1])
                print(f'Tema: {self.desafio.tema}')
                print(f'Total de letras: {self.desafio.tamanho}')
                self.escrevePalavra(self.segredo)
                letra = self.validaTentativa()
                self.tentativas += self.verificaLetra(letra, self.desafio, self.segredo)
            if self.tentativas == 3:
                print(self.forcas[2])
                print(f'Tema: {self.desafio.tema}')
                print(f'Total de letras: {self.desafio.tamanho}')
                self.escrevePalavra(self.segredo)
                letra = self.validaTentativa()
                self.tentativas += self.verificaLetra(letra, self.desafio, self.segredo)
            if self.tentativas == 2:
                print(self.forcas[3])
                print(f'Tema: {self.desafio.tema}')
                print(f'Total de letras: {self.desafio.tamanho}')
                self.escrevePalavra(self.segredo)
                letra = self.validaTentativa()
                self.tentativas += self.verificaLetra(letra, self.desafio, self.segredo)
            if self.tentativas == 1:
                print(self.forcas[4])
                print(f'Tema: {self.desafio.tema}')
                print(f'Total de letras: {self.desafio.tamanho}')
                self.escrevePalavra(self.segredo)
                letra = self.validaTentativa()
                self.tentativas += self.verificaLetra(letra, self.desafio, self.segredo)
            if self.tentativas == 0:
                print(self.forcas[5])
                print(f'VOCÊ PERDEU!')
                print(f'A palavra era: {self.desafio.palavra}')
                break
            if ''.join(self.segredo) == self.desafio.palavra:#
                print('VOCÊ GANHOU!')
                print(f'A palavra era: {self.desafio.palavra}')
                break
    
    @staticmethod
    def validaTentativa():#Função que verifica o palpite, recebe de um input o palpite do jogador e verifica se o valor inserido pelo usuário é valido, após isso transforma o valor recebido num padrão usado pelo algoritimo de comparação, retornando esse caracter padronizado.
        while True:
            letra = input('Digite uma letra: ')
            if len(letra) > 1:
                print('DIGITE APENAS UMA LETRA!')
            if not letra.isalpha() and letra != '-':
                print('DIGITE APENAS LETRAS OU HÍFEN (-)!')
            else:
                break
        letra = letra.lower()
        letra = unicodedata.normalize("NFD", letra)
        letra = letra.encode("ascii", "ignore")
        letra = letra.decode("utf-8")
        return letra
    
    @staticmethod
    def verificaLetra(let, referencia, alvo):#Função que faz a comparação dos caracteres da palvra com o palpite do jogador, retornando valor 0 caso o palpite seja presente e fazendo a substituição dos underlines respectivos a esse palpite no elemento visual, caso não seja encontrada ela apenas retorna um valor -1, os valores retornados são somados ao número de tentativas.
        punicao = 0
        if let in referencia.referencia:
            for i in range(0, len(referencia.referencia)):
                if let == referencia.referencia[i]:
                    alvo[i] = referencia.palavra[i]
        else:
            punicao = -1
        return punicao

    @staticmethod
    def escrevePalavra(palavra):#Função que mostra visualmente variável self.segredo ao jogador.
        for n in palavra:
            print(f'{n}', end='')
        print('')


class desafio:#Classe que gera um objeto desafio, objeto com as propriedades relacionadas a palavra a ser adivinhada pelo usuário
    
    def __init__(self, tema, palavra):
        self.palavra = palavra #Recebe a palavra original que será usada para fins de comparação final e para gerar a sua versão usada pelo algoritimo de comparação.
        self.tema = tema #Recebe o tema da palavra.
        self.tamanho = len(palavra.replace(' ', '')) #Recebe o tamanho da palavra excluindo os espaços no caso de nomes compostos.
        self.referencia = self.geraReferencia(self.palavra) #Recebe a palavra tratada para comparação da sua composição com palpites.
    
    def geraSombra(self): #Função que gera uma lista analoga á palavra original para ser exibida como referencia, substitui os caracteres por underlines a exceção de espaços.
        self.sombra = ['_'] * len(self.palavra)
        for l in range(len(self.palavra)):
            if self.palavra[l] == ' ':
                self.sombra[l] = ' '
        return self.sombra
    
    @staticmethod
    def geraReferencia(palavra):#Função que pega como parametro um string, e a normaliza removendo acentos das letras e as pondo em sua forma minúscula (padrão de comparação) retornando a string após essa normalização.
        comparador = palavra.lower()
        comparador = unicodedata.normalize('NFD', comparador)
        comparador = comparador.encode("ascii", "ignore")
        comparador = comparador.decode("utf-8")
        return comparador

class bancoDeDados:#Classe responsável por gerar uma biblioteca a partir do arquivo txt, para a geração dos objetos desafio.
    
    def __init__(self, arquivo):
        self.banco, self.chavesBanco = self.geraBanco(arquivo)

    def geraDesafio(self):#Função que retorna um objeto desafio com a biblioteca e a lista gerada pela presente classe.
        a = random.choice(self.chavesBanco)
        b = random.choice(self.banco[a])
        return desafio(a, b)

    @staticmethod
    def geraBanco(banco):#Função que abre um arquivo txt, faz sua leitura e gera uma biblioteca e uma lista.A biblioteca tem como itens listas com palavras e como chaves desses itens os temas respectivos dessas listas. A lista é composta pelas chaves da biblioteca sendo usada para sortear o tema do desafio.
        with open(banco, 'r', encoding = "utf-8") as dados:
            dicionario = {}
            temas = []
            for linha in dados:
                tema, palavras = linha.split('#')
                palavras = palavras.replace('\n', '')
                palavras = palavras.split(',')
                dicionario[tema] = palavras
        
        for k in dicionario.keys():
            temas.append(k)
            
        return dicionario, temas
    
#Programa

print("""
    ---------
    |/      |
    |       
    |     JOGO
    |        DA
    |         FORCA
    |
    --""")
menssagem, validez = verificaArquivo('Biblio.txt')
if validez:
    print(menssagem)
    banco = bancoDeDados('Biblio.txt')
    while True:
        start = input('Deseja começar um novo jogo? [S/N] ').upper()
        if start not in 'SN':
            print('Digite apenas S ou N!')
        if len(start) > 1:
            print('Digite uma opção!')
        if start == "S":
            palavra = banco.geraDesafio()
            game = jogo(palavra)
            game.gameStart()
        if start == "N":
                print('Encerrando o jogo!')
                time.sleep(3)
                exit()
else:
    print(menssagem)
    print('Encerrando o programa...')
    time.sleep(5)
    exit()

#Disposições sobre o arquivo "Biblio.txt": o arquivo não pode estar vazio, assim como não pode ter linhas em branco, temas sem uma lista de palavras, listas de palavras sem tema, caracteres não alfabeticos com exceção do hashtag, virgulas e espaço, cada linha possuí um unico tema e sua respectiva lista de palavras, o nome do tema é anunciado primeiro, sendo sucedido por um # que age como separador entre o nome do tema e a lista de palavras, devendo haver o # como separador. As palvras de um tema devem estar separadas por virgula sem serem precedidas ou sucedidas por espaço.

#Disposições sobre o funcionamento geral do programa - o programa irá capturar as infomações do arquivo txt e gerará um objeto que funcionará como um banco de dados, esse objeto gerará um outro objeto que será a palavra usada no jogo juntamente com o seu tema e outras coisas relacionadas a ela, sendo escolhido aleatoriamente o tema e depois uma das palavras do tema. Feito isso esse objeto é fornecido como parametro para um outro objeto, que será responsável pela execução de uma partida, sendo um novo objeto dessa classe gerado sempre que se deseja uma nova partida. O programa se encerrará sempre que houver um erro conhecido na geração do banco de dados informando os erros existentes caso haja mais de um. Não havendo erros o programa inicia uma pergunta, em um loop, se um novo jogo deve ser iniciado, a pergunta só é possivel ser respondida com as letras "s" pra sim e "n" para não, caso a resposta seja "s", uma partida é executada e ao final da partida é exibida a mensagem de vitória ou derrota, o loop reinicia fazendo a pergunta e gerando novas partidas enquanto o usuário responder sim, ao responder "n" o programa exibe uma mensagem de encerramento e por fim é encerrado.