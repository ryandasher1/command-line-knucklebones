# Command Line Knucklebones

This is a competitive version of Knucklebones, playable by two people from the command line. This game is based off the version of Knucklebones from the videogame Cult of the Lamb, which I am not affiliated with.

## How to Play Knucklebones

The objective is to score more points than your opponent. A round begins by "rolling" a die, and then you place the die in one of three columns. The value of that die is added to your total score. Three dice will slot into each column, and the game will end when one player has filled all of their columns.

You can earn multipliers by putting die of the same value in the same column. The multiplier math is: ({die_value} * {num_of_die_in_column}) * {num_of_die_in_column}.

You can remove your opponent's dice by placing a die of the same value in a matching column. E.g. If your opponent has two sixes in the right column, and you place a six in the right column, their sixes will be removed from the board.

## How to Run Command Line Knucklebones

Requirements: Python3

    python play_knucklebones.py -p Sharon -p Ryan