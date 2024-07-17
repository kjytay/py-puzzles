import copy
import matplotlib.pyplot as plt
from typing import Dict, Iterable, List, Optional, Union, Tuple
from .rect import Rect
from .utils import get_factors

"""
Each Shikaku board is represented a `Board` object, where board[r][c] is either
a number or None (indicating an empty cell).
"""
# aliases
Board = List[List[Union[int, None]]]
Anchor = Tuple[int, int, int, int]  # (anchor_index, r, c, board[r][c])
State = List[Rect]  # State[i]: rectangle associated with anchor [i]
EMPTY = None

class Shikaku:

    def __init__(self, board: Iterable[Iterable[Union[int, None]]]):
        """
        Initializes a Shikaku board.
        An anchor refers to the cell which is given in the puzzle. Its value
        indicates the area of the rectangle that the cell belongs to.
        """
        self.rows = len(board)
        self.cols = len(board[0])
        for row in board:
            assert len(row) == self.cols, '# cols in board ({}) should be {}'.format(len(row), self.cols)
        self.board: Board = [
            [cell for cell in row] for row in board
        ]
        # replace anything other than valid integers with an empty cell
        # populate anchor list at the same time.
        self.anchors: List[Anchor] = []
        anchor_index = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if isinstance(self.board[r][c], int) is False or self.board[r][c] < 1:
                    self.board[r][c] = EMPTY
                else:
                    self.anchors.append((anchor_index, r, c, board[r][c]))
                    anchor_index += 1
        self.is_solved = False
        self.solution = None
    
    def solve(self) -> Optional[State]:
        """
        Solve the shikaku board. Solution is saved as self.solution, and also returned.
        """
        shikaku_solver = _ShikakuSolver(self)
        solution_list = shikaku_solver.backtracking_solve()
        self.is_solved = len(solution_list) > 0
        self.solution = solution_list[0] if self.is_solved else None
        return solution_list[0]
    
    def _is_rect_in_board(self, rect: Rect) -> bool:
        """
        Returns True if a rect is within the bounds of the board, else False.
        """
        return 0 <= rect.r1 and rect.r2 < self.rows and 0 <= rect.c1 and rect.c2 < self.cols

    @staticmethod
    def get_board_ascii(board: Board) -> str:
        rows = len(board)
        cols = len(board[0])
        maxval = max([max([x if x is not None else 0 for x in row]) for row in board])
        table = ''
        cell_length = len(str(maxval))
        format_int = '{0:0' + str(cell_length) + 'd}'
        for i, row in enumerate(board):
            if i == 0:
                table += ('+-' + '-' * (cell_length + 1) *
                          cols) + '+' + '\n'
            table += (('| ' + '{} ' * cols) + '|').format(*[format_int.format(
                x) if x != EMPTY else '-' * cell_length for x in row]) + '\n'
            if i == len(board) - 1:
                table += ('+-' + '-' * (cell_length + 1) *
                          cols) + '+' + '\n'
        return table
    
    def __str__(self) -> str:
        """
        Prints the original board.
        """
        return '''
--------------------
{}x{} SHIKAKU PUZZLE
--------------------
{}
        '''.format(self.rows, self.cols,
                   Shikaku.get_board_ascii(self.board))
    
    def show(self):
        print(Shikaku.get_board_ascii(self.board))
    
    def show_solution(self):
        if self.solution is not None:
            print('not implemented yet') # TODO
        return

    def show_as_image(self, title: str = 'Shikaku', save_path: str = '') -> None:
        """
        Draw image of the original board.
        """
        self._get_board_image(title=title, save_path=save_path)
    
    def show_solution_as_image(self, title: str = 'Shikaku', save_path: str = '') -> None:
        """
        Draw image of the board with solution overlaid on top.
        """
        self._get_board_image(self.solution, title=title, save_path=save_path)

    def _get_board_image(self, solution: Optional[List[Rect]] = None, title: str = '',
                         save_path: str = '') -> None:
        """
        Draw an image of the given board.
        If solution is provided, draw the rectangles of the solution too.
        """
        fig, ax = plt.subplots(figsize=(6, 6))

        # draw main grid
        for i in range(self.rows+1):
            ax.plot([0, self.cols], [i, i], color='black', linewidth=0.5)
        for i in range(self.cols+1):
            ax.plot([i, i], [0, self.rows], color='black', linewidth=0.5)

        # add numbers
        for (_, r, c, val) in self.anchors:
            ax.text(c + 0.5, self.rows - 0.5 - r, str(val),
                    ha='center', va='center', fontsize=12, color='black')
            
        # if solution is provided, draw the rectangles
        if solution is not None:
            for rect in solution:
                ax.plot([rect.c1, rect.c1], [self.rows-rect.r1, self.rows-rect.r2-1],
                        color='black', linewidth=3)
                ax.plot([rect.c2+1, rect.c2+1], [self.rows-rect.r1, self.rows-rect.r2-1],
                        color='black', linewidth=3)
                ax.plot([rect.c1, rect.c2+1], [self.rows-rect.r1, self.rows-rect.r1],
                        color='black', linewidth=3)
                ax.plot([rect.c1, rect.c2+1], [self.rows-rect.r2-1, self.rows-rect.r2-1],
                        color='black', linewidth=3)
        
        # set the axis properties
        ax.set_xlim(-1, self.cols+1)
        ax.set_ylim(-1, self.rows+1)
        ax.set_aspect('equal')
        ax.axis('off')

        # add title
        ax.set_title(title, fontsize=20, pad=20)

        if save_path != '':
            plt.savefig(save_path, bbox_inches='tight')
        
        plt.show()


class _ShikakuSolver:
    def __init__(self, shikaku: Shikaku):
        self.shikaku = shikaku
        self.rows = shikaku.rows
        self.cols = shikaku.cols
        self.board = shikaku.board
        self.anchors = shikaku.anchors
        self.num_anchors = len(self.anchors)
    
    def _get_valid_rects(self, anchor: Anchor, state: State) -> List[Rect]:
        """
        Given a board state, return all possible rectangles for a given anchor as a list.
        """
        valid_rect_list = []
        anchor_index, r, c, area = anchor
        factor_list = get_factors(area)
        for num_rows in factor_list:
            num_cols = area // num_rows
            for row_offset in range(num_rows):
                for col_offset in range(num_cols):
                    r1 = r - row_offset
                    c1 = c - col_offset
                    rect = Rect(r1, r1 + num_rows - 1, c1, c1 + num_cols - 1)
                    if not self.shikaku._is_rect_in_board(rect):  # out of bounds
                        continue
                    overlaps = False
                    for i, s in enumerate(state):
                        if anchor_index != i and rect.does_rect_overlap(s):
                            # overlaps with existing rectangle
                            overlaps = True
                            break
                    if not overlaps:
                        valid_rect_list.append(rect)
        
        return valid_rect_list
    
    @staticmethod
    def _prune_candidates_dict(candidates_dict: Dict[int, List[Rect]],
                               anchor_index_added: int, rect_added: Rect):
        new_candidates_dict = {}
        for i, original_candidate_rects in candidates_dict.items():
            if i == anchor_index_added:
                new_candidates_dict[i] = candidates_dict[i]
            else:
                new_candidates_dict[i] = []
                for rect in original_candidate_rects:
                    if not rect.does_rect_overlap(rect_added):
                        new_candidates_dict[i].append(rect)
        return new_candidates_dict

    def backtracking_solve(self) -> List[State]:
        """
        Solve the shikaku puzzle with backtracking. Solutions are returned as a list: if the
        board admits multiple solutions, all solutions are returned. If there is no solution,
        empty list is returned.
        """
        # initialize board with 1x1 rectangles on each anchor
        current_state = [Rect(r, r, c, c) for (_, r, c, _) in self.anchors]

        # for each anchor, find all valid rectangles for it
        candidates_dict: Dict[int, List[Rect]] = {}
        for anchor in self.anchors:
            candidates_dict[anchor[0]] = self._get_valid_rects(anchor, current_state)
        
        solution_list = []
        self._do_backtracking(current_state, candidates_dict, solution_list)

        return solution_list
    
    def _do_backtracking(self, current_state: State, candidates_dict: Dict[int, List[Rect]],
                         solution_list: List[State]) -> None:
        if len(candidates_dict) == 0:
            # recursion base case: all anchors assigned
            solution_list.append(copy.deepcopy(current_state))
            return
        else:
            # recursive case
            # assign an anchor (the one with the smallest no of possibilities)
            candidates_list = sorted(candidates_dict.items(), key=lambda item: len(item[1]))
            current_anchor_index = candidates_list[0][0]
            current_candidates = candidates_list[0][1]
            for candidate in current_candidates:
                # explore
                current_state[current_anchor_index] = candidate
                original_candidates_dict = copy.deepcopy(candidates_dict)
                del candidates_dict[current_anchor_index]
                pruned_candidates_dict = _ShikakuSolver._prune_candidates_dict(
                    candidates_dict, current_anchor_index, candidate)

                self._do_backtracking(current_state, pruned_candidates_dict, solution_list)

                # undo recursion
                candidates_dict = original_candidates_dict
                current_state[current_anchor_index] = Rect(
                    self.anchors[current_anchor_index][1],
                    self.anchors[current_anchor_index][1],
                    self.anchors[current_anchor_index][2],
                    self.anchors[current_anchor_index][2])

if __name__ == '__main__':

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
    print(test_shikaku)
    test_shikaku.solve()
    test_shikaku.show_solution_as_image()
