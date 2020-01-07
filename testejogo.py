import os
import sys
from random import randint
import pygame
import time

pygame.init()

# Play surface
tela = pygame.display.set_mode((900,500))
pygame.display.set_caption("Battle Star")

# função para colocar imagem
def load_image(image_name):
    '''carrega uma imgagem na memoria'''

    try:
        image = pygame.image.load(image_name).convert_alpha()
    except pygame.error:
        raise SystemExit
    return image

def posicaonave1(inix, iniy):
    inix = randint(0, 450)
    iniy = -200
    return inix, iniy


def posicaonave2(inix, iniy):
    inix = randint(450, 800)
    iniy = -150
    return inix, iniy


def txt(msg,tam,cor):
    fonte = pygame.font.SysFont("freesansbold.ttf", tam)
    texto = fonte.render(msg, True, cor)
    return texto


def botao(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(tela, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if "start" == action:
                intro()
            elif action == "quit":
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(tela, ic, (x, y, w, h))
    texto = txt(msg, 25,(0,0,0))
    tela.blit(texto, ((x + (w / 2) - 13), (y + (h / 2) - 8)))

def winner(imagem, ptsvida, pontos):
    tela.blit(imagem, (0,0))
    if ptsvida < 1:
        mensagem = txt(" 0 VIDA, VOCE FOI DERROTADO PELO IMPERIO!!", 50, (255, 215, 0))
    elif pontos > 99:
        mensagem = txt("100 PONTOS, VENCEDOR, DERROTOU O IMPERIO!!", 50, (255, 215, 0))

    tela.blit(mensagem, (30, 200))
    pygame.display.update()
    time.sleep(7)
    menu()

def playexplosao():
    pygame.mixer.music.load("explosao.ogg")
    pygame.mixer.music.play(1)

def playtiro():
    pygame.mixer.music.load("tiro.ogg")
    pygame.mixer.music.play(1)

def playaudio():
    pygame.mixer.music.load("audiofundo.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)


def jogo():
    yinimiga = -100
    xinimiga = 200
    yinimiga2 = -100
    xinimiga2 = 400
    numtiro = 0
    tx = [-100, -100, -100, -100, -100]
    ty = [-100, -100, -100, -100, -100]
    explosaox = [-200, -200]
    explosaoy = [-200, -200]
    mover = 20
    moveini = 5
    imagem = load_image("fundoespaco.jpg")
    nave = load_image("navee.png")
    naveinimiga = load_image("naveinimi.png")
    naveinimiga2 = load_image("naveinimi.png")
    explosao = [load_image("explosao.png"), load_image("explosao.png")]
    tiro = [load_image("tiro.png"), load_image("tiro.png"), load_image("tiro.png"), load_image("tiro.png"),
            load_image("tiro.png")]
    pontovida = load_image("pontosevida.png")

    pontos = 0
    vida = 1000

    tempofim = 180

    comandoexplosao = 1000
    comandoexplosao2 = 1000

    level=10

    x = 450
    y = 350


    while True:

        pygame.time.delay(50)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        comando = pygame.key.get_pressed()
        if comando[pygame.K_UP]:
            if y > 0:
                y -= mover
        if comando[pygame.K_DOWN]:
            if y < 350:
                y += mover
        if comando[pygame.K_LEFT]:
            if x > 0:
                x -= mover
        if comando[pygame.K_RIGHT]:
            if x < 800:
                x += mover
        if comando[pygame.K_SPACE]:
            tempoinicio = time.time() * 60
            if (tempoinicio - tempofim) > 60:
                ty[numtiro] = y
                tx[numtiro] = x + 45
                numtiro += 1
                playtiro()
                tempofim = time.time() * 60
                if numtiro > 4:
                    numtiro = 0

        yinimiga += moveini
        yinimiga2 += moveini

        if ty[0] > -100:
            ty[0] -= 5
        if ty[1] > -100:
            ty[1] -= 5
        if ty[2] > -100:
            ty[2] -= 5
        if ty[3] > -100:
            ty[3] -= 5
        if ty[4] > -100:
            ty[4] -= 5

        if yinimiga > 600:
            xinimiga, yinimiga = posicaonave1(xinimiga, yinimiga)

        if yinimiga2 > 600:
            xinimiga2, yinimiga2 = posicaonave2(xinimiga2, yinimiga2)

        if (x + 90) > xinimiga and x < (xinimiga + 140):
            if y < (yinimiga + 114) and yinimiga < (y + 120):
                vida-=5

        if (x + 90) > xinimiga2 and x < (xinimiga2 + 140):
            if y < (yinimiga2 + 114) and yinimiga2 < (y + 120):
                vida-=5

        if (tx[0] + 9) > xinimiga and tx[0] < (xinimiga + 140):
            if ty[0] < (yinimiga + 90) and yinimiga < (ty[0] + 78):
                explosaox[0], explosaoy[0] = xinimiga, yinimiga
                xinimiga, yinimiga = posicaonave1(xinimiga, yinimiga)
                tx[0], ty[0] = -100, -100
                comandoexplosao, pontos = 1000, (pontos+1)
                playexplosao()

        if (tx[1] + 9) > xinimiga and tx[1] < (xinimiga + 140):
            if ty[1] < (yinimiga + 90) and yinimiga < (ty[1] + 78):
                explosaox[0], explosaoy[0] = xinimiga, yinimiga
                xinimiga, yinimiga = posicaonave1(xinimiga, yinimiga)
                tx[1], ty[1] = -100, -100
                comandoexplosao, pontos = 1000, (pontos+1)
                playexplosao()

        if (tx[2] + 9) > xinimiga and tx[2] < (xinimiga + 140):
            if ty[2] < (yinimiga + 90) and yinimiga < (ty[2] + 78):
                explosaox[0], explosaoy[0] = xinimiga, yinimiga
                xinimiga, yinimiga = posicaonave1(xinimiga, yinimiga)
                tx[2], ty[2] = -100, -100
                comandoexplosao, pontos = 1000, (pontos+1)
                playexplosao()

        if (tx[3] + 9) > xinimiga and tx[3] < (xinimiga + 140):
            if ty[3] < (yinimiga + 90) and yinimiga < (ty[3] + 78):
                explosaox[0], explosaoy[0] = xinimiga, yinimiga
                xinimiga, yinimiga = posicaonave1(xinimiga, yinimiga)
                tx[3], ty[3] = -100, -100
                comandoexplosao, pontos = 1000, (pontos+1)
                playexplosao()

        if (tx[4] + 9) > xinimiga and tx[4] < (xinimiga + 140):
            if ty[4] < (yinimiga + 90) and yinimiga < (ty[4] + 78):
                explosaox[0], explosaoy[0] = xinimiga, yinimiga
                xinimiga, yinimiga = posicaonave1(xinimiga, yinimiga)
                tx[4], ty[4] = -100, -100
                comandoexplosao, pontos = 1000, (pontos+1)
                playexplosao()

        if (tx[0] + 9) > xinimiga2 and tx[0] < (xinimiga2 + 140):
            if ty[0] < (yinimiga2 + 90) and yinimiga2 < (ty[0] + 78):
                explosaox[1], explosaoy[1] = xinimiga2, yinimiga2
                xinimiga2, yinimiga2 = posicaonave2(xinimiga2, yinimiga2)
                tx[0], ty[0] = -100, -100
                comandoexplosao2, pontos = 1000, (pontos+1)
                playexplosao()

        if (tx[1] + 9) > xinimiga2 and tx[1] < (xinimiga2 + 140):
            if ty[1] < (yinimiga2 + 90) and yinimiga2 < (ty[1] + 78):
                explosaox[1], explosaoy[1] = xinimiga2, yinimiga2
                xinimiga2, yinimiga2 = posicaonave2(xinimiga2, yinimiga2)
                tx[1], ty[1] = -100, -100
                comandoexplosao2, pontos = 1000, (pontos+1)
                playexplosao()

        if (tx[2] + 9) > xinimiga2 and tx[2] < (xinimiga2 + 140):
            if ty[2] < (yinimiga2 + 90) and yinimiga2 < (ty[2] + 78):
                explosaox[1], explosaoy[1] = xinimiga2, yinimiga2
                xinimiga2, yinimiga2 = posicaonave2(xinimiga2, yinimiga2)
                tx[2], ty[2] = -100, -100
                comandoexplosao2, pontos = 1000, (pontos+1)
                playexplosao()

        if (tx[3] + 9) > xinimiga2 and tx[3] < (xinimiga2 + 140):
            if ty[3] < (yinimiga2 + 90) and yinimiga2 < (ty[3] + 78):
                explosaox[1], explosaoy[1] = xinimiga2, yinimiga2
                xinimiga2, yinimiga2 = posicaonave2(xinimiga2, yinimiga2)
                tx[3], ty[3] = -100, -100
                comandoexplosao2, pontos = 1000, (pontos+1)
                playexplosao()

        if (tx[4] + 9) > xinimiga2 and tx[4] < (xinimiga2 + 140):
            if ty[4] < (yinimiga2 + 90) and yinimiga2 < (ty[4] + 78):
                explosaox[1], explosaoy[1] = xinimiga2, yinimiga2
                xinimiga2, yinimiga2 = posicaonave2(xinimiga2, yinimiga2)
                tx[4], ty[4] = -100, -100
                comandoexplosao2, pontos = 1000, (pontos+1)
                playexplosao()

        if comandoexplosao < 0:
            explosaox[0], explosaoy[0] = -200, -200
        else:
            comandoexplosao -= 100

        if comandoexplosao2 < 0:
            explosaox[1], explosaoy[1] = -200, -200
        else:
            comandoexplosao2 -= 100

        if pontos > level:
            moveini += 2
            level=level+10

        if pontos > 99 or vida < 0: winner(imagem, vida, pontos)

        tela.blit(imagem, (0, 0))
        tela.blit(nave, (x, y))
        tela.blit(naveinimiga, (xinimiga, yinimiga))
        tela.blit(naveinimiga2, (xinimiga2, yinimiga2))
        tela.blit(tiro[0], (tx[0], ty[0]))
        tela.blit(tiro[1], (tx[1], ty[1]))
        tela.blit(tiro[2], (tx[2], ty[2]))
        tela.blit(tiro[3], (tx[3], ty[3]))
        tela.blit(tiro[4], (tx[4], ty[4]))
        tela.blit(explosao[0], (explosaox[0], explosaoy[0]))
        tela.blit(explosao[1], (explosaox[1], explosaoy[1]))
        tela.blit(pontovida, (250, 0))
        vidatxt = txt(str(vida),25,(0,0,0))
        ptstxt = txt(str(pontos),25,(0,0,0))
        tela.blit(vidatxt, (320, 13))
        tela.blit(ptstxt, (490, 15))



        pygame.display.update()



def intro():
    intro = load_image("intro.png")
    tela.blit(intro, (-40, -40))
    pygame.display.update()
    time.sleep(4)
    jogo()


def menu():
    playaudio()
    while True:
        mouse = pygame.mouse.get_pos()
        fundomenu = load_image("fundomenu.jpg")
        tela.blit(fundomenu, (0, 0))
        pygame.draw.rect(tela, (255, 181, 0), (250, 150, 400, 50))
        pygame.draw.rect(tela, (255, 181, 0), (250, 250, 400, 50))

        botao("STAR", 250, 150, 400, 50, (255, 181, 0), (255, 218, 0), "start")
        botao("QUIT", 250, 250, 400, 50, (255, 181, 0), (255, 218, 0), "quit")
        creditos = txt("Desenvolvivodo por Josimar Rachetti", 30,(255, 255, 0))
        tela.blit(creditos, (250, 450))
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

menu()