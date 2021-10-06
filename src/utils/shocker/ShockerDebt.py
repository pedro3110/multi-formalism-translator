import math
from jinja2 import DictLoader, Environment, FileSystemLoader
import os


class ShockerDebt:

    ####################################################
    def __init__(self, templates_dir, type_, name_, limit, shock_only_once, n_outports, n_outports_to_shock, nombre_shock):
        assert(math.sqrt(n_outports).is_integer) # TODO: por ahora solo se permite shockear en cuadrados
        assert(n_outports > 1)
        assert(n_outports_to_shock > 0)
        self.templates_dir = templates_dir
        self.inputvariables = ["Debt"]
        self.limit = limit
        self.shock_only_once = shock_only_once

        self.nombre_shock = nombre_shock
        self.type = type_
        self.name = name_
        self.n_outports = n_outports
        self.n_outports_to_shock = n_outports_to_shock
        self.outports = []
        self.shock_value = type_
        self.cells = []
        if(type_ in [5,6,7,8]):
            for i in range(int(math.sqrt(n_outports))):
                for j in range(int(math.sqrt(n_outports))):
                    i_str = str(i)
                    if i < 10:
                        i_str = "0" + i_str
                    j_str = str(j)
                    if j < 10:
                        j_str = "0" + j_str
                    port = i_str + j_str
                    self.outports.append("out" + port)
                    self.cells.append((i,j))
        else:
            raise Exception('Type of shocker not implemented yet')

        self.path = '/'
        self.template_environment = Environment(
            autoescape=False,
            loader=FileSystemLoader(templates_dir),
            trim_blocks=False
        )

    ####################################################
    def render_template(self, template_filename, context):
        return self.template_environment.get_template(template_filename).render(context)

    def generate_shocker(self, folder):

        # TODO: hacer diferentes templates-devs para diferentes SHOCKERS
        template_h = 'template-shocker-debt.h'
        template_cpp = 'template-shocker-debt.cpp'

        shocker_name = self.name
        n_outports = self.n_outports
        n_outports_to_shock = self.n_outports_to_shock
        outports = self.outports
        shock_value = self.shock_value
        limit = self.limit

        context = {
            'limit': limit,
            'shock_only_once': 'true' if self.shock_only_once else 'false',
            'atomicClass': shocker_name,
            'atomicClassConstant' : shocker_name.upper(),
            'outPorts': outports,
            'shockValue': shock_value,
            'numberOfOutputPorts' : n_outports,
            'numberOfChosenOutputPorts' : n_outports_to_shock
        }
        with open(folder + shocker_name + '.h', 'w') as f:
            hFile   = self.render_template(template_h, context)
            f.write(hFile)

        with open(folder + shocker_name + '.cpp', 'w') as f:
            cppFile = self.render_template(template_cpp, context)
            f.write(cppFile)
        return True