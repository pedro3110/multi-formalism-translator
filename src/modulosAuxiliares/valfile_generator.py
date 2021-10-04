import random
from src.modulosAuxiliares.map_generator import map_generator


class valfile_generator(object):
    def __init__(self, name, dim):
        # 'n' es el identificador de cada generador (?)
        self.name = name
        self.dim = dim

    ####################
    # Access generators
    def generate(self):
        if self.name == 'opinion':
            return self.opinion_valfile_rows()
        elif self.name == 'manhattan':
            return self.manhattan_valfile_rows()
        else:
            raise Exception('Error: generador "' + self.name + '" no soportado')

    ####################
    # Valfile generators

    # Opinion
    def opinion_valfile_rows(self):
        # Aux function
        def generate_cell_value_opinion(i, j, k):
            if k == 0:
                return random.uniform(-3, 3)
            if k == 1:
                return random.randint(1, 4)
            return 0

        # Generate valfile
        ans = []
        for k in range(self.dim[2]):
            for i in range(self.dim[0]):
                for j in range(self.dim[1]):
                    cell = '(' + str(i) + ',' + str(j) + ',' + str(k) + ')'
                    value = str(generate_cell_value_opinion(i, j, k))
                    row = cell + ' = ' + value + '\n'
                    ans.append(row)
        return ans

    # Manhattan city
    def manhattan_valfile_rows(self):
        src_dir_manhattan_map = 'root/data/manhattan.png'
        rows = map_generator(self.dim, src_dir_manhattan_map).generate()
        return rows
