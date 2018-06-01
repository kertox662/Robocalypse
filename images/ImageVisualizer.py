from tkinter import *

root = Tk()
c = Canvas(root,width = 600, height = 600)
c.pack()

options = ["knife1.gif", "knife1Highlight.gif"]
options1 = ["crowbar.gif", "crowbarHighlight.gif"]
options2 = ["baseballBat.gif", "baseballBatHighlight.gif"]


toggle = 0
prevToggle = 0


def Pickup(Event):
    item = c.find_closest(Event.x, Event.y)
    print("Clicked on {}".format(c.itemcget(item, "image")))

img0 = PhotoImage(file = options[0])
img0_1 = PhotoImage(file = options[1])
i = c.create_image(100, 300, image = img0, activeimage = img0_1)
c.tag_bind(i, "<1>", Pickup)

img1 = PhotoImage(file = options1[0])
img1_1 = PhotoImage(file = options1[1])
i1 = c.create_image(300, 300, image = img1, activeimage = img1_1)
c.tag_bind(i1, "<1>", Pickup)

img2 = PhotoImage(file = options2[0])
img2_1 = PhotoImage(file = options2[1])
i2 = c.create_image(500, 300, image = img2, activeimage = img2_1)
c.tag_bind(i2, "<1>", Pickup)


c.mainloop()