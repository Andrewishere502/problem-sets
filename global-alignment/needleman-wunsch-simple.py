'''Align two sequences globally using the Needleman-Wunsch algorithm.'''


__author__ = 'Andrew Berntson'
__date__ = '06/03/2025'
__version__ = '1.0'


from typing import List, Tuple

import numpy as np


class GlobalAlignment:
    def __init__(self, sequence_1: str, sequence_2: str, match=1, mismatch=-1, indel=-1):
        self.__sequence_1 = sequence_1
        self.__sequence_2 = sequence_2
        self.__penalty_table = {
                'match': match,        # Reward for matching base pairs
                'mismatch': mismatch,  # Penalty for mismatching base pairs
                'indel': indel         # Penalty for insertion/deletion
            }

        # Represent the grid as a score layer and a path layer of arrows
        self.__score_grid = np.zeros((self.n_rows, self.n_cols), dtype=int)
        self.__path_grid = np.zeros((self.n_rows, self.n_cols), dtype=np.byte)
        return
    
    @property
    def n_cols(self):
        '''Return the number of columns in the grid.'''
        return len(self.__sequence_1) + 1
    
    @property
    def n_rows(self):
        '''Return the number of rows in the grid.'''
        return len(self.__sequence_2) + 1
    
    @property
    def col_header(self):
        '''Return the grid header for the columns.'''
        return ' ' + self.__sequence_1

    @property
    def row_header(self):
        '''Return the grid header for the rows.'''
        return ' ' + self.__sequence_2
    
    def get_score(self, row, col):
        return self.__score_grid[row][col]

    def get_arrow(self, row, col):
        return self.__path_grid[row][col]

    @staticmethod
    def compare_chars(char_1, char_2):
        '''Return match if the characters match, or mismatch if they don't.'''
        if char_1 == char_2:
            return 'match'
        else:
            return 'mismatch'

    @staticmethod
    def encode_direction(dr: int, dc: int) -> np.byte:
        '''Encode the position vector's components as a byte with one
        bit set, which corresponds to the direction that the position
        vector points int.
            
        left - 0b001
        up - 0b010
        up left - 0b100
        '''
        if dr == 0 and dc == -1:
            return np.byte(0b001)
        elif dr == -1 and dc == 0:
            return np.byte(0b010)
        elif dr == -1 and dc == -1:
            return np.byte(0b100)

    @staticmethod
    def decode_directions(arrow: np.byte) -> List[str]:
        '''Return a list of directions based on the given encoding.
        Valid directions include left, up, and upleft
        '''
        # Parse the bits corresponding to each direction
        go_left = bool(0b001 & arrow)
        go_up = bool(0b010 & arrow)
        go_up_left = bool(0b100 & arrow)

        # Construct the directions
        directions = []
        if go_left:
            directions.append('left')
        if go_up:
            directions.append('up')
        if go_up_left:
            directions.append('upleft')
        return directions

    def get_neighbor_scores(self, row, col) -> List[Tuple[np.byte, int]]:
        '''Return a list of tuples where the first tuple element is
        the direction of the neighbor encoded as a byte and the second
        element is the score of that neighbor.
        Returns an empty list if the target cell is in the top left
        corner.
        '''

        # Store neighbors as a position vector relative to any given
        # cell
        neighbors_deltas = [
            (0, -1),  # Left neighbor
            (-1, 0),  # Up neighbor
            (-1, -1)  # Diagonal up-left neighbor
        ]
        # Append an arrow pointing to each neighbor and its score
        scores = []
        for dr, dc in neighbors_deltas:
            neighbor_row = row + dr
            if neighbor_row < 0:  # Skip up neighbor if in top row
                continue

            neighbor_col = col + dc
            if neighbor_col < 0:  # Skip left neighbor if in left column
                continue
            

            # Now calculate the penalty based on indel, match, or
            # mismatch
            penalty = 0
            
            if dr != dc:  # indel
                penalty = self.__penalty_table['indel']
            else:
                char_1 = self.col_header[col]
                char_2 = self.row_header[row]
                status = self.compare_chars(char_1, char_2)
                penalty = self.__penalty_table[status]

            # Get the neighbor's score
            neighbor_score = self.__score_grid[neighbor_row][neighbor_col]

            scores.append((self.encode_direction(dr, dc), neighbor_score + penalty))

        return scores

    def solve_cell(self, row, col) -> None:
        '''Compute the score for a cell given by its row and column in
        the grid. Store the computed score in the score grid directly,
        and store the arrow pointing to the donor neighbor(s) in the
        path grid directly.
        '''
        # Get scores for each neighbor
        neighbor_scores = self.get_neighbor_scores(row, col)  # NOTE this actually gets the scores for this cell based on the neighbors, not the actual neighbor's scores

        # If there were no neighbors, cell must be in top left corner, so
        # it should be set to 0
        if len(neighbor_scores) == 0:
            self.__score_grid[row][col] = 0
            # Don't change the path_grid direction for this cell

        # Otherwise, chose the maximum neighbor score
        else:
            best_score = max(neighbor_scores, key=lambda p: p[1])[1]
            self.__score_grid[row][col] = best_score
            # Update path_grid with directions to the neighboring cells
            # that gave this cell its score
            for arrow, _ in filter(lambda ns: ns[1] == best_score, neighbor_scores):
                # Bitwise or to combine encodings
                self.__path_grid[row][col] |= arrow
        return

    def solve_all(self):
        # Solve the cells row-by-row, building the path
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                self.solve_cell(r, c)
        return None

    def print_grid(self) -> None:
        grid = self.__score_grid
        # grid = self.__path_grid

        print('   ' + ' '.join(map(lambda c: f'{c:>3}', self.col_header)))
        for i, row in enumerate(grid):
            print(f'{self.row_header[i]:3}' + ' '.join(map(lambda r: f'{r:>3}', row)))
        return

    def traverse(self, row=None, col=None, alignment_i=0, alignments=[['', '']]) -> List[List]:
        # Set row and column to bottom right corner
        if row == None and col == None:
            row = self.n_rows - 1
            col = self.n_cols - 1

        directions = self.decode_directions(self.__path_grid[row][col])

        alignment_1 = alignments[alignment_i][0]
        alignment_2 = alignments[alignment_i][1]

        for i, direction in enumerate(directions):
            if i > 0:
                alignments.append([alignment_1, alignment_2])
                alignment_i = len(alignments) - 1

            if direction == 'upleft':
                base_1 = self.__sequence_1[col - 1]
                base_2 = self.__sequence_2[row - 1]
                next_row = row - 1
                next_col = col - 1
            elif direction == 'up':
                base_1 = '-'
                base_2 = self.__sequence_2[row - 1]
                next_row = row - 1
                next_col = col
            elif direction == 'left':
                base_1 = self.__sequence_1[col - 1]
                base_2 = '-'
                next_row = row
                next_col = col - 1

            alignments[alignment_i][0] = base_1 + alignment_1
            alignments[alignment_i][1] = base_2 + alignment_2
            self.traverse(next_row, next_col, alignment_i=alignment_i, alignments=alignments) 
        
        return alignments
    



if __name__ == '__main__':
    print('Running example from Needleman-Wunsch algorithm Wikipedia page:')

    sequence_1 = 'GCATGCG'
    sequence_2 = 'GATTACA'

    align = GlobalAlignment(sequence_1, sequence_2)

    align.solve_all()
    
    align.print_grid()

    for alignment_1, alignment_2 in align.traverse():
        print(alignment_1, alignment_2, sep='\n', end='\n\n')

