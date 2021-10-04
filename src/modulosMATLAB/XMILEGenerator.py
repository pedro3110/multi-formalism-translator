from jinja2 import DictLoader, Environment, FileSystemLoader
import os
import re
import xml.etree.ElementTree as etree
from py_expression_eval import Parser


class XMILEGenerator(object):
    def __init__(self, matlab_code, xmile_template_filename):
        self.source_xmlns = "{http://docs.oasis-open.org/xmile/ns/XMILE/v1.0}"
        self.source_xmlns_isee = "{http://iseesystems.com/XMILE}"
        self.path = './'
        self.template_environment = Environment(
            autoescape=False,
            loader=FileSystemLoader(os.path.join(self.path, 'root/templates')),
            trim_blocks=False)
        self.xmile_template_filename = xmile_template_filename
        self.matlab_code = matlab_code
        self.context = self.generate_context()

    def render_template(self, template_filename, context):
        return self.template_environment.get_template(template_filename).render(context)

    def generate_xmile(self, xmile_output_filename):
        with open(xmile_output_filename, 'w') as f:
            f.write(self.render_template(self.xmile_template_filename, self.context))

    def generate_context(self):
        parser = Parser()

        # stocks ids
        stocks_ids_re = re.compile(r"[\w]+=x\(\d+\)")
        stocks_ids = {
            re.search(re.compile(r"(.+)="), exp).group(0)[:-1]:
                re.search(re.compile(r"x\((.+)\)"), exp).group(1)
            for exp in stocks_ids_re.findall(self.matlab_code)
            }

        stocks_init_values_re = re.compile(r"x0\(\d+\)=-?\d+[\.\d+]*")
        stocks_init_values_dict = {
            re.search(re.compile(r"x0\((.+)\)"), exp).group(1):
                re.search(re.compile(r"=(.+)"), exp).group(0)[1:]
            for exp in stocks_init_values_re.findall(self.matlab_code)
            }

        # Joineo los 'stocks' con sus valores iniciales Capital=x(1) => x0(1)=300
        stocks_init_values_re = re.compile(r"[\w]+=x\(\d+\)")
        stocks_init_values = {
            re.search(re.compile(r"(.+)="), exp).group(0)[:-1]:
                stocks_init_values_dict[re.search(re.compile(r"x\((.+)\)"), exp).group(1)]
            for exp in stocks_init_values_re.findall(self.matlab_code)
            }

        stocks_change_re = re.compile(r"f\(\d+\)=[\w\(\)\+\-\*\/\.]+")
        stocks_change_dict = {
            re.search(re.compile(r"f\((\d+)\)"), exp).group(1):
                parser.parse(re.search(re.compile(r"=(.+)"), exp).group(0)[1:])
            for exp in stocks_change_re.findall(self.matlab_code)
            }

        # Joineo los 'stocks' con sus rates de cambio Capital=x(1) => f(1)=InvestmentNetReal
        stocks_change = {k: stocks_change_dict[stocks_ids[k]]
                         for k, v in stocks_init_values.iteritems()
                         }

        auxs_init_values_re = re.compile(r"[\w]+=\d+[\.\d+]*")
        auxs_init_values = {
            re.search(re.compile(r"(.+)="), exp).group(0)[:-1]:
                re.search(re.compile(r"=(.+)"), exp).group(0)[1:]
            for exp in auxs_init_values_re.findall(self.matlab_code)
            }

        auxs_equations_re = re.compile(r"[\w]+=[\w\(\)\+\-\*\/\.]+")
        auxs_equations = {
            re.search(re.compile(r"(.+)="), exp).group(0)[:-1]:
                parser.parse(re.search(re.compile(r"=(.+)"), exp).group(0)[1:])
            for exp in auxs_equations_re.findall(self.matlab_code)[1:]
            if re.search(re.compile(r"(.+)="), exp).group(0)[:-1] not in
            auxs_init_values.keys() + stocks_init_values.keys()
            }

        # Estructura de datos con informacion de stocks / flows / auxs
        stocks = [
            {'name': k, 'eqn': v, 'inflow': 'chg' + k}
            for k, v in stocks_init_values.iteritems()
            ]
        flows = [
            {'name': 'chg' + k, 'eqn': stocks_change[k].toString()}
            for k, v in stocks_init_values.iteritems()
            ]

        # Auxs : definidas de forma DIRECTA / INDIRECTA
        auxs = [
                   {'name': k, 'eqn': v.toString()}
                   for k, v in auxs_equations.iteritems()
                   ] + [
                   {'name': k, 'eqn': v}
                   for k, v in auxs_init_values.iteritems()
                   ]

        dependencies = [
                           {'name': 'chg' + k, 'inputs': stocks_change[k].variables()}
                           for k, v in stocks_init_values.iteritems()
                           ] + [
                           {'name': k, 'inputs': v.variables()}
                           for k, v in auxs_equations.iteritems()
                           ]

        # Generacion de archivo XMILE
        model_name = 'test'
        time_start = 1
        time_stop = 5
        time_delta = 0.01
        context = {
            'model_name': model_name,
            'time_start': time_start,
            'time_stop': time_stop,
            'time_delta': time_delta,
            'stocks': stocks,
            'flows': flows,
            'auxs': auxs,
            'dependencies': dependencies
        }
        return context
