import pygame
import random
from tkinter import simpledialog
from balao import draw_speech_bubble as balaoSonho

pygame.init()

relogio = pygame.time.Clock()

# buscando recursos
icone  = pygame.image.load("recursos/icone.ico")

monitor = pygame.image.load("recursos/monitor.png") # monitor
fundo = pygame.image.load("recursos/fundo.jpg")
fundoStart = pygame.image.load("recursos/fundoStart.png")
fundoDead = pygame.image.load("recursos/fundoDead.png")
fastOlivia = pygame.image.load("recursos/ataque.png") # olivia
oliviaDeRoupa = pygame.image.load("recursos/oliviadeRoupa.png")
kiara = pygame.image.load("recursos/kiara_nanando.png")
helloKitty = pygame.image.load("recursos/helloKitty.png")

fatality = pygame.mixer.Sound("recursos/fatality.mp3")
ataqueNormal = pygame.mixer.Sound("recursos/ataqueNormal.mp3")
ataqueCarregado = pygame.mixer.Sound("recursos/ataqueCarregado.mp3")

fonte = pygame.font.Font("recursos/VCR_OSD_MONO_1.001.ttf",28)
fonteStart = pygame.font.Font("recursos/VCR_OSD_MONO_1.001.ttf",110)
fonteRanking = pygame.font.Font("recursos/VCR_OSD_MONO_1.001.ttf", 50)

# setando propriedades inicias
tamanho = (800,600)
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Olivia, the Destroyer")
pygame.display.set_icon(icone)

branco = (255,255,255)
preto = (0, 0 ,0 )
vermelho = (255,0,0)

def jogar(nome):
    pygame.mixer.music.load("recursos/soundtrack.mp3")
    pygame.mixer.music.play(-1)

    # posicoes
    posicaoXPersona = 400
    posicaoYPersona = 500
    posicaoXOlivia = 400
    posicaoYOlivia = -240

    # movimento
    movimentoXPersona  = 0
    
    # dimensoes
    larguraPersona = 82
    alturaPersona = 100
    sizeBalao = 35

    velocidadeOlivia = 1
    pontos = 0
    dificuldade  = 20
    oliviaNaTela = fastOlivia

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
        
        if posicaoXPersona < 50 :
            posicaoXPersona = 60
        elif posicaoXPersona > 650:
            posicaoXPersona = 640
            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        tela.blit(monitor, (posicaoXPersona, posicaoYPersona))
        tela.blit(kiara, (300, 200))
        tela.blit(helloKitty, (360, 235))

        # coloca o balao de soninho da kiara
        balaoSonho(tela, "ZzZzZZ", preto, branco, (340, 220), sizeBalao)
        
        posicaoYOlivia = posicaoYOlivia + velocidadeOlivia
        
        if posicaoYOlivia > 600:
            posicaoYOlivia = -240
            pontos = pontos + 1
            velocidadeOlivia = velocidadeOlivia + 1      
            posicaoXOlivia = random.randint(60,640)      
            sizeBalao = 35 if sizeBalao == 20 else 20
            oliviaNaTela = oliviaDeRoupa if oliviaNaTela == fastOlivia else fastOlivia
            
        if oliviaNaTela == fastOlivia:
            larguraOlivia  = 150
            alturaOlivia  = 266
            tela.blit(oliviaNaTela, (posicaoXOlivia, posicaoYOlivia) )
            pygame.mixer.Sound.stop(ataqueCarregado)
            pygame.mixer.Sound.play(ataqueNormal)
        else:
            larguraOlivia = 106
            alturaOlivia = 182
            tela.blit(oliviaNaTela, (posicaoXOlivia, posicaoYOlivia))
            pygame.mixer.Sound.stop(ataqueNormal)
            pygame.mixer.Sound.play(ataqueCarregado, loops=0)
        
        texto = fonte.render(nome+" - Score: "+str(pontos), True, vermelho)
        tela.blit(texto, (10,10))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsOliviaX = list(range(posicaoXOlivia, posicaoXOlivia + larguraOlivia))
        pixelsOliviaY = list(range(posicaoYOlivia, posicaoYOlivia + alturaOlivia))
        
        # vai verificar se não encostou na olivia
        if  len(list( set(pixelsOliviaY).intersection(set(pixelsPersonaY)))) > dificuldade:
            if len(list( set(pixelsOliviaX).intersection(set(pixelsPersonaX))))  > dificuldade:
                pygame.mixer.Sound.stop(ataqueNormal if oliviaNaTela == fastOlivia else ataqueCarregado)
                dead(nome, pontos)
        
        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(fatality)

    pygame.mixer.music.load("recursos/gameovermusic.mp3")
    pygame.mixer.music.play(-1)
    
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
        buttonStart = pygame.draw.rect(tela, vermelho, (100,530,600,50),border_radius=15)
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (200,540))
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
        buttonStart = pygame.draw.rect(tela, vermelho, (200,485,400,100),0)
        textoStart = fonteRanking.render("BACK TO START", True, branco)
        tela.blit(textoStart, (211,510))
        
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
        buttonStart = pygame.draw.rect(tela, vermelho, (200,485,400,100),0)
        buttonRanking = pygame.draw.rect(tela, vermelho, (35,25,150,45),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (53,33))
        textoStart = fonteStart.render("FIGHT", True, branco)
        tela.blit(textoStart, (250,480))

        pygame.display.update()
        relogio.tick(60)

start()