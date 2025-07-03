import random
import time
import numpy as np
from sklearn.cluster import KMeans
from tsp.utils import generate_instance, evaluate_solution
from tsp.rech_loc import recherche_locale

def cluster_clients_with_kmeans(coords, k_livreur):
    """Répartit les clients en k groupes géographiquement proches"""
    n_clients = len(coords) - 1
    client_coords = np.array([coords[i] for i in range(1, n_clients + 1)])
    
    # Utilisation de K-means pour former les groupes
    kmeans = KMeans(n_clusters=k_livreur, init='k-means++', n_init=5, random_state=42)
    labels = kmeans.fit_predict(client_coords)
    
    # Construction des groupes
    clusters = [[] for _ in range(k_livreur)]
    for i, label in enumerate(labels):
        client_id = i + 1
        clusters[label].append(client_id)
    
    return clusters

def optimize(clusters, coords, dist):
    """Optimise chaque tournée avec la recherche locale"""
    depot = 0
    tournees = []
    costs = []
    
    for cluster_idx, cluster in enumerate(clusters):
        if not cluster:
            tournees.append([depot, depot])
            costs.append(0)
            continue
        
        # Tournée initiale: dépôt → clients → dépôt
        tournee_initiale = [depot] + cluster + [depot]
        
        # Optimisation par recherche locale
        tournee_optimisee = recherche_locale(tournee_initiale.copy(), dist)
        cout = evaluate_solution(tournee_optimisee, dist)
            
        tournees.append(tournee_optimisee)
        costs.append(cout)
        
        print(f"    → Coût après optimisation: {cout}")
    
    return tournees, costs

def solve_real_problem(coords, dist, k_livreur):
    """Résout le problème de logistique avec clustering + recherche locale"""
    start_time = time.time()
    n_clients = len(coords) - 1
    
    print(f"Problème: {n_clients} clients, {k_livreur} livreurs")
    
    # 1. Grouper les clients par proximité
    clusters = cluster_clients_with_kmeans(coords, k_livreur)
    
    # Affichage des groupes
    total_clients = 0
    for i, cluster in enumerate(clusters):
        total_clients += len(cluster)
        print(f"  Groupe {i+1}: {len(cluster)} clients")
        
        if cluster:
            cost = evaluate_solution([0] + cluster + [0], dist)
            print(f"    Coût initial: {cost}")
    
    print(f"  Total clients: {total_clients}/{n_clients}")
    
    # 2. Optimiser chaque tournée
    tournees, costs = optimize(clusters, coords, dist)
    
    execution_time = time.time() - start_time
    max_cost = max(costs)
    
    return tournees, costs, max_cost, execution_time

def display_results(tournees, costs):
    """Affiche les résultats: tournées et statistiques"""
    print("\nTournées:")
    print("="*30)
    
    for i, (tournee, cost) in enumerate(zip(tournees, costs)):
        clients = len(tournee) - 2
        print(f"Livreur {i+1}: {clients} clients, coût = {cost}")
        print(f"  {tournee}")
        print()
    
    # Statistiques
    max_cost = max(costs)
    avg_cost = sum(costs) / len(costs)
    std_dev = np.std(costs)
    
    print("Statistiques:")
    print("-"*20)
    print(f"  Max: {max_cost}")
    print(f"  Moyenne: {avg_cost:.2f}")
    print(f"  Écart-type: {std_dev:.2f}")
    
    if min(costs) > 0:
        print(f"  Ratio max/min: {(max_cost/min(costs)):.2f}")

def main():
    """Génération d'une instance et résolution"""
    n_clients = 100  # Nombre de clients
    k_livreur = 10   # Nombre de livreurs

    print("Génération d'une instance...")
    coords, dist = generate_instance(n_clients)
    
    print("\n" + "="*40)
    print("RÉSOLUTION PROBLÈME DE LOGISTIQUE")
    print("="*40)
    tournees, costs, max_cost, execution_time = solve_real_problem(coords, dist, k_livreur)
    
    display_results(tournees, costs)
    
    print(f"\nTemps d'exécution: {execution_time:.2f}s")
    print(f"Coût maximal d'une tournée: {max_cost}")

if __name__ == "__main__":
    main()