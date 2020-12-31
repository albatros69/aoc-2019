#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def fuel_req(mass):
    return mass//3 - 2

# Part 1
total = sum([ fuel_req(int(mass)) for mass in lines ])
print(total)

# Part 2
total = 0
for mass in lines:
    extra_fuel = fuel_req(int(mass))
    while extra_fuel >= 0:
        total += extra_fuel
        extra_fuel = fuel_req(extra_fuel)

print(total)