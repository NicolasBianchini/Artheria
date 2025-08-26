# 🚤 Aetheria - Jogo de Controle por Sopro

**Aetheria** é um jogo 2D desenvolvido em Python com Pygame que utiliza o microfone do computador para controlar um barco através do sopro do jogador.

## 🎮 Sobre o Jogo

Aetheria é uma aventura mágica onde você controla um barco voador usando apenas sua respiração. O jogo combina elementos de plataforma com controle único por sopro, criando uma experiência imersiva e terapêutica.

## ✨ Funcionalidades

### 🎤 Controle por Sopro
- **Detecção de respiração** em tempo real
- **Filtro de ruído inteligente** para controle preciso
- **Sensibilidade ajustável** via teclas ↑/↓
- **Barra visual** de controle de respiração

### 📹 Detecção de Movimento
- **Câmera integrada** para detecção de gestos
- **Sensibilidade ajustável** via teclas ←/→
- **Processamento em tempo real** com OpenCV

### 🚤 Física do Barco
- **Movimento vertical** controlado pelo sopro
- **Gravidade realista** quando não está assoprando
- **Caminho pré-definido** com variações de altura
- **Controle suave** e responsivo

### 🪙 Sistema de Progressão
- **23 moedas** distribuídas pelo percurso
- **3 fases progressivas** com objetivos diferentes
- **Sistema de desbloqueio** automático
- **Métricas de progresso** em tempo real

## 🛠️ Tecnologias Utilizadas

- **Python 3.13+**
- **Pygame** - Engine de jogos
- **OpenCV** - Processamento de imagem
- **SoundDevice** - Captura de áudio
- **NumPy** - Processamento numérico

## 📋 Requisitos

### Sistema
- macOS, Windows ou Linux
- Python 3.13 ou superior
- Microfone funcional
- Webcam (opcional, para detecção de movimento)

### Dependências
```
pygame
opencv-python
numpy
sounddevice
```

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/NicolasBianchini/Artheria.git
cd Artheria
```

2. **Crie um ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute o jogo:**
```bash
python3 main.py
```

## 🎯 Como Jogar

### Controles Básicos
- **Sopro no microfone**: Controla a altura e movimento do barco
- **ESC**: Volta ao mapa do mundo
- **↑/↓**: Ajusta sensibilidade do microfone
- **←/→**: Ajusta sensibilidade da detecção de movimento

### Objetivos
1. **Colete moedas** durante o percurso
2. **Complete as fases** desbloqueando objetivos
3. **Chegue à linha de chegada** para completar o nível
4. **Use o sopro estrategicamente** para navegar pelo caminho

### Sistema de Fases
- **Fase 1**: 4 moedas + 25% da distância
- **Fase 2**: 7 moedas + 55% da distância
- **Fase 3**: 10 moedas + 100% da distância

## 🎨 Estrutura do Projeto

```
Aetheria/
├── main.py                 # Arquivo principal do jogo
├── input_manager.py        # Gerenciador de entrada (microfone + câmera)
├── scene_manager.py        # Gerenciador de cenas
├── profile_manager.py      # Gerenciador de perfis
├── settings.py            # Configurações do jogo
├── scenes/                # Cenas do jogo
│   ├── base_scene.py      # Cena base
│   ├── login_scene.py     # Tela de login
│   ├── calibration_scene.py # Calibração do microfone
│   ├── world_map_scene.py # Mapa do mundo
│   ├── boat_scene.py      # Cena principal do barco
│   └── test_scene.py      # Cena de teste
├── assets/                # Recursos do jogo
│   └── images/           # Imagens
├── requirements.txt       # Dependências Python
└── README.md             # Este arquivo
```

## 🔧 Configuração

### Microfone
- O jogo detecta automaticamente o microfone padrão
- Use a cena de calibração para ajustar a sensibilidade
- Ajuste o multiplicador via teclas ↑/↓ durante o jogo

### Câmera
- A câmera é opcional e pode ser desabilitada
- Use a tecla **C** para mostrar/ocultar a visualização
- Ajuste a sensibilidade via teclas ←/→

## 🎮 Cenas do Jogo

### 🏠 Login Scene
- Criação e carregamento de perfis
- Sistema de persistência de dados

### 🎯 Calibration Scene
- Calibração do microfone
- Ajuste da sensibilidade base

### 🗺️ World Map Scene
- Navegação entre diferentes minigames
- Acesso à cena de teste

### 🚤 Boat Scene
- Minigame principal do barco
- Sistema de moedas e fases
- Física realista de voo

### 🧪 Test Scene
- Teste do microfone e câmera
- Ajustes de sensibilidade em tempo real

## 🐛 Solução de Problemas

### Microfone não funciona
- Verifique as permissões do sistema
- Teste com outros aplicativos
- Ajuste a sensibilidade via teclas ↑/↓

### Câmera não funciona
- Verifique as permissões do sistema
- A câmera é opcional para o jogo funcionar

### Performance baixa
- Feche outros aplicativos
- Reduza a sensibilidade da detecção de movimento
- Use a cena de teste para otimizar configurações

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Nicolas Bianchini**
- GitHub: [@NicolasBianchini](https://github.com/NicolasBianchini)
- Projeto: [Artheria](https://github.com/NicolasBianchini/Artheria)

## 🙏 Agradecimentos

- Comunidade Pygame
- Biblioteca OpenCV
- Biblioteca SoundDevice
- Todos os contribuidores e testadores

---

**Divirta-se jogando Aetheria! 🚤✨**
