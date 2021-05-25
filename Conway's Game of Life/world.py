import random

import pygame


class World(pygame.surface.Surface):
    def __init__(self, width, height, side_length, initial_spawn_chance):
        super().__init__((width * side_length, height * side_length))
        
        self.side_length = side_length
        
        self.cells_width = width
        self.cells_height = height
        
        self.cells = [1 if initial_spawn_chance > random.random() else 0
                      for _ in range(width * height)]
        self.generation = 0
        return

    def clear(self):
        """Fill the screen with black to erase previous drawings."""
        self.fill((0, 0, 0))
        return

    def update(self):
        """Iterate through cells, drawing each on the World surface and
        checking if the cell should die (if it's alive) or if a new
        cell should be created here.
        """
        x = 0
        y = 0
        new_cells = self.cells.copy()
        for i in range(len(self.cells)):
            if self.cells[i] == 1:
                color = (120, 40, 180)
                pygame.draw.rect(self, color,
                                (x, y, self.side_length, self.side_length)
                                )
            # Dead cells will not be drawn, and will appear
            # as the background color.

            new_state = self.get_new_state(i)
            new_cells[i] = new_state

            x += self.side_length
            if x >= self.get_width():
                x = 0
                y += self.side_length
        self.cells = new_cells
        self.generation += 1
        return

    def get_new_state(self, cell_index):
        """Return the new state of a cell based on the number of living
        adjacent cells.
        """
        live_adjecents = self.get_live_adjacents(cell_index)
        if self.cells[cell_index] == 1:
            if live_adjecents > 1 and live_adjecents < 4:
                return 1
        else:
            # Cells with 2 or 3 neighbors live
            if live_adjecents == 3:
                return 1
        return 0

    def get_live_adjacents(self, cell_index):
        """Return the total number of living adjacent cells."""
        in_leftmost_col = cell_index % self.cells_width == 0
        in_rightmost_col = cell_index % self.cells_width == self.cells_width - 1
        in_topmost_row = cell_index // self.cells_width == 0
        in_botmost_row = cell_index // self.cells_width == self.cells_width - 1
        
        in_leftmost_col = cell_index % self.cells_width == 0
        in_rightmost_col = cell_index % self.cells_width == self.cells_width - 1
        in_topmost_row = cell_index // self.cells_width == 0
        in_botmost_row = cell_index // self.cells_width == self.cells_width - 1
        
        cell_count = 0

        if not in_leftmost_col:
            # Cell is not in the leftmost column, so it has a left
            # adjacent tile
            if self.cells[cell_index - 1] == 1:
                cell_count += 1
        if not in_rightmost_col:
            # Cell is not in the rightmost column, so it has a right
            # adjacent tile
            if self.cells[cell_index + 1] == 1:
                cell_count += 1
        if not in_topmost_row:
            # Cell is not in the top row, so it has a top adjacent tile
            if self.cells[cell_index - self.cells_width] == 1:
                cell_count += 1
        if not in_botmost_row:
            # Cell is not in the bottom row, so it has a bottom adjacent
            # tile
            if self.cells[cell_index + self.cells_width] == 1:
                cell_count += 1
        
        if not in_topmost_row and not in_leftmost_col:
            # Cell is not in the top row or leftmost column, so it has
            # a top left (diagonal) adjacent tile.
            if self.cells[cell_index - self.cells_width - 1] == 1:
                cell_count += 1
        if not in_topmost_row and not in_rightmost_col:
            # Cell is not in the top row or rightmost column, so it has
            # a top left (diagonal) adjacent tile.
            if self.cells[cell_index - self.cells_width + 1] == 1:
                cell_count += 1
        if not in_botmost_row and not in_leftmost_col:
            # Cell is not in the bottom row or leftmost column, so it
            # has a top left (diagonal) adjacent tile.
            if self.cells[cell_index + self.cells_width - 1] == 1:
                cell_count += 1
        if not in_botmost_row and not in_rightmost_col:
            # Cell is not in the bottom row or rightmost column, so it
            # has a top left (diagonal) adjacent tile.
            if self.cells[cell_index + self.cells_width + 1] == 1:
                cell_count += 1

        return cell_count
