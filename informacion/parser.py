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
    # def generar_grupos(self):
    #     for k, v in self.areas.items():
    #         self.areas[k]['inf'] = [
    #             x for x in range(self.areas[k]['inf'] * self.areas[k]['n_est'] // 100)
    #         ]
    #         self.areas[k]['juv'] = [
    #             x for x in range(self.areas[k]['juv'] * self.areas[k]['n_est'] // 100)
    #         ]
    #         self.areas[k]['pro'] = [
    #             x for x in range(self.areas[k]['pro'] * self.areas[k]['n_est'] // 100)
    #         ]
