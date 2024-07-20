import cvxpy as cp
import matplotlib.pyplot as plt
import random
from typing import Dict, Iterable, List, Optional, Union, Set, Tuple

"""
Each Sudoku board is represented by a `Board` object, where board[r][c] is either a number
or None (indicating an empty cell).
"""
# type alias for the board
Board = List[List[Union[int, None]]]
EMPTY = None

"""
Basic sudoku puzzle.
"""
class Sudoku:

    def __init__(self, minirows: int = 3, minicols: Optional[int] = None,
                 board: Optional[Iterable[Iterable[Union[int, None]]]] = None):
        """
        Initializes a Sudoku board

        :param minirows: Integer representing the rows of the small Sudoku grid. Defaults to 3.
        :param minicols: Optional integer representing the columns of the small Sudoku grid.
        If not provided, defaults to the value of `minirows`.
        :param board: Optional iterable for a the initial state of the Sudoku board.
        If not provided, generates an empty board.

        :raises AssertionError: If the minirows, minicols, or size of the board is invalid.
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
            self.board: Board = [
                [cell for cell in row] for row in board]
            # replace anything other than valid integers with an empty cell
            for row in self.board:
                for j in range(len(row)):
                    if not row[j] in range(1, self.size + 1):
                        row[j] = EMPTY
            if self.validate() is False:
                self.is_valid_puzzle = False
                print('Given puzzle is invalid! No solution exists.')
            else:
                self.is_valid_puzzle = True
        else:
            # if board was not passed in set board as empty board
            self.board = Sudoku.get_empty_board(self.minirows, self.minicols)
            self.is_valid_puzzle = True

        self.blank_count = len(self._get_empty_cells(self.board))
        self.is_solved = True if self.blank_count == 0 and self.is_valid_puzzle else False
        self.solution = self.board if self.is_solved else None

    def validate(self) -> bool:
        """
        Check if the board is valid, i.e. no number is repeated in a row/column/box.
        (Note that this does not automatically mean that a solution exists.)
        """
        row_numbers = [[False for _ in range(self.size)] for _ in range(self.size)]
        col_numbers = [[False for _ in range(self.size)] for _ in range(self.size)]
        box_numbers = [[False for _ in range(self.size)] for _ in range(self.size)]

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
        solution_board = sudoku_solver.backtracking_solve()
        self.is_solved = len(solution_board) > 0
        self.solution = solution_board[0] if self.is_solved else None
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
    def get_empty_board(minirows: int = 3, minicols: Optional[int] = None) -> Board:
        minicols = minicols if minicols else minirows
        size = minirows * minicols
        return [[EMPTY] * size for _ in range(size)]
    
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
        sudoku_solver = _SudokuSolver(Sudoku(self.minirows, self.minicols, puzzle_board))
        solution_list = sudoku_solver.backtracking_solve()
        while len(solution_list) > 1:
            r,c = cells_to_remove.pop()
            puzzle_board[r][c] = complete_board[r][c]
            solution_list = [board for board in solution_list if board[r][c] == complete_board[r][c]]

        self.board = puzzle_board
        self.is_valid_puzzle = True
        self.blank_count = len(self._get_empty_cells(self.board))
        self.is_solved = True if self.blank_count == 0 and self.is_valid_puzzle else False
        self.solution = self.board if self.is_solved else None
    
    def _generate_complete_board(self) -> Board:
        """
        Generate a random complete sudoku board.
        We do so by randomly generating the first row, then filling everything else in
        one-by-one, with backtracking to ensure validity.
        """
        board = [[EMPTY] * self.size for _ in range(self.size)]
        board[0] = list(range(1, self.size+1))
        random.shuffle(board[0])

        empty_cells = Sudoku._get_empty_cells(board)
        candidates_dict = {}
        for (r,c) in empty_cells:
            candidates_dict[(r,c)] = self._get_candidates_for_cell(r, c, board)
            
        solution_list = []
        self._complete_board_recursion(board, candidates_dict, solution_list)

        return solution_list[0]

    def _complete_board_recursion(self, board: Board, candidates_dict: Dict[Tuple[int, int], Set[int]],
                                  solution_list: List[Board]) -> Board:
        if len(candidates_dict) == 0:
            # recursion base case 1: no more empty cells
            solution_list.append(Sudoku._copy_board(board))
            return True
        elif 0 in [len(v) for v in candidates_dict.values()]:
            # recursion base case 2: at least one remaiing empty cell has no candidates
            return False
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
                board[current_row][current_col] = candidate
                current_neighbors = self._get_neighbors_for_cell(current_row, current_col)
                current_neighbors = current_neighbors & set(candidates_dict.keys())
                for (r,c) in current_neighbors:
                    original_candidates_dict[(r,c)] = candidates_dict[(r,c)]
                    candidates_dict[(r,c)] = self._get_candidates_for_cell(r, c, board)
                del candidates_dict[current_cell]
                if self._complete_board_recursion(board, candidates_dict, solution_list):
                    return True

                # undo recursion
                board[current_row][current_col] = EMPTY
                for cell in original_candidates_dict:
                    candidates_dict[cell] = original_candidates_dict[cell]
            return False
    
    def _get_candidates_for_cell(self, r: int, c: int, board: Board) -> Set[int]:
        """
        Return possible values in (r,c) given the current board. It ignores the value (if present)
        at (r,c).
        """
        candidates = set(range(1, self.size + 1))

        neighbors = self._get_neighbors_for_cell(r, c)
        neighbor_values = set([board[i][j] for (i,j) in neighbors]) - {EMPTY}

        return candidates - neighbor_values
    
    def _get_neighbors_for_cell(self, r: int, c: int) -> Set[Tuple[int, int]]:
        """
        Return cells which are in the same row, column or box as (r,c). Does not include (r,c).
        """
        row_neighbors = set([(row, c) for row in range(self.size) if row != r])
        col_neighbors = set([(r, col) for col in range(self.size) if col != c])
        box_corner_row = (r // self.minirows) * self.minirows
        box_corner_col = (c // self.minicols) * self.minicols
        box_neighbors = set([(box_corner_row+row, box_corner_col+col) \
                                  for row in range(self.minirows) for col in range(self.minicols) \
                                    if box_corner_row+row != r or box_corner_col+col != c])
        return row_neighbors | col_neighbors | box_neighbors

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
    
    def show_as_image(self, title: str = 'Sudoku', save_path: str = '') -> None:
        """
        Draw image of the original board.
        """
        self._get_board_image(self.board, title=title, save_path=save_path)
    
    def show_solution_as_image(self, title: str = 'Sudoku', save_path: str = '') -> None:
        """
        Draw image of the solution board.
        """
        self._get_board_image(self.solution, self.board, title=title, save_path=save_path)

    def _get_board_image(self, board: Board, original_board: Board = None,
                         title: str = 'Sudoku', save_path: str = '') -> None:
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


class _SudokuSolver:
    def __init__(self, sudoku: Sudoku):
        self.minirows = sudoku.minirows
        self.minicols = sudoku.minicols
        self.size = sudoku.size
        self.sudoku = sudoku
        self.is_valid_puzzle = sudoku.is_valid_puzzle
        self.original_board = sudoku.board
    
    def ip_solve(self) -> Optional[Board]:
        """
        Solve the sudoku puzzle as an IP.
        Board has numbers in range (1, self.size+1), we solve the IP with numbers in range(self.size).
        Ref: https://www.mathworks.com/help/optim/ug/sudoku-puzzles-problem-based.html
        """
        if not self.is_valid_puzzle:
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
            candidates_dict[(r,c)] = self.sudoku._get_candidates_for_cell(
                r, c, self.original_board)
        
        solution_list = []
        current_board = Sudoku._copy_board(self.original_board)
        self._do_backtracking(current_board, candidates_dict, solution_list)

        return solution_list
    
    def _do_backtracking(self, current_board: Board, candidates_dict: Dict[Tuple[int, int], Set[int]],
                         solution_list: List[Board]) -> None:
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
                current_neighbors = self.sudoku._get_neighbors_for_cell(current_row, current_col)
                current_neighbors = current_neighbors & set(candidates_dict.keys())
                for (r,c) in current_neighbors:
                    original_candidates_dict[(r,c)] = candidates_dict[(r,c)]
                    candidates_dict[(r,c)] = self.sudoku._get_candidates_for_cell(r, c, current_board)
                del candidates_dict[current_cell]
                self._do_backtracking(current_board, candidates_dict, solution_list)

                # undo recursion
                current_board[current_row][current_col] = EMPTY
                for cell in original_candidates_dict:
                    candidates_dict[cell] = original_candidates_dict[cell]


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
    test_sudoku.show_as_image()

    test_sudoku.solve()
    test_sudoku.show_solution()
    test_sudoku.show_solution_as_image()