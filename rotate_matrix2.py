"""
Creator: Andrew Berntson
Date: September 4 2020

Problem Set Description:
Given a matrix N by N, rotate it 90 degrees clockwise.

Solution Description:
This is my second version of this solution
"""
import copy


def show_matrix(matrix):
    """Print matrix in a pretty way."""
    pad = max([len(str(i)) for row in matrix for i in row])
    print(" " + "-" * (pad + 2) * len(matrix[0]) + " ")
    for row in matrix:
        print("|", end="")
        for num in row:
            print(" {:<{pad}} ".format(num, pad=pad), end="")
        print("|")
    print(" " + "-" * (pad + 2) * len(matrix[-1]) + " ")
    return


def rotate_layer(matrix, layer):
    """Rotate a specified layer in a copy of matrix and return this copy.
    NOTE: does not modify the matrix itself!
    """
    new_matrix = copy.deepcopy(matrix)
    row = layer
    col = layer
    end_row = len(matrix) - (layer + 1)
    end_col = len(matrix) - (layer + 1)
    for _ in range((len(matrix[layer]) - 1) * 4):
        move_to_row = row
        move_to_col = col
        if row == layer and col < end_col:
            move_to_row = col
            move_to_col = end_col
        elif col == end_col and row <= end_row:
            move_to_row = end_row
            move_to_col = end_col - row
        elif row == end_col and col >= layer:
            move_to_row = col
            move_to_col = layer
        else:
            move_to_row = layer
            move_to_col = end_col - row
        new_matrix[move_to_row][move_to_col] = matrix[row][col]

        if col < end_col and row == layer:
            col += 1
        elif col == end_col and row < end_row:
            row += 1
        elif row == end_row and col <= end_col and col > layer:
            col -= 1
        elif col == layer and row <= end_row:
            row -= 1
    return new_matrix


def rotate_matrix(matrix):
    """Call rotate_layer for each layer in matrix.
    Return the rotated matrix as new_matrix.
    """
    new_matrix = matrix
    for layer in range(len(matrix) // 2):  # loop through each layer
        new_matrix = rotate_layer(new_matrix, layer)  # rotate layer
    return new_matrix


matrix1 = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]
  ]
matrix2 = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12],
          [13, 14, 15, 16]
  ]


show_matrix(matrix2)
rmatrix2 = rotate_matrix(matrix2)
show_matrix(rmatrix2)