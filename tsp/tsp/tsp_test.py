import time
from utils import generate_instance, check_solution, evaluate_solution, convert_dist_format
from approx import solve_tsp_2approx
from rech_loc import recherche_locale
from progdyn import tspPrDy
from ilp import tsp_ilp_solver

def test_comparaison(n_clients):
    """
    Teste et compare les différentes approches sur une instance de taille n_clients.
    """
    print(f"=== Test de comparaison pour {n_clients} clients ===")
    
    # Génération de l'instance
    print("\nGénération de l'instance...")
    coords, dist = generate_instance(n_clients)
    print(f"Instance créée avec {n_clients} clients + 1 dépôt")
    
    # Conversion du format du dictionnaire de distances pour programmation dynamique et ILP
    new_dist = convert_dist_format(dist, n_clients + 1)  # +1 pour inclure le dépôt
    
    optimal_cost = None  # Variable pour stocker le coût optimal (sera déterminé par PD ou ILP)
    
    # 3. Programmation dynamique - On l'exécute d'abord pour connaître la solution optimale
    print("\n3. Test de la programmation dynamique...")
    # Limitation de la programmation dynamique pour des instances de petite taille
    if n_clients > 15:
        print("Instance trop grande pour la programmation dynamique (n > 15)")
        pd_time = "N/A"
        pd_cost = "N/A"
        pd_valid = "N/A"
        pd_tour = "N/A"
        pd_status = "Non exécuté"
    else:
        start_time = time.time()
        pd_result = tspPrDy(new_dist, 0)  # 0 est l'indice du dépôt
        pd_time = time.time() - start_time
        pd_cost = pd_result[0]
        pd_tour = pd_result[1]
        
        pd_valid = check_solution(pd_tour, n_clients)
        pd_status = "Optimal"  # La programmation dynamique garantit l'optimalité
        
        # Définir le coût optimal connu
        optimal_cost = pd_cost
        
        print(f"Temps d'exécution: {pd_time:.4f} secondes")
        print(f"Coût de la solution: {pd_cost}")
        print(f"Tournée: {pd_tour}")
    
    # 4. Programmation linéaire (ILP) - Exécutée ensuite pour confirmer l'optimalité
    print("\n4. Test de la programmation linéaire (ILP)...")
    # Limitation de l'ILP pour des instances de petite taille
    if n_clients > 15:
        print("Instance trop grande pour la programmation linéaire (n > 20)")
        ilp_time = "N/A"
        ilp_cost = "N/A"
        ilp_valid = "N/A"
        ilp_tour = "N/A"
        ilp_status = "Non exécuté"
    else:
        start_time = time.time()
        ilp_result = tsp_ilp_solver(0, new_dist)  # 0 est l'indice du dépôt
        ilp_time = time.time() - start_time
        ilp_cost = ilp_result[0]
        ilp_tour = ilp_result[1]
        
        ilp_valid = check_solution(ilp_tour, n_clients)
        ilp_status = "Optimal"  # L'ILP garantit l'optimalité
        
        print(f"Temps d'exécution: {ilp_time:.4f} secondes")
        print(f"Coût de la solution: {ilp_cost}")
        print(f"Tournée: {ilp_tour}")
    
    # Si nous n'avons toujours pas de coût optimal (ni PD ni ILP n'ont pu être exécutés),
    # nous ne pourrons pas déterminer l'optimalité des heuristiques
    can_determine_optimality = optimal_cost is not None
    
    # 1. Algorithme 2-approx
    print("\n1. Test de l'algorithme 2-approximation...")
    start_time = time.time()
    approx_tour = solve_tsp_2approx(coords, dist)
    approx_time = time.time() - start_time
    approx_cost = evaluate_solution(approx_tour, dist)
    approx_valid = check_solution(approx_tour, n_clients)
    
    approx_status = "Optimal" if approx_cost == optimal_cost else "Non optimal"
    gap = ((approx_cost - optimal_cost) / optimal_cost) * 100 if optimal_cost > 0 else 0

    
    print(f"Temps d'exécution: {approx_time:.4f} secondes")
    print(f"Coût de la solution: {approx_cost}")
    print(f"Status: {approx_status}")
    if approx_status != "Optimal":
        print(f"Écart avec l'optimal: {gap:.2f}%")
    print(f"Tournée: {approx_tour}")
    
    # 2. Recherche locale avec solution initiale simple
    print("\n2. Test de la recherche locale...")
    # Création d'une tournée initiale simple: dépôt -> clients dans l'ordre -> dépôt
    initial_tour = [0] + list(range(1, n_clients + 1)) + [0]
    initial_cost = evaluate_solution(initial_tour, dist)
    
    start_time = time.time()
    local_tour = recherche_locale(initial_tour.copy(), dist)
    local_time = time.time() - start_time
    local_cost = evaluate_solution(local_tour, dist)
    local_valid = check_solution(local_tour, n_clients)
    
    # Déterminer si la solution est optimale
    local_status = "Optimal" if local_cost == optimal_cost else "Non optimal"
    gap = ((local_cost - optimal_cost) / optimal_cost) * 100 if optimal_cost > 0 else 0

    print(f"Temps d'exécution: {local_time:.4f} secondes")
    print(f"Status: {local_status}")
    if local_status != "Optimal":
        print(f"Écart avec l'optimal: {gap:.2f}%")
    print(f"Tournée: {local_tour}")
    
    # Résumé des résultats
    print("\n=== Résumé des résultats ===")
    print(f"{'Méthode':<30} | {'Coût':<10} | {'Temps (s)':<10} | {'Valide':<10} | {'Status':<15}")
    print("-" * 80)
    
    if isinstance(pd_time, float):
        print(f"{'Programmation dynamique':<30} | {pd_cost:<10} | {pd_time:<10.4f} | {'Oui' if pd_valid else 'Non':<10} | {pd_status:<15}")
    else:
        print(f"{'Programmation dynamique':<30} | {pd_cost:<10} | {pd_time:<10} | {pd_valid:<10} | {pd_status:<15}")
    
    if isinstance(ilp_time, float):
        print(f"{'Programmation linéaire (ILP)':<30} | {ilp_cost:<10} | {ilp_time:<10.4f} | {'Oui' if ilp_valid else 'Non':<10} | {ilp_status:<15}")
    else:
        print(f"{'Programmation linéaire (ILP)':<30} | {ilp_cost:<10} | {ilp_time:<10} | {ilp_valid:<10} | {ilp_status:<15}")
    
    print(f"{'Algorithme 2-approx':<30} | {approx_cost:<10} | {approx_time:<10.4f} | {'Oui' if approx_valid else 'Non':<10} | {approx_status:<15}")
    print(f"{'Recherche locale':<30} | {local_cost:<10} | {local_time:<10.4f} | {'Oui' if local_valid else 'Non':<10} | {local_status:<15}")
    
    # Déterminer la meilleure méthode
    best_methods = []
    best_cost = float('inf')
    
    if approx_valid and isinstance(approx_cost, (int, float)):
        if approx_cost < best_cost:
            best_cost = approx_cost
            best_methods = ["Algorithme 2-approx"]
        elif approx_cost == best_cost:
            best_methods.append("Algorithme 2-approx")
    
    if local_valid and isinstance(local_cost, (int, float)):
        if local_cost < best_cost:
            best_cost = local_cost
            best_methods = ["Recherche locale"]
        elif local_cost == best_cost:
            best_methods.append("Recherche locale")
    
    if pd_valid == True and isinstance(pd_cost, (int, float)):
        if pd_cost < best_cost:
            best_cost = pd_cost
            best_methods = ["Programmation dynamique"]
        elif pd_cost == best_cost:
            best_methods.append("Programmation dynamique")
    
    if ilp_valid == True and isinstance(ilp_cost, (int, float)):
        if ilp_cost < best_cost:
            best_cost = ilp_cost
            best_methods = ["Programmation linéaire (ILP)"]
        elif ilp_cost == best_cost:
            best_methods.append("Programmation linéaire (ILP)")
    

def main():
    # Taille de l'instance à tester - ATTENTION: utiliser de petites valeurs
    # car la programmation dynamique et l'ILP sont exponentielles
    n_clients = 8  # Pour tester les 4 méthodes, garder n ≤ 15
    
    # Lancer le test de comparaison
    test_comparaison(n_clients)
    

if __name__ == "__main__":
    main()