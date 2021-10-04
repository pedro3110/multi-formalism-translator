class DEVSExternalInputConnection(object):
    def __init__(self, port_from, port_to, component_to):
        self.port_from = port_from
        self.port_to = port_to
        self.component_to = component_to

    def __repr__(self):
        return str({
            'port_from': self.port_from.get_name(),
            'port_to': self.port_to.get_name(),
            'component_to': self.component_to.get_name()
        })

    def __eq__(self, other):
        return self.port_from == other.get_port_from() and \
               self.port_to == other.get_port_to() and \
               self.component.get_name() == other.get_component_to().get_name()

    def __hash__(self):
        return hash(self.port_from) ^ hash(self.port_to) ^ hash(self.component_to)

    # Getters
    def get_component_to(self):
        return self.component_to

    def get_port_from(self):
        return self.port_from

    def get_port_to(self):
        return self.port_to