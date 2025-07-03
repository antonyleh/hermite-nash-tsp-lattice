import pulp
from pulp import LpVariable, LpProblem, LpMinimize, LpStatus, lpSum, value

##Code pour résoudre tsp via un problème d'optimisation linéaire


# Pour visualiser une variable x_i_j

def var(i,j):
    return "x_"+str(i)+","+str(j)  

# Pour créer les variables du problème

def create_variables_x(n):
    x=[n*[None] for i in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            x[i][j]=LpVariable( var(i,j), cat="Binary") #valeur soit 0 soit 1
            x[j][i]=LpVariable( var(j,i), cat="Binary")

    return x

def create_variables_u(n,origin):
    l="u_"
    max_cap = n-1
    u=[None for i in range(n)]
    for i in range(0,n):
        if i!=origin:
            u[i] = LpVariable(name=l+str(i), lowBound=1, upBound=max_cap, cat="Integer")


    return u
        
# Pour créer la fonction objectif (fonction à minimiser)

def add_objective_func(problem,n,distances,x_var):
    T = []
    for i in range(n):
        for j in range(i+1,n):
            T.append(distances[i][j]*x_var[i][j])
            T.append(distances[j][i]*x_var[j][i])

    problem += lpSum(T)
    return problem

#déclaration des contraintes

def add_basic_constraints(problem,n,x_var):
    for i in range(n):
        T_1 = []
        T_2 = []
        for j in range(n):
            if i!=j:
                T_1.append(1*x_var[i][j])
                T_2.append(1*x_var[j][i])

        problem += (lpSum(T_1) == 1)
        problem += (lpSum(T_2) == 1)

    return problem

def add_special_constraints(problem,n,origin,x_var,u_var):
    for i in range(n):
        if i!=origin:
            for j in range(n):
                if j!=origin and j!=i:
                    temp = lpSum([1*u_var[i],(-1)*u_var[j],(n-1)*x_var[i][j]])
                    problem += ( temp <= (n-2))

    return problem

# Définition du problème TSP sous forme ILP

def tsp_ilp_solver(origin,distances):
    n=len(distances)
    x_var=create_variables_x(n)
    u_var=create_variables_u(n,origin)
    problem=LpProblem("TSP_ILP",LpMinimize)
    problem=add_objective_func(problem,n,distances, x_var)
    problem=add_basic_constraints(problem,n,x_var)
    problem=add_special_constraints(problem,n,origin,x_var,u_var)
    solver = pulp.PULP_CBC_CMD(msg=False)
    problem.solve(solver)
    print("Status:", LpStatus[problem.status])
    
    path=[None]*(n+1)
    path[0]=origin
    step=origin
    for i in range(0,n+1):
        path[i]=step
        for j in range(0,n):
            if j!=step and (value(x_var[step][j]) == 1):
              step = j
              break

    return (value(problem.objective), path)




