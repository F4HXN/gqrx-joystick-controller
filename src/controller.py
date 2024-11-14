!/usr/bin/env python3
import pygame
import telnetlib
import time
import threading
import math

class GQRXJoystickControl:
    def __init__(self, host="127.0.0.1", port=7356):
        # Initialisation de pygame pour le joystick
        pygame.init()
        pygame.joystick.init()
        
        # Configuration par défaut
        self.host = host
        self.port = port
        self.connected = False
        self.running = True
        self.frequency = 100000000  # Fréquence de départ (100 MHz)
        self.freq_step = 100  # Pas de fréquence par défaut
        self.volume = 0  # Volume initial
        
        # Essayer de se connecter à GQRX
        self.connect_to_gqrx()
        
        # Initialiser le joystick s'il est disponible
        self.init_joystick()
        
        # Thread pour la mise à jour continue
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def connect_to_gqrx(self):
        """Établir la connexion avec GQRX"""
        try:
            self.tn = telnetlib.Telnet(self.host, self.port)
            self.connected = True
            print("Connecté à GQRX")
            
            # Configuration initiale
            self.send_command("f")  # Obtenir la fréquence actuelle
            self.send_command("l NONE")  # Désactiver le verrouillage
            
        except Exception as e:
            print(f"Erreur de connexion à GQRX: {e}")
            self.connected = False

    def init_joystick(self):
        """Initialiser le premier joystick trouvé"""
        try:
            if pygame.joystick.get_count() > 0:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                print(f"Joystick initialisé: {self.joystick.get_name()}")
            else:
                print("Aucun joystick trouvé")
                self.joystick = None
        except Exception as e:
            print(f"Erreur d'initialisation du joystick: {e}")
            self.joystick = None

    def send_command(self, cmd):
        """Envoyer une commande à GQRX"""
        if self.connected:
            try:
                self.tn.write(f"{cmd}\n".encode('ascii'))
                response = self.tn.read_until(b"\n").decode('ascii').strip()
                return response
            except:
                self.connected = False
                print("Connexion perdue avec GQRX")
        return None

    def adjust_frequency(self, delta):
        """Ajuster la fréquence"""
        self.frequency += delta
        if self.connected:
            self.send_command(f"F {self.frequency}")
            print(f"Fréquence: {self.frequency/1000000:.3f} MHz")

    def adjust_volume(self, value):
        """Ajuster le volume"""
        self.volume = max(0, min(100, value))
        if self.connected:
            self.send_command(f"L SQL {self.volume}")
            print(f"Volume: {self.volume}")

    def process_joystick_input(self):
        """Traiter les entrées du joystick"""
        if not self.joystick:
            return

        # Mise à jour des événements pygame
        pygame.event.pump()

        # Axe X pour la fréquence (axe 0)
        freq_change = self.joystick.get_axis(0)
        if abs(freq_change) > 0.1:  # Zone morte
            # Ajustement exponentiel pour un contrôle plus précis
            direction = 1 if freq_change > 0 else -1
            magnitude = math.pow(abs(freq_change), 2) * 10000
            self.adjust_frequency(int(direction * magnitude))

        # Axe Y pour le volume (axe 1)
        volume_change = -self.joystick.get_axis(1)  # Inversé pour que haut = plus fort
        if abs(volume_change) > 0.1:  # Zone morte
            new_volume = int(self.volume + volume_change * 2)
            self.adjust_volume(new_volume)

        # Boutons pour les préréglages
        for i in range(self.joystick.get_numbuttons()):
            if self.joystick.get_button(i):
                # Exemple de préréglages de fréquences
                presets = {
                    0: 87500000,  # FM Radio
                    1: 144800000,  # 2m Amateur
                    2: 433500000,  # 70cm Amateur
                    3: 156800000,  # Marine VHF
                }
                if i in presets:
                    self.frequency = presets[i]
                    self.send_command(f"F {self.frequency}")
                    print(f"Préréglage {i+1}: {self.frequency/1000000:.3f} MHz")

    def update_loop(self):
        """Boucle principale de mise à jour"""
        while self.running:
            if self.connected and self.joystick:
                self.process_joystick_input()
            time.sleep(0.05)  # 20 Hz update rate

    def cleanup(self):
        """Nettoyer les ressources"""
        self.running = False
        if self.connected:
            self.tn.close()
        pygame.quit()

if __name__ == "__main__":
    try:
        controller = GQRXJoystickControl()
        print("Appuyez sur Ctrl+C pour quitter")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nArrêt du programme...")
        controller.cleanup()
