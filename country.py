from .action import Outcome

R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P

class Country:

    def __init__(self, name, m, loc, e, i, strategy):
        self.name = name
        self.m = m
        self.loc = loc
        self.e = e
        self.i = i
        self.fitness = 0
        self.moves = []
        self.history = []
        self.strategy = strategy #a function (self, opponent, **kwargs) -> [C,D]
        self.outcomeDict = {R: 0, T: 0, S: 0, P: 0}

    def __str__(self):
        return self.name
