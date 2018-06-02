from tkinter import *
from getData import loadSettings

class GameObject:
    def __init__(self, initx, inity, objType, id, sprite, screen, camera):
        self.x = initx
        self.y = inity
        self.type = objType
        self.id = id
        self.screen = screen
        self.camera = camera
        if objType == "img":
            self.sprite = PhotoImage(file = sprite)
        elif objType == "polygon":
            pass
        self.screenObj = -1

    def isOnScreen(self):
        if -100 - self.screen.width/2 <= self.x - self.camera.x + self.screen.width/2<= self.screen.width + 100:
            if -100 - self.screen.height/ 2<= self.y - self.camera.y + self.screen.height/2 <= self.screen.height + 100:
                return True
        
        return False
    
    def display(self, camera, screen):
        self.screen.canv.delete(self.screenObj)
        if self.isOnScreen():
            if self.type == "img":
                self.screenObj = self.screen.canv.create_image(self.x - camera.x, self.y - camera.y, image = self.sprite)

        

