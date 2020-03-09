import random
from typing import List


class Weapon:
    weapons: List['Weapon'] = []  # static

    def __init__(self, name: str, damage: int):
        self.weapons.append(self)
        self.name = name
        self.damage = damage

    def __str__(self):
        return f"{self.name}, урон {self.damage}"


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
        if self.integrity <= 0:
            return weapon.damage

        k = self.damping * self.integrity / self.health
        if k * weapon.damage > self.integrity:
            r = k * weapon.damage - self.integrity
            self.integrity = 0
            return int(r)
        self.integrity -= k * weapon.damage
        return int((1 - k) * weapon.damage)

    def __str__(self):
        return f"Броня {self.name} гасит {self.damping}"


class Warrior:
    warriors: List['Warrior'] = []  # static

    health = 100
    is_alive = True
    armor: 'Armor' = None

    def __init__(self, name="Default Warrior", weapon=None, armor=None):
        if weapon is None:
            weapon = random.choice(Weapon.weapons)
        if armor is None:
            armor = random.choice(Armor.armors)

        self.warriors.append(self)

        self.name = name
        self.weapon = weapon
        self.armor = armor
        self.default_damage = self.weapon.damage

    def __str__(self):
        return f"Воин {self.name}"

    def hit(self, enemy: 'Warrior'):
        if enemy.is_alive and self.is_alive:
            enemy.set_damage(self.weapon)

            print(
                f"{self.name} наносит удар оружием {self.weapon} {enemy.name} на {self.armor.get_damage(self.weapon)} урона, здоровье {enemy} {enemy.health} единиц")
            if not enemy.is_alive:
                print(f"{self.name} победил!")

    def set_damage(self, weapon):
        self.health -= self.armor.get_damage(weapon)
        if self.health <= 0:
            self.is_alive = False
            print(f"{self.name} погибает!")


def create_weapons(data):
    for w in data:
        Weapon(name=w.get("name", None), damage=w.get("damage", 0))


def create_warriors(data):
    for w in data:
        Warrior(name=w.get('name'))


def create_armours(data: List[dict]):
    for a in data:
        Armor(damping=a.get("damping", 0), health=a.get("health", 0), name=a.get("name"))
