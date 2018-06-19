#Standard Library
import json as js
import os
from random import choice, randint
import atexit
import sys
from threading import Thread
from queue import Queue
from math import *


dependencyPath = __file__.split('EngineMain.py')[0] + "Dependencies"
sys.path.append(dependencyPath)

#Runs the package installer
import InstallPip
if __name__ == '__main__':
    InstallPip.checkDependencies()

from Screen import *

from getData import *

#Loads settings to make the Screen
#Need to do it here so that the screen can be made and images loaded

settings = loadSettings()
    #=====Screen and Tkinter windows=====
if settings["window"]["width"] == None:
    s = makeScreen(1024, 768, settings["window"]["fullscreen"], "Robocalypse", __file__.split('EngineMain.py')[0] + "images/Robot16.xpm")
    settings["window"]["width"] = s.canv.winfo_screenwidth()
    settings["window"]["height"] = s.canv.winfo_screenheight()
    
else:
    s = makeScreen(settings["window"]["width"], settings["window"]["height"], settings["window"]["fullscreen"], "Robocalypse Game", __file__.split('EngineMain.py')[0] + "images/Robot16.xpm")

if settings["window"]["fullscreen"] == True:
        sWidth = s.root.winfo_screenwidth()
        sHeight = s.root.winfo_screenheight()
    
else:
    sWidth = int(s.canv.cget('width'))
    sHeight = int(s.canv.cget('height'))
    
    s.width = sWidth
    s.height = sHeight   

#Scenes
from SceneManager import *

#Downloaded Modules
from PIL import Image, ImageTk, ImageFilter
from pygame import mixer

#Miscellaneous
from keyHandler import KeyHandler


#Game Scene Stuff
from GameSceneObjects import *
from UserInterfaces import *

#Import here due to coflicts
from time import sleep, time
from tkinter import *

#Length formula
def dist(p1, p2):
    l = sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )
    return l


#Event to run saveSettings
def saveSettingsEvent(Event):
    saveSettings()

#Saves the current settings from SettingsScene 
def saveSettings():
    global s, sWidth, sHeight, settings, hotbar
    updatedSettings = []
    #Gets text information from screen
    for item in settingsS.settingText:
        itemText = s.canv.itemcget(item, 'text').split()
        if itemText[0:2] == ['Screen', 'Size']:
            updatedSettings.append(itemText[3])
            updatedSettings.append(itemText[5])
        else:
            updatedSettings.append(itemText[-1])
    
    #Puts it in variables
    width = int(updatedSettings[0])
    height = int(updatedSettings[1])
    fullScr = eval(updatedSettings[2])
    sound = eval(updatedSettings[3])
    showFps = eval(updatedSettings[4])
    dayNight = eval(updatedSettings[5])
    
    s.updateShownDimensions(width, height)
    
    #Saves the setting into dictionary
    settings['window']['width'] = width
    settings['window']['height'] = height
    settings['window']['fullscreen'] = fullScr
    settings['sound'] = sound
    settings['displayFPS'] = showFps
    settings["doDayNight"] = dayNight
    
    #Saves to file
    with open('data/configs.json', 'w') as jsonFile:
        js.dump(settings, jsonFile, indent = 4)
    
    s.fullscreen = fullScr
    
    global applyButton
    s.canv.delete(applyButton)
    applyButton = -1
    
    settingsS.deleteSettings()
    global firstTime
    firstTime = True
    settingsS.change_scene("scene_main")
    
    #Update Screen and screen variables
    if fullScr == True:
        s.root.attributes("-fullscreen", fullScr)
        sleep(0.1)
        sWidth = s.root.winfo_screenwidth()
        sHeight = s.root.winfo_screenheight()

        s.width = sWidth
        s.height = sHeight
    else:
        sWidth = width
        sHeight = height
        
        s.root.attributes("-fullscreen", fullScr)
        s.root.geometry("{}x{}+20+20".format(width, height))
    
    
    s.canv.config(width = s.width, height = s.height)

        
    
    s.updateDimensions()

    hotbar.x = s.width / 2
    hotbar.y = s.height - 25
    
        


#==========================================
#=============Thread Functions=============
#==========================================

#Calculates the FPS
def countFrameRate():
    global frame
    global fps
    fps = 0
    startTime = time()
    while True:
        sleep(1)
        fps = round(frame / (time() - startTime),2)
        frame = 0
        startTime = time()

#displays the FPS
def displayFPS():
    global fpsText
    text = "{} fps".format(fps)
    s.canv.delete(fpsText)
    fpsText = s.canv.create_text(37, 10, text = text, fill = '#20FF20')

#Ticks up dayFrame
def doDayCycle():
    global dayFrame
    while True:
        if Scene.current_scene == "scene_game" and mainS.switch == False:
            dayFrame += 1

        
        sleep(1/60)

#The calculation thread
def doGameCalculations():
    global bindQueue, timeOfDay, renderedTiles, CraftWin, dayFrame
    while True:
        if Scene.current_scene == "scene_game" and mainS.switch == False:
            #Player Movement
            player.applyFriction()            
            player.updateVelocity()
            player.move()
            #Crafting Abilities
            player.checkNearTable(renderedTiles)
            player.checkNearChest()

            #Check tile collision
            for i in renderedTiles:
                for j in i:
                    for k in j.entities:
                        player.doStationaryCollisions(player.isColliding(k), k)
                        k.checkLife()
            
            #Set time of Day from dayFrame
            if dayFrame < 10800:
                timeOfDay = "Day"
            
            elif 10800 <= dayFrame <= 12600 and settings["doDayNight"] == True:
                timeOfDay = "Evening"
            
            elif 19800 <= dayFrame <= 21700 and settings["doDayNight"] == True:
                timeOfDay = "Evening"
            
            else:
                timeOfDay = "Night"
            
            #Every certain amount of frames, electricity decreases
            if dayFrame % 400 == 0:
                player.electricity -= 1
                player.electricity = max(0,player.electricity)
            
            #Decreases player health if no electricity
            if player.electricity <= 0:
                player.wireHP -= 1
            
            #Checks for game loss from health
            if player.wireHP <= 0:
                gameS.change_scene("scene_gameOver")
            
            #Checks for win
            for i in furnitureArray:
                if i.id == 6:
                    if i.resource >= 600 and i.wires >= 300:
                        i.sprite = i.altSprite
            
            #Checks for game loss from days
            if dayNum >= 8:
                gameS.change_scene("scene_gameOver")


            if CraftWin.openWindow: #Moves the crafting window depending on if it is open or not
                if CraftWin.x < 112:
                    CraftWin.x += 8
            
            else:
                if CraftWin.x > -112:
                    CraftWin.x -= 8
            
            if gameS.checkRendered(renderedTiles) == False: #If a tile in rendered tiles goes offscreen, sets a new rendered tiles array
                renderedTiles = gameS.setRenderGrid()
            
            player.chooseAnimFrame()

            dayFrame += 2
            
        sleep(1/60)

#Events from crafting and action button
def customEventHandler():
    global resources, CraftWin, tempFurniture, bindQueue
    while True:
        #A loop to continue while there are events in the array
        for e in KH.checkEvents:
                #If placing down furniture
                if e == "Place Furniture":
                    #If furniture is not yet a furniture object, makes a furniture object that follows the mouse
                    if player.isPlacing == False:
                        player.isPlacing = True
                        hotbar.lockCursor = True
                        curTileX = int(player.x // Tile.tileWidth)
                        curTileY = int(player.y // Tile.tileHeight)
                        curTile = tileGrid[curTileY][curTileX]
                        tempFurniture = Furniture(KH.mouseX, KH.mouseY, hotbar.inventory[hotbar.cursorPosition - 1].furnitureId, s, Cam, player, deleteQueue, curTile, resources)
                        curTile.entities.sort(key = lambda entity: entity.y)
                    
                    #If furniture object, permanently places it in a spot, and puts it into a tile's entity array
                    if player.isPlacing == True:
                        if tempFurniture.shownSprite == tempFurniture.spriteGreen:
                            tempFurniture.isPlacing = False
                            tempFurniture.doCollision = True

                            bindQueue.put(["<Right>",tempFurniture.moveThroughItems])
                            bindQueue.put(["<Left>",tempFurniture.moveThroughItems])
                            
                            tileX = int(tempFurniture.x // Tile.tileWidth)
                            tileY = int(tempFurniture.y // Tile.tileHeight)
                            tileGrid[tileY][tileX].entities.append(tempFurniture)
                            furnitureArray.append(tempFurniture)

                            tempFurniture = None

                            player.isPlacing = False
                            hotbar.lockCursor = False
                            hotbar.inventory[hotbar.cursorPosition - 1] = 0
                            
                #Increases electricity if battery is used
                elif e == "Use Battery":
                    player.electricity += 50
                    player.electricity = min(100, player.electricity)
                    hotbar.inventory[hotbar.cursorPosition - 1] = 0
                
                #For gathering resources
                else:
                    for i in renderedTiles:
                        for j in i:
                            for k in j.entities:
                                if k.life > 0:
                                    if player.actionFrame == 0:
                                        #Checks if the tool is an axe
                                        if e == 'Cut Tree':
                                            if k.type == "Tree":
                                                #Sets the velocity of the player to 0 and starts the axe animation
                                                player.doingAction = "Tree"
                                                player.actionFrame = 0
                                                player.Velx = 0
                                                player.Vely = 0
                                                if dist([player.x, player.y], [k.x, k.y]) < 280:
                                                    #Checks if the player is close to the entity and clicks inside the hitbox
                                                    #If yes, gives a random amount of the resource and reduces the entity's life by that amount
                                                    if k.isPointInBox([KH.mouseClickx, KH.mouseClicky], "hitbox", True):
                                                        amount = randint(1,5)
                                                        resources["wood"]["amount"] += amount
                                                        k.life -= amount

                                        #if the tool is a pickaxe  
                                        elif e == "Mine Rock":
                                            player.doingAction = "Rock"
                                            player.actionFrame = 0
                                            player.Velx = 0
                                            player.Vely = 0
                                            if k.type == "Rock":
                                                if dist([player.x, player.y], [k.x, k.y]) < 280:
                                                    #Same as Tree
                                                    if k.isPointInBox([KH.mouseClickx, KH.mouseClicky], "hitbox", True):
                                                        amountStone = randint(1,5)
                                                        resources["stone"]["amount"] += amountStone
                                                        k.life -= amountStone
                                                        metalChance = randint(1,100)
                                                        #Mining a rock has a 7% chance of giving metal
                                                        # If given, 80% for 1 piece, 18% for 2, 2% for 3
                                                        if metalChance <= 7:
                                                            amountChance = randint(1,100)
                                                            if amountChance <= 80:
                                                                amount = 1
                                                            elif amountChance <= 98:
                                                                amount = 2
                                                            else:
                                                                amount = 3
                                                            resources["metal"]["amount"] += amount
                                            
                                            elif k.type == "Ore":
                                                if dist([player.x, player.y], [k.x, k.y]) < 280:
                                                    #Same as stone but reversed
                                                    if k.isPointInBox([KH.mouseClickx, KH.mouseClicky], "hitbox", True):
                                                        amountMetal = randint(1,5)
                                                        resources["metal"]["amount"] += amountMetal
                                                        k.life -= amountMetal
                                                        stoneChance = randint(1,100)
                                                        if stoneChance <= 30:
                                                            amountChance = randint(1,100)
                                                            if amountChance <= 80:
                                                                amount = 1
                                                            elif amountChance <= 98:
                                                                amount = 2
                                                            else:
                                                                amount = 3
                                                            resources["stone"]["amount"] += amount
                                                    
                            
                                

                            
                #Removed the event once it's done
                KH.checkEvents.pop(0)
        
        #Checks if the player is colliding with special hitboxes on a tile
        #This is water for water and coast tiles, which damage the player
        #And roads on road tiles
        currentTileX = int(player.x // Tile.tileWidth)
        currentTileY = int((player.y + 35) // Tile.tileHeight)
        tileToCheck = tileGrid[currentTileY][currentTileX]
        #Ids are taken from tiles.json
        if int(tileToCheck.id) in [2, 19, 20, 21, 22]:
            if tileToCheck.isPointInBox([player.x, player.y + 35]):
                # player.wireHP -= 0.1
                Player.playerSpeed = 5
            
            else:
                Player.playerSpeed = 7

        elif int(tileToCheck.id) in [4,5,6,7,8,9,10,11]:
            if not tileToCheck.isPointInBox([player.x, player.y + 35]):
                # player.wireHP -= 0.1
                Player.playerSpeed = 5
            
            else:
                Player.playerSpeed = 7
        
        #If on road, the player goes faster
        elif int(tileToCheck.id) in [12,13,14,15,16,17,18,23,24,25,26]:
            if tileToCheck.isPointInBox([player.x, player.y]):
                Player.playerSpeed = 8.5
            else:
                Player.playerSpeed = 7
        
        else:
            Player.playerSpeed = 7
        

        #Does the crafting
        if CraftWin.toDoCrafting != False:
            costForItem = itemData[str(CraftWin.toDoCrafting)]["cost"] #Gets the item's cost from item dictionary
            curResources = []
            for i in resourceOrder:
                curResources.append(resources[i]["amount"])
            
            craftAvailable = True #Until the game finds that the player's resource of a certain kind, it considers the crafting to be legal
            for i in range(len(curResources)):
                if curResources[i] < costForItem[i]:
                    craftAvailable = False
            
            if craftAvailable == True:
                if CraftWin.toDoCrafting == 14: #Wires from crafting get added to the resource pool
                        resources["metal"]["amount"] -= 2
                        resources["wood"]["amount"] -= 1
                        resources["wires"]["amount"] += 1

                elif hotbar.addItem(CraftWin.toDoCrafting): #Game checks if it is possible to place the item in the hotbar
                    for i in resourceOrder: #If it is, the game subtracts the resources from the resource pool
                        resources[i]["amount"] -= costForItem[resourceOrder.index(i)]
                
                else: #Otherwise, puts up an alert
                    alerts.put({"text":"There is not enough space in the\ninventory to craft this item", "delay":2.5})
            
            else:
                alerts.put({"text":"Insufficient Resources to craft this item", "delay":2.5}) #If not enough resources, puts up an alert
            
            CraftWin.toDoCrafting = False #Resets the crafting
        sleep(1/60)
    

def doGraphicCalcs():
    global renderedTiles
    while True:
        if Scene.current_scene == "scene_game": #If in game
             #Selects player animation frame
             pass

        sleep(1/60)

def craftingWindowCalcs():
    global CraftWin
    while True:
        if CraftWin.openWindow: #Moves the crafting window depending on if it is open or not
            if CraftWin.x < 112:
                CraftWin.x += 8
        
        else:
            if CraftWin.x > -112:
                CraftWin.x -= 8
        
        sleep(1/60)
        
#Sets the position and text for the alerts
def doAlert():
    global alerts, alertCount, newAlert
    global notifY
    while True:
        if not alerts.empty():
            alertCount += 1
            newAlert = alerts.get() #Gets the next alert
            if Scene.current_scene == "scene_game":
                while notifY < 80: #Starts moving it down
                    notifY += 5
                    sleep(1/60)
                sleep(newAlert["delay"]) #Sleeps for specified delay
                while notifY > -85: #Starts moving back up
                    notifY -= 5
                    sleep(1/60)
                sleep(1/4)
       
        else:
            notifY = -85
        
        sleep(1/60)
                    
        
#Loads the tiles in a tileGrid array
def loadTiles():
    global tileGrid, percentDone
    tileGrid = []
    

    print("Starting to Build World...")
    for i in range(tileGridHeight):
        percentDone[0] = (i + 1) / tileGridHeight * 100 #Every row is 2% done as the grid is 50x50
        if percentDone[0] % 10 == 0:
            print("{}% complete...".format(int(percentDone[0])))
        
        tileGrid.append([])

        for j in range(tileGridWidth):
            tileId = tileMap[i][j]
            variationAmount = tileData[str(tileId)]["variations"] #Gets the amount of possible variations for a specific tile

            #Chooses one of those variations
            if variationAmount > 1:
                variationChoice = randint(0,variationAmount - 1)
        
            else:
                variationChoice = 0
            
            sprite = tileSprites[str(tileId)][variationChoice] #Gets the sprite for that variation
            
            #Makes the tile Object
            tileGrid[i].append(Tile(j * Tile.tileWidth,i * Tile.tileHeight,tileId, sprite, s, Cam, i, j, tileData[str(tileMap[i][j])]["collision"]))
            curTile = tileGrid[i][j]
            
            if str(tileId) in entityArrangementData: #Chooses a random tile arrangement of entities for grass tiles
                entityArrangementID = randint(1, len(entityArrangementData[str(tileId)]))

                #Copies the arrangement array as changes will be made to it
                entityArrangement = entityArrangementData[str(tileId)][str(entityArrangementID)].copy()
                entityNum = entityArrangement[0] #The first number of the array is always how many entities the variation holds
                entityArrangement.pop(0)
                for ent in range(entityNum): #For each variation, it gets the id, x, and y
                    x = entityArrangement[1]
                    y = entityArrangement[2]
                    eID = entityArrangement[0]

                    if eID in ['1','2','3','4']: #Makes a ground item which can be picked up
                        eInfo = groundItemData[entityArrangement[0]]
                        curTile.entities.append(GroundItem(x + curTile.x, y + curTile.y, eInfo["name"], 0, entitySprites[eID], entityHighlights[eID], s, Cam, resources, curTile, player, eInfo["resource"], deleteQueue))
                    
                    else: #Makes an entity which has collision
                        eInfo = entityData[entityArrangement[0]]
                        curTile.entities.append(stationaryEntity(x + curTile.x, y + curTile.y, eInfo["name"], 0, entitySprites[eID],entityAnimations[eID], s, Cam, eInfo["collision"], eInfo["doCollision"], eInfo["hitbox"], curTile, deleteQueue))
                    if len(entityArrangement) > 3: #If not the last one, scraps the used entity data
                        entityArrangement = entityArrangement[3:]
                    
                    curTile.entities.sort(key = lambda entity: entity.y)

    print("Finished Building World!")


#===================================================
#==============Draw Graphics Functions==============
#===================================================
def toggleOpenCrafting(cWin, event):
    if Scene.current_scene == "scene_game":
        cWin.openWindow = not cWin.openWindow #Toggles the crafting window

def drawNotifBox():
    global notifBox, notifText
    s.canv.delete(notifBox)
    s.canv.delete(notifText)
    notifBox = s.canv.create_image(s.width - 240, notifY, image = UISprites["Notification"])
    notifText = s.canv.create_text(s.width - 240, notifY, text = newAlert["text"])

def drawGroundGraphics():
    gameS.showTiles(renderedTiles)#Draws the tiles

    gameS.displayStationaryEntities(player, True, renderedTiles) #Draws the entities that are below the player (Are higher up on screen so they would be covered)
    player.display(player, True, player.collisionBox, True)
    # player.drawEntityBox(player.collisionBox)
    # gameS.displayStationaryBoxes(renderedTiles, "collision")
    gameS.displayStationaryEntities(player, False, renderedTiles) #Draws the entities that are above the player(Are lower on screen so would cover player)

    
def drawClock():
    global clock, clockHand, dayFrame, dayNum
    s.canv.delete(clock, clockHand)
    if dayFrame >= 21600: #Up ticks the day number
        dayNum += 1
    dayFrame = dayFrame % 21600
    angle = radians(dayFrame / 21600 * 360) - pi / 2 #Gets the angle of the clock hand

    if settings["doDayNight"] == True: #Chooses a clock sprite depending on it is doing day/night cycle or not
        sprite = dayNightClockSprite
    
    else:
        sprite = fullClockSprite

    x = s.width - 40
    y = 50

    clock = s.canv.create_image(x, y, image = sprite)

    xHand = 25*cos(angle)
    yHand = 25*sin(angle) #Gets the coordinates of the clock hand relative to the clock center

    clockHand = s.canv.create_line(x, y, x+xHand, y + yHand, width = 2) 
    

def drawResources():
    for i in range(len(resourceOrder)):
        key = resourceOrder[i] #Draws each resource on the left of the screen along with the corresponding amounts
        s.canv.delete(resources[key]["icon"], resources[key]["text"])
        resources[key]["icon"] = s.canv.create_image(25, 40*i + 70, image = resources[key]["sprite"])
        resources[key]["text"] = s.canv.create_text(50, 40*i + 70, text = str(resources[key]["amount"]))

def drawTempFurniture():
    if tempFurniture != None:
        tempFurniture.chooseSprite(renderedTiles)
        if tempFurniture.isPlacing: #Displays the green/red furniture sprite as it's being placed
            tempFurniture.display(player, None, None)

def drawCostWindow():
    global costBox, costIcons, costText, CraftWin
    for i in costIcons:
        s.canv.delete(i)
    for i in costText:
        s.canv.delete(i)
    s.canv.delete(costBox)
    
    costIcons = []
    costText = []

    if not CraftWin.openWindow: #if the window is closed, reset the box
        CraftWin.currentCostWindow = None

    if CraftWin.currentCostWindow != None: # if the window is open:
        xPos = KH.mouseX
        yPos = KH.mouseY
        costBox = s.canv.create_rectangle(2, yPos - 60, 224, yPos - 15, fill = 'white', outline = 'black') #Draw the box above the mouse
        for i in range(4):
            costIcons.append(s.canv.create_image(24 + 48*i, yPos - 50, image = resources[resourceOrder[i]]["spriteSmall"])) #Draw icons inside the box
            
            curCost = CraftWin.currentCostWindow[i] #Draw the amounts of resources that are needed and if the player has enough (green = yes, red = no).
            if resources[resourceOrder[i]]["amount"] >= curCost:
                color = 'green'
            else:
                color = 'red'
            
            costText.append(s.canv.create_text(24 + 48*i, yPos - 30, text = str(curCost), fill = color))

#When switch hotbar position, text appears for a brief second above the hotbar displaying what item is currently selected
def drawItemName():
    global hotbar
    s.canv.delete(hotbar.itemName)
    if hotbar.inventory[hotbar.cursorPosition - 1] != 0:
        if hotbar.itemFrame < 30:
            hotbar.itemName = s.canv.create_text(s.width / 2, s.height - 60, text = hotbar.inventory[hotbar.cursorPosition - 1].name, fill = "white")
            hotbar.itemFrame += 1
        
        else:
            hotbar.itemName = -1

#draws the chest inventory
def drawOpenChestInv():
    chest = player.inChest[1]
    if chest != None:
        chest.displayInventory()

#Collects all of the UI functions into a single procedure
def drawUIGraphics():
    if settings["doDayNight"] == True:
        drawNight()
    drawOpenChestInv()
    displayResourceScreens()
    drawResources()
    
    if settings["displayFPS"] == True:
        displayFPS()

    drawTempFurniture()
    hotbar.display()
    CraftWin.display()
    drawClock()
    drawCostWindow()
    player.displayLife()
    drawItemName()
    drawNotifBox()
    displayDay()
    drawLaunchSequence()
    
#Draws a different tint on screen depending on the time of day
def drawNight():
    global nightObj
    s.canv.delete(nightObj)

    if timeOfDay != "Day":
        if timeOfDay == "Night":
            nightSprite = nightImages[7]
        
        else:
            if dayFrame < 11100 or dayFrame > 21300:
                nightSprite = nightImages[0]
            
            elif dayFrame < 11400 or dayFrame > 21000:
                nightSprite = nightImages[1]
            
            elif dayFrame < 11700 or dayFrame > 20700:
                nightSprite = nightImages[2]

            elif dayFrame < 12000 or dayFrame > 20400:
                nightSprite = nightImages[3]

            elif dayFrame < 12300 or dayFrame > 20100:
                nightSprite = nightImages[4]

            elif dayFrame < 12600 or dayFrame > 19800:
                nightSprite = nightImages[5]
            
            else:
                nightSprite = nightImages[6]



        nightObj = s.canv.create_image(s.width / 2, s.height / 2, image = nightSprite)

#For generator and launch pad, displays the resources if it is open
def displayResourceScreens():
    for i in furnitureArray:
        if i.id in [4,6]:
            if i.open == True:
                i.displayResourceScreen()

def drawPlayerLight():
    s.canv.delete(player.lightObj)
    if player.light == True or True:
        player.lightObj = s.canv.create_image(player.x - Cam.x + s.width / 2, player.y - Cam.y + s.height/2, image = player.lightSprite)

#Writes the day number in the top right
def displayDay():
    global dayNumObj
    s.canv.delete(dayNumObj)
    dayNumObj = s.canv.create_text(s.width - 40, 10, text = "Day: {}".format(dayNum))

#When you have enough resources, the game freezes and displays text on the launch sequence
#I think it's kind of lame how it is now, but I didn't have time to render a rocket animation
def drawLaunchSequence():
    global launchText
    for i in furnitureArray:
        if i.id == 6:
            if i.sprite == i.altSprite:
                launchText = -1
                for i in range(5):
                    s.canv.delete(launchText)
                    #Displays text in the middle of the screen
                    launchText = s.canv.create_text(s.width / 2, s.height / 2, text = "Launching in {}".format(5 - i), font = ("Helvetica", 72), fill = 'red')
                    s.canv.update()
                    sleep(1)
                
                s.canv.delete(launchText)
                launchText = s.canv.create_text(s.width / 2, s.height / 2, text = "Blast Off!", font = ("Helvetica", 72), fill = 'red')
                s.canv.delete(launchText)
                sleep(2)
                gameS.change_scene("scene_win")
                s.canv.update()

                    
#Deletes all of the screen objects (or attempts to)
def deleteAll():
    s.canv.delete(player.screenObj)
    s.canv.delete(player.metalHPBar, player.metalHPBarOutline, player.metalHPIcon, player.metalHPText)
    s.canv.delete(player.wireHPBar, player.wireHPBarOutline, player.wireHPIcon, player.wireHPText)
    s.canv.delete(player.electricityBar, player.electricityBarOutline, player.electricityIcon, player.electricityText)

    for i in renderedTiles:
        for j in i:
            s.canv.delete(j.screenObj)
            for k in j.entities:
                s.canv.delete(k.screenObj)
    
    for i in range(len(resourceOrder)):
        key = resourceOrder[i]
        s.canv.delete(resources[key]["icon"], resources[key]["text"])
    
    s.canv.delete(clock, clockHand)
    
    try:
        s.canv.delete(tempFurniture.screenObj)
    except AttributeError:
        pass
    
    s.canv.delete(hotbar.itemName)
    for i in costIcons:
        s.canv.delete(i)
    for i in costText:
        s.canv.delete(i)
    s.canv.delete(costBox)
    s.canv.delete(nightObj)
    s.canv.delete(gameoverS.text, gameoverS.title, gameoverS.dayText)
    s.canv.delete(dayNumObj)
    s.canv.delete(hotbar.screenObj, hotbar.cursorScreenObj)
    for i in hotbar.inventory:
        if i != 0:
            s.canv.delete(i.screenObj)
    
    try:
        s.canv.delete(launchText)
    
    except:
        pass    



#===================================================
#==============Maintainance Functions==============
#===================================================
def emptyDelQueue():
    global deleteQueue
    if not deleteQueue.empty():
        objToDelete = deleteQueue.get()
        s.canv.delete(objToDelete.screenObj)
        objToDelete.tile.entities.remove(objToDelete)

#Because of tkinter's threading issues, binding the Key handler is done on the main thread
def emptyBindQueue():
    while not bindQueue.empty():
        nextBind = bindQueue.get()
        KH.addTkinterBind(*nextBind)

#Handles the scroll event for different parts of the screen
def doScroll(event):
    if CraftWin.isMouseInWindow():
        CraftWin.changeY(event)
    else:
        hotbar.changeCursorPositionScroll(event)

#
def interact(event):

    x = KH.mouseX + Cam.x - s.width/2 #Gets the mouse coordinates relative to the world
    y = KH.mouseY + Cam.y - s.height/2

    indX = int(x // Tile.tileWidth) #Gets the tile of the mouse coords
    indY = int(y // Tile.tileHeight)
    curTile = tileGrid[indY][indX]


    for i in curTile.entities: 
        if dist([x, y], [player.x, player.y]) < 200:
            if isinstance(i, GroundItem): #For each entity, it checks if it's a ground item, and then if the player is able to pick it up      
                if dist([x,y], [i.x, i.y]) < 30:
                    i.pickUpItem()
            elif isinstance(i,Furniture): #Checks if it is furniture, if it is, toggle the open attribute
                if i.id == 2:
                    if dist([x,y], [i.x, i.y]) < 60:
                        if player.inChest[0] == False or i.open == True:
                            i.toggleChest()
                elif i.id in [4,6]:
                    i.open = not i.open

#Similar to set initial values, but does not load images, or remake tiles (just the entities on the tiles)
def resetValues():
    global dayNum, dayFrame, resources, tileGrid, hotbar, percentDone
    
    dayNum = 0
    dayFrame = 21540
    for i in resourceOrder:
        resources[i]["amount"] = 0
    
    hotbar.inventory = [0]*6

    player.x = 1900
    player.y = 1200
    Cam.x = 1900
    Cam.y = 1200

    player.electricity = 100
    player.wireHP = 50
    

    for i in tileGrid:
        for j in i:
            j.entities = []
    
            tileId = j.id
            curTile = j

            if str(tileId) in entityArrangementData:
                entityArrangementID = randint(1, len(entityArrangementData[str(tileId)]))
                entityArrangement = entityArrangementData[str(tileId)][str(entityArrangementID)].copy()
                entityNum = entityArrangement[0]
                entityArrangement.pop(0)
                for ent in range(entityNum):
                    x = entityArrangement[1]
                    y = entityArrangement[2]
                    eID = entityArrangement[0]

                    if eID in ['1','2','3','4']:
                        eInfo = groundItemData[entityArrangement[0]]
                        curTile.entities.append(GroundItem(x + curTile.x, y + curTile.y, eInfo["name"], 0, entitySprites[eID], entityHighlights[eID], s, Cam, resources, curTile, player, eInfo["resource"], deleteQueue))
                    
                    else:
                        eInfo = entityData[entityArrangement[0]]
                        curTile.entities.append(stationaryEntity(x + curTile.x, y + curTile.y, eInfo["name"], 0, entitySprites[eID],entityAnimations[eID], s, Cam, eInfo["collision"], eInfo["doCollision"], eInfo["hitbox"], curTile, deleteQueue))
                    if len(entityArrangement) > 3:
                        entityArrangement = entityArrangement[3:]
                    
                    curTile.entities.sort(key = lambda entity: entity.y)




#==========================================================
#====================Grouping Functions====================
#==========================================================


def runGame():
    global firstTime
    global renderedTiles
    global applyButton
    global frame
    

    while True:
        KH.scene = Scene.current_scene

        if Scene.current_scene == "scene_main": #Displays the options for main Scene
            mainS.displayOptions(s.width//2, s.height//2)
            deleteAll()
            s.canv.update()
            
        elif Scene.current_scene == "scene_settings": #Displays the option for main scene, holding the data in updated settings
            if not firstTime:
                updatedSettings = []
                for item in settingsS.settingText: #gets the canvas items of the settings
                    itemText = s.canv.itemcget(item, 'text').split() #Gets the text data of the option
                    try:
                        if itemText[0:2] == ['Screen', 'Size']: #Tries to add it to the updated array
                            updatedSettings.append(itemText[3])
                            updatedSettings.append(itemText[5])
                        else:
                            updatedSettings.append(itemText[-1])
                    except IndexError: #I don't think this is necessary anymore, but it's more of a failsafe now
                        updatedSettings = [settings["window"]["width"],settings["window"]["height"],settings["window"]["fullscreen"],settings["sound"], settings["displayFPS"], settings["doDayNight"]]
                        saveSettings()
                        break
                            
            else: #If it's the first time launching settings, it uses the currently loaded settings
                updatedSettings = [settings["window"]["width"],settings["window"]["height"],settings["window"]["fullscreen"],settings["sound"], settings["displayFPS"], settings["doDayNight"]]
                firstTime = False

            settingsS.displaySettings(s.width//2, s.height//2, *updatedSettings)
            
            s.canv.delete(applyButton) #The button that saves the settings
            applyButton = s.canv.create_text(s.width // 2, s.height - 100, text = "Save and Apply", fill = 'black', activefill = 'yellow', font = ('Helvetica', 16))
            s.canv.tag_bind(applyButton, '<Button-1>', saveSettingsEvent)
        
        elif Scene.current_scene == "scene_game": #This is mostly for showing graphics as a lot of the calculations are threaded
            if mainS.switch == True and gameS.ingame == False: #If the game just switched from main scene (and the game was not running before) it resets the values
                resetValues()
                
            mainS.switch = False
            gameS.ingame = True
            drawGroundGraphics()
            drawUIGraphics()
            emptyDelQueue()
            emptyBindQueue()

        elif Scene.current_scene == "scene_gameOver": #Displays game over scene for 5 seconds
            deleteAll()
            gameoverS.displayGO(dayNum)
            s.canv.update()
            sleep(5)
            gameS.ingame = False
            gameoverS.change_scene("scene_main")
            
        elif Scene.current_scene == "scene_win": #Displays win screen for 5 seconds
            deleteAll()
            winS.displayWin(dayNum)
            s.canv.update()
            sleep(5)
            gameS.ingame = False
            winS.change_scene("scene_main")


        s.canv.update()
        sleep(1/60)
        frame += 1
        
    

def setInitialValues():
    global sWidth, sHeight
    global mainS, settingsS, gameS, gameoverS, winS, Cam, KH, player
    global s, firstTime, updatePosition
    global settings , TESTING, testEntity, applyButton
    global renderedTiles, tileGrid, tileData, tileSprites, tileMap
    global frame, fpsText
    global alerts, alertCount, newAlert, UISprites, hotbar, notifBox, notifText
    global resources, itemData, itemSprites, deleteQueue
    global CraftWin, costBox, costIcons, costText, resourceOrder
    global tempFurniture
    global entityData, entityArrangementData, entitySprites, entityHighlights, entityAnimations, groundItemData, percentDone
    global bindQueue
    global nightImages, nightObj
    global dayFrame, fullClockSprite, dayNightClockSprite, clock, clockHand, dayNum, dayNumObj, timeOfDay
    global furnitureArray

    #=====Basic Variables=====
    TESTING = False
    frame = 0
    alerts = Queue()
    alertCount = 0
    tempFurniture = None
    costIcons = []
    costText = []
    newAlert = {"text":""}
    resourceOrder = ["wood", "stone", "metal", "wires"]
    deleteQueue = Queue()
    bindQueue = Queue()
    dayFrame = 21540
    dayNum = 0
    timeOfDay = "Day"
    nightImages = []
    furnitureArray = []

    #Init Canvas objects
    fpsText = -1
    applyButton = -1
    notifBox = -1
    notifText = -1
    costBox = -1
    nightObj = -1
    dayNumObj = -1
    clock = -1
    clockHand = -1



    #=====Item Data From files=====
    print("Starting to load data...")
    itemData = loadSettings("data/items.json")
    tileData = loadSettings("data/tiles.json")
    entityData = loadSettings("data/entities.json")
    entityArrangementData = loadSettings("data/tileEntityArrangement.json")
    groundItemData = loadSettings("data/groundItemData.json")
    UISpritesData = loadSettings("data/UISprites.json")
    print("Finished Loading Data!")


    print("Starting to Load images...")

    for i in range(8): #Night tints
        nightImages.append(loadImage("images/Lights/DarkNight{}0.png".format(i+1)))
    fullClockSprite = loadImage("images/UI/FullDayClock.png")
    dayNightClockSprite = loadImage("images/UI/DayNightClock.png")

    entitySprites = {} #Images for sprites of collidible entities
    entityHighlights = {}
    entityAnimations = {}

    for i in entityData:
        entitySprites[i] = loadImage(entityData[i]["sprite"])
        entityAnimations[i] = []
        curAnimations = entityData[i]["animations"]
        for j in range(0,len(curAnimations), 2):
            entityAnimations[i].append(loadAnimation(curAnimations[j], curAnimations[j+1]))
    
    for i in groundItemData: #Loads ground item sprites
        entitySprites[i] = loadImage(groundItemData[i]["sprite"])
        entityHighlights[i] = loadImage(groundItemData[i]["spriteHighlight"])

    tileSprites = {} #Loads each variation of the tile sprites
    for i in range(1,27):
        tileSprites[str(i)] = []
        imageBase = tileData[str(i)]["imageBase"] #Gets the images based on a base name specified in tiles.json
        for j in range(1, tileData[str(i)]["variations"] + 1):
            imagePath = "{}{}.png".format(imageBase, j)
            tileSprites[str(i)].append(loadImage(imagePath))

    itemSprites = [] #Sprites for hotbar and crafting window items
    for i in itemData:
        itemSprites.append(loadImage(itemData[i]["icon"]))
    
    UISprites = {}
    for i in UISpritesData:
        UISprites[i] = loadImage(UISpritesData[i])

    #Initializes resources
    resources = {"wood":{"amount": 0, "text":-1, "icon":-1, "sprite": loadImage("images/Resources/Wood Log/log.png"), "spriteSmall":loadImage("images/Resources/Wood Log/logsmall.png")},
                 "metal":{"amount": 0, "text":-1, "icon":-1, "sprite":loadImage("images/Resources/Metal/metal.png"), "spriteSmall":loadImage("images/Resources/Metal/metalSmall.png")},
                 "stone":{"amount":0, "text":-1, "icon": -1, "sprite":loadImage("images/Resources/Rock/rock2.png"),"spriteSmall":loadImage("images/Resources/Rock/rock2small.png")},
                  "wires":{"amount": 0, "text":-1, "icon":-1, "sprite": loadImage("images/Resources/Electrical/wires.png"),"spriteSmall": loadImage("images/Resources/Electrical/wiresSmall.png")}}
    
    
    print("Finished loading images!")
    
    startx = 1900
    starty = 1200 #Starting player position

    #Creates instances for the 
    hotbar = Hotbar(s, itemSprites)
    KH = KeyHandler(s, hotbar, Scene)
    Cam = Camera(startx, starty, s, KH)
    player = Player(startx, starty, s, Cam, KH, resources)
    
    

    
    #Gets the map data to know where to put each tile
    with open('data/TileData.txt') as mapD:
        tileMap = mapD.read().split('\n')
    
    for i in range(len(tileMap)):
        tileMap[i] = tileMap[i].split(',')

    percentDone = [0]
    #Starts a thread to make the tileGrid
    loadingThread = Thread(target = loadTiles)
    loadingThread.daemon = True
    loadingThread.start()

    loadScene = LoadingScene(s, percentDone)
    loadScene.updateLoading()
    
    #Makes the Scenes for the game
    mainS = MainScene("Robocalypse", s, KH)
    settingsS = SettingsScene(s,KH)
    gameS = GameScene(s,Cam, KH, tileGrid, player)
    gameoverS = GameOverScene(s, KH, player)
    winS = WinScene(s, KH)

    #Sets which tiles to render on screen
    renderedTiles = gameS.setRenderGrid()
    
    #For settings scene
    firstTime = True

    #sorted the entities in order of y value
    for i in tileGrid:
        for j in i:
            j.entities = sorted(j.entities, key = lambda entity: entity.y)
    
    CraftWin = CraftingWindow(s, hotbar, KH, player)

    #Makes initial binds
    KH.addTkinterBind("<space>", player.itemInChestMovement)
    KH.addTkinterBind("<c>", lambda e: toggleOpenCrafting(CraftWin, e))
    if sys.platform == 'linux':
        KH.addTkinterBind("<4>", doScroll)
        KH.addTkinterBind("<5>", doScroll)
    else:
        KH.addTkinterBind("<MouseWheel>", doScroll)
    
    KH.addTkinterBind("e", interact)

    #Creates threads
    frameThread = Thread(target=countFrameRate)
    frameThread.daemon = True

    calcThread = Thread(target = doGameCalculations)
    calcThread.daemon = True

    eventThread = Thread(target = customEventHandler)
    eventThread.daemon = True

    graphCalcThread = Thread(target = doGraphicCalcs)
    graphCalcThread.daemon = True

    craftWinThread = Thread(target = craftingWindowCalcs)
    craftWinThread.daemon = True

    alertThread = Thread(target=doAlert)
    alertThread.daemon = True

    dayCycleThread = Thread(target = doDayCycle)
    dayCycleThread.daemon = True
      

    #Starts threads 
    frameThread.start()
    calcThread.start()
    eventThread.start()
    # graphCalcThread.start()
    # craftWinThread.start()
    alertThread.start()
    # dayCycleThread.start()

    sleep(0.1)

    #Does run game
    s.root.after(200, runGame)
        




if __name__ == '__main__':    
    s.canv.after(200,setInitialValues())
    s.canv.focus_set()
    s.canv.mainloop()
    
