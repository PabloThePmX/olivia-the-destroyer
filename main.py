import pygame
import random
import os
from tkinter import simpledialog
from balao import draw_speech_bubble as balaoSonho

pygame.init()

relogio = pygame.time.Clock()
icone  = pygame.image.load("recursos/icone.ico")
iron = pygame.image.load("recursos/monitor.png") # monitor
fundo = pygame.image.load("recursos/fundo.jpg")
fundoStart = pygame.image.load("recursos/fundoStart.png")
fundoDead = pygame.image.load("recursos/fundoDead.png")

fastOlivia = pygame.image.load("recursos/ataque.png") # olivia
oliviaDeRoupa = pygame.image.load("recursos/oliviadeRoupa.png")
kiara = pygame.image.load("recursos/kiara_nanando.png")
helloKitty = pygame.image.load("recursos/helloKitty.png")
tamanho = (800,600)
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Olivia, the Destroyer")
pygame.display.set_icon(icone)
ataqueNormal = pygame.mixer.Sound("recursos/ataqueNormal.mp3")
# explosaoSound = pygame.mixer.Sound("recursos/explosao.wav")
fonte = pygame.font.SysFont("futura",28)
fonteStart = pygame.font.SysFont("futura",110)
fonteMorte = pygame.font.SysFont("futura",150)
pygame.mixer.music.load("recursos/soundtrack.mp3")

branco = (255,255,255)
preto = (0, 0 ,0 )
vermelho = (255,0,0)


def jogar(nome):
    pygame.mixer.Sound.play(ataqueNormal)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 400
    posicaoYPersona = 500
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXfastOlivia = 400
    posicaoYfastOlivia = -240
    posicaoXoliviaDeRoupinha = 200
    posicaoYoliviaDeRoupinha = -240
    velocidadefastOlivia = 1
    pontos = 0
    larguraPersona = 82
    alturaPersona = 100
    larguafastOlivia  = 150
    alturafastOlivia  = 266
    larguraoliviaDeRoupinha = 160
    alturaoliviaDeRoupinha = 284
    dificuldade  = 20
    sizeBalao = 35

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0

        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 50 :
            posicaoXPersona = 60
        elif posicaoXPersona > 650:
            posicaoXPersona = 640
            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        tela.blit(iron, (posicaoXPersona, posicaoYPersona) )
        tela.blit(kiara, (300, 200))
        tela.blit(helloKitty, (360, 235))

        # coloca o balao de soninho da kiara
        balaoSonho(tela, "ZzZzZZ", preto, branco, (340, 220), sizeBalao)
        
        posicaoYfastOlivia = posicaoYfastOlivia + velocidadefastOlivia
        posicaoYoliviaDeRoupinha = posicaoYoliviaDeRoupinha + velocidadefastOlivia
        
        if posicaoYfastOlivia > 600 and posicaoYoliviaDeRoupinha > 600:
            posicaoYfastOlivia = -240
            posicaoYoliviaDeRoupinha = -240
            pontos = pontos + 1
            velocidadefastOlivia = velocidadefastOlivia + 1
            posicaoXfastOlivia = random.randint(10,750)      
            posicaoXoliviaDeRoupinha = random.randint(10,750)      
            pygame.mixer.Sound.play(ataqueNormal)
            sizeBalao = 35 if sizeBalao == 20 else 20
            
            
        tela.blit(fastOlivia, (posicaoXfastOlivia, posicaoYfastOlivia) )
        tela.blit(oliviaDeRoupa, (posicaoXoliviaDeRoupinha, posicaoYoliviaDeRoupinha))
        
        texto = fonte.render(nome+" - Pontos: "+str(pontos), True, vermelho)
        tela.blit(texto, (10,10))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsfastOliviaX = list(range(posicaoXfastOlivia, posicaoXfastOlivia + larguafastOlivia))
        pixelsfastOliviaY = list(range(posicaoYfastOlivia, posicaoYfastOlivia + alturafastOlivia))
        pixelsolivaDeRoupinhaX = list(range(posicaoXoliviaDeRoupinha, posicaoXoliviaDeRoupinha + larguraoliviaDeRoupinha))
        pixelsolivaDeRoupinhaY = list(range(posicaoYoliviaDeRoupinha, posicaoYoliviaDeRoupinha + alturaoliviaDeRoupinha))
        
        if  len( list( set(pixelsfastOliviaY).intersection(set(pixelsPersonaY))) or list( set(pixelsolivaDeRoupinhaY).intersection(set(pixelsPersonaY)))) > dificuldade:
            if len( list( set(pixelsfastOliviaX).intersection(set(pixelsPersonaX)) ) or  list( set(pixelsolivaDeRoupinhaX).intersection(set(pixelsPersonaX)) ))  > dificuldade:
                dead(nome, pontos)
        
        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    # pygame.mixer.Sound.play(explosaoSound)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        buttonStart = pygame.draw.rect(tela, vermelho, (35,482,750,100),0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400,482))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60,482))
        pygame.display.update()
        relogio.tick(60)


def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8" )
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass
    
    nomes = sorted(estrelas, key=estrelas.get,reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, vermelho, (35,482,750,100),0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330,482))
        
        
        posicaoY = 50
        for key,nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - "+str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300,posicaoY))
            posicaoY = posicaoY + 30

            
        
        pygame.display.update()
        relogio.tick(60)


def start():
    nome = simpledialog.askstring("Olivia, the Destroyer","Nome Completo:")
    
    
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        buttonStart = pygame.draw.rect(tela, vermelho, (35,482,750,100),0)
        buttonRanking = pygame.draw.rect(tela, vermelho, (35,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90,50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330,482))

        
        
        pygame.display.update()
        relogio.tick(60)

start()