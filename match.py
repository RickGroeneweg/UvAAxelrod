
from .game import *


class Match:
    '''A Match is a series of games between the same two countries, where the countries can react to the previous turns'''

    def __init__(self, game):
        self.game = game
        self.changeInFitness = (0,0)

    def __str__(self):
        return "<" + self.game.__str__() + " " + str(self.turns) + " turns>"
    def __repr__(self):
        return "<" + self.game.__str__() + " " + str(self.turns) + " turns>"


    def play(self, printing = True, turns = 12): #only changes the players and cahngeinfitness
        '''plays a Match'''
        assert(self.game.country1.moves == [])
        initialFitness = (self.game.country1.fitness, self.game.country2.fitness)


        for _ in range(turns):
            self.game.play()


#        if printing: print("match played:" + self.__str__())
        self.changeInFitness = (self.game.country1.fitness - initialFitness[0], self.game.country2.fitness - initialFitness[1])



        #reset the moves that were stored in the game object.
        self.game.country1.moves = []
        self.game.country2.moves = []
