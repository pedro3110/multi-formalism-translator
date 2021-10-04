class Module(object):
    def __init__(self, module_element, source_xmlns, parent, sim_specs, dimensions, debug):
        self.debug = debug
        self.sim_specs = sim_specs
        self.dimensions = dimensions
        self.parent = parent
        self.source_xmlns = source_xmlns
        self.module_element = module_element
        self.name = self.get_name()
        self.connections = self.get_connections()
        
    def __repr__(self):
        return str({
            'parent' : self.parent,
            'name' : self.name,
            'connections' : self.connections
        })
    
    def __repr__(self):
        return str({
            'parent' : self.parent,
            'name' : self.name,
            'connections' : self.connections
        })
        
    def get_name(self):
        name = self.module_element.get('name')
        if name is None:
            raise Exception('Error: los modulos deben tener nombre')
        return name
    
    def get_connections(self):
        connections = self.module_element.findall(self.source_xmlns + 'connect')
        if len(connections) == 0:
            if self.debug:
                print('Alerta: el modelo ' + self.name + ' no tiene niguna conexion')
        return list(map(lambda x : ModuleConnection(x, self.source_xmlns, self.debug), connections))