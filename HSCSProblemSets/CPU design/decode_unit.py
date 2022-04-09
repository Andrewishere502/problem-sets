class DecodeUnit:
    def __init__(self):
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

    @staticmethod
    def choose_input_output(opperand):
        """Determine if the IO opcode refers to input or output."""
        if opperand == "0001":
            return "input"
        elif opperand == "0010":
            return "output"
        return

    def decode(self, instruction):
        """Turn an instruction into an opcode and operand. Return the
        opcode and operand.
        """
        opcode = self.opcodes.get(instruction[:4])
        operand = instruction[4:]

        if opcode == "end":
            return "end", "end"
        elif opcode == "IO":  # input/output
            operand = self.choose_input_output(operand)
        return opcode, operand