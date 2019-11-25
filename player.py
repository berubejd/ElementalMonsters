#!/usr/bin/env python3.8

import os
import pickle
import random
import sys
from datetime import datetime
from pathlib import Path
from monster import Monster

class Player:

    save_dir = 'player_saves'

    def __init__(self, name: str, monster: Monster):
        self.created = datetime.now()
        self.name = name
        self.monster = monster
        self.gold = 0
        self.blessing = datetime.now()

        self.savepath = Path(f'{self.save_dir}/{self.name}')

    @classmethod
    def interactive(cls):
        """Provide interactive constructor for player class"""
        while True:
            try:
                name = input("Please enter a name for your adventure: ")

                if name.lower() == 'quit':
                    sys.exit()

                savepath = Path(f'{cls.save_dir}/{name}')

                if cls.save_exists(cls, savepath):
                    response = None

                    while not response in ['l', 'o', 's']:
                        try:
                            response = input('\nThere appears to be a save with that name.\n\nWould you like to (L)oad the game, (O)verwrite, or (S)tart again? ')
                            reponse = response.lower()

                        except KeyboardInterrupt:
                            sys.exit()

                        except:
                            pass

                    if response == 'l':
                        player = cls.load_player(cls, savepath)
                        return player

                    if response == 's':
                        print()
                        continue

                print(f"\nWelcome, {name}!  Now it's time to select your monsterly companion...\n")

                monster = cls.select_monster()
                print(f'\nYou have selected the {monster.name}!')

                if name and monster:
                        return cls(name, monster)
            
            except KeyboardInterrupt:
                sys.exit()
            
            except:
                pass

    @staticmethod
    def select_monster():
        """Provide interactive interface for user to choose from three randomly selected
           'Common' rarity monsters"""

        # Select the three elements for the player and generate those monsters
        monster_data = [Monster.random_monster_filter('Common', element) for element in random.sample(Monster.available_elements(), 3)]

        # Set up the column and row values
        column_titles = ['Monster 1', ' Monster 2', 'Monster 3']
        row_titles = ['Name', 'Element', None, 'Strength', 'Defense', 'Hit Points']

        # Define the table header formatting and render the table
        row_format ="{:<10} " + "{:^20}" * (len(column_titles))
        print(row_format.format("", *column_titles))
        print()

        for row in row_titles:
            if row is None:
                print()
            else:
                if row == 'Hit Points':
                    row = 'HP'

                if row == 'Element':
                    print(row_format.format(f'{row}:', *[f'{monster.element} ({monster.rarity})' for monster in monster_data]))
                else:
                    print(row_format.format(f'{row}:', *[getattr(monster, row.lower()) for monster in monster_data]))

        print()

        while True:
            response = input("Please enter the number of your chosen companion: ")

            if response.isnumeric() and 1 <= int(response) <= 3:
                return monster_data[int(response) - 1]
            elif response.lower() == 'quit':
                exit()
            else:
                print('Enter a number between 1 and 3 that corresponds with your selection.')
                continue

    def save_player(self):
        """Save current player object to disk so that it can be used later"""

        savepath = Path(f'{self.save_dir}/{self.name}')

        savepath.parent.mkdir(exist_ok=True)

        try:
            savepath.rename(savepath.with_suffix('.bak'))
        except:
            pass

        with open(savepath, 'wb') as fp:
            pickle.dump(self,fp)

    def load_player(self, savepath: str = None):
        """Attempt to load and return an existing player object that has been saved"""

        if not savepath:
            savepath = self.savepath

        if self.save_exists(self, savepath):
            with open(savepath, 'rb') as fp:
                player = pickle.load(fp)

            return player

    def save_exists(self, savepath: str = None):
        """Verify the existance of the save file given the file name and path"""

        if not savepath:
            savepath = self.savepath

        save_file = Path(savepath)

        return save_file.is_file()
