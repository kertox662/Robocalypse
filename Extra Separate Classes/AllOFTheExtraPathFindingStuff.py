def doPathFindingCalc():
    while True:
        if Scene.current_scene == "scene_game":
            for i in enemies:
                
                if player.x != i.prevPlayerX or player.y != i.prevPlayerY or True:
                    listInd = enemies.index(i)

                    xInd = int(i.x // Tile.tileWidth)
                    yInd = int(i.y // Tile.tileHeight)

                    myTile = tileGrid[yInd][xInd]
                    
                    tileXpossibilities = [-1, 0, 1]
                    tileYpossibilities = [-1, 0, 1]
                    

                    playerTileX = int(player.x // 400)
                    playerTileY = int((player.y ) // 400)#+ (min(player.collisionBox[1]) + max(player.collisionBox[1]))/2 )// 400)

                    playerTile = tileGrid[playerTileY][playerTileX]



                    for j in tileGrid:
                        for k in j:
                            k.nodeType = 0
                    i.findShortestPath(tileGrid, [playerTileX, playerTileY], player, myTile)
                    if i.path[0] == myTile:
                        i.path.pop(0)
                    
                    i.prevPlayerX = player.x
                    i.prevPlayerY = player.y
                    print("Set New Path")
            
        sleep(0.1)


class Enemy(movingEntity):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox):
        super().__init__(x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox)
        self.path = []
        self.baseSpeed = 4
        self.onPlayerTile = False
        self.prevPlayerX = None
        self.prevPlayerY = None
    
    def findShortestPath(self, grid, target, player, tile):
        x = self.x - grid[0][0].x
        y = self.y - grid[0][0].y


        print(int(x // 400), int(y // 400))
        print(target[0],target[1])
        startNode = grid[int(y // 400)][int(x // 400)]
        targetNode = grid[target[1]][target[0]]

        print("CHECKING:", startNode == tile)

        self.onPlayerTile = False
        if startNode == targetNode:
            self.onPlayerTile = True
        print(self.onPlayerTile)
        
        # self.onPlayerTile = False

        if self.onPlayerTile == False:
            if startNode.nodeType == 1:
                toBreak = False
                for i in range(-1,2):
                    for j in range(-1, 2):
                        if grid[int(y // 400) + i][int(x // 400) + j].nodeType == 0:
                            startNode = grid[int(y // 400) + i][int(x // 400) + j]

            self.path = list(reversed(getPath(grid, int(startNode.x // 400), int(startNode.y // 400), target[0], target[1])))
            
        
        else:
            # startNode
            startNodeX = int((self.x - targetNode.x) // 20)
            startNodeY = int((self.y - targetNode.y) // 20)
            # print("Start:",startNodeX, startNodeY)
            # print(targetNode.nodeMap[startNodeY][startNodeX].x , targetNode.nodeMap[startNodeY][startNodeX].y)

            playerNodeX = int((player.x - targetNode.x) // 20)
            playerNodeY = int((player.y - targetNode.y) // 20)
            
            # print("Player Node at:", playerNodeX, playerNodeY)
            # print(targetNode.nodeMap[playerNodeY][playerNodeX].x , targetNode.nodeMap[playerNodeY][playerNodeX].y)

            # print("Target Index:",target)
            for i in range(len(grid)):
                try:
                    xInd = grid[i].index(targetNode)
                    yInd = i
                    break
                
                except:
                    xInd, yInd = None, None

            # print("Target Actual:", xInd, yInd)

            self.path = list(reversed(getPath(targetNode.nodeMap, startNodeX, startNodeY, playerNodeX, playerNodeY)))
        
        while len(self.path) >= 2:
            if dist(self.x, self.path[0].x, self.y, self.path[0].y) > dist(self.x, self.path[1].x, self.y, self.path[1].y):
                self.path.pop(0)
            else:
                break
    
    def move(self, player):
        if not self.onPlayerTile:
            buffer = 210
        else:
            buffer = 10
        
        angle = atan2(self.path[0].y - self.y + buffer , self.path[0].x - self.x + buffer)
        # print("Going To:", self.path[0].x + buffer, self.path[0].y + buffer)
        # print("Agent:", self.x, self.y)
        # print("Player:", player.x, player.y)


        # angle = atan2(player.y - self.y, player.x -self.x)

        self.x += self.baseSpeed * cos(angle)
        self.y += self.baseSpeed * sin(angle)

        # print(self.x, self.y)
    
    def distFromPath(self):
        dx = (self.x - self.path[0].x)**2
        dy = (self.y - self.path[0].y)**2
        l = sqrt(dx + dy)
        return l
    
    def removeNodeFromPath(self):
        if self.distFromPath() < 5:
            self.path.pop(0)
    
    def display(self):
        self.screen.canv.delete(self.screenObj)
        bufferX = self.screen.width / 2 - self.camera.x
        bufferY = self.screen.height / 2 - self.camera.y
        self.screenObj = self.screen.canv.create_rectangle(self.x - 10 + bufferX, self.y - 10 + bufferY, self.x + 10 + bufferX, self.y + 10 + bufferY, fill = 'white')
    
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
    



def setNodeMap(self, nMap):
        for i in range(20):
            # print(self.y, self.y + i*20)
            for j in range(20):
                nMap[i][j] = Node(self.x + j * 20, self.y + i*20, nMap[i][j])
        self.nodeMap = nMap



curTile.setNodeMap(entityArrangement[0])

                # curTile.setNodeMap([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

            else:
                curTile.setNodeMap([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

def nodeMapFromTiles(grid):
    nMap = []
    for i in range(len(grid)*20):
        nMap.append([])

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            curTile = grid[i][j]
            for y in range(len(curTile.nodeMap)):
                for x in range(len(curTile.nodeMap[0])):
                    setToNode = Node.fromCopy(curTile.nodeMap[y][x])
                    nMap[y + i*20].append(setToNode)
                
    
    return nMap