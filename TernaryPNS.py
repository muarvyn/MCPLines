import sys

INF = float('inf')
class ProofNumberNode:
    def __init__(self, is_and, pn, dn):
        self.is_and = is_and
        self.expanded = not (pn==1 and dn==1)
        self.proof_num = pn
        self.disproof_num = dn
        self.children = []

    def isAnd(self):
        return self.is_and

    def isExpanded(self):
        return self.expanded

    def update(self):
        if len(self.children) == 0: return
        if not self.is_and:
            self.disproof_num = 0
            self.proof_num = INF
            for child in self.children:
                self.disproof_num += child.disproof_num
                self.proof_num = min(child.proof_num, self.proof_num)
        else:
            self.proof_num = 0
            self.disproof_num = INF
            for child in self.children:
                self.proof_num += child.proof_num
                self.disproof_num = min(child.disproof_num, self.disproof_num)

    def expand(self):
        self.no_expansion = self.expanded
        if self.no_expansion: return
        self.expanded = True
        it = self.getExpandIterator()
        for child in it:
            shortcut = child.proof_num == 0 and not self.is_and or \
               child.disproof_num == 0 and self.is_and
            self.children.append(child)
            if shortcut: break

    def __repr__(self):
        return "<Type: "+["OR","AND"][self.is_and]+"; pn:"+str(self.proof_num)+ \
            "; dn:"+str(self.disproof_num)+"; "+["","expd "][self.expanded]+ \
            str(len(self.children))+" ch>"

INF2 = sys.maxsize
UNKNOWN = 0
WIN = 1
LOOSE = 2
DRAW = 3

class BidirPNSNode(ProofNumberNode):
    def __init__(self, state, parent=None):
        self.state = state
        is_and = not self.state.isOpposite()
        #       UNKNOWN  WIN    LOOSE     DRAW
        pn,dn = [(1,1),(0,INF),(INF,0),(INF2,INF2)][self.state.evaluate()]
        super().__init__(is_and, pn, dn)
        self.parents = []
        if parent:
            self.parents.append(parent)
        BidirPNSNode.count += 1

    def addParent(self, parent):
        if not parent in self.parents:
            self.parents.append(parent)

    def update(self):
        pn = self.proof_num
        dn = self.disproof_num
        super().update()
        if pn == self.proof_num and dn == self.disproof_num:
            return
        for parent in self.parents:
            parent.update()

    getExpandIterator = lambda self: map(lambda child_state: BidirPNSNode(child_state, self),
                                         self.state.getExpandIterator())

def seekMPN(node):
    while node.isExpanded():
        select = None
        if node.isAnd():
            dn = INF
            for child in node.children:
                if child.disproof_num <= dn:
                    dn = child.disproof_num
                    select = child
        else:
            pn = INF
            for child in node.children:
                if child.proof_num <= pn:
                    pn = child.proof_num
                    select = child
        if not select:
            break
        node = select

    return node

def iterateBidirSearch(root, max_iterations=None, max_nodes=None):
    n=0
    while (not max_nodes or root.count < max_nodes) and \
        (not max_iterations or n < max_iterations):
        MPN = seekMPN(root)
        MPN.expand()
        MPN.update()

        if MPN.no_expansion:
            print("\nNo expansion. Search terminated.")
            break
        if root.proof_num == 0:
            print("\nprooved")
            break
        elif root.disproof_num == 0:
            print("\ndisprooved")
            break
        else:
            n += 1
            print("\rIteration {:4}: nodes count is {:5}".format(n,root.count), 
                  flush=True, end='')
    print("\nIterations performed: {:4}; nodes created: {:5}".format(n,root.count))
