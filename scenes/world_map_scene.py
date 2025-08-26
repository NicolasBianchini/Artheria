# scenes/world_map_scene.py
import pygame
from scenes.base_scene import BaseScene
import settings

class WorldMapScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.profile = self.scene_manager.profile_manager.get_current_profile()
        self.font = pygame.font.Font(settings.FONT_PATH, settings.DEFAULT_FONT_SIZE)
        self.small_font = pygame.font.Font(settings.FONT_PATH, 20)
        
        try:
            self.background = pygame.image.load('assets/images/world_map.png').convert()
            self.background = pygame.transform.scale(self.background, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        except pygame.error:
            self.background = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            self.background.fill(settings.GREEN)

        self.locations = {
            "Travessia dos Ventos": {'pos': (300, 300), 'scene': 'BoatScene'},
            "Jardim Sussurrante": {'pos': (800, 450), 'scene': None}, # Em Breve
        }

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica cliques nos locais do mapa
                for name, data in self.locations.items():
                    rect = pygame.Rect(data['pos'][0] - 100, data['pos'][1] - 30, 200, 60)
                    if rect.collidepoint(event.pos) and data['scene']:
                        self.scene_manager.go_to_scene(data['scene'])
                
                # Verifica clique no botão de teste
                test_button_rect = pygame.Rect(20, settings.SCREEN_HEIGHT - 80, 200, 50)
                if test_button_rect.collidepoint(event.pos):
                    self.scene_manager.go_to_scene('TestScene')

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        title_surf = self.font.render(f"Bem-vindo, Guardião {self.profile.name}!", True, settings.BLACK)
        screen.blit(title_surf, (20, 20))
        
        # Desenha os locais do mapa
        for name, data in self.locations.items():
            rect = pygame.Rect(data['pos'][0] - 150, data['pos'][1] - 30, 300, 60)
            color = settings.ORANGE if data['scene'] else settings.GREY
            pygame.draw.rect(screen, color, rect, border_radius=15)
            
            text = name if data['scene'] else f"{name} (Em Breve)"
            text_surf = self.font.render(text, True, settings.WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
        
        # Botão de teste
        test_button_rect = pygame.Rect(20, settings.SCREEN_HEIGHT - 80, 200, 50)
        pygame.draw.rect(screen, settings.BLUE, test_button_rect, border_radius=10)
        pygame.draw.rect(screen, settings.WHITE, test_button_rect, 3, border_radius=10)
        
        test_text = self.small_font.render("🧪 TESTE MIC/CÂMERA", True, settings.WHITE)
        test_text_rect = test_text.get_rect(center=test_button_rect.center)
        screen.blit(test_text, test_text_rect)