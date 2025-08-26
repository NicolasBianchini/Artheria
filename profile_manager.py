# profile_manager.py
import json
import os

class Profile:
    def __init__(self, name):
        self.name = name
        self.is_calibrated = False
        self.calibration_data = {
            'max_breath_rms': 1.0,
        }
        self.progress = {
            'worlds_unlocked': ['boat_scene'],
            'achievements': []
        }

    def save(self):
        profile_path = f"profile_{self.name}.json"
        with open(profile_path, "w") as f:
            json.dump(self.__dict__, f, indent=4)
        print(f"Perfil '{self.name}' salvo.")

    @staticmethod
    def load(name):
        profile_path = f"profile_{name}.json"
        if not os.path.exists(profile_path):
            return None
        try:
            with open(profile_path, "r") as f:
                data = json.load(f)
                profile = Profile(name)
                profile.__dict__.update(data)
                print(f"Perfil '{name}' carregado.")
                return profile
        except (json.JSONDecodeError, KeyError):
            print(f"Erro ao carregar o perfil '{name}'. Arquivo corrompido.")
            return None

class ProfileManager:
    def __init__(self):
        self.current_profile = None

    def create_profile(self, name):
        if not name.isalnum(): # Nomes simples para evitar problemas com nome de arquivo
            print("Nome de perfil inválido. Use apenas letras e números.")
            return False
        self.current_profile = Profile(name)
        self.current_profile.save()
        return True

    def load_profile(self, name):
        profile = Profile.load(name)
        if profile:
            self.current_profile = profile
            return True
        return False

    def get_current_profile(self):
        return self.current_profile