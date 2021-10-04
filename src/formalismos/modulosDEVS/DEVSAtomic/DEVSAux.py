from src.formalismos.modulosDEVS.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent
from src.formalismos.modulosDEVS.DEVSPort import DEVSPort


class DEVSAux(DEVSAtomicComponent):
    def __init__(self, xmile_aux, xmile_model, xmile_dependencies):
        self.xmile_model = xmile_model
        self.xmile_aux = xmile_aux
        self.parent = self.xmile_aux.get_parent()
        self.access = self.xmile_aux.get_access()
        self.subscript = self.xmile_aux.get_subscript()
        self.name = self.xmile_aux.get_name()
        self.equation = self.xmile_aux.get_equation()
        self.input_ports = self.set_input_ports(xmile_dependencies)
        self.output_ports = self.set_output_ports()
        self.non_negative = self.xmile_aux.get_non_negative()
        self.type = "DEVSAux"

    def __repr__(self):
        return str({
            'access': self.access,
            'name': self.name,
            'equation': self.equation,
            'parent': self.parent,
            'input_ports': self.input_ports,
            'type': self.type,
            'non_negative': self.non_negative
        })

    def __str__(self):
        return str({
            'access': self.access,
            'name': self.name,
            'equation': self.equation,
            'parent': self.parent,
            'input_ports': self.input_ports,
            'type': self.type,
            'non_negative': self.non_negative
        })

    # Un aux puede recibir : Cte's / Aux's / Acoplados (Stock's)
    def set_input_ports(self, xmile_dependencies):
        # Para cada dependencia, buscar en el modelo xmile si es Cte / Aux / Stock
        input_ports = []
        variables = self.equation.get_variables()
        for var in variables:
            input_ports.append(DEVSPort(var, self, 'in'))
        # Agrego inputs correspondientes a funciones especiales
        for special_func_obj in self.equation.get_special_functions(self.parent):
            input_ports.append(DEVSPort(special_func_obj.get_name(), self, 'in'))
        return list(set(input_ports))

    def set_output_ports(self):
        # '*' : el output de Aux podria ir a 
        # un DEVSCoupledComponent (si va a flows en xmile) o 
        # a un DEVSAux (si va a un aux en xmile), o a ambos
        return [DEVSPort(self.get_name(), self, 'out')]

    def get_access(self):
        return self.access

    def get_subscript(self):
        return self.subscript

    def get_name(self):
        return self.name

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
        return {
            'equation': self.equation.get_equation(),
            'non_negative': self.non_negative
        }

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}