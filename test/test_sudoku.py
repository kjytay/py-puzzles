import pytest
from ktaypuzzles.sudoku import Board, EMPTY, Sudoku, _SudokuSolver

# Reused constants
INVALID_BOARD_1 = [
    [0,0,0,0,0,4,0,0,0],
    [0,4,0,0,6,0,0,0,0],
    [6,3,0,7,0,9,0,0,2],
    [1,2,4,0,0,6,0,0,5],
    [0,0,3,9,0,0,0,0,0],
    [0,0,0,0,4,2,0,0,3],
    [7,0,0,0,0,0,1,5,7],
    [8,0,9,6,0,5,0,3,0],
    [0,0,0,0,7,0,9,0,0]
]

VALID_BOARD_1 = [
    [0,0,0,0,0,3,5,0,0],
    [0,7,0,0,0,0,0,8,1],
    [0,0,0,1,0,8,9,0,0],
    [4,0,0,9,2,0,3,0,0],
    [7,0,0,0,0,4,0,0,0],
    [1,0,0,0,0,0,6,9,0],
    [6,0,0,4,0,9,0,0,0],
    [0,0,0,6,0,0,0,0,3],
    [0,3,0,0,0,0,2,0,0]
]

VALID_BOARD_2 = [
    [3,4,0,0,0,0],
    [0,0,6,0,0,0],
    [4,0,0,2,0,0],
    [1,5,0,0,0,0],
    [0,0,0,0,6,5],
    [0,0,0,3,0,0]
]

# Tests begin here
def test_invalid_board():
    # Invalid board
    sudoku = Sudoku(board=INVALID_BOARD_1)
    assert sudoku.is_valid_board is False

def test_get_empty_cells():
    actual_empty_cells = Sudoku._get_empty_cells([
        [3,4,EMPTY,EMPTY,2,6],
        [5,2,6,4,1,3],
        [4,6,3,2,5,1],
        [1,5,2,EMPTY,EMPTY,4],
        [EMPTY,3,4,1,6,5],
        [6,1,5,3,4,2]
    ])
    expected_empty_cells = {(0,2), (0,3), (3,3), (3,4), (4,0)}
    assert actual_empty_cells == expected_empty_cells

def test_ip_solve():
    # Test IP solver with a valid board
    sudoku = Sudoku(board=VALID_BOARD_1)
    sudoku_solver = _SudokuSolver(sudoku)
    actual_solution = sudoku_solver.ip_solve()
    expected_solution: Board = [
        [9, 8, 1, 7, 4, 3, 5, 2, 6],
        [3, 7, 5, 2, 9, 6, 4, 8, 1],
        [2, 4, 6, 1, 5, 8, 9, 3, 7],
        [4, 6, 8, 9, 2, 1, 3, 7, 5],
        [7, 5, 9, 3, 6, 4, 8, 1, 2],
        [1, 2, 3, 8, 7, 5, 6, 9, 4],
        [6, 1, 2, 4, 3, 9, 7, 5, 8],
        [5, 9, 7, 6, 8, 2, 1, 4, 3],
        [8, 3, 4, 5, 1, 7, 2, 6, 9]
    ]
    assert actual_solution == expected_solution

def test_ip_solve2():
    # Test IP solver with a 2x3 minigrid board
    sudoku = Sudoku(minirows=2, minicols=3, board=VALID_BOARD_2)
    sudoku_solver = _SudokuSolver(sudoku)
    actual_solution = sudoku_solver.ip_solve()
    expected_solution: Board = [
        [3,4,1,5,2,6],
        [5,2,6,4,1,3],
        [4,6,3,2,5,1],
        [1,5,2,6,3,4],
        [2,3,4,1,6,5],
        [6,1,5,3,4,2]
    ]
    assert actual_solution == expected_solution

def test_ip_solve_invalid():
    # Test IP solver with an invalid board
    sudoku = Sudoku(board=INVALID_BOARD_1)
    sudoku_solver = _SudokuSolver(sudoku)
    actual_solution = sudoku_solver.ip_solve()
    assert actual_solution is None

def test_backtracking_solve():
    # Test backtracking solver with 2x3 minigrid board
    sudoku = Sudoku(minirows=2, minicols=3, board=VALID_BOARD_2)
    sudoku_solver = _SudokuSolver(sudoku)
    actual_solution = sudoku_solver.backtracking_solve()
    expected_solution = [[
        [3,4,1,5,2,6],
        [5,2,6,4,1,3],
        [4,6,3,2,5,1],
        [1,5,2,6,3,4],
        [2,3,4,1,6,5],
        [6,1,5,3,4,2]
    ]]
    assert actual_solution == expected_solution

def test_backtracking_solve2():
    # Test backtracking solver with 2x2 minigrid board that has multiple solutions
    sudoku = Sudoku(minirows=2, minicols=2, board = [
        [1,2,3,0],
        [3,4,1,0],
        [2,0,0,0],
        [0,0,0,0]
    ])
    sudoku_solver = _SudokuSolver(sudoku)
    actual_solution = sudoku_solver.backtracking_solve()
    expected_solution = [
        [
            [1, 2, 3, 4],
            [3, 4, 1, 2],
            [2, 1, 4, 3],
            [4, 3, 2, 1]
        ], [
            [1, 2, 3, 4],
            [3, 4, 1, 2],
            [2, 3, 4, 1],
            [4, 1, 2, 3]
        ]
    ]
    assert actual_solution == expected_solution

def test_backtracking_solve_invalid():
    # Test IP solver with an invalid board
    sudoku = Sudoku(board=INVALID_BOARD_1)
    sudoku_solver = _SudokuSolver(sudoku)
    actual_solution = sudoku_solver.backtracking_solve()
    assert actual_solution == []


def test_get_candidates_for_cell():
    sudoku = Sudoku(board=VALID_BOARD_1)
    sudoku_solver = _SudokuSolver(sudoku)
    actual_candidates = _SudokuSolver._get_candidates_for_cell(2, 8, board=VALID_BOARD_1)
    expected_candidates = {2, 4, 6, 7}
    assert actual_candidates == expected_candidates

def test_get_neighbors_for_cell():
    actual_neighbors = _SudokuSolver._get_neighbors_for_cell(2, 4, minirows=2, minicols=3)
    expected_neighbors = {
        (2,0), (2,1), (2,2), (2,3), (2,5),
        (0,4), (1,4), (3,4), (4,4), (5,4),
        (3,3), (3,5)
    }
    assert actual_neighbors == expected_neighbors