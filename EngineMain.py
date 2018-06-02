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
    
    s.updateShownDimensions(width, height)
    
    settings['window']['width'] = width
    settings['window']['height'] = height
    settings['window']['fullscreen'] = fullScr
    settings['sound'] = sound
    
    with open('data/configs.json', 'w') as jsonFile:
        js.dump(settings, jsonFile, indent = 4)
    
    
    
    global applyButton
    s.canv.delete(applyButton)
    applyButton = None
    
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


frame = 0

def countFrameRate():
    global frame
    while True:
        sleep(1)
        print(frame)
        frame = 0

# def updateGraphics():
#     global renderedTiles
#     while True:
#         if Scene.current_scene == "scene_game":

            
        


frameThread = Thread(target=countFrameRate)
frameThread.daemon = True
frameThread.start()

# graphicsThread = Thread(target = updateGraphics)
# graphicsThread.daemon = True
# graphicsThread.start()

def runGame():
    global firstTime
    global renderedTiles
    
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
            updatedSettings = [settings["window"]["width"],settings["window"]["height"],settings["window"]["fullscreen"],settings["sound"]]
            
            global applyButton
            applyButton = s.canv.create_text(sWidth // 2, sHeight - 100, text = "Save and Apply", fill = 'black', activefill = 'yellow', font = ('Helvetica', 16))
            s.canv.tag_bind(applyButton, '<Button-1>', saveSettingsEvent)
            
            firstTime = False
        settingsS.displaySettings(sWidth//2, sHeight//2, *updatedSettings)
    
    elif Scene.current_scene == "scene_game":
        if gameS.checkRendered(renderedTiles) == False:
            renderedTiles = gameS.setRenderGrid(tileGrid)
        gameS.showTiles(renderedTiles)

        Cam.updateVelocity()
        Cam.move()
        Cam.applyFriction()
    
    



def setInitialValues():
    global sWidth, sHeight
    global mainS, settingsS, gameS, Cam, KH
    global s, firstTime, updatePosition
    global settings , TESTING
    global renderedTiles, tileGrid, tileData, tileSprites
    global frame

    settings = loadSettings()
    TESTING = False

    if settings["window"]["width"] == None:
        s = makeScreen(1024, 768, settings["window"]["fullscreen"], "Robocalypse", "images/Robot.ico")
        settings["window"]["width"] = s.canv.winfo_screenwidth()
        settings["window"]["height"] = s.canv.winfo_screenheight()
        
    else:
        s = makeScreen(settings["window"]["width"], settings["window"]["height"], settings["window"]["fullscreen"], "Robocalypse Game", "images/Robot.ico")

    tileData = loadSettings("data/tiles.json")
    tileSprites = []
    for i in range(1,29):
        imgTemp = Image.open(tileData[str(i)]["image"])
        tileSprites.append(ImageTk.PhotoImage(image=imgTemp))


    KH = KeyHandler(s)
    Cam = Camera(s, KH)
    

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

    
    
    tileGrid = []
    for i in range(tileGridHeight):
        tileGrid.append([])
        for j in range(tileGridWidth):
            # if i in [0, tileGridHeight - 1] or j in [0, tileGridWidth - 1]:
            #     tileC = 'blue'
            # else:
            #     tileC = 'green'

            choiceID = randint(0,27)           

            tileGrid[i].append(Tile(j * Tile.tileWidth,i * Tile.tileHeight, tileSprites[choiceID], s, Cam, i, j))

    renderedTiles = gameS.setRenderGrid(tileGrid)
        
    firstTime = True
    if TESTING: print(sWidth, sHeight)
    while True:
        runGame()
        s.canv.update()
        sleep(1/60)
        frame += 1




if __name__ == '__main__':    
    setInitialValues()
