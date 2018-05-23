class Camera:
    def __init__(self, screen):
        self.x = screen.width/2
        self.y = screen.height/2
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy*-1
    
    def setCoords(self, newX, newY):
        self.x = newX
        self.y = newY
