from jinja2 import Environment, FileSystemLoader
import os

class HCPPConfiguration:

    def render_template(self, template_filename, context):
        # TODO : parametrizar esto
        PATH = './'
        PATH_TEMPLATES = 'root/templates'
        TEMPLATE_ENVIRONMENT = Environment(autoescape=False,
                                           loader=FileSystemLoader(os.path.join(PATH, PATH_TEMPLATES)),
                                           trim_blocks=False)
        return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)