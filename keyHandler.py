from GameSceneObjects import Camera
from pynput import keyboard
from threading import Thread

def keyboardThread(self):
    with keyboard.Listener(on_press=self.onPress, on_release=self.onRelease) as l:
            l.join()


class KeyHandler:
    def __init__(self, screen, hotbar, SceneClass):
        self.screen = screen
        self.scene = "scene_main"
        self.hotbar = hotbar

        self.wToggle = False
        self.aToggle = False
        self.sToggle = False
        self.dToggle = False

        self.checkEvents = []
        self.screen.canv.bind("<Button-1>", self.doAction)
        self.screen.root.bind("<Motion>", self.updateMousePostion)
        self.mouseClickx = -1000
        self.mouseClicky = -1000
        self.mouseX = -1000
        self.mouseY = -1000

        t = Thread(target=keyboardThread, args=(self,))
        t.daemon = True
        t.start()

        self.SceneClass = SceneClass
        
    
            
    def onPress(self, key):
        try:
            ch = key.char

        except AttributeError:
            ch = ''
        
        if ch == 'w':
            self.wToggle = True
        if ch == 'a':
            self.aToggle = True
        if ch == 's':
            self.sToggle = True
        if ch == 'd':
            self.dToggle = True
    
    
    def onRelease(self, key):
        try:
            ch = key.char
            if ch == 'w':
                self.wToggle = False
            if ch == 'a':
                self.aToggle = False
            if ch == 's':
                self.sToggle = False
            if ch == 'd':
                self.dToggle = False
            
        
        except AttributeError:
            pass
    
    def doAction(self, event):
        if self.SceneClass.current_scene == "scene_game":
            if self.hotbar.inventory[self.hotbar.cursorPosition - 1] == 0:
                return

            elif self.hotbar.inventory[self.hotbar.cursorPosition - 1].id == 1:
                self.checkEvents.append("Cut Tree")
            
            elif self.hotbar.inventory[self.hotbar.cursorPosition - 1].id == 2:
                self.checkEvents.append("Mine Rock")
            
            elif self.hotbar.inventory[self.hotbar.cursorPosition - 1].id in [7,8,9,10,11,12,13]:
                self.checkEvents.append("Place Furniture")
            
            elif self.hotbar.inventory[self.hotbar.cursorPosition - 1].id == 6:
                self.checkEvents.append("Use Battery")
            
            else:
                return
            
            self.mouseClickx = event.x
            self.mouseClicky = event.y

    def cancelAction(self, event):
        self.checkEvents.append("Cancel")

    def updateMousePostion(self, event):
        self.mouseX = event.x 
        self.mouseY = event.y
    
    def addTkinterBind(self, bind, function):
        self.screen.root.bind(bind, function)
        



        