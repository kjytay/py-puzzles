from ktaypuzzles.rect import Rect
from ktaypuzzles.shikaku import Shikaku

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

def test_is_rect_in_board():
    shikaku = Shikaku(VALID_SHIKAKU_BOARD)
    assert shikaku._is_rect_in_board(Rect(0, 5, 0, 9))
    assert shikaku._is_rect_in_board(Rect(0, 5, 0, 10)) is False
    assert shikaku._is_rect_in_board(Rect(5, 10, 0, 9)) is False

def test_get_valid_rects():
    shikaku = Shikaku(VALID_SHIKAKU_BOARD)
    state = [Rect(r, r, c, c) for (_, r, c, _) in shikaku.anchors]
    actual_rects = shikaku._get_valid_rects((0, 0, 1, 4), state)
    expected_rects = [Rect(0, 0, 1, 4), Rect(0, 0, 0, 3), Rect(0, 1, 1, 2), Rect(0, 3, 1, 1)]
    assert actual_rects == expected_rects

def test_get_valid_rects2():
    shikaku = Shikaku(VALID_SHIKAKU_BOARD)
    state = [Rect(r, r, c, c) for (_, r, c, _) in shikaku.anchors]
    state[1] = Rect(0, 0, 4, 5)
    actual_rects = shikaku._get_valid_rects((0, 0, 1, 4), state)
    expected_rects = [Rect(0, 0, 0, 3), Rect(0, 1, 1, 2), Rect(0, 3, 1, 1)]
    assert actual_rects == expected_rects