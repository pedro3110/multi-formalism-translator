from src.modulosAuxiliares.Equation import *
from src.formalismos.modulosXMILE.Inflow import Inflow
from src.formalismos.modulosXMILE.Outflow import Outflow


class Stock(object):
    def __init__(self, stock_element, source_xmlns, parent, sim_specs, dimensions, debug):
        self.debug = debug
        self.sim_specs = sim_specs
        self.dimensions = dimensions
        self.parent = parent
        self.source_xmlns = source_xmlns
        self.stock_element = stock_element
        self.name = self.get_name()
        self.access = self.get_access()
        self.equation = self.get_equation()
        self.outflows = self.get_outflows()
        self.inflows = self.get_inflows()
        self.nonNegative = self.get_non_negative()
        
    def __repr__(self):
        return str({
            'parent' : self.parent,
            'name' : self.name,
            'access' : self.access,
            'equation' : self.equation,
            'outflows' : self.outflows,
            'inflows' : self.inflows,
            'nonNegative' : self.nonNegative
        })
    
    def __str__(self):
        return str({
            'parent' : self.parent,
            'name' : self.name,
            'access' : self.access,
            'equation' : self.equation,
            'outflows' : self.outflows,
            'inflows' : self.inflows,
            'nonNegative' : self.nonNegative
        })
        
    def get_name(self):
        name = self.stock_element.get('name')
        if name is None:
            raise Exception('Error: todos los stocks deben tener nombre')
        return name
    
    def get_access(self):
        access = self.stock_element.get('access')
        if access is None:
            return None
        if self.debug:
            print('El stock ' + self.parent + '.' + self.name + ' es de acceso tipo ' + access)
        return access
    
    def get_equation(self):
        equation = self.stock_element.find(self.source_xmlns + 'eqn').text
        if equation == '':
            raise Exception('Error: hay una ecuacion definida sin ningun simbolo (invalida) en' + self.name)
        return Equation(equation, self.sim_specs, self.dimensions, self.name, self.debug)
    
    def get_outflows(self):
        outflows = self.stock_element.findall(self.source_xmlns + 'outflow')
        return list(map(lambda x : Outflow(x, self.source_xmlns, self.debug), outflows))
    
    def get_inflows(self):
        inflows = self.stock_element.findall(self.source_xmlns + 'inflow')
        return list(map(lambda x : Inflow(x, self.source_xmlns, self.debug), inflows))
    
    def get_non_negative(self):
        nonNegative = self.stock_element.find('non_negative')
        if nonNegative is None:
            return 0
        return 1

    def get_equation_variables(self):
        return self.equation.get_variables()