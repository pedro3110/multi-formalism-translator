import os
from jinja2 import Environment, FileSystemLoader
from src.traductor.config import ROOT_TEMPLATES

class HCPPConfiguration:

    def render_template(self, template_filename, context):
        TEMPLATE_ENVIRONMENT = Environment(autoescape=False,
                                           loader=FileSystemLoader(ROOT_TEMPLATES),
                                           trim_blocks=False)
        return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)