from tkinter import *

class GameObject:
    def __init__(self, initx, inity, objType, id, sprite):
        self.x = initx
        self.y = inity
        self.type = objType
        self.id = id
        if objType == "img":
            self.sprite = PhotoImage(file = sprite)
        elif objType == "polygon":
            pass
        self.screenObj = -1

    def isOnScreen(self, camera, screen):
        if -100 <= self.x - camera.x <= screen.width + 100:
            if -100 <= self.y - camera.y <= screen.height + 100:
                return True
        
        return False
    
    def display(self, camera, screen):
        screen.canv.delete(self.screenObj)
        if self.isOnScreen(camera, screen):
            if self.type == img:
                self.screenObj = screen.canv.create_image(self.x - camera.x, self.y - camera.y, image = self.sprite)
        

