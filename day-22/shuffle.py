#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def deal_new(deck):
    deck.reverse()
    return deck

def cut(deck, N):
    return deck[N:]+ deck[:N]

def deal(deck, N):
    result=list(deck)
    j=0
    for v in deck:
        result[j]=v
        j=(j+N)%len(deck)
    return result

# for test files...
# deck=list(range(10007))
# for l in lines:
#     if l.startswith('cut'):
#         deck = cut(deck, int(l[4:]))
#     elif l.startswith('deal with'):
#         deck = deal(deck, int(l[20:]))
#     elif l=='deal into new stack':
#         deck = deal_new(deck)
#     # print(l, ':', *deck)
# print('Result:', *deck)

# Part 1
print("-- Part 1 --")
deck=list(range(10007))
for l in lines:
    if l.startswith('cut'):
        deck = cut(deck, int(l[4:]))
    elif l.startswith('deal with'):
        deck = deal(deck, int(l[20:]))
    elif l=='deal into new stack':
        deck = deal_new(deck)
print('Card 2019 position:', deck.index(2019))


# Part 2
# Obviously, considering the numbers given, the above strategy won't work...
# We have to redo the whole thing, bearing in mind that the shuffling is
# an affine function in a finite group

class Shuffle():
    size=0
    a=1
    b=0

    def __init__(self, size) -> None:
        self.size=size
        self.a=1
        self.b=0

    def deal_new(self):
        self.a=(-self.a)%self.size
        self.b=(-1-self.b)%self.size

    def cut(self, N):
        self.b=(self.b-N)%self.size

    def deal(self, N):
        self.a=(self.a*N)%self.size
        self.b=(self.b*N)%self.size

    def compose(self, other):
        self.a=(other.a*self.a)%self.size
        self.b=(other.a*self.b+other.b)%self.size
        return self

    def get_card_position(self, card):
        return (card*self.a+self.b)%self.size

    def get_card(self, position):
        invmod=pow(self.a, self.size-2, self.size)
        return ((position-self.b)*invmod) % self.size


print('-- Part 1 (bis) --')
deck = Shuffle(10007)
for l in lines:
    if l.startswith('cut'):
        deck.cut(int(l[4:]))
    elif l.startswith('deal with'):
        deck.deal(int(l[20:]))
    elif l=='deal into new stack':
        deck.deal_new()
print('Card 2019 position:', deck.get_card_position(2019))

print('-- Part 2 --')

# Quick exponentiating by squaring
def compose_n(shuffle, n):
    result=Shuffle(shuffle.size)
    if n==0:
        pass
    elif n==1:
        result.compose(shuffle)
    else:
        tmp = compose_n(shuffle, n//2)
        if n%2==0:
            result.compose(tmp).compose(tmp)
        else:
            result.compose(shuffle).compose(tmp).compose(tmp)
    return result

deck=Shuffle(119315717514047)
for l in lines:
    if l.startswith('cut'):
        deck.cut(int(l[4:]))
    elif l.startswith('deal with'):
        deck.deal(int(l[20:]))
    elif l=='deal into new stack':
        deck.deal_new()

loop=compose_n(deck, 101741582076661)
print('Card in position 2020:', loop.get_card(2020))
