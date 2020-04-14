import json

import pygame

from models import *
from ui.constants import *


class Game:
    ai_warrior: Warrior
    user_warrior: Warrior

    def __init__(self, file, size):
        self.data = json.load(file)

        create_weapons(self.data['weapons'])
        create_armours(self.data['armors'])
        create_warriors(self.data['warriors'])

        [self.user_warrior, self.ai_warrior] = Warrior.warriors

        self.user_warrior.rect.y = self.ai_warrior.rect.y = size[1] / 2
        self.user_warrior.rect.x = self.ai_warrior.rect.x = size[0] / 2
        self.user_warrior.rect.x -= Warrior.size[0]
        self.ai_warrior.rect.x += Warrior.size[0]

        self.user_warrior.set_color(GREEN)
        self.ai_warrior.set_color(RED)

    def process_event(self, event: pygame.event.EventType) -> None:
        '''
        Обработка событий игры
        :param event:
        '''
        print('game.py ', event.key)
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.user_warrior.move(0, -1)
        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.user_warrior.move(1, 0)
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.user_warrior.move(0, 1)
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.user_warrior.move(-1, 0)
        elif event.key == pygame.K_SPACE:
            self.user_warrior.hit(self.ai_warrior)

        self.ai_warrior.make_move(self.user_warrior)
