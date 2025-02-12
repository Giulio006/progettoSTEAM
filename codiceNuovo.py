import networkx as nx
import random

def generate_graph(rows, cols):
    # Creare un grafo vuoto
    G = nx.Graph()
    
    # Generare nodi in una struttura a griglia
    for r in range(rows):
        for c in range(cols):
            node_id = r * cols + c
            G.add_node(node_id)
    
    # Dizionario per memorizzare i nodi adiacenti
    adjacent_nodes = {}
    
    # Aggiungere connessioni tra nodi adiacenti
    for r in range(rows):
        for c in range(cols):
            current_node = r * cols + c
            adjacent = []
            
            # Connessione destra
            if c < cols - 1:
                right_node = current_node + 1
                G.add_edge(current_node, right_node)
                adjacent.append(right_node)
            
            # Connessione sinistra
            if c > 0:
                left_node = current_node - 1
                adjacent.append(left_node)
            
            # Connessione sotto
            if r < rows - 1:
                down_node = current_node + cols
                G.add_edge(current_node, down_node)
                adjacent.append(down_node)
            
            # Connessione sopra
            if r > 0:
                up_node = current_node - cols
                adjacent.append(up_node)
            
            # Memorizzare i nodi adiacenti
            adjacent_nodes[current_node] = adjacent
    
    # Rimuovere connessioni in modo selettivo
    for node in list(G.nodes()):
        # Ottenere i vicini attuali
        current_neighbors = list(G.neighbors(node))
        
        # Numero massimo di connessioni da rimuovere
        max_removals = len(current_neighbors)
        
        # Numero casuale di connessioni da rimuovere
        num_removals = random.randint(0, 1)  # Puoi cambiare il range se necessario
        
        # Tentativi di rimozione
        for _ in range(num_removals):
            if len(current_neighbors) > 1:  # Assicurarsi di mantenere almeno una connessione
                # Scegliere un vicino casuale da rimuovere
                neighbor_to_remove = random.choice(current_neighbors)
                
                # Simulare la rimozione e verificare la connettività
                G_temp = G.copy()
                G_temp.remove_edge(node, neighbor_to_remove)
                
                # Verificare che la rimozione non isoli nessun nodo
                if nx.is_connected(G_temp):
                    G = G_temp
                    current_neighbors.remove(neighbor_to_remove)
    
    # Aggiornare il dizionario dei nodi adiacenti dopo la rimozione
    adjacent_nodes = {node: list(G.neighbors(node)) for node in G.nodes()}
    
    # Restituire il dizionario dei nodi e delle adiacenze
    return adjacent_nodes


def main():
    # Esempio di utilizzo
    rows = 4
    cols = 6
    nodi_adiacenti = generate_graph(rows, cols)

    # Stampa il dizionario dei nodi e delle adiacenze
    print("Nodi adiacenti:")
    for node, neighbors in nodi_adiacenti.items():
        print(f"Nodo {node}: {neighbors}")