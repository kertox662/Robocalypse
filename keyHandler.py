from Camera import Camera
from pynput import keyboard
from threading import Thread

def keyboardThread(self):
    with keyboard.Listener(on_press=self.onPress, on_release=self.onRelease) as l:
            l.join()


class KeyHandler:
    def __init__(self, screen):
        self.screen = screen
        self.scene = "scene_main"
        self.wToggle = False
        self.aToggle = False
        self.sToggle = False
        self.dToggle = False
        self.shiftToggle = False

        t = Thread(target=keyboardThread, args=(self,))
        t.daemon = True
        t.start()
        
    
            
    def onPress(self, key):
        # print(arg2)
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
    
        # print(self.aToggle, self.wToggle, self.sToggle, self.dToggle)
    
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
        
        
        # print(self.aToggle, self.wToggle, self.sToggle, self.dToggle)