from src.modulosDEVS.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent
from src.modulosDEVS.DEVSPort import DEVSPort

PLUS_INDEX = 0
MINUS_INDEX = 1


class DEVSFpm(DEVSAtomicComponent):
    def __init__(self, xmile_flow, xmile_stocks, parent_name):
        self.xmile_flow = xmile_flow
        self.xmile_stocks = xmile_stocks
        self.parent = parent_name
        self.equation = self.xmile_flow.get_equation()
        self.non_negative = self.xmile_flow.get_non_negative()
        self.corresponding_stock_names_plus_minus = self.set_corresponding_stocks()
        self.fp = self.set_fplus()
        self.fm = self.set_fminus()
        self.name = xmile_flow.get_name()

    def __repr__(self):
        return str({
            'name': self.name,
            'equation': self.equation,
            'non_negative': self.non_negative
        })

    def __str__(self):
        return str({
            'name': self.name,
            'equation': self.equation,
            'non_negative': self.non_negative
        })

    # Getters
    def get_name(self):
        return self.name
        
    def get_fplus(self):
        return self.fp

    def get_fminus(self):
        return self.fm

    def get_equation(self):
        return self.equation

    def get_non_negative(self):
        return self.non_negative

    # Setters
    def set_corresponding_stocks(self):
        flow_name = self.xmile_flow.get_name()
        corresponding_stock_name_plus = None
        corresponding_stock_name_minus = None

        # ver si flow_name esta entre los inflows/outflows 
        # de algun stock - puede ser inflow/outflow de 0 o 1 stock solamente -
        for stock in self.xmile_stocks:
            if flow_name in list(map(lambda x: x.get_name(),
                                     stock.get_inflows())):
                corresponding_stock_name_plus = stock.get_name()
            if flow_name in list(map(lambda x: x.get_name(),
                                     stock.get_outflows())):
                corresponding_stock_name_minus = stock.get_name()

        return corresponding_stock_name_plus, corresponding_stock_name_minus

    def set_fplus(self):
        corresponding_stock_name_plus = self.corresponding_stock_names_plus_minus[PLUS_INDEX]
        if corresponding_stock_name_plus is None:
            return None
        return DEVSFplus(self.xmile_flow, corresponding_stock_name_plus, self.parent)

    def set_fminus(self):
        corresponding_stock_name_minus = self.corresponding_stock_names_plus_minus[MINUS_INDEX]
        if corresponding_stock_name_minus is None:
            return None
        return DEVSFminus(self.xmile_flow, corresponding_stock_name_minus, self.parent)

    def parameters(self):
        return {
            'equation': self.equation.get_equation(),
            'non_negative': self.non_negative
        }
###############################################################


class DEVSFminus(DEVSFpm):
    def __init__(self, xmile_flow, stock_name, parent_name):
        self.xmile_flow = xmile_flow
        self.stock_name = stock_name
        self.parent = parent_name
        self.original_name = xmile_flow.get_name()
        self.name = self.set_name()
        self.equation = self.xmile_flow.get_equation()
        self.non_negative = self.xmile_flow.get_non_negative()
        self.input_ports = self.set_input_ports()
        self.output_ports = [DEVSPort(self.name, self, 'out'), DEVSPort(self.original_name, self, 'out')]
        self.output_ports_tot = [DEVSPort(self.name, self, 'out')]
        self.type = 'DEVSFminus'

    def __repr__(self):
        return str({
            'name': self.name,
            'original_name': self.original_name,
            'equation': self.equation,
            'input_ports': self.input_ports,
            'output_ports': self.output_ports,
            'type': self.type,
            'non_negative': self.non_negative
        })

    def __str__(self):
        return str({
            'name': self.name,
            'original_name': self.original_name,
            'equation': self.equation,
            'input_ports': self.input_ports,
            'output_ports': self.output_ports,
            'type': self.type,
            'non_negative': self.non_negative
        })

    def set_equation(self, eq):
        self.equation = eq

    def set_input_ports(self, default=[]):
        if default == []:
            input_ports = []
            variables = self.equation.get_variables()
            for var in variables:
                input_ports.append(DEVSPort(var, self, 'in'))
            # Agrego inputs correspondientes a funciones especiales
            for special_func_obj in self.equation.get_special_functions(self.parent):
                input_ports.append(DEVSPort(special_func_obj.get_name(),
                                            self, 'in'))
            return list(set(input_ports))
        else:
            self.input_ports = default



    def set_name(self):
        return self.xmile_flow.get_name() + '_' + self.stock_name

    def get_original_name(self):
        return self.original_name

    def get_name(self):
        return self.name

    def get_parent_name(self):
        return self.parent

    def get_type(self):
        return self.type

    def get_equation(self):
        return self.equation

    def get_non_negative(self):
        return self.non_negative

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    def get_output_ports_tot(self):
        return self.output_ports_tot

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}
###############################################################


class DEVSFplus(DEVSFpm):
    def __init__(self, xmile_flow, stock_name, parent_name):
        self.xmile_flow = xmile_flow
        self.stock_name = stock_name
        self.parent = parent_name
        self.original_name = xmile_flow.get_name()
        self.name = self.set_name()
        self.equation = self.xmile_flow.get_equation()
        self.non_negative = self.xmile_flow.get_non_negative()
        self.input_ports = self.set_input_ports()
        self.output_ports = [DEVSPort(self.name, self, 'out'), DEVSPort(self.original_name, self, 'out')]
        self.output_ports_tot = [DEVSPort(self.name, self, 'out')]
        self.type = 'DEVSFplus'

    def __repr__(self):
        return str({
            'name': self.name,
            'original_name': self.original_name,
            'equation': self.equation,
            'input_ports': self.input_ports,
            'output_ports': self.output_ports,
            'type': self.type,
            'non_negative': self.non_negative
        })

    def __str__(self):
        return str({
            'name': self.name,
            'original_name': self.original_name,
            'equation': self.equation,
            'input_ports': self.input_ports,
            'output_ports': self.output_ports,
            'type': self.type,
            'non_negative': self.non_negative
        })

    def set_equation(self, eq):
        self.equation = eq

    def set_input_ports(self, default=[]):
        if default == []:
            input_ports = []
            variables = self.equation.get_variables()
            for var in variables:
                input_ports.append(DEVSPort(var, self, 'in'))
            # Agrego inputs correspondientes a funciones especiales
            for special_func_obj in self.equation.get_special_functions(self.parent):
                input_ports.append(DEVSPort(special_func_obj.get_name(),
                                            self, 'in'))
            return list(set(input_ports))
        else:
            self.input_ports = default

    def set_name(self):
        return self.xmile_flow.get_name() + '_' + self.stock_name

    def get_original_name(self):
        return self.original_name

    def get_name(self):
        return self.name

    def get_parent_name(self):
        return self.parent

    def get_type(self):
        return self.type

    def get_equation(self):
        return self.equation

    def get_non_negative(self):
        return self.non_negative

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    def get_output_ports_tot(self):
        return self.output_ports_tot

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}