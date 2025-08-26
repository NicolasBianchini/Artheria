# input_manager.py
import cv2
import sounddevice as sd
import numpy as np
import threading

class InputManager:
    def __init__(self, mic_id=None, mic_samplerate=44100, cam_id=0):
        # Microfone
        self.mic_id = mic_id
        self.mic_samplerate = mic_samplerate
        self.breath_intensity = 0.0
        self.breath_multiplier = 50.0  # Multiplicador reduzido para menos sensibilidade
        self._mic_thread = threading.Thread(target=self._listen_mic, daemon=True)
        self.mic_running = False
        
        # Filtro de ruído para microfone
        self.noise_threshold = 0.05  # Threshold aumentado para filtrar mais ruído
        self.breath_history = []  # Histórico para filtro de média móvel
        self.history_size = 8  # Histórico maior para mais suavização
        
        # Câmera e detecção de movimento
        self.cam_id = cam_id
        self.camera = None
        self.motion_detected = False
        self.motion_intensity = 0.0
        self._camera_thread = threading.Thread(target=self._process_camera, daemon=True)
        self.camera_running = False
        
        # Para detecção de movimento
        self.prev_frame = None
        self.motion_threshold = 30

    def start(self):
        self.mic_running = True
        self.camera_running = True
        self._mic_thread.start()
        self._camera_thread.start()

    def stop(self):
        self.mic_running = False
        self.camera_running = False

    def set_breath_multiplier(self, multiplier):
        """Ajusta a sensibilidade do microfone (1.0 = normal, 2.0 = 2x mais sensível)"""
        self.breath_multiplier = multiplier
        print(f"Sensibilidade do microfone ajustada para: {multiplier}x")

    def set_motion_threshold(self, threshold):
        """Ajusta a sensibilidade da detecção de movimento"""
        self.motion_threshold = threshold
        print(f"Sensibilidade do movimento ajustada para: {threshold}")

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Erro no microfone: {status}")
        
        # Calcula a RMS (Root Mean Square) como uma boa métrica de intensidade
        rms = np.sqrt(np.mean(indata**2))
        
        # Aplica filtro de ruído mais rigoroso
        if rms > self.noise_threshold:
            # Adiciona ao histórico
            self.breath_history.append(rms)
            if len(self.breath_history) > self.history_size:
                self.breath_history.pop(0)
            
            # Calcula média móvel para suavizar o sinal
            filtered_rms = np.mean(self.breath_history)
            
            # Aplica um filtro adicional para reduzir picos
            if filtered_rms > 0.1:  # Só considera sopros mais fortes
                self.breath_intensity = float(filtered_rms)
            else:
                # Para sopros muito fracos, diminui gradualmente
                self.breath_intensity = max(0, self.breath_intensity * 0.8)
        else:
            # Se abaixo do threshold, diminui mais rapidamente
            self.breath_intensity = max(0, self.breath_intensity * 0.7)
            # Limpa o histórico quando não há sopro
            if self.breath_intensity < 0.001:
                self.breath_history.clear()

    def _listen_mic(self):
        try:
            with sd.InputStream(device=self.mic_id, channels=1, callback=self._audio_callback,
                                samplerate=self.mic_samplerate, blocksize=1024):
                while self.mic_running:
                    sd.sleep(100)
        except Exception as e:
            print(f"Não foi possível iniciar o microfone: {e}")
            self.breath_intensity = -1 # Sinaliza erro

    def _process_camera(self):
        """Processa a câmera para detecção de movimento"""
        try:
            self.camera = cv2.VideoCapture(self.cam_id)
            if not self.camera.isOpened():
                print(f"Não foi possível abrir a câmera {self.cam_id}")
                return
                
            while self.camera_running:
                ret, frame = self.camera.read()
                if not ret:
                    continue
                    
                # Processa frame para detecção de movimento
                self._detect_motion(frame)
                
                # Pequena pausa para não sobrecarregar
                cv2.waitKey(1)
                
        except Exception as e:
            print(f"Erro na câmera: {e}")
        finally:
            if self.camera:
                self.camera.release()

    def _detect_motion(self, frame):
        """Detecta movimento usando diferença entre frames"""
        # Converte para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if self.prev_frame is None:
            self.prev_frame = gray
            return
        
        # Calcula diferença entre frames
        frame_delta = cv2.absdiff(self.prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        # Dilata para preencher buracos
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Encontra contornos
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Calcula intensidade do movimento
        motion_area = 0
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Filtra ruído
                motion_area += cv2.contourArea(contour)
        
        # Normaliza a intensidade do movimento
        frame_area = frame.shape[0] * frame.shape[1]
        self.motion_intensity = min(100.0, (motion_area / frame_area) * 10000)
        
        # Define se há movimento detectado
        self.motion_detected = self.motion_intensity > self.motion_threshold
        
        # Atualiza frame anterior
        self.prev_frame = gray

    def get_breath_intensity(self):
        """Retorna a intensidade do sopro com multiplicador ajustável"""
        return self.breath_intensity * self.breath_multiplier

    def get_motion_detected(self):
        """Retorna se há movimento detectado"""
        return self.motion_detected

    def get_motion_intensity(self):
        """Retorna a intensidade do movimento (0-100)"""
        return self.motion_intensity

    def get_camera_frame(self):
        """Retorna o frame atual da câmera para exibição"""
        if self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return frame
        return None