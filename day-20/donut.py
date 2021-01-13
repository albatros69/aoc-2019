#! /usr/bin/env python

import sys
from collections import defaultdict, deque

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


def add(point, dir):
    return (point[0]+dir[0], point[1]+dir[1])

def rev(dir):
    return (-dir[0],-dir[1])


class Donut():
    area=None
    entrance=None
    exit=None
    directions=((0,1),(0,-1),(-1,0),(1,0),)
    tunnels=None
    min_x,min_y,max_x,max_y=(0,0,0,0)

    def __init__(self, lines) -> None:
        self.area = defaultdict(lambda: ' ')
        for y,l in enumerate(lines):
            for x,c in enumerate(l):
                self.area[x,y]=c

        self.max_x, self.max_y = max(x for x,_ in self.area.keys()), max(y for _,y in self.area.keys())

        extremities=defaultdict(list)
        for pt in tuple(self.area.keys()):
            if self.area[pt].isupper():
                neigh = tuple(add(pt,d) for d in self.directions)
                open_neigh = tuple(p for p in neigh if self.area[p]=='.')
                other_cap = tuple(p for p in neigh if self.area[p].isupper())

                if len(open_neigh)==1 and len(other_cap)==1:
                    label=''.join(sorted([self.area[pt],self.area[other_cap[0]]]))
                    if label=='AA':
                        self.entrance=open_neigh[0]
                    elif label=='ZZ':
                        self.exit=open_neigh[0]
                    else:
                        extremities[label].append(open_neigh[0])

        self.tunnels=dict()
        for s,e in extremities.values():
            self.tunnels[s]=e
            self.tunnels[e]=s


    def optimal_path_part1(self, source, destination):
        stack=deque([(source,(0,0),0)])

        seen = set()
        while stack:
            position, direction, steps = stack.popleft()
            # print("%6d %6d" % (len(stack), steps), end='\r')

            if position==destination:
                return steps
            elif position in seen:
                continue
            else:
                seen.add(position)
                for dir in self.directions:
                    new_pos = add(position, dir)
                    if dir==rev(direction):
                        continue
                    elif new_pos== destination:
                        return steps+1
                    elif self.area[new_pos]=='.':
                        stack.append((new_pos, dir, steps+1))
                    elif self.area[new_pos].isupper():
                        if position in self.tunnels: # Entrance and exit are no tunnels...
                            stack.append((self.tunnels[position], (0,0), steps+1))

        return None


    def optimal_path_part2(self, source, destination):
        stack=deque([(source, (0,0), 0, 0)])

        seen = set()
        while stack:
            position, direction, steps, level = stack.popleft()
            # print("%6d %6d" % (len(stack), steps), end='\r')

            if level==0 and position==destination:
                return steps
            elif (position, level) in seen:
                continue
            else:
                seen.add((position, level))
                for dir in self.directions:
                    new_pos = add(position, dir)
                    if dir==rev(direction):
                        continue
                    elif level==0 and new_pos==destination:
                        return steps+1
                    elif self.area[new_pos]=='.':
                        stack.append((new_pos, dir, steps+1, level))
                    elif self.area[new_pos].isupper() and position in self.tunnels: # Entrance and exit are no tunnels...
                        x,y=new_pos
                        is_outer=any(a<2 for a in (x, self.max_x-x, y, self.max_y-y))
                        if is_outer and level>0: # outer edge
                            stack.append((self.tunnels[position], (0,0), steps+1, level-1))
                        elif not is_outer: # inner edge
                            stack.append((self.tunnels[position], (0,0), steps+1, level+1))

        return None


    def print_screen(self):
        for y in reversed(range(self.max_y+1)):
            print(''.join( self.area[x,y] for x in range(self.max_x+1)))


donut = Donut(lines)

# Part 1
print('-- Part 1 --')
print("Shortest path:", donut.optimal_path_part1(donut.entrance, donut.exit))

# Part 2
print('-- Part 2 --')
print("Shortest path:", donut.optimal_path_part2(donut.entrance, donut.exit))