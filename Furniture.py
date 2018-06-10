from Entity import stationaryEntity
from getData import *
from math import sqrt


class Furniture(stationaryEntity):
    furnitureData = loadSettings("data/furniture.json")
    
    furnitureSprites = []
    furnitureHighlights = []
    furnitureSpritesRed = []
    furnitureSpritesGreen = []

    for i in range(len(furnitureData)):
        furnitureSprites.append(loadImage(furnitureData[str(i+1)]["furnitureSprite"]))
        furnitureHighlights.append(loadImage(furnitureData[str(i+1)]["furnitureHighlight"]))
        furnitureSpritesRed.append(loadImage(furnitureData[str(i+1)]["furnitureRed"]))
        furnitureSpritesGreen.append(loadImage(furnitureData[str(i+1)]["furnitureGreen"]))

    def __init__(self, x, y, id, screen, camera, player):
        sprite = Furniture.furnitureSprites[int(id) - 1]
        self.highlight = Furniture.furnitureHighlights[int(id) - 1]
        self.spriteRed = Furniture.furnitureSpritesRed[int(id) - 1]
        self.spriteGreen = Furniture.furnitureSpritesGreen[int(id) - 1]

        colBox = Furniture.furnitureData[str(id)]["collision"]

        super().__init__(x,y, "Furniture", id, sprite, screen, camera, colBox, False, None)

        self.player = player
        self.isPlacing = True
        player.isPlacing = True
        
        self.shownSprite = None
        self.shownActive = None

        self.colliding = False
    
    def chooseSprite(self, tileArray):
        self.colliding = False
        self.x = self.player.x + self.player.KH.mouseX - self.screen.width/2
        self.y = self.player.y + self.player.KH.mouseY - self.screen.height/2
        for i in tileArray:
            for j in i:
                for k in j.entities:
                    if self.dist(k.x, k.y) < 400:
                        for p in range(len(k.collisionBox[0])):
                            point = [k.x + k.collisionBox[0][p], k.y + k.collisionBox[1][p]]
                            if self.isPointInBox(point, "collision"):
                                self.colliding = True
        
        if self.dist(self.player.x, self.player.y) < 400:
            # print(dist(self.x, self.player.x, self.y, self.player.y))
            for p in range(len(self.player.collisionBox[0])):
                            point = [self.player.x + self.player.collisionBox[0][p], self.player.y + self.player.collisionBox[1][p]]
                            # print(point)
                            # print(min(self.collisionBox[0]) + self.x + self.xOff, max(self.collisionBox[0]) + self.x + self.xOff)
                            if self.isPointInBox(point, "collision"):
                                self.colliding = True
                            # if self.player.isColliding(self):
                            #     self.colliding = True
        
        if self.colliding == False:
            self.shownSprite = self.spriteGreen
        else:
            self.shownSprite = self.spriteRed

            


    def display(self, player, lessOrGreater, collision):
        if self.isPlacing == False:
            collisionMid = (min(collision[1]) + max(collision[1]))/2
            playerColDist = min(player.collisionBox[1])
            if (self.y + self.yOff + collisionMid <= player.y + player.yOff + playerColDist) == lessOrGreater:
                self.screen.canv.delete(self.screenObj)

        else:
            self.screen.canv.delete(self.screenObj)

        if self.isOnScreen():
            if self.isPlacing == False:
                if (self.y + self.yOff + collisionMid <= player.y + player.yOff + playerColDist) == lessOrGreater:
                    self.screenObj = self.screen.canv.create_image(self.x - self.camera.x + self.xOff + self.screen.width/2, self.y - self.camera.y + self.yOff + self.screen.height/2, image = self.sprite, activeimage = self.highlight)
            else:
                # print(self.player.KH.mouseX - self.camera.x + self.xOff + self.screen.width/2, self.player.KH.mouseY - self.camera.y + self.yOff + self.screen.height/2)
                self.screenObj = self.screen.canv.create_image(self.player.KH.mouseX , self.player.KH.mouseY, image = self.shownSprite)

    
    def dist(self,x,y):
        dx = (self.x - x)**2
        dy = (self.y - y)**2
        l = sqrt(dx + dy)
        return l