from Tile import *
from GameObject import *
from GameItem import *
from Scene import Scene

class GameScene(Scene):

    def __init__(self, screen, KHandler):
        super().__init__("scene_game", screen, KHandler, connections = ["scene_main", "scene_menu"])

    def showTiles(self, tileArray):
        for i in tileArray:
            for j in i:
                j.display()