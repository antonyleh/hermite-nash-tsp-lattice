from code import *
from numpy.linalg import solve

#test consistant à générer une base B et une matrice U unimodulaire
#de même dimension n, ainsi qu'un vecteur v afin d'essayer d'approcher
#la distance (euclidienne) entre le vecteur v et le réseau engendré
#par B. Par unimodularité, B et BU engendrent le même réseau. De plus,
#par l'algorithme LLL, B (resp. BU) et sa base réduite B_1 (resp. B_2)
#engendrent le même réseau.

#Plus exactement, pour chacune des bases évoquées (ie B, B_1, BU, B_2)
#on va calculer une approximation d'un vecteur w du réseau le plus proche à v
#et on calculera la distance entre v et w (i.e norme 2 de v-w )
#La fonction test_LLL permettra d'exécuter le test avec les paramètres transmis
#et affichera pour chaque base la distance entre v et w


def test_LLL(n,d,a,b1,b2):
    #section où les paramètres n,d,a,b1,b2 sont utilisés
    
    B = genUniformBasis(n,d)
    U = genUniModMatrix(n,a,b1)
    BU = B.dot(U)
    B_1, Bo_1, M_1 = reduce(B)
    B_2, Bo_2, M_2 = reduce(BU)
    v = genVector(n,b2)
    
    
    #calcul des approximations pour chaque base
    #et de leur distance à v
    
    matrices = [B,B_1,BU,B_2]
    name_mat = ["B         ","B_reduced ","BU        ","BU_reduced"]
    
    results, distances = [], []
    
    for A in matrices:
        w = A @ approxByIntegers(A,v)
        results.append(w)
        norm_sqr = getNorm_sqr(v - w)
        distances.append(math.sqrt(norm_sqr))

    #Affichage des distances calculées
    print("Tableau des distances entre w calculé et v:\n")
    for i in range(len(matrices)):
        print(name_mat[i]," : ",distances[i],"\n")


if __name__ == "__main__":
    #paramètres
    n = 100
    d = 100
    a = 10000
    b1 = 1
    b2 = 100

    test_LLL(n,d,a,b1,b2)
   
    
#Conclusion des tests effectués:
#Le caractère aléatoire du choix de U fait qu'on n'est pas
#surpris que l'approximation déduite de BU puisse être mauvaise
#par rapport à celle déduite de B (surtout si U possède de grands entiers).
#L'effet de la réduction sur B et BU n'amène pas à des résultats très concluants
#puisqu'en fonction de B et BU, l'approximation w obtenue de leur réduction
#peut être parfois plus mauvaise et parfois vraiment meilleur. On en déduit
#qu'une façon d'obtenir une bonne approximation pour une base B et un vecteur
#v donnés, c'est de faire le même test qu'avant mais on génère plusieurs U 
#au lieu d'un, et on calcule plusieurs approximations pour chaque base pour
#choisir la meilleure (cependant, cette méthode semble clairement coûteuse)

