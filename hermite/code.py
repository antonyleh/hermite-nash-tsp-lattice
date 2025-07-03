import numpy as np
import random

dataType = object
# question 1

def xyFromGCD(a,b):
    k,l = abs(a),abs(b)
    echange = k<l
    if echange:
        k,l = l,k
     
    u0,v0,a0 = 1,0,k
    u1,v1,a1 = 0,1,l
    
    temp1,temp2 = 0,0
    while a1 > 0:
        r = a0%a1
        q = a0//a1
        temp1,temp2 = u0-(u1*q),v0-(v1*q)
        u0,v0,a0 = u1,v1,a1
        u1,v1,a1 = temp1,temp2,r
     
    if echange :
        u0,v0 = v0,u0
    
    if a < 0:
        u0=-u0
    if b < 0:
        v0=-v0
    
    return u0,v0,a0


# question 2

def createU(A):
    return np.identity(n=A.shape[1],dtype=dataType)


# question 3

def cancelij(A,U,i,j):
    if i>=j:
        return
    m,n = A.shape
    a = A[i,i]
    b = A[i,j]
    x,y,g = xyFromGCD(a,b)
    q_a = a//g
    q_b = b//g
    for k in range(m):
        temp = A[k,i]
        A[k,i] = (A[k,i]*x) + (A[k,j]*y)
        A[k,j] = (temp*(-q_b)) + (A[k,j]*q_a)
    for k in range(n):
        temp_U = U[k,i]
        U[k,i] = (U[k,i]*x) + (U[k,j]*y)
        U[k,j] = (temp_U*(-q_b)) + (U[k,j]*q_a)


# question 4

def minus_one(A,U,j):
    m,n = A.shape  
    for k in range(m):
        A[k,j] = -A[k,j]
    for l in range(n):
        U[l,j] = -U[l,j]

# question 5

def substractji(A,U,j,i):
    if i<=j:
        return
        
    m,n = A.shape
    q = A[i,j]//A[i,i]
    for k in range(m):
        A[k,j] = A[k,j] + (A[k,i]*(-q))
        
    for k in range(n):
        U[k,j] = U[k,j] + (U[k,i]*(-q))
        
# question 6

def getHNF(A):
    m,n = A.shape
    H = np.array(A,dtype=dataType)
    U = createU(A)
    for i in range(m):
        for j in range(i+1,n):
            if H[i,i]!=0 or H[i,j]!=0 :
                cancelij(H,U,i,j)
        if H[i,i] < 0 :
            minus_one(H,U,i)
        for j in range(0,i):
            substractji(H,U,j,i)

    return H,U



# question 7

def intSolverByHermite(A,b):
    m,n = A.shape
    H,U = getHNF(A)
    x = np.array([0]*n,dtype=dataType)
    for i in range(m):
        v=0
        for j in range(i):
            v=v+(H[i,j]*x[j])
        v = b[i]-v
        if v % H[i,i] != 0 :
            return None,None
        x[i]=v//H[i,i]
    return x, U.dot(x)



def matrix_generator(m,n,lim):
    r = np.zeros((m,n),dtype=dataType)
    for i in range(m):
        for j in range(n):
            r[i,j]=random.randint(-lim,lim)
    return r


def genVector(n,b):
    v = np.zeros(n,dtype=dataType)
    for i in range(n):
        v[i] = random.randint(-b,b)
    return v
