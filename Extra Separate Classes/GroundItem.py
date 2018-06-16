from Entity import stationaryEntity
from random import randint
from getData import loadImage

def dist(x1, y1, x2, y2):
    dx = (x2 - x1)**2
    dy = (y2 - y1)**2
    #print(dx, dy)
    l = sqrt(dx + dy)
    
    return l

class GroundItem(stationaryEntity):



    def __init__(self, x, y, entityType, id, sprite, highlight, screen, camera, resources, tile, player, resourceType, delQueue):
        super().__init__(x,y,entityType, id, sprite, screen, camera, None, False, None, tile, delQueue)
        self.resources = resources
        self.player = player
        self.resourceType = resourceType
        self.highlight = loadImage(highlight)

        

    def display(self, player, lessOrGreater, collision, isPlayer = False):
        if lessOrGreater == True:
            self.screen.canv.delete(self.screenObj)
            self.screenObj = self.screen.canv.create_image(self.x - self.camera.x + self.xOff + self.screen.width/2, self.y - self.camera.y + self.yOff + self.screen.height/2, image = self.sprite, activeimage = self.highlight)
            self.screen.canv.tag_bind(self.screenObj, 'e', self.pickUpItem)

    def pickUpItem(self, e):
        # if e.keysym == "e":
        print(e)
        if dist(self.x, self.y, player.x, player.y) < 150:
            self.resources[self.resourceType]["amount"] += randint(1,2)
            
            self.screen.canv.delete(self.screenObj)
            self.tile.entities.remove(self)


        