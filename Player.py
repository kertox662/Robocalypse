from GameObject import *
from PIL import Image, ImageTk
from Tile import *

class Player(GameObject):
    playerSpeed = 10
    playerFriction = 0.9

    def __init__(self, x, y, screen, camera, KH):
        pImg = Image.open("images/Robot1.png")
        img = ImageTk.PhotoImage(image=pImg)
        super().__init__(x,y,"img", 0, img, screen, camera, yOff = 15)
        self.Velx = 0
        self.Vely = 0
        self.KH = KH
    

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
        
        restrictions = [True, True, True, True]

        if self.x - self.camera.x < 0:
            restrictions[3] = False
        elif self.x - self.camera.x > 0:
            restrictions[2] = False

        if self.y - self.camera.y < 0:
            restrictions[1] = False
        elif self.y - self.camera.y > 0:
            restrictions[0] = False
        
        self.moveCam(restrictions)
        
    
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



        
