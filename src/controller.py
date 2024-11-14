#!/usr/bin/env python3
import pygame
import socket
import time
import threading
import math
import logging

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GQRXJoystickControl:
    def __init__(self, host="127.0.0.1", port=7356):
        pygame.init()
        pygame.joystick.init()
        
        self.host = host
        self.port = port
        self.connected = False
        self.running = True
        self.frequency = 100000000
        self.freq_step = 100
        self.volume = 0
        
        self.connect_to_gqrx()
        self.init_joystick()
        
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def connect_to_gqrx(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connected = True
            logger.info("Connecté à GQRX")
        except Exception as e:
            logger.error(f"Erreur de connexion à GQRX: {e}")
            self.connected = False

    def init_joystick(self):
        try:
            if pygame.joystick.get_count() > 0:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                logger.info(f"Joystick initialisé: {self.joystick.get_name()}")
            else:
                logger.warning("Aucun joystick trouvé")
                self.joystick = None
        except Exception as e:
            logger.error(f"Erreur d'initialisation du joystick: {e}")
            self.joystick = None

    def cleanup(self):
        self.running = False
        if self.connected:
            self.sock.close()
        pygame.quit()

if __name__ == "__main__":
    try:
        controller = GQRXJoystickControl()
        logger.info("Contrôleur démarré. Appuyez sur Ctrl+C pour quitter.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Arrêt du programme...")
        controller.cleanup()
