#! /usr/bin/env python

import sys
from collections import Counter

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Component():
    name=None
    batch_size=0
    reqs=None

    def __init__(self, line) -> None:
        reqs, component = (c.strip() for c in line.split('=>'))
        self.batch_size, self.name = component.split(' ')
        self.batch_size = int(self.batch_size)
        self.reqs = dict( req.strip().split(' ')[::-1] for req in reqs.split(',') )
        for k in self.reqs:
            self.reqs[k] = int(self.reqs[k])

    def __repr__(self) -> str:
        return "{0.name}: {0.batch_size} => {0.reqs}".format(self)

    def recipe(self, qty):
        nb_batch = (qty//self.batch_size)+int(qty%self.batch_size>0)
        result = { k: -nb_batch*v for k,v in self.reqs.items() }
        result[self.name] = nb_batch*self.batch_size
        return result


components = dict()
for l in lines:
    tmp = Component(l)
    components[tmp.name] = tmp

# Part 1
def produce_fuel(fuel_qty):
    """ Gives the amount of ORE required for a certain amount of fuel"""
    stocks = Counter({ 'ORE': 0, 'FUEL': -fuel_qty })
    tmp=Counter()

    while any(v<0 for k,v in stocks.items() if k!='ORE'):
        tmp.clear()
        for c in stocks:
            if stocks[c]<0 and c!='ORE':
                tmp.update(components[c].recipe(-stocks[c]))
        stocks.update(tmp)

    return stocks['ORE']

ratio = produce_fuel(1)
print("ORE:", ratio)

# Part 2
target_ORE=-1000000000000
fuel=target_ORE//ratio
step=10**(len(str(fuel))-2)

# Looking for the optimal by dichotomy
while step!=0:
    req_ORE = produce_fuel(fuel)
    if (req_ORE-target_ORE)*step<0:
        step=-step//2
    fuel+=step
print("Max fuel:", fuel)