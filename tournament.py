import networkx as nx
import numpy as np
from geopy.distance import distance
import time

from .strategies import cooperate, defect, tit_for_tat, generous_tit_for_tat, win_stay_lose_shift
from .initialize_countries import *

from itertools import combinations
from .payoff_functions import default_payoff_functions, traditional_payoff_functions, selfreward

from .enums import to_outcome, Action, random_action

class Tournament:
    """
    A Tournament instance is meant to be used for one simulation. This
    simulation is a variation on an Axelrod tournament. This class is
    the central class of this package. More can be read in the README.md file
    and in the paper (todo: add link).
    """
    def __init__(
        self, 
        countries, 
        max_rounds, 
        strategy_list, 
        payoff_functions=default_payoff_functions, # rewards that countries get, defaults to the functions described in the paper.
        distance_function = lambda d: d, # defaults to just the identity, if one wanted that distances get less important the larger they are, one could use the sqrt.
        surveillance_penalty = True,
        penalty_dict = {cooperate: 1, defect: 1, tit_for_tat: 0.95, generous_tit_for_tat: 0.95, win_stay_lose_shift: 0.95}, # Ask sebastian value for generous-tit-for-tat
        noise = 0
    ):
        """
        parameters:
            - countries: Country
            - max_rounds: int
            - strategy_list: list
            - payoff_functions: dict
        """
        # meta data
        self.max_rounds: int = max_rounds
        self.strategy_list: list = strategy_list
        self.payoff_functions: dict = payoff_functions
        self.surveillance_penalty = surveillance_penalty
        self.penalty_dict = penalty_dict
        self.noise = noise
        
        # Data from the simulations will be stored in an NetworkX-graph
        self.graph = self.init_graph(countries, distance_function, self.payoff_functions)
        
        # results of a the simulations
        self.fitness_results = np.zeros((len(self.countries()), max_rounds))
        self.evolution = [] # Todo: add evolution
        
        # state variables
        self.round = 0
        self.is_done = False
       
    @staticmethod
    def init_graph(countries, distance_function, payoff_functions):
        """
        initialize the graph (form the NetworkX library), that is used to store
        data from the simulation. Nodes in this graph store countries, and edges
        store the data associated with games between these countries (history, 
        payoff values, distance).
        
        parameters:
            - countries: list of Country, countries that take part in the Tournament
        """
        # we need to use DiGraph (directional edges) since Temptation and Sucker events are asymmetrical
        graph = nx.DiGraph() 
        
        # add nodes to graph
        for country in countries:
            graph.add_node(country)
            country.d = distance_function(country.sqrt_area)
            
        # add edges to graph
        # loop through all combinations of countries in the tournament.
        # the index of country 1 (c1) is always less than that of country 2 (c2)
        for c1, c2 in combinations(countries, 2):
            # calculate the payoff values that are associated with games 
            # between these two countries, and store them as tupples
            # R: reward, P: punishment, T: temptation, S: sucker
            real_distance = distance(c1.location, c2.location).km
            d = distance_function(real_distance) if distance_function else real_distance
            RR = (payoff_functions['R'](c1,c2,d), 
                  payoff_functions['R'](c2,c1,d))
            PP = (payoff_functions['P'](c1,c2,d), 
                  payoff_functions['P'](c2,c1,d))
            TS = (payoff_functions['T'](c1,c2,d), 
                  payoff_functions['S'](c2,c1,d))
            ST = (payoff_functions['S'](c1,c2,d), 
                  payoff_functions['T'](c2,c1,d))
            
            assert RR[0] <= TS[0], f'reward was greater than temptation for countries {c1.name} and {c2.name}'
            assert RR[1] <= ST[1], f'reward was greater than temptation for countries {c1.name} and {c2.name}'
            
            
            # initialize all edges
            graph.add_edge(
                c1, 
                c2,
                # we add data to each edge
                history_1 = [], # list to accumulate tuples of actions
                history_2 = [],
                distance = d,
                RR = RR, 
                PP = PP,
                TS = TS,
                ST = ST
            )
        
        return graph
    
    
    
    def countries(self):
        """
        return:
            - countries partaking in this tournament
        """
        return self.graph.nodes()
    
    
    # Todo: this now gives an assertion error
    def init_strategies(self, countries = None, strategy = None):
        """
        initizalize strategy for given countries. 
        
        parameters:
            countries: list or None, countries to change strategy, if None, then all countries are used
            strategy: list or None, stratey to be given to countries, if None, then echt country
                      is randomly assigned a strategy from self.strategy_list.
        
        side effects:
            - changes the countries strategy
            
        example:
            >>> tournament = Tournament(...)
            >>> tournament.init_strategies(china, cooperate)
        """
        assert self.round == 0
        
        if isinstance(countries, Country):
            countries = [countries]
        
        countries = countries or self.countries()
        
        for country in countries:
            country.change_strategy(
                    0, strategy or np.random.choice(self.strategy_list)
                    )
        
        
    def init_fitness(self, init_fitnes_as_m, countries = None):
        """
        initizalize the fiteness for each country
        
        parameters:
            - init_fitnes_as_m: bool, if countries should start out with fitness
                                equal to their market size.
        
        side effects:
            - changes `fitness` and `fitness_history` for all countries
        """
        countries = countries or self.countries()
        
        for country in countries:
            # todo: think if this logic has a better place in the country class itself..
            country.fitness = country.m if init_fitnes_as_m else 0
            country.fitness_history = [country.fitness]
        
    def countries_per_strategy_dict(self):
        """
        return:
            - dictionary where the keys are strategies and the values the number of countries that play this strategy
            
        example:
            >>> tournament = Tournament(XXX)
            >>> tournament.init_strategies(None, cooperate)
            >>> tournament.countries_per_strategy_dict()
            {cooperate: 100, defect: 0}
        """
        d = {strategy: 0 for strategy in self.strategy_list}
        for country in self.countries():
            d[country._strategy] += 1
        return d
        
        
        
    def one_strategy_left(self, strategy_n_countries_dict):
        """
        returns:
            - True if there is only one strategy left in the simulation
            
        example:
            >>> tournament = Tournament(XXX)
            >>> tournament.init_strategies(None, cooperate)  # set al countries to cooperating strategy
            >>> tournament.one_strategy_left()
            True
        """
        for value in strategy_n_countries_dict.values():
            if value == len(self.countries()):
                return True
        return False

    
    def change_a_strategy(self, mutation_rate, round_num):
        """
        Change the strategy of a random country, to become the strategy of a
        'winning country', that was selected with probabilites proporitonal to 
        the fitness. This way strategies that do well in the tournament will
        spread through countries.
        
        Sometimes, in stead of the above, there will be a change in strategy
        that is entirely random.
        
        parameters:
            - mutation_rate: probabilitie of a random strategy change
            
        side effect:
            - changes a countries strategy
            
        """
        
        country_list = list(self.countries())

        N = len(country_list)
        
        # randomly select a country that will lose it's strategy to the winning strategy
        elimiation_idx = np.random.randint(N)
        losing_country = country_list[elimiation_idx]
        losing_strategy = losing_country.get_current_strategy()
        
        # select a winning strategy
        mutation = bool(np.random.binomial(1, mutation_rate))
        if mutation:
            # in stead of changing a strategy according to the rules of the simmulation
            # we sometimes have a random mutation
            winning_strategy = np.random.choice(self.strategy_list)
            winning_country = 'random_mutation'
        else:
            # we select a winning strategy with the probabilites of 'how much fitness each strategy has'
            fitness_scores = [country.fitness for country in country_list]
            fitness_scores_non_neg = [max(0, fitness) for fitness in fitness_scores]
            total_fitness = sum(fitness_scores_non_neg)
            probabilities = [fitness_scores_non_neg[j]/total_fitness for j in range(N)] # errors if total fitness becomes negative...
            
            # select a random country, with probabilities by normalized fitnesses
            reproduce_idx = np.random.choice(range(N), p=probabilities)
            winning_country = country_list[reproduce_idx]
            winning_strategy = winning_country.get_current_strategy()
        
        # actually CHANGE the strategy
        losing_country.change_strategy(round_num, winning_strategy)
        print(f'  strategy change: {losing_country} {losing_strategy.name} -> {winning_strategy.name} ({winning_country})')
        
        # for logging
        return losing_country, winning_strategy 
    
    def play_prisoners_dilema(self, country_1, country_2, game):
        """
        parameters:
            - coutry_1, country_2: Country
            - game: dict, data associated with the game between countr_1 and country_2 
            
        side effects:
            - appends history of game
            - changes fitness of country_1 and country_2
            
        example:
            >>> country_1, country_2, data = self.graph.get_edge(india, japan)
            >>> self.play_prisoners_dilema(country_1, country_2, data)
            XXX check this example
        """
                   
            
        # let countries' strategies choose an action
        action_1 = country_1.select_action(game['history_1'], game['history_2'], self.noise)
        action_2 = country_2.select_action(game['history_2'], game['history_1'], self.noise)
        
        # append game history
        game['history_1'].append(action_1)
        game['history_2'].append(action_2)
        
        # get payoff values
        outcome = to_outcome(action_1, action_2)
        Δfitness_1,  Δfitness_2 = game[outcome] #self.graph.get_edge_data(country_1, country_2)[outcome]
        
        if self.surveillance_penalty:
            # to simmulate the effort that it takes to take a certain strategy
            # for some strategies a penalty is added, so that only part of the
            # change in fitness is really received.
            Δfitness_1 *= self.penalty_dict[country_1.get_current_strategy()]
            Δfitness_2 *= self.penalty_dict[country_2.get_current_strategy()]
            
        #change fitness
        country_1.fitness += Δfitness_1
        country_2.fitness += Δfitness_2

        
        return Δfitness_1,  Δfitness_2, outcome
        
    def check_all_strategies_initialized(self):
        """
        example:
            >>> tournament = Tournament(XXX)
            >>> tournament.check_all_strategies_initialized()
            False
            >>> tournament.init_strategies()
            >>> tournament.check_all_strategies_initialized()
            True
        """
        for country in self.countries():
            if country.get_current_strategy() is None:
                print(f'WARNING: {country} has no initizalized strategy')
        
    def play(self, self_reward, playing_each_other, nr_strategy_changes, mutation_rate):
        """
        parameters:
            - self_reward: function or None, None indicates countries do not get 
                           reward from their internal market, if they do, self_reward
                           should be the function of the country that gives them 
                           self_reward.
            - playing_each_other: bool, if countries play prisoners-dilema's with each
              other, and get/lose fitness from this
            - nr_strategy_changes: int, number of strategy-changes that occura
              after each round
              
        example:
            >>> tournament = Tournament(XXX)
            >>> tournament.init_strategies()
            >>> tournament.play(XXX)
            XXXXXXX
        """
        if self.is_done:
            print("WARNING: you are playing a tournament that has already been played. This will accumulate more"\
                  "data in the graph, which is probably incorrect. You probably want to re-initalize the tournament and"\
                  "countries, or refresh the kernel")
        
        strategies_initialized = self.check_strategies_initialized()
        if not strategies_initialized:
            print(f'All countries mus have initialized strategies, this can be done using the init_strategies method')
            return
        
        #TODO: ad warning for not initializing fitness
        
        for i in range(self.max_rounds):
            #start_t = time.time()
            
            self.round += 1
            print(f'=== ROUND {self.round} ===')
            
            if self_reward:
                # countries get fitness from their own internal market
                for country in self.countries():
                    country.fitness += self_reward(country)
            
            if playing_each_other:
                # this can be switched to False to create a control-simulation for comparison
                for country_1, country_2, data in self.graph.edges(data=True): # data: include edge-attributes in the iteration
                    # todo: we are looping though edges twice.. this could be done only once.
                    self.play_prisoners_dilema(country_1, country_2, data)
                    
                    
            for _ in range(nr_strategy_changes):
                # change {nr_strategy_changes} strategies
                losing_country, winning_strategy = self.change_a_strategy(mutation_rate, self.round)
                
            # update fitness_histories
            for country in self.countries():
                country.fitness_history.append(country.fitness)
                
            if self.one_strategy_left(self.countries_per_strategy_dict()):
                print(f'The process ended in {i+1} rounds\n Winning strategy: {list(self.countries())[0].get_current_strategy().name}')
                break
            
            #end_t = time.time()
            #print(f'    time round: {end_t-start_t} seconds')
            if self.round % 10 == 0:
                for (s,i) in self.countries_per_strategy_dict().items():
                    print(f'    {s.name}: {i}')

        # flag that the tournament has ended
        self.is_done = True
        
            
    def check_strategies_initialized(self):
        """
        check if all countries have a strategy.
        """
        for country in self.countries():
            if country.get_current_strategy() not in self.strategy_list:
                print(f'country {country.name} has strategy {country.get_current_strategy()} which is not in the strategy_list')
                return False
        return True

            
    #Todo: remove initial fitness
    @classmethod
    def create_play_tournament(cls, 
                 countries, 
                 max_rounds, 
                 strategy_list=[defect, cooperate], 
                 payoff_functions=default_payoff_functions, 
                 distance_function = lambda d: d, # defaults to just the identity
                 surveillance_penalty = True,
                 self_reward = selfreward, #default function
                 playing_each_other=True,
                 nr_strategy_changes = 1,
                 mutation_rate =0.1,
                 init_fitnes_as_m=False,
                 noise = 0
                 ):
        """
        Create a tournament, initialize al the variables of the countries and
        then play the tournament.
        
        parameters:
            - countries: list, countries that take part in the tournament
            - max_rounds: int, maximum number of rounds, after which the tournament will stop
            - strategy_list: list, strategies that are played in the tournament
            - payoff_functions: functions to compute the changes in fitness, e.g. `default_payoff_functions` or `traditional_payoff_functions`
            - distance_function: function to rescale the distance. e.g. `lambda d:d` for linear scaleing and `lambda d: math.log(1+d)` for log-scaling
            - surveillance_penalty: bool, if countries should be penalized for playing certain strategies
            - self_reward: function or None, a function if countries should get reward from their internal market each round, 
                           otherwize, if countries should not get reward from their internal market, None
            - playing_each_other: bool, if countries should play prisoners delemma's with each other, set to false to create a control-group
            - nr_strategy_changes: int, number of strategy changes after eacht round
            - mutation_rate: probability that a strategy change is random
            - init_fitnes_as_m: bool, if countries start with self.fitness==self.m or self.fitness==0
        
        returns:
            the tournament object, with data from the simulation inside the
            graph attribute.
            
        example: 
            >>> tournament = Tournament.create_play_tournament(G50, 100, [cooperate, defect, tit_for_tat])
            ..... <code printed during the simulation>
            >>> tournament  # now this Tournament can be used for plotting and analytics
            <UvAAxelrod.tournament.Tournament at 0x7f115d97fcf8>
        """
        tournament = cls(countries, 
                 max_rounds, 
                 strategy_list, 
                 payoff_functions=payoff_functions, # rewards that countries get, defaults to the functions described in the paper.
                 distance_function = distance_function, # defaults to just the identity, if one wanted that distances get less important the larger they are, one could use the sqrt.
                 surveillance_penalty = surveillance_penalty,
                 noise=noise
                 )
        tournament.init_strategies()
        tournament.init_fitness(init_fitnes_as_m=init_fitnes_as_m)
        
        tournament.play(self_reward, playing_each_other, nr_strategy_changes, mutation_rate)
        
        return tournament
        
    
