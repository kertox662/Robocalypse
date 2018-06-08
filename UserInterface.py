from GameObject import *
from getData import loadImage
from Hotbar import Hotbar

class UserInterface(GameObject):
    def __init__(self, screen):
        x = screen.width/2
        hotbarSprite = loadImage("images/UI/Hotbar.png")
        super().__init__(x, screen.height - 25, "img", 0, hotbarSprite, screen, None)
        self.cursorSprite = loadImage("images/UI/cursor.png")
        self.cursorPosition = 1
        self.cursorScreenObj = -1

        screen.root.bind("<KeyPress>", lambda e: self.changeCursorPosition(e))
    
    def display(self):
        self.screen.canv.delete(self.screenObj, self.cursorScreenObj)

        self.screenObj = self.screen.canv.create_image(self.x, self.y, image = self.sprite)
        self.cursorScreenObj = self.screen.canv.create_image(self.x - 133 + 38*self.cursorPosition, self.y, image = self.cursorSprite)
    
    def changeCursorPosition(self, event):
        if event.keysym in ['1','2','3','4','5','6']:
            self.cursorPosition = int(event.keysym)