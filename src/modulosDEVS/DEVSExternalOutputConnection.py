class DEVSExternalOutputConnection(object):
    def __init__(self, component_from, port_from, port_to):
        self.component_from = component_from
        self.port_from = port_from
        self.port_to = port_to

    def __repr__(self):
        return str({
            'component_from': self.component_from.get_name(),
            'port_from': self.port_from.get_name(),
            'port_to': self.port_to.get_name()
        })

    def __eq__(self, other):
        return self.port_from == other.get_port_from() and \
               self.port_to == other.get_port_to() and \
               self.component.get_name() == other.get_component_from().get_name()

    def __hash__(self):
        return hash(self.port_from) ^ hash(self.port_to) ^ hash(self.component_from)

    # Getters
    def get_component_from(self):
        return self.component_from

    def get_port_from(self):
        return self.port_from

    def get_port_to(self):
        return self.port_to