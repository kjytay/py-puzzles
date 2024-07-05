import cvxpy as cp
import random
from overrides import override
from typing import Dict, Iterable, List, Optional, Union, Set, Tuple

from .sudoku import Board, EMPTY, Sudoku, _SudokuSolver

"""
Sudoku puzzle with diagonal constraints: numbers must be unique on each main diagonal.
"""
class DiagonalSudoku(Sudoku):

    def __init__(self, minirows: int = 3,
                 board: Optional[Iterable[Iterable[Union[int, None]]]] = None):
        """
        Initializes a diagonal Sudoku board

        :param minirows: Integer representing the rows of the small Sudoku grid. Defaults to 3.
        :param board: Optional iterable for a the initial state of the Sudoku board.
        If not provided, generates an empty board.

        :raises AssertionError: If the minirows or size of the board is invalid.
        """
        self.minirows = minirows
        self.minicols = minirows
        self.size = self.minirows * self.minicols

        assert self.minirows > 0, 'minirows cannot be less than 1'
        assert self.minicols > 0, 'minicols cannot be less than 1'
        assert self.size > 1, 'Board size cannot be 1 x 1'

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
            if self.validate() is False:
                self.is_valid_board = False
                print('Given board is invalid! No solution exists.')
            else:
                self.is_valid_board = True
        else:
            # if board was not passed in set board as empty board
            self.board = Sudoku.get_empty_board(self.minirows, self.minicols)
            self.is_valid_board = True

        self.blank_count = len(self._get_empty_cells(self.board))
        self.is_solved = True if self.blank_count == 0 and self.is_valid_board else False
        self.solution = self.board if self.is_solved else None

    @override
    def validate(self) -> bool:
        # check basic sudoku
        if super().validate() is False:
            return False

        # check diagonals
        diagonal_numbers = [[False for _ in range(self.size)] for _ in range(2)]
        for i in range(self.size):
            cell = self.board[i][i]
            if cell == EMPTY:
                continue
            elif isinstance(cell, int):
                if diagonal_numbers[0][cell - 1]:
                    return False
                diagonal_numbers[0][cell - 1] = True
        for i in range(self.size):
            cell = self.board[i][self.size-1-i]
            if cell == EMPTY:
                continue
            elif isinstance(cell, int):
                if diagonal_numbers[1][cell - 1]:
                    return False
                diagonal_numbers[1][cell - 1] = True

        return True

    @override
    def solve(self) -> Optional[Board]:
        """
        Solve the sudoku board. Board is saved as self.solution, and also returned.
        """
        sudoku_solver = _DiagonalSudokuSolver(self)
        solution_board = sudoku_solver.backtracking_solve()
        self.is_solved = len(solution_board) > 0
        self.solution = solution_board[0] if self.is_solved else None
        return solution_board
    
    @override
    def generate_puzzle_board(self, blank_proportion: float = 0.5) -> Board:
        """
        Generate a new random sudoku puzzle and save in self.board. We do so in the following way:
        1. Generate a complete board with _generate_complete_board().
        2. Randomly remove `blank_proportion` of the cells.
        3. Use backtracking_solve() to check if the solution is unique. If not, keeping adding
           cells back until the solution is unique.
        """
        assert blank_proportion > 0 and blank_proportion < 1, 'blank_proportion must be in (0,1)'
        complete_board = self._generate_complete_board()

        num_cells_to_remove = round(self.size * self.size * blank_proportion)
        puzzle_board = Sudoku._copy_board(complete_board)
        cells_to_remove = random.sample([(r,c) for r in range(self.size) for c in range(self.size)],
                                        num_cells_to_remove)
        for (r,c) in cells_to_remove:
            puzzle_board[r][c] = EMPTY

        # get solutions for this board, then keeping adding cells until solution is unique
        sudoku_solver = _DiagonalSudokuSolver(DiagonalSudoku(self.minirows, puzzle_board))
        solution_list = sudoku_solver.backtracking_solve()
        while len(solution_list) > 1:
            r,c = cells_to_remove.pop()
            puzzle_board[r][c] = complete_board[r][c]
            solution_list = [board for board in solution_list if board[r][c] == complete_board[r][c]]

        self.board = puzzle_board
        self.is_valid_board = True
        self.blank_count = len(self._get_empty_cells(self.board))
        self.is_solved = True if self.blank_count == 0 and self.is_valid_board else False
        self.solution = self.board if self.is_solved else None
     
    @override
    def _get_neighbors_for_cell(self, r: int, c: int) -> Set[Tuple[int, int]]:
        """
        Return cells which are in the same row, column or box as (r,c). If (r,c) is on a main
        diagonal, other cells on that main diagonal are included too.
        """
        basic_neighbors = super()._get_neighbors_for_cell(r, c)
        l2r_neighbors = set([(i,i) for i in range(self.size) if i != r]) if r == c else set()
        r2l_neighbors = set([(i,self.size-1-i) for i in range(self.size) if i != r]) \
            if r+c == self.size-1 else set()
        return basic_neighbors | l2r_neighbors | r2l_neighbors

    @override
    def __str__(self) -> str:
        """
        Prints the original board.
        """
        return '''
------------------------------------
{}x{} ({}x{}) DIAGONAL SUDOKU PUZZLE
------------------------------------
{}
        '''.format(self.size, self.size, self.minirows, self.minicols,
                   Sudoku.get_board_ascii(self.minirows, self.minicols, self.board))
    

class _DiagonalSudokuSolver(_SudokuSolver):
    def __init__(self, sudoku: DiagonalSudoku):
        super().__init__(sudoku)
    
    @override
    def ip_solve(self) -> Optional[Board]:
        raise NotImplementedError


if __name__ == '__main__':

    test_sudoku = DiagonalSudoku(
        board = [
            [9,0,0,0,0,0,0,0,0],
            [0,5,8,0,0,9,4,0,0],
            [7,0,0,0,5,0,0,0,0],
            [8,0,3,0,2,0,5,0,0],
            [1,0,0,0,0,5,8,0,3],
            [0,0,0,8,7,0,1,2,0],
            [0,8,9,2,1,0,7,0,0],
            [6,0,5,0,4,0,9,8,0],
            [0,1,7,5,0,0,0,0,0]
        ])
    test_sudoku.show()
    
    test_sudoku.solve()
    test_sudoku.show_solution()