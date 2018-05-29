from .action import *
from .strategies import Strategy

R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P

class Country:
    '''All features of countries are stored here'''

    def __init__(self, name, m, loc, e, i, area):
        self.name = name
        self.m = m
        self.loc = loc
        self.e = e
        self.i = i
        self.fitness = 0
        self.fitnessHistory = [0]
        self.history = []
        self.strategy = None
        self.area = area
        self.outcomeDict = {R: 0, T: 0, S: 0, P: 0}
        self.evolution = []

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

    def init_strategy(self, strat_enum, noise = 0.0):
        function = strat_enum.toFunction()
        self.strategy = Strategy(strat_enum, function, self)
        self.evolution = [(0,self.strategy.strat_enum)]

    def reset_after_tournament(self, strategy):
        self.fitness = 0
        self.fitnessHistory = [0]
        self.history = []
        self.strategy = None #a function (self, opponent, **kwargs) -> [C,D]
        self.outcomeDict = {R: 0, T: 0, S: 0, P: 0}
        self.evolution = []
