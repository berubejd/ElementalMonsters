#!/usr/bin/env python3.8

import csv
import random
from collections import defaultdict

DMGMODIFIERS = 'dmgmodifiers.csv'
MONSTERDATA = 'monsterdata.csv'

class Monster:

    MIN_HP_PER_LEVEL = 6
    MAX_HP_PER_LEVEL = 10

    BASE_DMG = 4
    BASE_DEFENSE = 4

    # Can these functions be moved somewhere more appropriate?
    def load_modifiers() -> defaultdict:
        mods = defaultdict(dict)

        with open(DMGMODIFIERS) as fp:
            for line in csv.DictReader(fp):
                element_type = line['type']
                del line['type']

                mods[element_type] = line

        return mods

    element_modifiers = load_modifiers()

    # Can these functions be moved somewhere more appropriate?
    def load_monsters() -> defaultdict:
        monsters = defaultdict(list)

        with open(MONSTERDATA) as fp:
            for line in csv.DictReader(fp):
                monsters[line['rarity']].append(line)

        return monsters

    monster_list = load_monsters()

    def __init__(self, name: str, element: str, description: str = '', tier: int = 1 , level: int = 1, rarity: str = 'Common', strength: int = 1, defense: int = 1):
        # Basic information
        self.name = name
        self.description = description
        self.element = element
        self.rarity = rarity
        self.tier = tier

        # Level and Experience
        self.level = int(level)
        self.experience = 0
        self.experience_needed = int(level ** 1.8 + level * 4 + 8)  # Source GDquest

        # Strength - Attack and Defense - Armor
        self.strength = int(strength)
        self.defense = int(defense)

        self.attack = self.BASE_DMG * self.strength + self.level
        self.armor = self.BASE_DEFENSE * self.defense

        # Hit Points
        self.hp = sum(random.randint(self.MIN_HP_PER_LEVEL, self.MAX_HP_PER_LEVEL) for _ in range(self.level))

    @classmethod
    def random_monster(self):
        # Hardcode a distribution here because I can't figure out a better way
        # distribution = [len(cls.monster_list[key]) for key in cls.monster_list.keys()]
        distribution = [80, 16, 4]
        rarity = random.choices(self.available_rarities(), weights=distribution)[0]

        return self(**random.choice(self.monster_list[rarity]))

    @classmethod
    def random_monster_filter(self, rarity: str = 'Common', element: str = None):
        if rarity in self.available_rarities():
            if element and element in self.available_elements():
                filtered_monsters = [monster for monster in self.monster_list[rarity] if monster['element'] == element]

                if len(filtered_monsters):
                    monster = random.choice(filtered_monsters)
                else:
                    raise ValueError('This combination of rarity and element does not exist.')
            else:
               monster = random.choice(self.monster_list[rarity])

        return self(**monster)

    def __repr__(self):
        return f'{self.name}'

    def attack_target(self, target) -> bool:
        # Sourced from Tamer's Tale
        return round(sum(random.randint(1,self.attack) for _ in range(self.tier)) + (self.attack * float(self.element_modifiers[self.element][target.element])) + self.level - target.armor)

    @staticmethod
    def available_rarities() -> list:
        return list(Monster.monster_list.keys())

    @staticmethod
    def available_elements() -> list:
        return list(Monster.element_modifiers.keys())