from src.modulosDEVS.DEVSPort import DEVSPort
from src.modulosDEVS.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent


class DEVSFtot(DEVSAtomicComponent):
    def __init__(self, xmile_stock, parent_name):
        self.stock = xmile_stock
        self.parent = parent_name
        # TODO : con o sin el 'Tot' ?
        self.name = 'Tot' + xmile_stock.get_name()
        self.access = xmile_stock.get_access()
        self.equation = xmile_stock.get_equation()
        self.input_ports = []
        self.output_ports = [DEVSPort(self.name, self, 'out')]
        self.type = 'DEVSFtot'

    def __repr__(self):
        return str({
            'name': self.name,
            'access': self.access,
            'equation': self.equation,
            'input_ports': self.input_ports,
            'output_ports': self.output_ports
            })

    def __str__(self):
        return str({
            'name': self.name,
            'access': self.access,
            'equation': self.equation,
            'input_ports': self.input_ports,
            'output_ports': self.output_ports
            })

    # Setters
    def add_plus_port(self, port_name):
        new_port = DEVSPort(port_name, self, 'in_plus')
        self.input_ports.append(new_port)
        return new_port

    def add_minus_port(self, port_name):
        new_port = DEVSPort(port_name, self, 'in_minus')
        self.input_ports.append(new_port)
        return new_port

    # Getters
    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_parent_name(self):
        return self.parent

    def get_input_ports(self):
        return self.input_ports

    def get_input_ports_names(self):
        return list(map(lambda x: x.get_name(), self.input_ports))

    def get_output_ports(self):
        return self.output_ports

    def get_equation(self):
        return self.equation

    def parameters(self):
        return {'equation': self.equation.get_equation()}

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}