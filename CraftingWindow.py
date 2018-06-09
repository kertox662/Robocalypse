from getData import loadImage

class CraftingWindow():
    def __init__(self, screen, hotbar):
        self.openWindow = False
        self.x = -192
        self.y = 0
        self.outline = loadImage("images/CraftingWindowOutline2.png")
        self.fill = loadImage("images/CraftingWindowFill2.png")
        self.text = loadImage("images/CraftingWindowText.png")
        self.screen = screen

        self.screenObjOutline = -1
        self.screenObjFill = -1
        self.screenObjText = -1

        self.itemSprites = hotbar.Item.itemSprites
        self.itemData = hotbar.Item.ItemData
        self.noTableItems = []
        for i in self.itemData:
            if self.itemData[i]["tableRequired"] == False:
                self.noTableItems.append(i)
        print(self.noTableItems)
        
        self.screenObjects = []

        self.currentCostWindow = None

    def display(self):
        self.screen.canv.delete(self.screenObjFill, self.screenObjOutline, self.screenObjText)
        # print(self.screen.width)
        if self.x >= -112:
            self.screenObjOutline = self.screen.canv.create_image(self.x, self.screen.height - 256, image = self.outline)
            self.screenObjFill = self.screen.canv.create_image(self.x, self.screen.height - 256, image = self.fill)
            self.screenObjText = self.screen.canv.create_image(self.x, self.screen.height - 256, image = self.text)

            self.displayRecipes()
    
    def displayRecipes(self):
        print(self.currentCostWindow)
        for i in self.screenObjects:
            self.screen.canv.delete(i)
        self.screenObjects = []
        for i in self.itemData:
            y = self.screen.height - 448 + self.y + 44*int(i)
            self.screenObjects.append(self.screen.canv.create_image(self.x - 86, y, image = self.itemSprites[int(i) - 1]))
            self.screen.canv.tag_bind(self.screenObjects[-1], "<Enter>", self.setCostWindow)
            self.screen.canv.tag_bind(self.screenObjects[-1], "<Leave>", self.resetCostWindow)
            
            self.screenObjects.append(self.screen.canv.create_text(self.x, y, text = self.itemData[i]["name"]))
            
    

    def setCostWindow(self, event):
        y = event.y
        y -= (self.screen.height - 428)
        # print(y)
        indexY = y//44 + 1
        # print(indexY)
        self.currentCostWindow = self.itemData[str(indexY)]["cost"]
    
    def resetCostWindow(self, event):
        self.currentCostWindow = None



    
    