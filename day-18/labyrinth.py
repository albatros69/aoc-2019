#! /usr/bin/env python

import sys
from collections import namedtuple
from itertools import combinations
from heapq import heappop, heappush

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

State=namedtuple('State', ('steps', 'positions', 'keys', ))

def add(point, dir):
    return (point[0]+dir[0], point[1]+dir[1])

def rev(dir):
    return (-dir[0],-dir[1])

class Labyrinth():
    area=None
    bots=None
    directions=((0,1),(0,-1),(-1,0),(1,0))
    keys=None
    doors=None
    paths=None
    height,width=0,0

    def __init__(self, lines) -> None:
        self.area = dict()
        self.keys=dict()
        self.doors=dict()
        self.height=len(lines)
        self.bots=[]
        for y,l in enumerate(lines):
            self.width=len(l)
            for x,c in enumerate(l):
                self.area[x,y]=c
                if c=='@':
                    self.bots.append((x,y)) # save it
                    self.area[x,y]='.'  # and make it a free slot
                elif c.islower():
                    self.keys[c]=(x,y)
                elif c.isupper():
                    self.doors[c]=(x,y)

        self.paths=dict()

    def optimal_path_to_keys(self, source):
        """ Optimal path to destination, with a list of doors crossed """
        stack=[(0, source, (0,0), frozenset(), )]

        seen = set((source, ))
        while stack:
            steps, position, direction, doors = heappop(stack)

            if self.keys.keys()<seen:
                break
            else:
                for dir in self.directions:
                    if dir==rev(direction):
                        continue

                    new_pos = add(position, dir)
                    if new_pos in seen:
                        continue
                    elif self.area[new_pos]=='.':
                        heappush(stack, (steps+1, new_pos, dir, doors, ))
                    elif self.area[new_pos].islower() :
                        self.paths[new_pos,source]=steps+1,doors
                        self.paths[source,new_pos]=steps+1,doors
                        heappush(stack, (steps+1, new_pos, dir, doors, ) )
                    elif self.area[new_pos].isupper():
                        heappush(stack, (steps+1, new_pos, dir, doors|set((self.area[new_pos], )), ))
                    else:
                        pass
                    seen.add(new_pos)

    def solve_labyrinth(self):
        for a in self.keys.values():
            self.optimal_path_to_keys(a)
        for a in self.bots:
            self.optimal_path_to_keys(a)

        stack=[State(steps=0, positions=tuple(self.bots), keys=[])]

        seen=set()
        while stack:
            state = heappop(stack)

            if len(state.keys)==len(self.keys):
                return state.steps, state.keys
            elif (state.positions, frozenset(state.keys)) in seen:
                continue
            else:
                seen.add((state.positions, frozenset(state.keys)))
                for key in self.keys.keys()-set(state.keys): # Missing keys
                    for i,bot in enumerate(state.positions):
                        if (bot, self.keys[key]) in self.paths:
                            steps, doors = self.paths[bot, self.keys[key]]
                            if set(state.keys)>=set(c.lower() for c in doors):
                                new_pos = list(state.positions)
                                new_pos[i]=self.keys[key]
                                heappush(stack, State(state.steps+steps, tuple(new_pos), state.keys+[key]))

        return None, None

    def print_screen(self):
        for y in range(self.height):
            print(''.join( self.area[x,y] for x in range(self.width)))


print('-- Part 1 --')
labyrinth = Labyrinth(lines)
# labyrinth.print_screen()
print(labyrinth.solve_labyrinth())

print('-- Part 2 --')
labyrinth = Labyrinth(lines)
for bot in labyrinth.bots:
    for d in ((-1,1),(-1,-1),(1,-1),(1,1),(0,1),(0,-1),(-1,0),(1,0)):
        labyrinth.area[add(bot,d)]='#'
labyrinth.bots=[add(bot, d) for bot in labyrinth.bots for d in ((-1,1),(-1,-1),(1,-1),(1,1))]
for bot in labyrinth.bots:
    labyrinth.area[bot]="."
# labyrinth.print_screen()

print(labyrinth.solve_labyrinth())


