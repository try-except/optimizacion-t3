class Parser:
    def __init__(self, filename):
        self.read_csv(filename)

    def read_csv(self, filename):
        '''
        Lee el archivo csv y genera el diccionario self.areas, donde cada key es
        un área geográfica.
        '''
        self.areas, self.escuelas = dict(), dict()
        with open(filename, 'r+') as fh:
            next(fh) #skip the headers
            for line in fh:
                area, n_est, p_inf, p_juv, p_pro, cost1, cost2, cost3, ce1, ce2, ce3 \
                = line.strip().split(',')
                capacidades = [ce1, ce2, ce3]
                self.areas[int(area)] = {
                    'n_est': int(n_est), #numero de estudiantes del área
                    'inf': int(p_inf), # porcentaje de infantiles
                    'juv': int(p_juv), # porcentaje de juveniles
                    'pro': int(p_pro), # porcentaje de pre-profesionales
                    'cost1': cost1, # costo para la escuela 1
                    'cost2': cost2, # costo para la escuela 2
                    'cost3': cost3, # costo para la escuela 3
                }
                for key in ['cost1', 'cost2', 'cost3']:
                    # convertimos los costos a entero y de no existir, los eliminamos
                    if self.areas[int(area)][key] != 'null':
                        self.areas[int(area)][key] = int(self.areas[int(area)][key])
                    else:
                        self.areas[int(area)].pop(key)
            # Generamos las escuelas
            self.escuelas = {
                i + 1: int(capacidades[i])
                for i in range(3)
            }

def write_latex(modelo) -> str:
    '''
    Recibe el estado final de las variables y el valor objetivo, construye
    una tabla en LaTeX a partir de los datos recibidos
    '''
    ## Ordenamos los datos en un diccionario
    clean_vars = {
        j: {
            i: {
                'inf': 0,
                'juv': 0,
                'pro': 0
            }
            for i in range(1, 4)
        }
        for j in range(1, 7)
    }
    for var in modelo.getVars():
        if not var.x: continue # Solo consideramos las asignaciones hechas.
        area = int(var.varName[1])
        cat, alumno, escuela = var.varName[3:-1].split(',')
        clean_vars[area][int(escuela)][cat] += 1

    ## Escribimos el LaTeX string
    #preamble
    output_latex = '\\documentclass{standalone}\n\\usepackage[utf8]{inputenc}\n'
    output_latex += '\\usepackage[spanish]{babel}\n\\begin{document}\n'
    #tabular
    output_latex += '\\begin{tabular}{c|ccc|ccc|ccc}\n'
    #asignaciones
    output_latex += ' & \\multicolumn{3}{c}{Infantil}'
    output_latex += ' & \\multicolumn{3}{c}{Juvenil}'
    output_latex += ' & \\multicolumn{3}{c}{Pre-Profesional}\\\\\n'
    output_latex += 'Área' + ' & Escuela 1 & Escuela 2 & Escuela 3' * 3
    output_latex += '\\\\\n\\hline\n'
    for area in clean_vars.keys():
        line = f'{area}'
        for categoria in ['inf', 'juv', 'pro']:
            for escuela in [1, 2, 3]:
                line += f' & {clean_vars[area][escuela][categoria]}'
        line += '\\\\\n'
        output_latex += line
    output_latex += '\\hline\n\hline\n'
    #totales
    output_latex += '& \\multicolumn{3}{|c}{Escuela 1}'
    output_latex += '& \\multicolumn{3}{|c}{Escuela 2}'
    output_latex += '& \\multicolumn{3}{|c}{Escuela 3}\\\\\n'
    output_latex += '& Infantil & Juvenil & Pre-Profesional ' * 3
    output_latex += '\\\\\n\hline\nTotal'
    for escuela in range(1, 4):
        for categoria in ['inf', 'juv', 'pro']:
            suma = sum([clean_vars[x][escuela][categoria] for x in range(1, 7)])
            output_latex += f'& {suma} '
    #porcentajes
    output_latex += '\\\\\nPorcentaje'
    for categoria in ['inf', 'juv', 'pro']:
        for escuela in range(1, 4):
            suma = sum([clean_vars[x][escuela][categoria] for x in range(1, 7)])
            total_asignados = sum(
                [clean_vars[x][escuela][j] for x in range(1, 7) for j in ['inf', 'juv', 'pro']]
            )
            output_latex += f'& {suma / total_asignados * 100}'[:8] + '\% '
    output_latex += '\\\\\n\hline\n\hline\n'
    #valor funcion objetivo
    miles = int(modelo.objVal // 1000)
    centenas = int(modelo.objVal % 1000)
    if centenas < 100:
        centenas = str(centenas)
        centenas = '0' * ( 3 - len(centenas)) + centenas
    costo_optimo = f'{miles}\\,{centenas}'
    output_latex += f'\\multicolumn{{10}}{{c}}{{Costo total óptimo: \${costo_optimo}}}'
    output_latex += '\n\\end{tabular}\n\\end{document}'
    #print(output_latex) #cambiar output a un archivo .tex
    info_modelo = modelo.ModelName.split(' ')
    nombre_output = info_modelo[0].lower() + '_' + info_modelo[1][1]
    if len(info_modelo) > 2:
        nombre_output += '_' + info_modelo[-1]
    with open(f'output_files/{nombre_output}.tex', 'w', encoding='utf-8') as fh:
        fh.write(output_latex)
