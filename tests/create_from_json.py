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
      "damage": 10
    },
    {
      "name": "вилка",
      "damage": 15
    },
    {
      "name": "нож",
      "damage": 30
    }
  ],
  "warriors": [
    {
      "name": "Миша"
    },
    {
      "name": "Паша"
    }
  ]
}''')

    def test_load(self):
        self.assertTrue('weapons' in self.data.keys())
        self.assertTrue('warriors' in self.data.keys())

    def test_weapon_creation(self):
        if len(Weapon.weapons) == 0:
            create_weapons(self.data['weapons'])
        self.assertEqual(3, len(Weapon.weapons))
        self.assertEqual('ложка', Weapon.weapons[0].name)

    def test_warrior_creation(self):
        if len(Weapon.weapons) == 0:
            create_weapons(self.data['weapons'])
        create_warriors(self.data['warriors'])
        self.assertEqual(2, len(Warrior.warriors))
        self.assertEqual('Миша', Warrior.warriors[0].name)


if __name__ == '__main__':
    unittest.main()
