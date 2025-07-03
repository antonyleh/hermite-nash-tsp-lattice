import numpy as np
import math
import random as rd


data_type = object


# Engendre une base de R^n où chaque coefficient
# est entier et est généré selon une loi uniforme sur [-d,d]
def genUniformBasis(n,d):
    B = np.zeros((n,n),dtype=data_type)
    for i in range(n):
        for j in range(n):
            B[i,j] = rd.randint(-d,d)

    return B


# Intervertit les colonnes j et k de B
# mais seulement les lim premiers éléments
def switchColumns(B,j,k,lim):
    temp = 0
    for i in range(lim):
        temp = B[i,j]
        B[i,j] =  B[i,k]
        B[i,k] = temp


# change le signe de la colonne j de B
def changeColumnSign(B,j):
    B[:,j] = -B[:,j]

# ajoute à la colonne i (de B) k fois la colonne j
def add_k_timesColumn(B,i,j,k):
    B[:,i] = B[:,i] + (k*B[:,j])

# procédure 0 qui intervertit deux colonnes au hasard
# pop correspond l'ensemble des indices de colonne que l'on veut considérer
def procedure_0(B,pop):
    elts = rd.sample(pop,2)
    j = elts[0]
    k = elts[1]
    switchColumns(B,j,k,B.shape[0])

# procédure 1 qui change au hasard le signe d'une colonne
def procedure_1(B,pop):
    j = rd.sample(pop,1)[0]
    changeColumnSign(B,j)

# procédure 2 qui pour deux colonnes i et j choisies au hasard
# ajoute k fois la colonne j à la colonne i où k est un entier
# choisi au hasard entre -b et b
def procedure_2(B,pop,b):
    elts = rd.sample(pop,2)
    i = elts[0]
    j = elts[1]
    k = rd.randint(-b,b)
    add_k_timesColumn(B,i,j,k)


# engendre une matrice unimodulaire de dimension n
def genUniModMatrix(n,a,b):
    U = np.eye(n,dtype=data_type)
    pop = range(n)
    for i in range(a):
        v = rd.randint(0,2)
        if v == 0:
            procedure_0(U,pop)
        elif v==1:
            procedure_1(U,pop)
        else :
            procedure_2(U,pop,b)

    return U


# engendre un vecteur de dimension n composé d'entiers
# choisis uniformément entre -b et b
def genVector(n,b):
    v = np.zeros(n,dtype=data_type)
    for i in range(n):
        v[i] = rd.randint(-b,b)
    return v

##########################################################################################

# Cette partie produit les fonctions nécessaires pour
# pour faire l'algorithme LLL qui sera la fonction reduce

data_type2 = object

# intervertit les lim 1ers éléments des colonnes j et j+1
def switchSbSColumns(B,j,lim):
    return switchColumns(B,j,j+1,lim)

# norme au carré de b
def getNorm_sqr(b):
    return np.dot(b,b)

# orthogonalisation de Gram-Schmidt optimisée                
def GSO_opt(B,Bo,M,j):
    m = B.shape[0]
    b_j_star_norm_sqr =  getNorm_sqr(Bo[:,j])
    b_jplusun_star_norm_sqr = getNorm_sqr(Bo[:,j+1])
    innProd = M[j,j+1]*b_j_star_norm_sqr
    new_bj_star_norm_sqr = b_jplusun_star_norm_sqr + (M[j,j+1]*innProd)
    new_mu_j_jplusun = innProd/new_bj_star_norm_sqr

    #la matrice A est la représentation des nouveaux vecteurs (b_j)*
    #et (b_{j+1})* dans la base des anciens vecteurs (b_j)* et
    #(b_{j+1})* qui constituent les colonnes j et j+1
    #de la matrice Bo pour le moment 
    b = b_jplusun_star_norm_sqr/new_bj_star_norm_sqr
    d = -new_mu_j_jplusun
    A = np.array([[M[j,j+1],b],[1,d]],dtype=data_type2)
    
    # les nouveaux vecteurs (b_j)* et (b_{j+1})*
    Bo[:,j:(j+2)] = Bo[:,j:(j+2)].dot(A)


    #coefs est la représentation des anciens vecteurs (b_j)* et (b_{j+1})*
    #dans la base des nouveaux vecteurs (b_j)* et (b_{j+1})*
    coefs = np.array(A,dtype=data_type2)
    det = (A[0,0]*A[1,1]) - (A[1,0]*A[0,1])
    coefs[0,0]=A[1,1]
    coefs[1,1]=A[0,0]
    coefs[1,0]=-A[1,0]
    coefs[0,1]=-A[0,1]
    coefs = (1/det) * coefs

    
    #modification de la matrice M
    switchSbSColumns(M,j,j-1)
    M[j,j+1] = new_mu_j_jplusun
    for k in range(j+2,m):
        M[j:(j+2),k] = np.dot(coefs, M[j:(j+2),k])

        
    #modification de la matrice B
    switchSbSColumns(B,j,m)


# orthogonalisation de Gram-Schmidt
def GSO(B):
    m = B.shape[0]
    Bo = np.array(B,dtype=data_type2)
    M = np.eye(m,dtype=data_type2)
    
    for j in range(m):
        for k in range(j):
            M[k,j] = np.dot(B[:,j],Bo[:,k])/getNorm_sqr(Bo[:,k])
            Bo[:,j] = Bo[:,j] - (M[k,j] * Bo[:,k])

    return Bo, M

# trouve l'entier le plus proche du float/int mu
def nearestInt(mu):
    result = math.floor(mu)
    if mu - result > 0.5:
        result = result + 1
    return result

# normalise une décomposition eue par Gram-Schmidt
def normalize(B,M):
    m = B.shape[0]
    for j in range(1,m):
        for i in range(j-1,-1,-1):
            if abs(M[i,j]) > 1/2 :
                nu = nearestInt(M[i,j])
                M[0:i+1,j] = M[0:i+1,j] - (nu*M[0:i+1,i])
                B[:,j] = B[:,j] - (nu*B[:,i])


# retourne vrai si ça vérifie la condition nécessitant de re-orthogonaliser
def condition(Bo,M,j):
    new_bj_star = Bo[:,j+1] + (M[j,j+1]*Bo[:,j])
    return getNorm_sqr(new_bj_star) < 0.75 * getNorm_sqr(Bo[:,j])

# algorithme LLL
def reduce(B):
    m,n = B.shape
    assert(n==m)
    Bo,M = GSO(B)
    B_ = np.array(B,dtype=data_type) 
    while True:
        normalize(B_,M)
        j=None
        for k in range(m-1):
            if condition(Bo,M,k) :
                j = k
                break
        if j==None:
            return B_,Bo,M
        else:
            GSO_opt(B_,Bo,M,j)


##############################################################################


#méthode d'élimination de Gauss pour résoudre Ax=b

def find_pivot(A,p,j):
    candidates = A[p:, j]
    max_v = 0
    pos = 0
    for j in range(len(candidates)):
        temp = abs(candidates[j])
        if max_v < temp:
            pos = j
            max_v = temp
    return p+pos

#on présumera que A est une matrice inversible
def gauss_elimination(A, b):
    r = -1
    M = np.c_[A,b]
    n,m = M.shape
    
    for j in range(min(n,m)):
        k = find_pivot(M,r+1,j)
        if M[k,j] != 0:
            r = r+1
            M[k]=M[k]/M[k,j]


            if k!=r:
                temp = M[k].copy()
                M[k] = M[r]
                M[r] = temp
            
            for i in range(n):
                if i!=r:
                    M[i] = M[i] - (M[i,j]*M[r])
        

    
    return M[:,-1]


#calcule z solution de Az=v puis chaque coefficient est
#remplacé par son entier le plus proche et le vecteur d'entiers
#obtenu est retourné
def approxByIntegers(A,v):
    n = len(v)
    z = gauss_elimination(A,v) #résolution de Az = v
    x = np.zeros(n,dtype=data_type)
    for j in range(n):
        x[j] = nearestInt(z[j])
    return x


