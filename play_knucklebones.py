import random
import argparse

from app.knucklebones import KnucklebonesGame, KnucklebonesPlayer

def game_loop():
    knucklebones_game = KnucklebonesGame()
    players = [KnucklebonesPlayer(), KnucklebonesPlayer()]
    player_names = args.player_names

    for i in range(len(players)):
        try:
            players[i].set_player_name(player_names[i])
        except (IndexError, TypeError): # Player names not initially provided.
            players[i].set_player_name()
            continue

    players = knucklebones_game.set_player_order(players)
    print(f"{players[0].name} will go first!")
    while knucklebones_game.active:
        index = 0
        for player in players:
            if index:
                opponent = players[index - 1]
            else:
                index += 1
                opponent = players[index]

            knucklebones_game.show_grid(matrices=[players[0].matrix, players[1].matrix])

            knucklebones_game.roll_the_die()

            player.add_to_matrix(knucklebones_game.current_die_value)
            opponent.remove_from_matrix(knucklebones_game.current_die_value, player.current_column)
            print(f"The score is now {players[0].score} to {players[1].score}!")

            knucklebones_game.check_for_full_matrix(player.matrix)

    knucklebones_game.determine_winner(players)


parser = argparse.ArgumentParser(prog="Knucklebones", description="A simple program for playing Knucklebones")
parser.add_argument('-p', '--player-name', action='append', help='Set player names (Up to 2)', dest='player_names')
args = parser.parse_args()

if __name__ == "__main__":
    game_loop()
