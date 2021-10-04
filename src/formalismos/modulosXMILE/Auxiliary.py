from src.modulosAuxiliares.Equation import Equation


class Aux:
    def __init__(self, aux_element, source_xmlns, parent, sim_specs, dimensions_global, debug):
        self.debug = debug
        self.parent = parent
        self.sim_specs = {k:v for k,v in sim_specs.items()} # paso de defaultdict a dict comun
        self.dimensions_global = dimensions_global
        self.dimensions_local = {}
        self.source_xmlns = source_xmlns
        self.aux_element = aux_element
        self.name = self.set_name()
        self.access = self.set_access()
        self.subscript = self.set_subscript()
        self.non_negative = self.get_non_negative()
        self.special_behavior = None
        self.equation = None
        self.parse_equation()

    def __repr__(self):
        return str({
            'parent': self.parent,
            'name': self.name,
            'equation': self.equation,
            'access': self.access,
            'special_behavior': self.special_behavior,
            'non_negative': self.non_negative
        })

    def __str__(self):
        return str({
            'parent': self.parent,
            'name': self.name,
            'equation': self.equation,
            'access': self.access,
            'special_behavior': self.special_behavior,
            'non_negative': self.non_negative
        })

    def get_special_behavior(self):
        return self.special_behavior

    def get_parent(self):
        return self.parent

    def set_name(self):
        name = self.aux_element.get('name')
        if name is None:
            raise Exception('Error: todos los auxs deben tener nombre')
        return name

    def get_name(self):
        return self.name

    def set_subscript(self):
        subscript = self.aux_element.get('subscript')
        return subscript

    def get_subscript(self):
        return self.subscript

    def parse_equation(self):
        # Graphical function
        res = {}
        gf = self.aux_element.find(self.source_xmlns + 'gf')
        elements = self.aux_element.findall(self.source_xmlns + 'element')
        equation = self.aux_element.find(self.source_xmlns + 'eqn')
        dimensions_local = self.aux_element.find(self.source_xmlns + 'dimensions')

        # Obtengo la posicion dentro del array de cada dimension, gracias a la dimensions_global, que viene por parametro
        if dimensions_local is not None:
            for index,d in enumerate(dimensions_local):
                self.dimensions_local[d.get('name')] = index
            # NOTA: Actualizo la dimensiosn_global antes de pasarla por parametro al resto de los Aux's
            # ATENCION! (TODO) : requiere que DEVSArrayAgregator tengan info de las dimensiones de los array's que consume
            # TODO: en principio, asumimos que la funcion solo agarra datos de un unico array
            # TODO: probar mandar a un ArrayAgregator datos de dos arrays distintos para evaluar su funcion?
            for d in self.dimensions_global:
                d['position'] = self.dimensions_local[d['name']]

        #####################
        # Deteccion de arrays
        if self.dimensions_global != [] and elements != []:
            res['array'] = {
                'dimensions': self.dimensions_global,
                'elements': [],
                'sim_specs': self.sim_specs
            }
            if equation is not None:
                res['array']['equation'] = equation.text
                self.equation = Equation(equation.text, self.sim_specs, self.dimensions_global, self.name, self.debug)
                
            # Parseo cada elemento => va a ser un atomico devs
            for element in elements:
                new_elem = {
                    'subscript': element.get('subscript').replace(' ', ''),
                    'name': self.name + '_' + element.get('subscript').replace(' ', '').replace(',','_')
                }
                # Considero funcion global para este elemento del array
                if equation is not None:
                    new_elem['equation'] = equation.text
                if element.find(self.source_xmlns + 'eqn') is not None:
                    new_elem['equation'] = element.find(self.source_xmlns + 'eqn').text

                # Considero funciones graficas
                if element.find(self.source_xmlns + 'gf/') is not None:
                    new_elem['gf'] = {
                        'xscale': {
                            'min': element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'xscale').get('min'),
                            'max': element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'xscale').get('max')
                        },
                        'yscale': {
                            'min': element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'yscale').get('min'),
                            'max': element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'yscale').get('max')
                        },
                        'ypts': element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'ypts').text
                    }
                                      
                    # NOTA: Agrego ecuacion particular para esta funcion, si fue seteada
                    if element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'eqn') is not None:
                        new_elem['gf']['equation'] = element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'eqn').text
                    else:
                        new_elem['gf']['equation'] = new_elem['equation']
                
                res['array']['elements'].append(new_elem)
            
        #####################
        # Deteccion de graphical functions
        elif gf is not None:
            xscale = self.aux_element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'xscale')
            yscale = self.aux_element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'yscale')
            ypts = self.aux_element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'ypts')
            res['gf'] = {
                'xscale': {'min': xscale.get('min'), 'max': xscale.get('max')},
                'yscale': {'min': yscale.get('min'), 'max': yscale.get('max')},
                'ypts': ypts.text
            }
            self.equation = Equation(equation.text, self.sim_specs, self.dimensions_global, self.name, self.debug)
        #####################
        # Deteccion de ecuacion normal o agregaciones SUM(array[1,*,2])
        elif equation is not None:
            self.equation = Equation(equation.text, self.sim_specs, self.dimensions_global, self.name, self.debug)
        else:
            raise Exception('Error: equation = None')
        #####################
        # Seteo special behavior (graphical functions, arrays)
        self.special_behavior = res

    # Extras
    def set_access(self):
        access = self.aux_element.get('access')
        if access is None:
            return None
        if self.debug:
            print('El aux ' + self.parent + '.' + self.name + ' es de acceso tipo ' + access)
        return access

    def get_access(self):
        return self.access

    def get_equation(self):
        return self.equation

    def get_equation_variables(self):
        return self.equation.get_variables()

    def get_non_negative(self):
        nonNegative = self.aux_element.find(self.source_xmlns + 'non_negative')
        if nonNegative is None:
            return 0
        return 1