import numpy as np
from TernaryPNS import WIN, LOOSE, DRAW, UNKNOWN, BidirPNSNode, iterateBidirSearch

class testState():
    def __init__(self, player):
        self.player = player

    def isOpposite(self):
        return self.player != testState.initial_player

    def evaluate(self):
        self.ch_num = 0
        if np.random.rand() < 0.1:
            return WIN
        elif np.random.rand() < 0.1:
            return LOOSE
        else:
            if np.random.rand() < 0.9:
                self.ch_num = np.random.randint(1,6)
            if self.ch_num == 0:
                return DRAW
            else:
                return UNKNOWN

    def getExpandIterator(self):
        for i in range(self.ch_num):
            yield testState(flip(self.player))

flip = lambda p: [0,2,1][p]

class rootState(testState):
    def __init__(self):
        testState.count = 0
        testState.initial_player = 1
        super().__init__(testState.initial_player)

    def evaluate(self):
        self.ch_num = np.random.randint(2,5)
        return UNKNOWN

def runPnsTest():
    BidirPNSNode.count = 0
    root = BidirPNSNode(rootState())
    iterateBidirSearch(root, max_nodes=1000)
    return root
