import pytest
from ktaypuzzles.sudoku import Sudoku

def test_invalid_board():
    """
    Invalid board.
    """
    with pytest.raises(Exception) as excinfo:
        sudoku = Sudoku(
            board = [
            [0,0,0,0,0,4,0,0,0],
            [0,4,0,0,6,0,0,0,0],
            [6,3,0,7,0,9,0,0,2],
            [1,2,4,0,0,6,0,0,5],
            [0,0,3,9,0,0,0,0,0],
            [0,0,0,0,4,2,0,0,3],
            [7,0,0,0,0,0,1,5,7],
            [8,0,9,6,0,5,0,3,0],
            [0,0,0,0,7,0,9,0,0]
        ])
    assert str(excinfo.value) == 'Given board is invalid!'