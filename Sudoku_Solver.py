import numpy as np
from copy import deepcopy

x = 0

class SudokuSolver:

    def __init__(self, grid: np.array):
        """
        Automatic sudokusolver
        :param grid: starting grid
        """

        # Current grid
        self.sudo_grid = grid

        # List of all seen grids
        self.grid_list = []
        self.grid_list.append(np.copy(self.sudo_grid))

    def print_grid(self):
        """
        Print Sudo_grid in a human readable form
        """
        for grid_n, row in enumerate(self.sudo_grid):
            for pos, number in enumerate(row):
                print(number, end=' ')
                if pos == 2 or pos == 5:
                    print(' | ', end='')
            print('')
            if grid_n == 2 or grid_n == 5:
                print("-----------------------")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    def check_axis(self, pos: list, number: int) -> bool:
        """
        Check x and y axis of the position for having a double number
        return True if number not in axis
        :param pos: first int row, second int column
        :param number: number to be added
        :return:
        """

        if np.all(self.sudo_grid[:, pos[1]] != number) and np.all(self.sudo_grid[pos[0], :] != number):
            return True
        else:
            return False

    def check_square(self, pos: list, number: int) -> bool:
        """
        Check square belonging to position for having double number
        :param pos:  list of row and column number
        :param number:
        :return:
        """
        # First 1 Column
        if pos[0] <= 2 and pos[1] <= 2:
            return np.all(self.sudo_grid[0:3, 0:3] != number)

        if 5 >= pos[0] > 2 >= pos[1]:
            return np.all(self.sudo_grid[3:6, 0:3] != number)

        if 5 < pos[0] <= 8 and pos[1] <= 2:
            return np.all(self.sudo_grid[6:9, 0:3] != number)

        # Second 2 column
        if pos[0] <= 2 and 3 <= pos[1] <= 5:
            return np.all(self.sudo_grid[0:3, 3:6] != number)

        if 2 < pos[0] <= 5 and 3 <= pos[1] <= 5:
            return np.all(self.sudo_grid[3:6, 3:6] != number)

        if 8 >= pos[0] > 5 >= pos[1] >= 3:
            return np.all(self.sudo_grid[6:9, 3:6] != number)

        # Second 3 column
        if pos[0] <= 2 and 6 <= pos[1] <= 8:
            return np.all(self.sudo_grid[0:3, 6:9] != number)

        if 2 < pos[0] <= 5 and 6 <= pos[1] <= 8:
            return np.all(self.sudo_grid[3:6, 6:9] != number)

        if 5 < pos[0] <= 8 and 6 <= pos[1] <= 8:
            return np.all(self.sudo_grid[6:9, 6:9] != number)

        return True

    def check_board_seen(self, temp_board: np.array) -> bool:
        """
        Check if board has been seen
        return true is board is not yet seen
        :param temp_board: np.array of previous board
        :return:
        """
        for board_hist in self.grid_list:
            if np.array_equal(board_hist, temp_board):
                return False
        return True

    def undo_move(self):
        """
        Undo last move. ie set the current board to the last one in the grid list.
        """
        self.sudo_grid = np.copy(self.grid_list[-2])

    def solve(self):

        if not np.all(self.sudo_grid != 0):

            for row_n, row_array in enumerate(self.sudo_grid):
                for col_n, number in enumerate(row_array):
                    if number == 0:
                        self.print_grid()
                        for i in range(1, 10):

                            temp_board = np.copy(self.sudo_grid)
                            temp_board[row_n, col_n] = i

                            if self.check_axis([row_n, col_n], i) and self.check_square([row_n, col_n], i) and self.check_board_seen(temp_board):

                                # Assign the number
                                self.sudo_grid[row_n, col_n] = i

                                # Add to list of tried
                                dummy_grid = deepcopy(self.sudo_grid)
                                self.grid_list.append(dummy_grid)

                                # Recursive with next move
                                self.solve()

                        # Undo move and start again
                        self.undo_move()
                        self.solve()
        else:
            print("Sudoku is solved")
            self.print_grid()
            return

""" 
1 4 5 |3 2 7 |6 9 8 
8 3 9 |6 5 4 |1 2 7 
6 7 2 |9 1 8 |5 4 3 
------+------+------
4 9 6 |1 8 5 |3 7 2 
2 1 8 |4 7 3 |9 5 6 
7 5 3 |2 9 6 |4 8 1 
------+------+------
3 6 7 |5 4 2 |8 1 9 
9 8 4 |7 6 1 |2 3 5 
5 2 1 |8 3 9 |7 6 4 

"""

starting_grid = np.array([[1,0,5,0,2,0,6,9,8],
                        [8,0,9,0,5,4,0,2,7],
                        [6,7,0,0,1,0,5,4,3],
                        [4,0,0,1,0,5,3,7,2],
                        [0,1,0,0,7,0,9,0,6],
                        [0,5,3,2,9,6,4,8,1],
                        [0,6,0,5,0,2,8,1,9],
                        [9,8,4,7,0,0,2,3,5],
                        [5,2,1,0,0,0,0,0,0]])

sudok = SudokuSolver(starting_grid)
sudok.solve()
