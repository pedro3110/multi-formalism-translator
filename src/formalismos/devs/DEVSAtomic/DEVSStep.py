from src.formalismos.devs.DEVSPort import DEVSPort
from src.formalismos.devs.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent


class DEVSStep(DEVSAtomicComponent):
    def __init__(self, destiny_name, height, time):
        # TODO : llamar constructor del parent : in Python 2 use super(DEVSPulse, self).__init__()
        self.destiny_name = destiny_name
        self.time = time
        self.height = height
        self.extra_inputs = []
        self.name = self.set_name()
        self.input_ports = self.set_input_ports()
        self.output_ports = self.set_output_ports()
        self.equation = self.set_equation()
        self.type = 'DEVSStep'
        self.parent = None

    # TODO: SETEAR EL DT (== PULSE TIME) ==> OPCION: ir a buscarlo en el xmile original!!!
    def __repr__(self):
        return str({
            'name': self.name,
            'time_input': self.time,
            'height': self.height,
            'destiny_name': self.destiny_name
        })

    def __str__(self):
        return str({
            'name': self.name,
            'time_input': self.time,
            'height': self.height,
            'destiny_name': self.destiny_name
        })

    # Setters
    def set_parent(self, parent_name):
        self.parent = parent_name

    def set_equation(self):
        from modulosAuxiliares.Equation import Equation
        return Equation(str(self.height), False)

    def set_name(self):
        # Nota : Reemplazamos el '.' de los floats por un '_'
        height_name = 'H_' + str(self.height).replace('.', '_')
        time_name = 'T_' + str(self.time).replace('.', '_')
        name = 'STEP_' + height_name + '_' + time_name + '_' + self.destiny_name
        return name

    def set_input_ports(self):
        # los correspondientes a las variables que se utilizen como parametro de la funcion
        input_ports = [
            DEVSPort(extra_input_name, self, 'in') for extra_input_name in self.extra_inputs
        ]

        input_ports.append(DEVSPort(self.time, self, 'in'))

        v = list(map(lambda x : x.isdigit(), self.height.split('.')))
        if not((len(v) == 1 or len(v) == 2) and all(v)): # si no es numerico
            input_ports.append(DEVSPort(self.height, self, 'in'))

        i = list(map(lambda x : x.isdigit(), self.time.split('.')))
        if not((len(i) == 1 or len(i) == 2) and all(i)): # si no es numerico
            input_ports.append(DEVSPort(self.time, self, 'in'))
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
            'height_param': '', 'height_input': '',
            'time_param': '', 'time_input': ''
        }

        h = list(map(lambda x : x.isdigit(), self.height.split('.'))) # chequea que sea numerico (no una var)
        if (len(h) == 1 or len(h) == 2) and all(h):
            # si es numerico
            p.update({'height_param': self.height})
        else:
            # si no
            p.update({'height_input': self.height})

        i = list(map(lambda x : x.isdigit(), self.time.split('.'))) # chequea que sea numerico (no una var)
        if (len(i) == 1 or len(i) == 2) and all(i): 
            # si es numerico
            p.update({'time_param': self.time})
        else:
            # si no
            p.update({'time_input': self.time})
        return p

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}