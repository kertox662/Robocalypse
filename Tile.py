from GameObject import *

tileGridWidth = 50
tileGridHeight = 50

class Tile(GameObject):
    tileWidth = 200
    tileHeight = 200
    def __init__(self, x, y, color, screen, camera, i1, i2):
        super().__init__(x, y, "tile", 0, None, screen, camera)
        self.entities = []
        self.color = color
        self.indexX = i1
        self.indexY = i2
    
    def display(self): #Don't want to use inherited version as it doesn't have a width and height parameter
        self.screen.canv.delete(self.screenObj)
        if self.isOnScreen():
            self.screenObj = self.screen.canv.create_rectangle(self.x - self.camera.x + self.screen.width/2, self.y - self.camera.y + self.screen.height/2, self.x - self.camera.x + Tile.tileWidth + self.screen.width/2, self.y - self.camera.y + Tile.tileHeight + self.screen.height/2, fill = self.color)


