#!/usr/bin/env python3.8

import textwrap
import random

from os import name
from os import system
from time import sleep

from monster import Monster
from player import Player

indent = ' ' * 6

def clear_screen() -> None:
    system('cls' if name=='nt' else 'clear')

def present_header() -> None:
    clear_screen()

    welcome_text = 'Prepare to enjoy the best in monster companionship as you adventure out into the wilds together!'

    print(f'{"-" * 70}')
    print(f'{"Welcome to Elemental Monsters!":^70}')
    print(f'{"---":^70}')

    for line in textwrap.wrap(welcome_text, width=50):
        print(line.center(70))

    print(f'{"-" * 70}\n')

def present_town_menu(player: Player) -> str:
    town_description = 'After looking around, you see that the small bustling town square offers you the following services:'
    menu_options = ['h', 'v', 'r', 'q']
    menu = (
        f'Welcome to the town of Everlook!\n'
        f'\n'
        f'{textwrap.fill(town_description, width=60)}\n'
        f'\n'
        f'{indent}(H)unt for local monsters\n'
        f'{indent}(V)isit the healers of the local sanctuary\n'
        f'{indent}(R)ookery where your companion is resting\n'
        f'\n'
        f'{indent}(Q)uit for the day and head to the inn\n'
    )

    clear_screen()
    print(menu)

    response = None

    while not response in menu_options:
        try:
            response = input(f'What should we do now, {player.name}? ')
            response = response[0].lower()

        except KeyboardInterrupt:
            quit()
            
        except:
            pass

    return response

def hunting_loop(player: Player) -> tuple:
    battles = 0
    wins = 0
    hunt = True

    battle_message = f"You and your companion creep through the dense underbrush and come upon"

    clear_screen()

    while hunt:
        print(battle_message, end='', flush=True)

        for _ in range(3):
            print('.', end='', flush=True)
            sleep(1)

        if random.randint(1, 100) < 5:
            print(" Nothing.")
        else:
            battles += 1
            monster = Monster.random_monster()

            print(f' a level {monster.level} wild {monster.rarity.lower()} ({monster.element}) {monster.name}!\n')

            if player.monster.attack_target(monster) > monster.attack_target(player.monster):
                wins += 1
                print(f'Your {player.monster.name} fought heroically and was victorious!\n')
            else:
                print('You are lucky to make it away! That monster was tougher than it looked...\n')

        response = None

        while not response in ['c', 'q']:
            try:
                response = input('Would you like to (C)ontinue hunting or (Q)uit and return to town? ')
                response = response.lower()

            except KeyboardInterrupt:
                quit()
                
            except:
                pass

        print()

        if response == 'q':
            hunt = False

    return (wins, battles)

def healing(player: Player) -> None:
    healing_text = 'The sanctuary towers above the surrounding buildings like a gray skeletal finger pointing at the gods.  The heat, smoke, and scents of smouldering herbs envelope you as you pass through the large blackened oak doors and you feel like they are trying to drag you down to the cool stone floor.  Glimmering gold, silver, and gems, sparkling in the scant light, remind you that the services offered here don\'t come cheap.'
    menu = (
        f'Santuary of the Blind God\n'
        f'\n'
        f'{textwrap.fill(healing_text, width=60)}\n'
        f'\n'
        f'{"You are unable to afford their services..." if player.gold < 100 else "A figure can barely be seen but beckonds you forward."}\n'
    )

    clear_screen()
    print(menu)
    input("Press ENTER to continue... ")

def monster_info(player) -> None:
    monster = player.monster
    rookery_text = f'You step across the threshold into a dimly lit rookery.  All around you are stalls occupied by monsters from all across the realm.  Off to one side you can hear the familiar sound of your {monster.name}...'
    complex_element = f'{monster.element} ({monster.rarity})'
    current_hp = f'{monster.current_hp} / {monster.hp}'
    menu = (
        f'Everlook Rookery\n'
        f'\n'
        f'{textwrap.fill(rookery_text, width=60)}\n'
        f'\n'
        f'{indent}Name:       {monster.name:>20}\n'
        f'{indent}Element:    {complex_element:>20}\n'
        f'\n'
        f'{indent}Attack:     {monster.attack:>20}\n'
        f'{indent}Defense:    {monster.defense:>20}\n'
        f'{indent}Hit Points: {current_hp:>20}\n'
    )

    clear_screen()
    print(menu)
    input("Press ENTER to continue... ")

def main():
    player_battles = 0
    player_wins = 0

    present_header()
    player = Player.interactive()

    print("Now that you have been introduced, let's head into town", end='', flush=True)

    for _ in range(5):
        print('.', end='', flush=True)
        sleep(1)

    while True:
        action = present_town_menu(player)

        if action == 'q':
            print(f'\nYou\'ve won {player_wins} of {player_battles} battles this session!')
            exit()

        if action == 'h':
            wins, total = hunting_loop(player)

            player_battles += total
            player_wins += wins

        if action == 'v':
            healing(player)

        if action == 'r':
            monster_info(player)

if __name__ == "__main__":
    main()

