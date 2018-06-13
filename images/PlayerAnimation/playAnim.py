from tkinter import *
from PIL import Image, ImageTk
from time import sleep

root = Tk()
c = Canvas(root, width = 400, height = 400)
c.pack()

#animBase = "Walking/Left/"
#animFrame = 12

animBase = "Walking/Left/"
animFrame = 11

frames = []
for i in range(animFrame):
    imageTemp = Image.open(animBase + "Frame{}.png".format(i+2))
    pImage = ImageTk.PhotoImage(image = imageTemp)
    frames.append(pImage)


frameNum = 0
sObj = -1

while True:
    c.delete(sObj)
    sprite = frames[(frameNum //4) % animFrame]
    sObj = c.create_image(200, 200, image = sprite)
    c.update()
    sleep(1/60)
    frameNum += 1