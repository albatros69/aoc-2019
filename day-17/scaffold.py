#! /usr/bin/env python

import sys
from itertools import product
from collections import defaultdict, namedtuple, deque
from copy import deepcopy
from intcode import IntCode


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))


directions={ '^':(0,-1), 'v':(0,1), '<':(-1,0), '>':(1,0), }
def add(point, dir):
    return (point[0]+directions[dir][0], point[1]+directions[dir][1])

rev_dir = { '^':'v', 'v':'^', '<':'>', '>':'<', }
def rev(dir):
    if isinstance(dir, tuple):
        return (-dir[0],-dir[1])
    elif dir in rev_dir:
        return rev_dir[dir]
    else:
        return '-'

def ascii_code(routine):
    return list(ord(c) for c in ','.join(map(str, routine)))

def is_prefix(prefix, function):
    if function==[]: # an empty function is OK for any prefix (if it later becomes this prefix)
        return True
    elif len(prefix)>len(function):
        return False
    else:
        return all(v==function[i] for i,v in enumerate(prefix[:-1])) and prefix[-1]<=function[len(prefix)-1]


transitions = { '^>': ['R'], '^<': ['L'], 'v>': ['L'], 'v<': ['R'],
                '>^': ['L'], '>v': ['R'], '<^': ['R'], '<v': ['L'], }
def translate_path(path, direction=None):
    if not path:
        return []

    routine=[]
    if not direction:
        direction=path[0]
    forward=0
    for dir in path:
        if dir != direction:
            if forward:
                routine.append(forward)
            forward=1
            routine.extend(transitions[direction+dir])
        else:
            forward+=1
        direction=dir
    else:
        if forward:
            routine.append(forward)
    return routine

State=namedtuple('State', ('position', 'direction', 'seen', 'main_routine', 'functions', 'prefix'))

class Robot():
    program=None
    area=None
    droid=0,0
    direction=0
    height=0
    width=0

    def __init__(self, line) -> None:
        self.program = IntCode(line.split(','), inputs=[self.direction+1])
        self.area = defaultdict(lambda: '.')

    def handle_output(self, output):
        dust = None

        i=j=0
        for c in output:
            if c>255:
                dust=c
                continue
            if c==10:
                self.width=max(i, self.width)
                j+=1; i=0
                continue
            elif chr(c) in directions:
                self.direction=chr(c)
                self.droid=(i,j)

            self.area[i,j]=chr(c)
            i+=1
        self.height=j-1

        return dust

    def move_robot(self):
        self.program.inputs=[self.direction+1]

    def run(self):
        while not self.program.finished:
            self.program.run()

        return self.handle_output(self.program.outputs)

    def list_intersections(self):
        result=[]
        for pt in product(range(self.width), range(self.height)):
            neigh=tuple(self.area[add(pt, dir)]=='#' for dir in directions)
            if self.area[pt]=='#' and all(neigh):
                result.append(pt)
        return result

    def routines(self):
        stack=deque([State(position=self.droid, direction=self.direction, seen=set((self.droid,)), main_routine=[], functions={'A':[], 'B':[], 'C':[]}, prefix=[])])
        field=set((x,y) for (x,y) in self.area if self.area[x,y] in ('#', '^'))

        while stack:
            state = stack.popleft()

            if state.position[1]==0 and 2*len(state.main_routine)-1<=20 and all(len(ascii_code(f))<=20 for f in state.functions.values()) and state.seen==field:
                for f in state.functions:
                    if state.prefix==state.functions[f]:
                        return state.main_routine+[f], state.functions

            if 2*len(state.main_routine)-1>20 or any(len(ascii_code(f))>20 for f in state.functions.values()) or len(ascii_code(state.prefix))>20:
                continue
            else:
                for dir in directions:
                    new_pos = add(state.position, dir)
                    if new_pos[1]==0 and 2*len(state.main_routine)-1<=20 and all(len(ascii_code(f))<=20 for f in state.functions.values()) and state.seen==field:
                        state.prefix[-1]+=1
                        for f in state.functions:
                            if state.prefix==state.functions[f]:
                                return state.main_routine+[f], state.functions

                    elif (self.area[new_pos]=='#') and dir!=rev(state.direction):
                        if dir==state.direction:
                            new_prefix=state.prefix[:]
                            new_prefix[-1]+=1
                            if any(is_prefix(new_prefix, f) for f in state.functions.values()):
                                stack.appendleft(State(new_pos, dir, state.seen|set((new_pos,)), state.main_routine[:], deepcopy(state.functions), new_prefix ))

                        else:
                            for f in state.functions:
                                new_functions=deepcopy(state.functions)
                                new_routine = state.main_routine[:]
                                if state.prefix!=[] and state.functions[f]==[]:
                                    new_functions[f]=state.prefix[:]
                                    new_routine+=[f]
                                    new_prefix=transitions[state.direction+dir]+[1]
                                    stack.append(State(new_pos, dir, state.seen|set((new_pos,)), new_routine, new_functions, new_prefix))
                                    break

                                elif state.prefix!=[] and state.functions[f]==state.prefix:
                                    new_routine+=[f]
                                    new_prefix=transitions[state.direction+dir]+[1]
                                    stack.appendleft(State(new_pos, dir, state.seen|set((new_pos,)), new_routine, new_functions, new_prefix))

                            new_prefix=state.prefix[:]+transitions[state.direction+dir]+[1]
                            if len(ascii_code(new_prefix))<=20 and any(is_prefix(new_prefix, f) for f in state.functions.values()):
                                stack.append(State(new_pos, dir, state.seen|set((new_pos,)), state.main_routine[:], deepcopy(state.functions), new_prefix))

        return None, None

    def print_screen(self):
        for y in reversed(range(self.height)):
            print(''.join( self.area[x,y] for x in range(self.width)))

# Part 1
print("-- Part 1 --")
robot = Robot(lines[0])
robot.run()
print("Alignements parameters:", sum(x*y for (x,y) in robot.list_intersections()))

# Part 2
print("-- Part 2 --")
main_routine, functions=robot.routines()
input=ascii_code(main_routine) + [10]
for f in functions.values():
    input+=ascii_code(f)+[10]
input+=ascii_code(('n', '\n',))

robot = Robot(lines[0])
robot.program.memory[0]=2 # we wake up the droid
robot.program.inputs = input
print("Dust quantity:", robot.run())
