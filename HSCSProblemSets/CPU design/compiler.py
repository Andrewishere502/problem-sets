from cpu import CPU, load_ram
from ram import RAM


class Compiler:
    def __init__(self):
        # opcodes compatable with the decode_unit in this folder
        self.opcodes = {
            "0000": "end",
            "0001": "add",
            "0010": "subtract",
            "0011": "store",
            "0100": "load",
            "0101": "branch",  # branch always
            "0110": "branchEqZero",  # branch if acc == 0
            "0111": "branchGtEqZero",  # branch if acc >= 0
            "1000": "branchGtZero",  # branch if acc > 0
            "1001": "branchLtEqZero",  # branch if acc <= 0
            "1010": "IO",  # input = opperand 0001
                           # input = opperand 0010
                           # I have no idea what these are for
            "1011": "print"
            }
        return

    def make_4bit(self, num):
        """Return a decimal number in 4-bit binary."""
        bin_num = bin(num)[2:]
        bit4 = "0" * (4 - len(str(bin_num))) + bin_num
        return bit4

    def make_8bit(self, num):
        """Return a decimal number in 8-bit binary."""
        bin_num = bin(num)[2:]
        bit8 = "0" * (8 - len(str(bin_num))) + bin_num
        return bit8

    def convert_set_data(self, convert_me):
        """Return a tuple with the address (int) and the value at that
        address (8-bit number).
        """
        return int(convert_me[1]), self.make_8bit(int(convert_me[2]))

    def convert_opcode(self, convert_me):
        """Return a 4-bit opcode corresponding to the opcode word."""
        find_opcode = {value: key for key, value in self.opcodes.items()}
        try:
            opcode = find_opcode[convert_me]
        except KeyError:
            raise ValueError("opcode for '{}' not found".format(convert_me))
        return opcode

    def convert_operand(self, convert_me):
        """Return a 4-bit number converted from a string"""
        return self.make_4bit(int(convert_me))

    def parse(self, filename):
        """Parse filename.txt, translate the lines into 8-bit
        instructions, return these instructions.
        """
        with open("programs/" + filename, "r") as file:
            lines = file.readlines()

        for i in range(len(lines)):
            if i != len(lines) - 1:
                lines[i] = lines[i][:-1]  # remove \n
            lines[i] = lines[i].split()

        instructions = []
        for i in range(len(lines)):
            line = lines[i]
            if len(line) == 2:
                # converts the opcode
                line[0] = self.convert_opcode(line[0])
                # converts the operand
                line[1] = self.convert_operand(line[1])
                instructions.append((i, "".join(line)))
            elif len(line) == 1:
                instructions.append((i, "00000000"))  # add end instruction
            # Allows explicit asignment of addresses,
            # for non-instructions.
            elif line[0] == "set":
                line = self.convert_set_data(line)
                instructions.append(line)
        return instructions


if __name__ == "__main__":
    compiler = Compiler()
    program = compiler.parse("divide.txt")
    ram = RAM(16)
    load_ram(ram, program)
    cpu = CPU(ram)
    cpu.excecute()  # execute full instructions
