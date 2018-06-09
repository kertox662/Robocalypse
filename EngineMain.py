#Standard Library
import json as js
import os
from time import sleep
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
from Scene import Scene

#Scenes
from MainScene import *
from SettingsScene import *
from GameScene import *

#Game Scene Stuff
from GameObject import *
from Tile import *
from Camera import Camera
from Player import Player
from Entity import Entity, stationaryEntity, movingEntity
from Hotbar import Hotbar
from CraftingWindow import CraftingWindow

#Downloaded Modules
from PIL import Image, ImageTk, ImageFilter
from pygame import mixer

#Miscellaneous
from keyHandler import KeyHandler
from getData import *

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
        s.canv.config(width = width, height = height)
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
        s.canv.config(width = width, height = height)

        
    
    s.updateDimensions()

    hotbar.x = s.width / 2
    hotbar.y = s.height - 25
    
        


#==========================================
#=============Thread Functions=============
#==========================================

def countFrameRate():
    global frame
    global fps
    while True:
        sleep(1)
        fps = frame
        frame = 0

def displayFPS():
    global fpsText
    text = "{} fps".format(fps)
    s.canv.delete(fpsText)
    fpsText = s.canv.create_text(30, 10, text = text, fill = '#20FF20')

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
            
            

        sleep(1/60)

def customEventHandler():
    global resources, CraftWin, tempFurniture
    while True:
        for e in KH.checkEvents:
                if e == "Place Furniture":
                    print(KH.checkEvents)
                    print(e)
                    if player.isPlacing == False:
                        player.isPlacing = True
                        hotbar.lockCursor = True
                        tempFurniture = FurnitureClass(KH.mouseX, KH.mouseY, hotbar.inventory[hotbar.cursorPosition - 1].furnitureId, s, Cam, player)
                    
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
                                if dist([player.x, player.y], [k.x, k.y]) < 140:
                                    if e == 'Cut Tree':
                                        # print("Tree")
                                        if k.type == "Tree":
                                            if k.isPointInBox([KH.mouseClickx, KH.mouseClicky], "hitbox", True):
                                                resources["wood"]["amount"] += randint(1,5)
                                        
                                    elif e == "Mine Rock":
                                        # print("Rock")
                                        if k.type == "Rock":
                                            if k.isPointInBox([KH.mouseClickx, KH.mouseClicky], "hitbox", True):
                                                resources["stone"]["amount"] += randint(1,5)
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
                                
                                

                            
            
                KH.checkEvents.pop(0)
            
        currentTileX = int(player.x // Tile.tileWidth)
        currentTileY = int(player.y // Tile.tileHeight)
        tileToCheck = tileGrid[currentTileY][currentTileX]
        if int(tileToCheck.id) in [2,29,30,31,32]:
            if tileToCheck.isPointInBox([player.x, player.y + 35]):
                player.wireHP -= 0.1

        elif int(tileToCheck.id) in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]:
            if not tileToCheck.isPointInBox([player.x, player.y + 35]):
                player.wireHP -= 0.1
        
        elif int(tileToCheck.id) in [20,21,22,23,24,25,26,27,28,33,34,35,36]:
            if tileToCheck.isPointInBox([player.x, player.y]):
                Player.playerSpeed = 8.5
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
    # player.drawCollision()

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
        print(tempFurniture)
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




def doScroll(event):
    if CraftWin.isMouseInWindow():
        CraftWin.changeY(event)
    else:
        hotbar.changeCursorPositionScroll(event)

#==========================================================
#====================Grouping Functions====================
#==========================================================


def runGame():
    global firstTime
    global renderedTiles
    global applyButton
    
    KH.scene = Scene.current_scene

    if Scene.current_scene == "scene_main":
        mainS.displayOptions(sWidth//2, sHeight//2)
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

        settingsS.displaySettings(sWidth//2, sHeight//2, *updatedSettings)
        
        s.canv.delete(applyButton)
        applyButton = s.canv.create_text(sWidth // 2, sHeight - 100, text = "Save and Apply", fill = 'black', activefill = 'yellow', font = ('Helvetica', 16))
        s.canv.tag_bind(applyButton, '<Button-1>', saveSettingsEvent)
    
    elif Scene.current_scene == "scene_game":
       drawGroundGraphics()
       drawUIGraphics()

        
    

def setInitialValues():
    global sWidth, sHeight
    global mainS, settingsS, gameS, Cam, KH, player
    global s, firstTime, updatePosition
    global settings , TESTING, testEntity, applyButton
    global renderedTiles, tileGrid, tileData, tileSprites, tileMap
    global frame, fpsText
    global alerts, alertCount, newAlert, UISprites, hotbar, notifBox, notifText
    global resources, itemData, itemSprites
    global CraftWin, costBox, costIcons, costText, resourceOrder
    global tempFurniture, FurnitureClass

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

    settings = loadSettings()
    #=====Screen and Tkinter windows=====
    if settings["window"]["width"] == None:
        s = makeScreen(1024, 768, settings["window"]["fullscreen"], "Robocalypse", __file__.split('EngineMain.py')[0] + "images/Robot16.xpm")
        settings["window"]["width"] = s.canv.winfo_screenwidth()
        settings["window"]["height"] = s.canv.winfo_screenheight()
        
    else:
        s = makeScreen(settings["window"]["width"], settings["window"]["height"], settings["window"]["fullscreen"], "Robocalypse Game", __file__.split('EngineMain.py')[0] + "images/Robot16.xpm")


    import Furniture
    FurnitureClass = Furniture.Furniture

    #=====Tile Data From files=====
    tileData = loadSettings("data/tiles.json")
    tileSprites = []
    for i in range(1,37):
        imgTemp = Image.open(tileData[str(i)]["image"])
        tileSprites.append(ImageTk.PhotoImage(image=imgTemp))

    #=====Item Data From files=====
    itemData = loadSettings("data/items.json")
    itemSprites = []
    for i in itemData:
        itemSprites.append(loadImage(itemData[i]["icon"]))

    resources = {"wood":{"amount": 0, "text":-1, "icon":-1, "sprite": loadImage("images/Resources/Wood Log/log.png"), "spriteSmall":loadImage("images/Resources/Wood Log/logsmall.png")},
                 "metal":{"amount": 0, "text":-1, "icon":-1, "sprite":loadImage("images/Resources/Metal/metal.png"), "spriteSmall":loadImage("images/Resources/Metal/metalSmall.png")},
                 "stone":{"amount":0, "text":-1, "icon": -1, "sprite":loadImage("images/Resources/Rock/rock2.png"),"spriteSmall":loadImage("images/Resources/Rock/rock2small.png")},
                  "wires":{"amount": 0, "text":-1, "icon":-1, "sprite": loadImage("images/Resources/Electrical/wires.png"),"spriteSmall": loadImage("images/Resources/Electrical/wiresSmall.png")}}

    startx = 1600
    starty = 1600

    hotbar = Hotbar(s, itemSprites)
    KH = KeyHandler(s, hotbar)
    Cam = Camera(startx, starty, s, KH)
    player = Player(startx, starty, s, Cam, KH, resources)
    
    with open('data/TileData.txt') as mapD:
        tileMap = mapD.read().split('\n')
    
    for i in range(len(tileMap)):
        tileMap[i] = tileMap[i].split(',')
    
    tileGrid = []
    for i in range(tileGridHeight):
        tileGrid.append([])
        for j in range(tileGridWidth):
            tileGrid[i].append(Tile(j * Tile.tileWidth,i * Tile.tileHeight,tileMap[i][j], tileSprites[int(tileMap[i][j])-1], s, Cam, i, j, tileData[str(tileMap[i][j])]["collision"]))

    if settings["window"]["fullscreen"] == True:
        sWidth = s.root.winfo_screenwidth()
        sHeight = s.root.winfo_screenheight()
        if TESTING:print(sHeight, sWidth)
        
    else:
        sWidth = int(s.canv.cget('width'))
        sHeight = int(s.canv.cget('height'))
    mainS = MainScene("Robocalypse", s, KH)
    settingsS = SettingsScene(s,KH)
    gameS = GameScene(s,Cam, KH, tileGrid, player)

    renderedTiles = gameS.setRenderGrid()
        
    firstTime = True
    if TESTING: print(sWidth, sHeight)

    for i in range(10):
        tempX = randint(1600, 2800)
        tempY = randint(1600, 2800)
        entityChoice = randint(1,2)
        if entityChoice == 1:
            tempEntity = stationaryEntity(tempX, tempY, "Tree", 0, "images/Tree1.png", s, Cam, ((-15, 20, 20, -15),(80,80,106,106)), True, ((-15, 20, 20, -15),(60,60,106,106)))#(-10, 15, 15, -10),(80,80,106,106)
        elif entityChoice == 2:
            tempEntity = stationaryEntity(tempX, tempY, "Rock", 0, "images/Rock1.png", s, Cam, ((-60, 60, 60, -60), (10, 10, 60, 60)), True, ((-60, 60, 60, -60), (-15, -15, 60, 60)))
        tileGrid[tempEntity.tileY][tempEntity.tileX].entities.append(tempEntity)
    
    for i in tileGrid:
        for j in i:
            j.entities = sorted(j.entities, key = lambda entity: entity.y)

    UISpritesData = loadSettings("data/UISprites.json")
    UISprites = {}
    for i in UISpritesData:
        img = Image.open(UISpritesData[i])
        UISprites[i] = ImageTk.PhotoImage(image=img)
    
    CraftWin = CraftingWindow(s, hotbar, KH, player)


    s.root.bind("<space>", lambda e: alerts.put(choice([{"text":"Hello", "delay":1},{"text":"World", "delay":0.5},{"text":"Notification", "delay": 1},{"text":"flrp", "delay":1/4}])))
    s.root.bind("<c>", lambda e: toggleOpenCrafting(CraftWin, e))
    KH.addTkinterBind("<MouseWheel>", doScroll)

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

    hotbar.addItem(1)
    hotbar.addItem(2)
    hotbar.addItem(9)
    hotbar.addItem(10)
    hotbar.addItem(11)
    
    frameThread.start()
    calcThread.start()
    eventThread.start()
    graphCalcThread.start()
    craftWinThread.start()
    alertThread.start()
    sleep(0.5)

    while True:
        runGame()
        s.canv.update()
        sleep(1/60)
        frame += 1
        # print(s.root.geometry())




if __name__ == '__main__':    
    setInitialValues()
    s.root.focus_set()
    s.root.mainloop()
    
