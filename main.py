
from game import Game
from models import *

game = Game(open('exampledata.json', 'r'))

print("Оружие: ", "\n".join([str(w) for w in Weapon.weapons]), sep="\n")
print("Броня:", *Armor.armors, sep='\n')
print("Воины: ", "\n".join([str(w) for w in Warrior.warriors]), sep="\n")

w1 = Warrior.warriors[0]
w2 = Warrior.warriors[1]

while all([w1.is_alive, w2.is_alive]):
    random.choice([w1.hit(w2), w2.hit(w1)])

for weapon in [w1.weapon, w2.weapon]:
    print(f'Средний урон {weapon.name} - {weapon.average_damage}')
