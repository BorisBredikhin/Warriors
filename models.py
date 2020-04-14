import random
from typing import List

from pygame.sprite import Sprite
from pygame.surface import Surface

from utils import Averager, sgn


class Weapon:
    weapons: List['Weapon'] = []  # static

    def __init__(self, name: str, damage: int, threshold: float):
        self.weapons.append(self)
        self.name = name
        self._damage = damage
        self.threshold = threshold
        self._total_damage = Averager()

    @property
    def damage(self) -> int:
        # threshold --- шанс попадания.
        # Мы берём равномерно распределённую величину Х.
        # Еесли её значение не превышает порога, то вероятность такого значения
        # равна порогу и наносится удар.
        return self._damage if random.uniform(0.0, 1.0) <= self.threshold else 0

    @property
    def average_damage(self):
        return float(self._total_damage)

    def update_average_damage(self, damage):
        self._total_damage.add(damage)

    def __str__(self):
        return f"{self.name}, урон {self._damage}"


class Armor:
    armors: List['Armor'] = []  # static

    damping: float
    integrity: float
    health: float
    name: str

    def __init__(self, name: str, damping: float, health: float) -> None:
        assert 0 <= damping < 1
        self.armors.append(self)
        self.name = name
        self.damping = damping
        self.integrity = self.health = health

    def get_damage(self, weapon: 'Weapon') -> int:
        weapon_damage = weapon.damage
        if self.integrity <= 0:
            return weapon_damage

        k = self.damping * self.integrity / self.health
        if k * weapon_damage > self.integrity:
            r = k * weapon_damage - self.integrity
            self.integrity = 0
            return int(r)
        self.integrity -= k * weapon_damage
        return int((1 - k) * weapon_damage)

    def copy(self):
        return Armor(self.name, self.damping, self.health)

    def __str__(self):
        return f"Броня {self.name} гасит {self.damping}"


class Warrior(Sprite):
    warriors: List['Warrior'] = []  # static

    health = 100
    is_alive = True
    armor: 'Armor' = None
    weapon: 'Weapon' = None

    size = (10, 10)

    def __init__(self, name="Default Warrior", weapon=None, armor=None, *groups):
        super().__init__(*groups)
        if weapon is None:
            weapon = random.choice(Weapon.weapons)
        if armor is None:
            armor = random.choice(Armor.armors)

        self.warriors.append(self)

        self.name = name
        self.weapon = weapon

        # без копиррования на двух воинах можзет оказаться одна броня
        self.armor = armor.copy()

        self.default_damage = self.weapon.damage

        self.image = Surface(self.size)
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()

    def set_color(self, color):
        self.image.fill(color)

    def move(self, dx, dy):
        '''

        :param dx: смеще6ние по горизонтали, в долях от размера
        :param dy: смеще6ние по вертикали, в долях от размера
        '''
        print('models.Warriors.move', self.name, dx, dy)
        self.rect.x += dx * self.size[0]
        self.rect.y += dy * self.size[0]
        print('\t', self.rect)

    def __str__(self):
        return f"Воин {self.name}\nЗдоровье {self.health}\nБроня:{self.armor.integrity}"

    def hit(self, enemy: 'Warrior'):
        if not self.can_hit(enemy):
            print(f"{self.name} промахивается!")
            return
        if enemy.is_alive and self.is_alive:
            damage = enemy.set_damage(self.weapon)
            self.weapon.update_average_damage(damage)

            if damage > 0:
                print(
                    f"{self.name} наносит удар оружием {self.weapon} {enemy.name} на {damage} урона, здоровье {enemy} {enemy.health} единиц")
                if not enemy.is_alive:
                    print(f"{enemy.name} погибает!")
                    print(f"{self.name} победил!")
            else:
                print(f"{self.name} промахивается!")

    def set_damage(self, weapon):
        damage = self.armor.get_damage(weapon)
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False

        return damage

    def can_hit(self, enemy):
        return abs(self.rect.x - enemy.rect.x) <= (self.size[0] + enemy.size[0]) >> 1 and abs(
            self.rect.y - enemy.rect.y) <= (self.size[1] + enemy.size[1]) >> 1

    def make_move(self, user_warrior):
        '''
        Делает автоход
        '''
        print('models.Warrior.make_move')
        boldness = random.random()
        delta = (self.rect.x - user_warrior.rect.x, self.rect.y - user_warrior.rect.y)
        if boldness < 0.5:
            # противник обороняется и отходит от игрка
            print('\tотступление')
            if abs(delta[0]) > abs(delta[1]):
                self.move(sgn(delta[0]), 0)
            else:
                self.move(0, sgn(delta[1]))
        else:
            if self.can_hit(user_warrior):
                print('\tудар')
                self.hit(user_warrior)
            else:
                print('\tприближение')
                if abs(delta[0]) > abs(delta[1]):
                    self.move(-sgn(delta[0]), 0)
                else:
                    self.move(0, -sgn(delta[1]))


def create_weapons(data):
    for w in data:
        Weapon(name=w.get("name", None), damage=w.get("damage", 0), threshold=w.get("threshold", 1.0))


def create_warriors(data):
    for w in data:
        Warrior(name=w.get('name'))


def create_armours(data: List[dict]):
    for a in data:
        Armor(damping=a.get("damping", 0), health=a.get("health", 0), name=a.get("name"))
