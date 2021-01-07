#! /usr/bin/env python

import sys
from collections import defaultdict
# from random import randint
from intcode import IntCode


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def add(point, dir):
    return (point[0]+dir[0], point[1]+dir[1])

def rev(dir):
    return (dir//2)*2+(dir+1)%2


class Robot():
    program=None
    area=None
    droid=0,0
    ox_vent=None
    directions=((0,1),(0,-1),(-1,0),(1,0)) # N S W E
    direction=3
    intersections=None

    def __init__(self, line) -> None:
        self.program = IntCode(line.split(','), inputs=[self.direction+1])
        self.area = defaultdict(lambda: ' ')
        self.intersections=[self.direction]
        self.cache=dict()

    def handle_output(self, output):
        """0: The repair droid hit a wall. Its position has not changed.
           1: The repair droid has moved one step in the requested direction.
           2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
        """
        dir=self.directions[self.direction]
        # We mark the area as visited
        if self.area[self.droid]==' ':
            self.area[self.droid]='.'

        if output==0:
            self.area[add(self.droid, dir)]='#'
            # We need to backtrack...
            self.intersections.pop()
        elif output==1:
            self.droid = add(self.droid, dir)
        elif output==2:
            self.droid = add(self.droid, dir)
            self.ox_vent=self.droid
            self.area[self.ox_vent]='.'

        self.rotate()
        self.move_robot()

    def rotate(self):
        choices=tuple(self.area[add(self.droid, dir)]==' ' for dir in self.directions)

        # Stochastic walk... it works but it's a little suboptimal!
        # if any(choices):
        #     self.direction=choices.index(True)
        # else:
        #     self.direction = randint(0,len(self.directions)-1) # (self.direction+1)%len(self.directions)
        #     dir=self.directions[self.direction]
        #     while self.area[add(self.droid, dir)]=='#':
        #         self.direction = randint(0,len(self.directions)-1) # (self.direction+1)%len(self.directions)
        #         dir=self.directions[self.direction]

        if not any(choices):
            # We need to backtrack...
            self.direction = rev(self.intersections.pop())
        else:
            self.direction=choices.index(True)
            # In case we need to backtrack
            self.intersections.append(self.direction)

    def move_robot(self):
        self.program.inputs=[self.direction+1]

    def run(self):
        while not self.program.finished and self.intersections:
            self.program.run()
            if not self.program.finished:
                self.handle_output(*self.program.outputs)
                self.program.outputs.clear()

    def optimal_path(self, source, destination):
        alternatives=[(source,-1,0)]

        while alternatives:
            new_source, direction, length = alternatives.pop(0)
            # self.area[new_source]='~'
            if new_source==destination:
                break
            else:
                for dir,vec in enumerate(self.directions):
                    s = add(new_source, vec)
                    if s == destination:
                        return length+1
                    elif self.area[s]=='.' and dir!=rev(direction):
                        alternatives.append((s, dir, length+1))

        return length

    def fill(self, source):
        alternatives=[(source,-1,0)]

        while alternatives:
            new_source, direction, length = alternatives.pop(0)
            # self.area[new_source]='O'
            for dir,vec in enumerate(self.directions):
                s = add(new_source, vec)
                if self.area[s]=='.' and dir!=rev(direction):
                    alternatives.append((s, dir, length+1))

        return length

    def print_screen(self):
        min_x=min(x for x,_ in self.area.keys())
        max_x=max(x for x,_ in self.area.keys())
        min_y=min(y for _,y in self.area.keys())
        max_y=max(y for _,y in self.area.keys())

        # directions = tuple('↑↓←→')
        # self.area[self.droid]=directions[self.direction]
        # self.area[0,0]='x'
        # if self.ox_vent: self.area[self.ox_vent]='@'

        for y in reversed(range(min_y, max_y+1)):
            print(''.join( self.area[x,y] for x in range(min_x, max_x+1)))


# Part 1
print("-- Part 1 --")
robot = Robot(lines[0])
robot.run()
# robot.print_screen()
print("Ox Vent:", robot.ox_vent)
print('Optimal path to Ox Vent:', robot.optimal_path((0,0), robot.ox_vent))

# Part 2
print("-- Part 2 --")
print("Ox fill time:", robot.fill(robot.ox_vent))
# robot.print_screen()