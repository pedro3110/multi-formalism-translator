from src.formalismos.devs.DEVSPort import DEVSPort
from src.formalismos.devs.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent
from src.modulosAuxiliares.Equation import Equation


class DEVSPulse(DEVSAtomicComponent):
    def __init__(self, destiny_name, volume, first_pulse, interval, dt):
        # TODO : llamar constructor del parent : in Python 2 use super(DEVSPulse, self).__init__()
        self.destiny_name = destiny_name
        self.first_pulse = first_pulse
        self.volume = volume
        self.interval = interval
        self.dt = dt
        self.extra_inputs = []
        self.name = self.set_name()
        self.input_ports = self.set_input_ports()
        self.output_ports = self.set_output_ports()
        self.equation = self.set_equation()
        self.type = 'DEVSPulse'
        self.parent = None

    # TODO: SETEAR EL DT (== PULSE TIME) ==> OPCION: ir a buscarlo en el xmile original!!!
    def __repr__(self):
        return str({
            'name': self.name,
            'dt': self.dt,
            'firstPulse': self.first_pulse,
            'volume': self.volume,
            'interval': self.interval,
            'destiny_name': self.destiny_name
        })

    def __str__(self):
        return str({
            'name': self.name,
            'dt': self.dt,
            'firstPulse': self.first_pulse,
            'volume': self.volume,
            'interval': self.interval,
            'destiny_name': self.destiny_name
        })

    # Setters
    def set_parent(self, parent_name):
        self.parent = parent_name

    def set_equation(self):
        return Equation(str(self.volume), False)

    def set_name(self):
        # Nota : Reemplazamos el '.' de los floats por un '_'
        vol_name = 'V_' + str(self.volume).replace('.', '_')
        interval_name = 'I_' + str(self.interval).replace('.', '_')
        name = 'PULSE_' + vol_name + '_' + interval_name + '_' + self.destiny_name
        return name

    def set_input_ports(self):
        # los correspondientes a las variables que se utilizen como parametro de la funcion
        input_ports = [
            DEVSPort(extra_input_name, self, 'in') for extra_input_name in self.extra_inputs
        ]

        input_ports.append(DEVSPort(self.first_pulse, self, 'in'))

        v = list(map(lambda x : x.isdigit(), self.volume.split('.')))
        if not((len(v) == 1 or len(v) == 2) and all(v)): # si no es numerico
            input_ports.append(DEVSPort(self.volume, self, 'in'))

        i = list(map(lambda x : x.isdigit(), self.interval.split('.')))
        if not((len(i) == 1 or len(i) == 2) and all(i)): # si no es numerico
            input_ports.append(DEVSPort(self.interval, self, 'in'))
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
            'dt': self.dt,
            'equation': self.equation.get_equation(),
            'volume_param': '', 'volume_input': '',
            'interval_param': '', 'interval_input': '',
            'firstPulse_input': ''
        }
        v = list(map(lambda x : x.isdigit(), self.volume.split('.')))

        p.update({'firstPulse_input': self.first_pulse})
        
        if (len(v) == 1 or len(v) == 2) and all(v):
            # si es numerico
            p.update({'volume_param': self.volume})
        else:
            # si no
            p.update({'volume_input': self.volume})

        i = list(map(lambda x : x.isdigit(), self.interval.split('.')))
        if (len(i) == 1 or len(i) == 2) and all(i): 
            # si es numerico
            p.update({'interval_param': self.interval})
        else:
            # si no
            p.update({'interval_input': self.interval})
        return p

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}