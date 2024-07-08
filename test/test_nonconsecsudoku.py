from ktaypuzzles.nonconsecsudoku import NonConsecSudoku, _NonConsecSudokuSolver

VALID_BOARD_1 = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,5,0,0,0,0],
    [0,0,1,0,3,0,2,0,0],
    [0,0,0,6,0,3,0,0,0],
    [0,7,4,0,0,0,3,6,0],
    [0,0,0,4,0,1,0,0,0],
    [0,0,3,0,4,0,9,0,0],
    [0,0,0,0,9,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]

VALID_BOARD_2 = [
    [9,5,2,7,1,4,8,3,6],
    [3,8,6,2,5,9,4,7,1],
    [7,4,1,8,3,6,2,5,9],
    [5,2,9,6,8,3,7,1,4],
    [1,7,4,9,2,5,3,6,8],
    [6,3,8,4,7,1,5,9,2],
    [8,6,3,1,4,7,9,2,5],
    [4,1,7,5,9,2,6,8,3],
    [2,9,5,3,6,8,1,4,7]
]

INVALID_BOARD_1 = [
    [6,3,5,7,9,4,1,8,2],
    [4,8,2,1,3,6,5,9,7],
    [7,9,1,2,8,5,6,3,4],
    [9,5,3,4,2,8,7,6,1],
    [1,2,4,3,6,7,9,5,8],
    [8,6,7,9,5,1,2,4,3],
    [5,7,6,8,1,3,4,2,9],
    [2,4,8,6,7,9,3,1,5],
    [3,1,9,5,4,2,8,7,6]
]

def test_valid_board():
    sudoku = NonConsecSudoku(board=VALID_BOARD_1)
    assert sudoku.is_valid_board

def test_valid_board2():
    sudoku = NonConsecSudoku(board=VALID_BOARD_2)
    assert sudoku.is_valid_board

def test_invalid_board():
    sudoku = NonConsecSudoku(board=INVALID_BOARD_1)
    assert sudoku.is_valid_board is False

def test_get_candidates_for_cell():
    sudoku = NonConsecSudoku(board=VALID_BOARD_1)
    actual_candidates = sudoku._get_candidates_for_cell(0, 4, board=VALID_BOARD_1)
    expected_candidates = {1, 2, 7, 8}
    assert actual_candidates == expected_candidates

def test_backtracking_solve():
    sudoku = NonConsecSudoku(board=VALID_BOARD_1)
    sudoku_solver = _NonConsecSudokuSolver(sudoku)
    actual_solution = sudoku_solver.backtracking_solve()
    expected_solution = [VALID_BOARD_2]
    assert actual_solution == expected_solution