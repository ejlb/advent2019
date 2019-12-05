class Computer:
    def __init__(self, program):
        self.memory = list(program[:])
        self.ip = 0

        self.opcodes = {
            1: {"name": "add", "size": 4, "body": self.opcode_add},
            2: {"name": "mul", "size": 4, "body": self.opcode_mul},
            3: {"name": "input", "size": 2, "body": self.opcode_input},
            4: {"name": "print", "size": 2, "body": self.opcode_print},
            5: {"name": "jump-true", "size": 3, "body": self.opcode_jump_true},
            6: {"name": "jump-false", "size": 3, "body": self.opcode_jump_false},
            7: {"name": "less", "size": 4, "body": self.opcode_less},
            8: {"name": "equal", "size": 4, "body": self.opcode_equal},
        }

    def opcode_add(self, a, b, p, modes=None):
        a, b = self.dereference_addresses([a,b], modes[:2])
        self.write(p, a + b)

    def opcode_mul(self, a, b, p, modes=None):
        a, b = self.dereference_addresses([a,b], modes[:2])
        self.write(p, a * b)

    def opcode_print(self, p, modes=None):
        p = self.dereference_addresses([p], modes)
        print(p[0])

    def opcode_input(self, p, modes=None):
        value = int(input('input please: '))
        self.write(p, value)

    def opcode_jump_true(self, a, p, modes=None):
        a, p = self.dereference_addresses([a,p], modes)
        if a:
            self.ip = p

    def opcode_jump_false(self, a, p, modes=None):
        a, p = self.dereference_addresses([a,p], modes)
        if not a:
            self.ip = p

    def opcode_less(self, a, b, p, modes=None):
        a, b = self.dereference_addresses([a,b], modes[:2])
        if a < b:
            self.write(p, 1)
        else:
            self.write(p, 0)

    def opcode_equal(self, a, b, p, modes=None):
        a, b = self.dereference_addresses([a,b], modes[:2])
        if a == b:
            self.write(p, 1)
        else:
            self.write(p, 0)

    def read(self, address):
        return self.memory[address]

    def read_range(self, start, stop):
        return self.memory[start:stop]

    def write(self, address, value):
        self.memory[address] = value

    def dereference_addresses(self, args, param_modes):
        while(len(args) > len(param_modes)):
            param_modes.append(0)

        for i in range(len(args)):
            if param_modes[i] == 0:
                args[i] = self.read(args[i])

        return args

    def run(self):
        while True:
            instruction = str(self.read(self.ip))
            opcode  = int(instruction[-2:])

            # special halting opcode
            if opcode == 99:
                break

            if opcode not in self.opcodes.keys():
                raise ValueError("unknown opcode {}".format(opcode))

            opcode_config = self.opcodes[opcode]
            param_modes = map(int, instruction[:-2])[::-1]
            args = self.read_range(self.ip + 1, self.ip + opcode_config["size"])

            old_ip = self.ip

            # execute opcode with arguments
            opcode_config["body"](*args, modes=param_modes)

            # only modify IP if op didn't change the IP
            if self.ip == old_ip:
                self.ip += opcode_config["size"]

if __name__ == "__main__":
    program_rom = tuple(map(int, open("005.txt").read().split(",")))

    computer = Computer(program_rom)
    computer.run()
