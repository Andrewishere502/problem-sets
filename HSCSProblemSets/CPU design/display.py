import pygame
from math import sin, cos, acos, pi, sqrt

from cpu import *  # sorry, there's a lot to import
from compiler import Compiler


class Arrow:
    """An arrow that can point at any angle, in a single direction."""
    def __init__(self, start, end, color, width, direction):
        self.start = start
        self.end = end
        x_diff = end[0] - start[0]
        y_diff = end[1] - start[1]
        length = round(sqrt((x_diff)**2 + (y_diff)**2))
        self.length = length
        angle = acos(x_diff / length)
        if y_diff > 0:
            angle = 2 * pi - angle
        self.angle = angle
        self.color = color
        self.width = width
        self.direction = direction
        return

    def draw_right_arrow(self, win):
        """Draw the right arrow head."""
        top_point_line_end_x = round(self.end[0] + 20 * cos(self.angle + 3 * pi/4))
        top_point_line_end_y = round(self.end[1] - 20 * sin(self.angle + 3 * pi/4))
        pygame.draw.line(win, self.color, self.end,
                        (top_point_line_end_x, top_point_line_end_y), self.width)
        
        top_point_line_end_x = round(self.end[0] + 20 * cos(self.angle - 3 * pi/4))
        top_point_line_end_y = round(self.end[1] - 20 * sin(self.angle - 3 * pi/4))
        pygame.draw.line(win, self.color, self.end,
                         (top_point_line_end_x, top_point_line_end_y), self.width)
        return

    def draw_left_arrow(self, win):
        """Draw the left arrow head."""
        top_point_line_end_x = round(self.start[0] - 20 * cos(self.angle + 3 * pi/4))
        top_point_line_end_y = round(self.start[1] + 20 * sin(self.angle + 3 * pi/4))
        pygame.draw.line(win, self.color, self.start,
                        (top_point_line_end_x, top_point_line_end_y), self.width)
        
        top_point_line_end_x = round(self.start[0] - 20 * cos(self.angle - 3 * pi/4))
        top_point_line_end_y = round(self.start[1] + 20 * sin(self.angle - 3 * pi/4))
        pygame.draw.line(win, self.color, self.start,
                         (top_point_line_end_x, top_point_line_end_y), self.width)
        return

    def draw(self, win):
        """Draw the arrow on the pygame window surface."""
        pygame.draw.line(win, self.color, self.start, self.end, self.width)

        if self.direction == "right":
            self.draw_right_arrow(win)
        elif self.direction == "left":
            self.draw_left_arrow(win)
        else:
            self.draw_right_arrow(win)
            self.draw_left_arrow(win)
        return


class ThickArrow:
    """A base thick arrow object. Use to represent a bus."""
    def __init__(self, start, width, height, direction, label, ):
        if direction != "right":
            start = start[0] + 20, start[1]
        self.start = start
        compensation = 40 if direction == "both" else 20
        self.width = width - compensation  # - width of arrowhead(s)
        self.height = height
        self.direction = direction
        self.font_small = pygame.font.SysFont("ariel", 20)
        self.font_big = pygame.font.SysFont("ariel", 30)
        self.label = label
        return

    def draw_right(self, win, color):
        """Draw the arrowhead pointing right."""
        point1 = (self.start[0] + self.width,
                  self.start[1] - 10)
        point2 = (self.start[0] + self.width,
                  self.start[1] + self.height + 10)
        point3 = (self.start[0] + self.width + 20,
                  self.start[1] + self.height / 2)
        pygame.draw.polygon(win, color, (point1, point2, point3))
        return

    def draw_left(self, win, color):
        """Draw the arrowhead pointing left."""
        point1 = (self.start[0],
                  self.start[1] - 10)
        point2 = (self.start[0],
                  self.start[1] + self.height + 10)
        point3 = (self.start[0] - 20,
                  self.start[1] + self.height / 2)
        pygame.draw.polygon(win, color, (point1, point2, point3))
        return

    def label_obj(self):
        """Return the label text as a font render object."""
        return self.font_small.render(self.label, True, (0, 0, 0))

    def value_obj(self, value):
        """Return the value as a font render object."""
        return self.font_big.render(value, True, (0, 0, 0))

    def draw(self, win, value):
        """Draw the arrow."""
        color = (168, 142, 136)
        pygame.draw.rect(win, color, (*self.start, self.width, self.height))

        if self.direction == "right":
            self.draw_right(win, color)
        elif self.direction == "left":
            self.draw_left(win, color)
        elif self.direction == "both":
            self.draw_right(win, color)
            self.draw_left(win, color)

        win.blit(self.label_obj(), self.start)
        win.blit(self.value_obj(value), (self.start[0] + 10, self.start[1] + self.height // 2))
        return


class Register:
    """A base register object."""
    def __init__(self, start, width, height, label):
        self.start = start
        self.width = width
        self.height = height
        self.font_small = pygame.font.SysFont("ariel", 20)
        self.font_big = pygame.font.SysFont("ariel", 30)
        self.label = label
        return

    def label_obj(self):
        """Return the label text as a font render object."""
        return self.font_small.render(self.label, True, (0, 0, 0))

    def value_obj(self, value):
        """Return the value as a font render object."""
        return self.font_big.render(value, True, (0, 0, 0))

    def draw(self, win, value):
        """Draw the register."""
        color = (255, 255, 255)
        pygame.draw.rect(win, color, (*self.start, self.width, self.height))
        win.blit(self.label_obj(), self.start)
        win.blit(self.value_obj(value), (self.start[0] + 5, self.start[1] + self.height // 2))
        return


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((width, height))
        self.font_small = pygame.font.SysFont("ariel", 20)
        self.font_big = pygame.font.SysFont("ariel", 30)

        pygame.display.set_caption("CPU Sim")
        return

    def clear(self):
        """Fill the window with black."""
        self.win.fill((0, 0, 0))
        return

    @staticmethod
    def update():
        """Update pygame display."""
        pygame.display.update()
        return

    def show(self, cpu):
        """Show all the components of the cpu simulation."""
        # It might be weird that these methods are separated because
        # the ram is a component of cpu (and thus is being passed in
        # for show_cpu too), but the compartimentalization of these
        # methods is logical.
        self.show_cpu(cpu)
        self.show_ram(cpu)
        self.show_buses(cpu)

        self.show_UI(cpu)  # display the lower UI
        return
    
    def show_UI(self, cpu):
        """Display the UI, things that aren't necessary for
        visualizing the cpu.
        """
        # display run status
        if cpu.run:
            color = 30, 179, 7  # green
        else:
            color = 85, 87, 83  # grey
        on_blit = self.font_big.render("On/Off: ", True, (255, 255, 255))
        self.win.blit(on_blit, (10, 520))
        pygame.draw.circle(self.win, color, (100, 530), 10)
        

        # display cycle number
        cycles_blit = self.font_big.render("Cylces: " + str(cpu.cycle_num), True, (255, 255, 255))
        self.win.blit(cycles_blit, (150, 520))
        return

    def show_decode_unit(self, cpu):
        """Display the decode unit, along with each opcode and it's
        meaning.
        """
        pygame.draw.rect(self.win, (166, 164, 129), (20, 110, 180, 400))
        label = self.font_big.render("Decode unit", True, (0, 0, 0))
        self.win.blit(label, (20, 110))
        y = 150
        for key, function in cpu.decode_unit.opcodes.items():
            key = self.font_small.render(key, True, (0, 0, 0))
            self.win.blit(key, (30, y))
            function = self.font_small.render(function, True, (0, 0, 0))
            self.win.blit(function, (80, y))
            y += 30
        return

    def show_cpu(self, cpu):
        """Display the cpu die with all it's registers."""
        pygame.draw.rect(self.win, (136, 168, 140), (10, 10, 500, 500))
        cpu_blit = self.font_big.render("CPU Die", True, (0, 0, 0))
        self.win.blit(cpu_blit, (20, 20))

        registers = [
            Register((110, 20), 120, 50, "Program counter"),
            Register((260, 20), 180, 50, "Memory address register"),
            Register((260, 100), 220, 50, "Accumulator"),
            Register((260, 300), 200, 50, "Memory data register"),
            Register((260, 400), 200, 50, "Current instruction register")
            ]
        for register in registers:
            value = str(getattr(cpu, register.label.lower().replace(" ", "_")))
            register.draw(self.win, value)


        pygame.draw.rect(self.win, (33, 89, 219), (260, 175, 120, 50))  # draw alu
        alu_blit = self.font_big.render("ALU", True, (255, 255, 255))
        self.win.blit(alu_blit, (260, 175))

        self.show_decode_unit(cpu)

        arrows = [
            Arrow((100, 110), (110, 65), (44, 18, 99), 4, "right"),
            Arrow((190, 200), (260, 200), (44, 18, 99), 4, "right"),
            Arrow((200, 110), (260, 70), (44, 18, 99), 4, "right"),
            Arrow((230, 35), (260, 35), (44, 18, 99), 4, "right"),
            Arrow((260, 425), (190, 425), (44, 18, 99), 4, "right"),
            Arrow((300, 300), (300, 225), (44, 18, 99), 4, "right"),
            Arrow((340, 175), (340, 150), (44, 18, 99), 4, "both"),
            Arrow((360, 350), (360, 400), (44, 18, 99), 4, "right"),
            Arrow((410, 300), (410, 150), (44, 18, 99), 4, "both"),
            Arrow((440, 35), (520, 35), (44, 18, 99), 4, "right"),
            Arrow((460, 320), (520, 320), (44, 18, 99), 4, "both")
            ]
        for arrow in arrows:
            arrow.draw(self.win)
        return

    def show_ram(self, cpu):
        """Display the stick of ram, including each address and it's
        corresponding data.
        """
        pygame.draw.rect(self.win, (136, 146, 168), (690, 10, 200, 500))
        label = self.font_big.render("RAM", True, (0, 0, 0))
        self.win.blit(label, (690, 10))
        y = 50
        for address, data in cpu.ram.addresses.items():
            if address == cpu.memory_address_register:
                pygame.draw.rect(self.win, (219, 210, 33), (695, y - 5, 190, 25))
            address = self.font_small.render(str(address), True, (0, 0, 0))
            self.win.blit(address, (700, y))
            data = self.font_small.render(data, True, (0, 0, 0))
            self.win.blit(data, (750, y))
            y += 25
        return

    def show_buses(self, cpu):
        """Display all the address buses."""
        buses = [
            ThickArrow((520, 30), 160, 30, "right", "Address bus"),
            ThickArrow((520, 300), 160, 30, "both", "Data bus"),
            ThickArrow((520, 455), 160, 30, "both", "Control bus")
            ]
        for bus in buses:
            value = str(getattr(cpu, bus.label.lower().replace(" ", "_")))
            bus.draw(self.win, value)
        return


def next_step(step):
    """Increment the step number, with a max of 9."""
    step += 1
    if step > 9:
        step = 1
    return step


pygame.init()

program_name = "add.txt"  # the name of the program file
ram = RAM(16)
compiler = Compiler()
program = compiler.parse(program_name)
load_ram(ram, program)
cpu = CPU(ram)

display = Display(900, 550)  # required dimensions are 900 and 520

step = 1  # which step of the cycle the cpu is on
args = None  # args to be passed to the next step
delay = 50  # time to complete one step
pause = False  # pause simulation without stopping cpu

run = True
while run:
    pygame.time.delay(delay)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                # press s to start the cpu
                cpu.start()
            elif event.key == pygame.K_r:
                # press r to reset the cpu and ram
                program = compiler.parse(program_name)
                ram = RAM(16)
                load_ram(ram, program)
                cpu.connect_ram(ram)
                cpu.reset()
            elif event.key == pygame.K_p:
                # press p to pause/unpause the simulation
                if pause:
                    pause = False
                else:
                    pause = True
            elif event.key == pygame.K_EQUALS:
                # increase the delay up to 100, increments of 10
                if delay == 1:
                    delay += 9
                elif delay < 100:
                    delay += 10
            elif event.key == pygame.K_MINUS:
                # decrease the delay down to 1, increments of 10
                if delay == 10:
                    delay -= 9
                elif delay > 1:
                    delay -= 10


    display.clear()
    display.show(cpu)
    if cpu.run and not pause:
        step_method = getattr(cpu, "step{}".format(step))
        if args != None:
            if isinstance(args, str):
                args = step_method(args)
            else:
                args = step_method(*args)
        else:
            args = step_method()
        step = next_step(step)
    display.update()
pygame.quit()