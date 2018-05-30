from Scene import *

class MainScene(Scene):
    def __init__(self, GameTitle, screen, KHandler):
        super().__init__("scene_main", screen, KHandler, connections = ["scene_settings", "scene_game"])
        self.options = ["Start Game", "Settings", "Quit Game"]
        self.optionsText = []
        self.title = 0
        self.titleText = GameTitle
    
    
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
        else:
            self.screen.canv.delete(option)

    def changeSceneHandler(self,target):
        self.deleteOptions("All")

        self.change_scene(target)

    def displayOptions(self,xC, yC):
        
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
    
