KEEP = list(map(int, open("002-001.txt").read().split(",")))


for n in range(0, 100):

    for v in range(0, 100):
        program = KEEP[:]
        program[1] = n
        program[2] = v

        for statement_i in range(0, len(program), 4):

            statement = program[statement_i : statement_i + 4]
            opcode = statement[0]

            if opcode == 99:
                break

            value_1 = program[statement[1]]
            value_2 = program[statement[2]]
            position = statement[3]

            if opcode == 1:
                program[position] = value_1 + value_2
            elif opcode == 2:
                program[position] = value_1 * value_2
            else:
                raise Exception("Unknown op code")

        if program[0] == 19690720:
            print("halt with {}".format(program[0]))
            print(n, v, 100 * n + v)
