import numpy as np
import math
from itertools import combinations
import random
from math import sqrt

from .country import *
from .game import *
from .strategies import *
from .match import *
from .action import *

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.patches as mpatches


R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P
Collaborate, Defect, TitForTat, Grudge, RandomMove, Alternate = Strat.Collaborate, Strat.Defect, Strat.TitForTat,Strat.Grudge, Strat.RandomMove, Strat.Alternate

class Tournament:
    '''Here a tournament between all countries is played, consisting of matches between all countries'''

    def __init__(self, *countries, initialFitnessEqualsM = True, rounds = 2000, seed = 4):
        self.countries = list(countries)
        self.matches = {} #dict is easy but not efficient.. we'll see if performance becomes an issue,
        self.selfMatches = []
        self.rounds = rounds


        if initialFitnessEqualsM:
            for country in self.countries:
                country.fitness = country.m
                country.fitnessHistory = [country.fitness]
        self.initialFitness = [c.fitness for c in self.countries]

        self.changeInFitness = []

        size = len(self.countries)
        self.matchResultsMatrix = np.zeros((size, size))
        self.strategyList = [Collaborate, Defect, TitForTat, Grudge, RandomMove, Alternate]
        random.seed(seed)

    def reset_after_tournament(self): #not yet tested
        for country in self.countries:
            country.reset_after_tournament(collaborate)
        self.matches = {} #dict is easy but not efficient.. we'll see if performance becomes an issue,
        self.selfMatches = []
        if initialFitnessEqualsM:
            for country in self.countries:
                country.fitness = country.m
                country.fitnessHistory = [country.fitness]
        self.initialFitness = [c.fitness for c in self.countries]

        self.changeInFitness = []

        size = len(self.countries)
        self.matchResultsMatrix = np.zeros((size, size))

    def play(self, printing = True, turns = 12, changingStrategy = True, playingThemselves = False, nrStrategyChanges = 1, surveillanceLoss = False, distance_function = lambda x: x, surveillancePenalty = False):
        '''plays the tournament'''

        #we initialize the rewards countries get from there own internal market
        if playingThemselves:
            for country in self.countries:
                newSelfGame = SelfGame(country, distance_function = distance_function) #the distance is chose to be the sqrt of the area of the country
                newSelfMatch = SelfMatch(newSelfGame)
                self.selfMatches.append(newSelfMatch)


        #now we initialize all matches between countries
        all_combinations = list(combinations(range(len(self.countries)), 2)) #first one always lower
        for (a, b) in all_combinations:
            newGame = Game(self.countries[a], self.countries[b], distance_function = distance_function)
            newMatch = Match(newGame)
            self.matches[(a,b)]= newMatch



        #now the tournament starts
        for n in range(self.rounds):

            #first countries get rewards from there own internal market
            if playingThemselves:
                for i, selfMatch in enumerate(self.selfMatches):
                    selfMatch.play(turns = turns)
                    self.matchResultsMatrix[i,i] += selfMatch.changeInFitness

            #next the countries play against each other
            for (a,b), match in self.matches.items():
                match.play(turns = turns, surveillancePenalty = surveillancePenalty)
                (self.matchResultsMatrix[a, b], self.matchResultsMatrix[b, a]) = (self.matchResultsMatrix[a, b]+match.changeInFitness[0], self.matchResultsMatrix[b, a]+ match.changeInFitness[1])


            if changingStrategy:
                for _ in range(nrStrategyChanges):
                    self.change_a_strategy(n+1, printing = printing)

            for country in self.countries:
                country.fitnessHistory.append(country.fitness)

            if printing: print("Round {} of tournament played".format(n+1))



            if self.endOfEvolution(self.countries):
                print("The Process ended in {} rounds\n Winning strategy: {}".format(n+1, str(self.countries[0].strategy.name())))
                self.rounds = n+1 #is the +1 correct? need to test
                break;

        self.changeInFitness = [(a.fitness - b) for (a,b) in zip(self.countries, self.initialFitness)]

    @staticmethod
    def endOfEvolution(countries):
        strategy1 = str(countries[0].strategy)
        for country in countries[1:]:
            if str(country.strategy) != strategy1:
                return False
        print("All strategies are the same")
        return True

    def change_a_strategy(self, roundNum,  printing = True ):
        '''selects a random country to change it's strategy to a strategy of a country with a high fitness'''

        N = len(self.countries)

        #probabilites cannot be negative, so all negative fitnesses are pretended to be 0
        fitnessScores= [(country.fitness>0)*country.fitness for country in self.countries] #True ==1, False ==0

        total_fitness = sum(fitnessScores)
        probabilities = [fitnessScores[i]/total_fitness for i in range(N)]

        reproduce_index = np.random.choice(range(N), p=probabilities)
        eliminate_index = np.random.randint(N)

        losingCountry = self.countries[eliminate_index]
        winningCountry = self.countries[reproduce_index]
        losingStrategyStr = str(losingCountry.strategy.name())
        winningStrategyStr = str(winningCountry.strategy.name())

        losingCountry.evolution.append((roundNum, winningCountry.strategy.name()))

        losingCountry.strategy = winningCountry.strategy
        if printing:
            print("strategy " + losingCountry.__str__() + " (" + losingStrategyStr + ") "+ "changed to strategy " + winningCountry.__str__() + " (" + winningStrategyStr + ")")

    def get_payoff_value(self, country1, country2, outcome1):

        if country1 == country2:
            if outcome1 == R:
                index = self.countries.index(country1)
                return self.selfMatches[index].selfgame.reward
            else:
                raise Exception("A country only cooperates against itself")
        else:

            index1 = self.countries.index(country1)
            index2 = self.countries.index(country2)

            if index2<index1:
                #countries are given in the other order than their match is stored in self.mathces
                (country1, country2) = (country2, country1)
                (index1, index2) = (index2, index1)
                swapped = True
            else:
                swapped = False

            game = self.matches[(index1, index2)].game

            if outcome1 == R:
                if swapped:
                    return game.reward2
                else:
                    return game.reward1
            elif outcome1 == S:
                if swapped:
                    return game.sucker2
                else:
                    return game.sucker1
            elif outcome1 == T:
                if swapped:
                    return game.temptation2
                else:
                    return game.temptation1
            elif outcome1 == P:
                if swapped:
                    return game.punishment2
                else:
                    return game.punishment1
            else:
                raise Exception









    @staticmethod
    def init_strategy(strategy, *countries):
        for country in countries:
            country.init_strategy(strategy)
