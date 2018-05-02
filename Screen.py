from tkinter import *

class Screen:
    def __init__(self, width, height, fullscreen, winName):
        self.root = Tk()
        self.width = width
        self.height = height
        self.root.attributes("-fullscreen", fullscreen)
        self.canv = Canvas(self.root, width = self.width, height = self.height)
        self.canv.pack(fill = 'both', expand = True)
        self.root.bind("<F11>", self.toggleFS)
        self.root.title(winName)
        #self.root.bind("<Button-1>", self.tempTestDraw)
    
    def toggleFS(self, Event):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        
    def tempTestDraw(self, Event):
        self.canv.create_oval(Event.x - 5, Event.y - 5, Event.x + 5, Event.y + 5, fill = 'red')


def makeScreen(width, height, fullscreen, winName):
    s = Screen(width, height, fullscreen, winName)
    s.root.bind("<Escape>", lambda e: s.root.destroy())
    return s