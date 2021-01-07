#! /usr/bin/env python
from collections import defaultdict

class IntCode():
    memory = None
    cursor = 0
    finished = False
    inputs = None
    outputs = None
    relative_base = 0

    def __init__(self, intcode, inputs=[]) -> None:
        self.memory = defaultdict(int)
        for i,code in enumerate(intcode):
            self.memory[i] = int(code)
        self.inputs = inputs
        self.outputs = []

    def read_opcode(self, modes):
        params = []
        for i,a in enumerate(reversed(modes)):
            if a=='0':
                params.append(self.memory[self.cursor+i+1])
            elif a=='1':
                params.append(self.cursor+i+1)
            elif a=='2':
                params.append(self.relative_base+self.memory[self.cursor+i+1])

        return params

    def opcode_01(self, modes):
        """ Addition """
        modes = f"{modes:03d}"
        params = self.read_opcode(modes)
        self.memory[params[2]] = self.memory[params[0]] + self.memory[params[1]]
        self.cursor += 4

    def opcode_02(self, modes):
        """ Multiplication """
        modes = f"{modes:03d}"
        params = self.read_opcode(modes)
        self.memory[params[2]] = self.memory[params[0]] * self.memory[params[1]]
        self.cursor += 4

    def opcode_03(self, modes):
        """ Read input """
        modes = f"{modes:01d}"
        params = self.read_opcode(modes)
        self.memory[params[0]] = self.inputs.pop(0)
        self.cursor += 2

    def opcode_04(self, modes):
        """ Print-Output """
        modes = f"{modes:01d}"
        params = self.read_opcode(modes)
        self.outputs.append(self.memory[params[0]])
        self.cursor += 2

    def opcode_05(self, modes):
        """ Jump-If-True """
        modes = f"{modes:02d}"
        params = self.read_opcode(modes)
        if self.memory[params[0]] != 0:
            self.cursor = self.memory[params[1]]
        else:
            self.cursor += 3

    def opcode_06(self, modes):
        """ Jump-If-False """
        modes = f"{modes:02d}"
        params = self.read_opcode(modes)
        if self.memory[params[0]] == 0:
            self.cursor = self.memory[params[1]]
        else:
            self.cursor += 3

    def opcode_07(self, modes):
        """ Less-Than """
        modes = f"{modes:03d}"
        params = self.read_opcode(modes)
        self.memory[params[2]] = int(self.memory[params[0]] < self.memory[params[1]])
        self.cursor += 4

    def opcode_08(self, modes):
        """ Equals """
        modes = f"{modes:03d}"
        params = self.read_opcode(modes)
        self.memory[params[2]] = int(self.memory[params[0]] == self.memory[params[1]])
        self.cursor += 4

    def opcode_09(self, modes):
        """ Adjust-Relative-Base """
        modes = f"{modes:01d}"
        params = self.read_opcode(modes)
        self.relative_base += self.memory[params[0]]
        self.cursor += 2

    def opcode_99(self, modes):
        self.finished = True
        # self.cursor += 1

    def execute(self):
        opcode=self.memory[self.cursor]%100
        modes=self.memory[self.cursor]//100
        getattr(self, f'opcode_{opcode:02d}')(modes)

    def run(self):
        while not (len(self.outputs)==1 or self.finished):
            self.execute()
