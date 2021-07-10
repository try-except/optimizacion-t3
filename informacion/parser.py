class Parser:
    def __init__(self, filename):
        self.read_csv(filename)
        #self.generar_grupos()

    def read_csv(self, filename):
        self.areas, self.escuelas = dict(), dict()
        with open(filename, 'r+') as fh:
            next(fh) #skip the headers
            for line in fh:
                area, n_est, p_inf, p_juv, p_pro, cost1, cost2, cost3, ce1, ce2, ce3 \
                = line.strip().split(',')
                capacidades = [ce1, ce2, ce3]
                self.areas[int(area)] = {
                    'n_est': int(n_est),
                    'inf': int(p_inf),
                    'juv': int(p_juv),
                    'pro': int(p_pro),
                    'cost1': cost1,
                    'cost2': cost2,
                    'cost3': cost3,
                }
                for key in ['cost1', 'cost2', 'cost3']:
                    if self.areas[int(area)][key] != 'null':
                        self.areas[int(area)][key] = int(self.areas[int(area)][key])
                    else:
                        self.areas[int(area)].pop(key)
            # Generamos las escuelas
            self.escuelas = {
                i + 1: int(capacidades[i])
                for i in range(3)
            }

def write_latex(variables : list) -> str:
    ## Ordenamos los datos en un diccionario
    clean_vars = {
        j: {
            i: {
                'inf': 0,#list(),
                'juv': 0,#list(),
                'pro': 0,#list()
            }
            for i in range(1, 4)
        }
        for j in range(1, 7)
    }
    for var in variables:
        if not var.x: continue
        area = int(var.varName[1])
        cat, alumno, escuela = var.varName[3:-1].split(',')
        #clean_vars[area][int(escuela)][cat].append(alumno)
        clean_vars[area][int(escuela)][cat] += 1
        
    ## Escribimos el LaTeX string
    output_latex = '\\documentclass{standalone}\n\\usepackage[utf8]{inputenc}'
    output_latex += '\\begin{document}\n'
    #output_latex += '\\begin{table}\n\\centering\n'
    output_latex += '\\begin{tabular}{c|ccc|ccc|ccc}\n'
    output_latex += ' & \\multicolumn{3}{c}{Infantil}'
    output_latex += ' & \\multicolumn{3}{c}{Juvenil}'
    output_latex += ' & \\multicolumn{3}{c}{Pre-Profesional}\\\\\n'
    output_latex += 'Área & ' + 'Escuela 1 & Escuela 2 & Escuela 3 & ' * 3
    output_latex = output_latex[:-2] + '\\\\\n'
    output_latex += '\\hline\n'
    for area in clean_vars.keys():
        line = f'{area} &'
        for categoria in ['inf', 'juv', 'pro']:
            for escuela in [1, 2, 3]:
                line += f' {clean_vars[area][escuela][categoria]} &'
        line = line[:-2] + '\\\\\n'
        output_latex += line
    output_latex += '\\end{tabular}\n'
    #latex_string += f'\\caption{{Asignaciones para el área {area}}}\n'
    #output_latex += '\\end{table}\n'
    output_latex += '\\end{document}'
    print(output_latex)
