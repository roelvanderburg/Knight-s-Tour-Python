import numpy as np
import sys
# sys.setrecursionlimit(30000)

class Board:

    def __init__(self, size_board, start_pos):

        self.size_board = size_board-1
        self.board = np.zeros((size_board, size_board))
            self.current_pos = start_pos
        self.integer = 1
        self.board[self.current_pos[0], self.current_pos[1]] = 1

        self.board_list = []
        self.board_list.append(self.board)

        self.position_list = []
        self.position_list.append(start_pos)

    def printboard(self):
        print(self.board)
        print("---------")

    def pin_board(self, new_pos):
        self.integer += 1
        self.board[new_pos[0], new_pos[1]] = self.integer
        copy_of_current_board = np.copy(self.board)

        self.board_list.append(copy_of_current_board)

    def check_if_position(self, temp_pos):

        if (temp_pos[0] <= self.size_board and temp_pos[0] >= 0 and temp_pos[1] <= self.size_board
                and temp_pos[1] >= 0 and self.board[temp_pos[0], temp_pos[1]] == 0):
            return True
        else:
            return False

    def number_of_onward_moves(self,new_pos):

        moves = [moverightup, moveleftup, moverightdown, moveleftdown, moverightup2, moveleftup2, moverightdown2,
                 moveleftdown2]
        new_moves = 0

        for move in moves:
            temp_new_pos = move(new_pos)

            if self.check_if_position(temp_new_pos):

                # Why need a np.copy with assignment
                temp_board = np.copy(self.board)
                dummy_integer = self.integer + 1

                temp_board[temp_new_pos[0], temp_new_pos[1]] = dummy_integer

                for board_hist in self.board_list:
                    if np.array_equal(board_hist, temp_board):
                        return
                new_moves += 1

        return new_moves

    def last_check_move(self, move):
        temp_new_pos = move(self.current_pos)

        if self.check_if_position(temp_new_pos):

            temp_board = np.copy(self.board)
            dummy_integer = self.integer + 1

            temp_board[temp_new_pos[0], temp_new_pos[1]] = dummy_integer

            for board_hist in self.board_list:
                if np.array_equal(board_hist, temp_board):
                    return False
            self.position_list.append(temp_new_pos)
            self.current_pos = temp_new_pos
            self.pin_board(temp_new_pos)
            return True
        return False

    def check_move(self, move):
        temp_new_pos = move(self.current_pos)

        if self.check_if_position(temp_new_pos):

            # Why need a np.copy with assignment
            temp_board = np.copy(self.board)
            dummy_integer = self.integer + 1

            temp_board[temp_new_pos[0], temp_new_pos[1]] = dummy_integer

            for board_hist in self.board_list:
                if np.array_equal(board_hist, temp_board):
                    return 0
            onward_moves = self.number_of_onward_moves(temp_new_pos)

            return onward_moves
        return 0

    def undo_last_move(self):

        self.board[self.current_pos[0], self.current_pos[1]] = 0
        self.current_pos = self.position_list[-2]
        self.integer -= 1
        self.position_list.pop()

    def start_tour(self):
        moves = [moverightup, moveleftup, moverightdown, moveleftdown, moverightup2, moveleftup2, moverightdown2,
                 moveleftdown2]


        squared = self.size_board+1


        while self.integer != (squared*squared):

            self.printboard()

            least_options = []
            for index, move in enumerate(moves):

                least_options.append(self.check_move(move))

            if self.integer == ((squared*squared)-1):
                for move in moves:
                    if self.last_check_move(move):
                        self.printboard()
                        return

            elif np.count_nonzero(least_options) == 0:
                self.undo_last_move()

            else:
                for i in range(len(least_options)):
                    if least_options[i] == 0:
                        least_options[i] = 100
                least_move_int = np.argmin(least_options)
                min_move = moves[least_move_int]

                temp_new_pos = min_move(self.current_pos)

                self.position_list.append(temp_new_pos)
                self.current_pos = temp_new_pos
                self.pin_board(temp_new_pos)


board = Board(size_board=5, start_pos=[3,3])

# print(board.start_tour ())

def moverightup(p):
    new_position = [p[0]+1, p[1]+2]
    return new_position

def moveleftup(p):
    new_position = [p[0]-1, p[1]+2]
    return new_position

def moverightdown(p):
    new_position = [p[0]+1, p[1]-2]
    return new_position

def moveleftdown(p):
    new_position = [p[0]-1, p[1]-2]
    return new_position

def moverightup2(p):
    new_position = [p[0]+2, p[1]+1]
    return new_position

def moveleftup2(p):
    new_position = [p[0]-2, p[1]+1]
    return new_position

def moverightdown2(p):
    new_position = [p[0]+2, p[1]-1]
    return new_position

def moveleftdown2(p):
    new_position = [p[0]-2, p[1]-1]
    return new_position
