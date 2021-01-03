#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class IntCode():
    memory = None
    cursor = 0
    finished = False
    inputs = None
    outputs = None

    def __init__(self, intcode, inputs=[]) -> None:
        self.memory = dict()
        for i,code in enumerate(intcode):
            self.memory[i] = int(code)
        self.golden_copy = self.memory.copy()
        self.inputs = inputs
        self.outputs = []

    def read_opcode(self, modes):
        params = []
        for i,a in enumerate(reversed(modes)):
            if a=='0':
                params.append(self.memory[self.cursor+i+1])
            elif a=='1':
                params.append(self.cursor+i+1)

        return params

    def opcode_01(self, modes):
        """ Addition """
        modes = f"{modes:03d}"
        params = self.read_opcode(modes)
        self.memory[params[2]] = self.memory[params[0]] + self.memory[params[1]]
        return 4

    def opcode_02(self, modes):
        """ Multiplication """
        modes = f"{modes:03d}"
        params = self.read_opcode(modes)
        self.memory[params[2]] = self.memory[params[0]] * self.memory[params[1]]
        return 4

    def opcode_03(self, modes):
        """ Read input """
        modes = f"{modes:01d}"
        params = self.read_opcode(modes)
        self.memory[params[0]] = self.inputs.pop(0)
        return 2

    def opcode_04(self, modes):
        """ Print output """
        modes = f"{modes:01d}"
        params = self.read_opcode(modes)
        self.outputs.append(self.memory[params[0]])
        return 2

    def opcode_05(self, modes):
        """ Jump-If-True """
        modes = f"{modes:02d}"
        params = self.read_opcode(modes)
        if self.memory[params[0]] != 0:
            return self.memory[params[1]] - self.cursor
        else:
            return 3

    def opcode_06(self, modes):
        """ Jump-If-False """
        modes = f"{modes:02d}"
        params = self.read_opcode(modes)
        if self.memory[params[0]] == 0:
            return self.memory[params[1]] - self.cursor
        else:
            return 3

    def opcode_07(self, modes):
        """ Less-Than """
        modes = f"{modes:03d}"
        params = self.read_opcode(modes)
        self.memory[params[2]] = int(self.memory[params[0]] < self.memory[params[1]])
        return 4

    def opcode_08(self, modes):
        """ Equals """
        modes = f"{modes:03d}"
        params = self.read_opcode(modes)
        self.memory[params[2]] = int(self.memory[params[0]] == self.memory[params[1]])
        return 4

    def opcode_99(self, modes):
        self.finished = True
        return 1

    def execute(self):
        opcode=self.memory[self.cursor]%100
        modes=self.memory[self.cursor]//100
        self.cursor += getattr(self, f'opcode_{opcode:02d}')(modes)

    def run(self):
        while not self.finished:
            self.execute()


# For testing
# for l in lines:
#     program = IntCode(l.split(','), inputs=[5])
#     program.run()
#    print(*program.memory.values(), sep=',')
#    print(*program.outputs, sep=',')

# Part 1
program = IntCode(lines[0].split(','), inputs=[1])
program.run()
print(*program.outputs, sep=',')

# # Part 2
program = IntCode(lines[0].split(','), inputs=[5])
program.run()
print(*program.outputs, sep=',')
