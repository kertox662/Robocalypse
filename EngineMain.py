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

import InstallPip
if __name__ == '__main__':
    InstallPip.checkDependencies()

#Parent Classes
from Screen import *
from getData import *

settings = loadSettings()
    #=====Screen and Tkinter windows=====
    #print("ABout toe meke screen")
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


def exitProcedure():
    pass

atexit.register(exit)


def dist(p1, p2):
    l = sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )
    return l

def saveSettingsEvent(Event):
    saveSettings()
    
def saveSettings():
    global s, sWidth, sHeight, settings, hotbar
    updatedSettings = []
    for item in settingsS.settingText:
        itemText = s.canv.itemcget(item, 'text').split()
        if TESTING: print(itemText[-1])
        if itemText[0:2] == ['Screen', 'Size']:
            updatedSettings.append(itemText[3])
            updatedSettings.append(itemText[5])
        else:
            updatedSettings.append(itemText[-1])
    
    if TESTING: print(updatedSettings)
    width = int(updatedSettings[0])
    height = int(updatedSettings[1])
    fullScr = eval(updatedSettings[2])
    sound = eval(updatedSettings[3])
    showFps = eval(updatedSettings[4])
    
    s.updateShownDimensions(width, height)
    
    settings['window']['width'] = width
    settings['window']['height'] = height
    settings['window']['fullscreen'] = fullScr
    settings['sound'] = sound
    settings['displayFPS'] = showFps
    
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
    
    if fullScr == True:
        # s.root.geometry("{}x{}+0+0".format(width, height))
        if TESTING:print(s.root.geometry())
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
        if TESTING: print(s.root.geometry())
    
    
    s.canv.config(width = s.width, height = s.height)

        
    
    s.updateDimensions()

    hotbar.x = s.width / 2
    hotbar.y = s.height - 25
    
        


#==========================================
#=============Thread Functions=============
#==========================================

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

def displayFPS():
    global fpsText
    text = "{} fps".format(fps)
    s.canv.delete(fpsText)
    fpsText = s.canv.create_text(37, 10, text = text, fill = '#20FF20')

def doGameCalculations():
    
    while True:
        if Scene.current_scene == "scene_game":
            player.applyFriction()            
            player.updateVelocity()
            player.move()
            player.checkNearTable(renderedTiles)

            for i in renderedTiles:
                for j in i:
                    for k in j.entities:
                        player.doStationaryCollisions(player.isColliding(k), k)
                        k.checkLife()
            
            

        sleep(1/60)

def customEventHandler():
    global resources, CraftWin, tempFurniture
    while True:
        for e in KH.checkEvents:
                if e == "Place Furniture":
                    # print(KH.checkEvents)
                    # print(e)
                    if player.isPlacing == False:
                        player.isPlacing = True
                        hotbar.lockCursor = True
                        curTileX = int(player.x // Tile.tileWidth)
                        curTileY = int(player.y // Tile.tileHeight)
                        curTile = tileGrid[curTileY][curTileX]
                        tempFurniture = Furniture(KH.mouseX, KH.mouseY, hotbar.inventory[hotbar.cursorPosition - 1].furnitureId, s, Cam, player, deleteQueue, curTile)
                        curTile.entities.sort(key = lambda entity: entity.y)
                    
                    if player.isPlacing == True:
                        if tempFurniture.shownSprite == tempFurniture.spriteGreen:
                            tempFurniture.isPlacing = False
                            tempFurniture.doCollision = True
                            
                            tileX = int(tempFurniture.x // Tile.tileWidth)
                            tileY = int(tempFurniture.y // Tile.tileHeight)
                            tileGrid[tileY][tileX].entities.append(tempFurniture)

                            tempFurniture = None

                            player.isPlacing = False
                            hotbar.lockCursor = False
                            hotbar.inventory[hotbar.cursorPosition - 1] = 0
                            
                
                
                else:
                    for i in renderedTiles:
                        for j in i:
                            for k in j.entities:
                                if k.life > 0:
                                    if player.actionFrame == 0:
                                        if e == 'Cut Tree':
                                            # print("Tree")
                                            if k.type == "Tree":
                                                player.doingAction = "Tree"
                                                player.actionFrame = 0
                                                player.Velx = 0
                                                player.Vely = 0
                                                if dist([player.x, player.y], [k.x, k.y]) < 280:
                                                    print("Close Enough")
                                                    if k.isPointInBox([KH.mouseClickx, KH.mouseClicky], "hitbox", True):
                                                        print("In box")
                                                        amount = randint(1,5)
                                                        resources["wood"]["amount"] += amount
                                                        k.life -= amount
                                                        print(k.life)
                                                
                                        elif e == "Mine Rock":
                                            player.doingAction = "Rock"
                                            player.actionFrame = 0
                                            player.Velx = 0
                                            player.Vely = 0
                                            print("=" * 20)
                                            if k.type == "Rock":
                                                if dist([player.x, player.y], [k.x, k.y]) < 280:
                                                    if k.isPointInBox([KH.mouseClickx, KH.mouseClicky], "hitbox", True):
                                                        amountStone = randint(1,5)
                                                        resources["stone"]["amount"] += amountStone
                                                        k.life -= amountStone
                                                        print(k.life)
                                                        metalChance = randint(1,100)
                                                        if metalChance <= 7:
                                                            amountChance = randint(1,100)
                                                            if amountChance <= 80:
                                                                amount = 1
                                                            elif amountChance <= 98:
                                                                amount = 2
                                                            else:
                                                                amount = 3
                                                            resources["metal"]["amount"] += amount
                                                        # 
                                                    
                            
                                

                            
            
                KH.checkEvents.pop(0)
            
        currentTileX = int(player.x // Tile.tileWidth)
        currentTileY = int((player.y + 35) // Tile.tileHeight)
        tileToCheck = tileGrid[currentTileY][currentTileX]
        if int(tileToCheck.id) in [2, 19, 20, 21, 22]:
            if tileToCheck.isPointInBox([player.x, player.y + 35]):
                player.wireHP -= 0.1
                Player.playerSpeed = 5
            
            else:
                Player.playerSpeed = 7

        elif int(tileToCheck.id) in [4,5,6,7,8,9,10,11]:
            if not tileToCheck.isPointInBox([player.x, player.y + 35]):
                player.wireHP -= 0.1
                Player.playerSpeed = 5
            
            else:
                Player.playerSpeed = 7
        
        elif int(tileToCheck.id) in [12,13,14,15,16,17,18,23,24,25,26]:
            if tileToCheck.isPointInBox([player.x, player.y]):
                Player.playerSpeed = 8.5
            else:
                Player.playerSpeed = 7
        
        else:
            Player.playerSpeed = 7
        
        if CraftWin.toDoCrafting != False:
            costForItem = itemData[str(CraftWin.toDoCrafting)]["cost"]
            curResources = []
            for i in resourceOrder:
                curResources.append(resources[i]["amount"])
            
            # print(costForItem, curResources)
            # print(resources)
            craftAvailable = True
            for i in range(len(curResources)):
                if curResources[i] < costForItem[i]:
                    craftAvailable = False
                # print(craftAvailable)
            
            if craftAvailable == True:
                if hotbar.addItem(CraftWin.toDoCrafting):
                    for i in resourceOrder:
                        resources[i]["amount"] -= costForItem[resourceOrder.index(i)]
                
                else:
                    alerts.put({"text":"There is not enough space in the\ninventory to craft this item", "delay":2.5})
            
            else:
                alerts.put({"text":"Insufficient Resources to craft this item", "delay":2.5})
            
            CraftWin.toDoCrafting = False
        sleep(1/60)
    

def doGraphicCalcs():
    global renderedTiles
    while True:
        if Scene.current_scene == "scene_game":
            if gameS.checkRendered(renderedTiles) == False:
                renderedTiles = gameS.setRenderGrid()
            
            player.chooseAnimFrame()

        sleep(1/60)

def craftingWindowCalcs():
    global CraftWin
    while True:
        if CraftWin.openWindow:
            if CraftWin.x < 112:
                CraftWin.x += 8
        
        else:
            if CraftWin.x > -112:
                CraftWin.x -= 8
        
        sleep(1/60)
        

def doAlert():
    global alerts, alertCount, newAlert
    global notifY
    while True:
        if not alerts.empty():
            alertCount += 1
            newAlert = alerts.get()
            if Scene.current_scene == "scene_game":
                while notifY < 80:
                    notifY += 5
                    sleep(1/60)
                sleep(newAlert["delay"])
                while notifY > -85:
                    notifY -= 5
                    sleep(1/60)
                sleep(1/4)
       
        else:
            notifY = -85
        
        sleep(1/60)
    

def doPathFindingCalc():
    start = time()
    currentNodeMap = []#[[]]*(len(renderedTiles) * 20)
    for i in range(len(renderedTiles)):
        for row in range(20):
            currentNodeMap.append([])
        for j in range(len(renderedTiles[0])):
            curTile = renderedTiles[i][j]
            for y in range(20):
                for x in range(20):
                    curNode = curTile.nodeMap[y][x]
                    # print(curNode.x, curNode.y)
                    # print(y, i*20)
                    currentNodeMap[y + i*20].append(Node.fromCopy(curNode))
    print(time() - start)
    print(len(currentNodeMap), len(currentNodeMap[0]))
    # for i in currentNodeMap:
    #     for j in i:
    #         print(j.x, j.y)

def loadTiles():
    global tileGrid, percentDone
    tileGrid = []
    

    print("Starting to Build World...")
    for i in range(tileGridHeight):
        percentDone[0] = (i + 1) / tileGridHeight * 100
        if percentDone[0] % 10 == 0:
            print("{}% complete...".format(int(percentDone[0])))
        tileGrid.append([])
        for j in range(tileGridWidth):
            tileId = tileMap[i][j]
            variationAmount = tileData[str(tileId)]["variations"]
            if variationAmount > 1:
                variationChoice = randint(0,variationAmount - 1)
            else:
                variationChoice = 0
            
            sprite = tileSprites[str(tileId)][variationChoice]
            tileGrid[i].append(Tile(j * Tile.tileWidth,i * Tile.tileHeight,tileId, sprite, s, Cam, i, j, tileData[str(tileMap[i][j])]["collision"]))
            curTile = tileGrid[i][j]
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
                
                curTile.setNodeMap(entityArrangement[0])
            
            else:
                curTile.setNodeMap([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    
    print("Finished Building World!")


def testDraw():
    global s
    x = s.canv.create_oval(100, 100, 200, 200, fill = 'red')
    while True:
        s.canv.delete(x)
        x = s.canv.create_oval(100, 100, 200, 200, fill = 'red')
        s.canv.update()
        sleep(0.05)


#===================================================
#==============Draw Graphics Functions==============
#===================================================
def toggleOpenCrafting(cWin, event):
    if Scene.current_scene == "scene_game":
        # print("toggled")
        cWin.openWindow = not cWin.openWindow

def drawNotifBox():
    global notifBox, notifText
    s.canv.delete(notifBox)
    s.canv.delete(notifText)
    notifBox = s.canv.create_image(s.width - 240, notifY, image = UISprites["Notification"])
    notifText = s.canv.create_text(s.width - 240, notifY, text = newAlert["text"])

def drawGroundGraphics():
    gameS.showTiles(renderedTiles)

    gameS.displayStationaryEntities(player, True, renderedTiles)
    player.display(player, True, player.collisionBox, True)
    # player.drawEntityBox(player.collisionBox)

    # gameS.displayStationaryBoxes(renderedTiles, "collision")
    gameS.displayStationaryEntities(player, False, renderedTiles)

def drawResources():
    for i in range(len(resourceOrder)):
        key = resourceOrder[i]
        s.canv.delete(resources[key]["icon"], resources[key]["text"])
        resources[key]["icon"] = s.canv.create_image(25, 40*i + 70, image = resources[key]["sprite"])
        resources[key]["text"] = s.canv.create_text(50, 40*i + 70, text = str(resources[key]["amount"]))

def drawTempFurniture():
    if tempFurniture != None:
        tempFurniture.chooseSprite(renderedTiles)
        if tempFurniture.isPlacing:
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

    if not CraftWin.openWindow:
        CraftWin.currentCostWindow = None

    if CraftWin.currentCostWindow != None:
        xPos = KH.mouseX
        yPos = KH.mouseY
        costBox = s.canv.create_rectangle(2, yPos - 60, 224, yPos - 15, fill = 'white', outline = 'black')
        for i in range(4):
            costIcons.append(s.canv.create_image(24 + 48*i, yPos - 50, image = resources[resourceOrder[i]]["spriteSmall"]))
            
            curCost = CraftWin.currentCostWindow[i]
            if resources[resourceOrder[i]]["amount"] >= curCost:
                color = 'green'
            else:
                color = 'red'
            
            costText.append(s.canv.create_text(24 + 48*i, yPos - 30, text = str(curCost), fill = color))
        


def drawUIGraphics():
    drawResources()
    
    if settings["displayFPS"] == True:
        displayFPS()
    
    drawTempFurniture()
    hotbar.display()
    CraftWin.display()
    drawCostWindow()
    player.displayLife()
    drawNotifBox()

def emptyDelQueue():
    global deleteQueue
    if not deleteQueue.empty():
        objToDelete = deleteQueue.get()
        s.canv.delete(objToDelete.screenObj)
        objToDelete.tile.entities.remove(objToDelete)


def doScroll(event):
    if CraftWin.isMouseInWindow():
        CraftWin.changeY(event)
    else:
        hotbar.changeCursorPositionScroll(event)

def interact(event):

    x = KH.mouseX + Cam.x - s.width/2
    y = KH.mouseY + Cam.y - s.height/2

    print("Player:", player.x, player.y)
    print("Clicked:",x,y)

    indX = int(x // Tile.tileWidth)
    indY = int(y // Tile.tileHeight)

    curTile = tileGrid[indY][indX]

    if dist([x, y], [player.x, player.y]) < 200:
        for i in curTile.entities:
            if dist([x,y], [i.x, i.y]) < 30:
                i.pickUpItem()
    
    else:
        print(dist([x, y], [player.x, player.y]))

#==========================================================
#====================Grouping Functions====================
#==========================================================


def runGame():
    global firstTime
    global renderedTiles
    global applyButton
    
    KH.scene = Scene.current_scene

    if Scene.current_scene == "scene_main":
        mainS.displayOptions(s.width//2, s.height//2)
        for i in tileGrid:
            for j in i:
                s.canv.delete(j.screenObj)
                for k in j.entities:
                    s.canv.delete(k.screenObj)
        s.canv.delete(player.screenObj)
        for i in renderedTiles:
            for j in i:
                for k in j.entities:
                    s.canv.delete(k.screenObj)
        s.canv.update()
        
    elif Scene.current_scene == "scene_settings":
        if not firstTime:
            updatedSettings = []
            for item in settingsS.settingText:
                itemText = s.canv.itemcget(item, 'text').split()
                try:
                    if itemText[0:2] == ['Screen', 'Size']:
                        updatedSettings.append(itemText[3])
                        updatedSettings.append(itemText[5])
                    else:
                        updatedSettings.append(itemText[-1])
                except IndexError:
                    updatedSettings = [settings["window"]["width"],settings["window"]["height"],settings["window"]["fullscreen"],settings["sound"], settings["displayFPS"]]
                    saveSettings()
                    break
                        
        else:
            updatedSettings = [settings["window"]["width"],settings["window"]["height"],settings["window"]["fullscreen"],settings["sound"], settings["displayFPS"]]
            firstTime = False

        settingsS.displaySettings(s.width//2, s.height//2, *updatedSettings)
        
        s.canv.delete(applyButton)
        applyButton = s.canv.create_text(s.width // 2, s.height - 100, text = "Save and Apply", fill = 'black', activefill = 'yellow', font = ('Helvetica', 16))
        s.canv.tag_bind(applyButton, '<Button-1>', saveSettingsEvent)
    
    elif Scene.current_scene == "scene_game":
       drawGroundGraphics()
       drawUIGraphics()
       emptyDelQueue()

    #    print(renderedTiles[0][0].x, renderedTiles[0][0].y)

        
    

def setInitialValues():
    global sWidth, sHeight
    global mainS, settingsS, gameS, Cam, KH, player
    global s, firstTime, updatePosition
    global settings , TESTING, testEntity, applyButton
    global renderedTiles, tileGrid, tileData, tileSprites, tileMap
    global frame, fpsText
    global alerts, alertCount, newAlert, UISprites, hotbar, notifBox, notifText
    global resources, itemData, itemSprites, deleteQueue
    global CraftWin, costBox, costIcons, costText, resourceOrder
    global tempFurniture
    global entityData, entityArrangementData, entitySprites, entityHighlights, entityAnimations, groundItemData, percentDone

    #=====Primitive Variables=====
    TESTING = False
    frame = 0
    fpsText = -1
    applyButton = -1
    alerts = Queue()
    alertCount = 0
    notifBox = -1
    notifText = -1
    costBox = -1
    tempFurniture = None
    costIcons = []
    costText = []
    newAlert = {"text":""}
    resourceOrder = ["wood", "stone", "metal", "wires"]
    deleteQueue = Queue()

    settings = loadSettings()
    #=====Screen and Tkinter windows=====
    #print("ABout toe meke screen")
    
    # if settings["window"]["width"] == None:
    #     s = makeScreen(1024, 768, settings["window"]["fullscreen"], "Robocalypse", __file__.split('EngineMain.py')[0] + "images/Robot16.xpm")
    #     settings["window"]["width"] = s.canv.winfo_screenwidth()
    #     settings["window"]["height"] = s.canv.winfo_screenheight()
        
    # else:
    #     s = makeScreen(settings["window"]["width"], settings["window"]["height"], settings["window"]["fullscreen"], "Robocalypse Game", __file__.split('EngineMain.py')[0] + "images/Robot16.xpm")



   
    

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
    entitySprites = {}
    entityHighlights = {}
    entityAnimations = {}

    for i in entityData:
        entitySprites[i] = loadImage(entityData[i]["sprite"])
        entityAnimations[i] = []
        curAnimations = entityData[i]["animations"]
        for j in range(0,len(curAnimations), 2):
            entityAnimations[i].append(loadAnimation(curAnimations[j], curAnimations[j+1]))
    
    for i in groundItemData:
        entitySprites[i] = loadImage(groundItemData[i]["sprite"])
        entityHighlights[i] = loadImage(groundItemData[i]["spriteHighlight"])

    tileSprites = {}
    for i in range(1,27):
        tileSprites[str(i)] = []
        imageBase = tileData[str(i)]["imageBase"]
        for j in range(1, tileData[str(i)]["variations"] + 1):
            imagePath = "{}{}.png".format(imageBase, j)
            tileSprites[str(i)].append(loadImage(imagePath))

    itemSprites = []
    for i in itemData:
        itemSprites.append(loadImage(itemData[i]["icon"]))
    
    UISprites = {}
    for i in UISpritesData:
        UISprites[i] = loadImage(UISpritesData[i])

    resources = {"wood":{"amount": 0, "text":-1, "icon":-1, "sprite": loadImage("images/Resources/Wood Log/log.png"), "spriteSmall":loadImage("images/Resources/Wood Log/logsmall.png")},
                 "metal":{"amount": 0, "text":-1, "icon":-1, "sprite":loadImage("images/Resources/Metal/metal.png"), "spriteSmall":loadImage("images/Resources/Metal/metalSmall.png")},
                 "stone":{"amount":0, "text":-1, "icon": -1, "sprite":loadImage("images/Resources/Rock/rock2.png"),"spriteSmall":loadImage("images/Resources/Rock/rock2small.png")},
                  "wires":{"amount": 0, "text":-1, "icon":-1, "sprite": loadImage("images/Resources/Electrical/wires.png"),"spriteSmall": loadImage("images/Resources/Electrical/wiresSmall.png")}}
    
    
    print("Finished loading images!")
    
    startx = 1900
    starty = 1200

    hotbar = Hotbar(s, itemSprites)
    KH = KeyHandler(s, hotbar)
    Cam = Camera(startx, starty, s, KH)
    player = Player(startx, starty, s, Cam, KH, resources)
    
    

    

    with open('data/TileData.txt') as mapD:
        tileMap = mapD.read().split('\n')
    
    for i in range(len(tileMap)):
        tileMap[i] = tileMap[i].split(',')

    percentDone = [0]

    loadingThread = Thread(target = loadTiles)
    loadingThread.daemon = True
    loadingThread.start()

    loadScene = LoadingScene(s, percentDone)
    loadScene.updateLoading()

    

    mainS = MainScene("Robocalypse", s, KH)
    settingsS = SettingsScene(s,KH)
    gameS = GameScene(s,Cam, KH, tileGrid, player)

    renderedTiles = gameS.setRenderGrid()
        
    firstTime = True
    if TESTING: print(sWidth, sHeight)

    
    for i in tileGrid:
        for j in i:
            j.entities = sorted(j.entities, key = lambda entity: entity.y)
    
    CraftWin = CraftingWindow(s, hotbar, KH, player)


    KH.addTkinterBind("<space>", lambda e: alerts.put(choice([{"text":"Hello", "delay":1},{"text":"World", "delay":0.5},{"text":"Notification", "delay": 1},{"text":"flrp", "delay":1/4}])))
    KH.addTkinterBind("<c>", lambda e: toggleOpenCrafting(CraftWin, e))
    if sys.platform == 'linux':
        KH.addTkinterBind("<4>", doScroll)
        KH.addTkinterBind("<5>", doScroll)
    else:
        KH.addTkinterBind("<MouseWheel>", doScroll)
    
    KH.addTkinterBind("e", interact)
    
    # print(itemData)
    # print("===============================")
    # print(itemSprites)

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

    pathFindingThread = Thread(target = doPathFindingCalc)
    pathFindingThread.daemon = True
    # gameS.setNodeMap()
    # gameS.setNodesThread.start()

    testThread = Thread(target=testDraw)
    testThread.daemon = True
    

    hotbar.addItem(1)
    hotbar.addItem(2)
    hotbar.addItem(9)
    
    frameThread.start()
    calcThread.start()
    eventThread.start()
    graphCalcThread.start()
    craftWinThread.start()
    alertThread.start()
    pathFindingThread.start()
    # testThread.start()

    sleep(0.1)

    while True:
        runGame()
        s.canv.update()
        sleep(1/60)
        frame += 1
        # print(s.root.geometry())




if __name__ == '__main__':    
    s.canv.after(200,setInitialValues())
    s.canv.focus_set()
    s.canv.mainloop()
    
