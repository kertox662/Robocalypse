from GameObject import *
from PIL import Image, ImageTk
from Node import Node

tileGridWidth = 10
tileGridHeight = 10

class Tile(GameObject):
    tileWidth = 400
    tileHeight = 400
    def __init__(self, x, y, id, sprite, screen, camera, i1, i2, collisionBox):
        super().__init__(x, y, "tile", id, sprite, screen, camera, xOff = 200, yOff = 200)
        self.entities = []
        self.indexX = i1
        self.indexY = i2
        self.collisionBox = collisionBox
    
    def display(self, camX, camY):
        self.screen.canv.delete(self.screenObj)
        if self.isOnScreen():
            self.screenObj = self.screen.canv.create_image(self.x - camX + self.xOff + self.screen.width/2, self.y - camY + self.yOff + self.screen.height/2, image = self.sprite)


    def isPointInBox(self, point):
        x = point[0]
        y = point[1]

        for i in self.collisionBox:
            if min(i[0]) + self.x + self.xOff <= x <= max(i[0]) + self.x + self.xOff:
                if min(i[1]) + self.y + self.yOff <= y <= max(i[1]) + self.y + self.yOff:
                    return True

        return False
    
    def setNodeMap(self, nMap):
        for i in range(20):
            for j in range(20):
                nMap[i][j] = Node(self.x - 200 + j * 20, self.y - 200 + i*20, nMap[i][j])
        
        self.nodeMap = nMap
    
