from alu import ALU
from ram import RAM
from decode_unit import DecodeUnit


class CPU:
    def __init__(self, ram):
        self.alu = ALU
        self.decode_unit = DecodeUnit()
        self.connect_ram(ram)

        self.reset()
        return

    def connect_ram(self, ram):
        """Set the ram for the cpu."""
        self.ram = ram  # isn't really on the cpu
        return

    def reset(self):
        """Reset all the cpu's registers, buses, etc."""
        self.program_counter = 0
        self.memory_address_register = 0
        self.memory_data_register = 0
        self.current_instruction_register = 0
        self.accumulator = 0
        self.address_bus = 0  # this is not on the cpu technically
        self.data_bus = 0  # neither is this
        self.control_bus = "read"  # neither is this

        self.display = 0
        self.run = False
        self.cycle_num = 0
        return

    def start(self):
        """Start the computer."""
        self.run = True
        return

    def halt(self):
        """Halt the cpu."""
        self.run = False
        return

    def make_bin(self, num):
        """Return a decimal number in 8-bit binary."""
        bin_num = bin(num)[2:]
        bit8 = "0" * (8 - len(str(bin_num))) + bin_num
        return bit8

    def step1(self):
        """Set the memory address register to the data in the program
        counter register.
        """
        # set memory address register to program counter
        self.memory_address_register = self.program_counter
        return

    def step2(self):
        """Set the address bus to the data in the memory address
        register.
        """
        self.address_bus = self.memory_address_register
        return

    def step3(self):
        """Fetch the instruction (from the address in the address bus)
        from primary memory. Return this instruction.
        """
        instruction = self.ram.get_address(self.address_bus)
        return instruction

    def step4(self, instruction):
        """Save the instruction to data bus."""
        self.data_bus = instruction
        return

    def step5(self):
        """Store data bus value into memory data register."""
        self.memory_data_register = self.data_bus
        return

    def step6(self):
        """Set current instruction register to memory data register."""
        self.current_instruction_register = self.memory_data_register
        return

    def step7(self):
        """Increment program counter."""
        self.program_counter += 1
        return

    def step8(self):
        """Return the instruction decoded into an opcode and operand."""
        opcode, operand = self.decode_unit.decode(self.current_instruction_register)
        # print(opcode, operand)
        return opcode, operand

    def step9(self, opcode, operand):
        """Interpret the decoded instruction (opcode, operand) and do
        the appropriate job.
        """
        # do something with the decoded instruction
        self.cycle_num += 1
        if opcode == "end":
            self.halt()
        else:
            if opcode == "add":
                # operand is an address
                num1 = self.accumulator
                address = int(operand, base=2)
                self.memory_data_register = self.ram.get_address(address)
                num2 = int(self.memory_data_register, base=2)
                self.accumulator = self.alu(num1, num2)
            elif opcode == "subtract":
                # operand is an address
                num1 = self.accumulator
                address = int(operand, base=2)
                self.memory_data_register = self.ram.get_address(address)
                num2 = int(self.memory_data_register, base=2)
                self.accumulator = self.alu(num1, num2, sub=True)
            elif opcode == "store":
                self.control_bus = "write"
                # operand is an address
                address = int(operand, base=2)
                data = self.make_bin(self.accumulator)
                self.ram.store_new(address, data)
            elif opcode == "load":
                self.control_bus = "read"
                # operand is an address
                address = int(operand, base=2)
                self.memory_data_register = self.ram.get_address(address)
                self.accumulator = int(self.memory_data_register, base=2)
            elif opcode == "branch":
                # operand is an address
                address = int(operand, base=2)
                self.program_counter = address
            elif opcode == "branchEqZero":
                if self.accumulator == 0:
                    # operand is an address
                    address = int(operand, base=2)
                    self.program_counter = address
            elif opcode == "branchGtEqZero":
                if self.accumulator >= 0:
                    # operand is an address
                    address = int(operand, base=2)
                    self.program_counter = address
            elif opcode == "branchGtZero":
                if self.accumulator > 0:
                    # operand is an address
                    address = int(operand, base=2)
                    self.program_counter = address
            elif opcode == "IO":
                pass  # I don't know what this is supposed to do
            elif opcode == "print":
                # operand is an address
                address = int(operand, base=2)
                self.memory_data_register = self.ram.get_address(address)
                print(int(self.memory_data_register, base=2))
        return

    def do_cycle(self):
        """Do a full cycle of the cpu."""
        # step 1:
        self.step1()

        # step 2:
        self.step2()

        # step 3:
        instruction = self.step3()

        # step 4:
        self.step4(instruction)

        # step 5:
        self.step5()

        # step 6:
        self.step6()

        # step 7:
        self.step7()

        # step 8:
        opcode, operand = self.step8()

        # step 9:
        self.step9(opcode, operand)
        return

    def excecute(self):
        """Run the loaded program."""
        self.start()
        while self.run:
            self.do_cycle()
        return


def load_ram(ram, instructions):
    """Load a set of instructions into RAM."""
    for address, data in instructions:
        ram.store_new(address, data)
    return


add_instructions = [  # add two numbers
    # data:
    (15, "01010101"),  # value 85
    (14, "00011011"),  # value 27
    # instructions:
    (0, "01001111"),  # load address 15 to accumulator
    (1, "00011110"),  # add address 14 and accumulator
    (2, "00111101"),  # store accumulator to address 13
    (3, "10111101"),  # print address 13
    (4, "00000000")   # end
    ]

multipy_instructions = [  # multiply two numbers
    # data:
    (15, "00001011"),  # 11
    (14, "00000111"),  # 7
    (13, "00000001"),  # 1
    (12, "00000000"),  # 0
    # instructions:
    (0, "01001100"),  # load acc 12
    (1, "00011111"),  # add acc 15
    (2, "00111100"),  # store acc at 12
    (3, "01001110"),  # load acc 14
    (4, "00101101"),  # sub acc 13
    (5, "00111110"),  # store acc 14
    (6, "10000000"),  # branch to 0 if acc = 0
    (7, "10111100"),   # print 12
    (8, "00000000")  # end
    ]

divide_instructions = [  # divide two numbers
    # data
    (15, '00000110'),  # 6
    (14, '00000010'),  # 2
    (13, '00000001'),  # 1
    (12, '00000000'),  # 0
    # instructions
    (0, '01001111'),
    (1, '00101110'),
    (2, '00111111'),
    (3, '01001100'),
    (4, '00011101'),
    (5, '00111100'),
    (6, '01001111'),
    (7, '10000000'),
    (8, '10111100'),
    (9, '00000000')  # end
    ]


if __name__ == "__main__":
    ram = RAM(16)
    load_ram(ram, divide_instructions)
    cpu = CPU(ram)
    cpu.excecute()  # execute full instructions
