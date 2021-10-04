from src.modulosDEVS.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent


class Cell(DEVSAtomicComponent):
    def __init__(self, name):
        self.name = name
        self.type = 'cell'
        self.dim = None
        self.delay = None
        self.default_delay_time = None
        self.border_type = None
        self.neighbors = None
        self.initial_value = None
        self.initial_cells_value = None
        self.local_transition = None
        self.rules = None
        self.macros = None
        self.input_ports = None
        self.output_ports = None
        self.internal_input_connections = None
        self.internal_output_connections = None
        self.internal_connections = None
        self.ports_in_transition = None
        self.zones = None

    # Setters
    def set_dim(self, dim):
        self.dim = dim

    def set_delay(self, delay):
        self.delay = delay

    def set_default_delay_time(self, delay):
        self.default_delay_time = delay

    def set_border_type(self, border_type):
        self.border_type = border_type

    def set_initial_value(self, initial_value):
        self.initial_value = initial_value

    def set_local_transition(self, local_transition_name):
        self.local_transition = local_transition_name

    def set_neighbors(self, neighbors):
        assert(self.dim is not None)
        for neighbor in neighbors:
            assert(len(neighbor) == len(self.dim))
        self.neighbors = neighbors

    def set_zones(self, zones):
        self.zones = zones

    def set_rules(self, rules):
        for rule_name, rule_list in rules.items():
            for rule in rule_list:
                rule['condition'] = rule['condition'].replace('>', '&gt;').replace('<', '&lt;')
                if type(rule['action']) is str:
                    rule['action'] = rule['action'].replace('>', '&gt;').replace('<', '&lt;')
                if type(rule['delay']) is str:
                    rule['delay'] = rule['delay'].replace('>', '&gt;').replace('<', '&lt;')
        self.rules = rules

    def set_input_ports(self, input_ports):
        self.input_ports = input_ports

    def set_output_ports(self, output_ports):
        self.output_ports = output_ports

    def set_internal_input_connections(self, internal_input_connections):
        assert(self.input_ports is not None)
        assert(self.dim is not None)
        for iic in internal_input_connections:
            assert('port_from' in iic.keys() and 'component_to' in iic.keys() and 'port_to' in iic.keys())
            assert(iic['port_from'] in self.input_ports)
            dims = iic['component_to']
            assert(len(dims) == len(self.dim))
            for i,x in enumerate(dims):
                assert(0 <= x and x < self.dim[i])
            iic['component_to'] = str(iic['component_to']).replace(' ', '')
        self.internal_input_connections = internal_input_connections

    def set_internal_output_connections(self, internal_output_connections):
        assert(self.output_ports is not None)
        assert(self.dim is not None)
        for ioc in internal_output_connections:
            assert('component_from' in ioc.keys() and 'port_from' in ioc.keys() and 'port_to' in ioc.keys())
            assert(ioc['port_to'] in self.output_ports)
            dims =  ioc['component_from']
            assert(len(dims) == len(self.dim))
            for i,x in enumerate(dims):
                assert(0 <= x and x < self.dim[i])
            ioc['component_from'] = str(ioc['component_from']).replace(' ', '')
        self.internal_output_connections = internal_output_connections

    def set_ports_in_transition(self, input_component_transition):
        for ict in input_component_transition:
            assert('input_port' in ict.keys() and 'component' in ict.keys() and 'rule' in ict.keys())
            assert(ict['rule'] in self.rules)
            component = ict['component']
            assert(len(component) == len(self.dim))
            for i,x in enumerate(component):
                assert(0 <= x and x < self.dim[i])
            ict['component'] = str(ict['component']).replace(' ', '')
        self.ports_in_transition = input_component_transition

    # Getters
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_dim(self):
        return str(self.dim).replace(' ', '')

    def get_delay(self):
        return self.delay

    def get_default_delay_time(self):
        return self.default_delay_time

    def get_border_type(self):
        return self.border_type

    def get_neighbors(self):
        return list(map(lambda x : str(x).replace(' ', ''), self.neighbors))

    def get_initial_value(self):
        return self.initial_value

    def get_local_transition(self):
        return self.local_transition

    def get_zones(self):
        return self.zones

    def get_rules(self):
        return self.rules

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    def get_internal_input_connections(self):
        return self.internal_input_connections

    def get_internal_output_connections(self):
        return self.internal_output_connections

    def get_internal_connections(self):
        return self.internal_input_connections + self.internal_output_connections

    def get_ports_in_transition(self):
        return self.ports_in_transition

    def get_dimensions(self):
        return []

    def get_atomics_array_position(self):
        return {}