from typing import Iterable, List, Optional, Union

"""
Each Sudoku board is represented by a `Board` object, where board[r][c] is either a number
or None (indicating an empty cell).
"""
# type alias for the board
Board = List[List[Union[int, None]]]
EMPTY = None

class Sudoku:

    def __init__(self, width: int = 3, height: Optional[int] = None,
                 board: Optional[Iterable[Iterable[Union[int, None]]]] = None):
        """
        Initializes a Sudoku board

        :param width: Integer representing the width of the small Sudoku grid. Defaults to 3.
        :param height: Optional integer representing the height of the small Sudoku grid.
        If not provided, defaults to the value of `width`.
        :param board: Optional iterable for a the initial state of the Sudoku board.
        If not provided, defaults to empty board.

        :raises AssertionError: If the width, height, or size of the board is invalid.
        :raises Exception: If given board is invalid.
        """
        self.width = width
        self.height = height if height else width
        self.size = self.width * self.height

        assert self.width > 0, 'Width cannot be less than 1'
        assert self.height > 0, 'Height cannot be less than 1'
        assert self.size > 1, 'Board size cannot be 1 x 1'

        if board:
            self.blank_count = 0
            self.board: Board = [
                [cell for cell in row] for row in board]
            # replace anything other than valid integers with an empty cell
            for row in self.board:
                for j in range(len(row)):
                    if not row[j] in range(1, self.size + 1):
                        row[j] = EMPTY
                        self.blank_count += 1
            if self.validate() is False:
                raise Exception('Given board is invalid!')
        else:
            # if board was not passed in, generate empty board
            # TODO: replace with random board generator
            self.board = [[EMPTY] * self.size for _ in range(self.size)]
            self.blank_count = self.size * self.size
        
        self.is_solved = True if self.blank_count == 0 else False
        self.solution = self.board if self.is_solved else None

    def validate(self) -> bool:
        """
        Check if the board is valid, i.e. no number is repeated in a row/column/box.
        (Note that this does not automatically mean that a solution exists.
        """
        row_numbers = [[False for _ in range(self.size)]
                       for _ in range(self.size)]
        col_numbers = [[False for _ in range(self.size)]
                       for _ in range(self.size)]
        box_numbers = [[False for _ in range(self.size)]
                       for _ in range(self.size)]

        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                box = (row // self.height) * self.height + (col // self.width)
                if cell == EMPTY:
                    continue
                elif isinstance(cell, int):
                    # check if the number in this cell has appeared in row/col/box before
                    if row_numbers[row][cell - 1]:
                        return False
                    elif col_numbers[col][cell - 1]:
                        return False
                    elif box_numbers[box][cell - 1]:
                        return False
                    row_numbers[row][cell - 1] = True
                    col_numbers[col][cell - 1] = True
                    box_numbers[box][cell - 1] = True
        return True


    def get_board_ascii(self) -> str:
        table = ''
        cell_length = len(str(self.size))
        format_int = '{0:0' + str(cell_length) + 'd}'
        for i, row in enumerate(self.board):
            if i == 0:
                table += ('+-' + '-' * (cell_length + 1) *
                          self.width) * self.height + '+' + '\n'
            table += (('| ' + '{} ' * self.width) * self.height + '|').format(*[format_int.format(
                x) if x != EMPTY else ' ' * cell_length for x in row]) + '\n'
            if i == self.size - 1 or i % self.height == self.height - 1:
                table += ('+-' + '-' * (cell_length + 1) *
                          self.width) * self.height + '+' + '\n'
        return table
    
    def __str__(self) -> str:
        return '''
---------------------------
{}x{} ({}x{}) SUDOKU PUZZLE
---------------------------
{}
        '''.format(self.size, self.size, self.width, self.height, self.get_board_ascii())
    

if __name__ == '__main__':
    test_sudoku = Sudoku(
        board = [
        [0,0,0,0,0,4,0,0,0],
        [0,4,0,0,6,0,0,0,0],
        [6,3,0,7,0,9,0,0,2],
        [1,2,4,0,0,6,0,0,5],
        [0,0,3,9,0,0,0,0,0],
        [0,0,0,0,4,2,0,0,3],
        [0,0,0,0,0,0,1,5,7],
        [8,0,9,6,0,5,0,3,0],
        [0,0,0,0,7,0,9,0,0]
    ])
    print(test_sudoku)