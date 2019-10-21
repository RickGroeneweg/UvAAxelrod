# UvA Axelrod 

## Simulating world trade relations based on the Axelrod tournament

Quick Start Guide

This package is written in Python, using libraries: NumPy, GeoPy, NetworkX which
should be installed.

First Create a Jupyter notebook in the directory that also contains the `UvAAxelrod` folder.
In this notebook we can import the package as follows:
```
    from UvAAxelrod import *
    import numpy as np
    import matplotlib.pyplot as plt

    np.random.seed(265)
``` 


% Unit test not yet runnable

To run an fast tournament:
`tournament = Tournament.create_play_tournament(G8, 100, [cooperate, defect, tit_for_tat])`

The example above uses the G8 list of countries. Other parameters can be given to this method too, you should consult the dock string in the source code for that.

We draw a graph showing the evolution of the strategies

    draw_stack(tour, xSize = 40)

We draw a graph illustrating the change in fitness of the population

    draw_fitness_graph(tour, delta=True,wholePopulation=True,xSize=40)
    
    
## Self reward
 
Countries can be set to receive fitness from their internal market. This is done by setting the `self_reward` parameter of the `Tournament.play` method equal to 
a function. The default value of this parameter in the `Tournament.create_play_tournament` method is defined in `payoff_functions.py`. If this parameter is set 
to `None`, then countries receive no fitness from their internal market.

## mini tutorial notebook:

Execute the following code sequentially in a notebook
```
from UvAAxelrod import *
```

```
# important to have the .csv files in the directory of this notebook
WTO_2017 = get_WTO_countries(2017)
```
```
tournament_2017 = Tournament.create_play_tournament(
                 countries=WTO_2017, 
                 max_rounds=400, 
                 strategy_list=[defect, tit_for_tat, generous_tit_for_tat, cooperate], 
                 payoff_functions=default_payoff_functions, 
                 distance_function = lambda d: d, # defaults to just the identity
                 surveillance_penalty = True,
                 self_reward = selfreward, #default function
                 playing_each_other=True,
                 nr_strategy_changes = 1,
                 mutation_rate =0.1,
                 init_fitnes_as_m=False,
                 noise = 0.05
                 )
```

```
C_D_ratios_per_round(tournament_2017)
```

```
outcome_ratios_per_round(tournament_2017)
```


```
draw_stack(tournament_2017)
```
