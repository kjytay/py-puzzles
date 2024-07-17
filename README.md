# py-puzzles

This is my collection of code for generating and solving puzzles. It contains both original code as well as code copied/inspired from other repos.

Here is a list of repos that I have drawn from:
- [jeffsieu/py-sudoku](https://github.com/jeffsieu/py-sudoku)
- [catlzy/shikaku-solver](https://github.com/catlzy/shikaku-solver)

Other credits:
- `shikaku-puzzles` folder copied from [catlzy/shikaku-solver](https://github.com/catlzy/shikaku-solver), originally from https://www.janko.at/Raetsel/Sikaku/index.htm.

# Usage

- [Sudoku](#sudoku)
- [Shikaku](#shikaku)

## Sudoku

Initialize by passing in a board with the `board` parameter. `minirows` (`minicols`) refers to the number of rows (`cols`). `minirows` defaults to 3, `minicols` defaults to `minirows`.

```
from ktaypuzzles.sudoku import Sudoku
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
# +-------+-------+-------+
# |       |     3 | 5     |
# |   7   |       |   8 1 |
# |       | 1   8 | 9     |
# +-------+-------+-------+
# | 4     | 9 2   | 3     |
# | 7     |     4 |       |
# | 1     |       | 6 9   |
# +-------+-------+-------+
# | 6     | 4   9 |       |
# |       | 6     |     3 |
# |   3   |       | 2     |
# +-------+-------+-------+
```
Solve the puzzle with the `solve()` method. Once this is called, the solution is saved as the
`solution` attribute of the Sudoku object. (If there is no solution, `solution` is `None`.) Print the solution to screen using `show_solution()`.
```
test_sudoku.solve()
test_sudoku.show_solution()
# +-------+-------+-------+
# | 9 8 1 | 7 4 3 | 5 2 6 |
# | 3 7 5 | 2 9 6 | 4 8 1 |
# | 2 4 6 | 1 5 8 | 9 3 7 |
# +-------+-------+-------+
# | 4 6 8 | 9 2 1 | 3 7 5 |
# | 7 5 9 | 3 6 4 | 8 1 2 |
# | 1 2 3 | 8 7 5 | 6 9 4 |
# +-------+-------+-------+
# | 6 1 2 | 4 3 9 | 7 5 8 |
# | 5 9 7 | 6 8 2 | 1 4 3 |
# | 8 3 4 | 5 1 7 | 2 6 9 |
# +-------+-------+-------+
```

The `show_as_image()` and `show_as_solution()` methods produce images of the original and solution board respectively. The `title` argument for these methods allow you to change the title of the image, and the `save_path` argument lets you save the image to disk.
```
test_sudoku.show_as_image()
test_sudoku.show_solution_as_image()
test_sudoku.show_solution_as_image(title='Sudoku solution', save_path='test_sudoku_solution.png')
```

If `board` is not passed to the `Sudoku` constructor, the board defaults to the empty board. You can generate a random board with approximately `blank_proportion` cells empty (default 0.5) by calling `generate_puzzle_board()`.
```
import random
random.seed(1)
sudoku = Sudoku(2,3)
sudoku.generate_puzzle_board()
sudoku.show()
# +-------+-------+
# |   4 6 |   5 2 |
# | 1     | 3 6 4 |
# +-------+-------+
# |       |   4 6 |
# |     4 | 5   1 |
# +-------+-------+
# |   6   | 4   5 |
# |     5 | 6     |
# +-------+-------+

sudoku.solve()
sudoku.show_solution()
# +-------+-------+
# | 3 4 6 | 1 5 2 |
# | 1 5 2 | 3 6 4 |
# +-------+-------+
# | 5 3 1 | 2 4 6 |
# | 6 2 4 | 5 3 1 |
# +-------+-------+
# | 2 6 3 | 4 1 5 |
# | 4 1 5 | 6 2 3 |
# +-------+-------+

random.seed(1)
sudoku = Sudoku()
sudoku.generate_puzzle_board(blank_proportion=0.6)
sudoku.show()
# +-------+-------+-------+
# |       |   4 1 |     3 |
# | 2 4   |       | 1 7 5 |
# |   3 1 |     9 | 6 4   |
# +-------+-------+-------+
# |       | 1     |       |
# | 1 8 6 | 2     | 4   9 |
# | 4   5 |       | 7     |
# +-------+-------+-------+
# | 7   3 |   1   |   9   |
# |       | 6 3   | 8 1   |
# | 8   2 | 9 7   |   6   |
# +-------+-------+-------+

# Running generate_puzzle_board() a second time will overwrite the previous puzzle
sudoku.generate_puzzle_board(blank_proportion=0.5)
# +-------+-------+-------+
# |   6 2 |   4   | 7 8 5 |
# | 4     |       | 6 9 1 |
# | 7     | 6   8 | 4   2 |
# +-------+-------+-------+
# | 9 2 7 | 5 3   | 8     |
# |     4 |   2   | 5 7 9 |
# |       | 4     |       |
# +-------+-------+-------+
# |   4   | 7   2 |   5   |
# | 2     |   8 4 | 9   7 |
# | 8   3 |   6 5 |   1   |
# +-------+-------+-------+
```

## Shikaku

[This article](https://www.puzzle-magazine.com/shikaku-strategy.php) contains instructions and strategies for playing Shikaku. Initialize the puzzle by passing in a `board` parameter:

```
from ktaypuzzles.shikaku import Shikaku
test_shikaku = Shikaku([
    [0, 4, 0, 0, 0, 2, 0, 0, 0, 3],
    [3, 0, 0, 0, 5, 0, 0, 0, 3, 0],
    [0, 0, 0, 3, 0, 0, 0, 6, 0, 0],
    [0, 0, 3, 0, 0, 0, 5, 0, 0, 0],
    [0, 3, 0, 0, 0, 4, 0, 0, 0, 5],
    [2, 0, 0, 0, 7, 0, 0, 0, 3, 0],
    [0, 0, 0, 5, 0, 0, 0, 4, 0, 0],
    [0, 0, 5, 0, 0, 0, 4, 0, 0, 0],
    [0, 6, 0, 0, 0, 2, 0, 0, 0, 3],
    [2, 0, 0, 0, 5, 0, 0, 0, 3, 0],
])
```

Print the puzzle to console with the `show()` method. The `show_as_image()` method produces an image of the puzzle.

```
test_shikaku.show()
# +---------------------+
# | - 4 - - - 2 - - - 3 |
# | 3 - - - 5 - - - 3 - |
# | - - - 3 - - - 6 - - |
# | - - 3 - - - 5 - - - |
# | - 3 - - - 4 - - - 5 |
# | 2 - - - 7 - - - 3 - |
# | - - - 5 - - - 4 - - |
# | - - 5 - - - 4 - - - |
# | - 6 - - - 2 - - - 3 |
# | 2 - - - 5 - - - 3 - |
# +---------------------+

test_shikaku.show_as_image()
```

Solve the puzzle with the `solve()` method. Once this is called, the solution is saved as the `solution` attribute of the Sudoku object. (If there is no solution, `solution` is `None`.) `show_solution()` prints the solution to the console (cells with the same number belong to the same rectangle), while `show_solution_as_image()` produces an image of the solution.

```
test_shikaku.solve()
test_shikaku.show_solution()
# +-------------------------------+
# | 00 00 00 00 01 01 09 02 02 02 |
# | 03 04 04 04 04 04 09 05 05 05 |
# | 03 06 06 06 14 11 09 07 07 12 |
# | 03 08 08 08 14 11 09 07 07 12 |
# | 10 10 10 16 14 11 09 07 07 12 |
# | 13 13 18 16 14 11 15 15 15 12 |
# | 20 20 18 16 14 17 17 17 17 12 |
# | 20 20 18 16 14 21 19 19 25 22 |
# | 20 20 18 16 14 21 19 19 25 22 |
# | 23 23 18 24 24 24 24 24 25 22 |
# +-------------------------------+
test_shikaku.show_solution_as_image()
```