import pygame

from world import World


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Conway's Game of Life")
        return

    def clear(self):
        self.win.fill((0, 0, 0))
        return

    def blit(self, surf, pos):
        self.win.blit(surf, pos)
        return

    @staticmethod
    def update_screen():
        pygame.display.update()
        return


pygame.init()

scale = 3
side_length = 2 ** (scale - 1)
cells_width = 512 // side_length
cells_height = 512 // side_length
initial_spawn_chance = 0.5
world = World(cells_width, cells_height, side_length,
              initial_spawn_chance)

display_width = cells_width * side_length
display_height = cells_height * side_length
display = Display(display_width, display_height)
run = True

while run:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                world = World(cells_width, cells_height, side_length,
                              initial_spawn_chance)

    world.clear()
    world.update()

    display.clear()
    display.blit(world, (0,0))
    display.update_screen()

    print(world.generation)

pygame.quit()