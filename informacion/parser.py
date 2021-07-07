class Parser:
    def __init__(self, filename):
        self.read_csv(filename)
        self.separar_areas()

    def read_csv(self, filename):
        self.areas = dict()
        self.escuelas = dict()
        with open(filename, 'r+') as fh:
            next(fh)
            for line in fh:
                area, n_est, p_inf, p_juv, p_pro, cost1, cost2, cost3, ce1, ce2, ce3 \
                = line.strip().split(',')
                capacidades = [ce1, ce2, ce3]
                self.areas[int(area)] = {
                    'n_est': int(n_est),
                    'p_inf': int(p_inf),
                    'p_juv': int(p_juv),
                    'p_pro': int(p_pro),
                    'cost1': cost1,
                    'cost2': cost2,
                    'cost3': cost3,
                }
                for key in ['cost1', 'cost2', 'cost3']:
                    if self.areas[int(area)][key] != 'null':
                        self.areas[int(area)][key] = int(self.areas[int(area)][key])
                    else:
                        self.areas[int(area)].pop(key)
                self.escuelas = {
                    i + 1: int(capacidades[i])
                    for i in range(3)
                }

    def separar_areas(self):
        nuevas_areas = {i: dict() for i in range(1, 7)}
        for k,v in self.areas.items():
            nuevas_areas[k][f'{k}_inf'] = v['p_inf'] * v['n_est'] // 100
            nuevas_areas[k][f'{k}_juv'] = v['p_juv'] * v['n_est'] // 100
            nuevas_areas[k][f'{k}_pro'] = v['p_pro'] * v['n_est'] // 100
            try:
                nuevas_areas[k]['cost1'] = v['cost1']
            except KeyError as e:
                pass
            try:
                nuevas_areas[k]['cost2'] = v['cost2']
            except KeyError as e:
                pass
            try:
                nuevas_areas[k]['cost3'] = v['cost3']
            except KeyError as e:
                pass
        self.areas = nuevas_areas
        #print(self.areas)

if __name__ == '__main__':
    Parser('datos.csv')
