from GameObject import *
from PIL import Image, ImageTk
from Tile import Tile
from getData import loadImage

class Entity(GameObject):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff = 0, yOff = 0):
        if type(sprite) == str:
            img = loadImage(sprite)
        else:
            img = sprite
        super().__init__(x, y, entityType, id, img, screen, camera, xOff, yOff)
        self.collisionBox = collisionBox
        self.doCollision = doCollision
        self.drawnCollision = -1
        self.hitBox = hitBox

        self.rawBox = []
    
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

    def isPointInBox(self, point, boxType, Mouse = False):
        x = point[0]
        y = point[1]

        if Mouse == True:
            bufferX = self.screen.width / 2 - self.camera.x
            bufferY = self.screen.height / 2 - self.camera.y

        else:
            bufferX = 0
            bufferY = 0
        
        # print("X:", min(self.collisionBox[0]) + self.x + self.xOff + bufferX, max(self.collisionBox[0]) + self.x + self.xOff + bufferX)
        # print("Y:", min(self.hitBox[1]) + self.y + self.yOff + bufferY, max(self.hitBox[1]) + self.y + self.yOff + bufferY)

        if boxType == "collision":
            if min(self.collisionBox[0]) + self.x + self.xOff + bufferX <= x <= max(self.collisionBox[0]) + self.x + self.xOff + bufferX:
                if min(self.collisionBox[1]) + self.y + self.yOff + bufferY <= y <= max(self.collisionBox[1]) + self.y + self.yOff + bufferY:
                    return True
        
        elif boxType == "hitbox":
             if min(self.hitBox[0]) + self.x + self.xOff + bufferX <= x <= max(self.hitBox[0]) + self.x + self.xOff + bufferX:
                if min(self.hitBox[1]) + self.y + self.yOff + bufferY <= y <= max(self.hitBox[1]) + self.y + self.yOff + bufferY:
                    return True
        
        return False



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