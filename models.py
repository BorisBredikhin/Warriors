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


class Warrior:
    warriors: List['Warrior'] = []  # static

    health = 100
    is_alive = True

    def __init__(self, name="Default Warrior"):
        self.warriors.append(self)

        self.name = name
        self.weapon = random.choice(Weapon.weapons)
        self.default_damage = self.weapon.damage

    def __str__(self):
        return f"Воин {self.name}"

    def hit(self, enemy):
        if enemy.is_alive and self.is_alive:
            print(f"{self.name} наносит удар оружием {self.weapon} {enemy.name} на {self.default_damage} урона")
            enemy.set_damage(self.default_damage)
            if not enemy.is_alive:
                print(f"{self.name} победил!")

    def set_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            print(f"{self.name} погибает!")


def create_weapons(data):
    for w in data:
        Weapon(name=w.get("name", None), damage=w.get("damage", 0))


def create_warriors(data):
    for w in data:
        Warrior(name=w.get('name'))
