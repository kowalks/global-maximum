import random

def random_node(lowest, highest):
    return tuple(random.uniform(l, w) for l,w in zip(lowest, highest))