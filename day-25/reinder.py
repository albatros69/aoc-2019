#! /usr/bin/env python

from intcode import IntCode
from itertools import combinations

with open('input') as f:
    lines = list(f)

def ascii_code(routine):
    return list(ord(c) for c in map(str, routine))


class Robot():
    program=None
    waiting_input=False
    prompt='Command?'
    list_cmds=None
    last_outputs=None

    def __init__(self, line, input) -> None:
        self.program = IntCode(line.split(','), inputs=input)
        self.last_outputs=''
        self.list_cmds=[]

    def handle_output(self):
        if self.program.outputs:
            output = ''.join(chr(c) if c<=255 else str(c) for c in self.program.outputs)
            print(output,end='')
            self.last_outputs+=output
            self.last_outputs=self.last_outputs[-8:]
            if self.last_outputs==self.prompt:
                self.waiting_input=True
        self.program.outputs.clear()


    def run(self):
        while not self.program.finished:
            self.program.run()
            self.handle_output()
            if self.waiting_input:
                self.waiting_input=False
                if CMDS:
                    command = CMDS.pop(0)
                    print(command)
                else:
                    command=input(" ")
                if command=='PRINT':
                    print(self.list_cmds)
                    break
                else:
                    self.list_cmds.append(command)
                    self.program.inputs=ascii_code(command)+[10]
        print()

    def print_screen(self):
        for y in reversed(range(self.height)):
            print(''.join( self.area[x,y] for x in range(self.width)))


CMDS = ['north', 'north', 'take mutex', 'east', 'take tambourine', 'south', 'south', 'north', 'north',
    'east', 'west', 'west', 'south', 'south', 'west', 'west', 'take loom', 'east', 'east', 'north',
    'west', 'take antenna', 'south', 'take hologram', 'west', 'take astronaut ice cream', 'east',
    'south', 'take mug', 'north', 'north', 'north', 'north', 'north', 'take space heater', 'north', 'east', 'east' ]

ITEMS = [ 'mutex', 'loom', 'tambourine', 'hologram', 'space heater', 'antenna', 'astronaut ice cream', 'mug', ]

DROP_ALL = [ f'drop {i}' for i in ITEMS ]

for size in range(1, 9):
    for subset in combinations(ITEMS, size):
        CMDS.extend(DROP_ALL)
        CMDS.extend([ f'take {i}' for i in subset ])
        CMDS.append('east')

robot = Robot(lines[0], [])
robot.run()
