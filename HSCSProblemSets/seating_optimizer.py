import random
from math import ceil


def make_rand_row(length):
    """Return a random list of length elements, 1's and 0's to
    represent a seating row with people in it.
    0 = unoccupied seat
    1 = occupied seat
    """
    return [random.choice((0, 0, 0, 1, 1)) % 2 for _ in range(length)]


def count_seats(row, target_seat):
    """Return the number of a single specific seat in a row."""
    total = 0
    for seat in row:
        if seat == target_seat:
            total += 1
    return total


def get_segment(row):
    """Determine the adjacent seats that should all be occupied.
    Return the starting index of this segment of seats, and it's
    length.
    """
    positions = {}
    segment_length = count_seats(row, 1)
    start_i = 0
    while True:
        segment = row[start_i:start_i + segment_length]
        positions.update({start_i: count_seats(segment, 1)})
        start_i += 1
        if start_i + segment_length - 1 == len(row):
            break
    
    best_start_i = None
    high_seats_taken = 0
    for i, seats_taken in positions.items():
        if seats_taken > high_seats_taken:
            high_seats_taken = seats_taken
            best_start_i = i
    return best_start_i, segment_length


def get_left_move(row, start_i, segment_length):
    """Get the best move to make starting from the left side.
    Return a tuple of the index of the person to move and the
    index of where to move it to.
    """
    target_segment = row[start_i:start_i + segment_length]

    if start_i != 0:
        left_segment = row[:start_i]
        # Search for a taken seat to the left of row_segment
        left_i = None  # all left seats might be empty
        for i, seat in enumerate(left_segment):
            if seat == 1:
                left_i = i
                break

        if left_i != None:
            # calculate the best move for the taken seat farthest left
            best_left_move = None
            best_cost = None
            for i, seat in enumerate(target_segment):
                i += start_i
                if seat == 0:
                    cost = i - left_i
                    if best_cost == None or cost < best_cost:
                        best_cost = cost
                        # move from, move to, cost
                        # ie move index 3 to index 10 for a cost of 7
                        best_left_move = (left_i, i)
            return best_left_move
    return


def get_right_move(row, start_i, segment_length):
    """Get the best move to make starting from the right side.
    Return a tuple of the index of the person to move and the
    index of where to move it to.
    """
    target_segment = row[start_i:start_i + segment_length]

    if start_i + segment_length != len(row):
        right_segment = row[start_i + segment_length:]
        # Search for a taken seat to the right of row_segment
        right_i = None  # all right seats might be empty
        for i, _ in enumerate(right_segment):
            # Do a little math to get indices in reverse, but keep
            # them positive
            i = len(row[start_i + segment_length:]) - 1 - i
            i += start_i + segment_length
            if row[i] == 1:
                right_i = i
                break

        if right_i != None:
            # calculate the best move for the taken seat farthest right
            best_right_move = None
            best_cost = None
            for i, seat in enumerate(target_segment):
                i += start_i
                if seat == 0:
                    cost = right_i - i
                    if best_cost == None or cost < best_cost:
                        best_cost = cost
                        # move from, move to
                        # ie move index 3 to index 10
                        best_right_move = (right_i, i)
            return best_right_move
    return


def choose_move(left_move, right_move):
    """Return the best move between the best possible left move
    and best possible right move.
    """
    if left_move == None and right_move == None:
        chosen_move = None
    elif right_move == None:
        chosen_move = left_move
    elif left_move == None:
        chosen_move = right_move
    else:
        left_cost = abs(left_move[0] - left_move[1])
        right_cost = abs(right_move[0] - right_move[1])
        if left_cost < right_cost:
            chosen_move = left_move
        else:
            chosen_move = right_move
    return chosen_move


def print_row(row):
    """Print out the row of seats with index labels above each seat.
    
    Note:
    As long as row doesn't get too long, the printing visuals won't
    get messed up but honestly I don't really remember.
    I say this as nicely as possible: the seat algorithm works,
    just make your own visual display if you want it so bad.
    """
    padding = max([len(str(i)) for i, seat in enumerate(row)]) + 1
    # print the indices of all seats in the row
    for i, _ in enumerate(row):
        if i == len(row) - 1:
            end = "\n"
        else:
            end = ""
        print("{i:<{pad}}".format(i=i, pad=padding), end=end)

    # print the seat row
    for i, seat in enumerate(row):
        if i == len(row) - 1:
            end = "\n"
        else:
            end = ""
        print("{seat:<{pad}}".format(seat=seat, pad=padding), end=end)
    return


ROW1 = [0, 0, 1, 1, 0, 1, 0, 0, 0, 1]
ROW2 = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
# Max length of 99, but just for visual purposes
# Also, consider your screen width
length = 15
row = make_rand_row(length)

start_i, segment_length = get_segment(row)
total_cost = 0
while True:
    print_row(row)

    row_segment = row[start_i:start_i + segment_length]
    left_move = get_left_move(row, start_i, segment_length)
    right_move = get_right_move(row, start_i, segment_length)
    
    move = choose_move(left_move, right_move)
    if move != None:
        # NOTE: Doesn't switch the seats! It just sets one to 0 and
        # the other to 1
        row[move[0]] = 0
        row[move[1]] = 1
        cost = abs(move[0] - move[1])
        total_cost += cost
        print("moved index {} to index {}".format(*move))
        print("added {} to total cost".format(cost))
    else:
        print("The total cost was", total_cost)
        break

    print_row(row)
    print("-" * 20)
