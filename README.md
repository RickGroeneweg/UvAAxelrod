# UvAAxelrod

#first we import the UvAAxelrod module, as well as numpy and matplotlib
from UvAAxelrod import *
import numpy as np
import matplotlib.pyplot as plt

#we set a seed for reproducible results.
np.random.seed(265)

#we initialize a tournament using the list of all countries including the EU
tour = Tournament(*AllCountriesEU, initialFitnessEqualsM = True, rounds = 100, strategyList = [Defect,TitForTat,GenerousTFT,Cooperate])

#we set a strategy for each country in the tournament, here we assign them randomly using numpy
for country in tour.countries:
    tour.init_strategy(np.random.choice(tour.strategyList),country)

#we play the tournament using the .play method
tour.play(turns = 1, changingStrategy = True, mutationRate = 0.1, playingThemselves = True, playingEachOther = True, nrStrategyChanges = 1, distance_function = sqrt, surveillancePenalty = True)

#we draw a graph showing the evolution of the strategies
draw_stack(tour, xSize = 40)

#we draw a graph illustrating the change in fitness of the population
draw_fitness_graph(tour, delta=True,wholePopulation=True,xSize=40)
