def solve_tsp_2approx(coords, dist):
    """
    Algorithme 2-approx:
      1) Construire un MST (ici version Kruskal)
      2) Effectuer un DFS depuis la racine (0) pour lister les sommets
      3) Fermer le circuit en revenant à 0
    """
    noeud  = list(coords.keys())  # ex. 0..n
    # Création d'une liste d'arêtes (poids, i, j)
    aretes = []
    for i in noeud :
        for j in noeud :
            if i < j:
                aretes.append((dist[(i,j)], i, j))
                
                
    # Tri des arêtes par poids
    aretes.sort(key=lambda e: e[0])
    
    # Structure pour l'union-find 
    parent = {v: v for v in noeud }
    rang = {v: 0 for v in noeud }
    

    def find(v):
        """
        Trouve le représentant (chef) de la composante de v.
        Si parent[v] != v, on met à jour parent[v] pour compresser le chemin.
        """
        
        if parent[v] != v:
            parent[v] = find(parent[v])
        return parent[v]
    
    def union(a, b):
        """
        Fusionne les composantes de a et de b si elles sont distinctes.
        On utilise le rang pour attacher l'arbre le plus petit sous le plus grand.
        """
        
        parentA = find(a)
        parentB = find(b)
        if parentA != parentB:
            if rang[parentA] < rang[parentB]:
                parent[parentA] = parentB
            elif rang[parentA] > rang[parentB]:
                parent[parentB] = parentA
            else:
                parent[parentB] = parentA
                rang[parentA] += 1
    
    # Construit l'arbre couvrant minimal sous forme d'une liste d'adjacence
    arbre_couvr_min = {v: [] for v in noeud }
    for w, i, j in aretes:
        # Si i et j ne sont pas déjà connectés (ce qui éviterait une boucle), alors on peut les relier.
        if find(i) != find(j):
            union(i, j)
            arbre_couvr_min[i].append(j)
            arbre_couvr_min[j].append(i)
    
    # DFS pour créer un ordre de visite
    visited = []
    def dfs(u):
        visited.append(u)
        for v in arbre_couvr_min[u]:
            if v not in visited:
                dfs(v)
                
    dfs(0)  # part du centre (0)
    
    # On "ferme" le cycle en revenant au centre
    visited.append(0)
    
    return visited

