class DEVSPort(object):

    def __init__(self, name, component, type_, is_for_constant=False):
        self.type = type_
        self.name = name
        # TODO : assert 'component' is of type 'DEVSComponent'
        self.component = component
        self.is_for_constant = is_for_constant

    def __repr__(self):
        return str(dict(name=self.name, type=self.type, component=self.component.get_name()))

    def __str__(self):
        return str(dict(name=self.name, type=self.type, component=self.component.get_name()))

    def __eq__(self, other):
        # TODO : same for DEVSCoupledComponent
        return self.name == other.get_name() and self.component.get_name() == other.get_component().get_name() and \
               other.get_type() == self.type

    def __hash__(self):
        return hash(self.name) ^ hash(self.component.get_name()) ^ hash(self.type)

    # Setters
    def set_type(self, type_):
        self.type = type_

    # Getters
    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_component(self):
        return self.component

    def get_is_for_constant(self):
        return self.is_for_constant
