#! /usr/bin/env python

import sys
from collections import defaultdict
from intcode import IntCode

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

class ArcadeCabinet():
    program=None
    tiles=None
    ball=0,0
    paddle=0,0
    score=0

    # 0 is an empty tile. No game object appears in this tile.
    # 1 is a wall tile. Walls are indestructible barriers.
    # 2 is a block tile. Blocks can be broken by the ball.
    # 3 is a horizontal paddle tile. The paddle is indestructible.
    # 4 is a ball tile. The ball moves diagonally and bounces off objects.
    textures = [ ' ', '#', '@', '_', 'o', ]

    def __init__(self, line) -> None:
        self.program = IntCode(line.split(','), inputs=[])
        self.tiles = defaultdict(int)

    def handle_output(self, x, y, tile_id):
        if x==-1 and y==0:
            self.score=tile_id
            return
        elif tile_id==3:
            self.paddle=x,y
        elif tile_id==4:
            self.ball=x,y
        self.move_paddle()

        self.tiles[x,y] = tile_id

    def move_paddle(self):
        if self.ball[0] > self.paddle[0]:
            self.program.inputs=[1]
        elif self.ball[0] < self.paddle[0]:
            self.program.inputs=[-1]
        else:
            self.program.inputs=[0]

    def run(self):
        while not self.program.finished:
            self.program.run()
            if not self.program.finished:
                self.handle_output(*self.program.outputs)
                self.program.outputs.clear()

    def print_screen(self):
        min_x, min_y=min(self.tiles.keys())
        max_x, max_y=max(self.tiles.keys())
        for y in range(min_y, max_y+1):
            print(''.join( self.textures[self.tiles[x,y]] for x in range(min_x, max_x+1)))
        print("Score:", self.score)


# Part 1
print("-- Part 1 --")
game = ArcadeCabinet(lines[0])
game.run()
game.print_screen()
print('nb blocks:', sum(game.tiles[x]==2 for x in game.tiles))

# Part 2
print("-- Part 2 --")
game = ArcadeCabinet(lines[0])
game.program.memory[0] = 2 # we cheat on our inserting coins
game.run()
game.print_screen()
