class ModuleConnection(object):
    def __init__(self, connection_element, source_xmlns, debug):
        self.source_xmlns = source_xmlns
        self.connection_element = connection_element
        self.from_ = self.get_from()
        self.to_   = self.get_to()
        self.debug = debug
    
    def __repr__(self):
        return str({'to' : self.to_, 'from' : self.from_})
    
    def __str__(self):
        return str({'to' : self.to_, 'from' : self.from_})
        
    def get_from(self):
        # Puede venir de un 'atomico' (stock / aux) o de un 'acoplado' (modulo)
        from_ = self.connection_element.get('from')
        coupled_atomic = from_.split('.')
        if len(coupled_atomic) == 0:
            raise Exception('Error: una conexion debe tener algun origen')
        atomic = coupled_atomic[1]
        if coupled_atomic[0] == '':
            coupled  = None
        else:
            coupled = coupled_atomic[0]
        return {'from_coupled' : coupled, 'from_atomic' : atomic}
    
    def get_to(self):
        # Puede ir a un 'atomico' (stock / aux) o a un 'acoplado' (modulo)
        to_ = self.connection_element.get('to')
        coupled_atomic = to_.split('.')
        if len(coupled_atomic) == 0:
            raise Exception('Error: una conexion debe tener algun origen')
        atomic = coupled_atomic[1]
        if coupled_atomic[0] == '':
            coupled  = None
        else:
            coupled = coupled_atomic[0]
        return {'to_coupled' : coupled, 'to_atomic' : atomic}