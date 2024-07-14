class Rect:

    def __init__(self, r1: int, r2: int, c1: int, c2: int):
        """
        Rectangle is defined by first and last row index of the rectangle (r1, r2)
        and first and last column index of the rectangle (c1, c2).
        In this implementation, think of each (r,c) index as representing a
        box rather than a point.
        """
        assert r1 <= r2, 'r1 ({}) must be <= r2 ({})'.format(r1, r2)
        assert c1 <= c2, 'c1 ({}) must be <= c2 ({})'.format(c1, c2)
        self.r1 = r1
        self.r2 = r2
        self.c1 = c1
        self.c2 = c2

    def does_rect_overlap(self, other: 'Rect'):
        # check if one rectangle is above the other
        if self.r2 < other.r1 or other.r2 < self.r1:
            return False
        
        # check if one rectangle is to the left of the other
        if self.c2 < other.c1 or other.c2 < self.c1:
            return False
        
        return True
    
    def __str__(self):
        return 'Rect({}, {}, {}, {})'.format(self.r1, self.r2, self.c1, self.c2)
    
    def __eq__(self, other):
        if not isinstance(other, Rect):
            return NotImplemented

        return (self.r1 == other.r1 and self.r2 == other.r2 and
                self.c1 == other.c1 and self.c2 == other.c2)