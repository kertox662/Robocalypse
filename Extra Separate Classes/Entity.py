from GameObject import *
from PIL import Image, ImageTk
from Tile import Tile
from getData import *
from random import randint

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
        if box == None:
            return

        self.screen.canv.delete(self.drawnCollision)

        self.rawBox = []
        for i in range(len(box[0])):
            self.rawBox.append(self.x + box[0][i] - self.camera.x + self.screen.width/2)
            self.rawBox.append(self.y + box[1][i] - self.camera.y + self.screen.height/2)

        self.drawnCollision = self.screen.canv.create_polygon(*self.rawBox, fill = 'red')
    


class stationaryEntity(Entity):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, tile, delQueue, xOff = 0, yOff = 0):
        super().__init__(x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff, yOff)
        self.tile = tile
        self.tileX = self.x // Tile.tileWidth
        self.tileY = self.y // Tile.tileHeight
        self.life = randint(25, 50)

        self.delQueue = delQueue
        if self.type == "Tree":
            self.falling = False
            self.display = self.treeDisplay


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
    
    def checkLife(self):
        if self.life <= 0:
            if self.type == "Tree":
                self.fallAnim = loadAnimation("images/Entities/TreeAnim/Falling/", 28)
                self.animFrame = 0
                self.falling = True
                print("I'm a dead tree")
            
            else:
                self.delQueue.put(self)
                print("I'm dead")
    
    def treeDisplay(self, player, lessOrGreater, collision, isPlayer = False):

        if self.falling:
            self.sprite = self.fallAnim[self.animFrame]
            self.animFrame += 1

        collisionMid = (min(collision[1]) + max(collision[1]))/2
        playerColDist = min(player.collisionBox[1])    

        if (self.y + self.yOff + collisionMid <= player.y + player.yOff + playerColDist) == lessOrGreater or isPlayer == True:
            self.screen.canv.delete(self.screenObj)
            self.screenObj = self.screen.canv.create_image(self.x - self.camera.x + self.xOff + self.screen.width/2, self.y - self.camera.y + self.yOff + self.screen.height/2, image = self.sprite)
        
        if self.falling:
            if self.animFrame == len(self.fallAnim):
                self.delQueue.put(self)




class movingEntity(Entity):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff = 0, yOff = 0):
        super().__init__(x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff, yOff)
    
    def isColliding(self, colObj):
        box = colObj.collisionBox

        collisions = [False]*8

        if box == None:
            return collisions

        for i in range(len(self.collisionBox[0])):
            # print("MAX:",min(box[1]) - colObj.y, self.collisionBox[1][i] - self.y,"MIN:", max(box[1]) - colObj.y)
            if min(box[0]) + colObj.x + colObj.xOff <= self.collisionBox[0][i] + self.x <= max(box[0]) + colObj.x + colObj.xOff:
                if min(box[1]) + colObj.y + colObj.yOff <= self.collisionBox[1][i] + self.y <= max(box[1]) + colObj.y + colObj.yOff:
                    collisions[i] = True
                    
        return collisions
