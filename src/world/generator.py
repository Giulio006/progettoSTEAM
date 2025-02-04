import numpy as np
import random
from typing import List, Tuple, Dict

class DungeonRoom:
    def __init__(self, x: int, y: int, width: int, height: int, room_id: int):
        """
        Rappresenta una singola stanza nel dungeon
        
        Args:
            x (int): Coordinata x dell'angolo superiore sinistro
            y (int): Coordinata y dell'angolo superiore sinistro
            width (int): Larghezza della stanza
            height (int): Altezza della stanza
            room_id (int): Identificatore unico della stanza
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room_id = room_id
        
    def intersects(self, other_room: 'DungeonRoom') -> bool:
        """
        Controlla se la stanza si interseca con un'altra stanza
        
        Args:
            other_room (DungeonRoom): Altra stanza da confrontare
        
        Returns:
            bool: True se le stanze si intersecano, False altrimenti
        """
        return (self.x < other_room.x + other_room.width and
                self.x + self.width > other_room.x and
                self.y < other_room.y + other_room.height and
                self.y + self.height > other_room.y)
    
    def center(self) -> Tuple[int, int]:
        """
        Calcola il centro della stanza
        
        Returns:
            Tuple[int, int]: Coordinate del centro della stanza
        """
        return (self.x + self.width // 2, self.y + self.height // 2)


class AdvancedDungeonGenerator:
    def __init__(self, 
                 width: int = 100, 
                 height: int = 100, 
                 max_rooms: int = 50, 
                 min_room_size: int = 5, 
                 max_room_size: int = 15,
                 room_separation: int = 2):
        """
        Generatore di dungeon avanzato con algoritmo di generazione procedurale
        
        Args:
            width (int): Larghezza totale della mappa
            height (int): Altezza totale della mappa
            max_rooms (int): Numero massimo di stanze
            min_room_size (int): Dimensione minima delle stanze
            max_room_size (int): Dimensione massima delle stanze
            room_separation (int): Spazio minimo tra le stanze
        """
        self.width = width
        self.height = height
        self.max_rooms = max_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.room_separation = room_separation
        
        # Mappa del dungeon (0: vuoto, 1: stanza, 2: corridoio)
        self.dungeon_map = np.zeros((height, width), dtype=int)
        self.rooms: List[DungeonRoom] = []
    
    def _create_room(self, room: DungeonRoom):
        """
        Disegna una stanza sulla mappa
        
        Args:
            room (DungeonRoom): Stanza da disegnare
        """
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                self.dungeon_map[y, x] = 1
    
    def _create_corridor(self, start: Tuple[int, int], end: Tuple[int, int]):
        """
        Crea un corridoio tra due punti utilizzando un percorso L-shape
        
        Args:
            start (Tuple[int, int]): Punto di partenza
            end (Tuple[int, int]): Punto di arrivo
        """
        x1, y1 = start
        x2, y2 = end
        
        # Muoversi prima orizzontalmente, poi verticalmente (L-shape)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.dungeon_map[y1, x] = 2
        
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.dungeon_map[y, x2] = 2
    
    def generate(self) -> np.ndarray:
        """
        Genera il dungeon procedurale
        
        Returns:
            np.ndarray: Mappa del dungeon generata
        """
        attempts = 0
        max_attempts = self.max_rooms * 10
        
        while len(self.rooms) < self.max_rooms and attempts < max_attempts:
            # Genera dimensioni casuali
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            
            # Posizione casuale
            x = random.randint(self.room_separation, 
                                self.width - w - self.room_separation)
            y = random.randint(self.room_separation, 
                                self.height - h - self.room_separation)
            
            # Crea nuova stanza
            new_room = DungeonRoom(x, y, w, h, len(self.rooms))
            
            # Controlla intersezioni
            if not any(new_room.intersects(existing_room) for existing_room in self.rooms):
                # Crea stanza
                self._create_room(new_room)
                
                # Connetti alla stanza precedente se non è la prima
                if self.rooms:
                    prev_room = self.rooms[-1]
                    self._create_corridor(prev_room.center(), new_room.center())
                
                self.rooms.append(new_room)
            
            attempts += 1
        
        return self.dungeon_map
    
    def get_room_info(self) -> List[Dict]:
        """
        Fornisce informazioni dettagliate sulle stanze generate
        
        Returns:
            List[Dict]: Lista di dizionari con info delle stanze
        """
        return [
            {
                "id": room.room_id,
                "x": room.x,
                "y": room.y,
                "width": room.width,
                "height": room.height,
                "center": room.center()
            } for room in self.rooms
        ]