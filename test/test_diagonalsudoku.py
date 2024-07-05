import pytest

from ktaypuzzles.diagonalsudoku import DiagonalSudoku, _DiagonalSudokuSolver

def test_valid_board():
    sudoku = DiagonalSudoku(2, board=[
        [1,4,2,3],
        [3,2,4,1],
        [4,1,3,2],
        [2,3,1,4]
    ])
    assert sudoku.is_valid_board

def test_invalid_board():
    # Invalid board
    sudoku = DiagonalSudoku(board=[
        [9, 8, 1, 7, 4, 3, 5, 2, 6],
        [3, 7, 5, 2, 9, 6, 4, 8, 1],
        [2, 4, 6, 1, 5, 8, 9, 3, 7],
        [4, 6, 8, 9, 2, 1, 3, 7, 5],
        [7, 5, 9, 3, 6, 4, 8, 1, 2],
        [1, 2, 3, 8, 7, 5, 6, 9, 4],
        [6, 1, 2, 4, 3, 9, 7, 5, 8],
        [5, 9, 7, 6, 8, 2, 1, 4, 3],
        [8, 3, 4, 5, 1, 7, 2, 6, 9]
    ])
    assert sudoku.is_valid_board is False

def test_get_neighbors_for_cell_l2r():
    actual_neighbors = DiagonalSudoku()._get_neighbors_for_cell(2, 2)
    expected_neighbors = {
        (2,0), (2,1), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8),
        (0,2), (1,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2),
        (0,0), (0,1), (1,0), (1,1),
        (3,3), (4,4), (5,5), (6,6), (7,7), (8,8)
    }
    assert actual_neighbors == expected_neighbors

def test_get_neighbors_for_cell_both():
    actual_neighbors = DiagonalSudoku()._get_neighbors_for_cell(4, 4)
    expected_neighbors = {
        (4,0), (4,1), (4,2), (4,3), (4,5), (4,6), (4,7), (4,8),
        (0,4), (1,4), (2,4), (3,4), (5,4), (6,4), (7,4), (8,4),
        (3,3), (3,5), (5,3), (5,5),
        (0,0), (1,1), (2,2), (6,6), (7,7), (8,8),
        (0,8), (1,7), (2,6), (6,2), (7,1), (8,0)
    }
    assert actual_neighbors == expected_neighbors

def test_get_neighbors_for_cell_neither():
    actual_neighbors = DiagonalSudoku(2)._get_neighbors_for_cell(0, 2)
    expected_neighbors = {
        (0,0), (0,1), (0,3),
        (1,2), (2,2), (3,2),
        (1,3)
    }
    assert actual_neighbors == expected_neighbors

def test_backtracking_solve():
    sudoku = DiagonalSudoku(board=[
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
    sudoku_solver = _DiagonalSudokuSolver(sudoku)
    actual_solution = sudoku_solver.backtracking_solve()
    expected_solution = [[
        [9,3,6,7,8,4,2,1,5],
        [2,5,8,1,3,9,4,7,6],
        [7,4,1,6,5,2,3,9,8],
        [8,9,3,4,2,1,5,6,7],
        [1,7,2,9,6,5,8,4,3],
        [5,6,4,8,7,3,1,2,9],
        [3,8,9,2,1,6,7,5,4],
        [6,2,5,3,4,7,9,8,1],
        [4,1,7,5,9,8,6,3,2]
    ]]
    assert actual_solution == expected_solution