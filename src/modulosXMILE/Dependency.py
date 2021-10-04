class Dependency:
    def __init__(self, var_element, source_xmlns, parent, sim_specs, dimensions, debug):
        self.parent = parent
        self.sim_specs = sim_specs
        self.dimensions = dimensions
        self.source_xmlns = source_xmlns
        self.var_element = var_element
        self.name = self.set_name()
        self.inputs = self.set_inputs()
        self.debug = debug
        
    def __repr__(self):
        return str({
            'parent' : self.parent,
            'name' : self.name,
            'inputs' : self.inputs
        })
    
    def __str__(self):
        return str({
            'parent' : self.parent,
            'name' : self.name,
            'inputs' : self.inputs
        })
    
    def set_name(self):
        name = self.var_element.get('name')
        if name is None:
            raise Exception('Error: todas las dependencies deben tener nombre')
        return name

    def get_name(self):
        return self.name

    def set_inputs(self):
        inputs = self.var_element.findall(self.source_xmlns + 'in')
        inputs = list(map(lambda x : x.text, inputs))
        return inputs

    def get_inputs(self):
        return self.inputs