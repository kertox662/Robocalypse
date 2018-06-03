#Standard Library
import json as js
import os
from time import sleep
from random import choice, randint
import atexit
import sys
from threading import Thread

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
from PIL import Image, ImageTk
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
        
        sleep(1/60)

def doGraphicCalcs():
    global renderedTiles
    while True:
        if Scene.current_scene == "scene_game":
            if gameS.checkRendered(renderedTiles) == False:
                renderedTiles = gameS.setRenderGrid(tileGrid)

        sleep(1/10)

frameThread = Thread(target=countFrameRate)
frameThread.daemon = True

calcThread = Thread(target = doGameCalculations)
calcThread.daemon = True

graphCalcThread = Thread(target = doGraphicCalcs)
graphCalcThread.daemon = True

def runGame():
    global firstTime
    global renderedTiles
    global applyButton
    
    KH.scene = Scene.current_scene

    if Scene.current_scene == "scene_main":
        mainS.displayOptions(sWidth//2, sHeight//2)
        
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
                    updatedSettings = [settings["window"]["width"],settings["window"]["height"],settings["window"]["fullscreen"],settings["sound"]]
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
        gameS.showTiles(renderedTiles)

        player.display()

        testEntity.drawCollision()
        testEntity.display()

        if settings["displayFPS"] == True:
            displayFPS()
    
    



def setInitialValues():
    global sWidth, sHeight
    global mainS, settingsS, gameS, Cam, KH, player
    global s, firstTime, updatePosition
    global settings , TESTING, testEntity
    global renderedTiles, tileGrid, tileData, tileSprites, tileMap
    global frame, fpsText
    global applyButton

    settings = loadSettings()
    TESTING = False
    frame = 0
    fpsText = -1
    applyButton = -1

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
    

    if settings["window"]["fullscreen"] == True:
        sWidth = s.root.winfo_screenwidth()
        sHeight = s.root.winfo_screenheight()
        if TESTING:print(sHeight, sWidth)
        
    else:
        sWidth = int(s.canv.cget('width'))
        sHeight = int(s.canv.cget('height'))
    mainS = MainScene("Robocalypse", s, KH)
    settingsS = SettingsScene(s,KH)
    gameS = GameScene(s,Cam, KH)

    with open('data/TileData.txt') as mapD:
        tileMap = mapD.read().split('\n')
    
    for i in range(len(tileMap)):
        tileMap[i] = tileMap[i].split(',')
    
    tileGrid = []
    for i in range(tileGridHeight):
        tileGrid.append([])
        for j in range(tileGridWidth):
            tileGrid[i].append(Tile(j * Tile.tileWidth,i * Tile.tileHeight, tileSprites[int(tileMap[i][j])-1], s, Cam, i, j))

    renderedTiles = gameS.setRenderGrid(tileGrid)
        
    firstTime = True
    if TESTING: print(sWidth, sHeight)

    testEntity = stationaryEntity(1200, 1200, "img", 0, "images/Tree1.png", s, Cam, ((-10, 80), (15, 80), (15, 106), (-10, 106)), True)
    
    frameThread.start()
    calcThread.start()
    graphCalcThread.start()
    sleep(0.5)

    while True:
        runGame()
        s.canv.update()
        sleep(1/60)
        frame += 1




if __name__ == '__main__':    
    setInitialValues()
    s.root.focus_set()
    s.root.mainloop()
    
