from os import path
from operator import methodcaller
from jinja2 import Environment, FileSystemLoader, DictLoader


class CdppModelToMaConverter(object):

    @classmethod
    def parse_model(cls, model):
        return Mafile(model, cls.templates_enviroment())

    @classmethod
    def templates_enviroment(cls):
        PATH = './'
        file_loader = FileSystemLoader(path.join(PATH, './root/modulosCDPP/templates'))
        return Environment(autoescape=False,
                           loader=file_loader,
                           trim_blocks=False)


class Mafile(object):

    def __init__(self, model, templates_enviroment):
        self.model = model
        self.templates_enviroment = templates_enviroment

    def model_name(self):
        if self.model.name == 'DEVS_COUPLED_top':
            return 'top'
        else:
            return self.model.name

    def model_name_level(self):
        return self.model.name_level

    def model_parent(self):
        return self.model.parent

    def model_neighbors(self):
        return self.model.neighbors

    def model_transitions(self):
        return self.model.transitions

    def model_ports_in_transition(self):
        return self.model.ports_in_transition

    #def model_parent(self):
    #    return self.parent

    def model_type(self):
        return self.model.model

    def model_in_ports(self):
        return sorted(self.model.in_ports)
    
    def model_in_minus_ports(self):
        return sorted(self.model.in_minus_ports)
    
    def model_in_plus_ports(self):
        return sorted(self.model.in_plus_ports)

    def model_out_ports(self):
        return sorted(self.model.out_ports)

    def model_external_input_connections(self):
        return sorted(self.model.external_input_connections)

    def model_external_output_connections(self):
        return sorted(self.model.external_output_connections)

    def model_internal_connections(self):
        return sorted(self.model.internal_connections)

    def model_parameters(self):
        return self.model.parameters

    def model_zones(self):
        return self.model.zones

    def components(self):
        return sorted(
            [Mafile(component, self.templates_enviroment) for component in self.model.components],
            key=lambda x: (x.model_type(), x.model_name()) 
        )

    def context(self):
        return {'models': [self]}

    def __str__(self):
        return (self.templates_enviroment
            .get_template('mafile.template')
            .render(self.context()))
