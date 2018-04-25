import numpy as np
import math
from itertools import combinations
import random
from math import sqrt

from .country import *
from .game import *
from .strategies import *
from .match import *

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

R,T,S,P = Outcome.R, Outcome.T, Outcome.S, Outcome.P


def marker_size(country ,string, factor, change = 0):
    if string == "m":
        return 1.128 * sqrt(country.m* factor)
    elif string == "fit":
        return 1.128 * sqrt(country.fitness* factor)
    elif string == "change":
        return 1.128 * sqrt(change* factor)
    else: raise Exception


def marker_color(country, string, change = 0):
    if string == "m":
        return country.m
    elif string == "fit":
        return country.fitness
    elif string == "change":
        return change

def marker_style(string):
    mydict = {"collaborate": "o", "defect": "v", "tit_for_tat": "s", "grudge": "x", "random_move": "D", "alternate": "*"}
    return mydict[string]


def draw_pie(ax, lat, lon, outcomeDict, size=600): #to do: adjust for any number of strategies, replace to a better location in the code

    total = sum(outcomeDict.values())
    r1 = outcomeDict[R]/total
    r2 = r1 + outcomeDict[T]/total
    r3 = r2 + outcomeDict[S]/total

    x = [0] + np.cos(np.linspace(0, 2 * np.pi * r1, 10)).tolist()
    y = [0] + np.sin(np.linspace(0, 2 * np.pi * r1, 10)).tolist()
    xy1 = np.column_stack([x, y])
    s1 = np.abs(xy1).max()

    x = [0] + np.cos(np.linspace(2 * np.pi * r1, 2 * np.pi * r2, 10)).tolist()
    y = [0] + np.sin(np.linspace(2 * np.pi * r1, 2 * np.pi * r2, 10)).tolist()
    xy2 = np.column_stack([x, y])
    s2 = np.abs(xy2).max()

    x = [0] + np.cos(np.linspace(2 * np.pi * r2, 2 * np.pi * r3, 10)).tolist()
    y = [0] + np.sin(np.linspace(2 * np.pi * r2, 2 * np.pi * r3, 10)).tolist()
    xy3 = np.column_stack([x, y])
    s3 = np.abs(xy3).max()

    x = [0] + np.cos(np.linspace(2 * np.pi * r3, 2 * np.pi, 10)).tolist()
    y = [0] + np.sin(np.linspace(2 * np.pi * r3, 2 * np.pi, 10)).tolist()
    xy4 = np.column_stack([x, y])
    s4 = np.abs(xy4).max()

    ax.scatter(lon, lat, marker = (xy1, 0), s=s1 **2 * size, facecolor = 'green')
    ax.scatter(lon, lat, marker = (xy2, 0), s=s2 **2 * size, facecolor = 'red')
    ax.scatter(lon, lat, marker = (xy3, 0), s=s3 **2 * size, facecolor = 'blue')
    ax.scatter(lon, lat, marker = (xy4, 0), s=s4 **2 * size, facecolor = 'black')

class TournamentRound:

    def __init__(self, *countries):
        self.countries = list(countries)
        self.matches = {} #dict is easy but not efficient.. we'll see if performance becomes an issue
        self.initialFitness = [c.fitness for c in self.countries]
        self.changeInFitness = []

    def play(self, printing = True, turns = 12, rounds=1, changingStrategy = False):
        all_combinations = list(combinations(range(len(self.countries)), 2)) #first one always lower
        for n in range(rounds):
            for (a, b) in all_combinations:
                newGame = Game(self.countries[a], self.countries[b])
                newMatch = Match(newGame, turns = turns)
                newMatch.play(printing = printing)
                self.matches[(a,b)] = newMatch
                #here we could also safe some information about this round

            if changingStrategy:
                self.change_a_strategy(n+1, printing = printing)

            if printing: print("One round of tournament matches played")



#            if endOfEvolution:
#                print("process ended in {} rounds".format(n+1))

        self.changeInFitness = [(a.fitness - b) for (a,b) in zip(self.countries, self.initialFitness)]





    def fitness_change_matrix(self, countryNames, indices): #This method does not work for rounds>1, only solution I see is geting a matrix as an attribute
        size = len(countryNames)
        assert(size == len(indices))
        result = np.zeros((size, size))

        #this for-loop is a bit complex...
        for i in range(size-1):
            for j in range(i+1, size):
                indexi = indices[i]
                indexj = indices[j]
                if indexi > indexj: (indexi, indexj) = (indexj, indexi); (i,j)=(j,i) #this is needed if we select on countries
                (result[i,j],result[j,i]) = self.matches[(indexi, indexj)].changeInFitness

        return result

    def change_a_strategy(self, roundNum,  printing = True ):

        N = len(self.countries)

        total_fitness = sum([country.fitness for country in self.countries])
        probabilities = [country.fitness/total_fitness for country in self.countries]
        reproduce_index = np.random.choice(range(N), p=probabilities)

        eliminate_index = np.random.randint(N)

        losingCountry = self.countries[eliminate_index]
        winningCountry = self.countries[reproduce_index]
        losingStrategyStr = str(losingCountry.strategy)
        winningStrategyStr = str(winningCountry.strategy)

        losingCountry.evolution.append((roundNum, winningStrategyStr))

        losingCountry.strategy = winningCountry.strategy
        if printing:
            print("strategy " + losingCountry.__str__() + " (" + losingStrategyStr + ") "+ " changed to strategy " + winningCountry.__str__() + " (" + winningStrategyStr + ")")

    def draw_evo(self, rounds, cmap = 'CMRmap'):

        valueDict = {"collaborate": 1, "defect": 2, "tit_for_tat": 3, "grudge": 4, "random_move": 5, "alternate": 6}
        allCountryNames = [country.__str__() for country in self.countries]

        matrix = self.make_evolution_matrix(self.countries, rounds)



        fig, ax = plt.subplots()
        im = ax.imshow(matrix, cmap =plt.get_cmap(cmap))

        ax.set_xticks(np.arange(rounds))
        ax.set_yticks(np.arange(len(allCountryNames)))

        ax.set_xticklabels(range(rounds))
        ax.set_yticklabels(allCountryNames)

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        cb = fig.colorbar(im)
        cb.set_label('strategies')
        ax.set_title("Evolution")
        fig.tight_layout()
        plt.show()

    @staticmethod
    def make_evolution_matrix(countries, rounds):

        valueDict = {"collaborate": 1, "defect": 2, "tit_for_tat": 3, "grudge": 4, "random_move": 5, "alternate": 6}
        result = np.zeros((len(countries), rounds+1))

        for country_index, country in enumerate(countries):
            le = len(country.evolution)
            for evo_nr in range(le-1):
                value = valueDict[country.evolution[evo_nr][1]]
                result[country_index, country.evolution[evo_nr][0]: country.evolution[evo_nr+1][0] ] = value
            #laatste balk
            last_value = valueDict[country.evolution[-1][1]]
            result[country_index, country.evolution[-1][0]: ] =last_value

        return result




    def draw_round_robin_matrix(self, texting = True, selecting = [], filtering = [], decimals =2, cmap = 'CMRmap'):
        allCountryNames = [country.__str__() for country in self.countries]
        if selecting:
            countryNames = selecting
        elif filtering:
            countryNames = [country.__str__() for country in self.countries if country.__str__() not in filtering ]
        else:
            countryNames = allCountryNames

        indices = [allCountryNames.index(cn) for cn in countryNames]

        matrix = self.fitness_change_matrix(countryNames, indices)

        fig, ax = plt.subplots()
        im = ax.imshow(matrix, cmap =plt.get_cmap(cmap))

        ax.set_xticks(np.arange(len(countryNames)))
        ax.set_yticks(np.arange(len(countryNames)))

        ax.set_xticklabels(countryNames)
        ax.set_yticklabels(countryNames)

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        if texting:
            for i in range(len(countryNames)):
                for j in range(len(countryNames)):
                    text = ax.text(j, i, round(matrix[i,j],decimals), ha="center", va="center", color="w")

        cb = fig.colorbar(im)
        cb.set_label('change in fitness')

        ax.set_title("Round Robin Matrix")
        fig.tight_layout()
        plt.show()

    def draw_geo(self, factor = 50, resol = 'c', svColor = "out", svSize = "m", projection = 'cyl'): #sv for state variable
        fig, ax = plt.subplots()

        m = Basemap(projection=projection,llcrnrlat=-60,urcrnrlat=75,\
                    llcrnrlon=-110,urcrnrlon=180, ax = ax)
        m.drawcoastlines(zorder = 0)
        m.drawcountries(linewidth=0.5, zorder = 0)

        #colorbar preparation:
        if svColor != "out":
            if svColor == "m":
                lijst = [country.m for country in self.countries]
                cmax = max(lijst)
                cmin = min(lijst)
            elif svColor == "change":
                cmax = max(self.changeInFitness)
                cmin = min(self.changeInFitness)
            elif svColor == "fit":
                lijst = [country.fitness for country in self.countries]
                cmax = max(lijst)
                cmin = min(lijst)
        else:
            cmax = 0
            cmin = 0 # not needed


        for i, country in enumerate(self.countries):
            self.draw_country_marker(ax, country, svColor, svSize, factor = factor, change = self.changeInFitness[i], cmax=cmax, cmin = cmin)

        cmap = plt.get_cmap('gnuplot')
        if svColor != "out":
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=cmin, vmax=cmax))
            sm._A = []
            plt.colorbar(sm)
        #sc = ax.scatter([],[], cmap = cmap, vmin = cmin, vmax = cmax)
        #cb = fig.colorbar(sc)
        #cb.set_label('change in fitness')

        plt.title("Geographical Plot")
        plt.show()

    @staticmethod
    def draw_country_marker(ax, country, svColor="out", svSize="m", factor = 1, change = 100, cmax = 0, cmin = 0):
        if svColor == "out":
            draw_pie(ax, country.loc[0], country.loc[1], country.outcomeDict, size = marker_size(country, svSize, factor, change = change))
        elif svSize == "strat":
            ax.scatter(country.loc[1], country.loc[0], marker = marker_style(str(country.strategy)), s = 3 * factor ,c = marker_color(country, svColor, change), cmap =plt.get_cmap('gnuplot'), vmax = cmax, vmin = cmin)
        else:
            #m.plot(country.loc[1], country.loc[0], 'ro', markersize = marker_size(markerSize, factor) ) #should be area in stead of radius
            ax.scatter(country.loc[1], country.loc[0], s= [marker_size(country, svSize, factor, change)], \
                c = marker_color(country, svColor, change), cmap =plt.get_cmap('gnuplot'), vmax = cmax, vmin = cmin)
