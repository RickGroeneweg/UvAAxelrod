from enum import Enum

class Action(Enum): #C for Collaborate, D for Defect
    C=1
    D=0


class Outcome(Enum): #R for Reward, T for Temptation, S for Sucker, P for Penalty
    R=0
    T=1
    S=2
    P=3

def to_outcome(act1, act2):
    '''from inputs (Action, Action), outputs (Outcome, Outcome)'''
    C, D = Action.C, Action.D
    R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P
    dicti = {(C, C): (R,R), (C,D): (S, T), (D,C): (T,S), (D,D): (P,P) }
    return dicti[(act1,act2)]
