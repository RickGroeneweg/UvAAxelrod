from enum import Enum
import numpy as np


class Action(Enum): 
    """C for Collaborate, D for Defect"""
    C=1
    D=0
C = Action.C
D = Action.D

outcomes_dict = {(C, C): 'RR', (C,D): 'ST', (D,C): 'TS', (D,D): 'PP'}
def to_outcome(action_1, action_2):
    '''
    return string that is the outcome of the two actions
    
    parameters:
        action_1, action_2: Action
        
    example:
        >>> to_outcome(Action.D, Action.C)
        'TS'    
        >>> to_outcome(Action.C, Action.C)
        'RR'
    '''
    assert action_1 == C or action_1 == D
    return outcomes_dict[(action_1, action_2)]

def random_action():
    """
    retruns: 
        - C of D at random
        
    example:
        >>> random_action()
        <Action.C>
        >>> random_action()
        <Action.D>
    """
    return np.random.choice([C, D])