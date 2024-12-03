# 🎮 GQRX Joystick Control

Script Python pour contrôler GQRX via un joystick.

## 📋 Prérequis
- Python 3.x
- pygame
- GQRX en cours d'exécution
- Joystick USB

## 🚀 Installation
```bash
git clone https://github.com/f4hxn/gqrx-joystick
cd gqrx-joystick
pip install pygame
./gqrx-joystick.py
```

## ⚙️ Configuration
```python
host = "127.0.0.1"  # IP GQRX
port = 7356         # Port GQRX
```

## 🕹️ Contrôles
- **Axe X**: Ajustement fréquence
- **Axe Y**: Contrôle volume
- **Boutons**: (Exemples de préréglages de fréquences)
  - 1: FM (87.5 MHz)
  - 2: Bande 2m (144.8 MHz)
  - 3: Bande 70cm (433.5 MHz)
  - 4: Marine VHF (156.8 MHz)

## 🛠️ Fonctionnalités
- Contrôle en temps réel
- Préréglages fréquences
- Ajustement volume progressif
- Interface Telnet GQRX

## 📜 License
MIT

## 📞 Support
- Questions: [Issues](https://github.com/F4HXN/issues)
- Contact: f4hxn@free.fr
