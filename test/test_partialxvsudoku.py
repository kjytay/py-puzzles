import pytest
from ktaypuzzles.partialxvsudoku import PartialXVSudoku

VALID_BOARD_1 = [
    [0,0,0,0,0,3,5,0,0],
    [0,7,0,0,0,0,0,8,1],
    [0,0,0,0,0,8,9,0,0],
    [4,0,0,0,2,0,3,0,0],
    [7,0,0,0,0,4,0,0,0],
    [1,0,0,0,0,0,6,9,0],
    [6,0,0,0,0,9,0,0,0],
    [0,0,0,0,0,0,0,0,3],
    [0,3,0,0,0,0,2,0,0]
]
VALID_X_POSITIONS_1 = [(2, 3, 3, 3), (6, 3, 7, 3)]
VALID_V_POSITIONS_1 = [(7, 6, 7, 7)]

VALID_BOARD_2 = [
    [0,0,0,0,0,3,5,0,0],
    [0,7,0,0,0,0,0,8,1],
    [0,0,0,1,0,8,9,0,0],
    [4,0,0,9,2,0,3,0,0],
    [7,0,0,0,0,4,0,0,0],
    [1,0,0,0,0,0,6,9,0],
    [6,0,0,0,0,9,0,0,0],
    [0,0,0,0,0,0,0,0,3],
    [0,3,0,0,0,0,2,0,0]
]

def test_invalid_board():
    # valid board, invalid X
    with pytest.raises(AssertionError) as exc_info:
        PartialXVSudoku(board=VALID_BOARD_1, X_positions=[(2, 3, 4, 3)], V_positions=VALID_V_POSITIONS_1)
    assert 'The two cells X_positions[i] represent' in str(exc_info.value)

def test_invalid_board2():
    # valid board, valid X, invalid V
    with pytest.raises(AssertionError) as exc_info:
        PartialXVSudoku(board=VALID_BOARD_1, X_positions=VALID_X_POSITIONS_1, V_positions=[(2, 3, 4, 3)])
    assert 'The two cells V_positions[i] represent' in str(exc_info.value)

def test_validate():
    # two filled cells for X clue don't add up to 10
    sudoku = PartialXVSudoku(board=VALID_BOARD_1, X_positions=[(0, 5, 0, 6)])
    assert sudoku.is_valid_puzzle is False

def test_validate2():
    # two filled cells for V clue don't add up to 5
    sudoku = PartialXVSudoku(board=VALID_BOARD_1, V_positions=[(0, 5, 0, 6)])
    assert sudoku.is_valid_puzzle is False

def test_validate3():
    # two filled cells for X clue add up to 10, should be valid
    sudoku = PartialXVSudoku(board=VALID_BOARD_2, X_positions=[(2, 3, 3, 3)])
    assert sudoku.is_valid_puzzle