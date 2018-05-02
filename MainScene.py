from Scene import *

class MainScene(Scene):
    def __init__(self, GameTitle):
        super().__init__("scene_main",["scene_settings", "scene_game"])
        self.options = ["Start Game", "Settings", "Quit Game"]
        self.optionsText = []
        self.title = 0
        self.titleText = GameTitle
    
    
    def deleteOptions(self, screen, option):
        if option == 'Title':
            if self.title != 0:
                screen.canv.delete(self.title)
        elif option == 'All':
            if self.title != 0:
                screen.canv.delete(self.title)            
            for i in range(len(self.optionsText)):
                screen.canv.delete(self.optionsText[-1])
                self.optionsText.pop(-1)
        else:
            screen.canv.delete(option)

    def changeSceneHandler(self,s, target):
        self.deleteOptions(s,"All")
        self.change_scene(target)

    def displayOptions(self,screen, xC, yC):
        
        self.deleteOptions(screen, 'Title')
        self.title = screen.canv.create_text(xC, yC *0.5, text = self.titleText, font = ('Helvetica', 24))
        
        if len(self.optionsText) == 0:
            for i in range(len(self.options)):
                text = screen.canv.create_text(xC, yC + 50*i, text = self.options[i], activefill = 'yellow',font = ('Helvetica', 16))
                self.optionsText.append(text)
                
                if self.options[i] == "Start Game":
                    screen.canv.tag_bind(text, "<Button-1>", lambda e: self.changeSceneHandler(screen,'scene_game'))
                elif self.options[i] == "Settings":
                    screen.canv.tag_bind(text, "<Button-1>", lambda e: self.changeSceneHandler(screen,'scene_settings'))
                elif self.options[i] == "Quit Game":
                    screen.canv.tag_bind(text, "<Button-1>", lambda e: screen.root.destroy())

        else:
            for i in range(len(self.optionsText)-1 , -1, -1):
                self.deleteOptions(screen,self.optionsText[i])
                self.optionsText.pop(i)
                text = screen.canv.create_text(xC, yC + 50*i, text = self.options[i], activefill = 'yellow',font = ('Helvetica', 16))
                self.optionsText.insert(i, text)
                
                if self.options[i] == "Start Game":
                    screen.canv.tag_bind(text, "<Button-1>", lambda e: self.changeSceneHandler(screen,'scene_game'))
                elif self.options[i] == "Settings":
                    screen.canv.tag_bind(text, "<Button-1>", lambda e: self.changeSceneHandler(screen,'scene_settings'))
                elif self.options[i] == "Quit Game":
                    screen.canv.tag_bind(text, "<Button-1>", lambda e: screen.root.destroy())
    
