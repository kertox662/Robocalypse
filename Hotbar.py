from GameObject import *
from getData import loadImage

class Hotbar(GameObject):
    def __init__(self, screen, itemSprites):
        x = screen.width/2
        hotbarSprite = loadImage("images/UI/Hotbar.png")
        super().__init__(x, screen.height - 25, "UI", 0, hotbarSprite, screen, None)
        self.cursorSprite = loadImage("images/UI/cursor.png")
        self.cursorPosition = 1
        self.cursorScreenObj = -1
        self.inventory = [0] * 6
        self.invScreenObj = [-1]*6
        self.itemSprites = itemSprites

        screen.root.bind("<KeyPress>", lambda e: self.changeCursorPosition(e))
    
    def display(self):
        self.screen.canv.delete(self.screenObj, self.cursorScreenObj)

        self.screenObj = self.screen.canv.create_image(self.x, self.y, image = self.sprite)
        self.cursorScreenObj = self.screen.canv.create_image(self.x - 133 + 38*self.cursorPosition, self.y, image = self.cursorSprite)

        for i in range(6):
            self.screen.canv.delete(self.invScreenObj[i])
            if self.inventory[i] == 0:
                self.invScreenObj[i] = -1
            else:
                self.invScreenObj[i] = self.screen.canv.create_image(self.x - 133 + 38*(i+1),self.y, image = self.itemSprites[self.inventory[i] - 1])
    
    def changeCursorPosition(self, event):
        if event.keysym in ['1','2','3','4','5','6']:
            self.cursorPosition = int(event.keysym)
    
    def addItem(self, item):
        try:
            self.inventory[self.inventory.index(0)] = item
            return True
        except IndexError:
            return False