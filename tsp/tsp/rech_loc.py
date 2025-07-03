from utils import  evaluate_solution

def recherche_locale(tour, dist):
    """
    Optimise une tournée en utilisant la recherche locale.
    """
    nb_clients = len(tour) - 1  # -1 car la tournée inclut le dépôt
    amelioration = True
    iteration = 0
    
    # S'assurer que le premier élément est le dépôt (indice 0)
    if tour[0] != 0:
        # Trouver la position du dépôt
        depot_pos = tour.index(0)
        # Réorganiser la tournée pour qu'elle commence par le dépôt
        tour = tour[depot_pos:] + tour[:depot_pos]
    
    cout_actuel = evaluate_solution(tour, dist)
    
    while amelioration:
        amelioration = False
        for i in range(1, len(tour) - 1):  # Exclure le dépôt au début et à la fin
            for j in range(i+1, len(tour) - 1):  # Exclure le dépôt à la fin
                # Créer une nouvelle tournée en inversant la séquence entre i et j
                nouvelle_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
                nouveau_cout = evaluate_solution(nouvelle_tour, dist)
                
                # Si la nouvelle tournée est meilleure, l'adopter
                if nouveau_cout < cout_actuel:
                    tour = nouvelle_tour
                    cout_actuel = nouveau_cout
                    amelioration = True
                    iteration += 1
                    break
            
            if amelioration:
                break
    
    # Assurer que la tournée se termine par le dépôt si ce n'est pas déjà le cas
    if tour[0] != tour[-1]:
        tour.append(tour[0])
    
    return tour

