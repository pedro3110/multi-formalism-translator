class DEVSInternalConnection(object):
    def __init__(self, port_from, component_from, port_to, component_to):
        self.port_from = port_from
        self.component_from = component_from
        self.port_to = port_to
        self.component_to = component_to
        self.type = port_to.get_type()

    def __repr__(self):
        return str({
            'port_from': self.port_from.get_name(),
            'component_from': self.get_component_from().get_name(),
            'port_to': self.port_to.get_name(),
            'component_to': self.component_to.get_name()
        })

    def __str__(self):
        return str({
            'port_from': self.port_from.get_name(),
            'component_from': self.get_component_from().get_name(),
            'port_to': self.port_to.get_name(),
            'component_to': self.component_to.get_name()
        })

    def __eq__(self, other):
        return self.port_from == other.get_port_from() and \
               self.port_to == other.get_port_to() and \
               self.component_to.get_name() == other.get_component_to().get_name() and \
               self.component_from.get_name() == other.get_component_from().get_name()

    def __hash__(self):
        return hash(self.port_from) ^ hash(self.port_to) ^ hash(self.component_to) ^ hash(self.component_from)

    def get_port_from(self):
        return self.port_from

    def get_port_to(self):
        return self.port_to

    def get_component_from(self):
        return self.component_from

    def get_component_to(self):
        return self.component_to

    def get_type(self):
        return self.type