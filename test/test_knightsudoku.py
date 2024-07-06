from ktaypuzzles.knightsudoku import KnightSudoku, _KnightSudokuSolver

def test_valid_board():
    sudoku = KnightSudoku(3, board=[
        [6,3,5,7,9,4,1,8,2],
        [4,8,2,1,3,6,5,9,7],
        [7,9,1,2,8,5,6,3,4],
        [9,5,3,4,2,8,7,6,1],
        [1,2,4,3,6,7,9,5,8],
        [8,6,7,9,5,1,2,4,3],
        [5,7,6,8,1,3,4,2,9],
        [2,4,8,6,7,9,3,1,5],
        [3,1,9,5,4,2,8,7,6]
    ])
    assert sudoku.is_valid_board

def test_invalid_board():
    sudoku = KnightSudoku(2, board=[
        [1,4,2,3],
        [3,2,4,1],
        [4,1,3,2],
        [2,3,1,4]
    ])
    assert sudoku.is_valid_board is False

def test_get_knight_neighbors():
    actual_neighbors = KnightSudoku()._get_knight_neighbors(2, 0)
    expected_neighbors = { (0,1), (1,2), (3,2), (4,1) }
    assert actual_neighbors == expected_neighbors

def test_get_knight_neighbors2():
    actual_neighbors = KnightSudoku()._get_knight_neighbors(8, 8)
    expected_neighbors = { (6,7), (7,6) }
    assert actual_neighbors == expected_neighbors

def test_get_knight_neighbors3():
    actual_neighbors = KnightSudoku()._get_knight_neighbors(3, 6)
    expected_neighbors = { (1,5), (1,7), (5,5), (5,7), (2,4), (4,4), (2,8), (4,8) }
    assert actual_neighbors == expected_neighbors

def test_get_neighbors_for_cell():
    actual_neighbors = KnightSudoku()._get_neighbors_for_cell(2, 0)
    expected_neighbors = {
        (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8),
        (0,0), (1,0), (3,0), (4,0), (5,0), (6,0), (7,0), (8,0),
        (0,1), (0,2), (1,1), (1,2),
        (3,2), (4,1)
    }
    assert actual_neighbors == expected_neighbors

def test_backtracking_solve():
    sudoku = KnightSudoku(board=[
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
    sudoku_solver = _KnightSudokuSolver(sudoku)
    actual_solution = sudoku_solver.backtracking_solve()
    expected_solution = [[
        [6,3,5,7,9,4,1,8,2],
        [4,8,2,1,3,6,5,9,7],
        [7,9,1,2,8,5,6,3,4],
        [9,5,3,4,2,8,7,6,1],
        [1,2,4,3,6,7,9,5,8],
        [8,6,7,9,5,1,2,4,3],
        [5,7,6,8,1,3,4,2,9],
        [2,4,8,6,7,9,3,1,5],
        [3,1,9,5,4,2,8,7,6]
    ]]
    assert actual_solution == expected_solution