from Tile import *

class Camera:
    camSpeed = 10

    def __init__(self, screen, KH):
        self.Velx = 0
        self.Vely = 0

        self.x = screen.width/2
        self.y = screen.height/2
        self.screen = screen
        self.KH = KH
        
    def updateVelocity(self):
        if self.KH.aToggle:
            self.Velx += -0.1
        if self.KH.dToggle:
            self.Velx += 0.1
        if self.KH.wToggle:
            self.Vely -= 0.1
        if self.KH.sToggle:
            self.Vely += 0.1
        
        if self.Velx > 1:
            self.Velx = 1
        elif self.Velx < -1:
            self.Velx = -1
        
        if self.Vely > 1:
            self.Vely = 1
        elif self.Vely < -1:
            self.Vely = -1


    def move(self):
        self.x += self.Velx * Camera.camSpeed
        self.y += self.Vely * Camera.camSpeed

        # print(self.screen.width, self.screen.height)

        if self.x < self.screen.width/2:
            self.x = self.screen.width/2
            self.Velx = 0
        elif self.x > Tile.tileWidth * tileGridWidth - self.screen.width:
            self.x = Tile.tileWidth * tileGridWidth - self.screen.width
            self.Velx = 0

        if self.y < self.screen.height/2:
            self.y = self.screen.height/2
            self.Vely = 0
        elif self.y > Tile.tileHeight * tileGridHeight - self.screen.height:
            self.y = Tile.tileHeight * tileGridHeight - self.screen.height
            self.Vely = 0

    def setCoords(self, newX, newY):
        self.x = newX
        self.y = newY
