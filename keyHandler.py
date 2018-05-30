from Camera import Camera

class KeyHandler:
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera
        self.scene = "scene_main"
    
            
    def handlerHandlerP(self, Event):
        # print(Event)
        keycode = Event.keysym
        keysym = Event.keysym
        self.pressHandler(keycode, keysym, self.scene)

    def handlerHandlerR(self, Event):
        # print(Event)
        keycode = Event.keycode
        keysym = Event.keysym
        self.releaseHandler(keycode, keysym, self.scene)

    def pressHandler(self, keycode, keysym, scene):
        if scene == "scene_game":
            if keysym == "Up":
                if self.camera.Vely > -1:
                    self.camera.Vely += -0.1
                    if self.camera.Vely < -1:
                        self.camera.Vely = -1
                print("Up Press")
                # print(self.camera.Movementx, self.camera.Movementy)
            
            elif keysym == "Down":
                if self.camera.Vely < 1:
                    self.camera.Vely += 0.1
                    if self.camera.Vely > 1:
                        self.camera.Vely = 1
                print("Down Press")
                # print(self.camera.Movementx, self.camera.Movementy)
            
            elif keysym == "Right":
                if self.camera.Velx < 1:
                    self.camera.Velx += 0.1
                    if self.camera.Velx > 1:
                        self.camera.Velx = 1
                print("Right Press")
                # print(self.camera.Movementx, self.camera.Movementy)
            
            elif keysym == "Left":
                if self.camera.Velx > -1:
                    self.camera.Velx -= 0.1
                    if self.camera.Velx < -1:
                        self.camera.Velx = -1
                print("Left Press")
                # print(self.camera.Movementx, self.camera.Movementy)
    
    def releaseHandler(self, keycode, keysym, scene):
        if scene == "scene_game":
            if keysym == "w":
                self.w = False
                print("Up Release")
            
            elif keysym == "s":
                self.s = False
                print("Down Release")
            
            elif keysym == "d":
                self.d = False
                print("Right Release")
            
            elif keysym == "a":
                self.a = False
                print("Left Release")
