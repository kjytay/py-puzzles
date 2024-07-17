from ktaypuzzles.rect import Rect
from ktaypuzzles.shikaku import Shikaku, _ShikakuSolver

VALID_SHIKAKU_BOARD = [
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
]

VALID_SHIKAKU_BOARD_2 = [
    [0, 0, 3, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 0],
    [0, 8, 4, 0, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0],
    [3, 0, 0, 5, 0, 2, 0]
]

# multiple solutions
VALID_SHIKAKU_BOARD_3 = [
    [0, 4, 0, 0],
    [0, 0, 0, 4],
    [0, 4, 4, 0],
    [0, 0, 0, 0]
]

def test_is_rect_in_board():
    shikaku = Shikaku(VALID_SHIKAKU_BOARD)
    assert shikaku._is_rect_in_board(Rect(0, 5, 0, 9))
    assert shikaku._is_rect_in_board(Rect(0, 5, 0, 10)) is False
    assert shikaku._is_rect_in_board(Rect(5, 10, 0, 9)) is False

def test_get_valid_rects():
    shikaku = Shikaku(VALID_SHIKAKU_BOARD)
    shikaku_solver = _ShikakuSolver(shikaku)
    state = [Rect(r, r, c, c) for (_, r, c, _) in shikaku.anchors]
    actual_rects = shikaku_solver._get_valid_rects((0, 0, 1, 4), state)
    expected_rects = [Rect(0, 0, 1, 4), Rect(0, 0, 0, 3), Rect(0, 1, 1, 2), Rect(0, 3, 1, 1)]
    assert actual_rects == expected_rects

def test_get_valid_rects2():
    shikaku = Shikaku(VALID_SHIKAKU_BOARD)
    shikaku_solver = _ShikakuSolver(shikaku)
    state = [Rect(r, r, c, c) for (_, r, c, _) in shikaku.anchors]
    state[1] = Rect(0, 0, 4, 5)
    actual_rects = shikaku_solver._get_valid_rects((0, 0, 1, 4), state)
    expected_rects = [Rect(0, 0, 0, 3), Rect(0, 1, 1, 2), Rect(0, 3, 1, 1)]
    assert actual_rects == expected_rects

def test_prune_candidates_dict():
    candidates_dict = {0: [Rect(0,0,0,3), Rect(0,1,0,1), Rect(0,1,1,2)]}
    pruned_candidates_dict = _ShikakuSolver._prune_candidates_dict(candidates_dict, 1, Rect(0,3,3,3))
    expected_dict = {0: [Rect(0,1,0,1), Rect(0,1,1,2)]}
    assert pruned_candidates_dict == expected_dict

def test_backtracking_solve():
    shikaku = Shikaku(VALID_SHIKAKU_BOARD_2)
    shikaku_solver = _ShikakuSolver(shikaku)
    actual_solution = shikaku_solver.backtracking_solve()
    expected_solution = [
        [Rect(0, 0, 0, 2), Rect(0, 0, 3, 6), Rect(1, 1, 2, 6), Rect(1, 4, 0, 1), Rect(2, 5, 2, 2),
         Rect(2, 6, 4, 4), Rect(2, 5, 5, 6), Rect(5, 5, 0, 1), Rect(6, 6, 0, 2), Rect(2, 6, 3, 3),
         Rect(6, 6, 5, 6)]]
    assert actual_solution == expected_solution

def test_backtracking_solve2():
    # board with multiple solutions
    shikaku = Shikaku(VALID_SHIKAKU_BOARD_3)
    shikaku_solver = _ShikakuSolver(shikaku)
    actual_solution = shikaku_solver.backtracking_solve()
    expected_solution = [
        [Rect(0, 0, 0, 3), Rect(1, 1, 0, 3), Rect(2, 3, 0, 1), Rect(2, 3, 2, 3)],
        [Rect(0, 1, 0, 1), Rect(0, 1, 2, 3), Rect(2, 3, 0, 1), Rect(2, 3, 2, 3)],
        [Rect(0, 1, 0, 1), Rect(0, 3, 3, 3), Rect(2, 3, 0, 1), Rect(0, 3, 2, 2)]
    ]
    assert actual_solution == expected_solution