import pytest
from ktaypuzzles.rect import Rect

def test_invalid_rect():
    with pytest.raises(AssertionError) as exc_info:
        Rect(1, 0, 1, 1)
    assert str(exc_info.value) == 'r1 (1) must be <= r2 (0)'

    with pytest.raises(AssertionError) as exc_info:
        Rect(0, 0, 2, 1)
    assert str(exc_info.value) == 'c1 (2) must be <= c2 (1)'

def test_does_rect_overlap():
    A = Rect(0, 2, 0, 2)
    B = Rect(0, 2, 3, 5)  # B on A's right
    C = Rect(3, 5, 0, 2)  # C below A
    assert A.does_rect_overlap(B) is False
    assert A.does_rect_overlap(C) is False

def test_does_rect_overlap2():
    # overlap
    A = Rect(0, 2, 0, 2)
    B = Rect(2, 5, 0, 2)
    C = Rect(0, 2, 2, 5)
    assert A.does_rect_overlap(B)
    assert A.does_rect_overlap(C)