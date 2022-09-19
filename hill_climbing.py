from ast import Call
import random
from math import exp, sqrt, pi, sin, cos
from typing import Callable
from itertools import product


def f(node):
    aux = lambda x,y: 4*exp(-(x**2 + y**2 - 2*(x+y-1))) + \
        exp(-((x-3)**2 + (y-3)**2)) + \
        exp(-((x+3)**2 + (y-3)**2)) + \
        exp(-((x-3)**2 + (y+3)**2)) + \
        exp(-((x+3)**2 + (y+3)**2))
    return aux(*node)


def neighbors(node, delta):
    for i in range(len(node)):
        for inc in [+delta, -delta]:
            new_node = list(node)
            new_node[i] = node[i] + inc
            yield tuple(new_node )

    values = [(dim+delta, dim-delta) for dim in node]
    return product(*values)

def random_neighbors(node, delta):
    while True:
        angle = random.random()*2*pi
        inc = [cos(angle), sin(angle)]
        new_node = [el + i*delta for el,i in zip(node,inc)]
        yield new_node

def random_node(lowest, highest):
    return tuple(random.uniform(l, w) for l,w in zip(lowest, highest))

pt_hc = []

def hill_climbing(f:Callable, lowest: list, highest: list, Δ: float, first=None) -> list:
    if not first:
        first = random_node(lowest, highest)
    current = first

    while True:
        neighbor = current
        for candidate_neighbor in neighbors(current, Δ):
            if f(candidate_neighbor) > f(neighbor):
                neighbor = candidate_neighbor
        if f(neighbor) <= f(current):
            return current
        current = neighbor
        pt_hc.append(current)

pt_fc = []

def first_choice_hill_climbing(f:Callable, lowest: list, highest: list, Δ: float, max_iter=100, first=None) -> list:
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
            return current
        current = neighbor
        pt_fc.append(current)

    return current

pt = []

def simulated_annealing(f:Callable, lowest: list, highest: list, Δ: float, max_iter=1000, T0=5230, first=None):
    if not first:
        first = random_node(lowest, highest)
    current = first
    schedule = (T0/(i+1) for i in range(max_iter))
    gen = random_neighbors(current, Δ)

    for temperature in schedule:
        if temperature == 0:
            return current
        next_node = next(gen)
        ΔE = f(next_node) - f(current)
        
        if ΔE > 0:
            current = next_node
            gen = random_neighbors(current, Δ)
            pt.append(current)
        elif random.random() < exp(ΔE/temperature):
            current = next_node
            gen = random_neighbors(current, Δ)
            pt.append(current)
    return current

random.seed(42)
lowest = (-5, -5)
highest = (5, 5)
# Δδ
Δ = 1e-2

first = random_node(lowest, highest)

max_sa = simulated_annealing(f, lowest=lowest, highest=highest, Δ=Δ, max_iter=10000, T0=1, first=first)
print(max_sa)
max_hc = hill_climbing(f, lowest=lowest, highest=highest, Δ=Δ, first=first)
print(max_hc)
max_fc_hc = first_choice_hill_climbing(f, lowest=lowest, highest=highest, Δ=Δ, max_iter=10000, first=first)
print(max_fc_hc)

import plotly.express as px

import pandas as pd
df_an = pd.DataFrame(pt, columns=['x', 'y'])
df_fc = pd.DataFrame(pt_fc, columns=['x', 'y'])
df_hc = pd.DataFrame(pt_hc, columns=['x', 'y'])
# fig.show()
# print(len(df))

df_an['algorithm'] = 'Simulated Annealing'
df_fc['algorithm'] = 'First-Choice Hill Climbing'
df_hc['algorithm'] = 'Hill Climbing'


df = pd.concat([df_an, df_fc, df_hc], ignore_index=True)
fig = px.scatter(x=df['x'], y=df['y'], color=df['algorithm'])#, range_y=(-1,2))

fig.update_yaxes(scaleratio = 1)
fig.show()