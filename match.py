
from .game import *


class Match:
    '''A Match is a series of games between the same two countries, where the countries can react to the previous turns'''

    def __init__(self, game, turns=12):
        self.game = game
        self.turns = turns
        self.summary = [] #
        self.initialFitness = (self.game.country1.fitness, self.game.country2.fitness)
        self.changeInFitness = (0,0)

    def __str__(self):
        return "<" + self.game.__str__() + " " + str(self.turns) + " turns>"
    def __repr__(self):
        return "<" + self.game.__str__() + " " + str(self.turns) + " turns>"


    def play(self, printing = True):
        '''plays a Match'''
        assert(self.game.country1.moves == [])
        assert(self.game.summary == [])

        for _ in range(self.turns):
            self.game.play()

#        if printing: print("match played:" + self.__str__())
        self.changeInFitness = (self.game.country1.fitness - self.initialFitness[0], self.game.country2.fitness - self.initialFitness[1])

        self.summary = self.game.summary

        #reset the moves that were stored in the game object. This information is now contained in self.summary
        self.game.country1.moves = []
        self.game.country2.moves = []
