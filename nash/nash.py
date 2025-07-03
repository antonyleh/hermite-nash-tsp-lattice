import pulp
import numpy as np

##############################################################################
# 1) Vérifier que (x, y) forme un équilibre de Nash
##############################################################################
def est_equilibre(A, B, x, y):
    eps = 1e-8  # Tolérance pour les comparaisons en flottant

    # Calcul du gain total attendu pour le joueur Ligne :
    gain_x = x @ A @ y
    # Calcul des gains purs pour chaque stratégie de Ligne 
    gain_pure_x = A @ y
    max_gain_pure_x = np.max(gain_pure_x)
    
    # Vérifier que xᵀ A y = max(eiᵀ A y) ( on se laisse une petite marge d'erreur )
    if not (abs(gain_x - max_gain_pure_x) <= eps):
        return False     
    
    # De même pour le joueur Colonne :
    gain_y = x @ B @ y
    gain_pure_y = x @ B 
    max_gain_pure_y = np.max(gain_pure_y)
    if not (abs(gain_y - max_gain_pure_y) <= eps):
        return False     
    
    return True


##############################################################################
# 2) Résolution d'un équilibre de Nash par MILP
##############################################################################
def equilibre_de_nash(A, B, M = 1000, solver = None):
    """
    Contraintes  :
      1. Simplex :
         • ∑ x[i] = 1
         • ∑ y[j] = 1
      2. M pour le support :
         • Pour tout i : x[i] ≤ M * (1 - r[i])
         • Pour tout j : y[j] ≤ M * (1 - s[j])
      3. Définition des gains purs :
         • Pour tout i : gain_purs_i[i] = ∑ (A[i,j] * y[j])
         • Pour tout j : gain_purs_j[j] = ∑ (B[i,j] * x[i])
      4. Meilleure réponse :
         • Pour tout i : gain_purs_i[i] ≤ alpha et gain_purs_i[i] ≥ alpha - M * r[i]
         • Pour tout j : gain_purs_j[j] ≤ beta  et gain_purs_j[j] ≥ beta  - M * s[j]
      5. Objectif :
         • Minimiser 0 (objectif trivial pour une solution faisable).
    """
    m, n = A.shape  # Nombre de stratégies pour chaque joueur

    # Création du problème MILP (objectif de minimisation trivial)
    prob = pulp.LpProblem("Equilibre_de_Nash", pulp.LpMinimize)

    # Variables de stratégies mixtes (probabilités entre 0 et 1)
    x = pulp.LpVariable.dicts("x", range(m), lowBound=0, upBound=1, cat=pulp.LpContinuous)
    y = pulp.LpVariable.dicts("y", range(n), lowBound=0, upBound=1, cat=pulp.LpContinuous)
    
    # Variables binaires indiquant si une stratégie n'est PAS jouée (support)
    r = pulp.LpVariable.dicts("r", range(m), cat=pulp.LpBinary)
    s = pulp.LpVariable.dicts("s", range(n), cat=pulp.LpBinary)
    
    # Variables de gain d'équilibre pour chaque joueur
    alpha = pulp.LpVariable("alpha", cat=pulp.LpContinuous) # pour Ligne
    beta  = pulp.LpVariable("beta",  cat=pulp.LpContinuous) #pour Colonne
    
    # Variables pour les gains purs (si stratégie pure jouée)
    gain_i = pulp.LpVariable.dicts("gain_i", range(m), cat=pulp.LpContinuous)
    gain_j = pulp.LpVariable.dicts("gain_j", range(n), cat=pulp.LpContinuous)

    # Contraintes : la somme des probabilités doit être égale à 1 pour chaque joueur
    prob += (pulp.lpSum([x[i] for i in range(m)]) == 1, "Somme_x_=_1")
    prob += (pulp.lpSum([y[j] for j in range(n)]) == 1, "Somme_y_=_1")

    # Contraintes M : xi <= M(1 - ri), ce qui force xi = 0 si ri = 1, idem pour yi et si
    for i in range(m):
        prob += (x[i] <= M * (1 - r[i]), f"M_x_{i}")
    for j in range(n):
        prob += (y[j] <= M * (1 - s[j]), f"M_y_{j}")

    # Définition du gain pur pour chaque stratégie pure
    for i in range(m):
        prob += (gain_i[i] - pulp.lpSum(A[i, j] * y[j] for j in range(n)) == 0,
                 f"gain_i_def_{i}")
    for j in range(n):
        prob += (gain_j[j] - pulp.lpSum(B[i, j] * x[i] for i in range(m)) == 0,
                 f"gain_j_def_{j}")

    # Contraintes de meilleure réponse : les stratégies jouées doivent rapporter exactement alpha (ou beta)
    for i in range(m):
        prob += (gain_i[i] <= alpha, f"1er_contrainte_alpha{i}")
        prob += (gain_i[i] >= alpha - M * r[i], f"2eme_contrainte_alpha{i}")
    for j in range(n):
        prob += (gain_j[j] <= beta, f"1er_contraite_beta{j}")
        prob += (gain_j[j] >= beta - M * s[j], f"2eme_contrainte_beta{j}")

    # Objectif trivial : minimiser 0 (on cherche simplement une solution faisable)
    prob.setObjective(pulp.lpSum([]))

    # Résolution avec le solveur CBC par défaut si aucun n'est fourni
    if solver is None:
        solver = pulp.PULP_CBC_CMD(msg=False)
    prob.solve(solver)

    # Vérification du statut de la solution
    if pulp.LpStatus[prob.status] != "Optimal":
        return None

    # Extraction des solutions
    x_sol = np.array([pulp.value(x[i]) for i in range(m)])
    y_sol = np.array([pulp.value(y[j]) for j in range(n)])
    alpha_sol = pulp.value(alpha)
    beta_sol = pulp.value(beta)

    return x_sol, y_sol, alpha_sol, beta_sol


##############################################################################
# 3) Fonctions de test sur différents jeux
##############################################################################
def test_classic_games():
    """
    Teste le modèle MILP sur quelques jeux classiques et affiche la solution
    et la vérification de l'équilibre de Nash.
    """
    games = []
    
    # a) Matching Pennies (jeu 2x2)
    A_mp = np.array([[1, -1],
                     [-1, 1]])
    B_mp = np.array([[-1, 1],
                     [1, -1]])
    games.append(("Matching Pennies", A_mp, B_mp))
    
    # b) Pierre-Feuille-Ciseaux (jeu 3x3)
    A_rps = np.array([[ 0, -1,  1],
                      [ 1,  0, -1],
                      [-1,  1,  0]])
    B_rps = -A_rps
    games.append(("Pierre-Feuille-Ciseaux", A_rps, B_rps))
    
    # c) Coordination Game (jeu 2x2)
    A_coord = np.array([[2, 0],
                        [0, 1]])
    B_coord = np.array([[2, 0],
                        [0, 1]])
    games.append(("Coordination Game", A_coord, B_coord))
    
    print("=== Tests sur jeux classiques ===")
    for name, A, B in games:
        print(f"\n--> Jeu : {name}")
        sol = equilibre_de_nash(A, B, M=10)
        if sol is None:
            print("  Pas de solution trouvée.")
        else:
            x_sol, y_sol, alpha_sol, beta_sol = sol
            print("  Solution MILP obtenue :")
            print("    x =", x_sol)
            print("    y =", y_sol)
            print("    alpha =", alpha_sol, ", beta =", beta_sol)
            is_NE = est_equilibre(A, B, x_sol, y_sol)
            print("  Est-ce un équilibre de Nash ? ->", is_NE)


def generate_random_game(m, n, low=-10, high=10):
    """
    Génère aléatoirement deux matrices A et B (m x n) avec des valeurs entières
    entre low et high.
    """
    A = np.random.randint(low, high+1, size=(m, n)).astype(float)
    B = np.random.randint(low, high+1, size=(m, n)).astype(float)
    return A, B


def test_random_games(nb_tests=5, m=3, n=3):
    """
    Teste le modèle MILP sur nb_tests jeux aléatoires et affiche la solution
    et la vérification de l'équilibre de Nash.
    """
    print(f"\n=== Tests sur jeux aléatoires (taille {m}x{n}, {nb_tests} instances) ===")
    for i in range(nb_tests):
        A, B = generate_random_game(m, n, low=-5, high=5)
        sol = equilibre_de_nash(A, B, M=1000)
        print(f"\nTest #{i+1} :")
        if sol is None:
            print("  Aucune solution trouvée (statut non Optimal).")
        else:
            x_sol, y_sol, alpha_sol, beta_sol = sol
            print("  Solution MILP obtenue :")
            print("    x =", x_sol)
            print("    y =", y_sol)
            print("    alpha =", alpha_sol, ", beta =", beta_sol)
            test = est_equilibre(A, B, x_sol, y_sol)
            print("  Est-ce un équilibre de Nash ? ->", test)
        print("  Matrice A :\n", A)
        print("  Matrice B :\n", B)


def test_non_equilibre():
    """
    Test supplémentaire sur un jeu dont la stratégie donnée n'est PAS un équilibre.
    Ici, on utilise le Coordination Game avec x = [0.5, 0.5] et y = [0.5, 0.5].
    """
    A = np.array([[2, 0],
                        [0, 1]])
    B= np.array([[2, 0],
                        [0, 1]])
    
    x = np.array([0.5, 0.5])
    y = np.array([0.5, 0.5])
    
    result = est_equilibre(A, B, x, y)
    print("Test non-équilibre (Coordination Game, x = [0.5,0.5], y = [0.5,0.5]) :")
    print("  est_equilibre =", result)


##############################################################################
# 4) Exécution des tests
##############################################################################
if __name__ == "__main__":
    test_classic_games()         # Tests sur des jeux classiques connus
    test_random_games(nb_tests=3, m=2, n=2)  # Tests sur jeux aléatoires (petite taille)
    test_random_games(nb_tests=2, m=3, n=4)  # Tests sur jeux aléatoires (taille différente)
    test_non_equilibre()       # Test supplémentaire (doit renvoyer False)
