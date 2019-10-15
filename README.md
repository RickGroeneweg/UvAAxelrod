# UvA Axelrod 

## Simulating world traide relations based on the Axelrod tournament

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
% Not yet Noise
% Generous tit for tat not yet implemented

To run an fast tournament:
`tournament = Tournament.create_play_tournament(G8, 10, [cooperate, defect, tit_for_tat])`

The example above uses the G8 list of countries. Other parameters can be given to this method too, you should consult the dock string in the source code for that.

We draw a graph showing the evolution of the strategies

    draw_stack(tour, xSize = 40)

We draw a graph illustrating the change in fitness of the population

    draw_fitness_graph(tour, delta=True,wholePopulation=True,xSize=40)
