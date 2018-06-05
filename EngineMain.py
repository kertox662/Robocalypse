#Standard Library
import json as js
import os
from time import sleep
from random import choice, randint
import atexit
import sys
from threading import Thread
from queue import Queue

dependencyPath = __file__.split('EngineMain.py')[0] + "Dependencies"
sys.path.append(dependencyPath)

#imagesPath = 
#sys.path.append(imagesPath)

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

#Downloaded Modules
from PIL import Image, ImageTk, ImageFilter
from pygame import mixer

#Miscellaneous
from keyHandler import KeyHandler
from getData import *

def exitProcedure():
    pass

atexit.register(exit)


def saveSettingsEvent(Event):
    saveSettings()
    
def saveSettings():
    global s, sWidth, sHeight, settings
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
    
    
    
    global applyButton
    s.canv.delete(applyButton)
    applyButton = -1
    
    settingsS.deleteSettings()
    global firstTime
    firstTime = True
    settingsS.change_scene("scene_main")
    
    if fullScr:
        sWidth = s.canv.winfo_screenwidth()
        sHeight = s.canv.winfo_screenheight()
        
        s.root.geometry("{}x{}+0+0".format(width, height))
        if TESTING:print(s.root.geometry())
        s.canv.config(width = width, height = height)
        s.root.attributes("-fullscreen", fullScr)
    else:
        sWidth = width
        sHeight = height
        
        s.root.attributes("-fullscreen", fullScr)
        s.root.geometry("{}x{}+20+20".format(width, height))
        if TESTING: print(s.root.geometry())
        s.canv.config(width = width, height = height)
    
    s.updateDimensions()

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

            for i in renderedTiles:
                for j in i:
                    for k in j.entities:
                        player.doStationaryCollisions(player.isColliding(k), k)

            
            # if True in player.isColliding(testEntity):
            #     print('colliding')
            # else:
            #     print("not colliding")
        
        sleep(1/60)

def doGraphicCalcs():
    global renderedTiles
    while True:
        if Scene.current_scene == "scene_game":
            if gameS.checkRendered(renderedTiles) == False:
                renderedTiles = gameS.setRenderGrid()

        sleep(1/10)

        

def doAlert():
    global alerts, alertCount, newAlert
    global notifY
    while True:
        if not alerts.empty():
            alertCount += 1
            newAlert = alerts.get()
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

    gameS.displayStationaryBoxes(renderedTiles, "hitBox")
    gameS.displayStationaryEntities(player, False, renderedTiles)

def drawResources():
    resourceList = ["wood", "stone", "metal", "wires"]
    for i in range(len(resourceList)):
        key = resourceList[i]
        s.canv.delete(resources[key]["icon"], resources[key]["text"])
        resources[key]["icon"] = s.canv.create_image(25, 40*i + 25, image = resources[key]["sprite"])
        resources[key]["text"] = s.canv.create_text(50, 40*i + 25, text = str(resources[key]["amount"]))

def drawUIGraphics():
    drawResources()
    if settings["displayFPS"] == True:
        displayFPS()
        
    drawNotifBox()


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
    global alerts, alertCount, newAlert, UISprites, notifBox, notifText
    global resources


    TESTING = False
    frame = 0
    fpsText = -1
    applyButton = -1
    alerts = Queue()
    alertCount = 0
    notifBox = -1
    notifText = -1
    newAlert = {"text":""}

    settings = loadSettings()
    
    if settings["window"]["width"] == None:
        s = makeScreen(1024, 768, settings["window"]["fullscreen"], "Robocalypse", __file__.split('EngineMain.py')[0] + "images/Robot16.xpm")
        settings["window"]["width"] = s.canv.winfo_screenwidth()
        settings["window"]["height"] = s.canv.winfo_screenheight()
        
    else:
        s = makeScreen(settings["window"]["width"], settings["window"]["height"], settings["window"]["fullscreen"], "Robocalypse Game", __file__.split('EngineMain.py')[0] + "images/Robot16.xpm")

    tileData = loadSettings("data/tiles.json")
    tileSprites = []
    for i in range(1,37):
        imgTemp = Image.open(tileData[str(i)]["image"])
        tileSprites.append(ImageTk.PhotoImage(image=imgTemp))

    startx = 1000
    starty = 1000

    KH = KeyHandler(s)
    Cam = Camera(startx, starty, s, KH)
    player = Player(startx, starty, s, Cam, KH)
    
    with open('data/TileData.txt') as mapD:
        tileMap = mapD.read().split('\n')
    
    for i in range(len(tileMap)):
        tileMap[i] = tileMap[i].split(',')
    
    tileGrid = []
    for i in range(tileGridHeight):
        tileGrid.append([])
        for j in range(tileGridWidth):
            tileGrid[i].append(Tile(j * Tile.tileWidth,i * Tile.tileHeight, tileSprites[int(tileMap[i][j])-1], s, Cam, i, j))

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

    for i in range(20):
        tempX = randint(1600, 2800)
        tempY = randint(1600, 2800)
        tempEntity = stationaryEntity(tempX, tempY, "img", 0, "images/Tree1.png", s, Cam, ((-15, 20, 20, -15),(80,80,106,106)), True, ((-15, 20, 20, -15),(60,60,106,106)))#(-10, 15, 15, -10),(80,80,106,106)
        tileGrid[tempEntity.tileY][tempEntity.tileX].entities.append(tempEntity)
    
    for i in tileGrid:
        for j in i:
            j.entities = sorted(j.entities, key = lambda entity: entity.y)

    UISpritesData = loadSettings("data/UISprites.json")
    UISprites = {}
    for i in UISpritesData:
        img = Image.open(UISpritesData[i])
        UISprites[i] = ImageTk.PhotoImage(image=img)
    
    s.root.bind("<space>", lambda e: alerts.put(choice([{"text":"Hello", "delay":1},{"text":"World", "delay":0.5},{"text":"Notification", "delay": 1},{"text":"flrp", "delay":1/4}])))

    resources = {"wood":{"amount": 0, "text":-1, "icon":-1, "sprite": loadImage("images/Resources/Wood Log/log.png")}, "metal":{"amount": 0, "text":-1, "icon":-1, "sprite":loadImage("images/Resources/Metal/metal.png")}, "stone":{"amount":0, "text":-1, "icon": -1, "sprite":loadImage("images/Resources/Rock/rock2.png")}, "wires":{"amount": 0, "text":-1, "icon":-1, "sprite": loadImage("images/Resources/Electrical/wires.png")}}

    frameThread = Thread(target=countFrameRate)
    frameThread.daemon = True

    calcThread = Thread(target = doGameCalculations)
    calcThread.daemon = True

    graphCalcThread = Thread(target = doGraphicCalcs)
    graphCalcThread.daemon = True

    alertThread = Thread(target=doAlert)
    alertThread.daemon = True

    frameThread.start()
    calcThread.start()
    graphCalcThread.start()
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
    
