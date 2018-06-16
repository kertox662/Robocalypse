from GameObject import *
from getData import loadImage
import sys

class Hotbar(GameObject):
    def __init__(self, screen, itemSprites):
        import Item
        self.Item = Item.Item
        x = screen.width/2
        y = screen.height - 25
        hotbarSprite = loadImage("images/UI/Hotbar.png")
        super().__init__(x, y, "UI", 0, hotbarSprite, screen, None)
        self.cursorSprite = loadImage("images/UI/cursor.png")
        self.cursorPosition = 1
        self.cursorScreenObj = -1
        self.inventory = [0] * 6
        self.invScreenObj = [-1]*6
        self.lockCursor = False

        screen.root.bind("<KeyPress>", self.changeCursorPosition)
    
    def display(self):
        self.screen.canv.delete(self.screenObj, self.cursorScreenObj)

        self.screenObj = self.screen.canv.create_image(self.x, self.y, image = self.sprite)
        self.cursorScreenObj = self.screen.canv.create_image(self.x - 133 + 38*self.cursorPosition, self.y, image = self.cursorSprite)

        for i in self.inventory:
            if i != 0:
                self.screen.canv.delete(i.screenObj)
                i.screenObj = self.screen.canv.create_image(self.x - 133 + 38*(self.inventory.index(i)+1),self.y, image = i.sprite)
    
    def changeCursorPosition(self, event):
        if not self.lockCursor:
            if event.keysym in ['1','2','3','4','5','6']:
                self.cursorPosition = int(event.keysym)
    
    def addItem(self, id):
        try:
            self.inventory[self.inventory.index(0)] = self.Item(id, 100)
            return True
        except ValueError:
            return False
    
    def changeCursorPositionScroll(self,event):
        if sys.platform == "linux":
            if event.num == 4:
                delta = 1
            else:
                delta = -1
        
        else:
            delta = event.delta
        
        if not self.lockCursor:
            if delta < 0:
                self.cursorPosition = (self.cursorPosition + 1) % 7
                if self.cursorPosition == 0:
                    self.cursorPosition = 1

            
            else:
                self.cursorPosition = self.cursorPosition - 1
                if self.cursorPosition < 1:
                    self.cursorPosition = 6