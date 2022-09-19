from typing import Callable
from utils import random_neighbors, random_node

def first_choice_hill_climbing(f:Callable, lowest: list, highest: list, Δ: float, max_iter=100, first=None) -> list:
    points = []
    
    if not first:
        first = random_node(lowest, highest)
    current = first

    iterations = 0
    neighbor = current
    while iterations < max_iter:
        for candidate_neighbor in random_neighbors(current, Δ):
            iterations += 1
            if iterations > max_iter:
                break
            if f(candidate_neighbor) > f(neighbor):
                neighbor = candidate_neighbor
                break
        if f(neighbor) <= f(current):
            return current, points
        current = neighbor
        points.append(current)

    return current, points