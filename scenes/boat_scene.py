# scenes/boat_scene.py
import pygame
from scenes.base_scene import BaseScene
import settings
import math
import random

class BoatScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.input_manager = self.scene_manager.input_manager
        self.profile = self.scene_manager.profile_manager.get_current_profile()
        
        if not self.profile or not self.profile.is_calibrated:
            self.scene_manager.go_to_scene('LoginScene')
            return

        self.max_calibrated_breath = self.profile.calibration_data.get('max_breath_rms', 1.0)
        
        # Posição do barco
        self.boat_pos_x = 100
        self.boat_pos_y = settings.SCREEN_HEIGHT - 150  # Posição Y inicial
        self.finish_line_x = settings.SCREEN_WIDTH + 300  # Mapa maior - linha mais distante
        
        # Limites do barco (definir ANTES de gerar o caminho)
        self.min_y = 50  # Altura mínima (topo da tela)
        self.max_y = settings.SCREEN_HEIGHT - 150  # Altura máxima (chão)
        
        # Caminho pré-definido (como na primeira versão)
        self.path_points = self._generate_path()
        self.current_path_index = 0
        
        # Física do barco
        self.boat_velocity_y = 0.0  # Velocidade vertical
        self.gravity = 0.8  # Força da gravidade
        self.lift_force = 0.0  # Força de elevação do sopro
        self.normalized_effort = 0.0
        
        # Sistema de moedas
        self.coins = []
        self.coins_collected = 0
        self.total_coins = 0
        self._generate_coins()
        
        # Sistema de fases
        self.current_phase = 1
        self.phases_completed = 0
        self.phase_requirements = {
            1: {"coins": 4, "distance": 0.25},  # Ajustado para mapa maior
            2: {"coins": 7, "distance": 0.55},  # Ajustado para mapa maior
            3: {"coins": 10, "distance": 1.0}   # Ajustado para mapa maior
        }
        
        # Carregar imagem do barco
        try:
            self.boat_image = pygame.image.load('assets/images/boat.png').convert_alpha()
            self.boat_image = pygame.transform.scale(self.boat_image, (100, 80))
        except pygame.error:
            self.boat_image = pygame.Surface((100, 80))
            self.boat_image.fill(settings.WHITE)
    
    def _generate_path(self):
        """Gera pontos do caminho que o barco deve seguir"""
        path = []
        start_x = 100
        end_x = self.finish_line_x
        
        # Gera pontos ao longo do caminho com variações de altura
        for x in range(start_x, end_x, 50):
            # Altura base (meio da tela)
            base_y = settings.SCREEN_HEIGHT - 200
            
            # Adiciona variações suaves no caminho
            variation = math.sin((x - start_x) * 0.01) * 100  # Variação senoidal
            y = base_y + variation
            
            # Garante que não saia dos limites
            y = max(self.min_y + 50, min(self.max_y - 50, y))
            
            path.append((x, y))
        
        return path
    
    def _generate_coins(self):
        """Gera moedas ao longo do caminho"""
        self.coins = []
        start_x = 150
        end_x = self.finish_line_x - 50
        
        # Gera moedas em posições estratégicas (mais moedas para mapa maior)
        for x in range(start_x, end_x, 60):  # Distância menor entre moedas
            # Altura baseada no caminho
            base_y = settings.SCREEN_HEIGHT - 200
            variation = math.sin((x - start_x) * 0.01) * 80
            y = base_y + variation + random.randint(-40, 40)  # Variação maior
            
            # Garante que a moeda esteja em uma posição válida
            y = max(self.min_y + 20, min(self.max_y - 20, y))
            
            self.coins.append({
                'x': x,
                'y': y,
                'collected': False,
                'radius': 15
            })
        
        self.total_coins = len(self.coins)
    
    def _get_target_y(self):
        """Retorna a altura alvo baseada na posição X atual"""
        if self.current_path_index >= len(self.path_points):
            return self.path_points[-1][1]
        
        # Encontra o ponto do caminho mais próximo da posição X atual
        for i, (x, y) in enumerate(self.path_points):
            if x >= self.boat_pos_x:
                self.current_path_index = i
                return y
        
        return self.path_points[-1][1]
    
    def _check_coin_collision(self):
        """Verifica colisão com moedas"""
        boat_rect = pygame.Rect(self.boat_pos_x, self.boat_pos_y, 100, 80)
        
        for coin in self.coins:
            if not coin['collected']:
                coin_rect = pygame.Rect(coin['x'] - coin['radius'], coin['y'] - coin['radius'], 
                                      coin['radius'] * 2, coin['radius'] * 2)
                
                if boat_rect.colliderect(coin_rect):
                    coin['collected'] = True
                    self.coins_collected += 1
                    print(f"Moeda coletada! Total: {self.coins_collected}/{self.total_coins}")
    
    def _check_phase_completion(self):
        """Verifica se completou a fase atual"""
        current_phase = self.phase_requirements.get(self.current_phase)
        if current_phase:
            progress = self.boat_pos_x / self.finish_line_x
            
            if (self.coins_collected >= current_phase["coins"] and 
                progress >= current_phase["distance"]):
                
                self.phases_completed += 1
                if self.current_phase < 3:
                    self.current_phase += 1
                    print(f"Fase {self.current_phase} desbloqueada!")
                else:
                    print("Todas as fases completadas!")
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.scene_manager.go_to_scene('WorldMapScene')

    def update(self):
        # Obtém a intensidade do sopro
        breath = self.input_manager.get_breath_intensity()
        
        # Normaliza o esforço baseado na calibração
        if self.max_calibrated_breath > 0.1:
            self.normalized_effort = breath / self.max_calibrated_breath
        else:
            self.normalized_effort = 0.0
        
        # Obtém a altura alvo do caminho
        target_y = self._get_target_y()
        
        # Calcula a força de elevação baseada no sopro
        if self.normalized_effort > 0.15:  # Limiar aumentado para menos sensibilidade
            # A força de elevação é proporcional ao sopro (reduzida)
            self.lift_force = self.normalized_effort * 10.0  # Reduzido de 15.0 para 10.0
        else:
            # Sem sopro, a força de elevação diminui gradualmente
            self.lift_force = max(0, self.lift_force - 1.5)  # Reduzido de 2.0 para 1.5
        
        # Aplica a física do barco
        self._update_boat_physics(target_y)
        
        # Verifica colisões com moedas
        self._check_coin_collision()
        
        # Verifica conclusão de fases
        self._check_phase_completion()
        
        # Verifica se chegou à linha de chegada
        if self.boat_pos_x > self.finish_line_x:
            print(f"Vitória! Fases completadas: {self.phases_completed}")
            self.scene_manager.go_to_scene('WorldMapScene')

    def _update_boat_physics(self, target_y):
        """Atualiza a física do barco (posição, velocidade, etc.)"""
        # Calcula a diferença entre a posição atual e a alvo
        y_diff = target_y - self.boat_pos_y
        
        # Aplica a força de elevação (para cima) baseada no sopro
        self.boat_velocity_y -= self.lift_force
        
        # Aplica a gravidade (para baixo)
        self.boat_velocity_y += self.gravity
        
        # Adiciona força para seguir o caminho (quando não está assoprando)
        if self.normalized_effort < 0.1:
            # Força suave para seguir o caminho
            path_force = y_diff * 0.02
            self.boat_velocity_y += path_force
        
        # Aplica resistência do ar (amortecimento)
        self.boat_velocity_y *= 0.95
        
        # Atualiza a posição Y do barco
        self.boat_pos_y += self.boat_velocity_y
        
        # Limita a posição Y do barco
        if self.boat_pos_y < self.min_y:
            self.boat_pos_y = self.min_y
            self.boat_velocity_y = 0  # Para o movimento para cima
        elif self.boat_pos_y > self.max_y:
            self.boat_pos_y = self.max_y
            self.boat_velocity_y = 0  # Para o movimento para baixo
        
        # Movimento horizontal suave baseado no sopro
        if self.normalized_effort > 0.25:  # Limiar aumentado para menos sensibilidade
            # Acelera para a direita quando assopra (mais suave)
            self.boat_pos_x += 2.5  # Reduzido de 3.0 para 2.5
        else:
            # Movimento mais lento quando não assopra
            self.boat_pos_x += 0.8  # Reduzido de 1.0 para 0.8

    def draw(self, screen):
        # Fundo azul (céu)
        screen.fill(settings.BLUE)
        
        # Desenha o chão (água)
        water_rect = pygame.Rect(0, settings.SCREEN_HEIGHT - 100, settings.SCREEN_WIDTH, 100)
        pygame.draw.rect(screen, (0, 100, 200), water_rect)
        
        # Desenha a linha de chegada
        pygame.draw.line(screen, settings.WHITE, (self.finish_line_x, 0), (self.finish_line_x, settings.SCREEN_HEIGHT), 5)
        
        # Desenha as moedas
        for coin in self.coins:
            if not coin['collected']:
                pygame.draw.circle(screen, (255, 215, 0), (coin['x'], coin['y']), coin['radius'])
                pygame.draw.circle(screen, (255, 165, 0), (coin['x'], coin['y']), coin['radius'], 3)
        
        # Desenha o barco na posição calculada
        screen.blit(self.boat_image, (self.boat_pos_x, self.boat_pos_y))
        
        # UI - Linha de controle de respiração
        self._draw_breath_control(screen)
        
        # UI - Informações do jogo
        self._draw_game_info(screen)
    
    def _draw_breath_control(self, screen):
        """Desenha a linha de controle de respiração"""
        # Barra de fundo
        bar_width = 300
        bar_height = 20
        bar_x = 20
        bar_y = 20
        
        # Fundo da barra
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=10)
        
        # Preenche a barra baseado no esforço
        if self.normalized_effort > 0:
            fill_width = min(self.normalized_effort * bar_width, bar_width)
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            
            # Cor baseada na intensidade
            if self.normalized_effort > 0.7:
                color = (255, 100, 100)  # Vermelho para sopro forte
            elif self.normalized_effort > 0.4:
                color = (255, 200, 100)  # Laranja para sopro médio
            else:
                color = (100, 255, 100)  # Verde para sopro suave
            
            pygame.draw.rect(screen, color, fill_rect, border_radius=10)
        
        # Texto da barra
        font = pygame.font.Font(settings.FONT_PATH, 16)
        breath_text = f"Respiração: {int(self.normalized_effort * 100)}%"
        text_surf = font.render(breath_text, True, (255, 255, 255))
        screen.blit(text_surf, (bar_x, bar_y + bar_height + 5))
    
    def _draw_game_info(self, screen):
        """Desenha informações do jogo"""
        font = pygame.font.Font(settings.FONT_PATH, 18)
        
        # Moedas coletadas
        coins_text = f"Moedas: {self.coins_collected}/{self.total_coins}"
        coins_surf = font.render(coins_text, True, (255, 215, 0))
        screen.blit(coins_surf, (20, 80))
        
        # Fase atual
        phase_text = f"Fase: {self.current_phase}/3"
        phase_surf = font.render(phase_text, True, (255, 255, 255))
        screen.blit(phase_surf, (20, 110))
        
        # Progresso da distância
        progress = self.boat_pos_x / self.finish_line_x
        progress_text = f"Progresso: {int(progress * 100)}%"
        progress_surf = font.render(progress_text, True, (255, 255, 255))
        screen.blit(progress_surf, (20, 140))
        
        # Requisitos da fase atual
        current_phase = self.phase_requirements.get(self.current_phase)
        if current_phase:
            req_text = f"Objetivo: {current_phase['coins']} moedas + {int(current_phase['distance'] * 100)}% distância"
            req_surf = font.render(req_text, True, (100, 255, 100))
            screen.blit(req_surf, (20, 170))