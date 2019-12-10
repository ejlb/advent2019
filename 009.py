import itertools

import scipy.sparse
import numpy as np
from collections import defaultdict

class Memory:
    def __init__(self, program):
        self.memory = defaultdict(int)

        for i, p in enumerate(program):
            self.memory[i] = p

    def __getitem__(self, key):
        return self.memory[key]

    def __setitem__(self, key, value):
        self.memory[key] = int(value)


class Computer:
    def __init__(self, program):
        self.memory = Memory(program[:])

        self.ip = 0
        self.input = 0
        self.output = 0
        self.rel_base = 0

        self.opcodes = {
            1: {"name": "add", "size": 4, "body": self.opcode_add},
            2: {"name": "mul", "size": 4, "body": self.opcode_mul},
            3: {"name": "input", "size": 2, "body": self.opcode_input},
            4: {"name": "print", "size": 2, "body": self.opcode_print},
            5: {"name": "je", "size": 3, "body": self.opcode_jump_true},
            6: {"name": "jne", "size": 3, "body": self.opcode_jump_false},
            7: {"name": "less", "size": 4, "body": self.opcode_less},
            8: {"name": "equal", "size": 4, "body": self.opcode_equal},
            9: {"name": "relbase", "size": 2, "body": self.opcode_relbase},
        }


    # todo
    # make write mode nicer
    # todo


    def opcode_add(self, a, b, out_addr, modes=None):
        a, b = self.dereference_addresses([a,b], [modes[0], modes[1]])
        out_addr = self.dereference_addresses([out_addr], [modes[2]], writeMode=True)[0]
        self.write(out_addr, a + b)

    def opcode_mul(self, a, b, out_addr, modes=None):
        a, b = self.dereference_addresses([a,b], [modes[0], modes[1]])
        out_addr = self.dereference_addresses([out_addr], [modes[2]], writeMode=True)[0]
        self.write(out_addr, a * b)

    def opcode_print(self, message, modes=None):
        message = self.dereference_addresses([message], [modes[0]])[0]
        self.output = message
        print(self.output)

    def opcode_input(self, out_addr, modes=None):
        out_addr = self.dereference_addresses([out_addr], [modes[0]], writeMode=True)[0]
        self.input = input('input :> ')
        self.write(out_addr, int(self.input))

    def opcode_jump_true(self, cond, addr, modes=None):
        cond, addr = self.dereference_addresses([cond,addr], modes)
        if cond:
            self.ip = addr

    def opcode_jump_false(self, cond, addr, modes=None):
        cond, addr = self.dereference_addresses([cond, addr], modes)
        if not cond:
            self.ip = addr

    def opcode_less(self, a, b, out_addr, modes=None):
        a, b = self.dereference_addresses([a,b], [modes[0], modes[1]])
        out_addr = self.dereference_addresses([out_addr], [modes[2]], writeMode=True)[0]
        self.write(out_addr, int(a < b))

    def opcode_equal(self, a, b, out_addr, modes=None):
        a, b = self.dereference_addresses([a,b], [modes[0], modes[1]])
        out_addr = self.dereference_addresses([out_addr], [modes[2]], writeMode=True)[0]
        self.write(out_addr, int(a == b))

    def opcode_relbase(self, base, modes=None):
        base = self.dereference_addresses([base], [modes[0]])[0]
        self.rel_base += base

    def read(self, address):
        return self.memory[address]

    def write(self, address, value):
        self.memory[address] = value

    def dereference_addresses(self, addresses, param_modes, writeMode=False):
        resolved = []

        for addr, param in zip(addresses, param_modes):
            if param == 0:
                if writeMode:
                    value = addr
                else:
                    value = self.read(addr)
            elif param == 1:
                value = addr
            elif param == 2:
                if writeMode:
                    value = addr + self.rel_base
                else:
                    value = self.read(addr + self.rel_base)
            else:
                raise ValueError('bad param mode')

            resolved.append(value)

        return resolved

    def send(self, arg):
        self.run.send(arg)

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
            param_modes = [int(i) for i in instruction[:-2][::-1]]

            args = [
                int(self.read(self.ip + 1 + offset))
                for offset in range(opcode_config["size"]-1)
            ]

            while len(args) > len(param_modes):
                param_modes.append(0)

            old_ip = self.ip

            # execute opcode with arguments
            opcode_config["body"](*args, modes=param_modes)

            # only modify IP if op didn't change the IP
            if self.ip == old_ip:
                self.ip += opcode_config["size"]

if __name__ == "__main__":
    program_rom = tuple(map(int, open("009.txt").read().split(",")))
    Computer(program_rom).run()

