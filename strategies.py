from .country import *
from .action import *
import random
import functools

C, D = Action.C, Action.D

def give_str (string):
    def function_with_str(f_without):
        class StrFunction:
            def __call__(self, *args, **kwargs):
                #return behaviour of function unchanged
                return f_without(*args, **kwargs)
            def __str__(self):
                return string
        return functools.wraps(function_with_str)(StrFunction())
    return function_with_str

@give_str("collaborate")
def collaborate(country1, country2):
    return C

@give_str("defect")
def defect(country1, country2):
    return D

@give_str("tit_for_tat")
def tit_for_tat(country1, country2):
    if country2.moves == []: # not country2.moves more efficient, but needs checking
        return C
    else: return country2.moves[-1]

@give_str("grudge")
def grudge(country1, country2):
    if country1.moves == [] or country2.moves == []: return C
    elif country2.moves[-1] == D or country1.moves[-1] == D:
        return D
    else: return C
@give_str("random_move")
def random_move(country1, country2):
    rnd = random.getrandbits(1)
    if rnd == 0:
        return C
    else: return D

@give_str("alternate")
def alternate(country1, country2):
    if country1.moves == []:
        return C
    elif country1.moves[-1] == C:
        return D
    else: return C
