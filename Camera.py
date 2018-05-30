class Camera:
    camSpeed = 10

    def __init__(self, screen):
        self.Velx = 0
        self.Vely = 0

        self.x = screen.width/2
        self.y = screen.height/2
        self.screen = screen
        

    def move(self):
        self.x += self.Velx * Camera.camSpeed
        self.y += self.Vely * Camera.camSpeed
    
    def setCoords(self, newX, newY):
        self.x = newX
        self.y = newY
