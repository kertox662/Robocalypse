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

    #Sees if the change is possible and changes it if it is
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
        self.switch = False   
    

    def deleteOptions(self, option): #Deletes menu options. 
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


    def changeSceneHandler(self,target): #deletes options and switches scene
        self.deleteOptions("All")
        self.switch = True
        self.change_scene(target)


    def displayOptions(self,xC, yC): #Draws the options on screen and bind clicking them to functions
        self.screen.canv.delete(self.Background) #White background
        self.Background = self.screen.canv.create_rectangle(-200, -200, self.screen.width + 200, self.screen.height + 200, fill = 'white')

        self.deleteOptions('Title') #Title of game
        self.title = self.screen.canv.create_text(xC, yC *0.5, text = self.titleText, font = ('Helvetica', 24))
        
        if len(self.optionsText) > 0: #deletes options
            for i in range(len(self.optionsText)-1 , -1, -1):
                self.deleteOptions(self.optionsText[i])
                self.optionsText.pop(i)
        
        
        for i in range(len(self.options)): #draws options
            text = self.screen.canv.create_text(xC, yC + 50*i, text = self.options[i], activefill = 'yellow',font = ('Helvetica', 16))
            self.optionsText.append(text)
            
            if self.options[i] == "Start Game": #Binds based on which option it is
                self.screen.canv.tag_bind(text, "<Button-1>", lambda e: self.changeSceneHandler('scene_game'))
            elif self.options[i] == "Settings":
                self.screen.canv.tag_bind(text, "<Button-1>", lambda e: self.changeSceneHandler('scene_settings'))
            elif self.options[i] == "Quit Game":
                self.screen.canv.tag_bind(text, "<Button-1>", lambda e: self.screen.root.destroy())



class SettingsScene(Scene): 
    screenOptions = [(1920,1200),(1920,1080),(1680,1050),(1600,900),(1440,900),(1360,768),(1280,1024),(1280,800),(1280,720),(1024,768)] #Starts off with many different screen options
    def __init__(self, screen, KHandler):
        super().__init__("scene_settings", screen, KHandler,connections = ["scene_main", "scene_menu"])
        self.settings = ["Screen Size", "Fullscreen","Sound", "Show FPS", "Day/Night Cycle"]
        self.settingText = []
        self.title = 0

        self.Background = self.screen.canv.create_rectangle(-200, -200, self.screen.width + 200, self.screen.height + 200, fill = 'white')

        maxWidth = screen.canv.winfo_screenwidth() #The size of the screen
        maxHeight = screen.canv.winfo_screenheight()

        for i in range(len(SettingsScene.screenOptions)-1, -1, -1): #removes screen options that are too big
            if SettingsScene.screenOptions[i][0] > maxWidth or SettingsScene.screenOptions[i][1] > maxHeight:
                SettingsScene.screenOptions.pop(i)
    

    def changeSetting(self, Event): #finds the item that was clicked and changes its value
        item = self.screen.canv.find_closest(Event.x, Event.y)
        text = self.screen.canv.itemcget(item, 'text')
        
        selOption = text.split()[0]
        if selOption == 'Screen': #If it's screen size, cycles to next possible resolution
            textSplit = text.split()
            width = int(textSplit[3])
            height = int(textSplit[5])
            index = (screenOptions.index((width, height)) + 1) % len(screenOptions)
            self.screen.canv.itemconfig(item , text = "Screen Size - {} x {}".format(screenOptions[index][0], screenOptions[index][1]))
            
        elif selOption in ['Sound', 'Fullscreen', 'Show', "Day/Night"]:  
            newVal = not eval(text.split()[-1])
            self.screen.canv.itemconfig(item , text = "{} - {}".format(selOption,newVal))
        
        
        else:
            newVal = not eval(text.split()[-1])
            self.screen.canv.itemconfig(item , text = "error - {}".format(newVal))
        
        
        self.screen.canv.update()

    
    def deleteSettings(self): #Deletes the title and option canvas objects
        self.screen.canv.delete(self.title)
        self.title = 0
        for i in range(len(self.settingText)):
            self.screen.canv.delete(self.settingText[-1])
            self.settingText.pop(-1)
        
        self.screen.canv.delete(self.Background)
    

    def displaySettings(self, x, y, width, height, fullscreen, sound, fps, dayNight): #Displays the options with given options
        self.deleteSettings()
        self.Background = self.screen.canv.create_rectangle(-200, -200, self.screen.width + 200, self.screen.height + 200, fill = 'white')


        self.title = self.screen.canv.create_text(x, y*0.5, text = "Settings", font = ('Helvetica', '24'))
        options = [fullscreen, sound, fps, dayNight]
        
        for i in self.settings: #Since screen resolution is 2 words essentially, this is done seperately
            if i == 'Screen Size':
                self.settingText.append(self.screen.canv.create_text(x, y + 50*self.settings.index(i), text = "Screen Size - {} x {}".format(width, height), font = ('Helvetica', '16'), fill = 'black',activefill = 'yellow'))
                self.screen.canv.tag_bind(self.settingText[-1],"<Button-1>", self.changeSetting)
            else:
                self.settingText.append(self.screen.canv.create_text(x, y + 50*self.settings.index(i), text = "{} - {}".format(i,options[self.settings.index(i) - 1]), font = ('Helvetica', '16'), fill = 'black', activefill = 'yellow'))
                self.screen.canv.tag_bind(self.settingText[-1], "<Button-1>", self.changeSetting)





class GameScene(Scene):

    def __init__(self, screen, camera, KHandler, tileArray, player):
        super().__init__("scene_game", screen, KHandler, connections = ["scene_main", "scene_gameOver", "scene_win"])
        self.camera = camera
        self.screen.root.bind("<Escape>", lambda e: self.change_scene("scene_main"))
        self.tileArray = tileArray
        self.player = player
        self.nodeMap = []
        self.ingame = False
    

    def showTiles(self, tileArray): #draws the tiles (the tileArray parameter will almost always be renderedTiles)
        camX = self.camera.x
        camY = self.camera.y
        for i in tileArray:
            for j in i:
                j.display(camX, camY) #tiles are displayed relative to the camera
    

    def displayStationaryEntities(self, player, lOrG, tileArray): #Displays the entities from each tile.
        for i in tileArray:
            for j in i:
                for k in j.entities:
                    k.display(player, lOrG, k.collisionBox)
    

    def displayStationaryBoxes(self, tileArray, boxType): #Displays the collision boxes for each entity for each tile
        for i in tileArray:
            for j in i:
                for k in j.entities:
                    if boxType == "hitBox":
                        k.drawEntityBox(k.hitBox)
                    elif boxType == "collision":
                        k.drawEntityBox(k.collisionBox)
                        
    
    def checkRendered(self, tileArray): #Sees if there are any tiles currently in renderedGrid that are now offscreen
        for i in tileArray:
            for j in i:
                if not j.isOnScreen():
                    return False
        
        return True
    
    def setRenderGrid(self):
        #Sets the boundaries for renderedTiles
        minX = floor((self.camera.x - self.screen.width/2 - 100) / Tile.tileWidth)
        maxX = ceil((self.camera.x + self.screen.width/2 + 100) / Tile.tileWidth)
        
        minY = floor((self.camera.y - self.screen.height/2 - 100) / Tile.tileHeight)
        maxY = ceil((self.camera.y + self.screen.height/2 + 100) / Tile.tileHeight)

        #Caps the boundaries to the edge most tiles
        minX = max(minX, 0)
        maxX = min(maxX, tileGridWidth)

        minY = max(minY, 0)
        maxY = min(maxY, tileGridHeight)

        newRenderArray = []
        for i in self.tileArray[minY:maxY+1]: #From a blank array, adds a list and then adds each tiles to the interior list to make a 2d array
            newRenderArray.append([])
            for j in i[minX:maxX + 1]:
                newRenderArray[-1].append(j)

        return newRenderArray

    #distance formula
    def dist(self, x1, x2, y1 ,y2):
        dx = (x1 - x2) ** 2
        dy = (y1 - y2) ** 2
        l = sqrt(dx + dy)
        return l

    def doNotification(self):
        pass

#Screen for display while loading data
class LoadingScene:
    def __init__(self, screen, percentDone):
        self.screen = screen
        self.playerAnim = loadAnimation("images/PlayerAnimation/Walking/Right/", 14)
        self.percentDone = percentDone

    def updateLoading(self): #Displays bar, percentage, and character animation
        animFrame = 0
        outline, bar, loadingtitle, loadtext, playerFrame = -1,-1,-1,-1, -1
        while self.percentDone[0] < 100:
            self.screen.canv.delete(outline, bar, loadingtitle, loadtext, playerFrame)
            outline = self.screen.canv.create_rectangle(100, self.screen.height/2 - 50, self.screen.width - 100, self.screen.height/2 + 50, width = 3)
            bar = self.screen.canv.create_rectangle(100, self.screen.height/2 - 50, (self.screen.width - 100)*self.percentDone[0]/100, self.screen.height/2 + 50, fill = 'red')
            loadingtitle = self.screen.canv.create_text(self.screen.width /2 , self.screen.height / 2 - 100, text = "Loading, Please Wait...")
            loadtext = self.screen.canv.create_text(self.screen.width / 2, self.screen.height / 2, text = "{}% Complete".format(int(self.percentDone[0])))
            
            playerFrame = self.screen.canv.create_image(100 + (self.screen.width-200)*self.percentDone[0]/100, self.screen.height/2 + 130, image = self.playerAnim[(animFrame) % len(self.playerAnim)])
            self.screen.canv.update()
            animFrame += 1
            sleep(0.02)

        self.screen.canv.delete(outline, bar, loadingtitle, loadtext, playerFrame)

#Scene to go to when fails
class GameOverScene(Scene):
    def __init__(self, screen, KH, player):
        super().__init__("scene_gameOver", screen, KH, ["scene_main"])
    
        self.player = player

        self.title = -1
        self.text = -1
        self.dayText = -1

    def displayGO(self, dayNum): #Displays text on screen. Title of GAME OVER, the reason for failure, and how long you survived
        if self.player.wireHP <= 0:
            text = "You Shutdown!"
        
        else:
            text = "You didn't escape in time!"
        
        if dayNum == 1:
            dayOrDays = "day"
        else:
            dayOrDays = "days"

        self.title = self.screen.canv.create_text(self.screen.width / 2, 200, text = "GAME OVER", font = ("Helvetica", 40))
        self.text = self.screen.canv.create_text(self.screen.width / 2, self.screen.height / 2, text = text)
        self.dayText = self.screen.canv.create_text(self.screen.width / 2, self.screen.height - 100, text = "You survived for {} {}.".format(dayNum, dayOrDays))
        


class WinScene(Scene): #Scene to go to when you win
    def __init__(self, screen, KH):
        super().__init__("scene_win", screen, KH, ["scene_main"])

    def displayWin(self, dayNum): #Displays a congratulatory message
        self.title = self.screen.canv.create_text(self.screen.width / 2, 200, text = "You Escaped the Planet", font = ("Helvetica", 40))
        self.text = self.screen.canv.create_text(self.screen.width / 2, self.screen.height / 2, text = "You escaped the planet!")