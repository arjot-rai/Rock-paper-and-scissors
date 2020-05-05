import pygame
from player import *

class Game:
    def __init__(self, id):
        self.id = id
        self.players = [Player(0), Player(1)]
        self.p1Play = False
        self.p2Play = False
        self.bothReady = False
        self.p1win = 0
        self.p2win = 0
        self.quit = False

    def play(self, p, move):
        self.players[int(p)].setMove(move)
        if p == 0:
            self.p1Play = True
        else:
            self.p2Play = True
        if self.p2Play and self.p1Play:
            self.checkWinner()
        else:
            print("Waiting for other player ....")

    def getP1win(self):
        return str(self.p1win)

    def getP2win(self):
        return str(self.p2win)

    def checkWinner(self):
        winner = -1
        if self.players[0].move == "R" and self.players[1].move == "S":
            winner = 0
        elif self.players[0].move == "S" and self.players[1].move == "R":
            winner = 1
        elif self.players[0].move == "P" and self.players[1].move == "R":
            winner = 0
        elif self.players[0].move == "R" and self.players[1].move == "P":
            winner = 1
        elif self.players[0].move == "S" and self.players[1].move == "P":
            winner = 0
        elif self.players[0].move == "P" and self.players[1].move == "S":
            winner = 1

        if winner == 0:
            self.p1win += 1
        elif winner == 1:
            self.p2win += 1

        return winner

    def getPlayerMove(self, p):
        return self.players[p].move

    def bothPlayed(self):
        return self.p1Play and self.p2Play

    def reset(self):
        self.p1Play = False
        self.p2Play = False


    def __str__(self):
        return str("Game id:" + str(self.id))