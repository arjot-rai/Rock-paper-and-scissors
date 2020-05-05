class Player:
    def __init__(self, id):
        self.pNo = id
        self.move = ""

    def getMove(self):
        return self.move

    def setMove(self, move):
        self.move = move