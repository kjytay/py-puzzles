import cvxpy as cp
from typing import Iterable, List, Optional, Union, Set, Tuple

"""
Each Sudoku board is represented by a `Board` object, where board[r][c] is either a number
or None (indicating an empty cell).
"""
# type alias for the board
Board = List[List[Union[int, None]]]
EMPTY = None

class Sudoku:

    def __init__(self, minirows: int = 3, minicols: Optional[int] = None,
                 board: Optional[Iterable[Iterable[Union[int, None]]]] = None):
        """
        Initializes a Sudoku board

        :param minirows: Integer representing the rows of the small Sudoku grid. Defaults to 3.
        :param minicols: Optional integer representing the columns of the small Sudoku grid.
        If not provided, defaults to the value of `minirows`.
        :param board: Optional iterable for a the initial state of the Sudoku board.
        If not provided, defaults to empty board.

        :raises AssertionError: If the minirows, minicols, or size of the board is invalid.
        :raises Exception: If given board is invalid.
        """
        self.minirows = minirows
        self.minicols = minicols if minicols else minirows
        self.size = self.minirows * self.minicols

        assert self.minirows > 0, 'minirows cannot be less than 1'
        assert self.minicols > 0, 'minicols cannot be less than 1'
        assert self.size > 1, 'Board size cannot be 1 x 1'

        if board:
            assert len(board) == self.size, '# rows in board ({}) should be {}'.format(len(board), self.size)
            assert len(board[0]) == self.size, '# cols in board ({}) should be {}'.format(len(board[0]), self.size)
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
                self.is_valid_board = False
                print('Given board is invalid! No solution exists.')
            else:
                self.is_valid_board = True
        else:
            # if board was not passed in, generate empty board
            # TODO: replace with random board generator
            self.board = [[EMPTY] * self.size for _ in range(self.size)]
            self.blank_count = self.size * self.size
            self.is_valid_board = True

        self.is_solved = True if self.blank_count == 0 and self.is_valid_board else False
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
                box = (row // self.minirows) * self.minirows + (col // self.minicols)
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

    def solve(self) -> Optional[Board]:
        """
        Solve the sudoku board. Board is saved as self.solution, and also returned.
        """
        sudoku_solver = _SudokuSolver(self)
        solution_board = sudoku_solver.ip_solve()
        self.is_solved = solution_board is not None
        self.solution = solution_board
        return solution_board
    
    @staticmethod
    def _copy_board(board: Board) -> Board:
        return [[cell for cell in row] for row in board]
    
    @staticmethod
    def _get_empty_cells(board: Board) -> Set[Tuple[int, int]]:
        """
        Empty cells returned as a set of (r,c) indices.
        """
        size = len(board)
        return set([(r,c) for r in range(size) for c in range(size) if board[r][c] is EMPTY])
    
    @staticmethod
    def get_board_ascii(minirows: int = 3, minicols: Optional[int] = None, board: Board = None) -> str:
        minicols = minicols if minicols else minirows
        size = minirows * minicols
        table = ''
        cell_length = len(str(size))
        format_int = '{0:0' + str(cell_length) + 'd}'
        for i, row in enumerate(board):
            if i == 0:
                table += ('+-' + '-' * (cell_length + 1) *
                          minicols) * minirows + '+' + '\n'
            table += (('| ' + '{} ' * minicols) * minirows + '|').format(*[format_int.format(
                x) if x != EMPTY else ' ' * cell_length for x in row]) + '\n'
            if i == size - 1 or i % minirows == minirows - 1:
                table += ('+-' + '-' * (cell_length + 1) *
                          minicols) * minirows + '+' + '\n'
        return table
    
    def __str__(self) -> str:
        """
        Prints the original board.
        """
        return '''
---------------------------
{}x{} ({}x{}) SUDOKU PUZZLE
---------------------------
{}
        '''.format(self.size, self.size, self.minirows, self.minicols,
                   Sudoku.get_board_ascii(self.minirows, self.minicols, self.board))
    
    def show(self):
        print(Sudoku.get_board_ascii(self.minirows, self.minicols, self.board))

    def show_solution(self):
        if self.solution is not None:
            print(Sudoku.get_board_ascii(self.minirows, self.minicols, self.solution))
        return


class _SudokuSolver:
    def __init__(self, sudoku: Sudoku):
        self.minirows = sudoku.minirows
        self.minicols = sudoku.minicols
        self.size = sudoku.size
        self.is_valid_board = sudoku.is_valid_board
        self.original_board = sudoku.board
    
    def ip_solve(self) -> Optional[Board]:
        """
        Solve the sudoku puzzle as an IP.
        Board has numbers in range (1, self.size+1), we solve the IP with numbers in range(self.size).
        Ref: https://www.mathworks.com/help/optim/ug/sudoku-puzzles-problem-based.html
        """
        if not self.is_valid_board:
            return None

        # x[v][r][c]: 1 if value of cell (r,c) is v, 0 otherwise
        x = [cp.Variable((self.size, self.size), integer=True) for _ in range(self.size)]
        constraints = []

        # binary constraints
        constraints.extend([0 <= xv for xv in x])
        constraints.extend([xv <= 1 for xv in x])

        # only one value for each cell
        constraints.extend([cp.sum([xv[r][c] for xv in x]) == 1 \
                            for r in range(self.size) for c in range(self.size)])
        
        # each digit appears exactly once in each row
        constraints.extend([cp.sum([xv[r][c] for c in range(self.size)]) == 1 \
                            for xv in x for r in range(self.size)])
        
        # each digit appears exactly once in each column
        constraints.extend([cp.sum([xv[r][c] for r in range(self.size)]) == 1 \
                            for xv in x for c in range(self.size)])
        
        # each digit appears exactly once in each mini-grid
        for box_row_index in range(self.minicols):
            for box_col_index in range(self.minirows):
                row_offset = box_row_index * self.minirows
                col_offset = box_col_index * self.minicols
                constraints.extend([
                    cp.sum(xv[row_offset:(row_offset+self.minirows), 
                              col_offset:(col_offset+self.minicols)]) == 1 for xv in x
                ])

        # original board constraints
        for r in range(self.size):
            for c in range(self.size):
                if self.original_board[r][c] in range(1, self.size + 1):
                    constraints.append(x[self.original_board[r][c] - 1][r][c] == 1)

        prob = cp.Problem(cp.Minimize(cp.sum(x[0])), constraints)
        prob.solve()

        if prob.value == float('inf'):
            return None
        else:
            # convert x to board
            solution_board: Board = [
                [[xv.value[r][c] for xv in x].index(1) + 1 for c in range(self.size)] \
                for r in range(self.size)
            ]
            return solution_board
    
    def backtracking_solve(self) -> List[Board]:
        """
        Solve the sudoku puzzle with backtracking. Solutions are returned as a list: if the
        board admits multiple solutions, all solutions are returned. If there is no solution,
        empty list is returned.
        """
        empty_cells = Sudoku._get_empty_cells(self.original_board)
        candidates_dict = {}
        for (r,c) in empty_cells:
            candidates_dict[(r,c)] = _SudokuSolver._get_candidates_for_cell(
                r, c, self.minirows, self.minicols, self.original_board)
        
        solution_list = []
        current_board = Sudoku._copy_board(self.original_board)
        self._do_backtracking(current_board, candidates_dict, solution_list)

        return solution_list
    
    def _do_backtracking(self, current_board, candidates_dict, solution_list) -> None:
        if len(candidates_dict) == 0:
            # recursion base case 1: no more empty cells
            solution_list.append(Sudoku._copy_board(current_board))
            return
        elif 0 in [len(v) for v in candidates_dict.values()]:
            # recursion base case 2: at least one remaiing empty cell has no candidates
            return
        else:
            # recursive case
            # pick an empty cell and fill it (choose a cell with fewest candidates)
            # update the candidates dictionary
            candidates_list = sorted(candidates_dict.items(), key=lambda item: len(item[1]))
            current_cell = candidates_list[0][0]
            (current_row, current_col) = current_cell
            current_candidates = candidates_list[0][1]
            for candidate in current_candidates:
                # explore
                original_candidates_dict = {current_cell: current_candidates}
                current_board[current_row][current_col] = candidate
                current_neighbors = _SudokuSolver._get_neighbors_for_cell(
                    current_row, current_col, self.minirows, self.minicols)
                current_neighbors = current_neighbors & set(candidates_dict.keys())
                for (r,c) in current_neighbors:
                    original_candidates_dict[(r,c)] = candidates_dict[(r,c)]
                    candidates_dict[(r,c)] = _SudokuSolver._get_candidates_for_cell(
                        r, c, self.minirows, self.minicols, current_board)
                del candidates_dict[current_cell]
                self._do_backtracking(current_board, candidates_dict, solution_list)

                # undo recursion
                current_board[current_row][current_col] = EMPTY
                for cell in original_candidates_dict:
                    candidates_dict[cell] = original_candidates_dict[cell]

    @staticmethod
    def _get_candidates_for_cell(r: int, c: int, minirows: int = 3, minicols: Optional[int] = None,
                                 board: Board = None) -> Set[int]:
        """
        Return possible values in (r,c) given the current board. It ignores the value (if present)
        at (r,c).
        """
        minicols = minicols if minicols else minirows
        size = minirows * minicols
        candidates = set(range(1, size + 1))
        current_row_values = set([board[r][col] for col in range(size) if col != c]) - {EMPTY}
        candidates = candidates - current_row_values
        current_col_values = set([board[row][c] for row in range(size) if row != r]) - {EMPTY}
        candidates = candidates - current_col_values
        box_corner_row = (r // minirows) * minirows
        box_corner_col = (c // minicols) * minicols
        current_box_values = set([board[box_corner_row+row][box_corner_col+col] \
                                  for row in range(minirows) for col in range(minicols) \
                                    if box_corner_row+row != r or box_corner_col+col != c]) - {EMPTY}
        candidates = candidates - current_box_values
        return candidates
    
    @staticmethod
    def _get_neighbors_for_cell(r: int, c: int, minirows: int = 3, minicols: Optional[int] = None) \
        -> Set[Tuple[int, int]]:
        """
        Return cells which are in the same row, column or box as (r,c).
        """
        minicols = minicols if minicols else minirows
        size = minirows * minicols
        row_neighbors = set([(row, c) for row in range(size) if row != r])
        col_neighbors = set([(r, col) for col in range(size) if col != c])
        box_corner_row = (r // minirows) * minirows
        box_corner_col = (c // minicols) * minicols
        box_neighbors = set([(box_corner_row+row, box_corner_col+col) \
                                  for row in range(minirows) for col in range(minicols) \
                                    if box_corner_row+row != r or box_corner_col+col != c])
        return row_neighbors | col_neighbors | box_neighbors


if __name__ == '__main__':

    test_sudoku = Sudoku(
        board = [
        [0,0,0,0,0,3,5,0,0],
        [0,7,0,0,0,0,0,8,1],
        [0,0,0,1,0,8,9,0,0],
        [4,0,0,9,2,0,3,0,0],
        [7,0,0,0,0,4,0,0,0],
        [1,0,0,0,0,0,6,9,0],
        [6,0,0,4,0,9,0,0,0],
        [0,0,0,6,0,0,0,0,3],
        [0,3,0,0,0,0,2,0,0]
    ])
    test_sudoku.show()

    test_sudoku.solve()
    test_sudoku.show_solution()