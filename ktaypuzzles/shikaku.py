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