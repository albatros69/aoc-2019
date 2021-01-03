#! /usr/bin/env python

import sys
from intcode import IntCode

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Part 1
print("-- Part 1 --")
for l in lines:
    program = IntCode(l.split(','), inputs=[1])
    program.run()
    print(*program.outputs, sep=',')

# Part 2
print("-- Part 2 --")
for l in lines:
    program = IntCode(l.split(','), inputs=[2])
    program.run()
    print(*program.outputs, sep=',')
