# scene_manager.py
from scenes.login_scene import LoginScene
from scenes.calibration_scene import CalibrationScene
from scenes.world_map_scene import WorldMapScene
from scenes.boat_scene import BoatScene
from scenes.test_scene import TestScene

class SceneManager:
    def __init__(self, input_manager, profile_manager):
        self.input_manager = input_manager
        self.profile_manager = profile_manager
        self.initializing = True
        
        # Create scenes dictionary first
        self.scenes = {}
        
        # Then create each scene
        self.scenes['LoginScene'] = LoginScene(self)
        self.scenes['CalibrationScene'] = CalibrationScene(self)
        self.scenes['WorldMapScene'] = WorldMapScene(self)
        self.scenes['BoatScene'] = BoatScene(self)
        self.scenes['TestScene'] = TestScene(self)
        
        self.current_scene_name = 'LoginScene'
        self.current_scene = self.scenes[self.current_scene_name]
        self.running = True
        self.initializing = False

    def go_to_scene(self, scene_name):
        if self.initializing:
            # Defer scene transition until after initialization
            self.current_scene_name = scene_name
            self.current_scene = self.scenes[scene_name]
            return
            
        if scene_name in self.scenes:
            self.current_scene_name = scene_name
            # Recriamos a cena para garantir que ela reinicie seu estado
            # Isso é importante para os minigames
            if scene_name == 'LoginScene':
                self.scenes[scene_name] = LoginScene(self)
            elif scene_name == 'CalibrationScene':
                self.scenes[scene_name] = CalibrationScene(self)
            elif scene_name == 'WorldMapScene':
                self.scenes[scene_name] = WorldMapScene(self)
            elif scene_name == 'BoatScene':
                self.scenes[scene_name] = BoatScene(self)
            elif scene_name == 'TestScene':
                self.scenes[scene_name] = TestScene(self)
            self.current_scene = self.scenes[scene_name]
            print(f"Transicionando para a cena: {scene_name}")
        else:
            print(f"Erro: Cena '{scene_name}' não encontrada.")
            
    def handle_events(self, events):
        self.current_scene.handle_events(events)
        
    def update(self):
        self.current_scene.update()
        
    def draw(self, screen):
        self.current_scene.draw(screen)

    def quit_game(self):
        self.running = False