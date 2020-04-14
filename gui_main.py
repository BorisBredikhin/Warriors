import pygame

pygame.init()
pygame.mixer.init()

import logging

logging.basicConfig(filename="warriors.log", level=logging.DEBUG, filemode='w')

from pygame.time import Clock

from game import Game
from ui.constants import *
from ui.font import show_text, Alignment


def main():
    pygame.display.set_caption("Warriors")

    screen: pygame.SurfaceType = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    game = Game(open('exampledata.json', 'r'), (WIDTH, HEIGHT))

    sprites.add(game.user_warrior, game.ai_warrior)

    running = True

    while running:
        event: pygame.event.EventType

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                game.process_event(event)

        sprites.update()
        screen.fill((0, 0, 0))
        sprites.draw(screen)

        show_text(screen, str(game.user_warrior), (0, 0), color=GREEN)
        show_text(screen, str(game.ai_warrior), (WIDTH, 0), align=Alignment.RIGHT, color=RED)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
