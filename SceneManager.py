from math import ceil, floor, sqrt
from threading import Thread
from time import sleep
from getData import *
from GameSceneObjects import Tile, tileGridHeight, tileGridWidth


class Scene:
    current_scene = "scene_main"

    def __init__(self, scene_name, screen, KHandler, connections = None):
        if connections == None or type(connections) != list:
            self.connections = []
        else:
            self.connections = connections
        self.scene_name = scene_name
        self.screen = screen
        self.KH = KHandler

    def change_scene(self, targetscene = None):
        if targetscene in self.connections:
            Scene.current_scene = targetscene





class MainScene(Scene):
    def __init__(self, GameTitle, screen, KHandler):
        super().__init__("scene_main", screen, KHandler, connections = ["scene_settings", "scene_game"])
        self.options = ["Start Game", "Settings", "Quit Game"]
        self.optionsText = []
        self.title = 0
        self.titleText = GameTitle
        self.Background = self.screen.canv.create_rectangle(-200, -200, self.screen.width + 200, self.screen.height + 200, fill = 'white')   
    

    def deleteOptions(self, option):
        if option == 'Title':
            if self.title != 0:
                self.screen.canv.delete(self.title)
        elif option == 'All':
            if self.title != 0:
                self.screen.canv.delete(self.title)            
            for i in range(len(self.optionsText)):
                self.screen.canv.delete(self.optionsText[-1])
                self.optionsText.pop(-1)
            self.screen.canv.delete(self.Background)
        else:
            self.screen.canv.delete(option)


    def changeSceneHandler(self,target):
        self.deleteOptions("All")
        self.change_scene(target)


    def displayOptions(self,xC, yC):
        self.screen.canv.delete(self.Background)
        self.Background = self.screen.canv.create_rectangle(-200, -200, self.screen.width + 200, self.screen.height + 200, fill = 'white')

        self.deleteOptions('Title')
        self.title = self.screen.canv.create_text(xC, yC *0.5, text = self.titleText, font = ('Helvetica', 24))
        
        if len(self.optionsText) == 0:
            for i in range(len(self.options)):
                text = self.screen.canv.create_text(xC, yC + 50*i, text = self.options[i], activefill = 'yellow',font = ('Helvetica', 16))
                self.optionsText.append(text)
                
                if self.options[i] == "Start Game":
                    self.screen.canv.tag_bind(text, "<Button-1>", lambda e: self.changeSceneHandler('scene_game'))
                elif self.options[i] == "Settings":
                    self.screen.canv.tag_bind(text, "<Button-1>", lambda e: self.changeSceneHandler('scene_settings'))
                elif self.options[i] == "Quit Game":
                    self.screen.canv.tag_bind(text, "<Button-1>", lambda e: screen.root.destroy())

        else:
            for i in range(len(self.optionsText)-1 , -1, -1):
                self.deleteOptions(self.optionsText[i])
                self.optionsText.pop(i)
                text = self.screen.canv.create_text(xC, yC + 50*i, text = self.options[i], activefill = 'yellow',font = ('Helvetica', 16))
                self.optionsText.insert(i, text)
                
                if self.options[i] == "Start Game":
                    self.screen.canv.tag_bind(text, "<Button-1>", lambda e: self.changeSceneHandler('scene_game'))
                elif self.options[i] == "Settings":
                    self.screen.canv.tag_bind(text, "<Button-1>", lambda e: self.changeSceneHandler('scene_settings'))
                elif self.options[i] == "Quit Game":
                    self.screen.canv.tag_bind(text, "<Button-1>", lambda e: self.screen.canv.destroy())
    
TESTING = False
screenOptions = [(1920,1200),(1920,1080),(1680,1050),(1600,900),(1440,900),(1360,768),(1280,1024),(1280,800),(1280,720),(1024,768)]






class SettingsScene(Scene):
    def __init__(self, screen, KHandler):
        super().__init__("scene_settings", screen, KHandler,connections = ["scene_main", "scene_menu"])
        self.settings = ["Screen Size", "Fullscreen","Sound", "Show FPS"]
        self.settingText = []
        self.title = 0
        # self.saveFunc = saveFunc

        self.Background = self.screen.canv.create_rectangle(-200, -200, self.screen.width + 200, self.screen.height + 200, fill = 'white')

        maxWidth = screen.canv.winfo_screenwidth()
        maxHeight = screen.canv.winfo_screenheight()

        global screenOptions
        for i in range(len(screenOptions)-1, -1, -1):
            if screenOptions[i][0] > maxWidth or screenOptions[i][1] > maxHeight:
                screenOptions.pop(i)
    

    def changeSetting(self, Event):
        item = self.screen.canv.find_closest(Event.x, Event.y)
        text = self.screen.canv.itemcget(item, 'text')
        
        selOption = text.split()[0]
        if selOption == 'Screen':
            textSplit = text.split()
            width = int(textSplit[3])
            height = int(textSplit[5])
            index = (screenOptions.index((width, height)) + 1) % len(screenOptions)
            self.screen.canv.itemconfig(item , text = "Screen Size - {} x {}".format(screenOptions[index][0], screenOptions[index][1]))
            
        elif selOption in ['Sound', 'Fullscreen', 'Show']:
            newVal = not eval(text.split()[-1])
            self.screen.canv.itemconfig(item , text = "{} - {}".format(selOption,newVal))
        
        
        else:
            newVal = not eval(text.split()[-1])
            self.screen.canv.itemconfig(item , text = "error - {}".format(newVal))
        
        
        self.screen.canv.update()

    
    def deleteSettings(self):
        self.screen.canv.delete(self.title)
        self.title = 0
        for i in range(len(self.settingText)):
            self.screen.canv.delete(self.settingText[-1])
            self.settingText.pop(-1)
        
        self.screen.canv.delete(self.Background)
    

    def displaySettings(self, x, y, width, height, fullscreen, sound, fps):
        self.deleteSettings()
        self.Background = self.screen.canv.create_rectangle(-200, -200, self.screen.width + 200, self.screen.height + 200, fill = 'white')


        if TESTING: print(x,y, fullscreen == True)
        self.title = self.screen.canv.create_text(x, y*0.5, text = "Settings", font = ('Helvetica', '24'))
        options = [fullscreen, sound, fps]
        
        for i in self.settings:
            if i == 'Screen Size':
                self.settingText.append(self.screen.canv.create_text(x, y + 50*self.settings.index(i), text = "Screen Size - {} x {}".format(width, height), font = ('Helvetica', '16'), fill = 'black',activefill = 'yellow'))
                self.screen.canv.tag_bind(self.settingText[-1],"<Button-1>", self.changeSetting)
            else:
                self.settingText.append(self.screen.canv.create_text(x, y + 50*self.settings.index(i), text = "{} - {}".format(i,options[self.settings.index(i) - 1]), font = ('Helvetica', '16'), fill = 'black', activefill = 'yellow'))
                self.screen.canv.tag_bind(self.settingText[-1], "<Button-1>", self.changeSetting)





class GameScene(Scene):

    def __init__(self, screen, camera, KHandler, tileArray, player):
        super().__init__("scene_game", screen, KHandler, connections = ["scene_main", "scene_menu"])
        self.camera = camera
        self.screen.root.bind("<Escape>", lambda e: self.change_scene("scene_main"))
        self.tileArray = tileArray
        self.player = player
        self.nodeMap = []
    

    def showTiles(self, tileArray):
        camX = self.camera.x
        camY = self.camera.y
        for i in tileArray:
            for j in i:
                j.display(camX, camY)
    

    def displayStationaryEntities(self, player, lOrG, tileArray):
        for i in tileArray:
            for j in i:
                for k in j.entities:
                    k.display(player, lOrG, k.collisionBox)
    

    def displayStationaryBoxes(self, tileArray, boxType):
        for i in tileArray:
            for j in i:
                for k in j.entities:
                    if boxType == "hitBox":
                        k.drawEntityBox(k.hitBox)
                    elif boxType == "collision":
                        k.drawEntityBox(k.collisionBox)
                        
    
    def checkRendered(self, tileArray):
        for i in tileArray:
            for j in i:
                if not j.isOnScreen():
                    return False
        
        return True
    
    def setRenderGrid(self):
        minX = floor((self.camera.x - self.screen.width/2 - 100) / Tile.tileWidth)
        maxX = ceil((self.camera.x + self.screen.width/2 + 100) / Tile.tileWidth)
        
        minY = floor((self.camera.y - self.screen.height/2 - 100) / Tile.tileHeight)
        maxY = ceil((self.camera.y + self.screen.height/2 + 100) / Tile.tileHeight)

        minX = max(minX, 0)
        maxX = min(maxX, tileGridWidth)

        minY = max(minY, 0)
        maxY = min(maxY, tileGridHeight)

        newRenderArray = []
        for i in self.tileArray[minY:maxY+1]:
            newRenderArray.append([])
            for j in i[minX:maxX + 1]:
                newRenderArray[-1].append(j)

        # print(len(newRenderArray[0]), len(newRenderArray))
        # self.setNodeMap()

        return newRenderArray
    
    def setNodeMap(self):
        mapRow = [0]*len(self.tileArray[0]) * 20
        nodeMap = [mapRow] * len(self.tileArray) * 20
        for i in range(len(nodeMap)):
            for j in range(len(nodeMap[0])):
                xCoor = j * 20
                yCoor = i * 20
                print("Checking Node at position {},{}".format(xCoor, yCoor))
                isBlocked = False

                xIndex = xCoor // 400
                yIndex = yCoor // 400

                for y in range(-1, 2):
                    for x in range(-1, 2):
                        tile = self.tileArray[yIndex + y][xIndex + x]
                        if self.dist(xCoor, tile.x, yCoor, tile.y) < 700:
                            for ent in tile.entities:
                                if ent.isPointInBox([xCoor, yCorr], "collision"):
                                    isBlocked = True
                                    break

                nodeMap[i][j] = Node(xCoor, yCoor, int(isBlocked))
        self.nodeMap = nodeMap


    def dist(self, x1, x2, y1 ,y2):
        dx = (x1 - x2) ** 2
        dy = (y1 - y2) ** 2
        l = sqrt(dx + dy)
        return l

    def doNotification(self):
        pass

class LoadingScene:
    def __init__(self, screen, percentDone):
        self.screen = screen
        self.playerAnim = loadAnimation("images/PlayerAnimation/Walking/Right/", 14)
        self.percentDone = percentDone

    def updateLoading(self):
        animFrame = 0
        outline, bar, loadingtitle, loadtext, playerFrame = -1,-1,-1,-1, -1
        while self.percentDone[0] < 100:
            self.screen.canv.delete(outline, bar, loadingtitle, loadtext, playerFrame)
            outline = self.screen.canv.create_rectangle(100, self.screen.height/2 - 50, self.screen.width - 100, self.screen.height/2 + 50, width = 3)
            bar = self.screen.canv.create_rectangle(100, self.screen.height/2 - 50, (self.screen.width - 100)*self.percentDone[0]/100, self.screen.height/2 + 50, fill = 'red')
            loadingtitle = self.screen.canv.create_text(self.screen.width /2 , self.screen.height / 2 - 100, text = "Loading, Please Wait...")
            loadtext = self.screen.canv.create_text(self.screen.width / 2, self.screen.height / 2, text = "{}% Complete".format(round(self.percentDone[0], 1)))
            
            playerFrame = self.screen.canv.create_image(100 + (self.screen.width-200)*self.percentDone[0]/100, self.screen.height/2 + 130, image = self.playerAnim[(animFrame) % len(self.playerAnim)])
            print(self.screen.canv.coords(playerFrame))
            self.screen.canv.update()
            animFrame += 1
            sleep(0.02)

        self.screen.canv.delete(outline, bar, loadingtitle, loadtext, playerFrame)