import pygame

pygame.init()
pygame.mixer.init()

from pygame.time import Clock

from game import Game
from ui.colors import *
from ui.font import show_text, Alignment

WIDTH = 320
HEIGHT = 240
FPS = 24


def main():
    pygame.display.set_caption("Warriors")

    screen: pygame.SurfaceType = pygame.display.set_mode((320, 240))

    clock = pygame.time.Clock()
    sprites = pygame.sprite.Group()

    game = Game(open('exampledata.json', 'r'))

    sprites.add(game.user_warrior, game.ai_warrior)

    running = True

    while running:
        event: pygame.event.EventType

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
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
