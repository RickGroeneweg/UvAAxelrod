from .enums import Action
import numpy as np
# Defining possible strategyes.
# A strategy is simpy a function, with a name-attribute added to it.

C, D = Action.C, Action.D

def cooperate(*args):
    return C
cooperate.name = 'cooperate'

def defect(*args):
    return D
defect.name = 'defect'

def tit_for_tat(selfmoves, othermoves):
    if othermoves == []:
        # start friendly
        return C
    else:
        # do what the other did last turn
        return othermoves[-1]
tit_for_tat.name = 'tit_for_tat'

def generous_tit_for_tat(selfmoves, othermoves):
    if selfmoves == []:
        return C
    elif othermoves[-1] == C:
        # other cooperated last time
        return C
    else:
        # last time, oponent did not cooperate
        return np.random.choice([C, D], p=[0.3, 0.7])
generous_tit_for_tat.name = 'generous_tit_for_tat'

def win_stay_lose_shift(selfmoves, othermoves):
    if selfmoves ==[]:
        return C
    elif othermoves[-1]==selfmoves[-1]:
        return C
    else:
        return D
win_stay_lose_shift.name = 'win_stay_lose_shift'