#! /usr/bin/env python

import sys
from itertools import permutations
from intcode import IntCode

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Part 1
print("-- Part 1 --")
for l in lines:
    result = None ; maxi = 0
    for phase_settings in permutations(range(5)):
        input = 0
        for i in range(5):
            program = IntCode(l.split(','), inputs=[phase_settings[i]]+[input])
            program.run()
            input = program.outputs[0]
        if input > maxi:
            result = phase_settings
            maxi = input

    print(result, '->', maxi)

# Part 2
print("-- Part 2 --")
for l in lines:
    program = IntCode(l.split(','))
    result = None ; maxi = 0
    for phase_settings in permutations(range(5, 10)):
        # Initialisation
        programs = [ IntCode(l.split(','), inputs=[phase_settings[i]]) for i in range(5) ]

        # Further runs till the end of every programs
        input = 0
        while all(not pgm.finished for pgm in programs):
            for program in programs:
                program.inputs.append(input)
                program.run()
                if not program.finished:
                    input = program.outputs.pop()

        if input > maxi:
            result = phase_settings
            maxi = input

    print(result, '->', maxi)

