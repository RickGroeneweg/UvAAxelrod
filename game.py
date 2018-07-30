import numpy as np
from .action import *
from .payoff_functions import reward, sucker, temptation, punishment, selfreward
from .strategies import *
#from .country import *

from geopy import distance
from math import sqrt, log

R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P
Cooperate, Defect, TitForTat, Grudge, RandomMove, Alternate, GenerousTFT = Strat.Cooperate, Strat.Defect, Strat.TitForTat,Strat.Grudge, Strat.RandomMove, Strat.Alternate, Strat.GenerousTFT

class SelfGame:
    def __init__(self, country, distance_function = lambda x: x):
        self.country = country
        self.distance = sqrt(self.country.area)
        self.fdistance = distance_function(self.distance)
        self.reward = selfreward(self.country, self.fdistance) #distance of a country and itself?

    def play(self):
        self.country.fitness = self.country.fitness + self.reward

class Game:
    '''Here the values of payoff functions are stored, and the history'''

    def __init__(self, country1, country2, distance_function = lambda x: x):

        self.country1 = country1
        self.country2 = country2

        self.distance = distance.distance(self.country1.loc, self.country2.loc).km
        self.fdistance = distance_function(self.distance)

        #parameters of the game
        self.reward1 = reward(self.country1, self.country2,self.fdistance)
        self.reward2 = reward(self.country2, self.country1,self.fdistance)
        self.temptation1 = temptation(self.country1, self.country2,self.fdistance)
        self.temptation2 = temptation(self.country2, self.country1,self.fdistance)
        self.sucker1 = sucker(self.country1, self.country2,self.fdistance)
        self.sucker2 = sucker(self.country2, self.country1,self.fdistance)
        self.punishment1 = punishment(self.country1, self.country2,self.fdistance)
        self.punishment2 = punishment(self.country1, self.country2,self.fdistance)

        self.country1moves = []
        self.country2moves = []

    def __str__(self):
        return self.country1.name + " vs " + self.country2.name


    def play(self, surveillancePenalty = False): #should this function really return something
        '''returns moves the countries make, and update attributes'''
        move_country1 = self.country1.strategy(self) #**kwargs?
        move_country2 = self.country2.strategy(self)


        outcome = to_outcome(move_country1, move_country2)
        self.country1.outcomeDict[outcome[0]] += 1
        self.country2.outcomeDict[outcome[1]] += 1


        self.country1moves.append(move_country1)
        self.country2moves.append(move_country2)

        (self.country1.fitness, self.country2.fitness) = self.update_fitness(outcome[0], surveillancePenalty = surveillancePenalty)




    def update_fitness(self, outcome_for_countr1, surveillancePenalty = False):
        '''updates the fitness of the two countries after a game'''


        if outcome_for_countr1 == Outcome.R:
            fitnessChange1 = self.reward1
            fitnessChange2 = self.reward2
        elif outcome_for_countr1 == Outcome.P:
            fitnessChange1 = self.punishment1
            fitnessChange2 = self.punishment2
        elif outcome_for_countr1 == Outcome.T:
            fitnessChange1 = self.temptation1
            fitnessChange2 = self.sucker2
        elif outcome_for_countr1 == Outcome.S:
            fitnessChange1 = self.sucker1
            fitnessChange2 = self.temptation2
        else:
            raise Exception("outcome_for_countr1 has not got the right format")

        if surveillancePenalty:
            surveillancePenaltyDict = surveillancePenaltyDict = {Cooperate: 1, Defect: 1, TitForTat: 0.95, Grudge: 0.95, RandomMove: 1, Alternate: 1, GenerousTFT: 0.95, WinStayLoseShift:1}
            fitnessChange1 = (fitnessChange1*surveillancePenaltyDict[self.country1.strategy.strat_enum])
            fitnessChange2  = (fitnessChange2*surveillancePenaltyDict[self.country2.strategy.strat_enum])


        updatedFitnessTuple = (self.country1.fitness + fitnessChange1, self.country2.fitness + fitnessChange2)

        return updatedFitnessTuple
