from Camera import Camera
from pynput import keyboard
from threading import Thread

def keyboardThread(self):
    with keyboard.Listener(on_press=self.onPress, on_release=self.onRelease) as l:
            l.join()


class KeyHandler:
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera
        self.scene = "scene_main"
        self.wToggle = False
        self.aToggle = False
        self.sToggle = False
        self.dToggle = False

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
        elif ch == 'a':
            self.aToggle = True
        elif ch == 's':
            self.sToggle = True
        elif ch == 'd':
            self.dToggle = True
    
        print(self.aToggle, self.wToggle, self.sToggle, self.dToggle)
    
    def onRelease(self, key):
        try:
            ch = key.char
            if ch == 'w':
                self.wToggle = False
            elif ch == 'a':
                self.aToggle = False
            elif ch == 's':
                self.sToggle = False
            elif ch == 'd':
                self.dToggle = False
        
        except AttributeError:
            pass
        
        print(self.aToggle, self.wToggle, self.sToggle, self.dToggle)