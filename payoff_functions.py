import math as m

# These functions are the suggested payoff_functions. That is, they 
# calculate how much fitness a country should  get/lose by
# playing a prisoners dilemma with another country. They are
# the default payoff functions, but in the Tournament instance you
# could specify to use other functions.

def selfreward(country):
    '''calculates how much reward a country gets from its own internal market'''
    return (1 - country.e)*country.m / country.d

def reward(country, other, d):
    '''calculates how much reward would change fitness'''
    return (country.e - country.i*other.e)*other.m / d

def temptation(country, other, d):
    '''calculates how much temptation would change fitness'''
    return country.e*other.m / d

def sucker(country, other, d):
    '''calculates how much sucker would change fitness'''
    return -country.i*other.e*other.m / d

def punishment(country, other, d):
    '''calculates how much punishment would chage fitness'''
    return 0

default_payoff_functions = {
        'R': reward,
        'T': temptation,
        'S': sucker,
        'P': punishment,
        'self_reward': selfreward
        }

# Ask Sebastian: can he confirm that these are the right values?
# in the traditional Axelrod tournament, payoffs are fixed for all participants
traditional_payoff_functions = {
        'R': lambda *args: 3,
        'T': lambda *args: 5,
        'S': lambda *args: 0,
        'P': lambda *args: 1
        }