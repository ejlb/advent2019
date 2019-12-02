class Computer:
    def __init__(self, program):
        self.memory = program[:]
        self.ip = 0

    def read(self, address):
        return self.memory[address]

    def write(self, address, value):
        self.memory[address] = value

    def run(self):
        while True:
            statement = self.memory[self.ip : self.ip + 4]
            opcode = statement[0]

            if opcode == 99:
                break

            value_1 = self.read(statement[1])
            value_2 = self.read(statement[2])
            position = statement[3]

            if opcode == 1:
                self.write(position, value_1 + value_2)
            elif opcode == 2:
                self.write(position, value_1 * value_2)
            else:
                raise Exception("Unknown op code")

            self.ip += 4


if __name__ == "__main__":
    program_rom = list(map(int, open("002.txt").read().split(",")))

    for noun in range(0, 100):
        for verb in range(0, 100):

            computer = Computer(program_rom)
            computer.write(1, noun)
            computer.write(2, verb)
            computer.run()
            value = computer.read(0)

            if value == 19690720:
                print(noun, verb, 100 * noun + verb)
