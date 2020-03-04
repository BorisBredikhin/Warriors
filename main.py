import json

from models import *

DATA = json.load(open('exampledata.json', 'r'))

create_weapons(DATA['weapons'])
create_warriors(DATA['warriors'])

print("Оружие: ", "\n".join([str(w) for w in Weapon.weapons]), sep="\n")
print("Воины: ", "\n".join([str(w) for w in Warrior.warriors]), sep="\n")

w1 = Warrior.warriors[0]
w2 = Warrior.warriors[1]

while all([w1.is_alive, w2.is_alive]):
    random.choice([w1.hit(w2), w2.hit(w1)])
