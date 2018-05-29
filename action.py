from enum import Enum
import numpy as np

#import random

class Action(Enum): #C for Collaborate, D for Defect
    C=1
    D=0

    def stoc(self, probability): #to do:add option for different probabilities
        if bool(np.random.binomial(1, probability)):
            if self == Action.C:
                return Action.D
            else:
                return Action.C
        else:
            return self
    def __str__(self):
        return self.name



class Outcome(Enum): #R for Reward, T for Temptation, S for Sucker, P for Penalty
    R=0
    T=1
    S=2
    P=3

    def switch(self):
        switchDict = {Outcome.R: Outcome.R, Outcome.T: Outcome.S, Outcome.S: Outcome.T, Outcome.P: Outcome.P}
        return switchDict[self]




class PlottingVariable(Enum):
    M = 0
    Fitness = 1
    FitnessChange = 2
    Strategy = 3


def to_outcome(act1, act2):
    '''from inputs (Action, Action), outputs (Outcome, Outcome)'''
    C, D = Action.C, Action.D
    R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P
    dicti = {(C, C): (R,R), (C,D): (S, T), (D,C): (T,S), (D,D): (P,P) }
    return dicti[(act1,act2)]
