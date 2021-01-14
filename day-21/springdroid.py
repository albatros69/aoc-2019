#! /usr/bin/env python

import sys
from intcode import IntCode


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def ascii_code(routine):
    return list(ord(c) for c in map(str, routine))


class Robot():
    program=None

    def __init__(self, line, input) -> None:
        self.program = IntCode(line.split(','), inputs=input)


    def handle_output(self):
        if self.program.outputs:
            output = ''.join(chr(c) if c<=255 else str(c) for c in self.program.outputs)
            print(output,end='')
        self.program.outputs.clear()


    def run(self):
        while not self.program.finished:
            self.program.run()
            self.handle_output()
        print()

    def print_screen(self):
        for y in reversed(range(self.height)):
            print(''.join( self.area[x,y] for x in range(self.width)))


# Part 1
print("-- Part 1 --")
# We jump if there's a hole in A, B, or C and if there's ground in D
routine="""OR A T
AND B T
AND C T
NOT T J
AND D J
WALK
"""
robot = Robot(lines[0], ascii_code(routine))
robot.run()

# Part 2
print("-- Part 2 --")
routine="""OR A T
AND B T
AND C T
NOT T J
AND D J
NOT J T
OR E T
OR H T
AND T J
RUN
"""
robot = Robot(lines[0], ascii_code(routine))
robot.run()
