from Scene import *

TESTING = False
screenOptions = [(1920,1200),(1920,1080),(1680,1050),(1600,900),(1440,900),(1360,768),(1280,1024),(1280,800),(1280,720),(1024,768)]


class SettingsScene(Scene):
    def __init__(self, screen):
        super().__init__("scene_settings",["scene_main", "scene_menu"])
        self.settings = ["Screen Size", "Fullscreen","Sound"]
        self.settingText = []
        self.title = 0

        maxWidth = screen.canv.winfo_screenwidth()
        maxHeight = screen.canv.winfo_screenheight()

        global screenOptions
        for i in range(len(screenOptions)-1, -1, -1):
            if screenOptions[i][0] > maxWidth or screenOptions[i][1] > maxHeight:
                screenOptions.pop(i)
    
    def changeSetting(self, Event, screen):
        item = screen.canv.find_closest(Event.x, Event.y)
        text = screen.canv.itemcget(item, 'text')
        
        selOption = text.split()[0]
        if selOption == 'Screen':
            textSplit = text.split()
            width = int(textSplit[3])
            height = int(textSplit[5])
            index = (screenOptions.index((width, height)) + 1) % len(screenOptions)
            screen.canv.itemconfig(item , text = "Screen Size - {} x {}".format(screenOptions[index][0], screenOptions[index][1]))
            
        elif selOption == 'Sound':
            newVal = not eval(text.split()[-1])
            screen.canv.itemconfig(item , text = "Sound - {}".format(newVal))
        
        
        elif selOption == 'Fullscreen':
            newVal = not eval(text.split()[-1])
            screen.canv.itemconfig(item , text = "Fullscreen - {}".format(newVal))
        
        
        screen.canv.update()

    
    def deleteSettings(self, screen):
        screen.canv.delete(self.title)
        self.title = 0
        for i in range(len(self.settingText)):
            screen.canv.delete(self.settingText[-1])
            self.settingText.pop(-1)
    
    def displaySettings(self, screen, x, y, width, height, fullscreen, sound):
        self.deleteSettings(screen)
##        print(type(fullscreen))
##        if eval(fullscreen) == True:
##            x = screen.root.winfo_screenwidth() // 2
##            y = screen.root.winfo_screenheight() // 2
        if TESTING: print(x,y, fullscreen == True)
        self.title = screen.canv.create_text(x, y*0.5, text = "Settings", font = ('Helvetica', '24'))
        options = [fullscreen , sound]
        
        for i in self.settings:
            if i == 'Screen Size':
                self.settingText.append(screen.canv.create_text(x, y + 50*self.settings.index(i), text = "Screen Size - {} x {}".format(width, height), font = ('Helvetica', '16'), fill = 'black',activefill = 'yellow'))
                screen.canv.tag_bind(self.settingText[-1],"<Button-1>", lambda e: self.changeSetting(e, screen))
            else:
                self.settingText.append(screen.canv.create_text(x, y + 50*self.settings.index(i), text = "{} - {}".format(i,options[self.settings.index(i) - 1]), font = ('Helvetica', '16'), fill = 'black', activefill = 'yellow'))
                screen.canv.tag_bind(self.settingText[-1], "<Button-1>", lambda e: self.changeSetting(e,screen))
