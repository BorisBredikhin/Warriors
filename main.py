import json
import random
from typing import List


class Weapon:
    def __init__(self, name: str, damage: int):
        weapons.append(self)
        self.name = name
        self.damage = damage

    def __str__(self):
        return f"{self.name}, урон {self.damage}"


class Warrior:
    health = 100
    is_alive = True

    def __init__(self, name="Default Warrior"):
        warriors.append(self)

        self.name = name
        self.weapon = random.choice(weapons)
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


weapons: List[Weapon] = []
warriors: List[Warrior] = []

WEAPONS = '[{"name": "ложка", "damage": 10}, {"name": "вилка", "damage": 15}, {"name": "нож", "damage": 30}]'

create_weapons(json.loads(WEAPONS))

w1 = Warrior(name="Миша")
w2 = Warrior(name="Паша")

print("Оружие: ", "\n".join([str(w) for w in weapons]), sep="\n")
print("Воины: ", "\n".join([str(w) for w in warriors]), sep="\n")

while all([w1.is_alive, w2.is_alive]):
    random.choice([w1.hit(w2), w2.hit(w1)])
