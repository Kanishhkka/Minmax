from copy import deepcopy
from math import inf


class Position(object):

    def __init__(self, table, white_to_move=True):
        self._table = table
        self._next_moves = None
        self._game_end = False
        self._white_to_move = white_to_move
        self._evaluation = 0

    def __gt__(self, other):
        return self._evaluation > other.get_evaluation()

    def __ge__(self, other):
        return self._evaluation >= other.get_evaluation()

    def __le__(self, other):
        return self._evaluation <= other.get_evaluation()

    def __lt__(self, other):
        return self._evaluation < other.get_evaluation()

    def __eq__(self, other):
        return self._evaluation == other.get_evaluation()

    def get_game_end(self):
        return self._game_end

    def set_white_to_move(self, value):
        self._white_to_move = value

    def get_white_to_move(self):
        return self._white_to_move

    def set_evaluation(self, new_eval):
        self._evaluation = new_eval

    def get_next_moves(self, forced=False):
        if self._next_moves is None:
            self.generate_next_moves(forced)
        return self._next_moves

    def get_evaluation(self):
        return self._evaluation

    def get_table(self):
        return self._table

    def count_pieces(self):
        num_white = 0
        num_black = 0
        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._table[i][j] == 'b':
                    num_white += 1
                if self._table[i][j] == 'c':
                    num_black += 1
                
        return num_white, num_black

    def find_move_played(self, previous):
        move = []
        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._table[i][j] != previous[i][j]:
                    move.append((i, j))

        return move

    def evaluate_state_ending(self):
        
        white_value = 0
        black_value = 0
        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._table[i][j] == 'b':
                    white_value += 2
                if self._table[i][j] == 'c':
                    black_value += 2
        self._evaluation = black_value - white_value
        return self._evaluation

    # def evaluate_state(self):
    #     
    #     white_value = 0
    #     black_value = 0
    #     for i in range(len(self._table)):
    #         for j in range(len(self._table[i])):
    #             if self._table[i][j] == 'b':
    #                 if i < 4:
    #                     white_value += 7
    #                 else:
    #                     white_value += 5
    #             if 

    def find_capturing_moves(self):
        captured = []
        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._white_to_move and (self._table[i][j] == 'b' or self._table[i][j] == 'B'):
                    move = self.find_valid_moves_for_piece((i, j))
                    for d in move:
                        if i - d[0] == 2 or i - d[0] == -2:
                            captured.append((i, j))
                            break
                if not self._white_to_move and (self._table[i][j] == 'c' or self._table[i][j] == 'C'):
                    move = self.find_valid_moves_for_piece((i, j))
                    for d in move:
                        if i - d[0] == 2 or i - d[0] == -2:
                            captured.append((i, j))
                            break
        return captured

    def evaluate_state(self):
       
        white_value = 0
        black_value = 0
        num_white = 0
        num_black = 0

        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._table[i][j] == 'b':
                    num_white += 1
                    if 2 < i < 5 and 1 < j < 6: 
                        white_value += 50
                    elif i < 4:
                        white_value += 45
                    else:
                        white_value += 40
                if self._table[i][j] == 'c':
                    num_black += 1
                    if 2 < i < 5 and 1 < j < 6:  
                        black_value += 50
                    elif i > 3:
                        black_value += 45
                    else:
                        black_value += 40

        self._evaluation = black_value - white_value
        if num_white == 0:
            self._evaluation = inf
            self._game_end = True
        if num_black == 0:
            self._evaluation = -inf
            self._game_end = True
        return self._evaluation

    # def evaluate_state_ending(self, x=None):
    #     
    #     white_value = 0
    #     black_value = 0
    #     num_white = 0
    #     num_black = 0
    #
    #     white_kings = 0
    #     black_kings = 0
    #
    #     for i in range(len(self._table)):
    #         for j in range(len(self._table[i])):
    #             if self._table[i][j] == 'b':
    #                 num_white += 1
    #                 if 2 < i < 5 and 1 < j < 6:  
    #                     white_value += 50
    #                 elif i < 4:
    #                     white_value += 45
    #                 else:
    #                     white_value += 40
    #             if self._table[i][j] == 'B':
    #             ack_value += 45
    #                 el

    def generate_next_moves(self, forced=False):
        self._next_moves = []
        captures = []
        all_moves = []

        for i in range(len(self._table)):
            for j in range(len(self._table[i])):
                if self._white_to_move:
                    if self._table[i][j] == "b" :
                        valid_moves = self.find_valid_moves_for_piece(
                            (i, j), forced)
                        for move in valid_moves:
                            if move[0] - i == 2 or move[0] - i == -2:
                                new_table = self.generate_new_state(
                                    (i, j), move)
                                position = Position(
                                    new_table, not self._white_to_move)
                                captures.append(position)
                            else:
                                new_table = self.generate_new_state(
                                    (i, j), move)
                                position = Position(
                                    new_table, not self._white_to_move)
                                all_moves.append(position)

                else:
                    if self._table[i][j] == "c":
                        valid_moves = self.find_valid_moves_for_piece(
                            (i, j), forced)
                        for move in valid_moves:
                            if move[0] - i == 2 or move[0] - i == -2:
                                new_table = self.generate_new_state(
                                    (i, j), move)
                                position = Position(
                                    new_table, not self._white_to_move)
                                captures.append(position)
                            else:
                                new_table = self.generate_new_state(
                                    (i, j), move)
                                position = Position(
                                    new_table, not self._white_to_move)
                                all_moves.append(position)
        if forced and len(captures) > 0:
            self._next_moves = captures
        else:
            self._next_moves = captures + all_moves

    def generate_new_state(self, figure, move):
        table_copy = deepcopy(self._table)
        figure_type = table_copy[figure[0]][figure[1]]
        if figure_type == "b" :
            if move[0] == 0:  
                table_copy[figure[0]][figure[1]] = "b"
            if figure[0] - move[0] == 2 or figure[0] - move[0] == -2:
                row = figure[0] + (move[0] - figure[0]) // 2
                column = figure[1] + (move[1] - figure[1]) // 2
                table_copy[row][column] = "."
        if figure_type == "c" :
            if move[0] == 7:  
                table_copy[figure[0]][figure[1]] = "c"
            if figure[0] - move[0] == 2 or figure[0] - move[0] == -2:
                row = figure[0] + (move[0] - figure[0]) // 2
                column = figure[1] + (move[1] - figure[1]) // 2
                table_copy[row][column] = "."
        table_copy[figure[0]][figure[1]], table_copy[move[0]][move[1]] = table_copy[move[0]][move[1]], \
            table_copy[figure[0]][figure[1]]

        return table_copy

    def play_move(self, figure, move):
        table = self.generate_new_state(figure, move)
        position = None
        for state in self.get_next_moves():
            if table == state.get_table():
                position = state
                break
        return position

    def find_valid_moves_for_piece(self, coord, forced=False):
        captures = []
        valid_moves = []
        
        figure = self._table[coord[0]][coord[1]]
        if figure != "b":
            if 0 <= coord[0] < 7:
                if (coord[1] - 1) >= 0:
                    if self._table[coord[0] + 1][coord[1] - 1] == '.':
                        valid_moves.append((coord[0] + 1, coord[1] - 1))
                   
                    elif coord[0] + 2 < 8 and coord[1] - 2 >= 0:
                        if self._table[coord[0] + 2][coord[1] - 2] == '.':
                            if figure.lower() != self._table[coord[0] + 1][coord[1] - 1].lower():
                                captures.append((coord[0] + 2, coord[1] - 2))
                                # valid_moves.append((coord[0] + 2, coord[1] - 2))
                if (coord[1] + 1) < 8:
                    if self._table[coord[0] + 1][coord[1] + 1] == '.':
                        valid_moves.append((coord[0] + 1, coord[1] + 1))
                    
                    elif coord[0] + 2 < 8 and coord[1] + 2 < 8:
                        if self._table[coord[0] + 2][coord[1] + 2] == '.':
                            if figure.lower() != self._table[coord[0] + 1][coord[1] + 1].lower():
                                captures.append((coord[0] + 2, coord[1] + 2))
                                # valid_moves.append((coord[0] + 2, coord[1] + 2))

        if figure != "c":
            if 0 < coord[0] < 8:
                if (coord[1] - 1) >= 0:
                    if self._table[coord[0] - 1][coord[1] - 1] == '.':
                        valid_moves.append((coord[0] - 1, coord[1] - 1))
                    
                    elif coord[0] - 2 >= 0 and coord[1] - 2 >= 0:
                        if self._table[coord[0] - 2][coord[1] - 2] == '.':
                            if figure.lower() != self._table[coord[0] - 1][coord[1] - 1].lower():
                                captures.append((coord[0] - 2, coord[1] - 2))
                                # valid_moves.append((coord[0] - 2, coord[1] - 2))

                if (coord[1] + 1) < 8:
                    if self._table[coord[0] - 1][coord[1] + 1] == '.':
                        valid_moves.append((coord[0] - 1, coord[1] + 1))
                    
                    elif coord[0] - 2 >= 0 and coord[1] + 2 < 8:
                        if self._table[coord[0] - 2][coord[1] + 2] == '.':
                            if figure.lower() != self._table[coord[0] - 1][coord[1] + 1].lower():
                                captures.append((coord[0] - 2, coord[1] + 2))
                                # valid_moves.append((coord[0] - 2, coord[1] + 2))

        if forced and len(captures) != 0:
            return captures
        return captures + valid_moves
