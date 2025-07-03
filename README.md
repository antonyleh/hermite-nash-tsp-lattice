# Algorithmique Avancée: Projet

## Auteurs

- Abongo Charles-Valentin
- Asso Ali Mullud
- Antony Lehmann

## Structure du projet

Le projet est divisé en 4 répertoires.
Chaque répertoire désigne un travail qui était à faire mêlant code et
test. Les sections suivantes décriront les emplacements du code et des tests.

## Hermite

Dans ce répertoire, le fichier code.py contient le code nécessaire afin
d'obtenir la forme normale de Hermite (FNH) d'une matrice A mxn à coefficients
entiers (où m <= n) et afin d'effectuer la résolution de Ax = b par la FNH.
Le fichier test.py contient l'ensemble des tests effectués (il suffit juste
de lancer une fois dans le répertoire: python test.py).

### Réutilisation du code de code.py

Après avoir importé code.py dans un autre script python, voici la procédure
pour calculer une FNH d'une matrice A et pour tenter de résoudre Ax = b où
A et b sont des arrays numpy décrivant matrice et vecteur:

- **getHNF(A)**: retourne un couple d'arrays H,U où H est la FNH calculée à
partir de A et U est la matrice unimodulaire telle que H = AU.

- **intSolverByHermite(A,b)**: retourne None si aucune solution x à coefficients
entiers à l'équation Ax = b, sinon un couple (y, x) de vecteurs de taille n est
retourné où y est une solution à l'équation Hy = b tandis que x est une solution
à l'équation Ax = b (remarque: x = Uy).

- **matrix_generator(m,n,lim)**: retourne un array décrivant une matrice mxn où
les coefficients ont été générés aléatoirement entre -lim et lim où lim est un
entier positif.

- **genVector(n,b)**: retourne un array décrivant un vecteur de taille n dont les
coefficients ont été générés aléatoirement entre -b et b où b est un
entier positif.



## Équilibre de Nash

Dans ce répertoire, le fichier nash.py contient l'implémentation de la recherche d'équilibres de Nash dans des jeux à somme non nulle sous forme normale. Le fichier inclut à la fois le code principal et les tests qui s'exécutent automatiquement lorsqu'on lance le script.

### Fonctionnalités et usage

Le fichier nash.py propose deux fonctions principales:

* **est_equilibre**: vérifie si une paire de stratégies mixtes forme un équilibre de Nash pour un jeu donné. La fonction prend en entrée deux matrices de gain A et B (pour les joueurs Ligne et Colonne) et deux vecteurs de stratégies mixtes x et y, puis retourne True si c'est un équilibre, False sinon.

* **equilibre_de_nash**: calcule un équilibre de Nash pour un jeu donné en utilisant une formulation de programmation linéaire mixte (MILP). La fonction prend en entrée les matrices de gain A et B, un paramètre M pour les contraintes "Big-M" et optionnellement un solveur spécifique. Elle retourne un quadruplet (x, y, alpha, beta) où x et y sont les stratégies
d'équilibre des deux joueurs Ligne et Colonne et alpha et beta sont les gains à l'équilibre de Ligne et Colonne respectivement.

Le fichier inclut également plusieurs fonctions de test qui démontrent l'utilisation sur des jeux classiques (Matching Pennies, Pierre-Feuille-Ciseaux, Coordination Game) et sur des jeux générés aléatoirement.

### Raisonnement et approche

Pour calculer un équilibre de Nash, nous avons transformé le problème en un programme linéaire mixte avec:

1. **Variables**:
   - Variables continues représentant les stratégies mixtes des joueurs
   - Variables binaires indiquant si une stratégie pure fait partie du support
   - Variables représentant les gains espérés pour chaque stratégie pure

2. **Contraintes clés**:
   - Contraintes de simplex: les stratégies mixtes sont des distributions de probabilité
   - Contraintes de support: liant les variables binaires aux stratégies mixtes
   - Contraintes de définition des gains purs pour chaque stratégie
   - Contraintes de meilleure réponse: assurant qu'aucun joueur ne peut améliorer son gain

3. **Objectif**:
   - La fonction objectif est triviale (minimiser 0) car nous cherchons simplement une solution faisable

Cette formulation MILP permet d'exprimer mathématiquement la définition d'un équilibre de Nash: dans un équilibre, toutes les stratégies pures jouées avec une probabilité positive donnent le même gain espéré, et toutes les autres stratégies pures donnent un gain inférieur ou égal.

### Utilisation et tests

Pour utiliser le fichier nash.py, il faut d'abord s'assurer que les bibliothèques numpy et pulp sont installées. On peut ensuite:

1. **Exécuter les tests intégrés** en lançant simplement le fichier 

2. **Utiliser les fonctions dans des scripts personnalisés** en important le module et en appelant les fonctions avec les paramètres appropriés

3. **Créer ses propres tests** en définissant des matrices de gain et en utilisant les fonctions fournies

4. **Tester des jeux de grande taille** en générant des jeux aléatoires et en ajustant le paramètre M pour les contraintes

## Problème du commis voyageur (TSP-métrique)

Ce module implémente différentes approches pour résoudre le problème du voyageur de commerce (TSP) avec une distance métrique (respectant l'inégalité triangulaire) ainsi qu'une application au problème de logistique du dernier kilomètre avec k livreurs.

## Structure du projet

Le projet est organisé comme suit:
- Le répertoire `tsp/` contient un package Python avec plusieurs modules implémentant différentes approches pour le TSP.
- Le fichier `solve_real_problem.py` utilise ce package pour résoudre un problème réel avec k livreurs.

## Package tsp

Le package `tsp` permet la résolution du problème TSP-métrique par 4 méthodes différentes sur un graphe complet et modélise la grille où le(s) livreur(s) devront délivrer leurs colis aux différents clients.

### utils.py

Ce module fournit des fonctions utilitaires pour générer des instances du problème, vérifier et évaluer les solutions:

- `generate_instance(n)`: Génère une instance du problème TSP avec n clients (+ 1 dépôt) positionnés sur une grille n²×n². Retourne un dictionnaire des coordonnées et un dictionnaire des distances (distance de Manhattan).
  
- `check_solution(tour, n)`: Vérifie qu'un circuit est valide (commence et finit au dépôt, visite chaque client exactement une fois).
  
- `evaluate_solution(tour, dist)`: Calcule le coût total d'un circuit (somme des distances).
  
- `convert_dist_format(dist_dict, n)`: Convertit le format du dictionnaire de distances en matrice 2D pour la programmation dynamique et l'ILP.

### progdyn.py

Ce module permet de résoudre le problème TSP par programmation dynamique. Le graphe
complet sera modélisé par D, une liste de listes ou un dictionnaire de dictionnaires
dont les clés seraient des entiers de façon que pour deux sommets d'indices i et j,
la distance entre les sommets soit obtenue en faisant D[i][j]. Il est important de
noter que pour le problème TSP, il faut indiquer le sommet du graphe qui correspond au
point et de départ et d'arrivée du livreur. La plupart du temps, ce sommet admet
l'indice 0 mais dans des cas plus généraux, on nomme l'indice de ce sommet origin.

Afin de manipuler ce module, l'unique fonction à connaître est la fonction
**tspPrDy(distances,origin)** où distances désigne D, la modélisation du graphe complet
et origin désigne l'indice entier évoqué juste avant. La fonction retourne un couple (v,c)
où v est le coût d'un cycle hamiltonien optimal et c est un tel cycle sous la forme d'une liste d'indices de sommets.

Cette méthode garantit l'optimalité mais a une complexité exponentielle en O(n²2ⁿ), ce qui la limite aux petites instances (n ≤ 15).

### ilp.py

Ce module permet de résoudre le problème TSP par résolution d'un problème d'optimisation
linéaire ILP (Integer Linear Programming). Pour plus de détails sur cette méthode de
résolution, on peut se référer au code du module pour les détails techniques ainsi qu'à la
feuille de TP pour les idées générales. Comme pour le module progdyn.py, le graphe complet
G est modélisé exactement de la même façon par D.

Afin de manipuler ce module, l'unique fonction à connaître est la fonction
**tsp_ilp_solver(origin,distances)** où distances désigne D, la modélisation du graphe complet
et origin désigne l'indice du sommet d'où doit partir et revenir le livreur. La fonction retourne un couple (v,c)
où v est le coût d'un cycle hamiltonien optimal et c est un tel cycle sous la forme d'une liste d'indices de sommets.

Cette méthode garantit également l'optimalité mais a une complexité exponentielle, ce qui la limite aussi aux petites instances (n ≤ 15).

### rech_loc.py

Ce module implémente la méthode de recherche locale (2-opt) pour le TSP:

- `recherche_locale(tour, dist)`: Optimise une tournée initiale en utilisant la recherche locale 2-opt. Cette méthode part d'une solution existante qui est générée de façon triviale en visitant les clients dans l'ordre croissant de leurs indices : [0, 1, 2, ..., n, 0],et l'améliore itérativement en échangeant des paires d'arêtes si cela réduit le coût total. La
fonction retourne sous forme d'une liste d'indices le cycle qui a été calculé.

- Approche: À chaque itération, examine toutes les paires d'arêtes non adjacentes et effectue un échange si cela améliore la solution. Continue jusqu'à ce qu'aucune amélioration ne soit possible.

Cette heuristique ne garantit pas l'optimalité mais donne de bonnes solutions en temps polynomial, ce qui la rend applicable aux grandes instances. Elle converge vers un optimum local.

### approx.py

Ce module implémente une approximation à facteur 2 pour le TSP:

- `solve_tsp_2approx(coords, dist)`: Implémente l'algorithme d'approximation à facteur 2 basé sur l'arbre couvrant minimal. La
fonction retourne sous forme d'une liste d'indices le cycle qui a été calculé.

- Approche:
  1. Construit un arbre couvrant minimal (MST) avec l'algorithme de Kruskal
  2. Effectue un parcours en profondeur (DFS) sur cet arbre pour visiter tous les sommets
  3. Revient au point de départ pour former un cycle hamiltonien

Cette méthode garantit que la solution est au plus 2 fois pire que l'optimal et s'exécute en temps polynomial O(n² log n), ce qui la rend applicable aux grandes instances.

### tsp_test.py

Ce module est un script de test qui compare les performances des 4 méthodes sur une même instance:

- `test_comparaison(n_clients)`: Génère une instance avec n_clients et teste les 4 méthodes, en affichant les résultats (coût, temps, validité, optimalité).

- Limitations: Pour une comparaison complète, conservez n ≤ 15 afin que les méthodes exactes (programmation dynamique et ILP) puissent s'exécuter.

## Problème réel : solve_real_problem.py

Ce script résout le problème de logistique du dernier kilomètre avec k livreurs en utilisant une approche en deux phases:

1. **Phase 1 - Clustering**: Les clients sont regroupés en k clusters à l'aide de K-means, ce qui divise le problème en k instances du TSP.
2. **Phase 2 - Optimisation**: Chaque tournée est optimisée individuellement avec la recherche locale.

### Choix de la recherche locale pour le problème réel

Bien que la recherche locale ne garantisse pas l'optimalité, plusieurs raisons justifient son utilisation pour le problème réel de logistique du dernier kilomètre:

1. **Passage à l'échelle**: Le problème réel cible environ 1000 clients et 10 livreurs. Les méthodes exactes (programmation dynamique et ILP) deviennent totalement impraticables pour de telles tailles, avec des temps d'exécution qui exploseraient exponentiellement.

2. **Qualité empirique des solutions**: En pratique, la recherche locale fournit des solutions très proches de l'optimal pour les instances TSP, particulièrement lorsque la distribution des clients est relativement uniforme. Pour de nombreuses instances réelles, la solution peut n'être que quelques pourcentages au-dessus de l'optimal.

3. **Équilibre temps/qualité**: Pour un problème opérationnel comme la logistique du dernier kilomètre, il est souvent préférable d'avoir une bonne solution en un temps raisonnable plutôt qu'une solution optimale qui prendrait des heures ou des jours à calculer.

4. **Décomposition du problème**: La décomposition du problème en k instances indépendantes via le clustering réduit significativement la complexité. Même si chaque sous-problème n'est pas résolu optimalement, la solution globale peut rester très satisfaisante en pratique.

### Fonctions principales:

- **cluster_clients_with_kmeans**: Répartit les clients en k groupes géographiquement proches à l'aide de K-means.

- **optimize**: Optimise chaque tournée avec la recherche locale.

- **solve_real_problem**: Fonction principale qui résout le problème complet (clustering + optimisation).

- **display_results**: Affiche les résultats et statistiques.

### Comment utiliser ce module

Pour tester le module avec vos propres paramètres, vous pouvez modifier les variables suivantes dans le fichier solve_real_problem.py:

- **n_clients**: Nombre de clients à servir
- **k_livreur**: Nombre de livreurs disponibles

Vous pouvez également ajouter vos propres méthodes de clustering ou d'optimisation en les intégrant dans les fonctions existantes.

## Comparaison des méthodes implémentées

| Méthode | Optimalité | Complexité | Applicable jusqu'à |
|---------|------------|------------|-------------------|
| Programmation Dynamique | Garantie | O(n²2ⁿ) | ~15 clients |
| ILP | Garantie | Exponentielle | ~15 clients |
| 2-Approximation | Facteur 2 | O(n² log n) | Centaines de clients |
| Recherche Locale | Optimum local | O(n²) par itération | Centaines de clients |


## Réduction de base et problème du vecteur le plus proche

Dans ce répertoire, se trouvent deux fichiers code.py et test.py.
Le fichier code.py contient le code pour calculer une base réduite associée à une base
B de R^n, B à coefficients entiers et qui est représentée par un array numpy de
dimension nxn (à voir comme une matrice inversible nxn) où les colonnes
décrivent les vecteurs de la base.

### Réutilisation du code de code.py

Après avoir importé code.py dans un autre script python, voici la procédure
pour calculer la base réduite associée à la base B et pour calculer à partir
de B et d'un vecteur v de taille n, le vecteur z solution de l'équation Bz = v
sauf que chaque coefficient de z a été approximé par son entier le plus proche
(remarque: cette approximation z est celle utilisée pour approcher le vecteur
du réseau engendré par B le plus proche du vecteur v).

- **reduce(B)**: retourne un triplet de 3 arrays de dimension nxn 
(B_red , Bo, M) où B_red est la base réduite associée à B et engendrant le
même réseau que B. Bo, M décrivent la décomposition de Gram-Schmidt de la base
réduite B_red (en particulier B_red = Bo.M, Bo est une matrice dont les
colonnes sont deux à deux orthogonales, M est une matrice triangulaire
supérieure dont la diagonale vaut 1 partout).

- **approxByIntegers(B,v)**: retourne un numpy array décrivant un vecteur de dimension n
qui est l'approximation z évoqué au début de cette section.

En plus de celles-ci, il existe d'autres fonctions utiles à disposition pour 
générer une base B aléatoirement de dimension n et dont les coefficients
sont des entiers variant entre -d et d (voir **genUniformBasis(n,d)**), ou pour
générer aléatoirement une matrice unimodulaire de dimension n
(voir **genUniModMatrix(n,a,b)**) ou pour générer un vecteur de dimension n
d'entiers (voir **genVector(n,b)**)
