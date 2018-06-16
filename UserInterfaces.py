from getData import *
import sys
from GameSceneObjects import GameObject, Item




class CraftingWindow():
    def __init__(self, screen, hotbar, KH, player):
        self.openWindow = False
        self.x = -112
        self.y = 0
        self.outline = loadImage("images/CraftingWindowOutline2.png")
        self.fill = loadImage("images/CraftingWindowFill2.png")
        self.text = loadImage("images/CraftingWindowText.png")
        self.screen = screen
        self.KH = KH
        self.player = player

        self.screenObjOutline = -1
        self.screenObjFill = -1
        self.screenObjText = -1

        self.itemSprites = Item.itemSprites
        self.itemSpriteHighlights = Item.itemSpriteHighlights
        self.itemData = Item.ItemData
        self.noTableItems = []
        for i in range(len(self.itemData)):
            if self.itemData[str(i+1)]["tableRequired"] == False:
                self.noTableItems.append(str(i+1))
        
        self.listToUse = self.itemData
        
        self.screenObjects = []

        self.currentCostWindow = None
        self.toDoCrafting = False
        self.yMax = (len(self.itemSprites) - 10) * -44


    def display(self):
        self.screen.canv.delete(self.screenObjFill, self.screenObjOutline, self.screenObjText)
        # print(self.screen.width)
        if self.x >= -112:
            self.screenObjFill = self.screen.canv.create_image(self.x, self.screen.height - 253, image = self.fill)
            self.screenObjOutline = self.screen.canv.create_image(self.x, self.screen.height - 253, image = self.outline)
   
            self.displayRecipes()
            self.screenObjText = self.screen.canv.create_image(self.x - 16, self.screen.height - 463, image = self.text)
             
    def displayRecipes(self):
        for i in self.screenObjects:
            self.screen.canv.delete(i)
        self.screenObjects = []
        
        if self.player.nearTable == True:
            self.listToUse = self.itemData
            self.yMax = (len(self.itemSprites) - 10) * -44
        else:
            self.listToUse = self.noTableItems
            self.yMax = 0

        for i in self.listToUse:
            if type(self.listToUse) == dict:
                y = self.screen.height - 460 + self.y + 44*int(i)
            else:
                y = self.screen.height - 460 + self.y + 44*(self.listToUse.index(i) + 1)
            if y > self.screen.height - 462:
                self.screenObjects.append(self.screen.canv.create_image(self.x - 86, y, image = self.itemSprites[int(i) - 1], activeimage = self.itemSpriteHighlights[int(i) - 1]))
                self.screen.canv.tag_bind(self.screenObjects[-1], "<Enter>", self.setCostWindow)
                self.screen.canv.tag_bind(self.screenObjects[-1], "<Leave>", self.resetCostWindow)
                self.screen.canv.tag_bind(self.screenObjects[-1], "<Button-1>", self.initCraftItem)
                
                self.screenObjects.append(self.screen.canv.create_text(self.x, y, text = self.itemData[i]["name"]))

    def setCostWindow(self, event):
        y = event.y
        y -= (self.screen.height - 440 + self.y)
        # print(y)
        indexY = y//44 + 1
        # print(indexY)
        if type(self.listToUse) == dict:
            self.currentCostWindow = self.itemData[str(indexY)]["cost"]
        else:
            self.currentCostWindow = self.itemData[str(self.listToUse[indexY - 1])]["cost"]
    
    def resetCostWindow(self, event):
        self.currentCostWindow = None

    def initCraftItem(self, event):
        y = event.y
        y -= (self.screen.height - 428)
        indexY = y//44 + 1
        if type(self.listToUse) == dict:
            self.toDoCrafting = indexY
        else:
            self.toDoCrafting = int(self.listToUse[indexY - 1])
    
    def changeY(self, event):
        
        if sys.platform == "linux":
            if event.num == 4:
                self.y += 3
            else:
                self.y -= 3
        
        else:
            self.y += event.delta
        
        if self.y >0:
            self.y = 0
        
        elif self.y < self.yMax:
            self.y = self.yMax
            

    def isMouseInWindow(self):
        x = self.KH.mouseX
        y = self.KH.mouseY

        if self.x > -112:
            if 0 <= x <= self.x + 112:
                if self.screen.height - 512 <= y <= self.screen.height:
                    return True
        
        return False


class Hotbar(GameObject):
    def __init__(self, screen, itemSprites):
        
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
            self.inventory[self.inventory.index(0)] = Item(id, 100)
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