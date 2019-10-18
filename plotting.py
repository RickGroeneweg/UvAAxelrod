"""
This file contains functions, that plot and aggregate results from a simulation
from the Tournament class.
"""

import matplotlib.pyplot as plt
import numpy as np
from .enums import Action, C, D

def template_for_sebastian(tournament):
    """
    Discription
    
    example:
        >>>
    """
    pass






def get_game_history(tournament, c1, c2):
    """
    get the history of a game betweet c1 and c2
    
    parameters:
        -c1, c2: Country, countries in question
        
    returns:
        - list of tupples, where the [0]th elements are moves by c1, and the [1]th elements are moves by c2
        
    example:
        >>> get_game_history(tournament, russia, china)
        [(<Action.C: 1>, <Action.C: 1>),
         (<Action.C: 1>, <Action.D: 0>),
         (<Action.D: 0>, <Action.D: 0>)]
    """
    data = tournament.graph.get_edge_data(c1, c2)
    if data is None:
        # order of c1 and c2 what wrong in the digraph
        data = tournament.graph.get_edge_data(c2, c1)
        return [(a1, a2) for (a2, a1) in data['history']]
    else:
        return data['history']

def C_D_dict_per_round(tournament):
    """
    retuns:
        - dict, with two keys"
            - Action.C: array with the number of cooperations per round
            - Action.D: array with the number of deffections per round
    """
    array_dict= {C: np.zeros((tournament.round,)), D: np.zeros((tournament.round,))}
    
    
    for country_1, country_2, data in tournament.graph.edges(data=True):
        for round_num, (action_1, action_2) in enumerate(data['history']):
            array_dict[action_1][round_num] += 1
            array_dict[action_2][round_num] += 1
    
    return array_dict

def overal_C_and_D(tournament):
    """
    returns:
        - tuple where the [0]th resp. [1]th element is the number of times any country cooperated resp. defected.
    """
    array_dict = C_D_dict_per_round(tournament)
    number_of_C = sum(array_dict[C])
    number_of_D = sum(array_dict[D])
    
    print(f'number of cooperations: {number_of_C}, number of deffections: {number_of_D}')
    
    return number_of_C, number_of_D
            

def draw_C_and_D_stack(tournament, rounds=None, cmap = 'Greys_r', length=10, width =23):
    rounds = rounds or tournament.round
    
    c_d_dict = C_D_dict_per_round(tournament)
    matrix = np.stack([c_d_dict[Action.C], c_d_dict[Action.D]])

    fig, ax = plt.subplots(figsize =(width, length))
    ax.stackplot(range(rounds), *matrix, colors=[(1,1,1), (0,0,0)]) #this needs to be adjusted for the number of strategies
    ax.legend(loc='upper right',bbox_to_anchor=(0.95,0.95),ncol=1, fontsize='xx-large')
    plt.ylabel('Moves', fontsize=24)
    print('Ask sebastian if he wants this per market share in stead of moves')
    plt.xlabel('Round number', fontsize=24)
    plt.tick_params(axis='both',labelsize=14)
    plt.title('Defection(Black) and Cooperation(White)', fontsize=24)

def draw_stack(tournament, rounds=None, cmap = 'Greys_r', length=10, width =23):
    
    rounds = rounds or tournament.round
    n_strategies = len(tournament.strategy_list)
    matrix = np.zeros((n_strategies, rounds+1))
    
    cmap = plt.get_cmap(cmap)
    colors = [cmap(value/(n_strategies-1)) for value in range(n_strategies)]
    
    for country in tournament.countries():
        for i, (n, strat) in enumerate(country._evolution[:-1]):

            row = tournament.strategy_list.index(strat)
            next_n = country._evolution[i+1][0]
            matrix[row, n:next_n] += country.m
        #last strategy
        last_evo, last_strategy = country._evolution[-1]
        row = tournament.strategy_list.index(last_strategy)
        matrix[row, last_evo:] += country.m
    
    fig, ax = plt.subplots(figsize =(width, length))
    ax.stackplot(range(rounds+1), *matrix, labels=[s.name for s in tournament.strategy_list], colors= colors) #this needs to be adjusted for the number of strategies
    ax.legend(loc='upper right',bbox_to_anchor=(0.95,0.95),ncol=1, fontsize='xx-large')
    plt.ylabel('Market share', fontsize=24)
    plt.xlabel('Round number', fontsize=24)
    plt.tick_params(axis='both',labelsize=14)
    plt.title('Evolution of Strategies in Heterogenous Populations', fontsize=24)

def draw_country_line(country, cmap, strategy_list): #need to add a color legend and color line option


    colors = [cmap(value/(len(strategy_list)-1)) for value in range(len(strategy_list))]

    colorDict = dict(zip(strategy_list, colors))

    le = len(country._evolution)


    for evo_nr in range(le-1):
        Xstart = country._evolution[evo_nr][0]
        Xend = country._evolution[evo_nr+1][0] +1
        newColor = colorDict[country._evolution[evo_nr][1]]
        plt.plot(range(Xstart, Xend), country.fitness_history[Xstart: Xend], color = newColor)


    Xstart = country._evolution[-1][0]
    Xend = len(country.fitness_history)
    lastColor = colorDict[country._evolution[-1][1]]
    plt.plot(range(Xstart, Xend), country.fitness_history[Xstart:], color = lastColor)



def draw_country_line_delta(country, cmap, strategy_list):
    fitness_history = country.fitness_history
    fitnessDeltas =[0]
    for i in range(len(fitness_history)-1):
        fitnessDeltas.append(fitness_history[i+1] - fitness_history[i])
    plt.plot(fitnessDeltas)
 
def wholePopulation_fitessList(countries, delta = False):
    def calculate_entire_fitness(roundNumber): #Give entire fitness in the population at roundNumber
        result = 0
        for country in countries:
            result += country.fitness_history[roundNumber]
        return result

    listOfFitnesses = []
    for round in range(len(countries[0].fitness_history)):
        listOfFitnesses.append(calculate_entire_fitness(round))

    if delta == False:
        return listOfFitnesses
    else:
        return [0] + [(listOfFitnesses[i+1] - listOfFitnesses[i]) for i in range(len(listOfFitnesses)-1)]    
    
def draw_fitness_graph(tournament, selecting=[], filtering = [], cmap = 'Greys_r', xSize = 10, ySize = 10, delta = False, wholePopulation = False):

    fig, ax = plt.subplots(figsize =(xSize, ySize))
    cmap = plt.get_cmap(cmap)

    if selecting:
        countries=selecting
    elif filtering:
        countries = [country for country in tournament.countries if not country in filtering]
    else:
        countries = list(tournament.countries())


    if delta == False and wholePopulation == False:
        for country in countries:
            draw_country_line(country, cmap, tournament.strategy_list)
            plt.annotate(country.name, xy=(len(country.fitness_history) - 0.5, country.fitness_history[-1]))
    elif delta == True and wholePopulation == False:
        for country in countries:
            draw_country_line_delta(country, cmap, tournament.strategy_list)
            plt.annotate(country.name, xy=(len(country.fitness_history) - 0.5, (country.fitness_history[-1] - country.fitness_history[-2])))
    elif wholePopulation == True:
        plt.plot(wholePopulation_fitessList(countries, delta = delta),c='black',linewidth=1)
        plt.title("Change in Fitness of Whole Population", fontsize = 24)
        plt.xlabel("Number of Rounds", fontsize = 24)
        plt.ylabel("Fitness Level", fontsize = 24)
        plt.tick_params(axis='both',labelsize=14)

    
    
    
    
    
    
    
    
    
    
    
