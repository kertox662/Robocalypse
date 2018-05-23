from tkinter import *
import sys
import os

# eggPath = "/Users/misha/Desktop/ZombieGame/Pillow-5.1.0-py3.6-win-amd64.egg"
# sys.path.append(eggPath)
# import PIL

# # print(__file__)
# # print(os.listdir("."))

# # DIR = os.path.dirname(__file__)
# # sys.path.append(DIR)

# # import PIL
# print(dir(PIL))
# # # img = PIL.Image("ak47-1.png")

class Screen:
    def __init__(self, width, height, fullscreen, winName):
        self.root = Tk()
        self.width = width
        self.height = height
        self.root.attributes("-fullscreen", fullscreen)
        self.canv = Canvas(self.root, width = self.width, height = self.height)
        self.canv.pack(fill = 'both', expand = True)
        self.root.title(winName)

def makeScreen(width, height, fullscreen, winName):
    s = Screen(width, height, fullscreen, winName)
    s.root.bind("<Escape>", lambda e: s.root.destroy())
    return s
