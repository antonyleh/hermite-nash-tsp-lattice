from code import *


#on importe de code la variable dataType qui vaut object

##test forme normale de Hermite

print('Test calcul forme normale de Hermite\n')

print('Test sur la matrice A suivante:')
L = [[2,3,4],[2,4,6]]
A = np.array(L,dtype=dataType)
print(A)
print("\n")

H,U = getHNF(A)

print('Matrice H obtenue:')
print(H)
print("\n")

print('Matrice U obtenue:')
print(U)
print("\n")

print('Produit AU obtenu:')
print(A.dot(U))


##test solver forme normale de Hermite
print("\n\n")
print('Test int-solver Ax=b par forme normale de Hermite\n')

print('Test sur la matrice A suivante:')
L = [[2,3,4],[2,4,6]]
A = np.array(L,dtype=dataType)
print(A)

print("\n")
print('et sur le vecteur b suivant:')
l = [3,4]
b=np.array(l,dtype=dataType)
print(b)

y,u_y = intSolverByHermite(A,b)

print("\n")
print('Une solution y à Hy=b:')
print(y)
print("\n")

print('Une solution z à Az = b via Hermite (z=U.y):')
print(u_y)
print("\n")

print('Produit Az obtenu:')
print(A.dot(u_y))



###############################################################################

##test forme normale de Hermite (matrice grande taille)
print('\nTest calcul forme normale de Hermite H=AU (matrice grande taille) \n')

lim = 50 # les entiers des arrays considérés varient dans [-lim,lim]
m=30 #au dela de 30x30 les calculs deviennent vraiment longs
n=m

print(f"Test sur une matrice A de taille {m}x{n} \n")
A=matrix_generator(m,n,lim)


H,U = getHNF(A)
verite = (A.dot(U) == H).all()
print(f"Est-ce que H = AU?: {verite} \n")


##test solver forme normale de Hermite (matrice grande taille)
print('\nTest int-solver Ax=b par forme normale de Hermite (matrice grande taille)\n')

print(f"Test sur une matrice A de taille {m}x{n} \n")
print(f"et un vecteur b de taille {m} \n")


b = genVector(m,lim)
    
y,u_y = intSolverByHermite(A,b)

if type(u_y) == type(None):
    print("Aucune solution x")
else:
    print("Une solution z a été calculée\n")
    temp = (A.dot(u_y) == b).all()
    print(f"Est-ce que Ax=b?: {temp} \n")
    
