import random
from overrides import override
from typing import Iterable, Optional, Union, Set, Tuple

from .sudoku import Board, Dict, EMPTY, List, Sudoku, _SudokuSolver

"""
Sudoku puzzle with non-consecutive constraint. Any two orthogonally adjacent cells cannot
contain consecutive numbers.
"""
class NonConsecSudoku(Sudoku):

    def __init__(self, minirows: int = 3, minicols: Optional[int] = None,
                 board: Optional[Iterable[Iterable[Union[int, None]]]] = None):
        super().__init__(minirows, minicols, board)
    
    @override
    def validate(self) -> bool:
        # check basic sudoku
        if super().validate() is False:
            return False

        # check non-consecutive constraint
        for r in range(self.size):
            for c in range(self.size):
                cell = self.board[r][c]
                if cell == EMPTY:
                    continue
                elif isinstance(cell, int):
                    cell_orthogonal_neighbors = self._get_orthogonal_neighbors(r, c)
                    for (i, j) in cell_orthogonal_neighbors:
                        if self.board[i][j] == EMPTY:
                            continue
                        elif abs(cell - self.board[i][j]) <= 1:
                            return False

        return True

    @override
    def solve(self) -> Optional[Board]:
        """
        Solve the sudoku board. Board is saved as self.solution, and also returned.
        """
        sudoku_solver = _NonConsecSudokuSolver(self)
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
        sudoku_solver = _NonConsecSudokuSolver(NonConsecSudoku(self.minirows, self.minicols, puzzle_board))
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
    def _generate_complete_board(self) -> Board:
        """
        Generate a random complete sudoku board.
        We do so by randomly filling every cell one-by-one, with backtracking to ensure validity.
        NOTE: Right now this is pretty slow as backtracking takes a long time to find a valid
        non-consecutive board. TODO Find a better strategy for generating such a board.
        """
        board = [[EMPTY] * self.size for _ in range(self.size)]

        empty_cells = Sudoku._get_empty_cells(board)
        candidates_dict = {}
        for (r,c) in empty_cells:
            candidates_dict[(r,c)] = self._get_candidates_for_cell(r, c, board)
            
        solution_list = []
        self._complete_board_recursion(board, candidates_dict, solution_list)

        return solution_list[0]

    def _get_orthogonal_neighbors(self, r: int, c: int) -> Set[Tuple[int, int]]:
        """
        Return cells which are orthogonal to (r,c). (r,c) itself is excluded.
        """
        orthogonal_neighbors = [(r,c-1), (r,c+1), (r-1,c), (r+1,c)]
        orthogonal_neighbors = [x for x in orthogonal_neighbors if x[0] >= 0 and x[0] < self.size and \
                          x[1] >= 0 and x[1] < self.size]
        return set(orthogonal_neighbors)

    @override
    def _get_candidates_for_cell(self, r: int, c: int, board: Board) -> Set[int]:
        """
        Return possible values in (r,c) given the current board. It ignores the value (if present)
        at (r,c).
        """
        # get candidates based on basic sudoku
        candidates = super()._get_candidates_for_cell(r, c, board)
        orthogonal_values = [board[i][j] for (i,j) in self._get_orthogonal_neighbors(r,c) \
                                 if board[i][j] in list(range(1, self.size+1))]

        return candidates - set(orthogonal_values) - set([x-1 for x in orthogonal_values]) \
            - set([x+1 for x in orthogonal_values])

    @override
    def __str__(self) -> str:
        """
        Prints the original board.
        """
        return '''
-------------------------------------------
{}x{} ({}x{}) NON-CONSECUTIVE SUDOKU PUZZLE
-------------------------------------------
{}
        '''.format(self.size, self.size, self.minirows, self.minicols,
                   Sudoku.get_board_ascii(self.minirows, self.minicols, self.board))
    

class _NonConsecSudokuSolver(_SudokuSolver):
    def __init__(self, sudoku: NonConsecSudoku):
        super().__init__(sudoku)
    
    @override
    def ip_solve(self) -> Optional[Board]:
        raise NotImplementedError


if __name__ == '__main__':

    # board taken from Cracking the Cryptic app
    test_sudoku = NonConsecSudoku(
        board = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,5,0,0,0,0],
            [0,0,1,0,3,0,2,0,0],
            [0,0,0,6,0,3,0,0,0],
            [0,7,4,0,0,0,3,6,0],
            [0,0,0,4,0,1,0,0,0],
            [0,0,3,0,4,0,9,0,0],
            [0,0,0,0,9,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
        ])
    test_sudoku.show()
    
    test_sudoku.solve()
    test_sudoku.show_solution()

    test_sudoku.generate_puzzle_board(0.1)
    test_sudoku.show()