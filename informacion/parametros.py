from informacion.parser import Parser

# Carga de Datos
parser = Parser('informacion/datos.csv')

#################
#*  CONJUNTOS  *#
#################

# A: Areas
A = dict()
for k,v in parser.areas.items():
    A[k] = dict()
    # Infantiles
    A[k]['inf'] = [
        x for x in range(
            1, 1 + parser.areas[k]['inf'] * parser.areas[k]['n_est'] // 100
        )
    ]
    # Juveniles
    A[k]['juv'] = [
        x for x in range(
            1, 1 + parser.areas[k]['juv'] * parser.areas[k]['n_est'] // 100
        )
    ]
    # Preprofesionales
    A[k]['pro'] = [
        x for x in range(
            1, 1 + parser.areas[k]['pro'] * parser.areas[k]['n_est'] // 100
        )
    ]

#E: Escuelas
E = list(parser.escuelas.keys())

#Q: Capacidades
Q = list(parser.escuelas.values())

# C: Costos
# K: Duplas infactibles
C = dict()
K = dict()
for k,v in parser.areas.items():
    C[k] = dict()
    K[k] = list()
    try:
        C[k][1] = parser.areas[k]['cost1']
    except KeyError as e:
        C[k][1] = 0
        K[k].append(1)
    try:
        C[k][2] = parser.areas[k]['cost2']
    except KeyError as e:
        C[k][2] = 0
        K[k].append(2)
    try:
        C[k][3] = parser.areas[k]['cost3']
    except KeyError as e:
        C[k][3] = 0
        K[k].append(3)
