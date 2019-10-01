from anytree import RenderTree, ContStyle

class XRenderTree(RenderTree):
    def __init__(self, node, style=ContStyle(), childiter=lambda x:iter(x),
                 nodeiter = lambda node: node.children):
        super().__init__(node, style, childiter)
        self.nodeiter = nodeiter

    def _RenderTree__next(self, node, continues):
        yield RenderTree._RenderTree__item(node, continues, self.style)
        it = self.childiter(self.nodeiter(node))
        child = next(it, None)
        while child:
            next_child = next(it, None)
            for grandchild in self._RenderTree__next(child, continues + (next_child != None, )):
                yield grandchild
            child = next_child
