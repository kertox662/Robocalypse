from tkinter import *
from getData import *
from PIL import Image, ImageTk, ImageFilter
import sys
from random import *
from math import sqrt

def dist(x1, y1, x2, y2):
    dx = (x2 - x1)**2
    dy = (y2 - y1)**2
    #print(dx, dy)
    l = sqrt(dx + dy)
    
    return l

class GameObject:
    def __init__(self, initx, inity, objType, id, sprite, screen, camera, xOff = 0, yOff = 0):
        self.x = initx
        self.y = inity
        self.type = objType
        self.id = id
        self.screen = screen
        self.camera = camera
        self.sprite = sprite
        self.screenObj = -1
        self.xOff = xOff
        self.yOff = yOff

    def isOnScreen(self, margin = 100):
        if margin*-1 - self.screen.width/2 <= self.x - self.camera.x + self.screen.width/2<= self.screen.width + margin:
            if margin * -1 - self.screen.height/ 2<= self.y - self.camera.y + self.screen.height/2 <= self.screen.height + margin:
                return True
        
        return False
    
    def display(self, player, lessOrGreater, collision, isPlayer = False):
        collisionMid = (min(collision[1]) + max(collision[1]))/2
        playerColDist = min(player.collisionBox[1])
        if (self.y + self.yOff + collisionMid <= player.y + player.yOff + playerColDist) == lessOrGreater or isPlayer == True:
            self.screen.canv.delete(self.screenObj)

        if (self.y + self.yOff + collisionMid <= player.y + player.yOff + playerColDist) == lessOrGreater or isPlayer == True:
            self.screenObj = self.screen.canv.create_image(self.x - self.camera.x + self.xOff + self.screen.width/2, self.y - self.camera.y + self.yOff + self.screen.height/2, image = self.sprite)

        

class Entity(GameObject):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff = 0, yOff = 0):
        if type(sprite) == str:
            img = loadImage(sprite)
        else:
            img = sprite
        super().__init__(x, y, entityType, id, img, screen, camera, xOff, yOff)
        self.collisionBox = collisionBox
        self.doCollision = doCollision
        self.drawnCollision = -1
        self.hitBox = hitBox

        self.rawBox = []
    
    def drawEntityBox(self, box):
        if box == None:
            return

        self.screen.canv.delete(self.drawnCollision)

        self.rawBox = []
        for i in range(len(box[0])):
            self.rawBox.append(self.x + box[0][i] - self.camera.x + self.screen.width/2)
            self.rawBox.append(self.y + box[1][i] - self.camera.y + self.screen.height/2)

        self.drawnCollision = self.screen.canv.create_polygon(*self.rawBox, fill = 'red')
    


class stationaryEntity(Entity):
    def __init__(self, x, y, entityType, id, sprite, animations, screen, camera, collisionBox, doCollision, hitBox, tile, delQueue, xOff = 0, yOff = 0):
        super().__init__(x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff, yOff)
        self.tileX = self.x // Tile.tileWidth
        self.tileY = self.y // Tile.tileHeight
        self.tile = tile
        self.life = randint(25, 50)
        self.dead = False

        self.delQueue = delQueue
        if self.type == "Tree":
            self.falling = False
            self.display = self.treeDisplay
            self.fallAnim = animations[0]
            self.xOff = -43


    def isPointInBox(self, point, boxType, Mouse = False):
        x = point[0]
        y = point[1]

        if Mouse == True:
            bufferX = self.screen.width / 2 - self.camera.x
            bufferY = self.screen.height / 2 - self.camera.y

        else:
            bufferX = 0
            bufferY = 0
        
        # print("X:", min(self.collisionBox[0]) + self.x + self.xOff + bufferX, max(self.collisionBox[0]) + self.x + self.xOff + bufferX)
        # print("Y:", min(self.hitBox[1]) + self.y + self.yOff + bufferY, max(self.hitBox[1]) + self.y + self.yOff + bufferY)

        if boxType == "collision":
            if min(self.collisionBox[0]) + self.x + self.xOff + bufferX <= x <= max(self.collisionBox[0]) + self.x + self.xOff + bufferX:
                if min(self.collisionBox[1]) + self.y + self.yOff + bufferY <= y <= max(self.collisionBox[1]) + self.y + self.yOff + bufferY:
                    return True
        
        elif boxType == "hitbox":
             if min(self.hitBox[0]) + self.x + self.xOff + bufferX <= x <= max(self.hitBox[0]) + self.x + self.xOff + bufferX:
                if min(self.hitBox[1]) + self.y + self.yOff + bufferY <= y <= max(self.hitBox[1]) + self.y + self.yOff + bufferY:
                    return True
        
        
        return False
    
    def checkLife(self):
        if not isinstance(self, GroundItem):
            # print("Life", self.life, self)
            if self.life <= 0 and self.dead == False:
                if self.type == "Tree":
                    # self.fallAnim = loadAnimation("images/Entities/TreeAnim/Falling/", 28)
                    self.animFrame = 0
                    self.falling = True
                    self.dead = True
                    # self.xOff = 
                    print("I'm a dead tree")
                
                else:
                    print("I'm dead")
                    self.dead = True
                    self.delQueue.put(self)
                    
                    
    
    def treeDisplay(self, player, lessOrGreater, collision, isPlayer = False):

        if self.falling:
            self.sprite = self.fallAnim[self.animFrame // 2]
            self.animFrame += 1

        collisionMid = (min(collision[1]) + max(collision[1]))/2
        playerColDist = min(player.collisionBox[1])    

        if (self.y + self.yOff + collisionMid <= player.y + player.yOff + playerColDist) == lessOrGreater or isPlayer == True:
            self.screen.canv.delete(self.screenObj)
            self.screenObj = self.screen.canv.create_image(self.x - self.camera.x + self.xOff + self.screen.width/2, self.y - self.camera.y + self.yOff + self.screen.height/2, image = self.sprite)
        
        if self.falling:
            if self.animFrame // 2 == len(self.fallAnim):
                self.delQueue.put(self)




class movingEntity(Entity):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff = 0, yOff = 0):
        super().__init__(x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff, yOff)
    
    def isColliding(self, colObj):
        box = colObj.collisionBox

        collisions = [False]*8

        if box == None:
            return collisions

        for i in range(len(self.collisionBox[0])):
            # print("MAX:",min(box[1]) - colObj.y, self.collisionBox[1][i] - self.y,"MIN:", max(box[1]) - colObj.y)
            if min(box[0]) + colObj.x <= self.collisionBox[0][i] + self.x <= max(box[0]) + colObj.x:
                if min(box[1]) + colObj.y <= self.collisionBox[1][i] + self.y <= max(box[1]) + colObj.y:
                    collisions[i] = True
                    
        return collisions







class Player(movingEntity):
    playerSpeed = 7
    playerFriction = 0.9

    def __init__(self, x, y, screen, camera, KH, resources):
        # pImg = Image.open()
        # img = ImageTk.PhotoImage(image=pImg)
        super().__init__(x,y,"Player", 0, "images/Robot1.png", screen, camera, ((-25, 0, 25, 25, 25, 0, -25, -25), (20,20,20,35,50,50,50,35)), True, None)#(-25, 0, 25, 25, 25, 0, -25, -25), (20,20,20,35,50,50,50,35)
        self.Velx = 0
        self.Vely = 0
        self.KH = KH
        self.resetX = False
        self.resetY = False
        self.resources = resources
        self.isPlacing = False
        self.nearTable = False

        self.metalHP = 50
        self.metalMaxHP = 50
        self.wireHP = 50
        self.wireMaxHP = 50

        self.metalHPBar = -1
        self.metalHPBarOutline = -1
        self.metalHPText = -1
        self.metalHPIcon = -1

        self.wireHPBar = -1
        self.wireHPBarOutline = -1
        self.wireHPText = -1
        self.wireHPIcon = -1

        self.metalIcon = resources["metal"]["spriteSmall"]
        self.wiresIcon = resources["wires"]["spriteSmall"]

        self.animFrame = 0
        self.direction = ["down"]
        self.previousDirection = self.direction.copy()

        self.downIdleAnim = loadAnimation("images/PlayerAnimation/Idle/Down/", 8)
        self.upIdleAnim = loadAnimation("images/PlayerAnimation/Idle/Up/", 8)
        self.leftIdleAnim = loadAnimation("images/PlayerAnimation/Idle/Left/", 8)
        self.rightIdleAnim = loadAnimation("images/PlayerAnimation/Idle/Right/", 8)

        self.rightdownIdleAnim = loadAnimation("images/PlayerAnimation/Idle/RightDown/", 8)
        self.leftdownIdleAnim = loadAnimation("images/PlayerAnimation/Idle/LeftDown/", 8)
        self.rightupIdleAnim = loadAnimation("images/PlayerAnimation/Idle/RightUp/", 8)
        self.leftupIdleAnim = loadAnimation("images/PlayerAnimation/Idle/LeftUp/", 8)


        self.leftWalkAnim = loadAnimation("images/PlayerAnimation/Walking/Left/", 14)
        self.rightWalkAnim = loadAnimation("images/PlayerAnimation/Walking/Right/", 14)
        self.upWalkAnim = loadAnimation("images/PlayerAnimation/Walking/Up/", 14)
        self.downWalkAnim = loadAnimation("images/PlayerAnimation/Walking/Down/", 14)

        self.leftupWalkAnim = loadAnimation("images/PlayerAnimation/Walking/LeftUp/", 14)
        self.leftdownWalkAnim = loadAnimation("images/PlayerAnimation/Walking/LeftDown/", 14)
        self.rightupWalkAnim = loadAnimation("images/PlayerAnimation/Walking/RightUp/", 14)
        self.rightdownWalkAnim = loadAnimation("images/PlayerAnimation/Walking/RightDown/", 14)
        

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
        
        self.restrictions = [True, True, True, True]

        if self.x - self.camera.x < 0:
            self.restrictions[3] = False
        elif self.x - self.camera.x > 0:
            self.restrictions[2] = False

        if self.y - self.camera.y < 0:
            self.restrictions[1] = False
        elif self.y - self.camera.y > 0:
            self.restrictions[0] = False
        
        self.moveCam(self.restrictions)
        
    
    def applyFriction(self):
        self.Velx *= Player.playerFriction
        self.Vely *= Player.playerFriction

        if self.KH.wToggle == False and self.KH.sToggle == False:
            if abs(self.Vely) < 0.3:
                self.Vely = 0
        
        if self.KH.aToggle == False and self.KH.dToggle == False:
            if abs(self.Velx) < 0.3:
                self.Velx = 0
        

    def moveCam(self, directionRestrictions):
        self.camera.updateVelocity(self.Velx, self.Vely)
        self.camera.move(directionRestrictions, Player.playerSpeed)

    def checkPlayerCollision(self, tiles):
        cTilex = self.x / Tile.tileWidth
        cTiley = self.y / Tile.tileHeight

        cTile = tiles[cTiley][cTilex]
    
    def doStationaryCollisions(self, collisions, entity):
        if True in [collisions[0], collisions[2], collisions[4], collisions[6]] and not True in [collisions[1], collisions[3], collisions[5], collisions[7]]:
            # factors = [1,1]
            xMid = (min(entity.collisionBox[0]) + max(entity.collisionBox[0]) + (entity.x + entity.xOff) * 2) / 2
            yMid = (min(entity.collisionBox[1]) + max(entity.collisionBox[1]) + (entity.y + entity.yOff) * 2) / 2

            collidingCorner = collisions.index(True)

            # self.x -= self.Velx * Player.playerSpeed
            # self.y -= self.Vely * Player.playerSpeed

            if not ((self.x + self.collisionBox[0][collidingCorner] + self.xOff > xMid and self.Velx > 0) or (self.x + self.collisionBox[0][collidingCorner] + self.xOff < xMid and self.Velx < 0)):
                self.x -= self.Velx * Player.playerSpeed
                # factors[0] = -1
                # self.Vely = 0
                self.Vely = self.Vely * -0.8

            if not ((self.y + self.collisionBox[1][collidingCorner] + self.yOff > yMid and self.Vely > 0) or (self.y + self.collisionBox[1][collidingCorner] + self.yOff < yMid and self.Vely < 0)):
                self.y -= self.Vely * Player.playerSpeed
                # factors[1] = -1
                # self.Velx = 0
                self.Velx = self.Velx * -0.8

            # self.moveCam(self.restrictions, -1,-1)
            while True in self.isColliding(entity):
                self.move()

            if abs(self.Velx) < 0.3:
                self.Velx = 0
            if abs(self.Vely) < 0.3:
                self.Vely = 0

            # print("Both")
        elif True in [collisions[1], collisions[5]]:
            # self.y -= self.Vely * Player.playerSpeed
            # self.moveCam(self.restrictions, 1, -1)
            self.Vely = self.Vely * -0.8
            while True in self.isColliding(entity):
                self.move()

            if abs(self.Vely) < 0.3:
                self.Vely = 0

            # self.Vely = 0
            # print("Y")
        elif True in [collisions[3], collisions[7]]:
            # self.x -= self.Velx * Player.playerSpeed
            # self.moveCam(self.restrictions, -1, 1)

            # self.Velx = 0
            self.Velx = self.Velx * -0.8
            while True in self.isColliding(entity):
                self.move()

            if abs(self.Velx) < 0.3:
                self.Velx = 0
            # print("X")
    
    def calculateEvents(self):
        pass
    
    def displayLife(self):
        self.screen.canv.delete(self.wireHPBar, self.wireHPIcon, self.wireHPText, self.wireHPBarOutline)
        self.screen.canv.delete(self.metalHPBar, self.metalHPIcon, self.metalHPText, self.metalHPBarOutline)

        self.metalHPBarOutline = self.screen.canv.create_polygon(9, 29, 9 + max(0,self.metalMaxHP), 29, 14 + max(0,self.metalMaxHP), 35, 14, 35, fill = 'white', outline = 'black', width = 1)
        self.wireHPBarOutline = self.screen.canv.create_polygon(9, 44, 9 + max(0,self.wireMaxHP), 44, 14 + max(0,self.wireMaxHP), 50, 14, 50, fill = 'white', outline = 'black', width = 1)

        self.metalHPBar = self.screen.canv.create_polygon(10, 30, 10 + max(0,self.metalHP), 30, 15 + max(0,self.metalHP), 35, 15, 35, fill = 'red', outline = '', width = 1)
        self.wireHPBar = self.screen.canv.create_polygon(10, 45, 10 + max(0,self.wireHP), 45, 15 + max(0,self.wireHP), 50, 15, 50, fill = 'red', outline = '', width = 1)
        
        self.metalHPIcon = self.screen.canv.create_image(30 + max(0,self.metalMaxHP), 32, image = self.metalIcon)
        self.wireHPIcon = self.screen.canv.create_image(30 + max(0,self.metalMaxHP), 48, image = self.wiresIcon)

        self.metalHPText = self.screen.canv.create_text(65 + max(0,self.metalMaxHP), 32, text = "{}/{}".format(max(0,int(self.metalHP)), self.metalMaxHP))
        self.wireHPText = self.screen.canv.create_text(65 + max(0,self.wireMaxHP), 48, text = "{}/{}".format(max(0,int(self.wireHP)), self.wireMaxHP))

    def checkNearTable(self, tileArray):
        self.nearTable = False
        for i in tileArray:
            for j in i:
                for k in j.entities:
                    if k.type == "Furniture":
                        if k.id == 1:
                            if k.isPlacing == False:
                                if k.dist(self.x, self.y) < 200:
                                    self.nearTable = True
    
    def chooseAnimFrame(self):
        if len(self.direction) > 0:
            self.previousDirection = self.direction.copy()
        self.direction = []
        if self.KH.dToggle == True and self.KH.aToggle == False:
            self.direction.append("right")
        
        elif self.KH.aToggle == True and self.KH.dToggle == False:
            self.direction.append("left")
        
        if self.KH.sToggle == True and self.KH.wToggle == False:
            self.direction.append("down")
        
        elif self.KH.wToggle == True and self.KH.sToggle == False:
            self.direction.append("up")
        
        if len(self.direction) == 0:
            curAnim = eval("self.{}IdleAnim".format("".join(self.previousDirection)))
        
        else:
            curAnim = eval("self.{}WalkAnim".format("".join(self.direction)))
        
        self.animFrame += 1
        id = self.animFrame//3 % len(curAnim)
        self.sprite = (curAnim[id])









tileGridWidth = 10
tileGridHeight = 10

class Tile(GameObject):
    tileWidth = 400
    tileHeight = 400
    def __init__(self, x, y, id, sprite, screen, camera, i1, i2, collisionBox):
        super().__init__(x, y, "tile", id, sprite, screen, camera, xOff = 200, yOff = 200)
        self.entities = []
        self.indexX = i1
        self.indexY = i2
        self.collisionBox = collisionBox
    
    def display(self, camX, camY):
        self.screen.canv.delete(self.screenObj)
        if self.isOnScreen():
            self.screenObj = self.screen.canv.create_image(self.x - camX + self.xOff + self.screen.width/2, self.y - camY + self.yOff + self.screen.height/2, image = self.sprite)


    def isPointInBox(self, point):
        x = point[0]
        y = point[1]

        for i in self.collisionBox:
            if min(i[0]) + self.x<= x <= max(i[0]) + self.x:
                if min(i[1]) + self.y <= y <= max(i[1]) + self.y:
                    return True

        return False
    
    def setNodeMap(self, nMap):
        for i in range(20):
            for j in range(20):
                nMap[i][j] = Node(self.x - 200 + j * 20, self.y - 200 + i*20, nMap[i][j])
        
        self.nodeMap = nMap


class Camera:
    def __init__(self, x, y, screen, KH):
        self.Velx = 0
        self.Vely = 0

        self.x = x
        self.y = y
        self.screen = screen
        self.KH = KH
        
    def updateVelocity(self, velx, vely):
        self.Velx = velx
        self.Vely = vely

    def move(self, dR, speed):
        if dR[0] == False and self.Vely < 0:
            self.Vely = 0
        elif dR[1] == False and self.Vely > 0:
            self.Vely = 0
        
        if dR[2] == False and self.Velx < 0:
            self.Velx = 0
        elif dR[3] == False and self.Velx > 0:
            self.Velx = 0

        self.x += self.Velx * speed
        self.y += self.Vely * speed

        # print(self.screen.width, self.screen.height)

        if self.x < self.screen.width/2:
            self.x = self.screen.width/2
            self.Velx = 0
        elif self.x > Tile.tileWidth * (tileGridWidth-1) - self.screen.width/2:
            self.x = Tile.tileWidth * (tileGridWidth-1) - self.screen.width/2
            self.Velx = 0

        if self.y < self.screen.height/2:
            self.y = self.screen.height/2
            self.Vely = 0
        elif self.y > Tile.tileHeight * (tileGridHeight-1) - self.screen.height/2:
            self.y = Tile.tileHeight * (tileGridHeight-1) - self.screen.height/2
            self.Vely = 0

    def applyFriction(self):
        if self.KH.aToggle == False and self.KH.dToggle == False:
            self.Velx *= Camera.camFriction
        
        if self.KH.wToggle == False and self.KH.sToggle == False:
            self.Vely *= Camera.camFriction

    def setCoords(self, newX, newY):
        self.x = newX
        self.y = newY






class GroundItem(stationaryEntity):
    def __init__(self, x, y, entityType, id, sprite, highlight, screen, camera, resources, tile, player, resourceType, delQueue):
        super().__init__(x,y,entityType, id, sprite, [], screen, camera, None, False, None, tile, delQueue)
        self.resources = resources
        self.player = player
        self.resourceType = resourceType
        self.highlight = highlight

        

    def display(self, player, lessOrGreater, collision, isPlayer = False):
        if lessOrGreater == True:
            self.screen.canv.delete(self.screenObj)
            self.screenObj = self.screen.canv.create_image(self.x - self.camera.x + self.xOff + self.screen.width/2, self.y - self.camera.y + self.yOff + self.screen.height/2, image = self.sprite, activeimage = self.highlight)
            self.screen.canv.tag_bind(self.screenObj, 'e', self.pickUpItem)

    def pickUpItem(self, e):
        # if e.keysym == "e":
        print(e)
        if dist(self.x, self.y, player.x, player.y) < 150:
            self.resources[self.resourceType]["amount"] += randint(1,2)
            
            self.screen.canv.delete(self.screenObj)
            self.tile.entities.remove(self)


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

    def __init__(self, x, y, id, screen, camera, player, tile, delQueue):
        sprite = Furniture.furnitureSprites[int(id) - 1]
        self.highlight = Furniture.furnitureHighlights[int(id) - 1]
        self.spriteRed = Furniture.furnitureSpritesRed[int(id) - 1]
        self.spriteGreen = Furniture.furnitureSpritesGreen[int(id) - 1]

        colBox = Furniture.furnitureData[str(id)]["collision"]

        super().__init__(x,y, "Furniture", id, sprite, [], screen, camera, colBox, False, None, tile, delQueue )

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


class Node:
    def __init__(self,x,y, nodeType):
        self.x = x
        self.y = y
        self.nodeType = nodeType
        self.shortPath = None
    
    @classmethod
    def fromCopy(cls, copy):
        # print(copy.x, copy.y, copy.nodeType)
        newNode = cls(copy.x, copy.y, copy.nodeType)
        return newNode

class Item:
    ItemData = loadSettings("data/items.json")
    itemSprites = []
    itemSpriteHighlights = []
    for i in range(len(ItemData)):
        itemSprites.append(loadImage(ItemData[str(i + 1)]["icon"]))
        itemSpriteHighlights.append(loadImage(ItemData[str(i + 1)]["iconHighlight"]))
    def __init__(self, id, durability):
        self.id = id
        self.name = Item.ItemData[str(id)]["name"]
        self.type = Item.ItemData[str(id)]["type"]
        self.cost = Item.ItemData[str(id)]["cost"]
        self.needTable = Item.ItemData[str(id)]["tableRequired"]
        self.sprite = Item.itemSprites[id - 1]
        self.spriteHighlight = Item.itemSpriteHighlights[id - 1]
        self.durability = durability
        self.screenObj = -1

        if id in [9,10,11]:
            self.furnitureId = Item.ItemData[str(id)]["furnitureID"]