import sys
from random import randint
import pygame
import time

pygame.init()

tela = pygame.display.set_mode((900, 500))

pygame.display.set_caption("Battle Star")

cor_amarelo = (255, 255, 0)
cor_amarelo_claro = (255, 218, 0)
cor_amarelo_escuro = (255, 181, 0)
cor_preta = (0, 0, 0)


def load_image(image_name):
    try:
        image = pygame.image.load(image_name).convert_alpha()
    except pygame.error:
        raise SystemExit
    return image


def render_on_scren(objeto):
    tela.blit(objeto["imagem"], (objeto["x"], objeto["y"]))


def posicao_nave_um(range_ini, range_end):
    pos_x = randint(range_ini, range_end)
    pos_y = -200
    return pos_x, pos_y


def txt(msg, tam, cor):
    fonte = pygame.font.SysFont("freesansbold.ttf", tam)
    texto = fonte.render(msg, True, cor)
    return texto


def botao(msg, x, y, weight, height, hover_cor_out, hover_cor_in, action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)
    pygame.draw.rect(tela, hover_cor_out, (x, y, weight, height))

    if x + weight > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(tela, hover_cor_in, (x, y, weight, height))
        if click[0] and action:
            action()

    x, y = (x + (weight / 2)*0.9), (y + (height / 2)*0.7)
    render_text_on_screen(msg["text"], msg["tam"], msg["cor"], x, y)


def render_text_on_screen(msg, size_font, color_font, x, y):
    texto = txt(msg, size_font, color_font)
    tela.blit(texto, (x, y))


def winner(imagem, ptsvida, pontos):
    tela.blit(imagem, (0, 0))
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


def play_tiro():
    pygame.mixer.music.load("tiro.ogg")
    pygame.mixer.music.play(1)


def playaudio():
    pygame.mixer.music.load("audiofundo.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)


def jogo():

    naves_inimigas = {"um": {"imagem": load_image("naveinimi.png"),
                             "x": 200,
                             "y": -100
                             },
                      "dois": {"imagem": load_image("naveinimi.png"),
                               "x": 400,
                               "y": -100}
                      }

    num_tiro = 0

    nave = {"imagem": load_image("navee.png"),
            "x": 450, "y": 350}

    tiros = {}
    explosoes = []

    movimento_nave = 20
    movimento_inimigo = 5

    imagem = load_image("fundoespaco.jpg")

    pontuacao_vida = load_image("pontosevida.png")
    pontos = 0
    vida = 1000

    tempo_fim = 180

    level = 10

    x, y = 450, 350

    while 1:
        pygame.time.delay(50)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit_game()

        comando = pygame.key.get_pressed()

        if comando[pygame.K_UP]:
            if y > 0:
                y -= movimento_nave
        elif comando[pygame.K_DOWN]:
            if y < 350:
                y += movimento_nave
        elif comando[pygame.K_LEFT]:
            if x > 0:
                x -= movimento_nave
        elif comando[pygame.K_RIGHT]:
            if x < 800:
                x += movimento_nave

        if comando[pygame.K_SPACE]:
            tempoinicio = time.time() * 60
            if (tempoinicio - tempo_fim) > 60:
                tiros.update({f"{num_tiro}": {
                                "imagem": load_image("tiro.png"),
                                "x": x+45,
                                "y": y
                            }
                         })
                num_tiro += 1
                play_tiro()
                tempo_fim = time.time() * 60

        for tiro in tiros:
            tiros[tiro]["y"] -= 5

        tiros_to_delete = []
        for m in naves_inimigas:
            if naves_inimigas[m]["y"] > 600:
                naves_inimigas[m]["x"], naves_inimigas[m]["y"] = posicao_nave_um(0, 800)
            else:
                naves_inimigas[m]["y"] += movimento_inimigo

            if (x + 90) > naves_inimigas[m]["x"] and x < (naves_inimigas[m]["x"] + 140):
                if y < (naves_inimigas[m]["y"] + 114) and naves_inimigas[m]["y"] < (y + 120):
                    vida -= 5

            for n in tiros:
                if (tiros[n]["x"] + 9) > naves_inimigas[m]["x"] and tiros[n]["x"] < (naves_inimigas[m]["x"] + 140):
                    if tiros[n]["y"] < (naves_inimigas[m]["y"] + 90) and naves_inimigas[m]["y"] < (tiros[n]["y"] + 78):
                        tiros_to_delete.append(n)
                        explosao = {"imagem": load_image("explosao.png")}
                        explosao_x, explosao_y = naves_inimigas[m]["x"], naves_inimigas[m]["y"]
                        explosao.update({"x": explosao_x,
                                         "y": explosao_y,
                                         "time": 1000})
                        explosoes.append(explosao)
                        naves_inimigas[m]["x"], naves_inimigas[m]["y"] = posicao_nave_um(0, 800)
                        comando_explosao, pontos = 1000, (pontos + 1)
                        playexplosao()

        for tiro_key in tiros_to_delete:
            del tiros[tiro_key]

        indeces_to_delete = []
        for indice_explosoes in range(len(explosoes)):
            if explosoes[indice_explosoes]["time"] < 0:
                indeces_to_delete.append(indice_explosoes)
            else:
                explosoes[indice_explosoes]["time"] -= 100

        for indece in indeces_to_delete:
            del explosoes[indece]

        if pontos > level:
            movimento_inimigo += 2
            level = level + 10

        if pontos > 99 or vida < 0: winner(imagem, vida, pontos)

        tela.blit(imagem, (0, 0))

        nave["x"], nave["y"] = x, y
        render_on_scren(nave)

        for nave_ini in naves_inimigas:
            render_on_scren(naves_inimigas[nave_ini])

        for tiro in tiros:
            render_on_scren(tiros[tiro])

        for explosao in explosoes:
            render_on_scren(explosao)

        tela.blit(pontuacao_vida, (250, 0))
        vidatxt = txt(str(vida), 25, (0, 0, 0))
        ptstxt = txt(str(pontos), 25, (0, 0, 0))
        tela.blit(vidatxt, (320, 13))
        tela.blit(ptstxt, (490, 15))

        pygame.display.update()


def intro():
    intro_info = load_image("intro.png")
    tela.blit(intro_info, (-40, -40))
    pygame.display.update()
    time.sleep(4)
    jogo()


def quit_game():
    pygame.quit()
    sys.exit()


def menu():
    playaudio()
    while 1:
        fundo_menu = load_image("fundomenu.jpg")

        tela.blit(fundo_menu, (0, 0))

        start_msg = {"text": "START", "tam": 25, "cor": cor_preta}
        quit_msg = {"text": "QUIT", "tam": 25, "cor": cor_preta}

        botao(start_msg, 250, 150, 400, 50, cor_amarelo_escuro, cor_amarelo_claro, intro)
        botao(quit_msg, 250, 250, 400, 50, cor_amarelo_escuro, cor_amarelo_claro, quit_game)

        render_text_on_screen("Desenvolvido por Josimar Rachetti", 30, cor_amarelo, 300, 50)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit_game()


if __name__ == "__main__":
    menu()
