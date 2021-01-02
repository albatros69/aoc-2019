#! /usr/bin/env python

import sys
from collections import Counter

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

inf, sup = map(int, lines[0].split('-'))

def is_valid_part1(args):
    return len(Counter(args))<6 and inf <= int(''.join(args)) <= sup

def is_valid_part2(args):
    return (2 in Counter(args).values()) and inf <= int(''.join(args)) <= sup

result_part1=0; result_part2=0
try:
    for i in range(int(str(inf)[0]), int(str(sup)[0])+1):
        for j in range(i, 10):
            for k in range(j, 10):
                for l in range(k, 10):
                    for m in range(l, 10):
                        for n in range(m, 10):
                            tmp = tuple(map(str,(i,j,k,l,m,n)))
                            if int(''.join(tmp)) > sup:
                                raise StopIteration
                            else:
                                result_part1 += int(is_valid_part1(tmp))
                                result_part2 += int(is_valid_part2(tmp))

except StopIteration:
    print(result_part1, result_part2)