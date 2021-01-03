#! /usr/bin/env python

import sys
from collections import Counter, defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

col, row = 25, 6
layers = []
layer = []
for cursor in range(0, len(lines[0]), col):
    layer.append(lines[0][cursor:cursor+col])
    if len(layer)==row:
        layers.append(layer)
        layer=[]
if layer:
    layers.append(layer)

mini = col*row ; result = 0
for layer in layers:
    tmp = Counter(''.join(layer))
    zero_sum = tmp['0']
    if zero_sum<mini:
        mini = zero_sum
        result = tmp['1']*tmp['2']

# Part 1
print(result)

# Part 2
def print_img(img):
    for j in range(row):
        for i in range(col):
            if img[i,j]==0:
                print(' ', end='')
            elif img[i,j]==1:
                print('@', end='')
            else:
                print(' ', end='')
        print()

image = defaultdict(lambda: 2)
for layer in layers:
    for j in range(row):
        for i in range(col):
            if image[i,j]==2:
                image[i,j] = int(layer[j][i])
print_img(image)


