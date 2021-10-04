from src.formalismos.modulosDEVS.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent
from src.formalismos.modulosDEVS.DEVSPort import DEVSPort


class DEVSConstant(DEVSAtomicComponent):
    def __init__(self, xmile_aux, xmile_model):
        self.xmile_model = xmile_model
        self.xmile_constant = xmile_aux
        self.parent = self.xmile_constant.get_parent()
        self.access = self.xmile_constant.get_access()
        self.name = self.xmile_constant.get_name()
        self.subscript = self.set_subscript()
        self.equation = self.xmile_constant.get_equation()
        self.input_ports = self.set_input_ports()
        self.output_ports = [DEVSPort(self.get_name(), self, 'out')]
        self.type = 'DEVSConstant'

    def __repr__(self):
        return str({'access': self.access, 'name': self.name, 'equation': self.equation, 'parent': self.parent,
            'type': self.type})

    def __str__(self):
        return str({'access': self.access, 'name': self.name, 'equation': self.equation, 'parent': self.parent,
            'type': self.type})

    # Setters
    def set_input_ports(self):
        input_ports = [DEVSPort(self.name, self, 'in')]
        variables = self.equation.get_variables()
        for var in variables:
            input_ports.append(DEVSPort(var, self, 'in'))
        # Agrego inputs correspondientes a funciones especiales
        for special_func_obj in self.equation.get_special_functions(self.parent):
            input_ports.append(DEVSPort(special_func_obj.get_name(), self, 'in'))
        return list(set(input_ports))

    def set_subscript(self):
        subscript = self.xmile_constant.get_subscript()
        return subscript

    # Getters
    def get_access(self):
        return self.access

    def get_name(self):
        return self.name

    def get_subscript(self):
        return self.subscript

    def get_equation(self):
        return self.equation

    def get_parent(self):
        return self.parent

    def get_parent_name(self):
        return self.parent

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    def get_type(self):
        return self.type

    def parameters(self):
        return {'value': self.equation.get_equation()}

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}