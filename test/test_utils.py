from ktaypuzzles.utils import *

def test_get_factors():
    assert get_factors(1) == [1]
    assert get_factors(49) == [1, 7, 49]
    assert get_factors(50) == [1, 2, 5, 10, 25, 50]