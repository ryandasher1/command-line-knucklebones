import random
import os
import sys

class KnucklebonesGame:

    def __init__(self):
        self._active = True
        self._current_die_value = None
        self.die_render_lookup = {
            '0': self.render_no_die,
            '1': self.render_die_1,
            '2': self.render_die_2,
            '3': self.render_die_3,
            '4': self.render_die_4,
            '5': self.render_die_5,
            '6': self.render_die_6
        }

    @property
    def active(self):
        return self._active

    @property
    def current_die_value(self):
        return self._current_die_value

    @property
    def render_no_die(self):
        return ("           ",
                "           ",
                "           ",
                "           ",
                "           ")


    @property
    def render_die_1(self):
        return ("┌─────────┐",
                "│         │",
                "│    ●    │",
                "│         │",
                "└─────────┘")

    @property
    def render_die_2(self):
        return ("┌─────────┐",
                "│    ●    │",
                "│         │",
                "│    ●    │",
                "└─────────┘")

    @property
    def render_die_3(sef):
        return ("┌─────────┐",
                "│  ●      │",
                "│    ●    │",
                "│      ●  │",
                "└─────────┘")

    @property
    def render_die_4(self):
        return ("┌─────────┐",
                "│  ●   ●  │",
                "│         │",
                "│  ●   ●  │",
                "└─────────┘")

    @property
    def render_die_5(self):
        return ("┌─────────┐",
                "│  ●   ●  │",
                "│    ●    │",
                "│  ●   ●  │",
                "└─────────┘")

    @property
    def render_die_6(self):
        return ("┌─────────┐",
                "│  ●   ●  │",
                "│  ●   ●  │",
                "│  ●   ●  │",
                "└─────────┘")

    @property
    def die_height(self):
        return len(self.render_die_1)

    def set_player_order(self, players):
        """
        Choose a random player to make the first roll.
        """
        random.shuffle(players)

        return players

    def roll_the_die(self):
        """
        Let the player "roll" the die; and store the value rolled.
        """
        _ = detect_quit_game(input("\n** PRESS ENTER TO ROLL THE DIE! **"))

        self._current_die_value = random.randint(1, 6)
        print(f"\nYou rolled a {self.current_die_value}!\n")

        return None

    def show_grid(self, matrices):
        """
        Display the game board.
        """
        self._render_player_matrix(matrices[0], reverse=False)

        print(f"\n=======================================\n")

        self._render_player_matrix(matrices[1], reverse=True)

        return None

    def _render_player_matrix(self, matrix, reverse=False):
        """
        Show the layout of the die.
        """
        for i in range(len(matrix)):
            for line in range(self.die_height): # The die need to render line-by-line to show properly on the command line.
                if reverse:
                    index = len(matrix) - i - 1 # The second matrix should render inverted.
                else:
                    index = i

                print(
                    f"{self.die_render_lookup[str(matrix[0][index])][line]} * " \
                    f"{self.die_render_lookup[str(matrix[1][index])][line]} * " \
                    f"{self.die_render_lookup[str(matrix[2][index])][line]}"
                )

        return None

    def check_for_full_matrix(self, matrix):
        """
        Check if a matrix is full, to determine if a game should end.
        """
        open_space = False

        for column in matrix:
            if column[0] == 0: # We only need to check the first index to determine if space is open.
                open_space = True
                break

        if not open_space:
            self._active = False

        return None

    def determine_winner(self, players):
        """
        Show the winner of the game.
        """
        if players[0].score == players[1].score:
            print(f"THE GAME WAS A DRAW! WOW!")
        else:
            if players[0].score > players[1].score:
                winner = players[0].name
            else:
                winner = players[1].name

            print(f"{winner} WAS THE WINNER! THE SCORE WAS {players[0].score} TO {players[1].score}")


class KnucklebonesPlayer:

    def __init__(self):
        self._matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self._column_scores = [0, 0, 0]
        self._name = ''
        self.column_lookup = {
            'L': 0,
            'M': 1,
            'R': 2
        }

    @property
    def name(self):
        return self._name

    @property
    def matrix(self):        
        return self._matrix

    @property
    def score(self):
        return sum(self.column_scores)

    @property
    def current_column(self):
        return self._current_column

    @property
    def column_scores(self):
        return self._column_scores

    def set_player_name(self, name=None):
        """
        Pull name from script arguments, otherwise ask for input.
        """
        if name:
            self._name = name
        else:
            while not self.name.strip(' '):
                self._name = detect_quit_game(input("Please enter player name >> "))

        return None

    def add_to_matrix(self, die_value):
        """
        Prompt the player to choose the column where they wish to add their rolled value.
        """
        def choose_column():
            self._current_column = detect_quit_game(
                input("Please choose a column to insert your die. (L)eft, (M)iddle, or (R)ight >> ")
            )

            if self.current_column.upper() not in ['L', 'M', 'R']:
                print(f"Please put a valid entry of L, M, or R.")
                choose_column()
            else:
                self._current_column = self.column_lookup[self.current_column.upper()]

                if self.is_column_full():
                    print(f"Select a different column; the column you selected is full.")
                    choose_column()
                else:
                    return None

        choose_column()

        highest_open_index = 0
        for i in range(len(self.matrix[self.current_column])):
            if self.matrix[self.current_column][i] == 0:
                highest_open_index = i
            else:
                break # We've got the highest index.

        self.matrix[self.current_column][highest_open_index] = die_value

        self.update_column_score(self.current_column)

        return None

    def remove_from_matrix(self, die_value, column_index):
        """
        Check if the opposing player added a matching value to a matching column;
        and remove values from current player's matrix.
        """
        self.matrix[column_index] = [n for n in self.matrix[column_index] if n != die_value]
        
        if len(self.matrix[column_index]) < 3:
            while len(self.matrix[column_index]) < 3:
                self.matrix[column_index].insert(0, 0)

            self.update_column_score(column_index) # This only needs to recalculate if values have been removed.

        return None

    def update_column_score(self, column_index):
        """
        Update the specified column's score after an action happened.
        """
        column = self.matrix[column_index].copy()
        column.sort()

        matches, idx = 0, 1
        for n in column:
            if n == column[idx]:
                matches += 1
                match_value = n

            idx += 1
            if idx >= len(column):
                break

        if matches:
            # TODO: Less hardcoding here.
            if matches < 2:
                remainder_value = [n for n in column if n != match_value][0]
            else:
                remainder_value = 0

            matches += 1
            self._column_scores[column_index] = (match_value * matches) * matches + remainder_value
        else:
            self._column_scores[column_index] = sum(column)

        return None

    def is_column_full(self):
        """
        Check if column can accept new die values.
        """
        column = self.matrix[self.current_column]

        for i in column:
            if i == 0: return False

        return True

def detect_quit_game(input_value):
    """
    Allow the ability to quit the game early on input.
    """
    if input_value.upper() == "Q":
        print("Game ended early after pressing 'Q'!")
        sys.exit(0)

    return input_value
