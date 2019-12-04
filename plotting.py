"""
This file contains functions, that plot and aggregate results from a simulation
from the Tournament class.
"""

import matplotlib.pyplot as plt
import numpy as np
from .enums import Action, C, D
import pandas as pd
from .tournament import Tournament
from statistics import mean, stdev



def get_game_data(graph, c1, c2, OUTCOME):
    outcome ={'R':'RR', 'P':'PP', 'T':'TS', 'S':'ST'}[OUTCOME]
    
    data = graph.get_edge_data(c1, c2)
    if data is None:
        # order of c1 and c2 what wrong in the digraph
        data = graph.get_edge_data(c2, c1)
        
        # the outcome
        return data[outcome[::-1]][1]
    else:
        return data[outcome][0]

def get_payoff_dataframe(population,  payoff_functions, distance_function, outcome):
    """
    parameters:
        - outcome: one of 'R', 'S', 'P', 'T'
    """
    graph = Tournament.init_graph(population, distance_function, payoff_functions)
    names = [c.name for c in list(graph.nodes)]
    df = pd.DataFrame([], columns=names)
    for this_country in population:
        country_dict = {}
        for other_country in population:
            if this_country == other_country: continue

            dat = get_game_data(graph, this_country, other_country, outcome)

            country_dict[other_country.name] = dat
           
        
        
        country_dict['Receiving_Country'] = this_country.name
    

        df = df.append(country_dict, ignore_index=True)
    df = df.set_index('Receiving_Country')

    return df








def template_for_sebastian(tournament):
    """
    Discription
    
    example:
        >>>
    """
    pass


def get_country_df(tournament, add_outcomes=True):
    df = pd.DataFrame([[c.name, c.m, c.e, c.i, c.sqrt_area] for c in list(tournament.graph.nodes)], columns=['name', 'm', 'e', 'i', 'sqrt_area']).set_index('name')
    if add_outcomes:
        outcomes = get_outcomes(tournament, df)
        outcomes_df = pd.DataFrame.from_dict(outcomes, orient='index')
        df = df.join(outcomes_df)
        
    return df

def get_outcomes(tournament, df):
    acc_dict = {}
    
    for country in tournament.graph.nodes:
        games_1 = list(tournament.graph.out_edges(country, data=True))
        games_2 = list(tournament.graph.in_edges(country, data=True))
        
        #assert len(games_1)+len(games_2) == len(tournament.graph.nodes) -1
        outcome_dict = {(C,C): 'R', (C,D):'S', (D,C): 'T', (D,D): 'P'}
        outcome_acc = {'R': 0, 'S': 0, 'T':0, 'P':0}
        
        for game in games_1:
            c1, c2, data = game
            assert c1 == country
            zips = list(zip(data['history_1'], data['history_2']))
            for actions in zips:
                outcome_acc[outcome_dict[actions]] += 1
        for game in games_2:
            c2, c1, data = game
            assert c1 == country
            zips = list(zip(data['history_2'], data['history_1']))
            for actions in zips:
                outcome_acc[outcome_dict[actions]] += 1 
                
        #print(sum(outcome_acc.values()))
        acc_dict[country.name] = outcome_acc
    #print(acc_dict)
    return acc_dict    
            
        

def get_game_history(tournament, c1, c2):
    """
    get the history of a game betweet c1 and c2
    
    parameters:
        - c1, c2: Country, countries in question
        
    returns:
        - list of tupples, where the [0]th elements are moves by c1, and the [1]th elements are moves by c2
        
    example:
        >>> get_game_history(tournament, russia, china)
        [(<Action.C: 1>, <Action.C: 1>),
         (<Action.C: 1>, <Action.D: 0>),
         (<Action.D: 0>, <Action.D: 0>)]
    """
    # quick fix to be able to get the right countries by using their names as strings
    if isinstance(c1, str):
        c1 = [c for c in tournament.countries() if c.name==c1][0]
    if isinstance(c2, str):
        c2 = [c for c in tournament.countries() if c.name==c2][0]
        
    # Todo: if the name of a country is not in the list of names, then the code above error without clear message
    
    
    
    data = tournament.graph.get_edge_data(c1, c2)
    if data is None:
        # order of c1 and c2 what wrong in the digraph
        data = tournament.graph.get_edge_data(c2, c1)
        return zip(data['history_2'],data['history_1'])
    else:
        return zip(data['history_1'],data['history_2'])

def outcomes_dict_per_round(tournament):
    array_dict= {'Mutual_Cooperation': np.zeros((tournament.round,)), 'Mutual_Defection': np.zeros((tournament.round,)), 'Exploitation': np.zeros((tournament.round,))}

    for country_1, country_2 in tournament.graph.edges(data=False):     
        
        for round_num, (action_1, action_2) in enumerate(get_game_history(tournament, country_1, country_2)):
            if action_1 == action_2:
                outcome = 'Mutual_Cooperation' if action_1 == C else 'Mutual_Defection'
                array_dict[outcome][round_num] += 1
            else:
                array_dict['Exploitation'][round_num] += 1

    return array_dict


def C_D_dict_per_round(tournament):
    """
    retuns:
        - dict, with two keys"
            - Action.C: array with the number of cooperations per round
            - Action.D: array with the number of deffections per round
    """
    array_dict= {C: np.zeros((tournament.round,)), D: np.zeros((tournament.round,))}
    
    
    for country_1, country_2, data in tournament.graph.edges(data=True):
        for round_num, (action_1, action_2) in enumerate(get_game_history(tournament, country_1, country_2)):
            array_dict[action_1][round_num] += 1
            array_dict[action_2][round_num] += 1
    
    return array_dict

def mean_C(tournament):
    n_C, n_D = overal_C_and_D(tournament)
    result = n_C/(n_C+n_D)
    print(f'the mean level of Cooperation: {result}')
    return result

def standard_deviation_C(tournament):
    array_dict = C_D_dict_per_round(tournament)
    fractions_c = [num_c/(num_c + num_d) for num_c, num_d in zip(array_dict[C], array_dict[D])]
    result = np.std(fractions_c)
    print(f'the standard deviation of the series of standardized cooperation levels per round: {result}')
    
    return result
    

def overal_outcomes(tournament):
    array_dict = outcomes_dict_per_round(tournament)
    number_mutual_C = sum(array_dict['Mutual_Cooperation'])
    number_mutual_D = sum(array_dict['Mutual_Defection'])
    number_exploitation = sum(array_dict['Exploitation'])
    
    return number_mutual_C, number_mutual_D, number_exploitation

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
            
def outcome_ratios_per_round(tournament, x_size=10, y_size=10):
    array_dict = outcomes_dict_per_round(tournament)
    fractions_mutual_C = [num_c/(num_c + num_d + num_expl) for num_c, num_d, num_expl in zip(array_dict['Mutual_Cooperation'], array_dict['Mutual_Defection'],array_dict['Exploitation'])]
    fractions_mutual_D = [num_d/(num_c + num_d + num_expl) for num_c, num_d, num_expl in zip(array_dict['Mutual_Cooperation'], array_dict['Mutual_Defection'],array_dict['Exploitation'])]
    fractions_mutual_Expl = [num_expl/(num_c + num_d + num_expl) for num_c, num_d, num_expl in zip(array_dict['Mutual_Cooperation'], array_dict['Mutual_Defection'],array_dict['Exploitation'])]
    
    fig, ax = plt.subplots(figsize =(x_size, y_size))
    plt.plot(fractions_mutual_C, label='Mutual Cooperation', color =(0.8,)*3)
    plt.plot(fractions_mutual_D, label='Mutual Defection', color =(0.2,)*3)
    plt.plot(fractions_mutual_Expl, label='Exploitation', color =(0.5,)*3)
    plt.legend()
    plt.xlabel('Round number')
    plt.ylabel('Outcome ratios')

def C_D_ratios_per_round(tournament, x_size=10, y_size=10):
    array_dict = C_D_dict_per_round(tournament)
    fractions_c = [num_c/(num_c + num_d) for num_c, num_d in zip(array_dict[C], array_dict[D])]

    fig, ax = plt.subplots(figsize =(x_size, y_size))
    plt.plot(fractions_c, color='black')
    plt.xlabel('Round number')
    plt.ylabel('Cooperation ratio')

def draw_stack(tournament, rounds=None, cmap = 'Greys_r', x_size=10, y_size =23):
    
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
    
    fig, ax = plt.subplots(figsize =(y_size, x_size))
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

def wholePopulation_fitnessList(countries, delta = False):
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
    
def draw_fitness_graph(tournament, selecting=[], filtering = [], cmap = 'Greys_r', x_size = 10, y_size = 10, delta = False, wholePopulation = False):

    fig, ax = plt.subplots(figsize =(x_size, y_size))
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
        plt.plot(wholePopulation_fitnessList(countries, delta = delta),c='black',linewidth=1)
        plt.title("Change in Fitness of Whole Population", fontsize = 24)
        plt.xlabel("Number of Rounds", fontsize = 24)
        plt.ylabel("Fitness Level", fontsize = 24)
        plt.tick_params(axis='both',labelsize=14)

def fitness_history_sum_list(tournament, selecting=[], filtering = []):
    """
    return the fitness of all contries summed, in a list of rounds.
    """


    if selecting:
        countries=selecting
    elif filtering:
        countries = [country for country in tournament.countries if not country in filtering]
    else:
        countries = list(tournament.countries())

    fitness_histories = [c.fitness_history for c in countries]
    ls = [sum(fitnesses) for fitnesses in zip(*fitness_histories)]
    
    return ls
    

def draw_population_fitness(tournament, selecting=[], filtering = [], cmap = 'Greys_r', x_size = 10, y_size = 10):
    """
    population fitness (summed) per round
    """
   
    ls = fitness_history_sum_list(tournament, selecting=selecting, filtering = filtering)

    fig, ax = plt.subplots(figsize =(x_size, y_size))
    cmap = plt.get_cmap(cmap)

    plt.plot(ls,c='black',linewidth=1)
    plt.title("Fitness of Whole Population", fontsize = 24)
    plt.xlabel("Number of Rounds", fontsize = 24)
    plt.ylabel("Fitness Level", fontsize = 24)
    plt.tick_params(axis='both',labelsize=14)   

def draw_population_delta_fitness(tournament, selecting=[], filtering = [], cmap = 'Greys_r', x_size = 10, y_size = 10):
  
    fitnes_history_ls = fitness_history_sum_list(tournament, selecting=selecting, filtering = filtering)
    
    
    ls = [fitnes_history_ls[i + 1] - fitnes_history_ls[i] for i in range(len(fitnes_history_ls)-1)] 

    fig, ax = plt.subplots(figsize =(x_size, y_size))
    cmap = plt.get_cmap(cmap)

    #print(ls)
    
    max_y = max(ls)*1.1
    min_y = min(ls)*0.9
    ax.set_ylim(bottom=min_y, top=max_y)
    plt.plot(ls,c='black',linewidth=1)
    #plt.title("Fitness Changes of Whole Population", fontsize = 24)
    plt.xlabel("Number of Rounds", fontsize = 24)
    plt.ylabel("Fitness Change", fontsize = 24)
    plt.tick_params(axis='both',labelsize=14)     
    
    
### definitions by Sebastian
def get_rewards(population, payoff_functions, distance_function):
    """
    calculate the payoffs of every country with every other country when both of them cooperate.
    """
    return get_payoff_dataframe(population,  payoff_functions, distance_function, 'R')

def get_temptations(population, payoff_functions, distance_function):
    """
    calculate the payoffs of every country with every other country when itself defects and  the others cooperate.
    """
    return get_payoff_dataframe(population,  payoff_functions, distance_function, 'T')

def get_punishments(population, payoff_functions, distance_function):
    """
    calculate the payoffs of every country with every other country when both of them defect.
    """
    return get_payoff_dataframe(population,  payoff_functions, distance_function, 'P')
    
def get_suckers(population, payoff_functions, distance_function):
    """
    calculate the payoffs of every country with every other country when itself cooperates and the others defect.
    """
    return get_payoff_dataframe(population,  payoff_functions, distance_function, 'S')
    
    
def get_self_reward(population, payoff_functions, distance_function):
    """
    calculate fitness, which every country gets from its own market.
    """
    for country in population:
        country.d = distance_function(country.sqrt_area)
    self_reward_dict = {country: payoff_functions['self_reward'](country) for country in population}
    return pd.DataFrame.from_dict(self_reward_dict)

def get_mean_rewards(population, payoff_functions, distance_function):
    """
    calculate the mean 
    """ 
    df = get_rewards(population, payoff_functions, distance_function)
    return df.mean()

def get_mean_temptations(population, payoff_functions, distance_function):
    """
    calculate the mean 
    """
    df = get_temptations(population, payoff_functions, distance_function)
    return df.mean()    


def get_mean_punishments(population, payoff_functions, distance_function):
    """
    calculate the mean 
    """
    df = get_punishments(population, payoff_functions, distance_function)
    return df.mean()

def get_mean_suckers(population, payoff_functions, distance_function):
    """
    calculate the mean 
    """
    df = get_suckers(population, payoff_functions, distance_function)
    return df.mean()  


def get_sd_rewards(population, payoff_functions, distance_function):
    """
    calculate the standard deviation
    """
    df = get_rewards(population, payoff_functions, distance_function)
    return df.std()

def get_sd_temptations(population, payoff_functions, distance_function):
    """
    calculate the standard deviation
    """ 
    df = get_temptations(population, payoff_functions, distance_function)
    return df.std()    


def get_sd_punishments(population, payoff_functions, distance_function):
    """
    calculate the standard deviation
    """
    df = get_punishments(population, payoff_functions, distance_function)
    return df.std()

def get_sd_suckers(population, payoff_functions, distance_function):
    """
    calculate the standard deviation
    """
    df = get_suckers(population, payoff_functions, distance_function)
    return df.std()
    
    
    
def get_mean_self_rewards(population, payoff_functions, distance_function):  
    for country in population:
        country.d = distance_function(country.sqrt_area)
    
    return mean([payoff_functions['self_reward'](country) for country in population])
    
def get_sd_self_rewards(population, payoff_functions, distance_function):
    for country in population:
        country.d = distance_function(country.sqrt_area)    
    
    return stdev([payoff_functions['self_reward'](country) for country in population])




















