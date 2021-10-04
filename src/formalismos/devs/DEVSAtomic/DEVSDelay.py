from src.formalismos.devs.DEVSPort import DEVSPort
from src.formalismos.devs.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent
from src.modulosAuxiliares.Equation import Equation


class DEVSDelay(DEVSAtomicComponent):
    def __init__(self, destiny_name, input_parameter, delay_parameter, initial_delay_parameter):
        # TODO : llamar constructor del parent : in Python 2 use super(DEVSPulse, self).__init__()
        self.destiny_name = destiny_name
        self.input_parameter = input_parameter
        self.delay_parameter = delay_parameter
        self.initial_delay_parameter = initial_delay_parameter
        self.extra_inputs = []
        self.name = self.set_name()
        self.input_ports = self.set_input_ports()
        self.output_ports = self.set_output_ports()
        self.equation = self.set_equation()
        self.type = 'DEVSDelay'
        self.parent = None

    # TODO: SETEAR EL DT (== PULSE TIME) ==> OPCION: ir a buscarlo en el xmile original!!!
    def __repr__(self):
        return str({
            'name': self.name,
            'input_parameter': self.input_parameter,
            'delay_parameter': self.delay_parameter,
            'initial_delay_parameter': self.initial_delay_parameter,
            'destiny_name': self.destiny_name
        })

    def __str__(self):
        return str({
            'name': self.name,
            'input_parameter': self.input_parameter,
            'delay_parameter': self.delay_parameter,
            'initial_delay_parameter': self.initial_delay_parameter,
            'destiny_name': self.destiny_name
        })

    # Setters
    def set_parent(self, parent_name):
        self.parent = parent_name

    def set_equation(self):
        return Equation(str(self.input_parameter), False)

    def set_name(self):
        # Nota : Reemplazamos el '.' de los floats por un '_'
        name = 'DELAY_' + str(self.input_parameter).replace('.', '_') + '_' + self.destiny_name
        return name

    def set_input_ports(self):
        # los correspondientes a las variables que se utilizen como parametro de la funcion
        input_ports = [
            DEVSPort(extra_input_name, self, 'in') for extra_input_name in self.extra_inputs
        ]
        input_ports.append(DEVSPort(self.input_parameter, self, 'in'))
        input_ports.append(DEVSPort(self.delay_parameter, self, 'in'))
        if self.initial_delay_parameter is not None:
            input_ports.append(DEVSPort(self.initial_delay_parameter, self, 'in'))
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
            'input_parameter': self.input_parameter,
            'delay_parameter': self.delay_parameter,
            'initial_delay_parameter': self.initial_delay_parameter,
            'equation': self.equation.get_equation()
        }
        return p

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}