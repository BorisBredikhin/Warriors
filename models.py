import random
from typing import List

from pygame.sprite import Sprite
from pygame.surface import Surface

from utils import Averager


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
        self.armor = armor
        self.default_damage = self.weapon.damage

        self.image = Surface(self.size)
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()

    def __str__(self):
        return f"Воин {self.name}"

    def hit(self, enemy: 'Warrior'):
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


def create_weapons(data):
    for w in data:
        Weapon(name=w.get("name", None), damage=w.get("damage", 0), threshold=w.get("threshold", 1.0))


def create_warriors(data):
    for w in data:
        Warrior(name=w.get('name'))


def create_armours(data: List[dict]):
    for a in data:
        Armor(damping=a.get("damping", 0), health=a.get("health", 0), name=a.get("name"))
