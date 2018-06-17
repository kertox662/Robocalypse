from math import *

def dist(x1, y1, x2, y2):
    dx = (x2 - x1)**2
    dy = (y2 - y1)**2
    #print(dx, dy)
    l = sqrt(dx + dy)
    
    return l


def travel(fromNode, toNode):
    toNode.h = dist(toNode.x, toNode.y, target.x, target.y)
    toNode.g = fromNode.g + 0.5
    toNode.f = toNode.h + toNode.g
    if toNode.shortPath is None:
        # print("New Path")
        toNode.shortPath = fromNode
    else:
        # print("Old Path")
        if fromNode.g < toNode.shortPath.g:
            toNode.shortPath = fromNode
            # print("Overwrote old path")
    toNode.color = 'green'
    
    if toNode not in openNodes:
        for i in range(len(openNodes) - 1, -1 , -1):
            if toNode.f > openNodes[i].f :
                openNodes.insert(i + 1, toNode)
                break
        
        if toNode not in openNodes:
            openNodes.insert(0, toNode)

def goToNext(grid):
    global  openNodes, closedNodes, atEnd
    
    try:
        currentNode = openNodes[0]
    except IndexError:
        atEnd = True
        return False
    
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
    closedNodes.append(currentNode)
    
    if target in openNodes:
        atEnd = True
    
    return True    
       
    
    

def getPath(grid, startx, starty, targetx, targety):
    global atEnd, target, start, openNodes, closedNodes

    openNodes = []
    closedNodes = [] 

    for i in grid:
        for j in i:
            if j.nodeType == 1:
                closedNodes.append(j)
            
            j.shortPath = None

    target = grid[targety][targetx]

    start = grid[starty][startx]
    start.g = 0
    # print("Target:",target.x, target.y)
    start.f = dist(start.x, start.y, target.x, target.y)
    start.nodeType = 0
    openNodes.append(start)

    exploredNode = []
    atEnd = False
    iteration = 0
    while atEnd == False:
        goToNext(grid)
        iteration += 1
        # print(iteration)
        
    try:
        path = [openNodes[0]]
    except:
        path = [start]
        
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
    
    return path