from typing import Callable
from utils import random_node, neighbors

def hill_climbing(f:Callable, lowest: list, highest: list, Δ: float, first=None) -> list:
    points = []
    
    if not first:
        first = random_node(lowest, highest)
    current = first

    while True:
        neighbor = current
        for candidate_neighbor in neighbors(current, Δ):
            if f(candidate_neighbor) > f(neighbor):
                neighbor = candidate_neighbor
        if f(neighbor) <= f(current):
            return current, points
        current = neighbor
        points.append(current)