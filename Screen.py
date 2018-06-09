from tkinter import *
import sys
import os
import time

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
        self.fullscreen = fullscreen

        if fullscreen == True:
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
        # self.root.config(cursor = "none")
    
    def updateShownDimensions(self, width, height):
        self.setWidth = width
        self.setHeight = height

    def updateDimensions(self):
        if self.fullscreen:
            self.width = self.root.winfo_width()
            self.height = self.root.winfo_height()
        else:
            self.width = self.setWidth
            self.height = self.setHeight

def makeScreen(width, height, fullscreen, winName, winIcon):
    s = Screen(width, height, fullscreen, winName)
    s.root.bind("<q>", lambda e: s.canv.destroy())
    return s
