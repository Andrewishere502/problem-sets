"""
Creator: Andrew Berntson
Date: September 1 2020

Problem Set Description:
Given a matrix N by N, rotate it 90 degrees clockwise.

Solution Description:
This is my first version of this solution
"""
import os
from math import sqrt


def get_edge_values(matrix, layer_num):
    """Return a list of values in the specified layer of matrix"""
    nums = []
    start_row, start_col = layer_num, layer_num
    end_row = len(matrix) - (start_row + 1)
    end_col = len(matrix) - (start_col + 1)
    # print(end_row, end_col)

    row = start_row
    col = start_col
    perimeter = (len(matrix[row][start_col:end_col + 1]) - 1) * 4
    # print(perimeter)

    if start_row == end_row:
        return [matrix[row][col]]

    direction = "r"
    for i in range(perimeter):
        nums.append(matrix[row][col])

        if col == end_col and direction == "r":
            direction = "d"
        elif row == end_row and direction == "d":
            direction = "l"
        elif col == start_col and direction == "l":
            direction = "u"
        elif row == start_row and direction == "u":
            return nums[:-1]  # The start point gets counted twice
                              # (start and end)

        if direction == "r":
            col += 1
        elif direction == "d":
            row += 1
        elif direction == "l":
            col -= 1
        elif direction == "u":
            row -= 1
    return nums


def rotate_edge_values(edge_values):
    """Return list of values rotated by n indices. The values should
    come from a layer of a square matrix, thus len(edge_values) will
    equal the perimeter and len(edge_values) / 4 will equal side
    length.
    """
    # Make a copy of edge_values so it doesn't change future values
    # and then shift those values, resulting in duplicate values
    nums = edge_values.copy()
    n = int(len(edge_values) / 4)  # side length
    if len(nums) == 1:
        return nums

    for i in range(len(edge_values)):
        try:
            nums[i + n] = edge_values[i]
        except IndexError:  # value is close to end of list
            # value must move to the beginning (ish) of nums
            nums[i + n - len(nums)] = edge_values[i]
    return nums


def save_rotation(matrix, rotated_values, layer_num):
    """Write rotated_values to layer_num layer of matrix,
    then return the modified matrix.
    """
    start_row, start_col = layer_num, layer_num
    end_row = len(matrix) - (start_row + 1)
    end_col = len(matrix) - (start_col + 1)

    row = start_row
    col = start_col

    direction = "r"
    for num in rotated_values:
        # print(new_matrix[row][col], "to", num)
        matrix[row][col] = num

        if col == end_col and direction == "r":
            direction = "d"
        elif row == end_row and direction == "d":
            direction = "l"
        elif col == start_col and direction == "l":
            direction = "u"

        if direction == "r":
            col += 1
        elif direction == "d":
            row += 1
        elif direction == "l":
            col -= 1
        elif direction == "u":
            row -= 1
    return matrix


def rotate_matrix_90(matrix):
    """Rotate a matrix 90 degrees.
    NOTE: This will modify matrix itself.
    """
    for layer_num in range(round(len(matrix) / 2)):
        edge_values = get_edge_values(matrix, layer_num)
        rotated_values = rotate_edge_values(edge_values)
        matrix = save_rotation(matrix, rotated_values, layer_num)
    return matrix


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


matrix1 = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]
  ]
matrix2 = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12],
          [13, 14, 15, 16]
  ]
matrix3 = [
    [1, 2, 3, 4, 5],
    [16, 1, 0, 2, 6],
    [15, 0, 100, 0, 7],
    [14, 4, 0, 3, 8],
    [13, 12, 11, 10, 9]
    ]


matrices = [matrix1, matrix2, matrix3]

for i, matrix in enumerate(matrices):
    os.system("clear")
    show_matrix(matrix)
    # input("Press [return] to rotate:  ")
    print("Rotated 90 degrees:")
    rotate_matrix_90(matrix)
    show_matrix(matrix)
    if i == len(matrices) - 1:
        input("Press [return] to finish:  ")
    else:
        input("Press [return] to see next:  ")