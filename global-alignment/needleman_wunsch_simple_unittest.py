import unittest

import numpy as np

from global2 import GlobalAlignment


class GlobalAlignmentTest(unittest.TestCase):
    # Verify my implementation of the Needleman-Wunsch global,
    # alignment algorithm that I wrote using the example from the
    # "Needleman–Wunsch algorithm" Wikipedia page:
    # https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm

    @classmethod
    def setUpClass(cls):
        sequence_1 = 'GCATGCG'
        sequence_2 = 'GATTACA'

        cls.aligner = GlobalAlignment(sequence_1, sequence_2)
        cls.aligner.solve_all()
        return

    def test_score_grid(self):
        '''Verify that each cell in the computed score grid is correct.

        Tested against the example from the Wiki.
        '''

        # Correct score grid from the Wiki.
        correct_score_grid = [
            [0, -1, -2, -3, -4, -5, -6, -7],
            [-1, 1, 0, -1, -2, -3, -4, -5],
            [-2, 0, 0, 1, 0, -1, -2, -3],
            [-3, -1, -1, 0, 2, 1, 0, -1],
            [-4, -2, -2, -1, 1, 1, 0, -1],
            [-5, -3, -3, -1, 0, 0, 0, -1],
            [-6, -4, -2, -2, -1, -1, 1, 0],
            [-7, -5, -3, -1, -2, -2, 0, 0]
        ]
        correct_score_grid = np.array(correct_score_grid)

        # Make sure each value in the computed score grid matches the
        # the verified, correct score at that position.
        for row, col in np.ndindex(*correct_score_grid.shape):
            correct_score = correct_score_grid[row][col]
            computed_score = self.aligner.get_score(row, col)
            self.assertEqual(correct_score, computed_score)
        return
    
    def test_path_grid(self):
        '''Verify that each cell in the computed path grid is correct.

        Tested against the example from the Wiki.
        '''

        # Correct path grid from the Wiki.
        correct_path_grid = [
            [0, 1, 1, 1, 1, 1, 1, 1],
            [2, 4, 1, 1, 1, 5, 1, 5],
            [2, 2, 4, 4, 1, 1, 1, 1],
            [2, 2, 6, 2, 4, 1, 1, 1],
            [2, 2, 6, 2, 6, 4, 5, 5],
            [2, 2, 6, 4, 2, 6, 4, 5],
            [2, 2, 4, 2, 2, 6, 4, 1],
            [2, 2, 2, 4, 3, 6, 2, 4]
        ]  # BRAG: I typed in correctly first try B)
        correct_path_grid = np.array(correct_path_grid)

        # Make sure each value in the computed score grid matches the
        # the verified, correct score at that position.
        for row, col in np.ndindex(*correct_path_grid.shape):
            correct_score = correct_path_grid[row][col]
            computed_score = self.aligner.get_arrow(row, col)
            self.assertEqual(correct_score, computed_score)
        return
    
    def test_alignments(self):
        '''Verify that all valid alignments were found.

        Tested against the example from the Wiki.
        '''

        correct_alignments = [
            # First string is sequence 1 alignment, second string is sequence 2 alignment
            ['GCA-TGCG', 'G-ATTACA'],
            ['GCAT-GCG', 'G-ATTACA'],
            ['GCATG-CG', 'G-ATTACA']
        ]
        computed_alignments = self.aligner.traverse()
        for correct_alignment in correct_alignments:
            self.assertIn(correct_alignment, computed_alignments)

        return
    

if __name__ == '__main__':
    unittest.main()
