from app import knucklebones
from app.utils import helpers

import pytest
import mock
import copy


class TestKnucklebonesGame:

    def setup_method(self, method):
        self.game = knucklebones.KnucklebonesGame(['Jane', 'Jill'])
        self.matrices = [self.game.player_one.matrix, self.game.player_two.matrix]
        # This simulates the input for an entire game; and a player declining to play another round.
        self.simulated_game_inputs = ['ENTER', 'L'] * 6 + ['ENTER', 'R'] * 6 + ['ENTER', 'M'] * 5 + ['N']

    @pytest.fixture
    def mock_input(self):
        with mock.patch.object(helpers, 'input') as mock_input:
            yield mock_input

    @pytest.fixture
    def mock_print(self):
        with mock.patch.object(knucklebones, 'print') as mock_print:
            yield mock_print

    @pytest.fixture
    def mock_system(self):
        with mock.patch.object(knucklebones, 'system') as mock_system:
            yield mock_system        

    def test_game_is_initialized_inactive(self):
        assert self.game.active == False

    def test_game_is_initialized_with_no_die_value(self):
        assert self.game.current_die_value == None

    def test_die_lookup_contains_seven_keys(self):
        assert len(self.game.die_render_lookup.keys()) == 7

    def test_die_heights_are_all_the_same_value(self):
        assert len(self.game.render_no_die) == self.game.die_height
        assert len(self.game.render_die_1) == self.game.die_height
        assert len(self.game.render_die_2) == self.game.die_height
        assert len(self.game.render_die_3) == self.game.die_height
        assert len(self.game.render_die_4) == self.game.die_height
        assert len(self.game.render_die_5) == self.game.die_height
        assert len(self.game.render_die_6) == self.game.die_height

    def test_set_player_name_is_called_twice_during_initialization(self):
        assert self.game.player_one.name == 'JANE'
        assert self.game.player_two.name == 'JILL'

    def test_player_order_shuffle(self):
        self.game.set_player_order(self.game.players)

        assert self.game.players == [self.game.player_one, self.game.player_two] or [self.game.player_two, self.game.player_one]

    def test_die_roll_is_bound_to_expected_values(self, mock_input):
        self.game.roll_the_die(self.game.player_one.name)

        assert self.game.current_die_value in [1, 2, 3, 4, 5, 6]

    def test_grid_renders_both_player_matrices(self, mock_print):
        self.game.show_grid(matrices=self.matrices)

        assert mock_print.call_count == (self.game.die_height * len(self.game.player_one.matrix) * 2 + 1)

    def test_scoreboard_renders_at_proper_length(self, capfd):
        self.game.show_grid(matrices=self.matrices)

        out, err = capfd.readouterr()

        assert len(out) == 3102

    def test_scoreboard_renders_player_name(self, capfd):
        self.game.show_grid(matrices=self.matrices)

        out, err = capfd.readouterr()

        assert self.game.player_one.name in out
        assert self.game.player_two.name in out

    def test_scoreboard_renders_player_score(self, capfd):
        self.game.show_grid(matrices=self.matrices)

        out, err = capfd.readouterr()

        assert str(self.game.player_one.score) in out
        assert str(self.game.player_two.score) in out

    def test_screen_is_cleared(self, mock_system):
        self.game.clear_screen()

        assert mock_system.call_count == 1

    def test_game_is_inactive_when_matrix_is_full(self):
        full_matrix = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        self.game.set_game_to_active()
        self.game.check_for_full_matrix(full_matrix)

        assert self.game.active == False

    def test_game_is_active_when_matrix_is_not_full(self):
        partially_full_matrix = [[1, 1, 1], [0, 1, 1], [1, 1, 1]]
        self.game.set_game_to_active()
        self.game.check_for_full_matrix(partially_full_matrix)

        assert self.game.active == True

    def test_winner_is_determined(self, mock_input, capfd):
        mock_input.return_value = 'L'
        self.game.player_one.add_to_matrix(6)

        self.game.determine_game_winner()

        out, err = capfd.readouterr()

        assert self.game.player_one.wins == 1
        assert self.game.player_two.wins == 0
        assert self.game.player_one.name in out
        assert str(self.game.player_one.score) in out
        assert str(self.game.player_two.score) in out

    def test_result_when_game_is_a_draw(self, capfd):
        self.game.determine_game_winner()

        out, err = capfd.readouterr()

        assert self.game.player_one.wins == 0
        assert self.game.player_two.wins == 0
        assert "THE GAME WAS A DRAW! WOW!" in out

    def test_simulated_game_loop(self, mock_system, mock_input):
        with mock.patch.object(knucklebones.random, 'randint') as mock_randint:
            mock_randint.side_effect = [6, 5] * 8 + [6] # Player one receives all sixes; player two receives all fives.

            mock_input.side_effect = self.simulated_game_inputs

            self.game.loop()

            assert mock_system.call_count == 17 # 9 die in each column for each player - 1
            assert self.game.player_one.score == 162 # (6 * 3) * 3 * 3
            assert self.game.player_two.score == 110 # (5 * 3) * 3 * 2 + 20
            assert self.game.player_one.wins == 1
            assert self.game.player_two.wins == 0

    def test_player_board_is_reset_when_playing_another_round(self, mock_system, mock_input):
        with mock.patch.object(knucklebones.random, 'randint') as mock_randint:
            with mock.patch.object(knucklebones.random, 'shuffle') as mock_shuffle:
                mock_shuffle.return_value = [self.game.player_one, self.game.player_two]
                mock_randint.side_effect = [6, 5] * 8 + [6] + [6, 5] * 8 + [6]

                simulated_double_game = self.simulated_game_inputs.copy()
                simulated_double_game[-1] = 'Y'
                simulated_double_game.extend(self.simulated_game_inputs.copy())

                mock_input.side_effect = simulated_double_game

                self.game.loop()

                assert mock_system.call_count == 34
                assert self.game.player_one.score == 162
                assert self.game.player_two.score == 110
                assert self.game.player_one.wins == 2
                assert self.game.player_two.wins == 0

    def test_series_winner_determined(self, capfd):
        for i in range(3):
            self.game.player_one.increment_wins()

        for i in range(5):
            self.game.player_two.increment_wins()

        self.game.determine_series_winner()

        out, err = capfd.readouterr()

        assert self.game.player_two.name in out
        assert str(self.game.player_two.wins) in out
        assert str(self.game.player_one.wins) in out


class TestKnucklebonesPlayer:

    def setup_method(self, method):
        self.player = knucklebones.KnucklebonesPlayer()

    @pytest.fixture
    def mock_input(self):
        with mock.patch.object(helpers, 'input') as mock_input:
            yield mock_input

    def test_player_name_is_initialized_empty(self):
        assert self.player.name == ''

    def test_player_wins_are_initialized_at_zero(self):
        assert self.player.wins == 0

    def test_player_score_is_initialized_at_zero(self):
        assert self.player.score == 0

    def test_players_current_column_selection_is_initialized_as_none(self):
        assert self.player.current_column == None

    def test_players_column_lookup(self):
        assert self.player.column_lookup['L'] == 0
        assert self.player.column_lookup['M'] == 1
        assert self.player.column_lookup['R'] == 2

    def test_player_is_initialized_with_empty_game_board(self):
        assert self.player.matrix == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def test_player_win_total_is_incremented(self):
        assert self.player.wins == 0

        self.player.increment_wins()

        assert self.player.wins == 1

    def test_setting_player_name(self):
        self.player.set_player_name(name='Someone')

        self.player.name == 'SOMEONE'

    def test_setting_player_name_via_input(self, mock_input):
        mock_input.return_value = 'SomeName'

        self.player.set_player_name()

        assert self.player.name == 'SOMENAME'

    def test_long_player_name_gets_truncated(self):
        long_name = "Regina S. Hutchinsonville Jr. Esquire"
        self.player.set_player_name(name=long_name)

        assert self.player.name == long_name[:21].upper() + "..."

    def test_player_adding_die_to_column(self, mock_input):
        mock_input.return_value = 'l'
        die_value = 5

        self.player.add_to_matrix(die_value)

        assert self.player.matrix == [[0, 0, die_value], [0, 0, 0], [0, 0, 0]]
        assert self.player.score == die_value

    def test_choosing_incorrect_column_requires_multiple_inputs(self, mock_input):
        mock_input.side_effect = ['', 'l']

        self.player.add_to_matrix(3)

        assert mock_input.call_count == 2
        assert self.player.matrix == [[0, 0, 3], [0, 0, 0], [0, 0, 0]]

    def test_die_inserted_into_correct_position_in_column(self, mock_input):
        mock_input.side_effect = ['R', 'r', 'M']
        
        self.player.add_to_matrix(5)
        self.player.add_to_matrix(4)
        self.player.add_to_matrix(5)

        assert self.player.matrix == [[0, 0, 0], [0, 0, 5], [0, 4, 5]]
        assert self.player.score == 14

    def test_die_removed_from_matrix_column(self, mock_input):
        mock_input.side_effect = ['L', 'L']
        
        self.player.add_to_matrix(1)
        self.player.add_to_matrix(3)
        self.player.remove_from_matrix(1, 0)

        assert self.player.matrix == [[0, 0, 3], [0, 0, 0], [0, 0, 0]]
        assert self.player.score == 3

    def test_multiple_die_removed_from_matrix_column(self, mock_input):
        mock_input.side_effect = ['L', 'l', 'l']

        for i in range(3):
            self.player.add_to_matrix(2)

        self.player.remove_from_matrix(2, 0)

        assert self.player.matrix == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        assert self.player.score == 0

    def test_column_score_is_updated(self, mock_input):
        mock_input.side_effect = ['M', 'm', 'M']

        for i in range(3):
            self.player.add_to_matrix(6)

        assert self.player.column_scores == [0, 54, 0]
        assert self.player.score == 54

    def test_column_is_full(self, mock_input):
        mock_input.side_effect = ['R', 'R', 'R']

        for i in range(3):
            self.player.add_to_matrix(3)

        assert self.player.is_column_full() == True

    def test_column_is_not_full(self, mock_input):
        mock_input.side_effect = ['L', 'L']
        for i in range(2):
            self.player.add_to_matrix(3)

        assert self.player.is_column_full() == False
