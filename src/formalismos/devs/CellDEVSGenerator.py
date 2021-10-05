import os
import xml.etree.ElementTree as etree
import vkbeautify as vkb
from jinja2 import Environment, FileSystemLoader

###################################################################################################################
# Configuraciones
#logging.basicConfig(filename='logs/traductor_cell_devs.log', filemode='w+', level=logging.DEBUG)

class CellDEVSGenerator:

    def render_template(self, template_filename, context):
        # Jinja2
        PATH = '/'
        PATH_TEMPLATES = 'root/templates-devs'
        TEMPLATE_ENVIRONMENT = Environment(
            autoescape=False,
            loader=FileSystemLoader(os.path.join(PATH, PATH_TEMPLATES)),
            trim_blocks=False
        )
        return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

    def generateCellDEVSML(self, cell_devs, dst_file_cell_devs, valfile_generator, dst_valfile):

        # Order:
        # 1. generate valfile
        # 2. generate cell_devs model

        ########### Generate valfile ############
        valfile_rows = valfile_generator.generate()
        with open(dst_valfile, 'w+') as f:
            for row in valfile_rows:
                f.write(row)

        ########### Generate CellDevs model (object => xml) ###########
        for extension in ['.xml']:
            with open('tmp_file.xml', 'w+') as f:
                f.write(self.render_template('template-cell-devs' + extension, {
                    'name': cell_devs.get_name(),
                    'macro': 'macros.inc',
                    'type': cell_devs.get_type(),
                    'dim': cell_devs.get_dim(),
                    'delay': cell_devs.get_delay(),
                    'default_delay_time': cell_devs.get_default_delay_time(),
                    'border_type': cell_devs.get_border_type(),
                    'neighbors': cell_devs.get_neighbors(),
                    'initial_value': cell_devs.get_initial_value(),
                    'zones': cell_devs.get_zones(),

                    'local_transition': cell_devs.get_local_transition(),
                    'rules': cell_devs.get_rules(),
                    'neighbors': cell_devs.get_neighbors(),
                    'input_ports': cell_devs.get_input_ports(),
                    'output_ports': cell_devs.get_output_ports(),
                    'internal_input_connections': cell_devs.get_internal_input_connections(),
                    'internal_output_connections': cell_devs.get_internal_output_connections(),
                    'ports_in_transition': cell_devs.get_ports_in_transition()
                }))
            with open('tmp_file.xml', 'r') as xml_file_new:
                parser = etree.XMLParser(encoding="utf-8")
                xml_tree_new = etree.parse(xml_file_new, parser=parser)
                root = xml_tree_new.getroot()
                x = etree.tostring(root)
                vkb.xml(x, dst_file_cell_devs)
            os.remove('tmp_file.xml')