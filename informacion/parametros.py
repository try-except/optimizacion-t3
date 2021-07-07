from informacion.parser import Parser

# Carga de Datos
parser = Parser('informacion/datos.csv')

#################
#*  CONJUNTOS  *#
#################

# A: Areas
A = dict()
for k,v in parser.areas.items():
    A[f'{k}_inf'] = [i for i in range(1, v[f'{k}_inf'] + 1)]
    A[f'{k}_juv'] = [i for i in range(1, v[f'{k}_juv'] + 1)]
    A[f'{k}_pro'] = [i for i in range(1, v[f'{k}_pro'] + 1)]

#B: Escuelas
B = list(parser.escuelas.keys())

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
