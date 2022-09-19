import random
import plotly.express as px
from math import exp

from utils import random_node
from algorithms import first_choice_hill_climbing, hill_climbing, simulated_annealing

random.seed(42)

def f(node):
    aux = lambda x,y: 4*exp(-(x**2 + y**2 - 2*(x+y-1))) + \
        exp(-((x-3)**2 + (y-3)**2)) + \
        exp(-((x+3)**2 + (y-3)**2)) + \
        exp(-((x-3)**2 + (y+3)**2)) + \
        exp(-((x+3)**2 + (y+3)**2))
    return aux(*node)

lowest = (-5, -5)
highest = (5, 5)
Δ = 1e-2

first = random_node(lowest, highest)

sa, pt_sa = simulated_annealing(f, lowest=lowest, highest=highest, Δ=Δ, max_iter=10000, T0=1, first=first)
hc, pt_hc = hill_climbing(f, lowest=lowest, highest=highest, Δ=Δ, first=first)
fc, pt_fc = first_choice_hill_climbing(f, lowest=lowest, highest=highest, Δ=Δ, max_iter=10000, first=first)

import pandas as pd
df_sa = pd.DataFrame(pt_sa, columns=['x', 'y'])
df_fc = pd.DataFrame(pt_fc, columns=['x', 'y'])
df_hc = pd.DataFrame(pt_hc, columns=['x', 'y'])

df_sa['algorithm'] = 'Simulated Annealing'
df_fc['algorithm'] = 'First-Choice Hill Climbing'
df_hc['algorithm'] = 'Hill Climbing'

df = pd.concat([df_sa, df_fc, df_hc], ignore_index=True)
fig = px.scatter(x=df['x'], y=df['y'], color=df['algorithm'])

fig.update_yaxes(scaleratio = 1)
fig.show()