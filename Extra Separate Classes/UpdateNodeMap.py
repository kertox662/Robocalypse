from GameSceneObjects import Node

def findMap(grid, entities):
    for eY in range(20):
        for eX in range(20):
            for ent in entities:
                x = eX*20
                y = eY*20
                # print(x,y)
                grid[eY][eX] = Node(x, y ,int(ent.isPointInBox([x + grid[0][0].x, y + grid[0][0].y], "collision")))
                if grid[eY][eX].nodeType == 1:
                    break
    
    for i in grid[0]:
        i.nodeType = 0
    
    for i in grid[-1]:
        i.nodeType = 0
    
    for i in grid[1:-1]:
        i[0].nodeType = 0
        i[-1].nodeType = 0

    return grid
