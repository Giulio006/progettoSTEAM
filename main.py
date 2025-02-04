#!/usr/bin/env python3

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from src.core.Game import Game
from src.utils.config import load_config

def main():
    """
    Punto di ingresso principale del gioco
    """
    try:
        print("Caricamento configurazioni...")
        config = load_config()
        print("Configurazioni caricate con successo")
        
        print("Inizializzazione gioco...")
        game = Game()
        print("Avvio del gioco...")
        game.run()
    
    except Exception as e:
        print(f"Errore durante l'esecuzione del gioco: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()