from src.modulosDEVS.DEVSPort import DEVSPort
from src.modulosDEVS.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent
from src.modulosAuxiliares.Equation import Equation

class DEVSUniform(DEVSAtomicComponent):
    def __init__(self, destiny_name, min_val, max_val, dt):
        # TODO : llamar constructor del parent : in Python 2 use super(DEVSPulse, self).__init__()
        self.destiny_name = destiny_name
        self.min_val = min_val
        self.max_val = max_val
        self.extra_inputs = []
        self.dt = dt
        self.name = self.set_name()
        self.input_ports = self.set_input_ports()
        self.output_ports = self.set_output_ports()
        self.equation = self.set_equation()
        self.type = 'DEVSUniform'
        self.parent = None

    def __repr__(self):
        return str({
            'name': self.name,
            'min_val': self.min_val,
            'max_val': self.max_val,
            'dt': self.dt,
            'destiny_name': self.destiny_name
        })

    def __str__(self):
        return str({
            'name': self.name,
            'min_val': self.min_val,
            'max_val': self.max_val,
            'dt': self.dt,
            'destiny_name': self.destiny_name
        })

    # Setters
    def set_parent(self, parent_name):
        self.parent = parent_name

    def set_equation(self):
        return Equation(str(self.name), False)

    def set_name(self):
        # Nota : Reemplazamos el '.' de los floats por un '_'
        name = 'UNIFORM_' + \
            str(self.min_val).replace('.', '_') + '_' + \
            str(self.max_val).replace('.', '_') + '_' + \
            self.destiny_name
        return name

    def set_input_ports(self):
        # los correspondientes a las variables que se utilizen como parametro de la funcion
        input_ports = [
            DEVSPort(extra_input_name, self, 'in') for extra_input_name in self.extra_inputs
        ]
        input_ports.append(DEVSPort(self.min_val, self, 'in'))
        input_ports.append(DEVSPort(self.max_val, self, 'in'))
        return input_ports

    def set_output_ports(self):
        # el nombre de esta funcion
        return [DEVSPort(self.name, self, 'out')]

    # Getters
    # devuelve todo lo que sea numerico (int's, float's)
    def get_name(self):
        return self.name

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
        return self.equation.get_variables()

    def get_all_inputs(self):
        return self.get_variables() + list(map(lambda x : x.get_name(), self.input_ports))

    def parameters(self):
        p = {  
            'equation': self.equation.get_equation(),
            'dt': self.dt,
            'min_val': self.min_val,
            'max_val': self.max_val
        }
        return p

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}