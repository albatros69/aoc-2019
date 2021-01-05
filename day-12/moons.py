#! /usr/bin/env python

import sys
from itertools import combinations
from numpy import lcm

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Moon():
    position=(0,0,0)
    velocity=(0,0,0)

    def __init__(self,line) -> None:
        self.position = tuple(int(a.strip()[2:]) for a in line.split(','))

    def move(self):
        self.position = tuple(self.position[i]+self.velocity[i] for i in range(3) )

    def __repr__(self):
        return "pos=<x={0[0]:3},y={0[1]:3},z={0[2]:3}>, vel=<x={1[0]:3},y={1[1]:3},z={1[2]:3}>".format(self.position, self.velocity)

    @property
    def potential(self):
        return sum(abs(a) for a in self.position)

    @property
    def kinetic(self):
        return sum(abs(a) for a in self.velocity)


moons=[]
for l in lines:
    moons.append(Moon(l.strip('<>')))

def sign(a:int):
    """ Return the sign of a """
    if a==0:
        return 0
    elif a<0:
        return -1
    else:
        return 1

def apply_gravity_part1(m1, m2):
    gravity = tuple(sign(m2.position[i]-m1.position[i]) for i in range(3))

    m1.velocity = tuple(m1.velocity[i]+gravity[i] for i in range(3))
    m2.velocity = tuple(m2.velocity[i]-gravity[i] for i in range(3))


# Part 1
for i in range(1000):
    for m1,m2 in combinations(moons, 2):
        apply_gravity_part1(m1,m2)
    for m in moons:
        m.move()

print("Total energy:", sum(m.potential*m.kinetic for m in moons))

# Part 2
# We will look for periods on each axe, then the lcm of the periods gives us the result...
def apply_gravity_part2(m1, m2, axe):
    gravity = tuple(sign(m2.position[i]-m1.position[i]) if i==axe else 0 for i in range(3))

    m1.velocity = tuple(m1.velocity[i]+gravity[i] for i in range(3))
    m2.velocity = tuple(m2.velocity[i]-gravity[i] for i in range(3))

moons=[]
for l in lines:
    moons.append(Moon(l.strip('<>')))

periods=[]
for axe in range(3):
    already_seen=[]
    step=0

    pos_init=tuple(m.position[axe] for m in moons)
    vel_init=tuple(m.velocity[axe] for m in moons)
    while True:
        step+=1
        for m1,m2 in combinations(moons, 2):
            apply_gravity_part2(m1,m2,axe)
        for m in moons:
            m.move()
        pos=tuple(m.position[axe] for m in moons)
        vel=tuple(m.velocity[axe] for m in moons)
        if pos==pos_init and vel==vel_init:
            periods.append(step)
            break

print("Periods:", periods, lcm.reduce(periods))

