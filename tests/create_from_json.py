import json
import unittest

from models import *


class CreateFromJSON(unittest.TestCase):
    data: dict

    def setUp(self) -> None:
        self.data = json.loads('''{
  "weapons": [
    {
      "name": "ложка",
      "damage": 10,
      "threshold": 0.5
    },
    {
      "name": "вилка",
      "damage": 15,
      "threshold": 0.7
    },
    {
      "name": "нож",
      "damage": 30,
      "threshold": 0.9
    }
  ],
  "warriors": [
    {
      "name": "Миша"
    },
    {
      "name": "Паша"
    }
  ],
  "armors": [
    {
      "damping": 0.1,
      "health": 20,
      "name": "жилет"
    }
  ]
}'''
                               )
        create_weapons(self.data['weapons'])
        create_armours(self.data["armors"])
        create_warriors(self.data['warriors'])

    def tearDown(self) -> None:
        Weapon.weapons = []
        Armor.armors = []
        Warrior.warriors = []

    def test_load(self):
        self.assertTrue('weapons' in self.data.keys())
        self.assertTrue('warriors' in self.data.keys())

    def test_weapon_creation(self):
        self.assertEqual(3, len(Weapon.weapons))
        self.assertEqual('ложка', Weapon.weapons[0].name)
        self.assertTrue(Weapon.weapons[0].threshold in [0.5, 0.7, 0.9])

    def test_warrior_creation(self):
        self.assertEqual(2, len(Warrior.warriors))
        self.assertEqual('Миша', Warrior.warriors[0].name)

    def test_armor_creation(self):
        self.assertEqual(Armor.armors[0].name, "жилет")


if __name__ == '__main__':
    unittest.main()
