#! /usr/bin/env python

import sys
from collections import namedtuple

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


Point = namedtuple('Point', ('x', 'y'))

def read(pos, instr):
    dir, lg = instr[0], int(instr[1:])
    if dir=='R':
        return Point(pos.x+lg, pos.y)
    elif dir=='L':
        return Point(pos.x-lg, pos.y)
    elif dir=='U':
        return Point(pos.x, pos.y+lg)
    elif dir=='D':
        return Point(pos.x, pos.y-lg)

def intersection(a,b,c,d):
    if a.x == b.x and c.y == d.y and c.x <= a.x <= d.x and a.y <= c.y <= b.y:
        return Point(a.x, c.y)
    elif a.y == b.y and c.x == d.x and c.y <= a.y <= d.y and a.x <= c.x <= b.x:
        return Point(c.x, a.y)
    else:
        return None

def distance(pt):
    return sum(map(abs, pt))


class Wire():
    path = None

    def __init__(self, line) -> None:
        self.path = [ Point(0,0) ]
        pos = Point(0,0)
        for instr in line.split(','):
            pos = read(pos, instr)
            self.path.append(pos)

    def inter_segment(self, a,b):
        result = []
        for i in range(len(self.path)-1):
            inter = intersection(a,b, *sorted([self.path[i], self.path[i+1]]))
            if inter:
                result.append(inter)
        return result

    def inter_wire(self, wire):
        result = []
        for i in range(len(wire.path)-1):
            result.extend(self.inter_segment(*sorted([wire.path[i], wire.path[i+1]])))
        return result

    def steps(self, pt):
        result = 0
        for i in range(len(self.path)-1):
            a,b = self.path[i], self.path[i+1]
            if (a.x == pt.x and b.x == pt.x) or (a.y == pt.y and b.y == pt.y):
                result += abs(pt.x-a.x) + abs(pt.y-a.y)
                break
            else:
                result += abs(b.x-a.x) + abs(b.y-a.y)
        return result


while lines:
    wire1 = Wire(lines.pop(0))
    wire2 = Wire(lines.pop(0))
    inter = wire1.inter_wire(wire2)
    print('-- Part 1 --', min([ distance(pt) for pt in inter if pt != Point(0,0) ]))
    print('-- Part 2 --', min(map(sum, zip([ wire1.steps(pt) for pt in inter if pt != Point(0,0) ], [ wire2.steps(pt) for pt in inter if pt != Point(0,0) ]))))

