#! /usr/bin/env python

import sys
from itertools import product
from collections import defaultdict
from intcode import IntCode


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Beam():
    program=None
    area=None
    drone=0,0
    direction=0
    height=0
    width=0
    count=0

    def __init__(self, line) -> None:
        self.program = IntCode(line.split(','), inputs=[])
        self.area = defaultdict(lambda: '.')

    def run(self, x, y):
        self.height=max(self.height,y+1)
        self.width=max(self.width, x+1)

        if (x,y) not in self.area:
            self.program.inputs=[x,y]
            while not self.program.finished:
                self.program.run()

            if self.program.outputs and self.program.outputs[0]==1:
                self.area[x,y]='#'
            self.program.reset()

        return self.area[x,y]

    def print_screen(self):
        for y in range(self.height):
            print(''.join( self.area[x,y] for x in range(self.width)))


beam = Beam(lines[0])

# Part 1
print("-- Part 1 --")
print("Affected zone:", sum(beam.run(x,y)=='#' for (x,y) in product(range(50), range(50))))
# beam.print_screen()

# Part 2
print("-- Part 2 --")
x,y=0,0
while True:
    print("%6d"*2 % (x, y), end='\r')
    if beam.run(x,y+99)=='#' and beam.run(x+99, y)=='#':
        break
    elif beam.run(x,y+99)!='#':
        x+=1
    elif beam.run(x+99,y)!='#':
        y+=1

print("Closest to emitter:", (x,y), x*10000+y)