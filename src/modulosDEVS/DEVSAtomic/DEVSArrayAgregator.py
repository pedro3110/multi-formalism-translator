from src.modulosDEVS.DEVSPort import DEVSPort
import re


class DEVSArrayAgregator:
    def __init__(self, destiny_name, dimensions, array_function):

        # TODO: implementar c/u de las agregaciones
        self.aggregations = ['SUM', 'MEAN', 'PROD']
        self.parent = destiny_name
        self.array_function = array_function
        self.dimensions = dimensions
        self.name = self.set_name()
        self.input_ports = self.set_input_ports()
        self.output_ports = self.set_output_ports()
        self.type = 'DEVSArrayAgregator'

    ####
    def __repr__(self):
        return str({
            'name': self.name
        })

    def __str__(self):
        return str({
            'name': self.name
        })

    ####
    def set_name(self):
        name = self.array_function.replace("*","ALL").replace(",","_").replace("[","_").replace("]","")
        name = name.replace("(","_").replace(")","")
        return name

    def set_input_ports(self):
        # Recibe todos los input ports que necesite (aparte del correspondiente al Array)
        # NOTA: en principio, asumimos que 'equation' es una posicion del array (ie.: conv1[1,2])
        # NOTA: necesito conocer el array sobre el cual estoy haciendo la agregacion!!!
        ans = []
        regex = r"[\w]+\[[\*\d+][,\*\d+]*\]"
        search_results = re.findall(re.compile(regex), self.array_function)
        for res in search_results:
            x = res.split("[")[0]
            ans.append(DEVSPort(x, self, 'in'))
        return ans

    def set_output_ports(self):
        return [
            DEVSPort(self.get_name(), self, 'out')
        ]

    ####
    def get_name(self):
        return self.name

    def set_parent(self, parent_name):
        self.parent = parent_name

    def get_all_inputs(self):
        return [ip.get_name() for ip in self.input_ports]

    def get_type(self):
        return self.type

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    def get_parent_name(self):
        return self.parent

    def parameters(self):
        p = {  
            'equation': self.array_function
        }
        return p

    def get_dimensions(self):
        return self.dimensions

    def get_atomics_array_position(self):
        return {}