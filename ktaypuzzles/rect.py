from dataclasses import dataclass

@dataclass
class Rect:
    """
    Rectangle is defined by first and last row index of the rectangle (r1, r2)
    and first and last column index of the rectangle (c1, c2).
    In this implementation, think of each (r,c) index as representing a
    box rather than a point.
    """
    r1: int
    r2: int
    c1: int
    c2: int

    def __post_init__(self):
        assert self.r1 <= self.r2, 'r1 ({}) must be <= r2 ({})'.format(self.r1, self.r2)
        assert self.c1 <= self.c2, 'c1 ({}) must be <= c2 ({})'.format(self.c1, self.c2)

    def does_rect_overlap(self, other: 'Rect'):
        # check if one rectangle is above the other
        if self.r2 < other.r1 or other.r2 < self.r1:
            return False
        
        # check if one rectangle is to the left of the other
        if self.c2 < other.c1 or other.c2 < self.c1:
            return False
        
        return True
