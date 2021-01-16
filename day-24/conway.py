#! /usr/bin/env python

import sys
from collections import defaultdict, namedtuple
from itertools import product

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

Size=namedtuple('Size', ('w', 'h'))

class Planet():
    area = None
    part = None
    size = Size(0, 0)
    empty='.'
    occupied='#'

    def __init__(self, input, part):
        self.part=part
        self.size = Size(w=len(input[0]), h=len(input))
        if part=='part1':
            self.area = [ list(l) for l in input ]
        else:
            self.area = defaultdict(lambda: self.empty)
            for (x,y) in product(range(self.size.w), range(self.size.h)):
                self.area[0, (x,y)]=input[y][x]

    def occupied_neigh_std(self, col, row):
        """ Counting all the occupied neighbour tiles """
        neighbours=0
        for d in ((0,1), (0,-1), (1,0), (-1,0)):
            y,x = row+d[0], col+d[1]
            if 0 <= y < self.size.h and 0 <= x < self.size.w:
                neighbours += int(self.area[y][x]==self.occupied)

        return neighbours

    def occupied_neigh_rec(self, level, col, row):
        """ Counting all the occupied neighbour tiles """
        neighbours=0

        for d in ((0,1), (0,-1), (1,0), (-1,0)):
            x,y = col+d[0], row+d[1]
            if y>=self.size.h:
                neighbours += int(self.area[level-1, (2,3)]==self.occupied)
            elif y<0:
                neighbours += int(self.area[level-1, (2,1)]==self.occupied)
            elif x>=self.size.w:
                neighbours += int(self.area[level-1, (3,2)]==self.occupied)
            elif x<0:
                neighbours += int(self.area[level-1, (1,2)]==self.occupied)
            elif (x,y)==(2,2):
                if x==col:
                    neighbours += sum(int(self.area[level+1, (a,row-d[1])]==self.occupied) for a in range(self.size.w))
                else: #y==row
                    neighbours += sum(int(self.area[level+1, (col-d[0],b)]==self.occupied) for b in range(self.size.h))
            else: #if 0 <= y < self.size.h and 0 <= x < self.size.w and (x,y)!=(2,2):
                neighbours += int(self.area[level, (x,y)]==self.occupied)

        return neighbours

    def change_tile(self, *args):
        if self.part=='part2':
            level, col, row = args
            if (col, row)==(2,2):
                return '?'

            nb_occupied = self.occupied_neigh_rec(level, col, row)

            if self.area[level, (col,row)]==self.empty and nb_occupied in (1,2):
                return self.occupied
            elif self.area[level, (col,row)]==self.occupied and nb_occupied != 1:
                return self.empty
            else:
                return self.area[level, (col,row)]

        else:
            col, row = args
            nb_occupied = self.occupied_neigh_std(col,row)

            if self.area[row][col]==self.empty and nb_occupied in (1,2):
                return self.occupied
            elif self.area[row][col]==self.occupied and nb_occupied != 1:
                return self.empty
            else:
                return self.area[row][col]

    @property
    def biodiversity(self):
        result=0
        for y in range(self.size.h-1, -1, -1):
            for x in range(self.size.w-1, -1, -1):
                result=2*result+int(self.area[y][x]==self.occupied)
        return result

    @property
    def levels(self):
        if self.part=='part2':
            return min(l for l,_ in self.area.keys()), max(l for l,_ in self.area.keys())
        else:
            return None

    def change_area(self):
        if self.part=='part1':
            new_area = [ [ self.change_tile(x, y) for x in range(self.size.w) ]
                            for y in range(self.size.h) ]
        else:
            new_area = defaultdict(lambda: self.empty)
            min_level, max_level = self.levels

            for l in range(min_level-1, max_level+2):
                for (x,y) in product(range(self.size.w), range(self.size.h)):
                    new_area[l, (x,y)] = self.change_tile(l, x, y)

        self.area = new_area

    def print(self, level=0):
        """ To allow for step-by-step verifications """
        if self.part=='part1':
            for y in range(self.size.h):
                print(''.join(self.area[y]))
        else:
            for y in range(self.size.h):
                print(''.join(self.area[level,(x,y)] for x in range(self.size.w)))


# Part 1
eris = Planet(lines, 'part1')

already_seen=set()
while True:
    biodiversity=eris.biodiversity
    if biodiversity in already_seen:
        # eris.print()
        print("Biodiversity:", biodiversity)
        break
    already_seen.add(biodiversity)
    eris.change_area()

# Part 2
eris = Planet(lines, 'part2')
# print("Start:"); eris.print(0)

for _ in range(200):
    eris.change_area()

# for l in range(-5, 6):
#     print("Depth:", l)
#     eris.print(l)

print("Number of bugs:", sum(c==eris.occupied for c in eris.area.values()))