from tkinter import *
from time import sleep
from math import *
from random import randint

root = Tk()
c = Canvas(root, width = 1000, height = 1000)
c.pack()

def dist(x1, y1, x2, y2):
    dx = (x2 - x1)**2
    dy = (y2 - y1)**2
    #print(dx, dy)
    l = sqrt(dx + dy)
    
    return l

class Node:
    size = 10
    
    def __init__(self,x,y, color, nodeType):
        self.x = x
        self.y = y
        self.color = color
        self.screenOBJ = -1
        self.nodeType = nodeType
        self.shortPath = None
    
    def display(self):
        c.delete(self.screenOBJ)
        self.screenOBJ = c.create_rectangle(self.x * Node.size, self.y*Node.size, (self.x + 1)*Node.size, (self.y + 1)*Node.size, fill = self.color, outline = self.color)
    
    def toggleId():
        pass

possibleGrid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
                [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1],
                [1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
                [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
                [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
                [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]




def travel(fromNode, toNode):
    #print("Target:",target.x, target.y)
    #print("Node Coor:",toNode.x, toNode.y)
    toNode.h = dist(toNode.x, toNode.y, target.x, target.y)
    toNode.g = fromNode.g + 1
    toNode.f = toNode.h + toNode.g
    if toNode.shortPath == None:
        toNode.shortPath = fromNode
    else:
        if fromNode.g < toNode.shortPath.g:
            toNode.shortPath = fromNode
    toNode.color = 'green'
    
    if toNode not in openNodes:
        for i in range(len(openNodes) - 1, -1 , -1):
            #print("i:",i)
            if toNode.f > openNodes[i].f :
                openNodes.insert(i + 1, toNode)
                #print("insert")
                break
        
        if toNode not in openNodes:
            openNodes.insert(0, toNode)

def goToNext():
    global grid, openNodes, closedNodes, atEnd
    
    try:
        currentNode = openNodes[0]
    except IndexError:
        atEnd = True
        return False
    
    #print("Using NODE:", currentNode.x, currentNode.y, currentNode.f)
    
    for i in grid:
        try:
            xInd = i.index(currentNode)
            yInd = grid.index(i)
            break
        except ValueError:
            pass
    
    
    if xInd != 0:
        toNode = grid[yInd][xInd - 1]
        if toNode.nodeType == 0 and toNode not in closedNodes:
            travel(currentNode, toNode)
    
    if xInd != len(grid[0]) - 1:
        toNode = grid[yInd][xInd + 1]
        if toNode.nodeType == 0 and toNode not in closedNodes:
            travel(currentNode, toNode)
    
    if yInd != 0:
        toNode = grid[yInd-1][xInd]
        if toNode.nodeType == 0 and toNode not in closedNodes:
            travel(currentNode, toNode)
    
    if yInd != len(grid) - 1:
        toNode = grid[yInd + 1][xInd]
        if toNode.nodeType == 0 and toNode not in closedNodes:
            travel(currentNode, toNode)
    
    
    
    openNodes.remove(currentNode)
    #print(openNodes)
    closedNodes.append(currentNode)
    
    if target in openNodes:
        atEnd = True
    
    return True


def setup():
    global grid, gridSize, target, start, openNodes, closedNodes
    gridSize = 100
    grid = []
    for i in range(gridSize):
        grid.append([0]*gridSize)
    
    openNodes = []
    closedNodes = []    
    
    #grid = possibleGrid
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            randomID = randint(1,100)
            if randomID < 36:
                grid[i][j] = 1
            #if grid[i][j] == 1:
                color = 'orange'
            else:
                color = 'red'
            tempNode = Node(j,i, color, grid[i][j])
            if tempNode.nodeType != 0:
                closedNodes.append(tempNode)
            grid[i][j] = tempNode
    
    
    target = grid[94][98]
    target.nodeType = 0
    target.color = 'yellow'
    
    start = grid[1][1]
    start.color = 'yellow'
    start.g = 0
    start.f = dist(start.x, start.y, target.x, target.y)
    start.nodeType = 0
    openNodes.append(start)




def getPath():
    global atEnd
    exploredNode = []
    atEnd = False
    while atEnd == False:
        goToNext()
        
        #print("Open",openNodes[0].x, openNodes[0].y)
        #for i in closedNodes:
            #print("Closed:", i.x, i.y)
        #print("=====")
        #for i in openNodes:
            #print(i.f, i.x, i.y)
        #print("=====")
    try:
        path = [openNodes[0]]
    except:
        print("=====\nError Occured, Resetting...\n=====")
        run()
        return
        
    while start not in path:
        #print("Path",path)
        path.append(path[-1].shortPath)
        #print("Path")
        #for node in path:
            #print(node.x, node.y)
    
    print("Done Calculations\nStarting Graphics...")
    
    for i in grid:
        for j in i:
            j.display()
            c.update()
    
    for i in path:
        i.color = "blue"
        i.display()
    
    c.update()


def run():
    print("Start Setup...")
    setup()
    print("Done Setup\nStarting Calculations...")
    getPath()
    print("Finished All")

def runEv(event):
    run()

run()

root.bind("<space>", runEv)


print("HERE")
c.mainloop()