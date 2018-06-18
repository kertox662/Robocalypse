from tkinter import *
from PIL import Image, ImageTk
from time import sleep

root = Tk()
w = 1920
h = 1200
c = Canvas(root, width = w, height = h)
c.pack()

animBase = "UI/RainAnim/"
animFrame = 11

#animBase = "Walking/RightUp/"
#animFrame = 14

frames = []
for i in range(animFrame):
    imageTemp = Image.open(animBase + "Frame{}.png".format(i+1))
    pImage = ImageTk.PhotoImage(image = imageTemp)
    frames.append(pImage)


frameNum = 0
sObj = -1

while True:
    c.delete(sObj)
    sprite = frames[(frameNum //4) % animFrame]
    sObj = c.create_image(w/2, h/2, image = sprite)
    c.update()
    sleep(1/60)
    frameNum += 1