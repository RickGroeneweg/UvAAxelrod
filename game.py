
import numpy as np
from .payoff_functions import reward, sucker, temptation, punishment
from .country import *
from .action import Action, Outcome, to_outcome
from geopy import distance

R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P

class SelfGame:
    def __init__(self, country):
        self.country = country
        self.reward = reward(self.country, self.country, 1000) #distance of a country and itself?
    def play(self):
        self.country.fitness = self.country.fitness + self.reward

class Game:
    '''Here the values of payoff functions are stored'''

    def __init__(self, country1, country2):

        self.country1 = country1
        self.country2 = country2

        self.distance = distance.distance(self.country1.loc, self.country2.loc).km

        #parameters of the game
        self.reward1 = reward(self.country1, self.country2,self.distance)
        self.reward2 = reward(self.country2, self.country1,self.distance)
        self.temptation1 = temptation(self.country1, self.country2,self.distance)
        self.temptation2 = temptation(self.country2, self.country1,self.distance)
        self.sucker1 = sucker(self.country1, self.country2,self.distance)
        self.sucker2 = sucker(self.country2, self.country1,self.distance)
        self.punishment1 = punishment(self.country1, self.country2,self.distance)
        self.punishment2 = punishment(self.country1, self.country2,self.distance)

    def __str__(self):
        return self.country1.name + " vs " + self.country2.name


    def play(self): #should this function really return something
        '''returns moves the countries make, and update attributes'''
        move_country1 = self.country1.strategy(self.country1, self.country2) #*kwargs?
        move_country2 = self.country2.strategy(self.country2, self.country1)

        outcome = to_outcome(move_country1, move_country2)
        self.country1.outcomeDict[outcome[0]] += 1
        self.country2.outcomeDict[outcome[1]] += 1


        self.country1.moves.append(move_country1)
        self.country2.moves.append(move_country2)
        self.country1.history.append(outcome[0])
        self.country2.history.append(outcome[1])

        (self.country1.fitness, self.country2.fitness) = self.update_fitness(outcome[0])

        return (move_country1, move_country2)


    def update_fitness(self, outcome_for_countr1):
        '''updates the fitness of the two countries after a game'''
        if outcome_for_countr1 == Outcome.R:
            return (self.country1.fitness + self.reward1, self.country2.fitness + self.reward2)
        elif outcome_for_countr1 == Outcome.P:
            return (self.country1.fitness + self.punishment1, self.country2.fitness + self.punishment2)
        elif outcome_for_countr1 == Outcome.T:
            return (self.country1.fitness + self.temptation1, self.country2.fitness + self.sucker2)
        elif outcome_for_countr1 == Outcome.S:
            return (self.country1.fitness + self.sucker1, self.country2.fitness + self.temptation2)
        else:
            raise Exception("outcome_for_countr1 has not got the right format")
