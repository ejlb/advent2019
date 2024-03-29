class Computer:
    def __init__(self, program):
        self.memory = list(program[:])
        self.ip = 0

        self.opcodes = {
            1: {"name": "add", "size": 4, "body": self.opcode_add},
            2: {"name": "mul", "size": 4, "body": self.opcode_mul},
            3: {"name": "input", "size": 2, "body": self.opcode_input},
            4: {"name": "print", "size": 2, "body": self.opcode_print},
            5: {"name": "je", "size": 3, "body": self.opcode_jump_true},
            6: {"name": "jne", "size": 3, "body": self.opcode_jump_false},
            7: {"name": "less", "size": 4, "body": self.opcode_less},
            8: {"name": "equal", "size": 4, "body": self.opcode_equal},
        }

    def opcode_add(self, a, b, out_addr, modes=None):
        a, b = self.dereference_addresses([a,b], modes[:2])
        self.write(out_addr, a + b)

    def opcode_mul(self, a, b, out_addr, modes=None):
        a, b = self.dereference_addresses([a,b], modes[:2])
        self.write(out_addr, a * b)

    def opcode_print(self, message, modes=None):
        message = self.dereference_addresses([message], modes)
        print(message[0])

    def opcode_input(self, out_addr, modes=None):
        value = int(input('input please: '))
        self.write(out_addr, value)

    def opcode_jump_true(self, cond, addr, modes=None):
        cond, addr = self.dereference_addresses([cond,addr], modes)
        if cond:
            self.ip = addr

    def opcode_jump_false(self, cond, addr, modes=None):
        cond, addr = self.dereference_addresses([cond,addr], modes)
        if not cond:
            self.ip = addr

    def opcode_less(self, a, b, out_addr, modes=None):
        a, b = self.dereference_addresses([a,b], modes[:2])
        self.write(out_addr, int(a < b))

    def opcode_equal(self, a, b, out_addr, modes=None):
        a, b = self.dereference_addresses([a,b], modes[:2])
        self.write(out_addr, int(a == b))

    def read(self, address):
        return self.memory[address]

    def read_range(self, start, stop):
        return self.memory[start:stop]

    def write(self, address, value):
        self.memory[address] = value

    def dereference_addresses(self, addresses, param_modes):
        while(len(addresses) > len(param_modes)):
            param_modes.append(0) # zero-pad

        return [
            self.read(addresses[i]) if param_modes[i] == 0 else addresses[i]
            for i in range(len(addresses))
        ]

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
