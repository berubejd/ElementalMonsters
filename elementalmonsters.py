#!/usr/bin/env python3.8

import textwrap
import random
import sys

from os import name
from os import system
from time import sleep

from monster import Monster
from player import Player
from datetime import datetime
from datetime import timedelta

indent = " " * 6


def clear_screen() -> None:
    system("cls" if name == "nt" else "clear")


def present_header() -> None:
    clear_screen()

    welcome_text = "Prepare to enjoy the best in monster companionship as you adventure out into the wilds together!"

    print(f'{"-" * 70}')
    print(f'{"Welcome to Elemental Monsters!":^70}')
    print(f'{"---":^70}')

    for line in textwrap.wrap(welcome_text, width=50):
        print(line.center(70))

    print(f'{"-" * 70}\n')


def present_town_menu(player: Player) -> str:
    town_description = "After looking around, you see that the small bustling town square offers you the following services:"
    menu_options = ["h", "v", "s", "q"]
    menu = (
        f"Welcome to the town of Everlook!\n"
        f"\n"
        f"{textwrap.fill(town_description, width=70)}\n"
        f"\n"
        f"{indent}(H)unt for local monsters\n"
        f"{indent}(V)isit the healers of the local sanctuary\n"
        f"{indent}(S)tables where your companion is resting\n"
        f"\n"
        f"{indent}(Q)uit for the day and head to the inn\n"
    )

    clear_screen()
    print(menu)

    response = None

    while not response in menu_options:
        try:
            response = input(f"What should we do now, {player.name}? ")
            response = response[0].lower()

        except KeyboardInterrupt:
            sys.exit()

        except:
            pass

    return response


def hunting(player: Player) -> tuple:
    # Set up battle stats
    battles = 0
    wins = 0
    hunt = True

    battle_message = (
        f"\nYou and your companion creep through the dense underbrush and come upon"
    )

    while hunt:
        # Prep the hunting screen
        clear_screen()
        print(battle_message, end="", flush=True)

        for _ in range(3):
            print(".", end="", flush=True)
            sleep(1)

        print("\n")

        # Determine if a monster is encountered or if the player will rest
        if random.randint(1, 100) <= 5:
            print(f'{"Nothing.  You take this opportunity to rest.":^60}\n')
            player.monster.current_hp = player.monster.hp
            result = "Rested"

        else:
            battles += 1

            # Provide a random monster between -2 and +1 levels of the players

            if player.monster.level == 1:
                monster = Monster.random_monster()
            else:
                min_level = max(player.monster.level - 2, 1)
                max_level = min(player.monster.level + 1, 10)
                monster = Monster.random_monster(
                    level=random.randint(min_level, max_level)
                )

            message = (
                f'{"An" if monster.rarity[0].lower() in "aeiou" else "A"} {monster.rarity.lower()} {monster.name}!\n'
                f"Prepare for Battle!\n"
            )

            for line in message.splitlines():
                print(line.center(60))

            sleep(3)
            result = combat(player, monster)

        if result == "Won" or result == "Captured":
            wins += 1

        # Determine if the player would like to continue (default to 'q' if the player's monster is out of health)
        response = "q" if result == "Lost" or result == "Captured" else None

        while not response in ["h", "q"]:
            try:
                current_hp = f"{player.monster.current_hp} / {player.monster.hp}"
                current_xp = (
                    f"{player.monster.experience} / {player.monster.experience_needed}"
                )

                print(
                    f'\n[ {player.monster.name} - Level: {player.monster.level} - Exp: {current_xp} - Health: {current_hp} {"- Healing " if player.blessing > datetime.now() else ""}]'
                )
                response = input(
                    "Would you like to continue (H)unting or (Q)uit for town? "
                )
                response = response.lower()

            except KeyboardInterrupt:
                sys.exit()

            except:
                pass

        print()

        if response == "q":
            if wins > 0:
                bounty = wins * 5
                player.gold += bounty
                print(f"You have earned {bounty} gold in bounties!")
                player.save_player()

            sleep(3)
            hunt = False

    return (wins, battles)


def combat(player: Player, monster: Monster) -> str:
    companion = player.monster

    clear_screen()
    print(f'\n{"BATTLE!":^70}')

    battle = True

    while battle:
        companion_hp = f"{companion.current_hp} / {companion.hp}"
        companion_element = f"{companion.element} ({companion.rarity})"
        monster_hp = f"{monster.current_hp} / {monster.hp}"
        monster_element = f"{monster.element} ({monster.rarity})"

        monster_display = (
            f'{indent:<10}{"Your Monster":^20}{" ":^10}{"Wild Monster":^20}{indent:>10}\n'
            f'{"-" * 50:^70}\n'
            f"{indent:<10}{companion.name:<25}{monster.name:>25}{indent:>10}\n"
            f'{indent:<10}{companion_element:<20}{"Element":^10}{monster_element:>20}{indent:>10}\n'
            f'{indent:<10}{companion.level:<20}{"Level":^10}{monster.level:>20}{indent:>10}\n'
            f"\n"
            f'{indent:<10}{companion_hp:<20}{"Health":^10}{monster_hp:>20}{indent:>10}\n'
        )

        print()
        print(monster_display)

        response = None

        while not response in ["f", "h", "r"]:
            try:
                response = input(
                    f'Would you like to (F)ight{", (H)eal," if player.blessing > datetime.now() else ""} or (R)un? '
                )
                response = response.lower()

            except KeyboardInterrupt:
                sys.exit()

            except:
                pass

        print()

        # Handle player's turn
        if response == "f":
            damage = companion.attack_target(monster)

            if damage == 0:
                print(f"Your {companion.name} missed the {monster.name}.")
            else:
                print(
                    f"Your {companion.name} hit the {monster.name} for {damage} damage",
                    end="",
                )

                if monster.damage_taken(damage) == 0:
                    print(f" and defeated it!")

                    response = None

                    while not response in ["y", "n"]:
                        try:
                            response = input(
                                f"\nWould you like to capture this monster to replace your {companion.name}? (Y/N) "
                            )
                            response = response.lower()

                        except KeyboardInterrupt:
                            sys.exit()

                        except:
                            pass

                        if response == "y":
                            player.monster = monster
                            print(
                                f"Let's head back to town with your new {player.monster.name} for some rest."
                            )

                            return "Captured"

                    if player.monster.gain_xp(5):
                        print(f"\nCongratulations! Your monster has grown stronger!")
                        player.save_player()

                    return "Won"
                else:
                    print(".")

        if response == "h":
            if player.blessing > datetime.now():
                healing = random.randint(1, 3)
                print(f"You healed your {companion.name} for {healing} health.")

                companion.healing(healing)

        if response == "r":
            # Monster gets a free hit on the way out
            print(f"You attempt to run away but the {monster.name} charges!")
            battle = False

        # Handle monster's attack
        damage = monster.attack_target(companion)

        if damage == 0:
            print(f"The {monster.name} missed your {companion.name}.")
        else:
            print(
                f"The {monster.name} hit your {companion.name} for {damage} damage",
                end="",
            )

            if companion.damage_taken(damage) == 0:
                # Player lost so we need to head back to town
                print(f" and knocked it out!")
                print("Let's head back to town...\n")

                return "Lost"
            else:
                print(".")

    return "Fled"


def healer(player: Player) -> None:
    healing_text = "The sanctuary towers above the surrounding buildings like a gray skeletal finger pointing at the gods.  The heat, smoke, and scents of smouldering herbs envelope you as you pass through the large blackened oak doors and you feel like they are trying to drag you down to the cool stone floor.  Glimmering gold, silver, and gems, sparkling in the scant light, remind you that the services offered here don't come cheap."
    healing_intro = (
        f"Santuary of the Blind God\n"
        f"\n"
        f"{textwrap.fill(healing_text, width=70)}\n"
    )
    monster_healed = (
        f"Just being in this place you and your companion feel more rested.\n"
        f"\n"
        "Your {} has been completely healed!\n".format(player.monster.name).center(70)
    )
    healing_blessing = "A figure can barely be seen but beckons you forward.  In hushed tones the priest explains that for 40g he can provide you a blessing of healing which will allow you to heal your pet in the wilderness."
    healing_level1 = "Since your companion is young and going to help the village, the priest extends his blessing for free, however."

    clear_screen()
    print(healing_intro)

    if player.monster.current_hp < player.monster.hp:
        print(monster_healed)

        player.monster.current_hp = player.monster.hp

    print(f"{textwrap.fill(healing_blessing, width=70)}\n")

    if player.blessing > datetime.now():
        minutes, seconds = divmod((player.blessing - datetime.now()).seconds, 60)
        print(
            f'You have {str(minutes) + " minutes and" if minutes > 0 else ""} {seconds} seconds remaining of your blessing.\n'
        )

    else:
        if player.monster.level == 1:
            print(f"{textwrap.fill(healing_level1, width=70)}\n")
            player.blessing = datetime.now() + timedelta(minutes=10)

        elif player.gold >= 40:
            response = None

            while not response in ["y", "n"]:
                try:
                    response = input(
                        f"Would you like to purchase this blessing? [ {player.gold} available ] (Y/N) "
                    )
                    response = response.lower()

                except KeyboardInterrupt:
                    sys.exit()

                except:
                    pass

                if response == "y":
                    player.gold -= 40
                    player.blessing = datetime.now() + timedelta(minutes=10)

                    print()
                    print(f'{"You feel a warmth rush over you!":^70}\n')

        else:
            print(f"You are unable to afford their blessings...\n")

    try:
        input("Press ENTER to continue... ")
    except KeyboardInterrupt:
        sys.exit()


def monster_info(player) -> None:
    monster = player.monster
    stable_text = f"You step across the threshold into the dimly lit stables.  All around you are stalls occupied by monsters from all across the realm.  Off to one side you can hear the familiar sound of your {monster.name}..."
    complex_element = f"{monster.element} ({monster.rarity})"
    current_hp = f"{monster.current_hp} / {monster.hp}"
    current_xp = f"{monster.experience} / {monster.experience_needed}"
    menu = (
        f"Everlook Stables\n"
        f"\n"
        f"{textwrap.fill(stable_text, width=70)}\n"
        f"\n"
        f"{indent}Name:       {monster.name:>20}\n"
        f"{indent}Element:    {complex_element:>20}\n"
        f"\n"
        f"{indent}Level:      {monster.level:>20}\n"
        f"{indent}Experience: {current_xp:>20}\n"
        f"\n"
        f"{indent}Strength:   {monster.strength:>20}\n"
        f"{indent}Defense:    {monster.defense:>20}\n"
        f"{indent}Hit Points: {current_hp:>20}\n"
    )

    clear_screen()
    print(menu)
    input("Press ENTER to continue... ")


def main():
    player_battles = 0
    player_wins = 0

    present_header()
    player = Player.interactive()

    if not player.save_exists():
        player.save_player()

    print()
    print("Now that you have been introduced, let's head into town", end="", flush=True)

    for _ in range(5):
        print(".", end="", flush=True)
        sleep(1)

    while True:
        action = present_town_menu(player)

        if action == "q":
            print(
                f"\nYou've won {player_wins} of {player_battles} battles this session!"
            )
            player.save_player()
            return

        if action == "h":
            if player.monster.current_hp == 0:
                print(
                    f"\nYour {player.monster.name} needs some rest.\nMaybe a (v)isit to the healer will help get them ready for the hunt? ",
                    end="",
                )
                sleep(3)
                continue

            wins, total = hunting(player)

            player_battles += total
            player_wins += wins

        if action == "v":
            healer(player)

        if action == "s":
            monster_info(player)


if __name__ == "__main__":
    main()
