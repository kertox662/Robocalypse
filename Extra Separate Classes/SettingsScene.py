from Scene import *

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
