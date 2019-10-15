

class Country:
    """
    stores country hypterparamters, but also state from the simulation
    """
    
    def __init__(self, name, m, location, e, i, area): 
        
        # Variables that stay the same during simulations
        self.name = name
        self.m = m
        self.e = e
        self.i = i
        self.location = location
        self.area = area
        self.self_reward = None
        
        # State variables, not yet initialized since that will be done in the tournament
        self.fitness = None 
        self.fitness_history = []
    
        # private attributes, they should only be changed with `change_strategy`
        self._strategy = None 
        self._evolution = [] 
        
      
    def __str__(self):
        return f'<{self.name}>'
        
    def __repr__(self):
        return f'<{self.name}>'
    

    
    def change_strategy(self, round_num, strategy):
        """
        parameters:
            - round_num: int, round number when the change occured
            - strategy: new strategy that the country adopts
        
        side effects:
            - set self._strategy to the new strategy
            - appends self.evolution
        """
        self._strategy = strategy
        self._evolution.append((round_num, strategy))
        
    def select_action(self, selfmoves, othermoves):
        return self._strategy(selfmoves, othermoves)
    
    def get_current_strategy(self):
        """
        returns:
            - current strategy
        """
        return self._strategy
    
    def set_self_reward(self, function):
        self.self_reward = function(self, self.area)
