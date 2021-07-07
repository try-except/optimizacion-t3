from gurobipy import Model, GRB, quicksum, GurobiError
from informacion.parametros import A, B, Q, C, K


#print(A)
#print(B)
modelo = Model('AldeaMatematica')

# x_kab: x[subarea][numero, escuela]
# 1 si el alumno a del subarea k es asignado
# a la escuela b
# 0 en caso contrario
x = {k: modelo.addVars(A[k], B, vtype=GRB.BINARY, name='x')     for k in A.keys()}
print('C =', C)

# Todos los alumnos deben ser asignados
modelo.addConstrs(
    (1 == quicksum(quicksum(x[k][a, b] for b in B) for a in A[k])
                                                                for k in A.keys()
    ),
    name = 'R1'
)
# Restriccion de diversidad 1 #CREO QUE FALLAN LAS DE DIVERSIDAD !!!!
modelo.addConstrs(
    (quicksum(quicksum(x[k][a, b] for a in A[k]) for k in A.keys()) * 0.3 <= \
    quicksum(x[k][a, b] for a in A[k])                          for k in A.keys()
                                                                for b in B
    ),
    name = 'R2'
)
# Restriccion de diversidad 2
modelo.addConstrs(
    (quicksum(quicksum(x[k][a, b] for a in A[k]) for k in A.keys()) * 0.36 >= \
    quicksum(x[k][a, b] for a in A[k])                          for k in A.keys()
                                                                for b in B
    ),
    name = 'R3'
)
# Restriccion de capacidad
modelo.addConstrs(
    (quicksum(quicksum(x[k][a, b] for a in A[k]) for k in A.keys()) <= Q[b - 1]
                                                                for b in B
    ),
    name = 'R4'
)
# Asignaciones imposibles
modelo.addConstrs(
    (0 == quicksum(quicksum(x[k][a, b] for a in A[k]) for b in K.get(int(k[0]), list()))
                                                    for k in A.keys()
    ),
    name = 'R5'
)


modelo.setObjective(
    quicksum(
        quicksum(
            quicksum(
                C[int(k[0])][b] * x[k][a, b] for a in A[k]
            )
            for b in B
        )
        for k in A.keys()
    ),
    GRB.MINIMIZE
)

modelo.optimize()
