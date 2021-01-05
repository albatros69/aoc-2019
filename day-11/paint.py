#! /usr/bin/env python

import sys
from collections import defaultdict
from intcode import IntCode

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class Robot():
    program=None
    direction=(0,1)
    position=(0,0)
    panels=None

    def __init__(self, line) -> None:
        self.program = IntCode(line.split(','), inputs=[])
        self.panels = defaultdict(int)

    def move(self, val):
        dx,dy=self.direction
        if val==1:
            self.direction=dy,-dx
        else: # val==0:
            self.direction=-dy,dx

        self.position = tuple(self.position[i]+self.direction[i] for i in (0,1,))

    def run(self):
        while not self.program.finished:
            self.program.inputs.append(self.panels[self.position])
            self.program.run()
            if not self.program.finished:
                color, new_dir = self.program.outputs
                self.program.outputs.clear()
                self.panels[self.position] = color
                self.move(new_dir)


# Part 1
print("-- Part 1 --")
robot = Robot(lines[0])
robot.run()
dim = len(robot.panels.keys())
print(dim)

# Part 2
print("-- Part 2 --")
robot = Robot(lines[0])
robot.panels[0,0] = 1 # we start on a white panel instead
robot.run()

min_x, min_y, max_x, max_y = dim,dim,-dim,-dim
for (x,y) in robot.panels.keys():
    min_x = min(x,min_x)
    max_x = max(x,max_x)
    min_y = min(y,min_y)
    max_y = max(y,max_y)

for y in reversed(range(min_y, max_y+1)):
    print(''.join( '@' if robot.panels[x,y]==1 else ' ' for x in range(min_x, max_x+1)))