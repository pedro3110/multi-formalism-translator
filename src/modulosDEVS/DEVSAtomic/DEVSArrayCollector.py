from src.modulosDEVS.DEVSPort import DEVSPort


class DEVSArrayCollector:
    def __init__(self, destiny_name, dimensions, atomic_devs):
        self.parent = destiny_name
        self.type = 'DEVSArrayCollector'
        self.name = 'collector'
        self.atomic_devs = atomic_devs
        self.dimensions = dimensions
        self.input_ports = self.set_input_ports()
        self.output_ports = self.set_output_ports()
        self.atomics_array_position = self.set_atomics_array_position()

    def __repr__(self):
        return str({
            'name': self.name
        })

    def __str__(self):
        return str({
            'name': self.name
        })

    # Setters
    def set_input_ports(self):
        return [
            DEVSPort(at.get_name(), self, 'in') for at in self.atomic_devs
        ]

    def set_output_ports(self):
        return [
            # Comunicacion con DEVSArrayAgregator's: manda una tupla con toodos los valores del array actualizados
            DEVSPort(self.parent, self, 'out')
        ]

    def set_atomics_array_position(self):
        ans = {}
        for at in self.atomic_devs:
            assert(at.get_subscript() is not None)
            ans[at.get_name()] = at.get_subscript()
        return ans

    # Getters
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_parent_name(self):
        return self.parent

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    def parameters(self):
        p = { }
        return p

    def get_dimensions(self):
        return self.dimensions

    def get_atomics_array_position(self):
        return self.atomics_array_position

