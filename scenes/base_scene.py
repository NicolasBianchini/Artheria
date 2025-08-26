# scenes/base_scene.py
class BaseScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager

    def handle_events(self, events):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError