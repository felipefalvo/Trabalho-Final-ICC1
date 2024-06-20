import pymunk ##FÍSICA
import pygame ## DISPLAY

pygame.init()

tela = pygame.display.set_mode((1000,600))
tempo = pygame.time.Clock()
FPS = 60


def jogo():
    while True:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return

    pygame.display.update()
    tempo.tick(FPS)

pygame.quit()
