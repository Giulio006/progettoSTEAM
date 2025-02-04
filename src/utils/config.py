import yaml
import os

def load_config(config_path: str = None) -> dict:
    """
    Carica la configurazione dal file YAML
    
    Args:
        config_path (str, optional): Percorso personalizzato del file di configurazione
    
    Returns:
        dict: Configurazioni caricate
    """
    if not config_path:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.yaml')
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        return config
    except FileNotFoundError:
        # Configurazione di default se non trova il file
        return {
            'game': {
                'screen_width': 800,
                'screen_height': 600,
                'tile_size': 40
            },
            'world': {
                'room_count': 20,
                'min_room_size': 5,
                'max_room_size': 15
            },
            'ai': {
                'learning_rate': 0.001,
                'discount_factor': 0.99
            }
        }
