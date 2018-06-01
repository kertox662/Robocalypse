#Standard Library
import json as js
import os
from time import sleep
from random import choice
import atexit
import sys

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

#Miscellaneous
from keyHandler import KeyHandler

dependencyPath = __file__.split('EngineMain.py')[0] + "Dependencies"
sys.path.append(dependencyPath)
import InstallPip


# print(sys.path)

TESTING = False


def exitProcedure():
    pass

atexit.register(exit)

def loadSettings(sFile = "data/configs.json"):
    with open(sFile) as jsonFile:
        data = js.load(jsonFile)
    return data

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


def run():
    global firstTime
    
    KH.scene = Scene.current_scene
    # print(Cam.x, Cam.y)
    # print(KH.scene)

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
        gameS.showTiles(tileGrid)

        if KH.aToggle:
            Cam.Velx += -0.1
        if KH.dToggle:
            Cam.Velx += 0.1
        if KH.wToggle:
            Cam.Vely -= 0.1
        if KH.sToggle:
            Cam.Vely += 0.1
        
        if Cam.Velx > 1:
            Cam.Velx = 1
        elif Cam.Velx < -1:
            Cam.Velx = -1
        
        if Cam.Vely > 1:
            Cam.Vely = 1
        elif Cam.Vely < -1:
            Cam.Vely = -1

        Cam.move()

        # print(Cam.Velx, Cam.Vely)

        Cam.Velx *= 0.95
        Cam.Vely *= 0.95

        



def main():
    global sWidth, sHeight
    global mainS, settingsS, gameS, Cam, KH
    global s, firstTime, updatePosition, tileGrid

    if settings["window"]["width"] == None:
        s = makeScreen(1024, 768, settings["window"]["fullscreen"], "GameWindow")
        settings["window"]["width"] = s.canv.winfo_screenwidth()
        settings["window"]["height"] = s.canv.winfo_screenheight()
        
    else:
        s = makeScreen(settings["window"]["width"], settings["window"]["height"], settings["window"]["fullscreen"], "Game Window")

    
    Cam = Camera(s)
    KH = KeyHandler(s,Cam)
    # s.root.bind_all("<Up>", KH.handlerHandlerP)
    # s.root.bind_all("<Down>", KH.handlerHandlerP)
    # s.root.bind_all("<Left>", KH.handlerHandlerP)
    # s.root.bind_all("<Right>", KH.handlerHandlerP)
    # s.root.bind("<KeyRelease>", KH.handlerHandlerR)

    if settings["window"]["fullscreen"] == True:
        sWidth = s.root.winfo_screenwidth()
        sHeight = s.root.winfo_screenheight()
        if TESTING:print(sHeight, sWidth)
        
    else:
        sWidth = int(s.canv.cget('width'))
        sHeight = int(s.canv.cget('height'))
    mainS = MainScene("Zombie Game", s, KH)
    settingsS = SettingsScene(s,KH)
    gameS = GameScene(s,KH)

    
    
    tileGrid = []
    for i in range(tileGridHeight):
        tileGrid.append([])
        for j in range(tileGridWidth):
            tileGrid[i].append(Tile(j * Tile.tileWidth,i * Tile.tileHeight,choice(["red",'blue','yellow','green','orange','purple']), s, Cam))
        
    firstTime = True
    if TESTING: print(sWidth, sHeight)
    run()
    while True:
        run()
        s.canv.update()
        sleep(0.001)




if __name__ == '__main__':
    InstallPip.checkDependencies()
    # GO = GameObject()
    global settings
    settings = loadSettings()
    
    main()
