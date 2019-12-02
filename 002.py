class Computer:
    def __init__(self, program):
        self.memory = list(program)
        self.ip = 0

        self.opcodes = {
            1: {"name": "add", "size": 4, "body": self.opcode_add},
            2: {"name": "mul", "size": 4, "body": self.opcode_mul},
        }

    def opcode_add(self, a, b, p):
        self.write(p, self.read(a) + self.read(b))

    def opcode_mul(self, a, b, p):
        self.write(p, self.read(a) * self.read(b))

    def read(self, address):
        return self.memory[address]

    def read_range(self, start, stop):
        return self.memory[start:stop]

    def write(self, address, value):
        self.memory[address] = value

    def run(self):
        while True:
            opcode = self.read(self.ip)

            # special halting opcode
            if opcode == 99:
                break

            opcode_config = self.opcodes[opcode]

            if opcode not in self.opcodes.keys():
                raise ValueError("unknown opcode {}".format(opcode))

            args = self.read_range(self.ip + 1, self.ip + opcode_config["size"])

            # execute opcode with arguments
            opcode_config["body"](*args)

            self.ip += opcode_config["size"]


if __name__ == "__main__":
    program_rom = tuple(map(int, open("002.txt").read().split(",")))

    for noun in range(0, 100):
        for verb in range(0, 100):

            computer = Computer(program_rom)
            computer.write(1, noun)
            computer.write(2, verb)
            computer.run()
            value = computer.read(0)

            if value == 19690720:
                print(noun, verb, 100 * noun + verb)
