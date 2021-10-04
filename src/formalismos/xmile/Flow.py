from src.modulosAuxiliares.Equation import *


class Flow(object):
    def __init__(self, flow_element, source_xmlns, parent, sim_specs, dimensions, debug):
        self.debug = debug
        self.sim_specs = sim_specs
        self.dimensions = dimensions
        self.parent = parent
        self.source_xmlns = source_xmlns
        self.flow_element = flow_element
        self.name = self.get_name()
        self.equation = self.get_equation()
        self.nonNegative = self.get_non_negative()
        self.special_behavior = self.set_special_behavior()
        
    def __repr__(self):
        return str({
            'parent' : self.parent,
            'name' : self.name,
            'equation' : self.equation,
            'nonNegative' : self.nonNegative,
            'special_behavior': self.special_behavior
        })
    
    def __str__(self):
        return str({
            'parent' : self.parent,
            'name' : self.name,
            'equation' : self.equation,
            'nonNegative' : self.nonNegative,
            'special_behavior': self.special_behavior
        })

    def set_special_behavior(self):
        # Graphical function
        res = {}
        equation = self.flow_element.find(self.source_xmlns + 'eqn').text
        # TODO: 'TIME' es la unica funcion que su comportamiento no esta relacionado con alguna expresion matematica en 'equation'
        if equation in ['TIME']:
            xscale = self.flow_element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'xscale')
            yscale = self.flow_element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'yscale')
            ypts = self.flow_element.find(self.source_xmlns + 'gf/' + self.source_xmlns + 'ypts')
            res['gf'] = {
                'xscale': {'min': xscale.get('min'), 'max': xscale.get('max')},
                'yscale': {'min': yscale.get('min'), 'max': yscale.get('max')},
                'ypts': ypts.text
            }
        return res
    
    def get_special_behavior(self):
        return self.special_behavior

    def get_name(self):
        name = self.flow_element.get('name')
        if name is None:
            raise Exception('Error: todos los flows deben tener nombre')
        return name
    
    def get_equation(self):
        equation = self.flow_element.find(self.source_xmlns + 'eqn').text
        if equation == '':
            raise Exception('Error: hay una ecuacion definida sin ningun simbolo (invalida) en ' + self.name)
        return Equation(equation, self.sim_specs, self.dimensions, self.name, self.debug)
        
    def get_non_negative(self):
        nonNegative = self.flow_element.find(self.source_xmlns + 'non_negative')
        if nonNegative is None:
            return 0
        return 1