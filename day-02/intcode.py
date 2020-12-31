#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class IntCode():
    memory = None
    cursor = 0
    finished = False

    def __init__(self, intcode) -> None:
        self.memory = dict()
        for i,code in enumerate(intcode):
            self.memory[i] = int(code)
        self.golden_copy = self.memory.copy()

    def execute(self):
        opcode = self.memory[self.cursor]
        if opcode == 1:
            inputs = self.memory[self.cursor+1], self.memory[self.cursor+2]
            target = self.memory[self.cursor+3]
            self.memory[target] = self.memory[inputs[0]] + self.memory[inputs[1]]
            self.cursor += 4
        elif opcode == 2:
            inputs = self.memory[self.cursor+1], self.memory[self.cursor+2]
            target = self.memory[self.cursor+3]
            self.memory[target] = self.memory[inputs[0]] * self.memory[inputs[1]]
            self.cursor += 4
        elif opcode == 99:
            self.finished = True
            self.cursor += 1
        else:
            raise ValueError

    def output(self):
        return self.memory[0]

    def run(self):
        while not self.finished:
            self.execute()

    def reset(self, noun=12, verb=2):
        self.memory = self.golden_copy.copy()
        self.memory[1] = noun
        self.memory[2] = verb
        self.cursor = 0
        self.finished = False


# # For testing
# for l in lines:
#     program = IntCode(l.split(','))
#     program.run()
#     print(','.join([ str(v) for v in program.memory.values() ]))

# Part 1
program = IntCode(lines[0].split(','))
program.memory[1]=12 ; program.memory[2]=2
program.run()
print(program.output())

# Part 2
for noun in range(100):
    for verb in range(100):
        program.reset(noun=noun, verb=verb)
        program.run()
        if program.output() == 19690720:
            print(noun*100+verb)
            exit()
