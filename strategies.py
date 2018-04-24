from .country import *
from .action import *
import random

C, D = Action.C, Action.D

def collaborate(country1, country2):
    return C
def defect(country1, country2):
    return D
def tit_for_tat(country1, country2):
    if country2.moves == []: # not country2.moves more efficient, but needs checking
        return C
    else: return country2.moves[-1]
def grudge(country1, country2):
    if country1.moves == [] or country2.moves == []: return C
    elif country2.moves[-1] == D or country1.moves[-1] == D:
        return D
    else: return C
def random_move(country1, country2):
    rnd = random.getrandbits(1)
    if rnd == 0:
        return C
    else: return D
def alternate(country1, country2):
    if country1.moves == []:
        return C
    elif country1.moves[-1] == C:
        return D
    else: return C
