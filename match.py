
from .game import *

class SelfMatch:
    def __init__(self, selfgame):
        self.selfgame = selfgame
        self.changeInFitness = 0
    ##__str__

    def play(self, turns = 12):
        initialFitness = self.selfgame.country.fitness

        for _ in range(turns):
            self.selfgame.play()

        self.changeInFitness = self.selfgame.country.fitness - initialFitness

        self.selfgame.country.moves = [] #resetting de country's moves for the next match


class Match:
    '''A Match is a series of games between the same two countries, where the countries can react to the previous turns'''

    def __init__(self, game):
        self.game = game
        self.changeInFitness = (0,0)

    def __str__(self):
        return "<" + self.game.__str__() + ">"
    def __repr__(self):
        return "<" + self.game.__str__() + ">"


    def play(self, printing = False, turns = 12, surveillancePenalty = False): #only changes the players and cahngeinfitness
        '''plays a Match'''

        initialFitness = (self.game.country1.fitness, self.game.country2.fitness)


        for _ in range(turns):
            self.game.play(surveillancePenalty = surveillancePenalty)


        if printing: print("match played:" + self.__str__())
        self.changeInFitness = (self.game.country1.fitness - initialFitness[0], self.game.country2.fitness - initialFitness[1])



        #reset the moves that were stored in the game object.
        self.game.country1.moves = []
        self.game.country2.moves = []
