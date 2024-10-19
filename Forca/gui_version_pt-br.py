from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import Message
from PIL import Image, ImageTk
import random
import unicodedata
import os

root = Tk()

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

class desafio:#Classe que gera um objeto desafio, objeto com as propriedades relacionadas a palavra a ser adivinhada pelo usuário
    
    def __init__(self, tema, palavra):
        self.palavra = palavra #Recebe a palavra original que será usada para fins de comparação final e para gerar a sua versão usada pelo algoritimo de comparação.
        self.tema = tema #Recebe o tema da palavra.
        self.tamanho = len(palavra.replace(' ', '')) #Recebe o tamanho da palavra excluindo os espaços no caso de nomes compostos.
        self.referencia = self.geraReferencia(self.palavra) #Recebe a palavra tratada para comparação da sua composição com palpites.
        self.sombra = self.geraSombra()
        self.erros = list()

    def geraSombra(self): #Função que gera uma lista analoga á palavra original para ser editada de acordo com os acertos como referencia, substitui os caracteres por underlines a exceção de espaços.
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

class funcoes(): #Classe responsável pelas funções
        
    def Sair(self):# Função que fecha o jogo
        self.root.destroy()

    def geraQuadrados(self): #Função que gera um elemento visual analogo à palavra original para ser exibida como referencia, substitui os caracteres por quadrados a exceção de espaços.
        x0 = 25
        x1 = 45
        self.quadrados = list()
        self.coordenada = list()
        for l in self.desafio.palavra:
            if l != ' ':
                self.quadrados.append(self.canvasPalavra.create_rectangle(x0, 25, x1, 45, fill = 'yellow'))
                self.coordenada.append(x0)
            x0 += 30
            x1 += 30
            

    def validaTentativa(self):#Função que verifica o palpite, recebe de um input o palpite do jogador e verifica se o valor inserido pelo usuário é valido, após isso transforma o valor recebido num padrão usado pelo algoritimo de comparação, retornando esse caracter padronizado.
        letra = self.entradaLetra.get()
        if len(letra) > 1:
            self.rootMSG = Tk()
            self.rootMSG.withdraw()
            self.rootMSG.after(2000, self.rootMSG.destroy)
            Message(master = self.rootMSG, message = 'DIGITE APENAS UMA LETRA!').show()            
        elif not letra.isalpha() and letra != '-':
            self.rootMSG = Tk()
            self.rootMSG.withdraw()
            self.rootMSG.after(2000, self.rootMSG.destroy)
            Message(master = self.rootMSG, message = 'DIGITE APENAS LETRAS OU HÍFEN (-)!').show()
        elif letra in self.desafio.sombra:
            self.rootMSG = Tk()
            self.rootMSG.withdraw()
            self.rootMSG.after(2000, self.rootMSG.destroy)
            Message(master = self.rootMSG, message = 'CARACTER JÁ ESCOLHIDO!').show()
        else:
            letra = letra.lower()
            letra = unicodedata.normalize("NFD", letra)
            letra = letra.encode("ascii", "ignore")
            letra = letra.decode("utf-8")
            self.entradaLetra.delete(0, END)
            self.tentativas += self.verificaLetra(letra, self.desafio, self.desafio.sombra)
            if self.verificaLetra(letra, self.desafio, self.desafio.sombra) == -1:
                self.desafio.erros.append(letra)
                ', '.join(str(self.desafio.erros))
            print(self.desafio.sombra)

            print(self.desafio.erros)
        self.entradaLetra.delete(0, END)

    @staticmethod
    def verificaLetra(let, referencia, alvo1):#Função que faz a comparação dos caracteres da palvra com o palpite do jogador, retornando valor 0 caso o palpite seja presente e fazendo a substituição dos underlines respectivos a esse palpite no elemento visual, caso não seja encontrada ela apenas retorna um valor -1, os valores retornados são somados ao número de tentativas.
        punicao = 0
        if let in referencia.referencia:
            for i in range(0, len(referencia.referencia)):
                if let == referencia.referencia[i]:
                    alvo1[i] = referencia.palavra[i]
                    
        else:
            punicao = -1
        return punicao

    def novoJogo(self, desafio):#Função que cria um novo jogo, colocando variaveis em um estado inicial de acordo com o objeto desafio
        self.desafio = desafio #Variável que recebe um objeto desafio.
        self.tentativas = 5 #variavel que regula as tentativas do usuário.

        
        # Elemento visual do tema da partida
        self.labelTema =  Label(self.framePalavra, text = 'Tema:'+ self.desafio.tema, fg ='black')
        self.labelTema.place(x = 330, y = 50)
        self.mudaForca()
        self.geraQuadrados()
    
    def mudaForca(self):#função que muda o desenho da forca a cada tentativa ou novo jogo.
        forca0 = ImageTk.PhotoImage(Image.open('Forca/IMG/Forca0.jpg'))
        forca1 = ImageTk.PhotoImage(Image.open('Forca/IMG/Forca1.jpg'))
        forca2 = ImageTk.PhotoImage(Image.open('Forca/IMG/Forca2.jpg'))
        forca3 = ImageTk.PhotoImage(Image.open('Forca/IMG/Forca3.jpg'))
        forca4 = ImageTk.PhotoImage(Image.open('Forca/IMG/Forca4.jpg'))
        forca5 = ImageTk.PhotoImage(Image.open('Forca/IMG/Forca5.jpg'))
        
        if self.tentativas == 5:
            self.forca = forca0
        if self.tentativas == 4:
            self.forca = forca1
        if self.tentativas == 3:
            self.forca = forca2
        if self.tentativas == 2:
            self.forca = forca3
        if self.tentativas == 1:
            self.forca = forca4
        if self.tentativas == 0:
            self.forca = forca5
        
        self.imagemForca = self.canvas.create_image(0, 0, anchor = NW, image = self.forca)
    
    def mudaPalavra(self):#Função que revela as letra na palavra
        for n in range(len(self.desafio.sombra)):
            if self.desafio.sombra[n] not in ' _':
                self.quadrados[n] = Label(self.canvasPalavra, text = self.desafio.palavra[n])
                self.quadrados[n].place(x = self.coordenada[n], y = 25, width = 20, height = 20)

    def restart(self):#Função que reinicia o jogo
        self.resetFrames()
        self.novoJogo(self.banco.geraDesafio())

    def mudaErros(self):#Função que muda a exibição da caixa de erros
        self.caixaErros.destroy()
        self.caixaErros = Label(self.frameErros, text = self.desafio.erros)
        self.caixaErros.place(relx = 0.05, rely = 0.1, relheight = 0.8, relwidth = 0.9)

    def verificaVitória(self):#Função que verifica o encerramento do jogo
        if self.tentativas == 0:
                self.frameMenu.destroy()
                self.frameMenu = Frame(self.root, highlightbackground = "#759fe6", highlightthickness = 2)
                self.frameMenu.place(y = 300, x = 450, width = 250, height = 175)
                self.labelVitoria = Label(self.frameMenu, text = 'Você perdeu!', fg = 'Red')
                self.labelVitoria.pack()
                self.botãoNovoJogoMF = Button(self.frameMenu, text = 'Novo Jogo', command = self.restart, border = 2.5, bg = "#187db2", fg = "#dddddd", font = ('verdana', 8, 'bold'), activebackground = '#188ecb', activeforeground = 'white')
                self.botãoNovoJogoMF.place(x = 155, y = 120, width = 70, height = 25)
                self.botãoEncerrar = Button(self.frameMenu, text = 'Sair', command = self.Sair, border = 2.5, bg = "#187db2", fg = "#dddddd", font = ('verdana', 8, 'bold'), activebackground = '#188ecb', activeforeground = 'white')
                self.botãoEncerrar.place(x = 10, y = 120, width = 70, height = 25)
                
        if ''.join(self.desafio.sombra) == self.desafio.palavra:
                self.frameMenu.destroy()
                self.frameMenu = Frame(self.root, highlightbackground = "#759fe6", highlightthickness = 2)
                self.frameMenu.place(y = 300, x = 450, width = 250, height = 175)
                self.labelVitoria = Label(self.frameMenu, text = 'Você Venceu!', fg = 'Green')
                self.labelVitoria.pack()
                self.botãoNovoJogoMF = Button(self.frameMenu, text = 'Novo Jogo', command = self.restart, border = 2.5, bg = "#187db2", fg = "#dddddd", font = ('verdana', 8, 'bold'), activebackground = '#188ecb', activeforeground = 'white')
                self.botãoNovoJogoMF.place(x = 155, y = 120, width = 70, height = 25)
                self.botãoEncerrar = Button(self.frameMenu, text = 'Sair', command = self.Sair, border = 2.5, bg = "#187db2", fg = "#dddddd", font = ('verdana', 8, 'bold'), activebackground = '#188ecb', activeforeground = 'white')
                self.botãoEncerrar.place(x = 10, y = 120, width = 70, height = 25)

    def resetFrames(self):#Função que reinicia os frames do jogo
        self.frameErros.destroy()
        self.frameForca.destroy()
        self.frameMenu.destroy()
        self.framePalavra.destroy()
        self.frames()
        self.widgetsFrameForca()
        self.widgetsFrameMenu()
        self.widgetsFramePalavra()
        self.widgetsFrameErros()

    def tentativa(self):#Função que realiza uma tentativa
        self.validaTentativa()
        self.mudaForca()
        self.mudaErros()
        self.mudaPalavra()
        self.verificaVitória()

class aplicação(desafio, funcoes):#classe que estrutura a interface gráfica e atribui as funções a cada uma de suas partes
    
    def __init__(self):
        self.root = root
        self.tela()
        self.frames()
        self.widgetsFrameForca()
        self.widgetsFrameMenu()
        self.widgetsFramePalavra()
        self.widgetsFrameErros()
        self.telaInicial()
        root.mainloop()

    def tela(self):#Função que define a janela da interface gráfica
        self.root.title('Jogo da Forca')
        self.root.configure(background ="#dfe3ee")
        self.root.geometry('1000x500')
        self.root.resizable(False, False)

    def frames(self):#Define as divisões (frames) na tela do jogo
        self.frameForca = Frame(self.root)
        self.frameForca.place(y = 25, x = 725, width = 250, height = 450)
        self.frameErros = Frame(self.root, bg = '#ffffff', highlightbackground = "#759fe6", highlightthickness = 2)
        self.frameErros.place(y = 300, x = 25, width = 400, height = 175)
        self.framePalavra = Frame(self.root, highlightthickness = 2)
        self.framePalavra.place(y = 25, x = 25, width = 675, height = 250)
        self.frameMenu = Frame(self.root, highlightbackground = "#759fe6", highlightthickness = 2)
        self.frameMenu.place(y = 300, x = 450, width = 250, height = 175)

    def widgetsFrameForca(self):#Função que exibe o desenho da forca
        self.canvas = Canvas(self.frameForca, bg = 'white', width = 250, height = 450)
        self.canvas.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)
        self.forca = ImageTk.PhotoImage(Image.open('Forca/IMG/Forca0.jpg'))
        self.imagemForca = self.canvas.create_image(0, 0, anchor = NW, image = self.forca)
        
    
    def widgetsFrameMenu(self):#Função que define os widgets da Menu onde o usuário faz suas tentativas.
        self.entradaLetra = Entry(self.frameMenu, bg = "#dddddd", fg = "Black")
        self.entradaLetra.place(x = 125, y = 120, height = 20, width = 20)
        self.labelTentativa = Label(self.frameMenu, text = 'Insira sua tentativa:', fg ='black')
        self.labelTentativa.place(x = 10, y = 120, height = 20)
        self.botãoTentativa = Button(self.frameMenu, text = 'Tentar', command = self.tentativa, border = 2.5, bg = "#187db2", fg = "#dddddd", font = ('verdana', 8, 'bold'), activebackground = '#188ecb', activeforeground = 'white')
        self.botãoTentativa.place(x = 155, y = 120, width = 55, height = 20)
    
    def widgetsFramePalavra(self):#Função que cria os elementos dentro do frame framePalavra
        self.canvasPalavra = Canvas(self.framePalavra, bg = 'blue')
        self.canvasPalavra.place(relx = 0, rely = 0.5, relwidth = 1, relheight = 0.5)
    
    def widgetsFrameErros(self):#Função que cria os elementos dentro do frame caixaErros
        self.caixaErros = Label(self.frameErros, text = '')
        self.caixaErros.place(relx = 0.05, rely = 0.1, relheight = 0.8, relwidth = 0.9)
        
    
    def telaInicial(self):#Função que gera uma tela inicial de menu variável, onde no caso de se apresentar erro ou ausência do arquivo Biblio.txt exibirá uma menssagem relatando os erros e um botão que encerra o programa, caso contrário será exibido um botão que redireciona para tela de jogo e uma menssagem de que o arquivo txt está ok, além do botão que encerra o programa.
        
        def mudarTela():
            self.frameInicial.destroy()
            self.novoJogo(self.banco.geraDesafio())
        
        menssagem, validez = verificaArquivo('Forca/Biblio.txt')

        self.frameInicial = Frame(self.root)
        self.frameInicial.place(y = 0, x = 0, width = 1000, height = 500)
        
        self.botãoSairMP = Button(self.frameInicial, text = 'Sair', command = self.Sair, border = 2.5, bg = "#187db2", fg = "#dddddd", font = ('verdana', 10, 'bold'), activebackground = '#188ecb', activeforeground = 'white')
        self.botãoSairMP.place(x = 450, y = 400, width = 100, height = 30)

        self.canvasThumb = Canvas(self.frameInicial, bg = 'white', width = 800, height = 280)
        self.canvasThumb.place(x = 100, y = 50)
        self.imgThumb = ImageTk.PhotoImage(Image.open('IMG/thumb_pt-br.png'))
        self.thumb = self.canvasThumb.create_image(0, 0, anchor = NW, image = self.imgThumb)

        
        if validez:
            self.botãoNovoJogoMP = Button(self.frameInicial, text = 'Novo Jogo', command = mudarTela, border = 2.5, bg = "#187db2", fg = "#dddddd", font = ('verdana', 8, 'bold'), activebackground = '#188ecb', activeforeground = 'white')
            self.botãoNovoJogoMP.place(x = 450, y = 350, width = 100, height = 30)
            self.labelArquivoOK = Label(self.frameInicial, text = menssagem, font = ('verdana', 8, 'bold'), fg = 'green')
            self.labelArquivoOK.place(x = 350, y = 450, width = 300)
            self.banco = bancoDeDados('Forca/Biblio.txt')
        else:
            self.labelErroArquivo = Label(self.frameInicial, text = menssagem, font = ('verdana', 8, 'bold'), fg = 'red')
            self.labelErroArquivo.place(x = 350, y = 300, width = 300)


aplicação()