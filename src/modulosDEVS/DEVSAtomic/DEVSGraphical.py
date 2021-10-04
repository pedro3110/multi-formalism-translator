from src.modulosDEVS.DEVSPort import DEVSPort
from src.modulosDEVS.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent


class DEVSGraphical(DEVSAtomicComponent):
    def __init__(self, xmile_aux, parent_name):
        # TODO : llamar constructor del parent : in Python 2 use super(DEVSPulse, self).__init__()
        self.xmile_aux = xmile_aux
        self.destiny_name = ''
        self.parent = parent_name
        self.extra_inputs = []
        self.name = self.set_name()
        self.subscript = self.set_subscript()
        self.equation = self.xmile_aux.get_equation()
        self.input_ports = self.set_input_ports()
        self.output_ports = self.set_output_ports()
        self.xscale = self.set_xscale()
        self.yscale = self.set_yscale()
        self.ypts = self.set_ypts()
        self.type = 'DEVSGraphical'
        # TODO : capturar x/y values. Setear default para intervalo de tiempos que mira

    def __repr__(self):
        return str({
            'name': self.name,
            'xscale': self.xscale,
            'yscale': self.yscale,
            'ypts': self.ypts
        })

    def __str__(self):
        return str({
            'name': self.name,
            'xscale': self.xscale,
            'yscale': self.yscale,
            'ypts': self.ypts
        })

    # Setters
    def set_parent(self, parent_name):
        self.parent = parent_name

    def set_name(self, suffix=''):
        if suffix == '':
            name = self.xmile_aux.get_name()
            return name
        else:
            name = self.xmile_aux.get_name() + suffix
            self.name = name
            return name
    def set_subscript(self):
        subscript = self.xmile_aux.get_subscript()
        return subscript

    def set_input_ports(self):
        if self.equation.get_equation() == 'TIME':
            return []
        input_ports = []
        variables = self.equation.get_variables()
        for var in variables:
            input_ports.append(DEVSPort(var, self, 'in'))
        for special_func_obj in self.equation.get_special_functions(self.parent):
            input_ports.append(DEVSPort(special_func_obj.get_name(),
                                        self, 'in'))
        return list(set(input_ports))

    def set_output_ports(self, default=[]):
        if default == []:
            return [DEVSPort(self.name, self, 'out')]
        else:
            self.output_ports = default
            return self.output_ports

    def set_xscale(self):
        special_behavior = self.xmile_aux.get_special_behavior()
        assert 'gf' in special_behavior.keys()
        return special_behavior['gf']['xscale']

    def set_yscale(self):
        special_behavior = self.xmile_aux.get_special_behavior()
        assert 'gf' in special_behavior.keys()
        return special_behavior['gf']['yscale']

    def set_ypts(self):
        special_behavior = self.xmile_aux.get_special_behavior()
        assert 'gf' in special_behavior.keys()
        return special_behavior['gf']['ypts']

    # Getters
    def get_name(self):
        return self.name

    def get_subscript(self):
        return self.subscript

    def get_parent_name(self):
        return self.parent

    def get_type(self):
        return self.type

    def get_equation(self):
        return self.equation

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    def get_parameters(self):
        return self.equation.get_parameters()

    # devuelve todo lo que sea alfanumerico
    def get_variables(self):
        return []

    def get_all_inputs(self):
        return self.get_variables()

    def parameters(self):
        p = {  
            'equation': self.equation.get_equation(),
            'xscale_min': self.xscale['min'],
            'xscale_max': self.xscale['max'],
            'yscale_min': self.yscale['min'],
            'yscale_max': self.yscale['max'],
            'ypts': self.ypts
        }
        return p

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}