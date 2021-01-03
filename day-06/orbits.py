#! /usr/bin/env python

import sys
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

orbits = defaultdict(list)
for l in lines:
    center, obj = l.split(')')
    orbits[center].append(obj)

cache = dict()
def nb_orbits(obj):
    if obj not in orbits:
        return 0

    if obj not in cache:
        cache[obj] = len(orbits[obj]) + sum(map(nb_orbits, orbits[obj]))

    return cache[obj]

# Part 1
print(sum(map(nb_orbits, orbits)))

# Part 2
rev_orbits = dict()
for center in orbits:
    for o in orbits[center]:
        rev_orbits[o] = center

already_seen = set()
def look_for_path(obj):
    if obj not in orbits:
        return []
    elif obj in already_seen:
        return []
    elif 'SAN' in orbits[obj]:
        return [ obj ]
    else:
        already_seen.add(obj)

        for path in map(look_for_path, orbits[obj]):
            if path:
                return [obj]+path

        if rev_orbits[obj] in already_seen:
            return []
        else:
            return [obj] + look_for_path(rev_orbits[obj])

tmp=look_for_path(rev_orbits['YOU'])
print(len(tmp)-1)
