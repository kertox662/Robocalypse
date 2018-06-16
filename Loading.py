from tkinter import *
from time import sleep
from getData import loadAnimation

class LoadingScene:
    def __init__(self, screen):
        self.screen = screen
        self.playerAnim = loadAnimation("images/PlayerAnimation/Walking/Right/", 14)

    def updateLoading(self):
        global percentDone
        percentDone = 50
        animFrame = 0
        outline, bar, loadingtitle, loadtext, playerFrame = -1,-1,-1,-1, -1
        while percentDone < 100:
            self.loadCanv.delete(outline, bar, loadingtitle, loadtext, playerFrame)
            outline = self.loadCanv.create_rectangle(100, 300, 500, 400, width = 3)
            bar = self.loadCanv.create_rectangle(100,300, 100 + 400*percentDone, 400, fill = 'red')
            loadingtitle = self.loadCanv.create_text(300, 250, text = "Loading, Please Wait...")
            loadtext = self.loadCanv.create_text(300, 350, text = "{}% Complete".format(round(percentDone, 1)))
            
            playerFrame = self.loadCanv.create_image(100 + 400*percentDone, 480, image = self.playerAnim[(animFrame//2) % len(self.playerAnim)])
            self.loadCanv.update()
            animFrame += 1
            sleep(0.02)

        self.loadCanv.delete(outline, bar, loadingtitle, loadtext, playerFrame)