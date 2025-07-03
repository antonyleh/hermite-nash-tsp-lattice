#Idée: pour le problème delta-tsp, la méthode par programmation dynamique
#nécessite de calculer la quantité t(X,j) (voir le poly) où j est un nombre
#entre 1 et N mais où X est un sous-ensemble de S = {1,...,N}. Il est donc question
#de modéliser X en Python. Ici, on fait le choix de modéliser X par une chaîne
#de caractères T de longueur N telle que la chaîne est composée de 0 ou de 1 et
#pour tout i dans S, i est dans X si et seulement si T[i-1] vaut 1.

#Dans la définition de t(X,j), X ne contient jamais le sommet 1, par conséquent,
#si X est modélisé par T, T[0] vaudra toujours 0. On a ceci car on suppose dans la
#modélisation T, que chaque sommet i est associé à la position i-1 du tableau T, mais
#rien n'empêche de réétiqueter les sommets de S. Par conséquent, on devra explicitement
#donner l'indice dans T du sommet qui fait office de sommet 1. On nomme cet indice origin.
#Donc si le sommet 1 est bien en première position de T, alors origin vaudra 0 et si le
#sommet 1 est en 2ème position dans T, alors origin vaudra 1 et dans tous les cas T[origin]
#vaudra 0.

#Ensuite pour calculer t(X,j) il est nécessaire par sa formule de calculer
#d'autres t(Y,k). Pour ce faire, on décide de procéder par programmation dynamique mêlée
#à de la mémoisation:
# 1) on stocke les t(Y,k) déjà calculés dans un dictionnaire D
# 2) pour le calcul de t(X,j), chaque t(Y,k) à calculer non présent dans D (donc t(Y,k) inconnu),
#on fait le calcul de t(Y,k) récursivement jusqu'à pouvoir trouver des valeurs connues présentes
#dans D et pouvoir finalement calculer t(Y,k). Une fois t(X,j) calculé, on peut le mettre dans D
#et si on est amené à recalculer t(X,j), comme il est déjà dans D, il n'est en réalité pas
#utile de le recalculer, il suffit de le retourner.

#Pour chaque t(X,j), il est également possible de lui associer un plus court chemin
#C(X,j) de poids t(X,j) partant de 1, passant par chaque sommet de X une seule
#fois et terminant en le sommet j, ce que l'on fera dans les fonctions qui suivent.

#Pour le dictionnaire D évoqué, pour stocker t(X,j), il est assez évident que (X,j)
#est la clé et le couple (t(X,j), C(X,j)) sera la valeur. De plus, pour modéliser
#(X,j), on sait déjà que X est modélisé par la chaîne de caractère T évoquée plus tôt,
#mais pour modéliser j il est assez évident que l'on devra utiliser l'indice i_j qui
#dans la chaîne T correspond au sommet j. D'où (X,j) est modélisé par (T,i_j). 




#------------------------------------------------------------------------------------------------


import math
 
#La fonction initialise et retourne le dictionnaire D avec les valeurs de bases à connaître pour
#faire les calculs, i.e en notant E l'ensemble vide, les valeurs de bases t(E,1), t(E,2) jusqu'à
#t(E,N) associées respectivement à leur chemin-solution C(E,j).
#On notera que origin en paramètre désigne bien l'indice du sommet 1 dans la modélisation de E 
#par T qui est une chaîne de caractères de longueur nb_nodes=N et remplie de 0. distances[i,j]
#désigne la distance entre deux sommets I et J d'indice i et j (i,j à valeurs dans 0..N-1 donc) 
def init_storage(nb_nodes,origin,distances):
    storage = dict()
    empty_set = "0"*nb_nodes
    for i in range(nb_nodes):
        if i==origin:
            storage[(empty_set,origin)]=(distances[origin][origin],[origin])
        else:
            storage[(empty_set,i)]=(distances[origin][i],[origin,i])
    return storage


#algorithme de programmation dynamique 
def tspProgDyn(nb_nodes,distances,key,storage,origin):
    if key in storage:
        return storage[key]
    else:
        k=key[0]
        l=key[1]
        
        
        min_distance=math.inf
        set_minimizer= ""
        ind_minimizer=None

        for j in range(nb_nodes):
            if j==origin:
                continue
            if k[j] == '1':
                X_temp = k[0:j]+"0"+k[(j+1):nb_nodes]
                dist_calc = tspProgDyn(nb_nodes,distances,(X_temp,j),storage,origin)[0] + distances[j][l]
                if dist_calc < min_distance:
                    min_distance=dist_calc
                    set_minimizer=X_temp
                    ind_minimizer=j

        storage[key]=(min_distance,storage[(set_minimizer,ind_minimizer)][1]+[l])
        return storage[key]


#construire la modélisation de l'ensemble des sommets
#privé du sommet d'indice origin
def solution_set(nb_nodes,origin):
    part1 = "1"*origin
    part2 = "1"*(nb_nodes-origin-1)
    return part1+"0"+part2


#calcule d'un plus court cycle hamiltonien partant du sommet d'indice origin
#et retourne un couple (p,c) où p est le poids du plus court cycle et c est un
#plus court cycle décrit par une liste.
def tspPrDy(distances,origin):
    nb_nodes=len(distances)
    D=init_storage(nb_nodes,origin,distances)
    key=(solution_set(nb_nodes,origin),origin)
    return tspProgDyn(nb_nodes,distances,key,D,origin)



#-----------------------------------------------------------------------------------------


#test de l'algorithme tspPrDy sur un petit graphe complet 


if __name__ == "__main__":
    #graphe décrit par le dictionnaire suivant
    dist=( {
        0 : {0: 0.0, 1: 1.0, 2:2.0, 3:4.0},
        1 : {0: 1.0, 1: 0.0, 2:2.0, 3:4.0},
        2 : {0: 2.0, 1: 2.0, 2:0.0, 3:3.0},
        3 : {0: 4.0, 1: 4.0, 2:3.0, 3:0.0}
    })
    print(tspPrDy(dist,0))
