#! /usr/bin/env python

import sys
from collections import defaultdict
from math import gcd

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Map():
    map=None
    width=0
    height=0
    cursor=0
    station=None
    walk=None

    def __init__(self, lines) -> None:
        self.map=dict()
        self.height=len(lines)
        for j in range(self.height):
            l=lines[j]
            self.width=len(l)
            for i in range(self.width):
                self.map[i,j] = l[i]
        self.tmp_map=self.map.copy()

    def print_map(self):
        for j in range(self.height):
            for i in range(self.width):
                if (i,j) == self.station:
                    print('@', end='')
                elif self.walk and (i,j) == self.walk[self.cursor]:
                    print('X', end='')
                else:
                    print("%s"% self.tmp_map[i,j], end='')
            print()

    def is_visible(self, asteroid, other):
        ax, ay = asteroid
        ox, oy = other

        if ax==ox:
            return not any( self.map[ax,y]=='#' for y in range(min(ay,oy)+1, max(ay,oy)) )
        elif ay==oy:
            return not any( self.map[x,ay]=='#' for x in range(min(ax,ox)+1, max(ax,ox)) )
        else:
            return not any( self.map[x,y]=='#' and (ax-ox)*y-(ay-oy)*x==(ax-ox)*ay-(ay-oy)*ax
                            for x in range(min(ax,ox)+1, max(ax,ox)) for y in range(min(ay,oy)+1, max(ay,oy)) )

    def compute_visibles(self):
        result = defaultdict(int)
        for asteroid in self.map:
            if self.map[asteroid]=='#':
                for other in self.map:
                    if self.map[other]=='#' and other != asteroid and self.is_visible(asteroid, other):
                        result[asteroid]+=1
        return result

    def fire(self):
        asteroid = self.walk[self.cursor]

        if self.map[asteroid]=='#' and self.is_visible(asteroid, self.station):
            self.tmp_map[asteroid] = '-'
            return asteroid
        else:
            return None

    def compute_walk(self):
        def key(a):
            x,y = a
            sx,sy = self.station
            if x!=sx:
                return (y-sy)/(x-sx) # tangent
            else: # Not used because we're handling this case separately
                return (y-sy)*100000.

        self.walk = [ (self.station[0],y) for y in range(self.station[1]-1,-1,-1) ] + \
            sorted([ (x,y) for x in range(self.station[0]+1, self.width) for y in range(self.height) ], key=key) + \
            [ (self.station[0],y) for y in range(self.station[1]+1,self.height) ] + \
            sorted([ (x,y) for x in range(self.station[0]-1, -1, -1) for y in range(self.height) ], key=key)

    def rotate_laser(self):
        self.cursor = self.cursor+1
        if self.cursor >= len(self.walk):
            self.cursor = 0
            self.map = self.tmp_map.copy() # Full rotation completed, so we can apply the changes

asteroids = Map(lines)

# Part 1
tmp=asteroids.compute_visibles()
# for j in range(map.height):
#     for i in range(map.width):
#         print("% 2d"%tmp[i,j], end='')
#     print()
maxi = max(tmp, key=lambda x:tmp[x])
print(maxi, tmp[maxi])

# Part 2
asteroids.station = maxi
asteroids.compute_walk()
result=None ; count=0
while count < min(200, tmp[maxi]):
    # print('-'*8); asteroids.print_map();
    result = asteroids.fire()
    count+=int(result is not None)
    asteroids.rotate_laser()

print(count, result, result[0]*100+result[1])