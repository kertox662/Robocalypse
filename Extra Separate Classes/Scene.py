class Scene:
    current_scene = "scene_main"

    def __init__(self, scene_name, screen, KHandler, connections = None):
        if connections == None or type(connections) != list:
            self.connections = []
        else:
            self.connections = connections
        self.scene_name = scene_name
        self.screen = screen
        self.KH = KHandler

    def change_scene(self, targetscene = None):
        if targetscene in self.connections:
            Scene.current_scene = targetscene
