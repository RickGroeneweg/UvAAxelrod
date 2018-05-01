from .country import *
from .action import *
import random
import functools

C, D = Action.C, Action.D
Collaborate, Defect, TitForTat, Grudge, RandomMove, Alternate = Strat.Collaborate, Strat.Defect, Strat.TitForTat,Strat.Grudge, Strat.RandomMove, Strat.Alternate


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
def collaborate(country1, country2):
    '''Only collaborates'''
    return C

@give_strat(Defect)
def defect(country1, country2):
    '''Only defects'''
    return D

@give_strat(TitForTat)
def tit_for_tat(country1, country2):
    '''Starts the match by collaborating, then plays the move the opponent played last turn'''
    if country2.moves == []: # not country2.moves more efficient, but needs checking
        return C
    else: return country2.moves[-1]

@give_strat(Grudge)
def grudge(country1, country2):
    '''Starts collaborating, but once the opponent defects, it will defect for the rest of the match'''
    if country1.moves == [] or country2.moves == []: return C
    elif country2.moves[-1] == D or country1.moves[-1] == D:
        return D
    else: return C

@give_strat(RandomMove)
def random_move(country1, country2):
    '''returns a random move with uniform distribution'''
    rnd = random.getrandbits(1)
    if rnd == 0:
        return C
    else: return D

@give_strat(Alternate)
def alternate(country1, country2):
    '''alternates between collaborating dan defecting'''
    if country1.moves == []:
        return C
    elif country1.moves[-1] == C:
        return D
    else: return C
