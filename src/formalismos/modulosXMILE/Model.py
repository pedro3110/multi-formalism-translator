from src.formalismos.modulosXMILE.Stock import Stock
from src.formalismos.modulosXMILE.Flow import Flow
from src.formalismos.modulosXMILE.Module import Module
from src.formalismos.modulosXMILE.Auxiliary import Aux
from src.formalismos.modulosXMILE.Dependency import Dependency


class Model(object):

    def __init__(self, model_element, sim_specs, dimensions_element, debug):
        self.source_xmlns      = "{http://docs.oasis-open.org/xmile/ns/XMILE/v1.0}"
        self.source_xmlns_isee = "{http://iseesystems.com/XMILE}"
        self.sim_specs = sim_specs
        self.debug = debug
        self.model_element = model_element
        self.name      = self.set_name()
        self.dimensions = self.set_dimensions(dimensions_element)
        self.variables = self.set_variables()
        self.modules   = self.set_modules()
        self.auxs      = self.set_auxs()
        self.stocks    = self.set_stocks()
        self.flows     = self.set_flows()
        self.dependencies = self.set_dependencies()

    def __repr__(self):
        return str({
            'name' : self.name,
            'modules' : self.modules,
            'dimensions': self.dimensions,
            'auxs' : self.auxs,
            'stocks' : self.stocks,
            'flows' : self.flows,
            'dependencies' : self.dependencies
        })
    
    def __str__(self):
        return str({
            'name' : self.name,
            'modules' : self.modules,
            'dimensions': self.dimensions,
            'auxs' : self.auxs,
            'stocks' : self.stocks,
            'flows' : self.flows,
            'dependencies' : self.dependencies
        })

    def set_name(self):
        name = self.model_element.get('name')
        if name is None:
            return 'top'
        return name

    def get_name(self):
        return self.name

    def set_dimensions(self, dimensions_element):
        if dimensions_element is None:
            ans = {}
        else:
            ans = [
                {'name': dim.get('name'), 'size': int(dim.get('size'))}
                for dim in dimensions_element.findall(self.source_xmlns + 'dim')
            ]
        return ans

    def set_variables(self):
        variables = self.model_element.find(self.source_xmlns + 'variables')
        if variables is None:
            raise Exception('Error: hay un modelo que no contiene ninguna variable')
        variables_list = self.model_element.findall(self.source_xmlns + 'variables')
        if len(variables_list) > 1:
            raise Exception('Error: estamos asumiendo que solo puede haber 1 elemento de variables por modelo')
        return variables
    
    def set_modules(self):
        modules = self.variables.findall(self.source_xmlns + 'module')
        return list(map(lambda x : Module(x, self.source_xmlns, self.name, self.sim_specs, self.dimensions, self.debug), modules))

    def get_modules(self):
        return self.modules

    def set_auxs(self):
        auxs = self.variables.findall(self.source_xmlns + 'aux')
        return list(map(lambda x : Aux(x, self.source_xmlns, self.name, self.sim_specs, self.dimensions, self.debug), auxs))

    def get_auxs(self):
        return self.auxs

    def set_stocks(self):
        stocks = self.variables.findall(self.source_xmlns + 'stock')
        return list(map(lambda x : Stock(x, self.source_xmlns, self.name, self.sim_specs, self.dimensions, self.debug), stocks))

    def get_stocks(self):
        return self.stocks

    def set_flows(self):
        flows = self.variables.findall(self.source_xmlns + 'flow')
        return list(map(lambda x : Flow(x, self.source_xmlns, self.name, self.sim_specs, self.dimensions, self.debug), flows))
    
    def get_flows(self):
        return self.flows

    def set_dependencies(self):
        dependencies    = self.variables.find(self.source_xmlns_isee + 'dependencies')
        if dependencies is None:
            return []
        return list(map(lambda x : Dependency(x, self.source_xmlns, self.name, self.sim_specs, self.dimensions, self.debug), 
                        dependencies.findall(self.source_xmlns + 'var')))
    
    def get_dependencies(self):
        return self.dependencies
