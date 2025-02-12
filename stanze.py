import numpy as np
import pygame as p
import codiceNuovo as c

# Inizializza Pygame
p.init()

# Parametri casuali per il labirinto
NUM_ROWS = np.random.randint(3, 7)  # Numero casuale di righe (tra 3 e 6)
NUM_COLS = np.random.randint(4, 8)  # Numero casuale di colonne (tra 4 e 7)

# Calcola il numero totale di stanze
NUM_ROOMS = NUM_ROWS * NUM_COLS

# Dimensioni della finestra
WIDTH = 1600  # Larghezza fissa della finestra
HEIGHT = 900  # Altezza fissa della finestra

# Calcola la dimensione delle stanze in base alla finestra e al numero di righe e colonne
ROOM_SIZE = min(WIDTH // NUM_COLS, HEIGHT // NUM_ROWS)

# Crea una finestra Pygame
win = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Labirinto")

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)  # Colore per le porte
BLUE = (0, 0, 255)  # Colore per il personaggio

# Genera il grafo delle stanze
rooms = c.generate_graph(NUM_ROWS, NUM_COLS)
print(rooms)

# Posizione iniziale casuale del personaggio
current_room = np.random.randint(0, NUM_ROOMS)
player_pos = [ROOM_SIZE // 2, ROOM_SIZE // 2]  # Posizione relativa alla stanza

# Funzione per disegnare le stanze e le porte
def draw_matrix():
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            # Calcola la posizione della cella
            x = c * ROOM_SIZE
            y = r * ROOM_SIZE
            
            # Disegna il rettangolo per la cella
            p.draw.rect(win, GREEN, (x, y, ROOM_SIZE, ROOM_SIZE), 1)
            
            # Crea il testo per la cella
            font = p.font.SysFont(None, 36)
            text = font.render(f"{r * NUM_COLS + c}", True, BLACK)
            win.blit(text, (x + 30, y + 30))  # Posiziona il testo al centro della cella
            
            # Disegna le porte come aperture
            if c < NUM_COLS - 1:  # Porta a destra
                # Rimuovi parte del muro disegnando un rettangolo bianco
                p.draw.rect(win, WHITE, (x + ROOM_SIZE, y + ROOM_SIZE // 4, 10, ROOM_SIZE // 2))  # Apertura a destra
                # Disegna la linea rossa per la porta
                p.draw.line(win, RED, (x + ROOM_SIZE, y + ROOM_SIZE // 4), (x + ROOM_SIZE, y + ROOM_SIZE * 3 // 4), 5)
            if r < NUM_ROWS - 1:  # Porta in basso
                # Rimuovi parte del muro disegnando un rettangolo bianco
                p.draw.rect(win, WHITE, (x + ROOM_SIZE // 4, y + ROOM_SIZE, ROOM_SIZE // 2, 10))  # Apertura in basso
                # Disegna la linea rossa per la porta
                p.draw.line(win, RED, (x + ROOM_SIZE // 4, y + ROOM_SIZE), (x + ROOM_SIZE * 3 // 4, y + ROOM_SIZE), 5)

# Funzione per disegnare il personaggio
def draw_player():
    # Calcola la posizione assoluta del personaggio
    room_row = current_room // NUM_COLS
    room_col = current_room % NUM_COLS
    x = room_col * ROOM_SIZE + player_pos[0]
    y = room_row * ROOM_SIZE + player_pos[1]
    
    # Disegna il personaggio
    p.draw.circle(win, BLUE, (x, y), 10)

# Funzione per gestire il movimento del personaggio
def move_player(direction):
    global current_room, player_pos
    
    # Movimento all'interno della stanza
    if direction == "UP":
        player_pos[1] = max(0, player_pos[1] - 5)
    elif direction == "DOWN":
        player_pos[1] = min(ROOM_SIZE, player_pos[1] + 5)
    elif direction == "LEFT":
        player_pos[0] = max(0, player_pos[0] - 5)
    elif direction == "RIGHT":
        player_pos[0] = min(ROOM_SIZE, player_pos[0] + 5)
    
    # Verifica se il personaggio sta cercando di passare attraverso una porta
    if player_pos[0] <= 0:  # Porta a sinistra
        if current_room % NUM_COLS != 0:  # Se non è la prima colonna
            current_room -= 1
            player_pos[0] = ROOM_SIZE  # Posizione nella nuova stanza
    elif player_pos[0] >= ROOM_SIZE:  # Porta a destra
        if current_room % NUM_COLS != NUM_COLS - 1:  # Se non è l'ultima colonna
            current_room += 1
            player_pos[0] = 0  # Posizione nella nuova stanza
    elif player_pos[1] <= 0:  # Porta in alto
        if current_room >= NUM_COLS:  # Se non è la prima riga
            current_room -= NUM_COLS
            player_pos[1] = ROOM_SIZE  # Posizione nella nuova stanza
    elif player_pos[1] >= ROOM_SIZE:  # Porta in basso
        if current_room < NUM_ROOMS - NUM_COLS:  # Se non è l'ultima riga
            current_room += NUM_COLS
            player_pos[1] = 0  # Posizione nella nuova stanza

# Loop principale
running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    # Gestione del movimento del personaggio
    keys = p.key.get_pressed()
    if keys[p.K_UP]:
        move_player("UP")
    if keys[p.K_DOWN]:
        move_player("DOWN")
    if keys[p.K_LEFT]:
        move_player("LEFT")
    if keys[p.K_RIGHT]:
        move_player("RIGHT")

    # Disegna il labirinto e il personaggio
    win.fill(WHITE)
    draw_matrix()
    draw_player()
    p.display.flip()

# Chiudi Pygame
p.quit()