import random
from math import exp
from typing import Callable

from utils import random_node, random_neighbors

def simulated_annealing(f:Callable, lowest: list, highest: list, Δ: float, max_iter=1000, T0=5230, first=None):
    points = []
    
    if not first:
        first = random_node(lowest, highest)
    current = first
    schedule = (T0/(i+1) for i in range(max_iter))
    gen = random_neighbors(current, Δ)

    for temperature in schedule:
        if temperature == 0:
            return current, points
        next_node = next(gen)
        ΔE = f(next_node) - f(current)
        
        if ΔE > 0:
            current = next_node
            gen = random_neighbors(current, Δ)
            points.append(current)
        elif random.random() < exp(ΔE/temperature):
            current = next_node
            gen = random_neighbors(current, Δ)
            points.append(current)
    return current, points