import os


class Solver:
    def __init__(self, disk_num):
        self.disk_num = disk_num
        self.rods = [[d for d in range(disk_num)][::-1], [], []]
        self.moves = 0
        self.target_rod_stack = disk_num % 2 + 1
        self.target_rod_stack_num = 1
        return

    def is_rod_empty(self, rod):
        return not len(self.rods[rod])

    def can_move_disk(self, from_rod, to_rod):
        if self.is_rod_empty(from_rod):
            raise ValueError("from_rod can not be empty")
        try:
            can_move = self.rods[from_rod][-1] < self.rods[to_rod][-1]
            return can_move
        except IndexError:
            return True

    def move_disk(self, from_rod, to_rod):
        disk = self.rods[from_rod].pop(-1)
        self.rods[to_rod].append(disk)
        return

    def solve(self):
        print(self.rods, end="  -->  ")
        self.move_disk(0, self.target_rod_stack)

        if len(self.rods[self.target_rod_stack]) == self.target_rod_stack_num:
            self.target_rod_stack = self.target_rod_stack % 2 + 1
        print(self.rods)
        if len(self.rods[0]) == 0 and len(self.rods[1]) == 0:
            print("done!")
            return
        input()
        return self.solve()


class Table:
    def __init__(self, disk_num=3):
        # best moves = 2 ** disk_num - 1
        self.disk_num = disk_num
        self.rods = (list(range(0, disk_num)[::-1]), [], [])
        return

    def __getitem__(self, i):
        """return the top disk from the rod"""
        if len(self.rods[i]) == 0:
            return None
        else:
            return self.rods[i][-1]

    @property
    def is_complete(self):
        if len(self.rods[0]) == 0 and len(self.rods[1]) == 0:
            return True
        return False

    @property
    def highest_rod(self):
        return max([len(rod) for rod in self.rods])

    def move_disk(self, start_rod, end_rod):
        try:
            if self.rods[start_rod][-1] < self.rods[end_rod][-1]:
                self.__move_disk(start_rod, end_rod)
            else:  # disk is bigger than the one it would land on
                raise ValueError("Invalid move, can not put {} on {}".format(
                                                                             self[start_rod],
                                                                             self[end_rod]
                                                                             ))
        except IndexError:
            self.__move_disk(start_rod, end_rod)
        return

    def __move_disk(self, start_rod, end_rod):
        disk = self.rods[start_rod].pop(-1)
        self.rods[end_rod].append(disk)
        return

    def show_rods(self):
        pad = len(str(self.disk_num))  # Number of characters each
                                         # disk should be.
        for h in range(self.disk_num):
            h = self.disk_num - h - 1
            try:
                c1 = self.rods[0][h]
            except IndexError:
                c1 = " "
            try:
                c2 = self.rods[1][h]
            except IndexError:
                c2 = " "
            try:
                c3 = self.rods[2][h]
            except IndexError:
                c3 = " "
            row = "| {:{pad}}   {:{pad}}   {:<{pad}} |".format(c1, c2, c3,
                                                               pad=pad)
            print(row)
        print("-" * len(row))
        return


def clear():
    os.system("clear")
    return


clear()
table = Table()
solver = Solver(5)
solver.solve()
