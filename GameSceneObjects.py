from tkinter import *
from getData import *
from PIL import Image, ImageTk, ImageFilter
import sys
from random import *
from math import *

#Distance formula
def dist(x1, y1, x2, y2):
    dx = (x2 - x1)**2
    dy = (y2 - y1)**2
    l = sqrt(dx + dy)
    
    return l

class GameObject: #Base object for many of the other object
                    # It holds information about itself, as well as the memory locations of complementary objects such as screen and camera
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

    def isOnScreen(self, margin = 100): #Sees if the coordinates are in the range of the screen
        if margin*-1 - self.screen.width/2 <= self.x - self.camera.x + self.screen.width/2<= self.screen.width + margin:
            if margin * -1 - self.screen.height/ 2<= self.y - self.camera.y + self.screen.height/2 <= self.screen.height + margin:
                return True
        
        return False
    
    def display(self, player, lessOrGreater, collision, isPlayer = False): #general display function. Will only display is the coordinates relative to the player match less or greater
        collisionMid = (min(collision[1]) + max(collision[1]))/2
        playerColDist = min(player.collisionBox[1])
        #If player sprite would cover the object, the y must be less for the object.
        #lessOrGreater will either be true or false
        #If player would cover, the y of the object is less than that of the object, so lessOrGreater must be true to display
        #Otherwise the object will display after the player and cover the player sprite
        if (self.y + self.yOff + collisionMid <= player.y + player.yOff + playerColDist) == lessOrGreater or isPlayer == True: 
            self.screen.canv.delete(self.screenObj)

        if (self.y + self.yOff + collisionMid <= player.y + player.yOff + playerColDist) == lessOrGreater or isPlayer == True:
            self.screenObj = self.screen.canv.create_image(self.x - self.camera.x + self.xOff + self.screen.width/2, self.y - self.camera.y + self.yOff + self.screen.height/2, image = self.sprite)
            #self.x is not the absolute screen coordinate of an object
            #To get the absolute current value on screen, you have to subtract the camera
            #The problem is that the camera coordinates are in the center of the screen, so objects on the left of the camera but still on screen would not be displayed if left like this
            #This is because their values would be negative.
            #To fix this, half of the screen width/height (depending on x or y) to adjust the origin of the display

        

class Entity(GameObject):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff = 0, yOff = 0):
        if type(sprite) == str:
            img = loadImage(sprite)
        else:
            img = sprite
        super().__init__(x, y, entityType, id, img, screen, camera, xOff, yOff)
        self.collisionBox = collisionBox #The collision box is a set of points that relative to the objects x and y, giving a range of values
        self.doCollision = doCollision
        self.drawnCollision = -1
        self.hitBox = hitBox #Basically the same as collision box but bigger

        self.rawBox = []
    
    def drawEntityBox(self, box): #Draw the collision box
        if box == None:
            return

        self.screen.canv.delete(self.drawnCollision)

        self.rawBox = [] #Sets up points in a single array to be able to unpack it as a polygon
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
        self.life = randint(25, 50) #Each entity starts with a random life
        self.dead = False

        self.delQueue = delQueue
        if self.type == "Tree": #If its a tree, set death animation and death values
            self.falling = False
            self.display = self.treeDisplay #Special tree display
            self.fallAnim = animations[0]
            self.xOff = -43
        
        elif self.type == "Rock" or self.type == "Ore":
            self.display = self.rockDisplay #Special rock display
            self.damageSprites = animations[0]


    def isPointInBox(self, point, boxType, Mouse = False): #Checks is a point is located within the collision/hitbox ranges
        x = point[0]
        y = point[1]

        if Mouse == True:
            bufferX = self.screen.width / 2 - self.camera.x #If it's the mouse that is the point, then the coordinates should be absolute to the screen
            bufferY = self.screen.height / 2 - self.camera.y

        else:
            bufferX = 0
            bufferY = 0

        if boxType == "collision": #Checks if both x and y position are within the ranges
            if min(self.collisionBox[0]) + self.x + bufferX <= x <= max(self.collisionBox[0]) + self.x + bufferX:
                if min(self.collisionBox[1]) + self.y + bufferY <= y <= max(self.collisionBox[1]) + self.y + bufferY:
                    return True
        
        elif boxType == "hitbox":
             if min(self.hitBox[0]) + self.x + bufferX <= x <= max(self.hitBox[0]) + self.x + bufferX:
                if min(self.hitBox[1]) + self.y + bufferY <= y <= max(self.hitBox[1]) + self.y + bufferY:
                    return True
        
        
        return False
    
    def checkLife(self): #Checks if the entity is dead
        if not isinstance(self, GroundItem):
            if self.life <= 0 and self.dead == False:
                if self.type == "Tree":
                    self.animFrame = 0
                    self.falling = True
                    self.dead = True
                
                else:
                    self.dead = True
                    
                    
    
    def treeDisplay(self, player, lessOrGreater, collision, isPlayer = False): #Special tree display for falling animation

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

    def rockDisplay(self, player, lessOrGreater, collision, isPlayer = False): #Rocks display to update to damaged sprites
        if self.dead:
            self.sprite = self.damageSprites[1]
        
        elif self.life < 20:
            self.sprite = self.damageSprites[0]
        
        collisionMid = (min(collision[1]) + max(collision[1]))/2
        playerColDist = min(player.collisionBox[1])    

        if (self.y + self.yOff + collisionMid <= player.y + player.yOff + playerColDist) == lessOrGreater or isPlayer == True:
            self.screen.canv.delete(self.screenObj)
            self.screenObj = self.screen.canv.create_image(self.x - self.camera.x + self.xOff + self.screen.width/2, self.y - self.camera.y + self.yOff + self.screen.height/2, image = self.sprite)
         
         



class movingEntity(Entity): #Wanted more moving entities, eventually ended up with only the player, so this could technically be a player class
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff = 0, yOff = 0):
        super().__init__(x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, hitBox, xOff, yOff)
    
    def isColliding(self, colObj): #With an 8 point collision box, checks isPointInBox for all rendered entities for each point
        box = colObj.collisionBox

        collisions = [False]*8

        if box == None:
            return collisions

        for i in range(len(self.collisionBox[0])):
            if min(box[0]) + colObj.x <= self.collisionBox[0][i] + self.x <= max(box[0]) + colObj.x:
                if min(box[1]) + colObj.y <= self.collisionBox[1][i] + self.y <= max(box[1]) + colObj.y:
                    collisions[i] = True
                    
        return collisions







class Player(movingEntity):
    playerSpeed = 7
    playerFriction = 0.9

    def __init__(self, x, y, screen, camera, KH, resources):
        super().__init__(x,y,"Player", 0, "images/Robot1.png", screen, camera, ((-25, 0, 25, 25, 25, 0, -25, -25), (20,20,20,35,50,50,50,35)), True, None)
        self.Velx = 0
        self.Vely = 0
        self.KH = KH
        self.resetX = False
        self.resetY = False
        self.resources = resources 
        self.isPlacing = False #Initial states that change by interacting with objects
        self.nearTable = False
        self.nearWires = False
        self.inChest = [False, None] #First value is if a chest is open, second value is the memory location for the object

        self.light = False

        self.metalHP = 50 #Player HP, Ended up not using metal
        self.metalMaxHP = 50
        self.wireHP = 50
        self.wireMaxHP = 50
        self.electricity = 100
        self.electricityMax = 100

        #Setup for all life canvas objects
        self.metalHPBar = -1
        self.metalHPBarOutline = -1
        self.metalHPText = -1
        self.metalHPIcon = -1

        self.wireHPBar = -1
        self.wireHPBarOutline = -1
        self.wireHPText = -1
        self.wireHPIcon = -1

        self.electricityBar = -1
        self.electricityBarOutline = -1
        self.electricityIcon = -1
        self.electricityText = -1

        self.metalIcon = resources["metal"]["spriteSmall"]
        self.wiresIcon = resources["wires"]["spriteSmall"]
        self.electricityIconSprite = loadImage("images/Resources/Electrical/LightningBolt.png")

        #Values for animations
        self.animFrame = 0
        self.direction = ["down"]
        self.previousDirection = self.direction.copy()

        self.doingAction = False
        self.actionFrame = 0

        self.lightSprite = loadImage("images/Lights/LightCircle40.png")
        self.lightObj = -1

        #Loaded animations
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
        
        self.leftPickAnim = loadAnimation("images/PlayerAnimation/Pickaxe/Left/", 18)
        self.rightPickAnim = loadAnimation("images/PlayerAnimation/Pickaxe/Right/", 18)
        self.upPickAnim = loadAnimation("images/PlayerAnimation/Pickaxe/Up/", 18)
        self.downPickAnim = loadAnimation("images/PlayerAnimation/Pickaxe/Down/", 18)

        self.leftupPickAnim = loadAnimation("images/PlayerAnimation/Pickaxe/LeftUp/", 18)
        self.leftdownPickAnim = loadAnimation("images/PlayerAnimation/Pickaxe/LeftDown/", 18)
        self.rightupPickAnim = loadAnimation("images/PlayerAnimation/Pickaxe/RightUp/", 18)
        self.rightdownPickAnim = loadAnimation("images/PlayerAnimation/Pickaxe/RightDown/", 18)

        self.leftAxeAnim = loadAnimation("images/PlayerAnimation/Axe/Left/", 11)
        self.rightAxeAnim = loadAnimation("images/PlayerAnimation/Axe/Right/", 11)
        self.upAxeAnim = loadAnimation("images/PlayerAnimation/Axe/Up/", 11)
        self.downAxeAnim = loadAnimation("images/PlayerAnimation/Axe/Down/", 11)

        self.leftupAxeAnim = loadAnimation("images/PlayerAnimation/Axe/LeftUp/", 11)
        self.leftdownAxeAnim = loadAnimation("images/PlayerAnimation/Axe/LeftDown/", 11)
        self.rightupAxeAnim = loadAnimation("images/PlayerAnimation/Axe/RightUp/", 11)
        self.rightdownAxeAnim = loadAnimation("images/PlayerAnimation/Axe/RightDown/", 11)



    def updateVelocity(self): #Changes velocity if a key is held down
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
        
    def move(self): #Moves the character if it is not doing an actions (pickaxe, axe)
        if self.doingAction == False:
            if self.direction in ["up", "down", "left", "right"]:
                speedFactor = 1
            
            else:
                speedFactor = sqrt(2)

            self.x += self.Velx * Player.playerSpeed# / speedFactor    #Updates position
            self.y += self.Vely * Player.playerSpeed# / speedFactor    #Speed factor can be turned on for more accurate movement, but screen shakes

        if self.x < 0: #Stops the player from going out of bounds
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
        
        self.restrictions = [True, True, True, True] #For which way the camera can move

        if self.x - self.camera.x < 0:
            self.restrictions[3] = False
        elif self.x - self.camera.x > 0:
            self.restrictions[2] = False

        if self.y - self.camera.y < 0:
            self.restrictions[1] = False
        elif self.y - self.camera.y > 0:
            self.restrictions[0] = False
        
        self.moveCam(self.restrictions) #The player movement moves the camera
        
    
    def applyFriction(self): #Puts friction on player's velocity
        self.Velx *= Player.playerFriction
        self.Vely *= Player.playerFriction

        if self.KH.wToggle == False and self.KH.sToggle == False:
            if abs(self.Vely) < 0.3:
                self.Vely = 0
        
        if self.KH.aToggle == False and self.KH.dToggle == False:
            if abs(self.Velx) < 0.3:
                self.Velx = 0
        

    def moveCam(self, directionRestrictions): #calls procedure to update camera position
        self.camera.updateVelocity(self.Velx, self.Vely)
        self.camera.move(directionRestrictions, Player.playerSpeed)

    def checkPlayerCollision(self, tiles): #Gets the current tile of the player
        cTilex = self.x / Tile.tileWidth
        cTiley = self.y / Tile.tileHeight

        cTile = tiles[cTiley][cTilex]
    
    def doStationaryCollisions(self, collisions, entity): #Detects how the player is colliding and updates velocity accordingly
        if True in [collisions[0], collisions[2], collisions[4], collisions[6]] and not True in [collisions[1], collisions[3], collisions[5], collisions[7]]:
            xMid = (min(entity.collisionBox[0]) + max(entity.collisionBox[0]) + (entity.x + entity.xOff) * 2) / 2
            yMid = (min(entity.collisionBox[1]) + max(entity.collisionBox[1]) + (entity.y + entity.yOff) * 2) / 2

            collidingCorner = collisions.index(True)

            #The player bounces off with a velocity 0.8 times the magnitude of the incoming velocity in the opposite direction
            if not ((self.x + self.collisionBox[0][collidingCorner] + self.xOff > xMid and self.Velx > 0) or (self.x + self.collisionBox[0][collidingCorner] + self.xOff < xMid and self.Velx < 0)):
                self.x -= self.Velx * Player.playerSpeed
                self.Vely = self.Vely * -0.8

            if not ((self.y + self.collisionBox[1][collidingCorner] + self.yOff > yMid and self.Vely > 0) or (self.y + self.collisionBox[1][collidingCorner] + self.yOff < yMid and self.Vely < 0)):
                self.y -= self.Vely * Player.playerSpeed
                self.Velx = self.Velx * -0.8

            while True in self.isColliding(entity):
                self.move() #Move the player so that they are no longer colliding

            #If the magnitude of the velocity is less than 3, just stop the player completely
            if abs(self.Velx) < 0.3:
                self.Velx = 0
            if abs(self.Vely) < 0.3:
                self.Vely = 0

        elif True in [collisions[1], collisions[5]]:
            self.Vely = self.Vely * -0.8
            while True in self.isColliding(entity):
                self.move()

            if abs(self.Vely) < 0.3:
                self.Vely = 0

        elif True in [collisions[3], collisions[7]]:

            self.Velx = self.Velx * -0.8
            while True in self.isColliding(entity):
                self.move()

            if abs(self.Velx) < 0.3:
                self.Velx = 0
    
    def displayLife(self): #Draws bars and Icons on screen
        self.screen.canv.delete(self.wireHPBar, self.wireHPIcon, self.wireHPText, self.wireHPBarOutline)
        # self.screen.canv.delete(self.metalHPBar, self.metalHPIcon, self.metalHPText, self.metalHPBarOutline)
        self.screen.canv.delete(self.electricityBar, self.electricityBarOutline, self.electricityIcon, self.electricityText)

        # self.metalHPBarOutline = self.screen.canv.create_polygon(9, 29, 9 + max(0,self.metalMaxHP), 29, 14 + max(0,self.metalMaxHP), 35, 14, 35, fill = 'white', outline = 'black', width = 1)
        self.wireHPBarOutline = self.screen.canv.create_polygon(9, 29, 9 + max(0,self.wireMaxHP), 29, 14 + max(0,self.wireMaxHP), 35, 14, 35, fill = 'white', outline = 'black', width = 1)
        self.electricityBarOutline = self.screen.canv.create_polygon(9, 44, 9 + max(0,self.electricityMax), 44, 14 + max(0,self.electricityMax), 50, 14, 50, fill = 'white', outline = 'black', width = 1)


        # self.metalHPBar = self.screen.canv.create_polygon(10, 30, 10 + max(0,self.metalHP), 30, 15 + max(0,self.metalHP), 35, 15, 35, fill = 'red', outline = '', width = 1)
        self.wireHPBar = self.screen.canv.create_polygon(10, 30, 10 + max(0,self.wireHP), 30, 15 + max(0,self.wireHP), 35, 15, 35, fill = 'red', outline = '', width = 1)
        self.electricityBar = self.screen.canv.create_polygon(10, 45, 10 + max(0,self.electricity), 45, 15 + max(0,self.electricity), 50, 15, 50, fill = 'red', outline = '', width = 1)
        
        # self.metalHPIcon = self.screen.canv.create_image(30 + max(0,self.metalMaxHP), 32, image = self.metalIcon)
        self.wireHPIcon = self.screen.canv.create_image(30 + max(0,self.wireMaxHP), 32, image = self.wiresIcon)
        self.electricityIcon = self.screen.canv.create_image(30 + max(0,self.electricityMax), 48, image = self.electricityIconSprite)

        # self.metalHPText = self.screen.canv.create_text(65 + max(0,self.metalMaxHP), 32, text = "{}/{}".format(max(0,int(self.metalHP)), self.metalMaxHP))
        self.wireHPText = self.screen.canv.create_text(65 + max(0,self.wireMaxHP), 32, text = "{}/{}".format(max(0,int(self.wireHP)), self.wireMaxHP))
        self.electricityText = self.screen.canv.create_text(65 + max(0,self.electricityMax), 48, text = "{}/{}".format(max(0,int(self.electricity)), self.electricityMax))

    def checkNearTable(self, tileArray): #If the distance to an engineering table (or electrical station) is less than 200, it is considered near it
        self.nearTable = False
        self.nearWires = False
        for i in tileArray:
            for j in i:
                for k in j.entities:
                    if k.type == "Furniture":
                        if k.id == 1:
                            if k.isPlacing == False:
                                if k.dist(self.x, self.y) < 200:
                                    self.nearTable = True

                        if k.id == 3:
                            if k.isPlacing == False:
                                if k.dist(self.x, self.y) < 200:
                                    self.nearWires = True
    
    def checkNearChest(self): #if a chest is open, but the player is further than 250 pixels away, close the chest
        if self.inChest[0] == True:
            chest = self.inChest[1]
            if dist(self.x, self.y, chest.x, chest.y) > 250:
                chest.toggleChest()
    
    def itemInChestMovement(self, e): #If space is pressed while in chest inventory
        if self.inChest[0] == True: 
            chest = self.inChest[1]
            if self.KH.hotbar.inventory[self.KH.hotbar.cursorPosition - 1] != 0 and chest.cursorPosition == None: #If not selecting anything in chest and item selected in hotbar
                item = self.KH.hotbar.inventory[self.KH.hotbar.cursorPosition - 1]
                if chest.addItemToChest(item):
                    self.KH.hotbar.inventory[self.KH.hotbar.cursorPosition - 1] = 0
            
            elif chest.cursorPosition != None: #If selecting in chest
                if chest.inventory[chest.cursorPosition - 1] != 0: #If selected chest slot has an item
                    if self.KH.hotbar.addItem(None, chest.inventory[chest.cursorPosition - 1]):
                        chest.inventory[chest.cursorPosition - 1] = 0
                
                else:
                    chest.cursorPosition = None

            elif self.KH.hotbar.inventory[self.KH.hotbar.cursorPosition - 1] == 0: #If not selecting in chest and current hotbar slot is empty
                chest.cursorPosition = 1
            




    
    def chooseAnimFrame(self):
        if self.doingAction in ["Rock", "Tree"]: #Choose either axe or pickaxe animation
            if self.doingAction == "Rock":
                curAnim = eval("self.{}PickAnim".format("".join(self.previousDirection)))
                divisor = 2

            elif self.doingAction == "Tree":
                curAnim = eval("self.{}AxeAnim".format("".join(self.previousDirection)))
                divisor = 3
            
            if self.actionFrame // divisor == len(curAnim): #The divisor makes the animation slower the higher the divisor is
                self.actionFrame = 0 #If action frame is too big of an index, set to idle or walking animation and call the function again
                self.doingAction = False
                self.chooseAnimFrame()
                return

            self.sprite = curAnim[self.actionFrame // divisor % len(curAnim)] #The index increases slower than once per frame due to the divisor
            self.actionFrame += 1
            
            return

        else:
            if len(self.direction) > 0:
                self.previousDirection = self.direction.copy() #saves previous direction in case no direction is calculated
            self.direction = []
            if self.KH.dToggle == True and self.KH.aToggle == False: #adds the direction to the list is heading in one direction but not in the opposite direction as well
                #This is based on button presses
                self.direction.append("right")
            
            elif self.KH.aToggle == True and self.KH.dToggle == False:
                self.direction.append("left")
            
            if self.KH.sToggle == True and self.KH.wToggle == False:
                self.direction.append("down")
            
            elif self.KH.wToggle == True and self.KH.sToggle == False:
                self.direction.append("up")
            
            if len(self.direction) == 0:
                curAnim = eval("self.{}IdleAnim".format("".join(self.previousDirection))) #If there is no direction in movement, get the idle animation correspondant to previous direction
                #Eval takes a string and outputs whatever the string would normally evaluate to
                #For example, if there is variable x, which equals 5, eval("x") would evaluate to 5
                #In this case, eval is taking a formatted string with an object attribute, and outputs the object ID

            else:
                curAnim = eval("self.{}WalkAnim".format("".join(self.direction))) #If there is direction, get walking animation in that direction
        
        self.animFrame += 1 #Increase animation frame
        id = self.animFrame//3 % len(curAnim)
        self.sprite = (curAnim[id])









tileGridWidth = 50
tileGridHeight = 50

class Tile(GameObject): #Similar to entity, but has entities array
    tileWidth = 400
    tileHeight = 400
    def __init__(self, x, y, id, sprite, screen, camera, i1, i2, collisionBox):
        super().__init__(x, y, "tile", id, sprite, screen, camera, xOff = 200, yOff = 200)
        self.entities = []
        self.indexX = i1
        self.indexY = i2
        self.collisionBox = collisionBox
    
    def display(self, camX, camY): #Overrides the GameObject display as the tiles will always be below the the player
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

    def move(self, dR, speed): #Moves with the player
        if dR[0] == False and self.Vely < 0: #Apply restrictions on velocity (So the camera doesn't move without the player)
            self.Vely = 0
        elif dR[1] == False and self.Vely > 0:
            self.Vely = 0
        
        if dR[2] == False and self.Velx < 0:
            self.Velx = 0
        elif dR[3] == False and self.Velx > 0:
            self.Velx = 0

        self.x += self.Velx * speed #Update cam position
        self.y += self.Vely * speed


        if self.x < self.screen.width/2: #If the camera moves past the edge of where it's supposed to be, it goes back to the edge and set velocity to 0
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

    def applyFriction(self): #Useless now as cam velocity is the same as player
        if self.KH.aToggle == False and self.KH.dToggle == False:
            self.Velx *= Camera.camFriction
        
        if self.KH.wToggle == False and self.KH.sToggle == False:
            self.Vely *= Camera.camFriction

    def setCoords(self, newX, newY): #teleports camera (I don't think its used)
        self.x = newX
        self.y = newY






class GroundItem(stationaryEntity): 
    def __init__(self, x, y, entityType, id, sprite, highlight, screen, camera, resources, tile, player, resourceType, delQueue):
        super().__init__(x,y,entityType, id, sprite, [], screen, camera, None, False, None, tile, delQueue)
        self.resources = resources
        self.player = player
        self.resourceType = resourceType #What resource the item gives
        self.highlight = highlight #Highlight for hovering over the object

        

    def display(self, player, lessOrGreater, collision, isPlayer = False):
        if lessOrGreater == True:
            self.screen.canv.delete(self.screenObj)
            self.screenObj = self.screen.canv.create_image(self.x - self.camera.x + self.xOff + self.screen.width/2, self.y - self.camera.y + self.yOff + self.screen.height/2, image = self.sprite, activeimage = self.highlight)

    def pickUpItem(self): #Gives items to the player and removes it from the canvas and entities arrays
        self.resources[self.resourceType]["amount"] += randint(1,2)
        self.screen.canv.delete(self.screenObj)
        self.tile.entities.remove(self)


class Furniture(stationaryEntity):
    furnitureData = loadSettings("data/furniture.json") #Loads data and images for the class rather than in setInitialValues
    
    furnitureSprites = []
    furnitureHighlights = []
    furnitureSpritesRed = []
    furnitureSpritesGreen = []
    chestUI = [loadImage("images/UI/Hotbar8.png"), loadImage("images/UI/cursor.png")]

    arrowSprites = [[loadImage("images/Arrows/GreenRight.png"), loadImage("images/Arrows/GreenLeft.png"), loadImage("images/Arrows/GreenUp.png"), loadImage("images/Arrows/GreenDown.png")],
                    [loadImage("images/Arrows/RedRight.png"), loadImage("images/Arrows/RedLeft.png"), loadImage("images/Arrows/RedUp.png"), loadImage("images/Arrows/RedDown.png")]]
    
    rocketSprite = loadImage("images/Furniture/LaunchPad/WithRocket.png")

    for i in range(len(furnitureData)): #Set sprite arrays
        furnitureSprites.append(loadImage(furnitureData[str(i+1)]["furnitureSprite"]))
        furnitureHighlights.append(loadImage(furnitureData[str(i+1)]["furnitureHighlight"]))
        furnitureSpritesRed.append(loadImage(furnitureData[str(i+1)]["furnitureRed"]))
        furnitureSpritesGreen.append(loadImage(furnitureData[str(i+1)]["furnitureGreen"]))

    def __init__(self, x, y, id, screen, camera, player, tile, delQueue, resources = None):
        sprite = Furniture.furnitureSprites[int(id) - 1] #Gets sprites from id
        self.highlight = Furniture.furnitureHighlights[int(id) - 1]
        self.spriteRed = Furniture.furnitureSpritesRed[int(id) - 1]
        self.spriteGreen = Furniture.furnitureSpritesGreen[int(id) - 1]

        colBox = Furniture.furnitureData[str(id)]["collision"]

        super().__init__(x,y, "Furniture", id, sprite, [], screen, camera, colBox, False, None, tile, delQueue )

        self.player = player
        self.isPlacing = True #furniture object is made when a furniture item is used, so the player is and this object are in placing state
        player.isPlacing = True
        
        self.shownSprite = None 
        self.shownActive = None

        self.colliding = False


        if self.id == 2: #If chest, give item inventory
            self.inventory = [0]*8
            self.inventoryBarSprite = Furniture.chestUI[0]
            self.inventoryBar = -1
            self.open = False
            self.cursorSprite = Furniture.chestUI[1]
            self.cursorScreenObj = -1
            self.cursorPosition = None
        
        elif self.id == 4: #If generator, give wood resource inventory and canvas objects
            self.resource = 0 # the amount of the resource in the inventory
            self.resourceType = "wood" #the resource type (for dictionary)
            self.water = 0
            self.open = False
            self.playerResources = resources

            self.increaseArrow1 = -1
            self.decreaseArrow1 = -1
            self.increaseArrow10 = -1
            self.decreaseArrow10 = -1

            self.text1x = -1
            self.text10x = -1

            self.increaseSprite = Furniture.arrowSprites[1][0]
            self.increaseHighlight = Furniture.arrowSprites[0][0]

            self.decreaseSprite = Furniture.arrowSprites[1][1]
            self.decreaseHighlight = Furniture.arrowSprites[0][1]

            self.resourceWindow = -1
            self.resourceText = -1
            self.resourceIcon = -1

            self.charge = 0

        
        elif self.id == 6: #If launch pad, give metal and wire inventory and canvas objects for the ui there
            self.resource = 0
            self.resourceType = "metal"
            self.open = False
            self.playerResources = resources

            self.increaseArrow1 = -1
            self.decreaseArrow1 = -1
            self.increaseArrow10 = -1
            self.decreaseArrow10 = -1

            self.text1x = -1
            self.text10x = -1

            self.text1x2 = -1
            self.text10x2 = -1
            
            self.increaseSprite = Furniture.arrowSprites[1][0]
            self.increaseHighlight = Furniture.arrowSprites[0][0]

            self.decreaseSprite = Furniture.arrowSprites[1][1]
            self.decreaseHighlight = Furniture.arrowSprites[0][1]

            self.resourceWindow = -1
            self.resourceText = -1
            self.resourceIcon = -1

            self.charge = 0



            self.wires = 0
            self.resourceType2 = "wires"

            self.increaseArrow12 = -1
            self.decreaseArrow12 = -1
            self.increaseArrow102 = -1
            self.decreaseArrow102 = -1

            self.resourceText2 = -1
            self.resourceIcon2 = -1

            self.altSprite = Furniture.rocketSprite #rocket sprite for when enough material is put in
            

    
    def chooseSprite(self, tileArray): #If able to place down, green, if would be colliding if placed down, then red.
        self.colliding = False
        self.x = self.player.x + self.player.KH.mouseX - self.screen.width/2
        self.y = self.player.y + self.player.KH.mouseY - self.screen.height/2
        for i in tileArray:
            for j in i:
                for k in j.entities:
                    if not isinstance(k, GroundItem):
                        if self.dist(k.x, k.y) < 400:
                            for p in range(len(k.collisionBox[0])):
                                point = [k.x + k.collisionBox[0][p], k.y + k.collisionBox[1][p]]
                                if self.isPointInBox(point, "collision"):
                                    self.colliding = True
        
        if self.dist(self.player.x, self.player.y) < 400:
            for p in range(len(self.player.collisionBox[0])):
                            point = [self.player.x + self.player.collisionBox[0][p], self.player.y + self.player.collisionBox[1][p]]
                            if self.isPointInBox(point, "collision"):
                                self.colliding = True
        
        if self.colliding == False:
            self.shownSprite = self.spriteGreen
        else:
            self.shownSprite = self.spriteRed

            


    def display(self, player, lessOrGreater, collision): #If on ground, then display like stationary entity, otherwise display at mouse position
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
                self.screenObj = self.screen.canv.create_image(self.player.KH.mouseX , self.player.KH.mouseY, image = self.shownSprite)

    
    def dist(self,x,y):
        dx = (self.x - x)**2
        dy = (self.y - y)**2
        l = sqrt(dx + dy)
        return l
    

    def displayInventory(self): #If open, display similar to how the hotbar displays, instead the relative coordinate is just above the chest
        if self.open:
            self.screen.canv.delete(self.inventoryBar, self.cursorScreenObj)
            self.inventoryBar = self.screen.canv.create_image(self.x - self.camera.x +self.screen.width/2, self.y - self.camera.y + self.screen.height/2 - 50, image = self.inventoryBarSprite)
            if self.cursorPosition != None:
                self.cursorScreenObj = self.screen.canv.create_image(self.x - self.camera.x +self.screen.width/2 - 171 + 38*self.cursorPosition, self.y - self.camera.y + self.screen.height/2 - 50, image = self.cursorSprite)

            for i in self.inventory:
                if i != 0:
                    self.screen.canv.delete(i.screenObj)
                    i.screenObj = self.screen.canv.create_image(self.x - self.camera.x +self.screen.width/2 - 171 + 38*(self.inventory.index(i)+1),self.y - self.camera.y + self.screen.height/2 - 50, image = i.sprite)


    def toggleChest(self): #Toggles the open variable for player and chest
        self.player.inChest[0] = not self.player.inChest[0]  
        self.open = not self.open

        if self.player.inChest[0] == False:
            self.player.inChest[1] = None
            self.cursorPositon = None

        else:
            self.player.inChest[1] = self

    def addItemToChest(self, item): #attempts to add an item to any free spot in the chest
        try:
            index = self.inventory.index(0)

            self.inventory[index] = item
            return True
        except ValueError:
            return False
    
    def moveThroughItems(self, e): #moves the chest ui cursor with arrow keys
        if self.cursorPosition != None:
            if e.keysym == "Right":
                delta = -1
            else:
                delta = 1
            
            if delta < 0:
                    self.cursorPosition = (self.cursorPosition + 1) % 9
                    if self.cursorPosition == 0:
                        self.cursorPosition = 1

                
            else:
                self.cursorPosition = self.cursorPosition - 1
                if self.cursorPosition < 1:
                    self.cursorPosition = 8
    
    def toggleResourceScreen(): #toggles screen for generator and launch pas
        self.open = not self.open

    def displayResourceScreen(self): #displays the screen that gives access to resource inventory
        if self.id == 4: #Displays just the resource number if it's generator
            text = str(self.resource)
        
        elif self.id == 6: #Displays the fraction of resource inside of the launch pad
            text = "{} / 600".format(self.resource)

        camBufferX = self.screen.width / 2 - self.camera.x
        camBufferY = self.screen.height / 2 - self.camera.y
        
        self.screen.canv.delete(self.increaseArrow1, self.decreaseArrow1, self.increaseArrow10, self.decreaseArrow10 ,self.resourceText, self.resourceIcon, self.resourceWindow, self.text1x, self.text10x)


        if self.id != 6:
            self.resourceWindow = self.screen.canv.create_rectangle(self.x + camBufferX - 55, self.y + camBufferY - 80, self.x + camBufferX + 55, self.y + camBufferY - 30, fill = 'white')
       
        else: #The same as below, but for wires. displays window box, then displays icon, amounts, arrows, and arrow values in the box
            #then binds an action to the arrows
            self.screen.canv.delete(self.text1x2, self.text10x2, self.increaseArrow12, self.increaseArrow102, self.decreaseArrow12, self.decreaseArrow102, self.resourceIcon2, self.resourceText2)
            self.resourceWindow = self.screen.canv.create_rectangle(self.x + camBufferX - 80, self.y + camBufferY - 120, self.x + camBufferX + 80, self.y + camBufferY - 30, fill = 'white')
            self.text1x2 = self.screen.canv.create_text(self.x + camBufferX + 70, self.y + camBufferY - 110, text = "x1")
            self.text10x2 = self.screen.canv.create_text(self.x + camBufferX + 70, self.y + camBufferY - 90, text = "x10")

            self.increaseArrow12 = self.screen.canv.create_image(self.x + camBufferX + 40, self.y + camBufferY - 110, image = self.increaseSprite, activeimage = self.increaseHighlight)
            self.decreaseArrow12 = self.screen.canv.create_image(self.x + camBufferX - 60, self.y + camBufferY - 110, image = self.decreaseSprite, activeimage = self.decreaseHighlight)

            self.increaseArrow102 = self.screen.canv.create_image(self.x + camBufferX + 40, self.y + camBufferY - 90, image = self.increaseSprite, activeimage = self.increaseHighlight)
            self.decreaseArrow102 = self.screen.canv.create_image(self.x + camBufferX - 60, self.y + camBufferY - 90, image = self.decreaseSprite, activeimage = self.decreaseHighlight)

            self.resourceIcon2 = self.screen.canv.create_image(self.x+camBufferX, self.y + camBufferY - 110, image = self.playerResources[self.resourceType2]["spriteSmall"])
            self.resourceText2 = self.screen.canv.create_text(self.x + camBufferX, self.y + camBufferY - 90, text = "{} / 300".format(self.wires))

            self.screen.canv.tag_bind(self.increaseArrow12, "<Button-1>", self.placeWires1)
            self.screen.canv.tag_bind(self.increaseArrow102, "<Button-1>", self.placeWires10)
            self.screen.canv.tag_bind(self.decreaseArrow12, "<Button-1>", self.takeOutWires1)
            self.screen.canv.tag_bind(self.decreaseArrow102, "<Button-1>", self.takeOutWires10)


        if self.id == 6:
            self.resourceText = self.screen.canv.create_text(self.x + camBufferX, self.y + camBufferY - 40, text = text)
        else:
            self.resourceText = self.screen.canv.create_text(self.x + camBufferX - 10, self.y + camBufferY - 40, text = text)
        

        self.resourceIcon = self.screen.canv.create_image(self.x+camBufferX, self.y + camBufferY - 60, image = self.playerResources[self.resourceType]["spriteSmall"])

        self.increaseArrow1 = self.screen.canv.create_image(self.x + camBufferX + 40, self.y + camBufferY - 60, image = self.increaseSprite, activeimage = self.increaseHighlight)
        self.increaseArrow10 = self.screen.canv.create_image(self.x + camBufferX + 40, self.y + camBufferY - 40, image = self.increaseSprite, activeimage = self.increaseHighlight)

        if self.id != 6:
            self.decreaseArrow1 = self.screen.canv.create_image(self.x + camBufferX - 40, self.y + camBufferY - 60, image = self.decreaseSprite, activeimage = self.decreaseHighlight)
            self.decreaseArrow10 = self.screen.canv.create_image(self.x + camBufferX - 40, self.y + camBufferY - 40, image = self.decreaseSprite, activeimage = self.decreaseHighlight)

        else:
            self.decreaseArrow1 = self.screen.canv.create_image(self.x + camBufferX - 60, self.y + camBufferY - 60, image = self.decreaseSprite, activeimage = self.decreaseHighlight)
            self.decreaseArrow10 = self.screen.canv.create_image(self.x + camBufferX - 60, self.y + camBufferY - 40, image = self.decreaseSprite, activeimage = self.decreaseHighlight)
        
        if self.id != 6:
            self.text1x = self.screen.canv.create_text(self.x + camBufferX + 17, self.y + camBufferY - 60, text = "x1")
            self.text10x = self.screen.canv.create_text(self.x + camBufferX + 17, self.y + camBufferY - 40, text = "x10")
        
        else:
            self.text1x = self.screen.canv.create_text(self.x + camBufferX + 70, self.y + camBufferY - 60, text = "x1")
            self.text10x = self.screen.canv.create_text(self.x + camBufferX + 70, self.y + camBufferY - 40, text = "x10")
        

        self.screen.canv.tag_bind(self.increaseArrow1, "<Button-1>", self.placeResources1)
        self.screen.canv.tag_bind(self.increaseArrow10, "<Button-1>", self.placeResources10)
        self.screen.canv.tag_bind(self.decreaseArrow1, "<Button-1>", self.takeOutResources1)
        self.screen.canv.tag_bind(self.decreaseArrow10, "<Button-1>", self.takeOutResources10)

    def placeResources1(self, e):
        if self.playerResources[self.resourceType]["amount"] >= 1:
            if self.id != 6 and self.resource < 99 or self.id == 6 and self.resource < 1000:
                self.resource += 1
                self.playerResources[self.resourceType]["amount"] -= 1
    
    def placeResources10(self, e):
        if self.playerResources[self.resourceType]["amount"] >= 10:
            if self.id != 6 and self.resource < 90 or self.id == 6 and self.resource < 990:
                self.resource += 10
                self.playerResources[self.resourceType]["amount"] -= 10
    
    def takeOutResources1(self, e):
        if self.resource >= 1:
            self.resource -= 1
            self.playerResources[self.resourceType]["amount"] += 1
    
    def takeOutResources10(self, e):
        if self.resource >= 10:
            self.resource -= 10
            self.playerResources[self.resourceType]["amount"] += 10

    def placeWires1(self, e):
        if self.playerResources[self.resourceType2]["amount"] >= 1:
            if self.wires < 500:
                self.wires += 1
                self.playerResources[self.resourceType2]["amount"] -= 1
    
    def placeWires10(self, e):
        if self.playerResources[self.resourceType2]["amount"] >= 10:
            if self.wires < 490:
                self.wires += 10
                self.playerResources[self.resourceType2]["amount"] -= 10
    
    def takeOutWires1(self, e):
        if self.wires >= 1:
            self.wires -= 1
            self.playerResources[self.resourceType2]["amount"] += 1

    def takeOutWires10(self, e):
        if self.wires >= 10:
            self.wires -= 10
            self.playerResources[self.resourceType2]["amount"] += 10

class Item: #stores data for hotbar, chest, and crafting window
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

        if id in [7, 8, 9, 10, 11, 12, 13]:
            self.furnitureId = Item.ItemData[str(id)]["furnitureID"]



    
