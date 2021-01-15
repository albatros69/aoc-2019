#! /usr/bin/env python

import sys
from intcode import IntCode


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


class Computer():
    address=None
    nic=None

    def __init__(self, address, program) -> None:
        self.address=address
        self.nic=IntCode(program.split(','), inputs=[address])

    def __repr__(self):
        return f"{self.address}"


class Network():
    computers=None
    switch=None
    NAT=None
    NAT_seen=None

    def __init__(self, program, size) -> None:
        self.computers=[]
        self.switch=dict()
        for i in range(size):
            self.computers.append(Computer(i, program))
            self.switch[i]= {'in': [], 'out': [], }
        self.NAT_seen=set()

    def handle_outputs(self, node):
        if node.nic.outputs:
            self.switch[node.address]['out'].extend(node.nic.outputs)
        node.nic.outputs.clear()

    def handle_packets(self):
        for node in self.computers:
            while len(self.switch[node.address]['out'])>=3:
                dest,X,Y,*l=self.switch[node.address]['out']
                if dest in self.switch:
                    self.switch[dest]['in'].extend([X,Y])
                else: # 255 case
                    self.switch[dest]={'in': [X,Y], 'out':[], }
                self.switch[node.address]['out'] = l

        for node in self.computers:
            node.nic.inputs=self.switch[node.address]['in'][:]
            self.switch[node.address]['in'].clear()

        # We store the last packet send to the NAT
        if 255 in self.switch and len(self.switch[255]['in'])==2:
            self.NAT=self.switch[255]['in'][:]
            self.switch[255]['in'].clear()

    def is_idle(self):
        return all(node.nic.waiting for node in self.computers)

    def run(self):
        for node in self.computers:
            node.nic.run()
            self.handle_outputs(node)

        self.handle_packets()

        # All computers are idle: NAT send its packet to node 0
        if self.is_idle() and self.NAT:
            self.computers[0].nic.inputs=self.NAT[:]
            # We monitor for duplicates, values sent by the NAT
            if self.NAT[1] in self.NAT_seen:
                print("Duplicate Y:", self.NAT[1])
                raise StopIteration
            self.NAT_seen.add(self.NAT[1])

# Part 1
print("-- Part 1 --")
network=Network(lines[0], 50)
while (not network.NAT):
    network.run()
print("First Y:", network.NAT[1])

# Part 2
print("-- Part 2 --")
while True:
    try:
        network.run()
    except:
        break

