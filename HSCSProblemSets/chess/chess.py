"""
Creator: Andrew Berntson
Date: September 19 2020

Problem Set Description:
Create a chess game.
Solution Description:
I made chess. Different pieces can be found in pieces.py,
and it should be fairly easy to add your own pieces if you want.
Running this file will allow you to play chess.
"""


import os
import random
import re

from pieces import (Pawn, King, Knight,
                    Tower, Bishop, Queen)


class ChessBoard:
    def __init__(self, rows, cols, DEBUG=False):
        self.DEBUG = DEBUG  # give special privalges for debug mode
        # Special privalges include:
        #   - any player can move at any time, not alternating
        #   - don't force player to move out of a check

        self.rows = rows
        self.cols = cols
        self.x_labels = list(range(1, self.cols + 1))
        self.y_labels = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.empty_space = " "

        self.winner = None
        self.player_move = "white"
        self.turn = 0
        self.morgue = []
        self.reset_board()
        return

    def next_player_turn(self):
        """Switch turn to the next player."""
        if self.player_move == "white":
            self.player_move = "black"
        else:
            self.player_move = "white"
        return

    def reset_board(self):
        """Reset board to the original piece set up. This erases the
        previous board set up.
        """
        self.board = [self.empty_space for _ in range(self.rows * self.cols)]

        white = ("north", "white")
        black = ("south", "black")

        white_piece_rows = {
            -2: [Pawn(*white) for i in range(self.cols)],
            -1: [Tower(*white), Knight(*white), Bishop(*white), Queen(*white),
                King(*white), Bishop(*white), Knight(*white), Tower(*white)],
            }
        black_piece_rows = {
            0: [Tower(*black), Knight(*black), Bishop(*black), King(*black),
                Queen(*black), Bishop(*black), Knight(*black), Tower(*black)],
            1: [Pawn(*black) for i in range(self.cols)]
            }

        self.place_pieces(black_piece_rows)
        self.place_pieces(white_piece_rows)
        return

    def place_piece(self, piece, board_i):
        """Place a single piece at a specified board index."""
        self.board[board_i] = piece
        piece.set_location(board_i)
        return

    def place_pieces(self, piece_rows):
        """Place pieces from the left most row to the right most, at
        a specified row.
        
        piece_row -- a dict where each key is the row in board, and
                     the respective value is an iterable of
                     uninstantiated piece objects. Skipping columns
                     can be done by using None instead of a piece
                     object.
        """
        for row, pieces in piece_rows.items():
            for i in range(len(pieces)):
                if pieces[i] != None:
                    if row >= 0:
                        location = row * self.cols + i  # index of piece
                    else:
                        location = (self.rows - abs(row)) * self.cols + i
                    self.place_piece(pieces[i], location)
        return

    def draw(self):
        """Print the map out on to the screen."""
        vsep = "-"  # vertical separator
        hsep = "|"  # horizontal separator
        # padding for the pieces so they all take up the same space
        pad = max([len(str(p)) for p in self.board])
        board_width = (self.cols * (pad + 3) + 1)

        y_label_pad = 2  # spaces between the y label and the board
        left_indent = len(str(self.y_labels[-1])) + y_label_pad

        print(" " * left_indent, end="")
        for x_label in self.x_labels:
            print("  {:{pad}} ".format(x_label, pad=pad), end="")
        print()

        # print horizontal separator above first row
        print(" " * left_indent + " " + vsep * (board_width - 2) + " ")
        for row in range(self.rows):
            print(self.y_labels[row], end=" " * y_label_pad)
            for col in range(self.cols):
                i = row * self.cols + col  # index of the current piece
                piece = self.board[i]
                print(hsep + " {:{pad}} ".format(str(piece), pad=pad), end="")
            print(hsep)  # vertical separator at the end of each row
            # print horizontal separator bellow each row
            print(" " * left_indent + " " + vsep * (board_width - 2) + " ")
        return

    def __get_player_king_i(self, color):
        """Return the index of the specified player/color's king."""
        for piece in self.board:
            try:
                if (piece.color == color
                    and piece.name == "king"):
                    return piece.location
            except AttributeError:
                pass  # this piece is empty
        return

    def __get_all_player_pieces(self, color):
        """Return a list of all a player/color's living pieces."""
        pieces = []
        for piece in self.board:
            try:
                if piece.color == color:
                    pieces.append(piece)
            except AttributeError:
                pass  # this piece is empty
        return pieces

    def __get_all_player_moves(self, color):
        """Return a list of all indices a player/color can move to with
        at least one piece.
        """
        moves = []
        for piece in self.__get_all_player_pieces(color):
            moves.extend(piece.valid_moves(self))
        return moves

    def player_checkmated(self, color):
        """Return True if a player is checkmated, False if not."""
        player_pieces = self.__get_all_player_pieces(color)
        for piece in player_pieces:
            for move in piece.valid_moves(self):
                start_i = piece.location
                end_i = move
                moved_piece, move_to_piece = self.move_piece(start_i, end_i)
                if not self.is_player_checked(color):
                    self.move_piece(end_i, start_i, move_to_piece)
                    return False
                else:
                    self.move_piece(end_i, start_i, move_to_piece)
        return True
        
    def is_player_checked(self, color):
        """Return true if a player/color's king is checked."""
        other_player = self.get_other_player(color)
        return self.__get_player_king_i(color) in self.__get_all_player_moves(other_player)

    def get_other_player(self, color):
        """Return the player who is not the player passed as color arg."""
        players = ["white", "black"]
        players.remove(color)
        return players[0]

    @staticmethod
    def __letters_to_num(letters):
        """Convert a letter to a number, then return that number."""
        letter_to_num_dict = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8,
            "i": 9,
            "j": 10,
            "k": 11,
            "l": 12,
            "m": 13,
            "n": 14,
            "o": 15,
            "p": 16,
            "q": 17,
            "r": 18,
            "s": 19,
            "t": 20,
            "u": 21,
            "v": 22,
            "w": 23,
            "x": 24,
            "y": 25,
            "z": 26
            }
        total = 0
        for i in range(len(letters)):
            num = letter_to_num_dict[letters[i]]
            extra_26s = (len(letters) - i - 1)
            num = num * 26 ** extra_26s
            total += num
        return total

    def __coord_to_index(self, coords):
        """Convert a coordinate to an index value, then return that
        index.
        """
        # coords[0] is y, coords[1] is x
        coords = [i - 1 for i in coords]
        index = coords[0] * self.rows + coords[1]
        return index

    def parse_move(self, move):
        """Parse the move input by the player into a start coordinate
        and an end coordinate.
        """
        # NOTE: coordinates are (y, x)
        move = re.match(r"(?P<sy>[a-z]+)(?P<sx>[0-9]+)[^a-z0-9]*(?P<ey>[a-z]+)(?P<ex>[0-9]+)", move)
        start = list(move.groups()[0:2])
        start[0] = self.__letters_to_num(start[0])  # convert letter to num
        start[1] = int(start[1])  # convert num which is str to int

        end = list(move.groups()[2:])
        end[0] = self.__letters_to_num(end[0])  # convert letter to num
        end[1] = int(end[1])  # convert num which is str to int

        start = self.__coord_to_index(start)
        end = self.__coord_to_index(end)
        return start, end

    def move_piece(self, start_i, end_i, replace_piece=None):
        """Move a piece from it's index to another index."""
        # Pop piece and replace it's location in self.board with an
        # empty space (default), or a specified piece (replace_piece).
        moved_piece = self.board.pop(start_i)
        if replace_piece == None:
            replace_piece = self.empty_space
        self.board.insert(start_i, replace_piece)
        # Pop the piece that the selected piece will move to, then
        # replace it's location in self.board with the piece that
        # killed it.
        move_to_piece = self.board.pop(end_i)
        self.board.insert(end_i, moved_piece)
        moved_piece.move(end_i)  # update piece's index
        return moved_piece, move_to_piece

    def make_move(self, start_i, end_i):
        """Control the movement of a piece at start_i to end_i."""
        global message
        if self.board[start_i] != self.empty_space:
            if (self.board[start_i].color == self.player_move
                or self.DEBUG):
                valid_moves = self.board[start_i].valid_moves(self)
            else:
                message = "It is {}'s turn".format(self.player_move)
                return
        else:
            message = "Can't move blank space"
            return

        if end_i in valid_moves:
            moved_piece, move_to_piece = self.move_piece(start_i, end_i)  # do player move

            # Player is still checked, even after trying to move
            if (self.is_player_checked(self.player_move)
                and not self.DEBUG):
                # Undo the player move:
                self.move_piece(end_i, start_i)  # unpacking returned
                                                 # vars here isn't needed
                message = "Invalid, must move out of check"
                return

            # If the piece to move to is not just an empty
            # spot, log the kill in the morgue.
            if move_to_piece != self.empty_space:
                log = {
                    "RIP": move_to_piece,
                    "Killer": moved_piece,
                    "Turn": self.turn
                    }
                self.morgue.append(log)
                message = "{} sent {} to the morgue".format(str(moved_piece), str(move_to_piece))
            else:
                other_player = self.get_other_player(self.player_move)
                if self.is_player_checked(other_player):
                    if self.player_checkmated(other_player):
                        message = "Checkmate {}, {} wins!".format(other_player, self.player_move)
                        self.winner = self.player_move
                    else:
                        message = "Checked {}".format(other_player)
                else:
                    message = "Moved {}".format(str(moved_piece))
            self.next_player_turn()
            self.turn += 1

        else:  # move was not valid
            message = "Invalid move"
        return


def init_game():
    """Initiate key game variables:
        - message
        - chessboard
    """
    global cb
    global message
    cb = ChessBoard(8, 8, DEBUG=True)
    message = "Welcome! White moves first"
    return


def decimate_team(team):
    """Randomly kill ~half the pieces on the board, but never the king."""
    for i in range(len(cb.board)):
        if cb.board[i] != cb.empty_space:
            if cb.board[i].name != "king":
                if not random.randint(0, 1):  # 1/2 to kill
                    cb.board[i] = cb.empty_space
    global message
    message = "Decimated board population"
    return


def ask_play_again():
    """Ask the player(s) if they want to play again. Return False if
    they answer n/no, otherwise return True.
    """
    play_again = input("[Y/n]  ").lower().strip()
    if play_again[0] == "n":
        return False
    return True



init_game()
while True:
    os.system("clear")
    cb.draw()
    print("#  " + message + "  #")

    if cb.winner:
        ask_play_again()
        init_game()

    move = input("Enter a move (ie a3, e7)\n> ").lower().strip()
    if move == "r":
        init_game()
        continue
    elif move == "q":
        quit("Thank you for playing!")
    elif move == "sneeze!":  # easter egg hehe
        cb.next_player_turn()
        decimate_team(cb.player_move)
    else:
        try:
            move = cb.parse_move(move)
        except AttributeError:  # start is an empty spot
            message = "Invalid move"
        else:
            cb.make_move(*move)
