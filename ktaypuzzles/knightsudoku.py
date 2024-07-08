import random
from overrides import override
from typing import Iterable, Optional, Union, Set, Tuple

from .sudoku import Board, EMPTY, Sudoku, _SudokuSolver

"""
Sudoku puzzle with knight constraint. The same number cannot appear twice within a knight's move.
"""
class KnightSudoku(Sudoku):

    def __init__(self, minirows: int = 3, minicols: Optional[int] = None,
                 board: Optional[Iterable[Iterable[Union[int, None]]]] = None):
        super().__init__(minirows, minicols, board)

    @override
    def validate(self) -> bool:
        # check basic sudoku
        if super().validate() is False:
            return False

        # check knight moves
        for r in range(self.size):
            for c in range(self.size):
                cell = self.board[r][c]
                if cell == EMPTY:
                    continue
                elif isinstance(cell, int):
                    cell_knight_neighbors = self._get_knight_neighbors(r, c)
                    for (i, j) in cell_knight_neighbors:
                        if cell == self.board[i][j]:
                            return False

        return True

    @override
    def solve(self) -> Optional[Board]:
        """
        Solve the sudoku board. Board is saved as self.solution, and also returned.
        """
        sudoku_solver = _KnightSudokuSolver(self)
        solution_board = sudoku_solver.backtracking_solve()
        self.is_solved = len(solution_board) > 0
        self.solution = solution_board[0] if self.is_solved else None
        return solution_board
    
    @override
    def generate_puzzle_board(self, blank_proportion: float = 0.65) -> Board:
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
        sudoku_solver = _KnightSudokuSolver(KnightSudoku(self.minirows, self.minicols, puzzle_board))
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
     
    def _get_knight_neighbors(self, r: int, c: int) -> Set[Tuple[int, int]]:
        """
        Return cells which are a king's move away from (r,c). (r,c) itself is excluded.
        """
        knight_neighbors = [(r-2,c-1), (r-2,c+1),
                            (r+2,c-1), (r+2,c+1),
                            (r-1,c-2), (r+1,c-2),
                            (r-1,c+2), (r+1,c+2)]
        knight_neighbors = [x for x in knight_neighbors if x[0] >= 0 and x[0] < self.size and \
                          x[1] >= 0 and x[1] < self.size]
        return set(knight_neighbors)
    
    @override
    def _get_neighbors_for_cell(self, r: int, c: int) -> Set[Tuple[int, int]]:
        """
        Return cells which are in the same row, column or box as (r,c), or which are a knight's
        move away from (r,c).
        """
        basic_neighbors = super()._get_neighbors_for_cell(r, c)
        return basic_neighbors | self._get_knight_neighbors(r, c)
    
    @override
    def __str__(self) -> str:
        """
        Prints the original board.
        """
        return '''
----------------------------------
{}x{} ({}x{}) KNIGHT SUDOKU PUZZLE
----------------------------------
{}
        '''.format(self.size, self.size, self.minirows, self.minicols,
                   Sudoku.get_board_ascii(self.minirows, self.minicols, self.board))
    
    @override
    def show_as_image(self, title: str = 'Knight Sudoku', save_path: str = '') -> None:
        self._get_board_image(self.board, title=title, save_path=save_path)
    
    @override
    def show_solution_as_image(self, title: str = 'Knight Sudoku', save_path: str = '') -> None:
        self._get_board_image(self.solution, self.board, title=title, save_path=save_path)
    

class _KnightSudokuSolver(_SudokuSolver):
    def __init__(self, sudoku: KnightSudoku):
        super().__init__(sudoku)
    
    @override
    def ip_solve(self) -> Optional[Board]:
        raise NotImplementedError


if __name__ == '__main__':

    # board taken from Cracking the Cryptic app
    test_sudoku = KnightSudoku(
        board = [
            [0,0,0,0,0,0,0,0,0],
            [0,8,0,0,3,0,0,9,0],
            [0,0,1,2,0,5,6,0,0],
            [0,0,3,4,0,8,7,0,0],
            [0,2,0,0,6,0,0,5,0],
            [0,0,7,9,0,1,2,0,0],
            [0,0,6,8,0,3,4,0,0],
            [0,4,0,0,7,0,0,1,0],
            [0,0,0,0,0,0,0,0,0]
        ])
    test_sudoku.show()
    
    test_sudoku.solve()
    test_sudoku.show_solution()