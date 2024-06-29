from ktaypuzzles.sudoku import Sudoku


def test_placeholder():
    sudoku = Sudoku()
    assert sudoku.test == 'test'