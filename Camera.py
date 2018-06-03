from Tile import *

class Camera:
    def __init__(self, x, y, screen, KH):
        self.Velx = 0
        self.Vely = 0

        self.x = x
        self.y = y
        self.screen = screen
        self.KH = KH
        
    def updateVelocity(self, velx, vely):
        self.Velx = velx
        self.Vely = vely

    def move(self, dR, speed):
        if dR[0] == False and self.Vely < 0:
            self.Vely = 0
        elif dR[1] == False and self.Vely > 0:
            self.Vely = 0
        
        if dR[2] == False and self.Velx < 0:
            self.Velx = 0
        elif dR[3] == False and self.Velx > 0:
            self.Velx = 0

        self.x += self.Velx * speed
        self.y += self.Vely * speed

        # print(self.screen.width, self.screen.height)

        if self.x < self.screen.width/2:
            self.x = self.screen.width/2
            self.Velx = 0
        elif self.x > Tile.tileWidth * (tileGridWidth-1) - self.screen.width/2:
            self.x = Tile.tileWidth * (tileGridWidth-1) - self.screen.width/2
            self.Velx = 0

        if self.y < self.screen.height/2:
            self.y = self.screen.height/2
            self.Vely = 0
        elif self.y > Tile.tileHeight * (tileGridHeight-1) - self.screen.height/2:
            self.y = Tile.tileHeight * (tileGridHeight-1) - self.screen.height/2
            self.Vely = 0

    def applyFriction(self):
        if self.KH.aToggle == False and self.KH.dToggle == False:
            self.Velx *= Camera.camFriction
        
        if self.KH.wToggle == False and self.KH.sToggle == False:
            self.Vely *= Camera.camFriction

    def setCoords(self, newX, newY):
        self.x = newX
        self.y = newY
