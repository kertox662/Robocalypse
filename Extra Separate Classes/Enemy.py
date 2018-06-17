from Entity import *
from PIL import Image, ImageTk
from AstarPathAlgo import *
from math import *

class Enemy(movingEntity):
    def __init__(self, x, y, eType, id, screen, camera, collisionBox, doCollision, hitbox, player):
        sprite = Image.open(image = "images/Robot1.png")
        super().__init__(x,y,eType, id, sprite, screen, camera, collisionBox, doCollision, hitbox)
        self.player = player

    def findPathToPlayer(self):
        pass