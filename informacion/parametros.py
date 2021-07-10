from informacion.parser import Parser

# Carga de Datos
parser = Parser('informacion/datos.csv')

#################
#*  CONJUNTOS  *#
#################

# A: Areas
A = dict()
for k,v in parser.areas.items():
    '''
    Genera listas de enteros desde 1 a R, donde R es la cantidad de alumnos
    de cada categoria. Las listas luego son añadidas como valores del diccionario
    A, indexadas por área geográfica (k).
    '''
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
K_i = dict()
K_ii = dict()
for k,v in parser.areas.items():
    '''
    Genera C a partir de los costos para cada tupla (área, escuela) y cuando
    no existe el costo (porque la asignación es infactible), añade esa tupla
    al conjunto K.
    '''
    # Nota: cambiar de diccionario a tupla para mejor consistencia con el modelo.
    C[k] = dict()
    K[k] = list()
    K_i[k] = list()
    K_ii[k] = list()
    try:
        C[k][1] = parser.areas[k]['cost1']
        if parser.areas[k]['cost1'] == 200:
            K_i[k].append(1)
        if 0 < parser.areas[k]['cost1'] <= 300:
            K_ii[k].append(1)
    except KeyError as e:
        C[k][1] = 0
        K[k].append(1)
    try:
        C[k][2] = parser.areas[k]['cost2']
        if parser.areas[k]['cost2'] == 200:
            K_i[k].append(2)
        if 0 < parser.areas[k]['cost2'] <= 300:
            K_ii[k].append(2)
    except KeyError as e:
        C[k][2] = 0
        K[k].append(2)
    try:
        C[k][3] = parser.areas[k]['cost3']
        if parser.areas[k]['cost3'] == 200:
            K_i[k].append(3)
        if 0 < parser.areas[k]['cost3'] <= 300:
            K_ii[k].append(3)
    except KeyError as e:
        C[k][3] = 0
        K[k].append(3)
