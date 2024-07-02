import pytest
from ktaypuzzles.sudoku import Board, Sudoku

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

# Tests begin here
def test_invalid_board():
    # Invalid board
    sudoku = Sudoku(board=INVALID_BOARD_1)
    assert sudoku.is_valid_board is False

def test_ip_solve():
    # Test IP solver with a valid board
    sudoku = Sudoku(board=VALID_BOARD_1)
    actual_solution = sudoku.solve()
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

def test_ip_solve_invalid():
    # Test IP solver with an invalid board
    sudoku = Sudoku(board=INVALID_BOARD_1)
    actual_solution = sudoku.solve()
    assert actual_solution is None