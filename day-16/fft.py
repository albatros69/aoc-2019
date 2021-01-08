#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

pattern_seed = (0, 1, 0, -1)

def pattern(i, position):
    return pattern_seed[((i+1)%(position*len(pattern_seed)))//position]

def element(input, position):
    return abs(sum(a*pattern(i,position) for i,a in enumerate(input)))%10

print("-- Part 1 --")
for l in lines:
    input=[ int(a) for a in l ]
    for _ in range(100):
        input=[ element(input, pos+1) for pos in range(len(input)) ]
    print(*input[:8], sep='')

print("-- Part 2 --")
# https://www.reddit.com/r/adventofcode/comments/ebf5cy/2019_day_16_part_2_understanding_how_to_come_up/fb4bvw4/
for l in lines:
    offset=int(l[:7])
    input = ([ int(a) for a in l ]*10000)[offset:]
    for _ in range(100):
        for i in range(len(input)-2,-1,-1):
            input[i]=input[i]+input[i+1]
        for i in range(len(input)):
            input[i] = input[i]%10
    print(*input[:8], sep='')
