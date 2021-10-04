from src.formalismos.devs.DEVSPort import DEVSPort
from src.formalismos.devs.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent


class DEVSIntegrator(DEVSAtomicComponent):
    def __init__(self, xmile_stock, parent_name):
        self.stock = xmile_stock
        self.parent = parent_name
        self.name = xmile_stock.get_name()
        self.access = xmile_stock.get_access()
        self.equation = xmile_stock.get_equation()
        self.integrator_type = 'QSS1'
        # TODO : verify that 'x0' is set to a numeric value (might require preprocessing)
        self.integrator_parameters = {
            'x0': self.equation.get_equation(),
            'dQRel': '0.001',
            'dQMin': '0.001',
            'non_negative': xmile_stock.get_non_negative()
        }
        self.type = 'DEVSIntegrator'
        self.input_ports = self.set_input_ports()
        self.output_ports = [DEVSPort(self.name, self, 'out')]

    def __repr__(self):
        return str({
            'name': self.name,
            'access': self.access,
            'equation': self.equation,
            'integrator_type': self.integrator_type,
            'integrator_parameters': self.integrator_parameters
        })

    def __str__(self):
        return str({
            'name': self.name,
            'access': self.access,
            'equation': self.equation,
            'integrator_type': self.integrator_type,
            'integrator_parameters': self.integrator_parameters
        })

    # Setters
    def set_input_ports(self):
        # Note : appends 'Tot' as suffix
        input_ports = [
            DEVSPort('Tot' + self.name, self, 'in'), 
            DEVSPort('subtract', self, 'in'), 
            DEVSPort('increment', self, 'in')
        ]
        variables = self.equation.get_variables()
        for var in variables:
            input_ports.append(DEVSPort(var, self, 'in'))
        # Note : appends input ports corresponding to special functions
        # Note : lo de abajo es fruta, creo
        #for special_func_obj in self.equation.get_special_functions(self.parent):
        #    input_ports.append(DEVSPort(special_func_obj.get_name(), self, 'in'))
        return list(set(input_ports))

    # Getters
    def get_parent_name(self):
        return self.parent

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_access(self):
        return self.access

    def get_equation(self):
        return self.equation

    def get_integrator_type(self):
        return self.integrator_type

    def get_integrator_parameters(self):
        return self.integrator_parameters

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    def parameters(self):
        return self.integrator_parameters

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}
