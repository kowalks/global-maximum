import random
from math import pi, sin, cos

def neighbors(node, delta):
    for i in range(len(node)):
        for inc in [+delta, -delta]:
            new_node = list(node)
            new_node[i] = node[i] + inc
            yield tuple(new_node)

def random_neighbors(node, delta):
    while True:
        angle = random.random()*2*pi
        inc = [cos(angle), sin(angle)]
        new_node = [el + i*delta for el,i in zip(node,inc)]
        yield new_node