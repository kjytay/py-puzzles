import matplotlib.pyplot as plt
from overrides import override
from typing import Iterable, List, Optional, Union, Set, Tuple
from .sudoku import Board, EMPTY, Sudoku, _SudokuSolver

"""
Sudoku puzzle with partial XV constraints. If an X (V resp.) appears between two cells,
the sum of those two cells is 10 (5 resp.). Not all X's and V's are given.
"""
class PartialXVSudoku(Sudoku):

    def __init__(self, minirows: int = 3, minicols: Optional[int] = None,
                 board: Optional[Iterable[Iterable[Union[int, None]]]] = None,
                 X_positions: Optional[List[Tuple[int]]] = None,
                 V_positions: Optional[List[Tuple[int]]] = None):
        self.minirows = minirows
        self.minicols = minicols if minicols else minirows
        self.size = self.minirows * self.minicols

        assert self.minirows > 0, 'minirows cannot be less than 1'
        assert self.minicols > 0, 'minicols cannot be less than 1'
        assert self.size > 1, 'Board size cannot be 1 x 1'

        self.X_positions = [] if X_positions is None else X_positions
        for X_clue in self.X_positions:
            assert len(X_clue) == 4, 'Each element in X_positions should have length 4 (r1, c1, r2, c2)'
            assert abs(X_clue[0] - X_clue[2]) + abs(X_clue[1] - X_clue[3]) == 1, \
                'The two cells X_positions[i] represent ({},{}) and ({},{}) should be adjacent'.format(
                    X_clue[0], X_clue[1], X_clue[2], X_clue[3])
        
        self.V_positions = [] if V_positions is None else V_positions
        for V_clue in self.V_positions:
            assert len(V_clue) == 4, 'Each element in V_positions should have length 4 (r1, c1, r2, c2)'
            assert abs(V_clue[0] - V_clue[2]) + abs(V_clue[1] - V_clue[3]) == 1, \
                'The two cells V_positions[i] represent ({},{}) and ({},{}) should be adjacent'.format(
                    V_clue[0], V_clue[1], V_clue[2], V_clue[3])

        if board:
            assert len(board) == self.size, '# rows in board ({}) should be {}'.format(len(board), self.size)
            assert len(board[0]) == self.size, '# cols in board ({}) should be {}'.format(len(board[0]), self.size)
            self.board: Board = [
                [cell for cell in row] for row in board]
            # replace anything other than valid integers with an empty cell
            for row in self.board:
                for j in range(len(row)):
                    if not row[j] in range(1, self.size + 1):
                        row[j] = EMPTY
        else:
            # if board was not passed in set board as empty board
            self.board = Sudoku.get_empty_board(self.minirows, self.minicols)
        
        if self.validate() is False:
            self.is_valid_puzzle = False
            print('Given puzzle is invalid! No solution exists.')
        else:
            self.is_valid_puzzle = True

        self.blank_count = len(self._get_empty_cells(self.board))
        self.is_solved = True if self.blank_count == 0 and self.is_valid_puzzle else False
        self.solution = self.board if self.is_solved else None
    
    @override
    def validate(self) -> bool:
        # check basic sudoku
        if super().validate() is False:
            return False

        # check X rules if both cells are filled
        for (r1, c1, r2, c2) in self.X_positions:
            if self.board[r1][c1] is not EMPTY and self.board[r2][c2] is not EMPTY and \
                self.board[r1][c1] + self.board[r2][c2] != 10:
                return False

        # check V rules if both cells are filled
        for (r1, c1, r2, c2) in self.V_positions:
            if self.board[r1][c1] is not EMPTY and self.board[r2][c2] is not EMPTY and \
                self.board[r1][c1] + self.board[r2][c2] != 5:
                return False

        return True
    
    @override
    def show_as_image(self, title: str = 'Partial XV Sudoku', save_path: str = '') -> None:
        self._get_board_image(self.board, title=title, save_path=save_path)
    
    @override
    def show_solution_as_image(self, title: str = 'Partial XV Sudoku', save_path: str = '') -> None:
        self._get_board_image(self.solution, self.board, title=title, save_path=save_path)

    @override
    def _get_board_image(self, board: Board, original_board: Board = None,
                         title: str = 'Partial XV Sudoku', save_path: str = '') -> None:
        """
        Draw an image of the given board. Digits in both board and original_board are in black,
        digits in just board are in red.
        """
        if board is None:
            print('No board provided, returning')
            return
        if original_board is None:
            original_board = board
         
        fig, ax = plt.subplots(figsize=(6, 6))
    
        # draw main grid (horizontal, then vertical)
        for i in range(self.size+1):
            lw = 2 if i % self.minirows == 0 else 0.5
            ax.plot([0, self.size], [i, i], color='black', linewidth=lw)
        for i in range(self.size+1):
            lw = 2 if i % self.minicols == 0 else 0.5
            ax.plot([i, i], [0, self.size], color='black', linewidth=lw)
        
        # add numbers
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] in list(range(1, self.size+1)):
                    fontcolor = 'black' if original_board[i][j] in list(range(1, self.size+1)) else 'red'
                    ax.text(j + 0.5, self.size - 0.5 - i, str(board[i][j]), 
                            ha='center', va='center', fontsize=16, color=fontcolor)
        
        # add Xs and Vs
        for (r1, c1, r2, c2) in self.X_positions:
            ax.text((c1 + c2) / 2 + 0.5, self.size - 0.5 - (r1 + r2) / 2, 'x',
                    ha='center', va='center', fontsize=14, color='black')
        for (r1, c1, r2, c2) in self.V_positions:
            ax.text((c1 + c2) / 2 + 0.5, self.size - 0.5 - (r1 + r2) / 2, 'v',
                    ha='center', va='center', fontsize=14, color='black')
        
        # set the axis properties
        ax.set_xlim(0, self.size)
        ax.set_ylim(0, self.size)
        ax.set_aspect('equal')
        ax.axis('off')

        # add title
        ax.set_title(title, fontsize=20, pad=20)

        if save_path != '':
            plt.savefig(save_path, bbox_inches='tight')
        
        plt.show()

if __name__ == '__main__':

    test_sudoku = PartialXVSudoku(
        board = [
            [0,0,0,0,0,3,5,0,0],
            [0,7,0,0,0,0,0,8,1],
            [0,0,0,0,0,8,9,0,0],
            [4,0,0,0,2,0,3,0,0],
            [7,0,0,0,0,4,0,0,0],
            [1,0,0,0,0,0,6,9,0],
            [6,0,0,0,0,9,0,0,0],
            [0,0,0,0,0,0,0,0,3],
            [0,3,0,0,0,0,2,0,0]
        ],
        X_positions = [(2, 3, 3, 3), (6, 3, 7, 3)],
        V_positions = [(7, 6, 7, 7)]
    )

    VALID_X_POSITIONS_1 = [(2, 3, 3, 3), (6, 3, 7, 3)]
    VALID_V_POSITIONS_1 = [(7, 6, 7, 7)]
    test_sudoku.show_as_image()