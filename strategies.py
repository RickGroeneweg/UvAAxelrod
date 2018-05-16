from .country import *
from .action import *
#import random
import functools

C, D = Action.C, Action.D
Collaborate, Defect, TitForTat, Grudge, RandomMove, Alternate, GenerousTFT, WinStayLoseShift = Strat.Collaborate, Strat.Defect, Strat.TitForTat,Strat.Grudge, Strat.RandomMove, Strat.Alternate, Strat.GenerousTFT, Strat.WinStayLoseShift

DefaultNoise = 0.05

def give_strat (strat):
    '''A decorator function, that adds a Strat (Enum) method to a function object (like a strategy)'''
    def function_with_strat(f_without):
        class Function_w_name:
            def __call__(self, *args, **kwargs):
                #return behaviour of function unchanged
                return f_without(*args, **kwargs)
            def name(self):
                return strat
        return functools.wraps(function_with_strat)(Function_w_name())
    return function_with_strat

@give_strat(Collaborate)
def collaborate(country1, country2, noise=DefaultNoise):
    '''Only collaborates'''
    return C.stoc(noise)

@give_strat(Defect)
def defect(country1, country2, noise=DefaultNoise):
    '''Only defects'''
    return D.stoc(noise)

@give_strat(TitForTat)
def tit_for_tat(country1, country2, noise=DefaultNoise):
    '''Starts the match by collaborating, then plays the move the opponent played last turn'''
    if country2.moves == []: # not country2.moves more efficient, but needs checking
        return C.stoc(noise)
    else: return country2.moves[-1].stoc(noise)

@give_strat(Grudge)
def grudge(country1, country2, noise=DefaultNoise):
    '''Starts collaborating, but once the opponent defects, it will defect for the rest of the match''' #need thinking about noise
    if country1.moves == [] or country2.moves == []: return C.stoc(noise)
    elif country2.moves[-1] == D or country1.moves[-1] == D:
        return D.stoc(noise)
    else: return C.stoc(noise)

@give_strat(RandomMove)
def random_move(country1, country2, noise=DefaultNoise):
    '''returns a random move with uniform distribution'''
    rnd = np.random.binomial(1,1/2)
    if rnd == 0:
        return C.stoc(noise)
    else: return D.stoc(noise)

@give_strat(Alternate)
def alternate(country1, country2, noise=DefaultNoise):
    '''alternates between collaborating dan defecting'''
    if country1.moves == []:
        return C.stoc(noise)
    elif country1.moves[-1] == C:
        return D.stoc(noise)
    else: return C.stoc(noise)

@give_strat(GenerousTFT)
def generoustft(country1, country2, noise=DefaultNoise):
    if country2.moves == []: # not country2.moves more efficient, but needs checking
        return C.stoc(noise)
    elif country2.moves[-1] == C:
        return C.stoc(noise)
    else:
        return D.stoc(0.3).stoc(noise)

@give_strat(WinStayLoseShift)
def win_stay_lose_shift(country1, country2, noise=DefaultNoise):
    if country2.moves ==[]:
        return C.stoc(noise)
    elif country2.moves[-1]==country1.moves[-1]:
        return C.stoc(noise)
    else:
        return D.stoc(noise)

#HOW TO ADD A STRATEGY
#-create a new Strat(Enum) in action.py
#-add strategy to this file, following the syntax of the other strategies
#-add the strategy to the Tournament class, instance attribute strategyList
#-add strategy to surveillancePenaltyDict in the Game class
