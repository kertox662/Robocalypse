from Entity import movingEntity
from PIL import Image, ImageTk
from Tile import *


class Player(movingEntity):
    playerSpeed = 7
    playerFriction = 0.9

    def __init__(self, x, y, screen, camera, KH, resources):
        # pImg = Image.open()
        # img = ImageTk.PhotoImage(image=pImg)
        super().__init__(x,y,"Player", 0, "images/Robot1.png", screen, camera, ((-25, 0, 25, 25, 25, 0, -25, -25), (20,20,20,35,50,50,50,35)), True, None)#(-25, 0, 25, 25, 25, 0, -25, -25), (20,20,20,35,50,50,50,35)
        self.Velx = 0
        self.Vely = 0
        self.KH = KH
        self.resetX = False
        self.resetY = False
        self.resources = resources
    

    def updateVelocity(self):
        if self.KH.aToggle:
            self.Velx += -0.12
        if self.KH.dToggle:
            self.Velx += 0.12
        if self.KH.wToggle:
            self.Vely -= 0.12
        if self.KH.sToggle:
            self.Vely += 0.12
        
        if self.Velx > 1:
            self.Velx = 1
        elif self.Velx < -1:
            self.Velx = -1
        
        if self.Vely > 1:
            self.Vely = 1
        elif self.Vely < -1:
            self.Vely = -1
        
    def move(self):
        self.x += self.Velx * Player.playerSpeed
        self.y += self.Vely * Player.playerSpeed

        if self.x < 0:
            self.x = 0
            self.Velx = 0
        elif self.x > Tile.tileWidth * (tileGridWidth-1):
            self.x = Tile.tileWidth * (tileGridWidth-1)
            self.Velx = 0

        if self.y < 0:
            self.y = 0
            self.Vely = 0
        elif self.y > Tile.tileHeight * (tileGridHeight-1):
            self.y = Tile.tileHeight * (tileGridHeight-1)
            self.Vely = 0
        
        self.restrictions = [True, True, True, True]

        if self.x - self.camera.x < 0:
            self.restrictions[3] = False
        elif self.x - self.camera.x > 0:
            self.restrictions[2] = False

        if self.y - self.camera.y < 0:
            self.restrictions[1] = False
        elif self.y - self.camera.y > 0:
            self.restrictions[0] = False
        
        self.moveCam(self.restrictions)
        
    
    def applyFriction(self):
        # if self.KH.aToggle == False and self.KH.dToggle == False:
        self.Velx *= Player.playerFriction
        
        # if self.KH.wToggle == False and self.KH.sToggle == False:
        self.Vely *= Player.playerFriction
    
    def moveCam(self, directionRestrictions):
        self.camera.updateVelocity(self.Velx, self.Vely)
        self.camera.move(directionRestrictions, Player.playerSpeed)

    def checkPlayerCollision(self, tiles):
        cTilex = self.x / Tile.tileWidth
        cTiley = self.y / Tile.tileHeight

        cTile = tiles[cTiley][cTilex]
    
    def doStationaryCollisions(self, collisions, entity):
        if True in [collisions[0], collisions[2], collisions[4], collisions[6]] and not True in [collisions[1], collisions[3], collisions[5], collisions[7]]:
            # factors = [1,1]
            xMid = (min(entity.collisionBox[0]) + max(entity.collisionBox[0]) + (entity.x + entity.xOff) * 2) / 2
            yMid = (min(entity.collisionBox[1]) + max(entity.collisionBox[1]) + (entity.y + entity.yOff) * 2) / 2

            collidingCorner = collisions.index(True)

            # self.x -= self.Velx * Player.playerSpeed
            # self.y -= self.Vely * Player.playerSpeed

            if not ((self.x + self.collisionBox[0][collidingCorner] + self.xOff > xMid and self.Velx > 0) or (self.x + self.collisionBox[0][collidingCorner] + self.xOff < xMid and self.Velx < 0)):
                self.x -= self.Velx * Player.playerSpeed
                # factors[0] = -1
                # self.Vely = 0
                self.Vely = self.Vely * -0.8

            if not ((self.y + self.collisionBox[1][collidingCorner] + self.yOff > yMid and self.Vely > 0) or (self.y + self.collisionBox[1][collidingCorner] + self.yOff < yMid and self.Vely < 0)):
                self.y -= self.Vely * Player.playerSpeed
                # factors[1] = -1
                # self.Velx = 0
                self.Velx = self.Velx * -0.8

            # self.moveCam(self.restrictions, -1,-1)
            while True in self.isColliding(entity):
                self.move()

            if abs(self.Velx) < 0.3:
                self.Velx = 0
            if abs(self.Vely) < 0.3:
                self.Vely = 0

            # print("Both")
        elif True in [collisions[1], collisions[5]]:
            # self.y -= self.Vely * Player.playerSpeed
            # self.moveCam(self.restrictions, 1, -1)
            self.Vely = self.Vely * -0.8
            while True in self.isColliding(entity):
                self.move()

            if abs(self.Vely) < 0.3:
                self.Vely = 0

            # self.Vely = 0
            # print("Y")
        elif True in [collisions[3], collisions[7]]:
            # self.x -= self.Velx * Player.playerSpeed
            # self.moveCam(self.restrictions, -1, 1)

            # self.Velx = 0
            self.Velx = self.Velx * -0.8
            while True in self.isColliding(entity):
                self.move()

            if abs(self.Velx) < 0.3:
                self.Velx = 0
            # print("X")
    
    def calculateEvents(self):
        pass

        
        



        
