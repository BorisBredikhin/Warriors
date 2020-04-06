import json

from models import *


class Game:
    def __init__(self, file):
        self.data = json.load(file)
        create_weapons(self.data['weapons'])
        create_armours(self.data['armors'])
        create_warriors(self.data['warriors'])
