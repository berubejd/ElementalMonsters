#!/usr/bin/env python3.8

import csv
import random
from collections import defaultdict
from math import trunc

DMGMODIFIERS = 'dmgmodifiers.csv'
MONSTERDATA = 'monsterdata.csv'

class Monster:

    MIN_HP_PER_LEVEL = 6
    MAX_HP_PER_LEVEL = 10

    BASE_DMG = 6
    BASE_DEFENSE = 6

    # Can these functions be moved somewhere more appropriate?
    def load_modifiers() -> defaultdict:
        """Load element modifiers from provided csv"""

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
        """Load monsters from provided csv"""

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
        self.tier = int(tier)

        # Level and Experience
        self.level = int(level)
        self.experience = 0
        self.experience_needed = self.get_experience_needed(int(level) + 1)

        # Strength - Attack and Defense - Armor
        self.strength = int(strength) + trunc(int(level) / 2)
        self.defense = int(defense)

        self.str_mod = trunc((self.strength - 10) / 2)

        self.attack = self.BASE_DMG + self.str_mod
        self.armor = self.BASE_DEFENSE + self.defense

        # Hit Points
        self.hp = sum(random.randint(self.MIN_HP_PER_LEVEL, self.MAX_HP_PER_LEVEL) for _ in range(self.level))
        self.current_hp = self.hp

    @classmethod
    def random_monster(cls, level: int = 1):
        """ Return a random monster from the monster_list taking rarity into consideration"""

        # Hardcode a distribution here because I can't figure out a better way
        # distribution = [len(cls.monster_list[key]) for key in cls.monster_list.keys()]
        distribution = [80, 16, 4]
        rarity = random.choices(cls.available_rarities(), weights=distribution)[0]

        return cls(**random.choice(cls.monster_list[rarity]), level=level)

    @classmethod
    def random_monster_filter(cls, rarity: str = 'Common', element: str = None, level: int = 1):
        """Given a rarity, which defaults to 'Common', and an optional element type
           return a monster from the monster_list"""

        if rarity in cls.available_rarities():
            if element and element in cls.available_elements():
                filtered_monsters = [monster for monster in cls.monster_list[rarity] if monster['element'] == element]

                if len(filtered_monsters):
                    monster = random.choice(filtered_monsters)
                else:
                    raise ValueError('This combination of rarity and element does not exist.')
            else:
               monster = random.choice(cls.monster_list[rarity], level = 1)

        return cls(**monster)

    def __repr__(self):
        return f'{self.name}'

    def attack_target(self, target) -> int:
        """Return the amount of damage inflicted to 'target' based upon monster and target's stats and element"""

        # Bases loosely on Basic D&D 5.1
        return max(0, round((sum(random.randint(1,self.attack) for _ in range(self.tier)) * float(self.element_modifiers[self.element][target.element])))) if random.randint(1, 20) + self.str_mod > target.armor else 0

    def damage_taken(self, dmg_amount: int) -> int:
        """Track and determine the affects of damage taken returning remaining hit points"""

        self.current_hp = max(self.current_hp - dmg_amount, 0)

        return self.current_hp

    def healing(self, healing_amount: int) -> int:
        """Heal damage that may have been taken previously and return adjusted hit points"""
        
        self.current_hp = min(self.current_hp + healing_amount, self.hp)

        return self.current_hp

    def gain_xp(self, xp: int) -> bool:
        """Award monster experience and handle triggering of leveling. Return True if monster has leveled up."""

        leveled = False

        self.experience += xp

        if self.level == 10:
            # Max level has been reached so no reason to continue
            return
        else:
            while self.experience >= self.experience_needed:
                self.experience -= self.experience_needed
                self.level_up()

                leveled = True

        return leveled

    def level_up(self) -> None:
        """Handle monster progression that occurs with leveling up"""

        # Adjust level and experience requirement for next level
        self.level += 1

        # Tidy up experience if max level (level 10)
        if self.level == 10:
            self.experience = 0

        self.experience_needed = self.get_experience_needed(self.level + 1)

        # Adjust level based stats

        self.hp += random.randint(self.MIN_HP_PER_LEVEL, self.MAX_HP_PER_LEVEL)
        self.current_hp = self.hp

        # Strength is adjusted every other level
        if self.level % 2 == 0:
            self.strength += 1
            self.str_mod = trunc((self.strength - 10) / 2)
            self.attack = self.BASE_DMG + self.str_mod

    @staticmethod
    def get_experience_needed(level:int) -> int:
        """Calculate the experience required to gain a level - Source GDQuest"""

        return int(level ** 1.8 + level * 4 + 8)

    @staticmethod
    def available_rarities() -> list:
        """Helper function to provide access to the list of rarities provided by the loaded csv"""

        return list(Monster.monster_list.keys())

    @staticmethod
    def available_elements() -> list:
        """Helper function to provide access to the list of elements provided by the loaded csv"""

        return list(Monster.element_modifiers.keys())