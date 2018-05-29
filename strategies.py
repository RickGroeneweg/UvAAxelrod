from enum import Enum
from .action import *




class Strat(Enum):
    Collaborate = 0
    Defect = 1
    TitForTat = 2
    Grudge =3
    RandomMove = 4
    Alternate = 5
    GenerousTFT = 6
    WinStayLoseShift = 7
    Contrite = 8

    def toFunction(self):
        functioDict = {Collaborate: collaborate, Defect: defect, TitForTat: tit_for_tat, Grudge: grudge, RandomMove: random_move, Alternate: alternate, GenerousTFT: generoustft, WinStayLoseShift: win_stay_lose_shift, Contrite: contrite_titfortat}
        return functioDict[self]

    def __str__(self):
        return self.name

C, D = Action.C, Action.D
Collaborate, Defect, TitForTat, Grudge, RandomMove, Alternate, GenerousTFT, WinStayLoseShift,  = Strat.Collaborate, Strat.Defect, Strat.TitForTat,Strat.Grudge, Strat.RandomMove, Strat.Alternate, Strat.GenerousTFT, Strat.WinStayLoseShift
Contrite = Strat.Contrite

DefaultNoise = 0.1

class Strategy:
    def __init__(self, strat_enum, function, country, noise = DefaultNoise):
        self.strat_enum = strat_enum
        self.function = function
        self.country = country
        self.noise = noise

    def __str__(self):
        return "<" + str(self.strat_enum) + " by " + str(self.country) + ">"

    def __call__(self, game):
        switchPerspective = (self.country == game.country2 )
        if switchPerspective:
            selfmoves = game.country2moves
            othermoves = game.country1moves
        elif (self.country == game.country1):
            selfmoves= game.country1moves
            othermoves = game.country2moves
        else:
            raise Exeption



        return self.function(selfmoves, othermoves, noise = self.noise)


def collaborate(selfmoves, othermoves, noise=DefaultNoise):
    '''Only collaborates'''
    return C.stoc(noise)

def defect(selfmoves, othermoves, noise=DefaultNoise):
    '''Only defects'''
    return D.stoc(noise)


def tit_for_tat(selfmoves, othermoves, noise=DefaultNoise):
    '''Starts the match by collaborating, then plays the move the opponent played last turn'''
    if othermoves == []: # not country2.moves more efficient, but needs checking
        return C.stoc(noise)
    else: return othermoves[-1].stoc(noise)


def generoustft(selfmoves, othermoves, noise=DefaultNoise):
    if othermoves == []: # not country2.moves more efficient, but needs checking
        return C.stoc(noise)
    elif othermoves[-1] == C:
        return C.stoc(noise)
    else:
        return D.stoc(0.3).stoc(noise)


def grudge(selfmoves, othermoves, noise=DefaultNoise): #DOES NOT WORK
    #Starts collaborating, but once the opponent defects, it will defect for the rest of the match #need thinking about noise
    raise Exeption("Ask Vaclav how grudge should deal with noise")
    if selfmoves == [] or othermoves == []: return C.stoc(noise)
    elif country2.moves[-1] == D or country1.moves[-1] == D:
        return D.stoc(noise)
    else: return C.stoc(noise)


def random_move(selfmoves, othermoves, noise=DefaultNoise):
    #returns a random move with uniform distribution
    rnd = np.random.binomial(1,1/2)
    if rnd == 0:
        return C.stoc(noise)
    else: return D.stoc(noise)


def alternate(selfmoves, othermoves, noise=DefaultNoise):
    #alternates between collaborating dan defecting
    if selfmoves == []:
        return C.stoc(noise)
    elif selfmoves[-1] == C:
        return D.stoc(noise)
    else: return C.stoc(noise)


def win_stay_lose_shift(selfmoves, othermoves, noise=DefaultNoise):
    if selfmoves ==[]:
        return C.stoc(noise)
    elif othermoves[-1]==selfmoves[-1]:
        return C.stoc(noise)
    else:
        return D.stoc(noise)


def contrite_titfortat(selfmoves,othermoves, noise= DefaultNoise):
    if len(country1.moves <= 1):
        return tit_for_tat(selfmoves,othermoves, noise = noise)
    elif selfmoves[-2] == D and othermoves[-2] == C:
        return C
    else:
        return tit_for_tat(selfmoves, othermoves)

#HOW TO ADD A STRATEGY
#-create a new Strat(Enum) in action.py
#-add strategy to this file, following the syntax of the other strategies
#-add the strategy to the Tournament class, instance attribute strategyList
#-add strategy to surveillancePenaltyDict in the Game class
