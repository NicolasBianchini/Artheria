# scenes/login_scene.py
import pygame
from scenes.base_scene import BaseScene
import settings

class LoginScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.profile_manager = self.scene_manager.profile_manager
        self.font = pygame.font.Font(settings.FONT_PATH, settings.DEFAULT_FONT_SIZE)
        self.input_text = ""
        self.message = "Digite seu nome de Guardião e pressione Enter"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.input_text:
                        # Tenta carregar o perfil
                        if not self.profile_manager.load_profile(self.input_text):
                            # Se não existir, cria um novo
                            self.profile_manager.create_profile(self.input_text)
                        
                        profile = self.profile_manager.get_current_profile()
                        if profile.is_calibrated:
                            self.scene_manager.go_to_scene('WorldMapScene')
                        else:
                            self.scene_manager.go_to_scene('CalibrationScene')
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(settings.NIGHT_SKY)
        
        # Mensagem de instrução
        msg_surf = self.font.render(self.message, True, settings.WHITE)
        msg_rect = msg_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2 - 100))
        screen.blit(msg_surf, msg_rect)

        # Caixa de texto
        input_box = pygame.Rect(settings.SCREEN_WIDTH / 2 - 200, settings.SCREEN_HEIGHT / 2, 400, 50)
        pygame.draw.rect(screen, settings.WHITE, input_box, 2)
        
        text_surf = self.font.render(self.input_text, True, settings.WHITE)
        screen.blit(text_surf, (input_box.x + 10, input_box.y + 5))