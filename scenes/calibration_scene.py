# scenes/calibration_scene.py
import pygame
from scenes.base_scene import BaseScene
import settings
import time

class CalibrationScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.profile = self.scene_manager.profile_manager.get_current_profile()
        self.input_manager = self.scene_manager.input_manager
        self.font = pygame.font.Font(settings.FONT_PATH, settings.DEFAULT_FONT_SIZE)
        
        self.state = "INSTRUCTIONS" # INSTRUCTIONS, LISTENING, DONE
        self.instruction_text = "Vamos calibrar seu Sopro Mágico!"
        self.countdown = 3
        self.listen_duration = 4 # segundos
        self.start_time = 0
        self.max_rms_detected = 0.0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.state == "INSTRUCTIONS" and event.key == pygame.K_SPACE:
                    self.state = "LISTENING"
                    self.instruction_text = f"Sopre o mais forte que puder por {self.listen_duration} segundos!"
                    self.start_time = time.time()
                elif self.state == "DONE" and event.key == pygame.K_RETURN:
                    self.save_calibration()
                    self.scene_manager.go_to_scene('WorldMapScene')

    def update(self):
        if self.state == "LISTENING":
            elapsed_time = time.time() - self.start_time
            if elapsed_time <= self.listen_duration:
                current_breath = self.input_manager.get_breath_intensity()
                if current_breath > self.max_rms_detected:
                    self.max_rms_detected = current_breath
                self.instruction_text = f"Continue... {int(self.listen_duration - elapsed_time) + 1}"
            else:
                self.state = "DONE"
                self.instruction_text = "Calibração concluída! Pressione Enter para continuar."

    def save_calibration(self):
        self.profile.calibration_data['max_breath_rms'] = self.max_rms_detected if self.max_rms_detected > 0.1 else 1.0
        self.profile.is_calibrated = True
        self.profile.save()

    def draw(self, screen):
        screen.fill(settings.BLUE)
        msg_surf = self.font.render(self.instruction_text, True, settings.WHITE)
        msg_rect = msg_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2))
        screen.blit(msg_surf, msg_rect)

        if self.state == "INSTRUCTIONS":
            start_surf = self.font.render("Pressione ESPAÇO para começar", True, settings.WHITE)
            start_rect = start_surf.get_rect(center=(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2 + 100))
            screen.blit(start_surf, start_rect)