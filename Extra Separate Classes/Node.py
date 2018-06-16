class Node:
    def __init__(self,x,y, nodeType):
        self.x = x
        self.y = y
        self.nodeType = nodeType
        self.shortPath = None
    
    @classmethod
    def fromCopy(cls, copy):
        # print(copy.x, copy.y, copy.nodeType)
        newNode = cls(copy.x, copy.y, copy.nodeType)
        return newNode