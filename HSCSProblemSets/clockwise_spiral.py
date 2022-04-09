class Spiral:
    def __init__(self, start, stop, step=1, mode="pretty"):
        """Creates a list of numbers from start, stop, omitting stop.

        start -- an int
        stop -- an int
        step -- an int
        mode -- string: "pretty", "point", "raw"
                this determines what the spiral
                will look like graphically.
        
        "pretty" mode will separate all the column with a pipe (|) and
        print numbers in their respective position.

        "point" mode will separate all the column with whitespace and
        print an arrow pointing to the position that came right after
        it.

        "raw" mode will separate all the column with whitespace and
        print numbers in their respective position.
        """
        self.__nums = range(start, stop, step)
        self.__mode = mode
        # Every spot must be the same length
        # Stop is omitted so stop - 1 is the longest number
        side_length = self.__calc_length()
        len_number_spot = len(str(stop-1))
        self.__spiral = self.__fill(side_length, len_number_spot)
        return

    def __calc_length(self, length=1):
        """Calculate and return the length (same as height) of the
        spiral which nums will form.
        """
        # Either:
        # Numbers will make a perfect square with no uneven spaces.
        # or
        # Numbers can not make a larger square, but don't fit perfectly
        # into this area.
        if len(self.__nums) - length ** 2 <= 0:
            return length
        # More numbers than area in the square, loop again
        else:
            return self.__calc_length(length + 2)

    def __generate_template(self, side_length):
        """Return a list filled with length number of lists, which are
        filled with length number of strings. These strings act as
        placeholders for the numbers which will be filled later.
        """
        row_template = [0 for i in range(side_length)]
        empty_grid = [row_template.copy() for i in range(side_length)]
        return empty_grid

    def __fill(self, side_length, len_number_spot):
        """Take an empty grid and nums, then populate the empty grid with
        nums in a clockwise spiral expanding from the center.
        """
        template = self.__generate_template(side_length)

        layer = 1
        layer_width = 1
        show_num = 1

        # Creates a spot of uniform length for each number
        create_number_spot = lambda content: content + " " * (len_number_spot - len(content))

        # Starting position of num:
        position_row = side_length // 2  # like the y coord in a coord-plane
        position_col = side_length // 2  # like the x coord in a coord-plane
        for i in range(side_length ** 2):
            if show_num == 1:
                layer += 1
                layer_width += 2
                move_direction = ">"
            # This is the spot right after the top right spot
            elif (show_num - 1) ** 0.5 % 2 == 1:
                move_direction = "v"
            # This is the top right spot
            elif show_num ** 0.5 % 2 == 1:
                layer += 1
                layer_width += 2
            # This is the top left spot
            elif (show_num + layer_width - 1) ** 0.5 % 2 == 1:
                move_direction = ">"
            # This is the bottom left spot
            elif (show_num + (layer_width - 1) * 2) ** 0.5 % 2 == 1:
                move_direction = "^"
            # This is the bottom right spot
            elif (show_num + (layer_width - 1) * 3) ** 0.5 % 2 == 1:
                move_direction = "<"

            # determine what goes in the template spot
            if self.__mode == "pretty" or self.__mode == "raw":
                # numbers will fill the template
                try:
                    content = str(self.__nums[i])
                except IndexError:
                    content = "-" * len_number_spot  # all numbers have been placed
                formated_content = create_number_spot(content)
            elif self.__mode == "point":
                # directional arrows will fill the template
                if show_num == 1:
                    content = "≥"  # makes the start point special
                else:
                    content = move_direction
                formated_content = content

            template[position_row][position_col] = formated_content

            if move_direction == ">":
                position_col += 1
            elif move_direction == "v":
                position_row += 1
            elif move_direction == "<":
                position_col -= 1
            elif move_direction == "^":
                position_row -= 1

            show_num += 1
        return template  # is now filled from nums

    def __repr__(self):
        """Return an ascii representation of self.__spiral"""
        output = "{sep} " + " {sep}\n\n{sep} ".join([" {sep} ".join(row) for row in self.__spiral]) + " {sep}"
        if self.__mode == "pretty":
            sep = "|"
        elif self.__mode == "point" or self.__mode == "raw":
            sep = ""
        output = output.format(sep=sep)
        return output


if __name__ == "__main__":
    spiral = Spiral(0, 10, step=2, mode="raw")
    print(spiral)
