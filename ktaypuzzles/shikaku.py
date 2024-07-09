from typing import Iterable, List, Union

"""
Each Shikaku board is represented a `Board` object, where board[r][c] is either
a number or None (indicating an empty cell).
"""
# type alias for the board
Board = List[List[Union[int, None]]]
EMPTY = None

class Shikaku:

    def __init__(self, board: Iterable[Iterable[Union[int, None]]]):
        """
        Initializes a Shikaku board.
        """
        self.rows = len(board)
        self.cols = len(board[0])
        for row in board:
            assert len(row) == self.cols, '# cols in board ({}) should be {}'.format(len(row), self.cols)
        self.board: Board = [
            [cell for cell in row] for row in board
        ]
        # replace anything other than valid integers with an empty cell
        for row in self.board:
            for j in range(len(row)):
                if isinstance(row[j], int) is False or row[j] < 1:
                    row[j] = EMPTY
        self.is_solved = False
        self.solution = None
    
    @staticmethod
    def get_board_ascii(board: Board) -> str:
        rows = len(board)
        cols = len(board[0])
        maxval = max([max([x for x in row if x is not None]) for row in board])
        table = ''
        cell_length = len(str(maxval))
        format_int = '{0:0' + str(cell_length) + 'd}'
        for i, row in enumerate(board):
            if i == 0:
                table += ('+-' + '-' * (cell_length + 1) *
                          cols) + '+' + '\n'
            table += (('| ' + '{} ' * cols) + '|').format(*[format_int.format(
                x) if x != EMPTY else ' ' * cell_length for x in row]) + '\n'
            if i == len(board) - 1:
                table += ('+-' + '-' * (cell_length + 1) *
                          cols) + '+' + '\n'
        return table
    
    def __str__(self) -> str:
        """
        Prints the original board.
        """
        return '''
--------------------
{}x{} SHIKAKU PUZZLE
--------------------
{}
        '''.format(self.rows, self.cols,
                   Shikaku.get_board_ascii(self.board))


if __name__ == '__main__':

    test_shikaku = Shikaku([
        [0, 4, 0, 0, 0, 2, 0, 0, 0, 3],
        [3, 0, 0, 0, 5, 0, 0, 0, 3, 0],
        [0, 0, 0, 3, 0, 0, 0, 6, 0, 0],
        [0, 0, 3, 0, 0, 0, 5, 0, 0, 0],
        [0, 3, 0, 0, 0, 4, 0, 0, 0, 5],
        [2, 0, 0, 0, 7, 0, 0, 0, 3, 0],
        [0, 0, 0, 5, 0, 0, 0, 4, 0, 0],
        [0, 0, 5, 0, 0, 0, 4, 0, 0, 0],
        [0, 6, 0, 0, 0, 2, 0, 0, 0, 3],
        [2, 0, 0, 0, 5, 0, 0, 0, 3, 0],
    ])
    print(test_shikaku)

    test_shikaku2 = Shikaku([
        [2, 0, 0, 2, 0, 0, 3, 0, 0, 2, 0, 0, 4, 0],
        [0, 0, 3, 0, 0, 2, 0, 0, 2, 0, 0, 3, 0, 0],
        [0, 2, 0, 0, 4, 0, 0, 5, 0, 0, 2, 0, 0, 3],
        [3, 0, 0, 5, 0, 0, 2, 0, 0, 3, 0, 0, 4, 0],
        [0, 0, 5, 0, 0, 2, 0, 0, 2, 0, 0, 5, 0, 0],
        [0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 5, 0, 0, 4],
        [3, 0, 0, 2, 0, 0, 3, 0, 0, 2, 0, 0, 3, 0],
        [0, 0, 2, 0, 0, 3, 0, 0, 5, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 3, 0, 0, 4, 0, 0, 3, 0, 0, 3],
        [3, 0, 0, 5, 0, 0, 5, 0, 0, 2, 0, 0, 3, 0],
        [0, 0, 2, 0, 0, 3, 0, 0, 2, 0, 0, 2, 0, 0],
        [0, 4, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 3]
    ])
    print(test_shikaku2)