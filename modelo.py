from gurobipy import Model, GRB, quicksum, GurobiError
from informacion.parametros import A, E, Q, C, K

modelo = Model('AldeaMatematica')

# *************
# * VARIABLES *
# *************

# x_mjie = x[area, categoria][alumno, escuela]
# 1 si el alumno i de la categoria j del área m es asignado a la escuela e
# en caso contrario
x = dict()
for m in A.keys():
    for j in ['inf', 'juv', 'pro']:
        # for i in A[m][j]:
        # print(len(A[m][j]))
        x[m, j] = modelo.addVars(
                A[m], A[m][j], E, vtype=GRB.BINARY, name = 'x'
            )

# *****************
# * RESTRICCIONES *
# *****************

# Todos los alumnos deben ser asignados
for m in A.keys():
    for j in ['inf', 'juv', 'pro']:
        for i in A[m][j]:
            modelo.addConstr(
                1 == quicksum(x[m, j][j, i, e] for e in E),
                name = 'R1'
            )

# Restriccion de capacidad
for e in E:
    modelo.addConstr(
        quicksum(
            quicksum(
                quicksum(
                    x[m, j][j, i, e] for i in A[m][j]
                )
                for j in ['inf', 'juv', 'pro']
            )
            for m in A.keys()
        ) <= Q[e - 1],
        name = 'R2'
    )

# Restriccion inferior de diversidad
for e in E:
    for j in ['inf', 'juv', 'pro']:
        modelo.addConstr(
            0.3 * quicksum(
                quicksum(
                    quicksum(
                        x[m, j_][j_, i, e] for i in A[m][j_]
                    )
                    for j_ in ['inf', 'juv', 'pro']
                )
                for m in A.keys()
            ) <= quicksum(
                quicksum(
                    x[m, j][j, i, e] for i in A[m][j]
                )
                for m in A.keys()
            ),
            name = 'R3'
        )

# Restriccion superior de diversidad
for e in E:
    for j in ['inf', 'juv', 'pro']:
        modelo.addConstr(
            0.36 * quicksum(
                quicksum(
                    quicksum(
                        x[m, j_][j_, i, e] for i in A[m][j_]
                    )
                    for j_ in ['inf', 'juv', 'pro']
                )
                for m in A.keys()
            ) >= quicksum(
                quicksum(
                    x[m, j][j, i, e] for i in A[m][j]
                )
                for m in A.keys()
            ),
            name = 'R4'
        )

# Asignaciones imposibles
for m in A.keys():
    for e in K[m]:
        modelo.addConstr(
            quicksum(
                quicksum(
                    x[m, j][j, i, e] for i in A[m][j]
                )
                for j in ['inf', 'juv', 'pro']
            ) == 0,
            name = 'R5'
        )

# ********************
# * FUNCION OBJETIVO *
# ********************
#print(C)
modelo.setObjective(
    quicksum(
        quicksum(
            quicksum(
                quicksum(
                    C[m][e] * x[m, j][j, i, e] for i in A[m][j]
                )
                for j in ['inf', 'juv', 'pro']
            )
            for m in A.keys()
        )
        for e in E
    )
)

modelo.optimize()
for variable in modelo.getVars():
    if variable.x:
        print(variable.varName, variable.x)
