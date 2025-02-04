import pygame
import numpy as np

class Player:
    def __init__(self, x: int, y: int, tile_size: int):
        """
        Inizializza il giocatore
        
        Args:
            x (int): Posizione iniziale x
            y (int): Posizione iniziale y
            tile_size (int): Dimensione del tile
        """
        self.x = x
        self.y = y
        self.tile_size = tile_size
        
        # Statistiche del giocatore
        self.health = 100
        self.max_health = 100
        self.strength = 10
        
        # Colore del giocatore
        self.color = (0, 255, 0)  # Verde
    
    def move(self, dx: int, dy: int, dungeon_map: np.ndarray):
        """
        Muove il giocatore se la nuova posizione è valida
        
        Args:
            dx (int): Movimento sull'asse x
            dy (int): Movimento sull'asse y
            dungeon_map (np.ndarray): Mappa del dungeon
        """
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Controlla validità movimento
        if (0 <= new_x < dungeon_map.shape[1] and 
            0 <= new_y < dungeon_map.shape[0] and 
            dungeon_map[new_y, new_x] in [1, 2]):  # Stanze e corridoi
            self.x = new_x
            self.y = new_y
    
    def draw(self, screen: pygame.Surface):
        """
        Disegna il giocatore sullo schermo
        
        Args:
            screen (pygame.Surface): Superficie su cui disegnare
        """
        player_rect = pygame.Rect(
            self.x * self.tile_size, 
            self.y * self.tile_size, 
            self.tile_size - 1, 
            self.tile_size - 1
        )
        pygame.draw.rect(screen, self.color, player_rect)