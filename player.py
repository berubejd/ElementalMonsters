#!/usr/bin/env python3.8

import random
from monster import Monster

class Player:
    def __init__(self, name: str, monster: Monster):
        self.name = name
        self.monster = monster
        self.gold = 0

    @classmethod
    def interactive(self):
        while True:
            try:
                name = input("Please enter a name for your adventure: ")

                if name.lower() == 'quit':
                    exit()

                print(f"\nWelcome, {name}!  Now it's time to select your monsterly companion...")
                print()

                monster = self.select_monster()
                print(f'\nYou have selected the {monster.name}!')

                if name and monster:
                        return self(name, monster)
            except:
                continue

    @staticmethod
    def select_monster():
        # Select the three elements for the player and generate those monsters
        monster_data = [Monster.random_monster_filter('Common', element) for element in random.sample(Monster.available_elements(), 3)]

        # Set up the column and row values
        column_titles = ['Monster 1', ' Monster 2', 'Monster 3']
        row_titles = ['Name', 'Element', None, 'Attack', 'Defense', 'Hit Points']

        # Define the table header formatting and render the table
        row_format ="{:<11} " + "{:^25}" * (len(column_titles))
        print(row_format.format("", *column_titles))
        print()

        for row in row_titles:
            if row is None:
                print()
            else:
                if row == 'Hit Points':
                    row = 'hp'

                if row == 'Element':
                    print(row_format.format(f'{row}:', *[f'{monster.element} ({monster.rarity})' for monster in monster_data]))
                else:
                    print(row_format.format(f'{row}:', *[getattr(monster, row.lower()) for monster in monster_data]))

        print()

        while True:
            response = input("Please choose a companion (Enter a number between 1 and 3 that corresponds with your selection): ")

            if response.isnumeric() and 1 <= int(response) <= 3:
                return monster_data[int(response) - 1]
            elif response.lower() == 'quit':
                exit()
            else:
                continue