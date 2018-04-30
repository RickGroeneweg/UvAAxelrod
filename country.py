from .action import Outcome
from .strategies import *

R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P

class Country:
    '''All features of countries are stored here'''

    def __init__(self, name, m, loc, e, i, strategy):
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
        self.outcomeDict = {R: 0, T: 0, S: 0, P: 0}
        self.evolution = [(0, self.strategy.name())]

    def __str__(self):
        return self.name

    @classmethod
    def Country_w_random_strategy(cls, strategies = []):
        pass

    def country_reset(self, initFitness=0):
        self.fitness = initialFitness
        self.fitnessHistory = [self.fitness]
        self.moves= []
        self.hitory = []
        self.outcomeDict = {R: 0, T: 0, S: 0, P: 0}
        self.evolution = [(0, str(self.strategy))]
