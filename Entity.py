from GameObject import *
from PIL import Image, ImageTk
from Tile import Tile
from getData import loadImage

class Entity(GameObject):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff = 0, yOff = 0):
        img = loadImage(sprite)
        super().__init__(x, y, entityType, id, img, screen, camera, xOff, yOff)
        self.collisionBox = collisionBox
        self.doCollision = doCollision
        self.drawnCollision = -1
        self.hitBox = hitBox

        self.rawBox = []
        for i in range(len(collisionBox)):
            self.rawBox.append(collisionBox[i][0])
            self.rawBox.append(collisionBox[i][1])
    
    def drawEntityBox(self, box):
        self.screen.canv.delete(self.drawnCollision)

        self.rawBox = []
        for i in range(len(box[0])):
            self.rawBox.append(self.x + box[0][i] - self.camera.x + self.screen.width/2)
            self.rawBox.append(self.y + box[1][i] - self.camera.y + self.screen.height/2)

        self.drawnCollision = self.screen.canv.create_polygon(*self.rawBox, fill = 'red')
    


class stationaryEntity(Entity):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff = 0, yOff = 0):
        super().__init__(x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff, yOff)
        self.tileX = self.x // Tile.tileWidth
        self.tileY = self.y // Tile.tileHeight


class movingEntity(Entity):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff = 0, yOff = 0):
        super().__init__(x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff, yOff)
    
    def isColliding(self, colObj):
        box = colObj.collisionBox

        collisions = [False]*8

        for i in range(len(self.collisionBox[0])):
            # print("MAX:",min(box[1]) - colObj.y, self.collisionBox[1][i] - self.y,"MIN:", max(box[1]) - colObj.y)
            if min(box[0]) + colObj.x + colObj.xOff <= self.collisionBox[0][i] + self.x <= max(box[0]) + colObj.x + colObj.xOff:
                if min(box[1]) + colObj.y + colObj.yOff <= self.collisionBox[1][i] + self.y <= max(box[1]) + colObj.y + colObj.yOff:
                    collisions[i] = True
                    
        return collisions