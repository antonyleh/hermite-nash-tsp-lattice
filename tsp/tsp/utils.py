import random

def generate_instance(n):
    """
    Génère un problème TSP avec n clients + 1 centre (0).
    Positionne les clients dans une grille n^2 x n^2 au hasard.
    """
    coords = {}
    # Centre (index 0), placé au 'milieu' pour l'exemple
    center_x = n**2 // 2
    center_y = n**2 // 2
    coords[0] = (center_x, center_y)
    
    # Clients 1..n
    for i in range(1, n+1):
        x = random.randint(0, n**2 - 1)
        y = random.randint(0, n**2 - 1)
        coords[i] = (x, y)
    
    # Distances Manhattan
    dist = {}
    nodes = list(coords.keys())
    for i in nodes:
        for j in nodes:
            if i == j:
                dist[(i, j)] = 0
            else:
                (x1, y1) = coords[i]
                (x2, y2) = coords[j]
                dist[(i, j)] = abs(x2 - x1) + abs(y2 - y1)
    return coords, dist

def check_solution(tour, n):
    """
    Vérifie qu'un circuit 'tour' visite:
      - le centre (0) au départ et à la fin
      - chaque client 1..n exactement une fois
    """
    if len(tour) != n + 2:
        return False
    if tour[0] != 0 or tour[-1] != 0:
        return False
    clients_visited = set(tour[1:-1])
    return clients_visited == set(range(1, n+1))

def evaluate_solution(tour, dist):
    """
    Calcule la somme des distances pour une liste de sommets 'tour'.
    """
    cost = 0
    for i in range(len(tour) - 1):
        cost += dist[(tour[i], tour[i+1])]
    return cost


def convert_dist_format(dist_dict, n):
    """
    Convertit un dictionnaire de distances en une matrice 2D pour la programmation dynamique et l'ILP.
    """
    # Initialiser une matrice de distance n x n
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # Remplir la matrice avec les distances du dictionnaire
    for i in range(n):
        for j in range(n):
            if i != j:  # Pas de distance pour les mêmes nœuds (diagonale)
                key = (i, j) if (i, j) in dist_dict else (j, i)
                matrix[i][j] = dist_dict[key]

    
    return matrix