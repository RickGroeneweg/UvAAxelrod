
import numpy as np
import math
from itertools import combinations
from math import sqrt

from .country import *
from .game import *
from .strategies import *
from .match import *
from .action import *

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.patches as mpatches


def marker_size(country ,string, factor, change = 0):
    if string == "m":
        return 1.128 * sqrt(country.m* factor)
    elif string == "fit":
        return 1.128 * sqrt(country.fitness* factor)
    elif string == "change":
        return 1.128 * sqrt(change* factor)
    else: raise Exception("keyword for marker size not implemented")


def marker_color(country, string, change = 0):
    if string == "m":
        return country.m
    elif string == "fit":
        return country.fitness
    elif string == "change":
        return change
    elif string == "strat":
        raise Exception("strat not impemented as colorIndicator")
    else:
        raise Exception("colorIndicator not impemented")

def marker_style(strat):
    mydict = {Collaborate: "o", Defect: "v", TitForTat: "s", Grudge: "x", RandomMove: "D", Alternate: "*"}
    return mydict[strat]


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

def draw_stack(tournament, rounds= 0, cmap = 'jet', xSize = 20, ySize = 20):
    if rounds ==0:
        rounds = tournament.rounds
        numberOfStrategies = 6
    numberOfRounds = rounds
    matrix = np.zeros((numberOfStrategies, numberOfRounds+1))
    #mydict = {Collaborate: 0, Defect:1, TitForTat:2, Grudge: 3, RandomMove:4, Alternate: 5}
    cmap = plt.get_cmap(cmap)
    colors = [cmap(value/5) for value in range(6)]
    for country in tournament.countries:
        for i, (n, strat) in enumerate(country.evolution[:-1]):
            row = tournament.strategyList.index(strat)
            next_n = country.evolution[i+1][0]
            matrix[row, n:next_n] += country.m
        #to do: last line
        last_evo, last_strategy = country.evolution[-1]
        row = tournament.strategyList.index(last_strategy)
        matrix[row, last_evo:] += country.m

    stack = np.vstack(matrix)

    fig, ax = plt.subplots(figsize =(xSize, ySize))
    ax.stackplot(range(rounds+1), matrix[0,:], matrix[1,:], matrix[2,:], matrix[3,:], matrix[4,:], matrix[5,:], labels=tournament.strategyList, colors= colors)
    ax.legend(loc=5)
    plt.ylabel('Market share')
    plt.xlabel('Round number')
    plt.show()

def draw_fitness_graph(tournament, selecting=[], filtering = [], cmap = 'gnuplot'):

    cmap = plt.get_cmap(cmap)


    if selecting:
        countries=selecting
    elif filtering:
        countries = [country for country in tournament.countries if not country in filtering]
    else:
        countries = tournament.countries
    for country in countries:
        draw_country_line(country, cmap =cmap)


    plt.ylabel('fitness')
    plt.show()

def draw_country_line(country, cmap = 'gnuplot'): #need to add a color legend and collor line option
    colorDict = {Collaborate: 0, Defect: 1, TitForTat: 2, Grudge: 3, RandomMove: 4, Alternate: 5}
    cmap = plt.get_cmap(cmap)
    colors = [cmap(value) for value in range(6)]
    le = len(country.evolution)


    for evo_nr in range(le-1):
        Xstart = country.evolution[evo_nr][0]
        Xend = country.evolution[evo_nr+1][0]
        newColor = colorDict[country.evolution[evo_nr][1]]
        plt.plot(range(Xstart, Xend ), country.fitnessHistory[Xstart: Xend])

    Xstart = country.evolution[-1][0]
    Xend = len(country.fitnessHistory)
    lastColor = colorDict[country.evolution[-1][1]]
    plt.plot(range(Xstart, Xend), country.fitnessHistory[Xstart:])




def draw_evo(tournament, rounds =0 , cmap = 'jet' , xSize = 20, ySize = 40):
    '''draws for every country the evolution of its stategy'''
    if rounds ==0:
        rounds = tournament.rounds

    allCountryNames = [country.__str__() for country in tournament.countries]

    matrix = make_evolution_matrix(tournament.countries, rounds)



    fig, ax = plt.subplots(figsize=(xSize, ySize))
    im = ax.imshow(matrix, cmap =plt.get_cmap(cmap), aspect='auto')

    #ax.set_xticks(np.arange(rounds))
    ax.set_yticks(np.arange(len(allCountryNames)))

    #ax.set_xticklabels(range(rounds))
    ax.set_yticklabels(allCountryNames)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # get the colors of the values, according to the
    # colormap used by imshow
    colors = [ im.cmap(im.norm(value)) for value in range(len(tournament.strategyList))]
    # create a patch (proxy artist) for every color
    patches = [ mpatches.Patch(color=colors[i], label=tournament.strategyList[i]) for i in range(len(tournament.strategyList)) ]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=5, borderaxespad=0. )

    ax.set_title("Evolution")
    #fig.tight_layout()
    plt.show()


def make_evolution_matrix(countries, rounds):
    '''helper function to draw_evo'''
    valueDict = {Collaborate: 0, Defect: 1, TitForTat: 2, Grudge: 3, RandomMove: 4, Alternate: 5}
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


def select_or_filter_names(tournament, selecting =[], filtering = []):#not finished yet
    allCountryNames = [country.__str__() for country in tournament.countries]
    if selecting:
        countryNames = [country.__str__() for country in selecting]
    elif filtering:
        countryNames = [country.__str__() for country in tournament.countries if country not in filtering ]
    else:
        countryNames = allCountryNames

def draw_round_robin_matrix(tournament, texting = False, selecting = [], filtering = [], decimals =2, cmap = 'gnuplot', xSize = 20, ySize=20):
    '''draws a matrix where for every country the amount of change in fitness due to every other country is drawn'''
    #this should be a helper method using variables: selecting, filtering
         #returning: list of indices
    allCountryNames = [country.__str__() for country in tournament.countries]
    if selecting:
        countryNames = [country.__str__() for country in selecting]
    elif filtering:
        countryNames = [country.__str__() for country in tournament.countries if country not in filtering ]
    else:
        countryNames = allCountryNames
    print(countryNames)
    indices = [allCountryNames.index(cn) for cn in countryNames]
    print(indices)
    #helper method should end here


    matrix = tournament.matchResultsMatrix[indices, :][:, indices] #matrix with only rows and columns of indexed countries

    fig, ax = plt.subplots(figsize=(xSize, ySize))
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


def colorbarMinAndMax(tournament, colorIndicator):
    if colorIndicator != "out":
        if colorIndicator == "m":
            lijst = [country.m for country in tournament.countries]
            cmax = max(lijst)
            cmin = min(lijst)
        elif colorIndicator == "change":
            cmax = max(tournament.changeInFitness)
            cmin = min(tournament.changeInFitness)
        elif colorIndicator == "fit":
            lijst = [country.fitness for country in tournament.countries]
            cmax = max(lijst)
            cmin = min(lijst)
        else:
            cmax = 0
            cmin = 0 #variable not needed
    else:
        cmax = 0
        cmin = 0 # variable not needed
    return (cmin, cmax)

def draw_geo(tournament, factor = 50, resol = 'c', colorIndicator = "out", sizeIndicator = "m", projection = 'cyl', xSize = 10, ySize = 10): #sv for state variable
    '''draws a world map with all participating coutnries'''
    fig, ax = plt.subplots(figsize=(xSize, ySize))

    m = Basemap(projection=projection,llcrnrlat=-60,urcrnrlat=75,\
                llcrnrlon=-110,urcrnrlon=180, ax = ax)
    m.drawcoastlines(zorder = 0)
    m.drawcountries(linewidth=0.5, zorder = 0)
    #colorbar preparation:
    cmin, cmax = colorbarMinAndMax(tournament, colorIndicator)
    for i, country in enumerate(tournament.countries):
        draw_country_marker(ax, country, colorIndicator, sizeIndicator, factor = factor, change = tournament.changeInFitness[i], cmax=cmax, cmin = cmin)
    cmap = plt.get_cmap('gnuplot')
    if colorIndicator != "out":
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=cmin, vmax=cmax))
        sm._A = []
        plt.colorbar(sm)
    elif sizeIndicator == "strat":
        legendKeys = [plt.plot(1, "r"+i, markersize = 100) for i in ["o", "v", "s", "x", "D", "*"]]
        legendLabels = tournament.strategyList
        plt.legend(legendKeys, legendLabels)

    #sc = ax.scatter([],[], cmap = cmap, vmin = cmin, vmax = cmax)
    #cb = fig.colorbar(sc)
    #cb.set_label('change in fitness')

    plt.title("Geographical Plot")
    plt.show()


def draw_country_marker(ax, country, colorIndicator="out", sizeIndicator="m", factor = 1, change = 100, cmax = 0, cmin = 0):
    '''helper function to draw_geo'''
    if colorIndicator == "out":
        draw_pie(ax, country.loc[0], country.loc[1], country.outcomeDict, size = marker_size(country, sizeIndicator, factor, change = change))
    elif sizeIndicator == "strat":
        mymarker = marker_style(country.strategy.name())
        mylabel = str(country.strategy)
        ax.scatter(country.loc[1], country.loc[0], marker = mymarker, label = mylabel, s = 3 * factor ,c = marker_color(country, colorIndicator, change), cmap =plt.get_cmap('gnuplot'), vmax = cmax, vmin = cmin)
    else:
        #m.plot(country.loc[1], country.loc[0], 'ro', markersize = marker_size(markerSize, factor) ) #should be area in stead of radius
        ax.scatter(country.loc[1], country.loc[0], s= [marker_size(country, sizeIndicator, factor, change)], \
            c = marker_color(country, colorIndicator, change), cmap =plt.get_cmap('gnuplot'), vmax = cmax, vmin = cmin)
