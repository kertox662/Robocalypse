from GameObject import *
# from PIL import Image, ImageTk

class Entity(GameObject):
    def __init__(self, x, y, entityType, id, sprite, screen, camera, collisionBox, doCollision, xOff = 0, yOff = 0):
        pImg = Image.open(sprite)
        img = ImageTk.PhotoImage(image=pImg)
        super().__init__(x, y, entityType, id, img, screen, camera, xOff, yOff)
        self.collisionBox = collisionBox
        self.doCollision = doCollision
        self.drawnCollision = -1

        self.rawBox = []
        for i in range(len(collisionBox)):
            self.rawBox.append(collisionBox[i][0])
            self.rawBox.append(collisionBox[i][1])
    
    def drawCollision(self):
        self.screen.canv.delete(self.drawnCollision)

        self.rawBox = []
        for i in range(len(self.collisionBox)):
            self.rawBox.append(self.x + self.collisionBox[i][0] - self.camera.x + self.screen.width/2)
            self.rawBox.append(self.y + self.collisionBox[i][1] - self.camera.y + self.screen.height/2)

        self.drawnCollision = self.screen.canv.create_polygon(*self.rawBox, fill = 'red')