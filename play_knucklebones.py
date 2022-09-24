import random
import argparse

from app.knucklebones import KnucklebonesGame, KnucklebonesPlayer

def start_game():
    knucklebones_game = KnucklebonesGame(args.player_names)

    knucklebones_game.loop()

    print("** THANKS FOR PLAYING! **")

    return None


parser = argparse.ArgumentParser(prog="Knucklebones", description="A simple program for playing Knucklebones")
parser.add_argument('-p', '--player-name', action='append', help='Set player names (Up to 2)', dest='player_names')
args = parser.parse_args()

if __name__ == "__main__":
    start_game()
