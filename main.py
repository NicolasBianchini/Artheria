# main.py
import pygame
import settings
from input_manager import InputManager
from scene_manager import SceneManager
from profile_manager import ProfileManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        
        self.input_manager = InputManager(mic_id=settings.MIC_DEVICE_ID)
        self.profile_manager = ProfileManager()
        self.scene_manager = SceneManager(self.input_manager, self.profile_manager)

    def run(self):
        self.input_manager.start()
        
        while self.scene_manager.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.scene_manager.quit_game()
            
            self.scene_manager.handle_events(events)
            self.scene_manager.update()
            
            self.screen.fill(settings.BLACK)
            self.scene_manager.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(settings.FPS)
            
        self.quit()

    def quit(self):
        print("Encerrando Aetheria...")
        self.input_manager.stop()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()