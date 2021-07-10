from gurobipy import Model, GRB, quicksum, GurobiError
from informacion.parametros import A, E, Q, C, K
from informacion.parser import write_latex

################
# PREGUNTA (a) #
################

modelo_a = Model('Pregunta (a)')

# *************
# * VARIABLES *
# *************

# x_ajie = x[area, categoria][alumno, escuela]
# 1 si el alumno i de la categoria j del área a es asignado a la escuela e
# en caso contrario
x = dict()
for a in A.keys():
    for j in ['inf', 'juv', 'pro']:
        x[a, j] = modelo_a.addVars(
                A[a], A[a][j], E, vtype=GRB.BINARY, name = f'x{a}'
            )

# *****************
# * RESTRICCIONES *
# *****************

# Nota: las restricciones que son todas iguales podrían ser convertidas en funciones
#       para disminuir la cantidad de lineas.

# Todos los alumnos deben ser asignados
for a in A.keys():
    for j in ['inf', 'juv', 'pro']:
        for i in A[a][j]:
            modelo_a.addConstr(
                1 == quicksum(x[a, j][j, i, e] for e in E),
                name = 'R1'
            )

# Restriccion de capacidad
for e in E:
    modelo_a.addConstr(
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
        modelo_a.addConstr(
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
        modelo_a.addConstr(
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
        modelo_a.addConstr(
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
modelo_a.setObjective(
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

modelo_a.optimize()
write_latex(modelo_a.getVars(), modelo_a.objVal)

#===============================================================================

################
# PREGUNTA (c) #
################

modelo_c = Model('Pregunta (c)')

# *************
# * VARIABLES *
# *************

# x_mjie = x[area, categoria][alumno, escuela]
# 1 si el alumno i de la categoria j del área a es asignado a la escuela e
# en caso contrario
x = dict()
for a in A.keys():
    for j in ['inf', 'juv', 'pro']:
        x[a, j] = modelo_c.addVars(
                A[a], A[a][j], E, vtype=GRB.BINARY, name = f'x{a}'
            )

# *****************
# * RESTRICCIONES *
# *****************

# Todos los alumnos deben ser asignados
for a in A.keys():
    for j in ['inf', 'juv', 'pro']:
        for i in A[a][j]:
            modelo_c.addConstr(
                1 == quicksum(x[a, j][j, i, e] for e in E),
                name = 'R1'
            )

# Restriccion de capacidad
for e in E:
    modelo_c.addConstr(
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
        modelo_c.addConstr(
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
        modelo_c.addConstr(
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
        modelo_c.addConstr(
            quicksum(
                quicksum(
                    x[a, j][j, i, e] for i in A[a][j]
                )
                for j in ['inf', 'juv', 'pro']
            ) == 0,
            name = 'R5'
        )

# Todos los alumnos de una misma zona deben ser asignados a la misma escuela
modelo_c.addConstrs(
    (
        x[a, j][j, 1, e] == x[a, j][j, i, e]        for e in E
                                                    for a in A.keys()
                                                    for j in ['inf', 'juv', 'pro']
                                                    for i in A[a][j]
    ),
    name = 'R6'
)

# ********************
# * FUNCION OBJETIVO *
# ********************
modelo_c.setObjective(
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


modelo_c.optimize()
write_latex(modelo_c.getVars(), modelo_c.objVal)

#===============================================================================

################
# PREGUNTA (d) #
################

modelo_d1 = Model('Pregunta (d) opción 1')
modelo_d2 = Model('Pregunta (d) opción 2')

# *************
# * VARIABLES *
# *************

# x_mjie = x[area, categoria][alumno, escuela]
# 1 si el alumno i de la categoria j del área a es asignado a la escuela e
# en caso contrario
x1, x2 = dict(), dict()
for a in A.keys():
    for j in ['inf', 'juv', 'pro']:
        x1[a, j] = modelo_d1.addVars(
                A[a], A[a][j], E, vtype=GRB.BINARY, name = f'x{a}'
            )

for a in A.keys():
    for j in ['inf', 'juv', 'pro']:
        x2[a, j] = modelo_d2.addVars(
                A[a], A[a][j], E, vtype=GRB.BINARY, name = f'x{a}'
            )

# *****************
# * RESTRICCIONES *
# *****************

# Todos los alumnos deben ser asignados
for a in A.keys():
    for j in ['inf', 'juv', 'pro']:
        for i in A[a][j]:
            modelo_d1.addConstr(
                1 == quicksum(x1[a, j][j, i, e] for e in E),
                name = 'R1'
            )

for a in A.keys():
    for j in ['inf', 'juv', 'pro']:
        for i in A[a][j]:
            modelo_d2.addConstr(
                1 == quicksum(x2[a, j][j, i, e] for e in E),
                name = 'R1'
            )

# Restriccion de capacidad
for e in E:
    modelo_d1.addConstr(
        quicksum(
            quicksum(
                quicksum(
                    x1[a, j][j, i, e] for i in A[a][j]
                )
                for j in ['inf', 'juv', 'pro']
            )
            for a in A.keys()
        ) <= Q[e - 1],
        name = 'R2'
    )

for e in E:
    modelo_d2.addConstr(
        quicksum(
            quicksum(
                quicksum(
                    x2[a, j][j, i, e] for i in A[a][j]
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
        modelo_d1.addConstr(
            0.3 * quicksum(
                quicksum(
                    quicksum(
                        x1[a, j_][j_, i, e] for i in A[a][j_]
                    )
                    for j_ in ['inf', 'juv', 'pro']
                )
                for a in A.keys()
            ) <= quicksum(
                quicksum(
                    x1[a, j][j, i, e] for i in A[a][j]
                )
                for a in A.keys()
            ),
            name = 'R3'
        )

for e in E:
    for j in ['inf', 'juv', 'pro']:
        modelo_d2.addConstr(
            0.3 * quicksum(
                quicksum(
                    quicksum(
                        x2[a, j_][j_, i, e] for i in A[a][j_]
                    )
                    for j_ in ['inf', 'juv', 'pro']
                )
                for a in A.keys()
            ) <= quicksum(
                quicksum(
                    x2[a, j][j, i, e] for i in A[a][j]
                )
                for a in A.keys()
            ),
            name = 'R3'
        )

# Restriccion superior de diversidad
for e in E:
    for j in ['inf', 'juv', 'pro']:
        modelo_d1.addConstr(
            0.36 * quicksum(
                quicksum(
                    quicksum(
                        x1[a, j_][j_, i, e] for i in A[a][j_]
                    )
                    for j_ in ['inf', 'juv', 'pro']
                )
                for a in A.keys()
            ) >= quicksum(
                quicksum(
                    x1[a, j][j, i, e] for i in A[a][j]
                )
                for a in A.keys()
            ),
            name = 'R4'
        )

for e in E:
    for j in ['inf', 'juv', 'pro']:
        modelo_d2.addConstr(
            0.36 * quicksum(
                quicksum(
                    quicksum(
                        x2[a, j_][j_, i, e] for i in A[a][j_]
                    )
                    for j_ in ['inf', 'juv', 'pro']
                )
                for a in A.keys()
            ) >= quicksum(
                quicksum(
                    x2[a, j][j, i, e] for i in A[a][j]
                )
                for a in A.keys()
            ),
            name = 'R4'
        )

# Asignaciones imposibles
for a in A.keys():
    for e in K[a]:
        modelo_d1.addConstr(
            quicksum(
                quicksum(
                    x1[a, j][j, i, e] for i in A[a][j]
                )
                for j in ['inf', 'juv', 'pro']
            ) == 0,
            name = 'R5'
        )

for a in A.keys():
    for e in K[a]:
        modelo_d2.addConstr(
            quicksum(
                quicksum(
                    x2[a, j][j, i, e] for i in A[a][j]
                )
                for j in ['inf', 'juv', 'pro']
            ) == 0,
            name = 'R5'
        )

# ********************
# * FUNCION OBJETIVO *
# ********************
modelo_d1.setObjective(
    quicksum(
        quicksum(
            quicksum(
                quicksum(
                    C[a][e] * x1[a, j][j, i, e] for i in A[a][j]
                )
                for j in ['inf', 'juv', 'pro']
            )
            for a in A.keys()
        )
        for e in E
    )
)

modelo_d2.setObjective(
    quicksum(
        quicksum(
            quicksum(
                quicksum(
                    C[a][e] * x2[a, j][j, i, e] for i in A[a][j]
                )
                for j in ['inf', 'juv', 'pro']
            )
            for a in A.keys()
        )
        for e in E
    )
)

modelo_d1.optimize()

modelo_d2.optimize()
#write_latex(modelo_d.getVars(), modelo_d.objVal)
