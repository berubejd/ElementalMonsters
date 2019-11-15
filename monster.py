#!/usr/bin/env python3.8

import csv
import random
from collections import defaultdict

DMGMODIFIERS = 'dmgmodifiers.csv'

class Monster:

    min_hp_per_level = 6
    max_hp_per_level = 10

    base_dmg = 4
    base_defense = 4

    base_attack_modifier = .5

    def load_modifiers() -> defaultdict:
        mods = defaultdict(dict)

        with open(DMGMODIFIERS) as fp:
            for line in csv.DictReader(fp):
                element_type = line['Type']
                del line['Type']

                mods[element_type] = line

        return mods

    element_modifiers = load_modifiers()

    def __init__(self, name: str, element: str, level: int = 1, rarity: str = 'Common', strength: int = 1, defense: int = 1):
        # Basic information
        self.name = name
        self.element = element
        self.rarity = rarity
        self.tier = 1

        # Level and Experience
        self.level = level
        self.experience = 0
        self.experience_needed = int(level ** 1.8 + level * 4 + 8)  # Source GDquest

        # Strength - Attack and Defense - Armor
        self.strength = strength
        self.defense = defense

        self.attack = self.base_dmg * self.strength + self.level
        self.armor = self.base_defense * self.defense

        # Hit Points
        self.hp = sum(random.randint(self.min_hp_per_level, self.max_hp_per_level) for _ in range(self.level))

    def __repr__(self):
        return f'{self.name}'

    def attack_target(self, target) -> bool:
        return round(sum(random.randint(1,self.attack) for _ in range(self.tier)) + (self.attack * float(self.element_modifiers[self.element][target.element])) + self.level - target.armor)

