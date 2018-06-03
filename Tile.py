from GameObject import *
from PIL import Image, ImageTk

tileGridWidth = 50
tileGridHeight = 50

class Tile(GameObject):
    tileWidth = 400
    tileHeight = 400
    def __init__(self, x, y, sprite, screen, camera, i1, i2):
        super().__init__(x, y, "tile", 0, sprite, screen, camera, xOff = 100, yOff = 100)
        self.entities = []
        self.indexX = i1
        self.indexY = i2
    
    def display(self, camX, camY):
        self.screen.canv.delete(self.screenObj)
        if self.isOnScreen():
            if self.type == "img" or self.type == 'tile':
                self.screenObj = self.screen.canv.create_image(self.x - camX + self.xOff + self.screen.width/2, self.y - camY + self.yOff + self.screen.height/2, image = self.sprite)


