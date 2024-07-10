from math import sqrt
from typing import Set

"""
Utility functions that might apply across puzzles.
"""

def get_factors(n: int) -> Set[int]:
    """
    Return all factors of a positive integer n (including 1 and itelf) as a
    sorted list.
    """
    if isinstance(n, int) is False or n < 1:
        raise ValueError('n must an integer >= 1')
    factor_set = set()
    bound = round(sqrt(n))+1
    for i in range(1, int(bound)):
        if n % i == 0:
            if i == n // i:
                factor_set.add(i)
            else:
                factor_set.add(i)
                factor_set.add(n//i)
    
    return sorted(list(factor_set))
