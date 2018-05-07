from .action import Outcome
from .strategies import *

R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P

class Country:
    '''All features of countries are stored here'''

    def __init__(self, name, m, loc, e, i, strategy, area):
        self.name = name
        self.m = m
        self.loc = loc
        self.e = e
        self.i = i
        self.fitness = 0
        self.fitnessHistory = [0]
        self.moves = []
        self.history = []
        self.strategy = strategy #a function (self, opponent, **kwargs) -> [C,D]
        self.area = area
        self.outcomeDict = {R: 0, T: 0, S: 0, P: 0}
        self.evolution = [(0, self.strategy.name())]

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

    def init_strategy(self, strategy):
        self.strategy = strategy
        self.evolution = [(0,self.strategy.name())]

    def reset_after_tournament(self, strategy):
        self.fitness = 0
        self.fitnessHistory = [0]
        self.moves = []
        self.history = []
        self.strategy = strategy #a function (self, opponent, **kwargs) -> [C,D]
        self.outcomeDict = {R: 0, T: 0, S: 0, P: 0}
        self.evolution = [(0, self.strategy.name())]
