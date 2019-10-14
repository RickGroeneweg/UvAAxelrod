from enums import Action
# Defining possible strategyes.
# A strategy is simpy a function, with a name-attribute added to it.
penalty_dict = ...

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

def generous_tit_for_tat(selfmvoes, othermoves):
    pass
