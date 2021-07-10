from gurobipy import Model, GRB, quicksum, GurobiError
from informacion.parametros import A, E, Q, C, K
from informacion.parser import write_latex

modelo = Model('AldeaMatematica')

# *************
# * VARIABLES *
# *************

# x_mjie = x[area, categoria][alumno, escuela]
# 1 si el alumno i de la categoria j del área a es asignado a la escuela e
# en caso contrario
x = dict()
for a in A.keys():
    for j in ['inf', 'juv', 'pro']:
        # for i in A[a][j]:
        # print(len(A[a][j]))
        x[a, j] = modelo.addVars(
                A[a], A[a][j], E, vtype=GRB.BINARY, name = f'x{a}'
            )

# *****************
# * RESTRICCIONES *
# *****************

# Todos los alumnos deben ser asignados
for a in A.keys():
    for j in ['inf', 'juv', 'pro']:
        for i in A[a][j]:
            modelo.addConstr(
                1 == quicksum(x[a, j][j, i, e] for e in E),
                name = 'R1'
            )

# Restriccion de capacidad
for e in E:
    modelo.addConstr(
        quicksum(
            quicksum(
                quicksum(
                    x[a, j][j, i, e] for i in A[a][j]
                )
                for j in ['inf', 'juv', 'pro']
            )
            for a in A.keys()
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
                        x[a, j_][j_, i, e] for i in A[a][j_]
                    )
                    for j_ in ['inf', 'juv', 'pro']
                )
                for a in A.keys()
            ) <= quicksum(
                quicksum(
                    x[a, j][j, i, e] for i in A[a][j]
                )
                for a in A.keys()
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
                        x[a, j_][j_, i, e] for i in A[a][j_]
                    )
                    for j_ in ['inf', 'juv', 'pro']
                )
                for a in A.keys()
            ) >= quicksum(
                quicksum(
                    x[a, j][j, i, e] for i in A[a][j]
                )
                for a in A.keys()
            ),
            name = 'R4'
        )

# Asignaciones imposibles
for a in A.keys():
    for e in K[a]:
        modelo.addConstr(
            quicksum(
                quicksum(
                    x[a, j][j, i, e] for i in A[a][j]
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
                    C[a][e] * x[a, j][j, i, e] for i in A[a][j]
                )
                for j in ['inf', 'juv', 'pro']
            )
            for a in A.keys()
        )
        for e in E
    )
)

modelo.optimize()
# for variable in modelo.getVars():
#     if variable.x:
#         print(variable.varName, variable.x)
write_latex(modelo.getVars())
