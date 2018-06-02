from tkinter import *
import sys
import os

class Screen:
    def __init__(self, width, height, fullscreen, winName):
        self.root = Tk()
        self.setWidth = width
        self.setHeight = height
        self.width = width
        self.height = height
        self.root.attributes("-fullscreen", fullscreen)
        self.canv = Canvas(self.root, width = self.width, height = self.height)
        self.canv.pack(fill = 'both', expand = True)
        self.root.title(winName)
    
    def updateShownDimensions(self, width, height):
        self.setWidth = width
        self.setHeight = height

    def updateDimensions(self):
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()

def makeScreen(width, height, fullscreen, winName):
    s = Screen(width, height, fullscreen, winName)
    s.root.bind("<Escape>", lambda e: s.canv.destroy())
    return s
