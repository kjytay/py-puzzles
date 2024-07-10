import matplotlib.pyplot as plt
from typing import Dict, Iterable, List, Optional, Union, Tuple
from .rect import Rect

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
        An anchor refers to the cell which is given in the puzzle. Its value
        indicates the area of the rectangle that the cell belongs to.
        """
        self.rows = len(board)
        self.cols = len(board[0])
        for row in board:
            assert len(row) == self.cols, '# cols in board ({}) should be {}'.format(len(row), self.cols)
        self.board: Board = [
            [cell for cell in row] for row in board
        ]
        # replace anything other than valid integers with an empty cell
        # populate anchor list at the same time.
        self.anchors = []
        for r in range(self.rows):
            for c in range(self.cols):
                if isinstance(self.board[r][c], int) is False or self.board[r][c] < 1:
                    self.board[r][c] = EMPTY
                else:
                    self.anchors.append((r, c, board[r][c]))
        self.is_solved = False
        self.solution = None
    
    def solve(self):
        """
        Solve the shikaku board. Solution is saved as self.solution, and also returned.
        """
        raise NotImplementedError
    
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
    
    def show(self):
        print(Shikaku.get_board_ascii(self.board))
    
    def show_solution(self):
        if self.solution is not None:
            print('not implemented yet') # TODO
        return

    def show_as_image(self, title: str = 'Shikaku', save_path: str = '') -> None:
        """
        Draw image of the original board.
        """
        self._get_board_image(title=title, save_path=save_path)
    
    def show_solution_as_image(self, title: str = 'Shikaku', save_path: str = '') -> None:
        """
        Draw image of the board with solution overlaid on top.
        """
        self._get_board_image(self.solution, title=title, save_path=save_path)

    def _get_board_image(self, solution: Optional[Dict[int, Rect]] = None, title: str = '',
                         save_path: str = '') -> None:
        """
        Draw an image of the given board.
        If solution is provided, draw the rectangles of the solution too.
        """
        fig, ax = plt.subplots(figsize=(6, 6))

        # draw main grid
        for i in range(self.rows+1):
            ax.plot([0, self.cols], [i, i], color='black', linewidth=0.5)
        for i in range(self.cols+1):
            ax.plot([i, i], [0, self.rows], color='black', linewidth=0.5)

        # add numbers
        for (r, c, val) in self.anchors:
            ax.text(c + 0.5, self.rows - 0.5 - r, str(val),
                    ha='center', va='center', fontsize=12, color='black')
            
        # if solution is provided, draw the rectangles
        if solution is not None:
            for rect in solution.values():
                ax.plot([rect.c1, rect.c1], [self.rows-rect.r1, self.rows-rect.r2-1],
                        color='black', linewidth=3)
                ax.plot([rect.c2+1, rect.c2+1], [self.rows-rect.r1, self.rows-rect.r2-1],
                        color='black', linewidth=3)
                ax.plot([rect.c1, rect.c2+1], [self.rows-rect.r1, self.rows-rect.r1],
                        color='black', linewidth=3)
                ax.plot([rect.c1, rect.c2+1], [self.rows-rect.r2-1, self.rows-rect.r2-1],
                        color='black', linewidth=3)
        
        # set the axis properties
        ax.set_xlim(-1, self.cols+1)
        ax.set_ylim(-1, self.rows+1)
        ax.set_aspect('equal')
        ax.axis('off')

        # add title
        ax.set_title(title, fontsize=20, pad=20)

        if save_path != '':
            plt.savefig(save_path, bbox_inches='tight')
        
        plt.show()


class _ShikakuSolver:
    def __init__(self, shikaku: Shikaku):
        self.rows = shikaku.rows
        self.cols = shikaku.cols
        self.board = shikaku.board
        self.anchors = shikaku.anchors
        self.num_anchors = len(self.anchors)
    
    def backtracking_solve(self) -> Optional[Dict[int, Rect]]:
        raise NotImplementedError
    

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
    test_shikaku2.show_as_image()
    test_shikaku2.show_solution_as_image()