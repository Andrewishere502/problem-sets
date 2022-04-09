"""
Creator: Andrew Berntson
Date: September 19 2020

This file holds all the pieces for chess. You can make your own piece
fairly easily by adding a new piece object to this file (make sure you
inherit the Piece object though!).
"""


class Piece:
    """The general template for a piece, with basic functions
    that can be implemented to help determine if a move is valid.
    """
    def __init__(self, name, icon, facing, color):
        self.name = name
        self.icon = icon
        self.facing = 1 if facing == "north" else -1
        self.color = color
        self.location = None
        return

    def __str__(self):
        return self.color[0] + self.icon

    def set_location(self, location):
        self.location = location
        return

    def move(self, location):
        self.location = location
        return

    @staticmethod
    def past_top_row(loc):
        return loc < 0

    @staticmethod
    def past_bot_row(board, loc):
        try:
            board.board[loc]
        except IndexError:
            return True
        return False

    def past_left_col(self, board, loc):
        return loc % board.cols > self.location % board.cols

    def past_right_col(self, board, loc):
        return loc % board.cols < self.location % board.cols

    def loc_same_team(self, board, loc):
        try:
            return self.color == board.board[loc].color
        except AttributeError:  # empty space
            return False
        except IndexError:  # loc is outside of board
            return False  # let past_bot_row do it's thing

    def loc_empty(self, board, loc):
        try:
            return board.board[loc] == board.empty_space
        except IndexError:
            return False


class Pawn(Piece):
    def __init__(self, facing, color):
        name = "pawn"
        icon = "p"
        super().__init__(name, icon, facing, color)
        self.first_move = True
        return

    def move(self, location):
        super().move(location)
        if self.first_move == True:
            self.first_move = False
        return

    def valid_moves(self, board):
        moves = []

        loc = self.location - board.cols * self.facing * 2  # forward 2
        if (not self.past_bot_row(board, loc)  # prevent line bellow
                                               # from raising error
            and board.board[loc] == board.empty_space
            and self.first_move):
            moves.append(loc)

        loc = self.location - board.cols * self.facing  # forward
        if (not self.past_bot_row(board, loc)
            and not self.past_top_row(loc)
            and board.board[loc] == board.empty_space):
            moves.append(loc)

        loc = self.location - board.cols * self.facing - 1  # forward left
        if (not self.past_bot_row(board, loc)
            and not self.past_top_row(loc)
            and not self.loc_empty(board, loc)
            and not self.loc_same_team(board, loc)):
            moves.append(loc)

        loc = self.location - board.cols * self.facing + 1  # forward right
        if (not self.past_bot_row(board, loc)
            and not self.past_top_row(loc)
            and not self.loc_empty(board, loc)
            and not self.loc_same_team(board, loc)):
            moves.append(loc)
        return moves


class King(Piece):
    def __init__(self, facing, color):
        name = "king"
        icon = "K"
        super().__init__(name, icon, facing, color)
        return

    def valid_moves(self, board):
        moves = []

        loc = self.location - board.cols  # forward
        if (not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.loc_same_team(board, loc)):
            moves.append(loc)

        loc = self.location + board.cols  # backwards
        if (not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.loc_same_team(board, loc)):
            moves.append(loc)

        loc = self.location - 1  # left
        if (not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.loc_same_team(board, loc)
            and not self.past_left_col(board, loc)):
            moves.append(loc)

        loc = self.location + 1  # right
        if (not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.loc_same_team(board, loc)
            and not self.past_right_col(board, loc)):
            moves.append(loc)

        loc = self.location - board.cols - 1  # forward left
        if (not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.loc_same_team(board, loc)
            and not self.past_left_col(board, loc)):
            moves.append(loc)

        loc = self.location - board.cols + 1  # forward right
        if (not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.loc_same_team(board, loc)
            and not self.past_right_col(board, loc)):
            moves.append(loc)
        
        loc = self.location + board.cols - 1  # backwards left
        if (not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.loc_same_team(board, loc)
            and not self.past_left_col(board, loc)):
            moves.append(loc)

        loc = self.location + board.cols + 1  # backwards right
        if (not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.loc_same_team(board, loc)
            and not self.past_right_col(board, loc)):
            moves.append(loc)
        return moves


class Knight(Piece):
    def __init__(self, facing, color):
        name = "knight"
        icon = "H"
        super().__init__(name, icon, facing, color)
        return

    def is_forward_clear(self, board, loc_lambda, max_i):
        for i in range(1, max_i + 1):
            loc = loc_lambda(i)
            if (self.past_top_row(loc)
                or self.past_bot_row(board, loc)):
                # Forward is not clear so stop and return False
                return False
        return True

    def valid_moves(self, board):
        moves = []

        loc = self.location - board.cols * 2 - 1
        if (not self.loc_same_team(board, loc)
            and not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.past_left_col(board, loc)):  # forward left (L)
            moves.append(loc)
        
        loc = self.location - board.cols * 2 + 1
        if (not self.loc_same_team(board, loc)
            and not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.past_right_col(board, loc)):  # forward right (L)
            moves.append(loc)

        loc = self.location + board.cols * 2 - 1
        if (not self.loc_same_team(board, loc)
            and not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.past_left_col(board, loc)):  # backwards left (L)
            moves.append(loc)
        
        loc = self.location + board.cols * 2 + 1
        if (not self.loc_same_team(board, loc)
            and not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.past_right_col(board, loc)):  # backwards right (L)
            moves.append(loc)

        loc = self.location - 2 - board.cols
        if (not self.loc_same_team(board, loc)
            and not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.past_left_col(board, loc)):  # left up (L)
            moves.append(loc)

        loc = self.location + 2 - board.cols
        if (not self.loc_same_team(board, loc)
            and not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.past_right_col(board, loc)):  # right up (L)
            moves.append(loc)

        loc = self.location - 2 + board.cols
        if (not self.loc_same_team(board, loc)
            and not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.past_left_col(board, loc)):  # left down (L)
            moves.append(loc)

        loc = self.location + 2 + board.cols
        if (not self.loc_same_team(board, loc)
            and not self.past_top_row(loc)
            and not self.past_bot_row(board, loc)
            and not self.past_right_col(board, loc)):  # right down (L)
            moves.append(loc)
        return moves


class Tower(Piece):
    def __init__(self, facing, color):
        name = "tower"
        icon = "T"
        super().__init__(name, icon, facing, color)
        return

    def valid_moves(self, board):
        moves = []
        piece_row = self.location // board.cols
        piece_col = self.location % board.cols

        # NOTE: all valid moves will be calculated w/o taking into
        # account the direction the piece is facing
        
        if piece_row != 0:
            for i in range(1, piece_row + 1):  # move north
                loc = self.location - i * board.cols
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_row != board.rows:  # piece not in last row
            for i in range(1, (board.rows - piece_row)):  # move south
                loc = self.location + i * board.cols
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_col != 0:
            for i in range(1, piece_col + 1):  # move west
                loc = self.location - i
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_col != board.cols:  # piece not in last col
            for i in range(1, (board.cols - piece_col)):  # move east
                loc = self.location + i
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break
        return moves


class Bishop(Piece):
    def __init__(self, facing, color):
        name = "bishop"
        icon = "B"
        super().__init__(name, icon, facing, color)
        return

    def valid_moves(self, board):
        moves = []
        piece_row = self.location // board.cols
        piece_col = self.location % board.cols

        # NOTE: all valid moves will be calculated w/o taking into
        # account the direction the piece is facing
        
        if piece_row != 0:
            for i in range(1, piece_col + 1):  # move northwest
                loc = self.location - i * (board.cols + 1)
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_row != 0:
            for i in range(1, board.cols - piece_col):  # move northeast
                loc = self.location - i * (board.cols - 1)
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_row != board.rows:
            for i in range(1, piece_col + 1):  # move southwest
                loc = self.location + i * (board.cols - 1)
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_row != board.rows:
            for i in range(1, board.cols - piece_col):  # move southeast
                loc = self.location + i * (board.cols + 1)
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break
        return moves


class Queen(Piece):
    def __init__(self, facing, color):
        name = "queen"
        icon = "Q"
        super().__init__(name, icon, facing, color)
        return

    def valid_moves(self, board):
        moves = []
        piece_row = self.location // board.cols
        piece_col = self.location % board.cols

        # NOTE: all valid moves will be calculated w/o taking into
        # account the direction the piece is facing

        ##
        # Move vertically and horizontally
        ##
        if piece_row != 0:
            for i in range(1, piece_row + 1):  # move north
                loc = self.location - i * board.cols
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_row != board.rows:  # piece not in last row
            for i in range(1, (board.rows - piece_row)):  # move south
                loc = self.location + i * board.cols
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_col != 0:
            for i in range(1, piece_col + 1):  # move west
                loc = self.location - i
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_col != board.cols:  # piece not in last col
            for i in range(1, (board.cols - piece_col)):  # move east
                loc = self.location + i
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        ##
        # Move diagonally
        ##
        if piece_row != 0:
            for i in range(1, piece_col + 1):  # move northwest
                loc = self.location - i * (board.cols + 1)
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_row != 0:
            for i in range(1, board.cols - piece_col):  # move northeast
                loc = self.location - i * (board.cols - 1)
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_row != board.rows:
            for i in range(1, piece_col + 1):  # move southwest
                loc = self.location + i * (board.cols - 1)
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break

        if piece_row != board.rows:
            for i in range(1, board.cols - piece_col):  # move southeast
                loc = self.location + i * (board.cols + 1)
                if self.loc_same_team(board, loc):
                    break
                moves.append(loc)
                if (not self.loc_empty(board, loc)
                    and not self.loc_same_team(board, loc)):
                    break
        return moves


if __name__ == "__main__":
    print("~This is not the file you are looking for~\nDid you mean to run chess.py?")