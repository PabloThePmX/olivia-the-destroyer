import pygame
import random
import os
from tkinter import simpledialog
from balao import draw_speech_bubble as balaoSonho

pygame.init()

relogio = pygame.time.Clock()
icone  = pygame.image.load("recursos/icone.ico")
iron = pygame.image.load("recursos/iron.png") # monitor
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
explosaoSound = pygame.mixer.Sound("recursos/explosao.wav")
fonte = pygame.font.SysFont("futura",28)
fonteStart = pygame.font.SysFont("futura",130)
fonteMorte = pygame.font.SysFont("futura",150)
pygame.mixer.music.load("recursos/soundtrack.mp3")

branco = (255,255,255)
preto = (0, 0 ,0 )


def jogar(nome):
    pygame.mixer.Sound.play(ataqueNormal)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 400
    posicaoYPersona = 500
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXfastOlivia = 400
    posicaoYfastOlivia = -240
    velocidadefastOlivia = 1
    pontos = 0
    larguraPersona = 250
    alturaPersona = 127
    larguafastOlivia  = 50
    alturafastOlivia  = 250
    dificuldade  = 20
    posicaoYKiara = 100
    posicaoXKiara = 200
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
            # elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
            #     movimentoYPersona = -10
            # elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
            #     movimentoYPersona = 10
            # elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
            #     movimentoYPersona = 0
            # elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
            #     movimentoYPersona = 0

        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 10
        elif posicaoXPersona >550:
            posicaoXPersona = 540
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 10
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        
            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        #pygame.draw.circle(tela, preto, (posicaoXPersona,posicaoYPersona), 40, 0 )
        tela.blit( iron, (posicaoXPersona, posicaoYPersona) )

        # coloca o balao de soninho da kiara
        balaoSonho(tela, "ZzZzZZ", preto, branco, (750, 500), sizeBalao)
        
        posicaoYfastOlivia = posicaoYfastOlivia + velocidadefastOlivia
        if posicaoYfastOlivia > 600:
            posicaoYfastOlivia = -240
            pontos = pontos + 1
            velocidadefastOlivia = velocidadefastOlivia + 1
            posicaoXfastOlivia = random.randint(0,800)
            pygame.mixer.Sound.play(ataqueNormal)
            sizeBalao = 35 if sizeBalao == 20 else 20
            
            
        tela.blit( fastOlivia, (posicaoXfastOlivia, posicaoYfastOlivia) )
        
        texto = fonte.render(nome+"- Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (10,10))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsfastOliviaX = list(range(posicaoXfastOlivia, posicaoXfastOlivia + larguafastOlivia))
        pixelsfastOliviaY = list(range(posicaoYfastOlivia, posicaoYfastOlivia + alturafastOlivia))
        
        if  len( list( set(pixelsfastOliviaY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsfastOliviaX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                dead(nome, pontos)
        
        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    
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
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
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
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
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
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        buttonRanking = pygame.draw.rect(tela, preto, (35,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90,50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330,482))

        
        
        pygame.display.update()
        relogio.tick(60)

start()