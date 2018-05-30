from GameObject import *

tileGridWidth = 20
tileGridHeight = 20

class Tile(GameObject):
    tileWidth = 200
    tileHeight = 200
    def __init__(self, x, y, color, screen, camera):
        super().__init__(x, y, "tile", 0, None)
        self.entities = []
        self.color = color
        self.screen = screen
        self.camera = camera
    
    def display(self): #Don't want to use inherited version as it doesn't have a width and height parameter
        self.screen.canv.delete(self.screenObj)
        if self.isOnScreen(self.camera, self.screen):
            self.screenObj = self.screen.canv.create_rectangle(self.x - self.camera.x - Tile.tileWidth/2, self.y - self.camera.y - Tile.tileHeight/2, self.x - self.camera.x + Tile.tileWidth/2, self.y - self.camera.y + Tile.tileHeight/2, fill = self.color)
