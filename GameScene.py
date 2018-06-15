from Tile import *
from GameObject import *
from Scene import Scene
from math import ceil, floor, sqrt
from threading import Thread
from Node import Node

class GameScene(Scene):

    def __init__(self, screen, camera, KHandler, tileArray, player):
        super().__init__("scene_game", screen, KHandler, connections = ["scene_main", "scene_menu"])
        self.camera = camera
        self.screen.root.bind("<Escape>", lambda e: self.change_scene("scene_main"))
        self.tileArray = tileArray
        self.player = player
        self.nodeMap = []
    

    def showTiles(self, tileArray):
        camX = self.camera.x
        camY = self.camera.y
        for i in tileArray:
            for j in i:
                j.display(camX, camY)
    

    def displayStationaryEntities(self, player, lOrG, tileArray):
        for i in tileArray:
            for j in i:
                for k in j.entities:
                    k.display(player, lOrG, k.collisionBox)
    

    def displayStationaryBoxes(self, tileArray, boxType):
        for i in tileArray:
            for j in i:
                for k in j.entities:
                    if boxType == "hitBox":
                        k.drawEntityBox(k.hitBox)
                    elif boxType == "collision":
                        k.drawEntityBox(k.collisionBox)
                        
    
    def checkRendered(self, tileArray):
        for i in tileArray:
            for j in i:
                if not j.isOnScreen():
                    return False
        
        return True
    
    def setRenderGrid(self):
        minX = floor((self.camera.x - self.screen.width/2 - 100) / Tile.tileWidth)
        maxX = ceil((self.camera.x + self.screen.width/2 + 100) / Tile.tileWidth)
        
        minY = floor((self.camera.y - self.screen.height/2 - 100) / Tile.tileHeight)
        maxY = ceil((self.camera.y + self.screen.height/2 + 100) / Tile.tileHeight)

        minX = max(minX, 0)
        maxX = min(maxX, tileGridWidth)

        minY = max(minY, 0)
        maxY = min(maxY, tileGridHeight)

        newRenderArray = []
        for i in self.tileArray[minY:maxY+1]:
            newRenderArray.append([])
            for j in i[minX:maxX + 1]:
                newRenderArray[-1].append(j)

        # print(len(newRenderArray[0]), len(newRenderArray))
        # self.setNodeMap()

        return newRenderArray
    
    def setNodeMap(self):
        mapRow = [0]*len(self.tileArray[0]) * 20
        nodeMap = [mapRow] * len(self.tileArray) * 20
        for i in range(len(nodeMap)):
            for j in range(len(nodeMap[0])):
                xCoor = j * 20
                yCoor = i * 20
                print("Checking Node at position {},{}".format(xCoor, yCoor))
                isBlocked = False

                xIndex = xCoor // 400
                yIndex = yCoor // 400

                for y in range(-1, 2):
                    for x in range(-1, 2):
                        tile = self.tileArray[yIndex + y][xIndex + x]
                        if self.dist(xCoor, tile.x, yCoor, tile.y) < 700:
                            for ent in tile.entities:
                                if ent.isPointInBox([xCoor, yCorr], "collision"):
                                    isBlocked = True
                                    break

                nodeMap[i][j] = Node(xCoor, yCoor, int(isBlocked))
        self.nodeMap = nodeMap


    def dist(self, x1, x2, y1 ,y2):
        dx = (x1 - x2) ** 2
        dy = (y1 - y2) ** 2
        l = sqrt(dx + dy)
        return l

    def doNotification(self):
        pass