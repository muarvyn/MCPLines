from functools import reduce
from TicTacToeSetup import isStraitConnection, getVacationsIterator, isDraw
from TernaryPNS import WIN, LOOSE, DRAW, UNKNOWN, BidirPNSNode, INF2

class PlaySetKey():
    def __init__(self, key_set):
        self.key_set = key_set
        self.hash = reduce(lambda a,b: a^b, map(hash, key_set), 0)
    def __hash__(self):
        return self.hash
    def __eq__(self, another):
        return set(self.key_set) == set(another.key_set)

flip = lambda p: [0,2,1][p]

class TicTacToeState():
    def __init__(self, board, loc, player, depth, parent_key_set):
        self.depth = depth
        self.board = board.copy()
        self.loc = loc
        self.board[loc] = player
        self.player = player
        self.key = PlaySetKey(parent_key_set+[(loc,player)])

    def isOpposite(self):
        return self.player != TicTacToeState.initial_player

    def evaluate(self):
        if isStraitConnection(self.board, self.loc, self.player):
            return [LOOSE,WIN][self.player==TicTacToeState.initial_player]
        elif isDraw(self.board):
            return DRAW
        else:
            return UNKNOWN

    def getKey(self):
        return self.key

    def getExpandIterator(self):
        opposite = flip(self.player)
        for loc in getVacationsIterator(self.board):
            yield TicTacToeState(self.board, loc, opposite, self.depth+1, self.key.key_set)

class TranspositionNode(BidirPNSNode):
    def getExpandIterator(self):
        for child_state in self.state.getExpandIterator():
            node = TranspositionNode.table.get(child_state.getKey())
            if not node:
                node = TranspositionNode(child_state, self)
                TranspositionNode.table[child_state.getKey()] = node
            else:
                node.addParent(self)
                del child_state
            yield node

    def __repr__(self):
        pn = ["", "; pn="+str(self.proof_num)][self.proof_num < INF2]
        dn = ["", "; dn="+str(self.disproof_num)][self.disproof_num < INF2]
        return ["<UNKNOWN","<WIN","<LOOSE","<DRAW"][
                (self.proof_num==0)+((self.disproof_num==0)<<1)+
                (self.proof_num>=INF2 and self.disproof_num>=INF2)*3
            ]+pn+dn+">"

class RenderNode():
    def __init__(self, orig, parent=None):
        self.orig = orig
        if parent:
            parent_key_set = set(parent.orig.state.key.key_set)
        else:
            parent_key_set = set()
        self.loc = next(iter(set(orig.state.key.key_set) - parent_key_set), "root")

    def citer(self):
        return map(lambda orig: RenderNode(orig, self), self.orig.children)

    def __repr__(self):
        return str(self.loc)+"--"+str(self.orig)

def getTicTacToeRootNode(board, loc, player, init_depth):
    BidirPNSNode.count = 0
    TicTacToeState.initial_player = flip(player)
    root = TranspositionNode(TicTacToeState(board, loc, player, init_depth, []))
    TranspositionNode.table = {root.state.getKey():root}
    return root