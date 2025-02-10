import pygame
import numpy as np
from src.utils.config import load_config

class Player:
    def __init__(self, x: int, y: int, tile_size: int):
        """
        Inizializza il giocatore con posizione float per movimento continuo
        Args:
            x (int): Posizione iniziale x
            y (int): Posizione iniziale y
            tile_size (int): Dimensione del tile
        """
        self.config = load_config()
        # Posizione float per movimento continuo
        self.x = float(x * tile_size)
        self.y = float(y * tile_size)
        self.tile_size = tile_size
        
        # Velocità di movimento in pixel/frame
        self.speed = self.config['player']['speed']
        
        # Statistiche del giocatore
        self.health = 100
        self.max_health = 100
        self.strength = 10
        
        # Colore del giocatore
        self.color = (0, 255, 0)  # Verde
        
        # Flag per il movimento
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def handle_input(self, keys):
        """
        Gestisce l'input continuo da tastiera
        Args:
            keys: Lista dei tasti premuti
        """
        self.moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        self.moving_up = keys[pygame.K_UP] or keys[pygame.K_w]
        self.moving_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

    def update(self, dungeon_map: np.ndarray):
        """
        Aggiorna la posizione del giocatore in base al movimento
        Args:
            dungeon_map (np.ndarray): Mappa del dungeon
        """
        dx = 0.0
        dy = 0.0
        
        if self.moving_left:
            dx -= self.speed
        if self.moving_right:
            dx += self.speed
        if self.moving_up:
            dy -= self.speed
        if self.moving_down:
            dy += self.speed

        # Normalizza la velocità in diagonale
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/√2
            dy *= 0.707

        # Calcola la nuova posizione
        new_x = self.x + dx
        new_y = self.y + dy

        # Converti le coordinate in tile
        tile_x = int(new_x / self.tile_size)
        tile_y = int(new_y / self.tile_size)

        # Controlla collisioni
        if (0 <= tile_x < dungeon_map.shape[1] and
            0 <= tile_y < dungeon_map.shape[0] and
            dungeon_map[tile_y, tile_x] in [1, 2]):  # Stanze e corridoi
            self.x = new_x
            self.y = new_y

    def draw(self, screen: pygame.Surface):
        """
        Disegna il giocatore sullo schermo
        Args:
            screen (pygame.Surface): Superficie su cui disegnare
        """
        player_rect = pygame.Rect(
            int(self.x),
            int(self.y),
            self.tile_size - 1,
            self.tile_size - 1
        )
        pygame.draw.rect(screen, self.color, player_rect)