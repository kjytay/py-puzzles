from ktaypuzzles.kingsudoku import KingSudoku, _KingSudokuSolver

def test_valid_board():
    sudoku = KingSudoku(3, board=[
        [7,4,3,5,8,2,6,9,1],
        [9,5,6,4,7,1,8,3,2],
        [2,1,8,3,6,9,7,4,5],
        [4,6,5,7,1,8,3,2,9],
        [3,2,9,6,4,5,1,7,8],
        [1,8,7,2,9,3,4,5,6],
        [6,9,4,1,5,7,2,8,3],
        [8,7,2,9,3,6,5,1,4],
        [5,3,1,8,2,4,9,6,7]
    ])
    assert sudoku.is_valid_puzzle

def test_invalid_board():
    sudoku = KingSudoku(2, board=[
        [1,4,2,3],
        [3,2,4,1],
        [4,1,3,2],
        [2,3,1,4]
    ])
    assert sudoku.is_valid_puzzle is False

def test_get_king_neighbors():
    actual_neighbors = KingSudoku()._get_king_neighbors(2, 0)
    expected_neighbors = { (1,0), (1,1), (2,1), (3,0), (3,1) }
    assert actual_neighbors == expected_neighbors

def test_get_king_neighbors2():
    actual_neighbors = KingSudoku()._get_king_neighbors(8, 8)
    expected_neighbors = { (7,7), (7,8), (8,7) }
    assert actual_neighbors == expected_neighbors

def test_get_king_neighbors3():
    actual_neighbors = KingSudoku()._get_king_neighbors(3, 6)
    expected_neighbors = { (2,5), (2,6), (2,7), (3,5), (3,7), (4,5), (4,6), (4,7) }
    assert actual_neighbors == expected_neighbors

def test_get_neighbors_for_cell():
    actual_neighbors = KingSudoku()._get_neighbors_for_cell(2, 0)
    expected_neighbors = {
        (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8),
        (0,0), (1,0), (3,0), (4,0), (5,0), (6,0), (7,0), (8,0),
        (0,1), (0,2), (1,1), (1,2),
        (3,0), (3,1)
    }
    assert actual_neighbors == expected_neighbors

def test_backtracking_solve():
    sudoku = KingSudoku(board=[
        [0,0,0,0,0,2,0,0,0],
        [0,0,0,4,0,0,8,0,0],
        [0,0,0,0,0,9,7,0,0],
        [4,0,5,0,0,0,0,2,0],
        [0,0,9,0,0,0,1,0,0],
        [0,8,0,0,0,0,4,0,6],
        [0,0,4,1,0,0,0,0,0],
        [0,0,2,0,0,6,0,0,0],
        [0,0,0,8,0,0,0,0,0]
    ])
    sudoku_solver = _KingSudokuSolver(sudoku)
    actual_solution = sudoku_solver.backtracking_solve()
    expected_solution = [[
        [7,4,3,5,8,2,6,9,1],
        [9,5,6,4,7,1,8,3,2],
        [2,1,8,3,6,9,7,4,5],
        [4,6,5,7,1,8,3,2,9],
        [3,2,9,6,4,5,1,7,8],
        [1,8,7,2,9,3,4,5,6],
        [6,9,4,1,5,7,2,8,3],
        [8,7,2,9,3,6,5,1,4],
        [5,3,1,8,2,4,9,6,7]
    ]]
    assert actual_solution == expected_solution