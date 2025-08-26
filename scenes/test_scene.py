# scenes/test_scene.py
import pygame
import cv2
import numpy as np
from scenes.base_scene import BaseScene
import settings

class TestScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.input_manager = self.scene_manager.input_manager
        self.font = pygame.font.Font(settings.FONT_PATH, 24)
        self.small_font = pygame.font.Font(settings.FONT_PATH, 18)
        
        # Controles de sensibilidade
        self.breath_multiplier = 100.0
        self.motion_threshold = 30
        self.show_camera = True
        
        # Cores para UI
        self.colors = {
            'background': (20, 20, 40),
            'panel': (40, 40, 60),
            'text': (255, 255, 255),
            'highlight': (100, 200, 255),
            'success': (100, 255, 100),
            'warning': (255, 200, 100)
        }

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene_manager.go_to_scene('WorldMapScene')
                elif event.key == pygame.K_c:
                    self.show_camera = not self.show_camera
                elif event.key == pygame.K_UP:
                    self.breath_multiplier = min(500.0, self.breath_multiplier + 10.0)
                    self.input_manager.set_breath_multiplier(self.breath_multiplier)
                elif event.key == pygame.K_DOWN:
                    self.breath_multiplier = max(10.0, self.breath_multiplier - 10.0)
                    self.input_manager.set_breath_multiplier(self.breath_multiplier)
                elif event.key == pygame.K_LEFT:
                    self.motion_threshold = max(5, self.motion_threshold - 5)
                    self.input_manager.set_motion_threshold(self.motion_threshold)
                elif event.key == pygame.K_RIGHT:
                    self.motion_threshold = min(100, self.motion_threshold + 5)
                    self.input_manager.set_motion_threshold(self.motion_threshold)

    def update(self):
        # Atualiza dados em tempo real
        pass

    def draw(self, screen):
        screen.fill(self.colors['background'])
        
        # Painel principal
        panel_rect = pygame.Rect(20, 20, 400, 350)
        pygame.draw.rect(screen, self.colors['panel'], panel_rect, border_radius=10)
        pygame.draw.rect(screen, self.colors['highlight'], panel_rect, 3, border_radius=10)
        
        # Título
        title = self.font.render("CENA DE TESTE - MICROFONE E CÂMARA", True, self.colors['text'])
        screen.blit(title, (30, 30))
        
        # Informações do microfone
        breath_intensity = self.input_manager.get_breath_intensity()
        breath_text = f"Intensidade do Sopro: {breath_intensity:.1f}"
        breath_surf = self.small_font.render(breath_text, True, self.colors['text'])
        screen.blit(breath_surf, (30, 80))
        
        # Barra de intensidade do sopro
        bar_rect = pygame.Rect(30, 110, 360, 30)
        pygame.draw.rect(screen, self.colors['text'], bar_rect, 2, border_radius=5)
        
        # Preenche a barra baseado na intensidade
        if breath_intensity > 0:
            fill_width = min(breath_intensity / 10.0, 1.0) * 360
            fill_rect = pygame.Rect(30, 110, fill_width, 30)
            color = self.colors['success'] if breath_intensity > 5 else self.colors['warning']
            pygame.draw.rect(screen, color, fill_rect, border_radius=5)
        
        # Controles de sensibilidade do microfone
        sensitivity_text = f"Sensibilidade MIC: {self.breath_multiplier:.1f}x"
        sensitivity_surf = self.small_font.render(sensitivity_text, True, self.colors['text'])
        screen.blit(sensitivity_surf, (30, 160))
        
        # Informações de movimento
        motion_detected = self.input_manager.get_motion_detected()
        motion_intensity = self.input_manager.get_motion_intensity()
        
        motion_text = f"Movimento: {'SIM' if motion_detected else 'NÃO'}"
        motion_color = self.colors['success'] if motion_detected else self.colors['warning']
        motion_surf = self.small_font.render(motion_text, True, motion_color)
        screen.blit(motion_surf, (30, 200))
        
        motion_int_text = f"Intensidade Movimento: {motion_intensity:.1f}"
        motion_int_surf = self.small_font.render(motion_int_text, True, self.colors['text'])
        screen.blit(motion_int_surf, (30, 230))
        
        # Barra de intensidade do movimento
        motion_bar_rect = pygame.Rect(30, 260, 360, 20)
        pygame.draw.rect(screen, self.colors['text'], motion_bar_rect, 2, border_radius=5)
        
        if motion_intensity > 0:
            motion_fill_width = min(motion_intensity / 100.0, 1.0) * 360
            motion_fill_rect = pygame.Rect(30, 260, motion_fill_width, 20)
            motion_bar_color = self.colors['success'] if motion_detected else self.colors['warning']
            pygame.draw.rect(screen, motion_bar_color, motion_fill_rect, border_radius=5)
        
        # Controles de sensibilidade do movimento
        motion_sensitivity_text = f"Sensibilidade Movimento: {self.motion_threshold}"
        motion_sensitivity_surf = self.small_font.render(motion_sensitivity_text, True, self.colors['text'])
        screen.blit(motion_sensitivity_surf, (30, 300))
        
        # Instruções
        instructions = [
            "Controles:",
            "↑/↓ - Ajustar sensibilidade MIC",
            "←/→ - Ajustar sensibilidade Movimento",
            "C - Mostrar/Ocultar câmera",
            "ESC - Voltar ao mapa"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surf = self.small_font.render(instruction, True, self.colors['highlight'])
            screen.blit(inst_surf, (30, 400 + i * 25))
        
        # Câmera (lado direito)
        if self.show_camera:
            camera_frame = self.input_manager.get_camera_frame()
            if camera_frame is not None:
                # Converte frame OpenCV para Pygame
                camera_surface = self._cv2_to_pygame(camera_frame)
                
                # Redimensiona para caber na tela
                camera_width = 400
                camera_height = 300
                camera_surface = pygame.transform.scale(camera_surface, (camera_width, camera_height))
                
                # Desenha a câmera no lado direito
                camera_rect = pygame.Rect(450, 20, camera_width, camera_height)
                screen.blit(camera_surface, camera_rect)
                
                # Borda da câmera
                pygame.draw.rect(screen, self.colors['highlight'], camera_rect, 3, border_radius=10)
                
                # Título da câmera
                camera_title = self.small_font.render("CÂMARA - DETECÇÃO DE MOVIMENTO", True, self.colors['text'])
                screen.blit(camera_title, (450, 340))
        
        # Status da câmera
        camera_status = "Câmera: ATIVA" if self.show_camera else "Câmera: DESATIVADA"
        status_color = self.colors['success'] if self.show_camera else self.colors['warning']
        status_surf = self.small_font.render(camera_status, True, status_color)
        screen.blit(status_surf, (450, 370))

    def _cv2_to_pygame(self, cv2_frame):
        """Converte um frame OpenCV para uma superfície Pygame"""
        # Converte BGR para RGB
        rgb_frame = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
        
        # Redimensiona para melhor performance
        rgb_frame = cv2.resize(rgb_frame, (400, 300))
        
        # Converte para Pygame
        pygame_surface = pygame.surfarray.make_surface(rgb_frame.swapaxes(0, 1))
        return pygame_surface
