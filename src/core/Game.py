import pygame
import sys
import numpy as np
import random

# Import locali
from src.world.generator import AdvancedDungeonGenerator
from src.core.player import Player
from src.utils.config import load_config

class Game:
    def __init__(self):
        # Print di debug
        print("Inizializzazione Game...")
        
        # Carica configurazioni
        self.config = load_config()
        
        # Inizializzazione Pygame
        pygame.init()
        
        # Configurazioni schermo
        self.screen_width = self.config['game']['screen_width']
        self.screen_height = self.config['game']['screen_height']
        self.tile_size = self.config['game']['tile_size']
        
        # Setup schermo
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Roguelike AI Adventure')
        
        # Generazione dungeon
        print("Generazione dungeon in corso...")
        self.dungeon_generator = AdvancedDungeonGenerator(
            width=self.screen_width // self.tile_size,
            height=self.screen_height // self.tile_size,
            max_rooms=self.config['world']['room_count'],
            min_room_size=self.config['world']['min_room_size'],
            max_room_size=self.config['world']['max_room_size']
        )
        
        # Genera mappa
        self.dungeon_map = self.dungeon_generator.generate()
        print("Dungeon generato con successo")
        
        # Trova posizione iniziale del giocatore
        start_positions = np.argwhere(self.dungeon_map == 1)
        start_pos = start_positions[random.randint(0, len(start_positions) - 1)]
        
        # Inizializza giocatore
        self.player = Player(start_pos[1], start_pos[0], self.tile_size)
        
        # Clock per controllare framerate
        self.clock = pygame.time.Clock()
        
        print("Inizializzazione Game completata")

    def draw(self):
        self.screen.fill((0, 0, 0))  # Sfondo nero
        
        # Disegna dungeon
        for y in range(self.dungeon_map.shape[0]):
            for x in range(self.dungeon_map.shape[1]):
                rect = pygame.Rect(
                    x * self.tile_size, 
                    y * self.tile_size, 
                    self.tile_size - 1, 
                    self.tile_size - 1
                )
                
                if self.dungeon_map[y, x] == 1:  # Stanza
                    pygame.draw.rect(self.screen, (128, 128, 128), rect)
                elif self.dungeon_map[y, x] == 2:  # Corridoio
                    pygame.draw.rect(self.screen, (64, 64, 64), rect)
        
        # Disegna giocatore
        self.player.draw(self.screen)
        
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                
                if keys[pygame.K_LEFT]:
                    self.player.move(-1, 0, self.dungeon_map)
                if keys[pygame.K_RIGHT]:
                    self.player.move(1, 0, self.dungeon_map)
                if keys[pygame.K_UP]:
                    self.player.move(0, -1, self.dungeon_map)
                if keys[pygame.K_DOWN]:
                    self.player.move(0, 1, self.dungeon_map)
        
        return True

    def run(self):
        print("Avvio del loop di gioco...")
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()