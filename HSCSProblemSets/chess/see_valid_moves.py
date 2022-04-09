"""
Creator: Andrew Berntson
Date: September 19 2020

This file helps visualize the list of valid moves for a piece or
pieces at a location in board.
"""


import os
import random
from pieces import (Pawn, King, Knight,
                    Tower, Bishop, Queen)


class TestBoard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.empty_space = " "

        self.reset_board()
        return

    def get_pieces(self):
        return [space for space in self.board if space != self.empty_space]

    def reset_board(self):
        self.board = [self.empty_space for _ in range(self.rows * self.cols)]
        return

    def place_piece(self, piece, board_i):
        self.board[board_i] = piece
        piece.set_location(board_i)
        return

    def draw(self):
        vsep = "-"  # vertical separator
        hsep = "|"  # horizontal separator
        # padding for the pieces so they all take up the same space
        pad = max([len(str(p)) for p in self.board])
        board_width = (self.cols * (pad + 3) + 1)

        piece_moves = []
        for piece in self.get_pieces():
            piece_moves.extend(piece.valid_moves(self))

        # print horizontal separator above first row
        print(" " + vsep * (board_width - 2) + " ")
        for row in range(self.rows):
            for col in range(self.cols):
                i = row * self.cols + col  # index of the current piece
                if i in piece_moves and self.board[i] == self.empty_space:
                    piece = "x"
                else:
                    piece = self.board[i]
                print(hsep + " {:{pad}} ".format(str(piece), pad=pad), end="")
            print(hsep)  # vertical separator at the end of each row
            # print horizontal separator bellow each row
            print(" " + vsep * (board_width - 2) + " ")
        return


def see_piece_vm_all_cols(piece, start_row=0):
    """Show one piece's valid moves on every column, for both colors.

    start_row -- the row of each pieces as it changes column
    """
    for color in colors:  # colors is global var, don't change
        for i in range(BSIZE[1]):
            cpiece = piece(*color)
            board = TestBoard(*BSIZE)
            os.system("clear")
            board.place_piece(cpiece, start_row * BSIZE[1] + i)
            board.draw()
            input("[RETURN] to see next move")
    print("DONE")
    return


def see_piece_vm_all_rows(piece, start_col=0):
    """Show one piece's valid moves on every row, for both colors.

    start_col -- the column of each pieces as it changes row
    """
    for color in colors:  # colors is global var, don't change
        for i in range(BSIZE[0]):
            cpiece = piece(*color)
            board = TestBoard(*BSIZE)
            os.system("clear")
            board.place_piece(cpiece, i * BSIZE[1] + start_col)
            board.draw()
            input("[RETURN] to see next move")
    print("DONE")
    return


def see_all_pieces_vm(pieces, index):
    """Show each piece in pieces at index, for bothcolors.

    pieces -- all pieces which will can be shown on board
    index -- the index where each piece will be placed in board
    """
    for piece in pieces:
        for color in colors:
            cpiece = piece(*color)
            board = TestBoard(*BSIZE)
            os.system("clear")
            print("valid moves for {} {}:".format(color[1], cpiece.name))
            board.place_piece(cpiece, index)
            board.draw()
            input("[RETURN] to see next piece")
    print("DONE")
    return


def see_many_piece_vm_randindex(pieces, sample_num, setup_num=6):
    """Show the valid moves for number of randomly selected pieces
    (colors also random).

    pieces -- all pieces which will can be shown on board
    sample_num -- number of pieces being shown at once, must be
                  greater than 1
    setup_num -- number of random setups to be shown
    """
    for _ in range(setup_num):
        board = TestBoard(*BSIZE)
        sample_pieces = random.sample(pieces, sample_num)
        color = random.choice(colors)
        for piece in sample_pieces:
            board.place_piece(piece(*color), random.randint(0, BSIZE[0] * BSIZE[1] - 1))
        os.system("clear")
        board.draw()
        input("[RETURN] to see next set up")
    print("DONE")
    return


white = ("north", "white")
black = ("south", "black")
colors = [white, black]


all_pieces = (Pawn, King, Knight, Tower, Bishop, Queen)
# BSIZE = (25, 25)
BSIZE = (10, 11)  # size of board, (rows, columns)

see_piece_vm_all_cols(Queen, 0)
