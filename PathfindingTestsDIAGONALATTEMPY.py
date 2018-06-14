from tkinter import *
from time import sleep
from math import *
from random import randint
from time import time

root = Tk()
c = Canvas(root, width = 800, height = 800)
c.pack()

def dist(x1, y1, x2, y2):
    dx = (x2 - x1)**2
    dy = (y2 - y1)**2
    #print(dx, dy)
    l = sqrt(dx + dy)
    
    return l

class Node:
    size = 5
    
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
    toNode.g = fromNode.g + 0.3
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

times = []

def setup():
    global grid, gridSize, target, start, openNodes, closedNodes
    
    openNodes = []
    closedNodes = []    
    
    #grid = possibleGrid
    
    for i in grid:
        for j in i:
            if j.nodeType == 0:
                j.color = 'red'
            
            else:
                closedNodes.append(j)
    
    
    # target = grid[78][78]
    # target.nodeType = 0
    # target.color = 'yellow'
    
    


def gridCreation():
    global grid, gridSize
    gridSize = 160
    grid = []
    for i in range(gridSize):
        grid.append([0]*gridSize)
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            randomID = randint(1,100)
            if randomID < 16:
                grid[i][j] = 1
            #if grid[i][j] == 1:
                color = 'orange'
            else:
                color = 'red'
            tempNode = Node(j,i, color, grid[i][j])
            grid[i][j] = tempNode

def getPath(grid, startx, starty, targetx, targety):
    global atEnd, target, start, openNodes

    target = grid[targety][targetx]

    start = grid[starty][startx]
    start.color = 'yellow'
    start.g = 0
    print("Target:",target.x, target.y)
    start.f = dist(start.x, start.y, target.x, target.y)
    start.nodeType = 0
    openNodes.append(start)

    exploredNode = []
    atEnd = False

    calcStartTime = time()
    while atEnd == False and time() - calcStartTime < 5:
        goToNext()
        #print("Open",openNodes[0].x, openNodes[0].y)
        #for i in closedNodes:
            #print("Closed:", i.x, i.y)
        #print("=====")
        #for i in openNodes:
            #print(i.f, i.x, i.y)
        #print("=====")
    if time() - calcStartTime > 5:
        openNodes = []
    print("Calc End: ",time() - starttime,"seconds")
    try:
        path = [openNodes[0]]
    except:
        print("=====\nError Occured, Resetting...\n=====")
        gridCreation()
        run()
        return
        
    while start not in path:
        path.append(path[-1].shortPath)
        
        if len(path) >= 3:
            for row in grid:
                try:
                    previousXInd = row.index(path[-3])
                    previousYInd = grid.index(row)
                
                except ValueError:
                    pass
                
                try:
                    nextXInd = row.index(path[-1])
                    nextYInd = grid.index(row)
                
                except ValueError:
                    pass
            
            for x in [previousXInd - 1, previousXInd + 1]:
                for y in [previousYInd - 1, previousYInd + 1]:
                    if nextXInd == x and nextYInd == y:
                        path.pop(-2)
    
    # for i in grid:
    #     for j in i:
    #         j.display()
    
    c.update()
    # sleep(3)    
    for i in path:
        i.color = "blue"
        i.display()
    
    c.update()


def run():
    global starttime
    starttime = time()
    print("Start Setup...")
    setup()
    print("Finished Setup after", time() - starttime, "s")
    print("Done Setup\nStarting Calculations...")
    starttime = time()
    getPath(grid, 159, 146, 1, 1)
    print("Finished All")

def runEv(event):
    gridCreation()
    run()


for i in range(20):
    gridCreation()
    iteration = i + 1
    run()

root.bind("<space>", runEv)


print("HERE")
c.mainloop()