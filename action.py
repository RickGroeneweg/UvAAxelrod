from enum import Enum
import random

class Action(Enum): #C for Collaborate, D for Defect
    C=1
    D=0

    def stoc(self): #to do:add option for different probabilities
        if bool(random.getrandbits(1)):
            if self == Action.C:
                return Action.D
            else:
                return Action.C
        else:
            return self


class Outcome(Enum): #R for Reward, T for Temptation, S for Sucker, P for Penalty
    R=0
    T=1
    S=2
    P=3

class PlottingVariable(Enum):
    M = 0
    Fitness = 1
    FitnessChange = 2
    Strategy = 3

class Strat(Enum):
    Collaborate = 0
    Defect = 1
    TitForTat = 2
    Grudge =3
    RandomMove = 4
    Alternate = 5

    def __str__(self):
        return self.name

def to_outcome(act1, act2):
    '''from inputs (Action, Action), outputs (Outcome, Outcome)'''
    C, D = Action.C, Action.D
    R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P
    dicti = {(C, C): (R,R), (C,D): (S, T), (D,C): (T,S), (D,D): (P,P) }
    return dicti[(act1,act2)]
