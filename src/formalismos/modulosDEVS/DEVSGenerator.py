import os
from jinja2 import Environment, FileSystemLoader
import xml.etree.ElementTree as etree
import vkbeautify as vkb
from collections import defaultdict
from src.formalismos.modulosDEVS.DEVSCoupled.DEVSCoupledComponent import DEVSCoupledComponent
from src.formalismos.modulosXMILE.Model import Model
import logging


class DEVSGenerator:

    def __init__(self, root_templates):
        self.root_templates = root_templates

    def generateDEVSML(self, dir_xmile, devsml_template_filename, devsml_top_filename):
        source_xmlns = "{http://docs.oasis-open.org/xmile/ns/XMILE/v1.0}"
        source_xmlns_isee = "{http://iseesystems.com/XMILE}"

        # Auxiliary functions
        parser = etree.XMLParser(encoding="utf-8")
        with open(dir_xmile, 'r') as xml_file:
            xml_tree = etree.parse(xml_file, parser=parser)
        root = xml_tree.getroot()

        # Get simulation parameters
        sim_specs, sim_specs_tag = defaultdict(), root.find(source_xmlns + 'sim_specs')
        # TODO: que es instantaneous_flows?
        sim_specs['instantaneous_flows'] = sim_specs_tag.get(source_xmlns_isee + 'instantaneous_flows')

        # TODO: que es simulation_delay?
        sim_specs['simulation_delay'] = sim_specs_tag.get(source_xmlns_isee + 'simulation_delay')

        sim_specs['time_units'] = sim_specs_tag.get('time_units')
        sim_specs['start'] = sim_specs_tag.find(source_xmlns + 'start').text
        sim_specs['stop'] = sim_specs_tag.find(source_xmlns + 'stop').text
        sim_specs['dt'] = sim_specs_tag.find(source_xmlns + 'dt').text

        # Get models
        models_element = root.findall(source_xmlns + 'model')
        dimensions_element = root.find(source_xmlns + 'dimensions')

        # TODO: parametrizar esto
        DEBUG = False
        models_parsed = list(map(lambda x: Model(x, sim_specs, dimensions_element, DEBUG), models_element))

        # Template
        TEMPLATE_ENVIRONMENT = Environment(autoescape=False,
                                           loader=FileSystemLoader(self.root_templates),
                                           trim_blocks=False)

        def render_template(template_filename, context):
            return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

        # Code
        for model in models_parsed:
            logging.info('GENERATE MODEL : ' + model.get_name())
        ##
        top_model = models_parsed[0]
        dm = DEVSCoupledComponent(top_model, models_parsed, sim_specs)

        filenames = []
        sim_specs_val = [sim_specs, None]

        def traverse(dm, level):
            name = dm.get_name()
            dst_filename = name

            # Accumulate all names for deleting later
            filenames.append(name)

            ccs = dm.get_coupled_components()
            ccs_names = []

            # Recursion
            for cc in ccs:
                traverse(cc, level+1)
                ccs_names.append(cc.get_name())

            # Generate xml
            context = {
                'sim_specs': sim_specs_val[int(level > 0)],
                'type': dm.get_type(),
                'coupled_name': name,
                'coupled_filenames': ccs_names,
                'atomics': dm.get_atomic_components(),
                'input_ports': dm.get_input_ports(),
                'output_ports': dm.get_output_ports(),
                'internal_connections': dm.get_internal_connections(),
                'external_input_connections': dm.get_external_input_connections(),
                'external_output_connections': dm.get_external_output_connections()
            }
            coupled_xml = render_template(devsml_template_filename, context)

            # Cargo los 'include' del modelo
            from xml.etree import ElementTree as et
            tree = et.fromstring(coupled_xml)
            includes = tree.findall('.//include')

            for include in includes:
                include_filename = include.get('filename')
                include_tree = et.parse(include_filename)

                for element in tree.iter():
                    if element.tag == 'include' and element.get('filename') == include_filename:
                        tree.find('components').append(include_tree.getroot())

            tree2 = et.tostring(tree)
            with open(dst_filename, 'wb') as f:
                f.write(tree2)

        traverse(dm, 0)

        # Pretty print
        with open('DEVS_COUPLED_top', 'r') as xml_file_new:
            parser = etree.XMLParser(encoding="utf-8")
            xml_tree_new = etree.parse(xml_file_new, parser=parser)
        root = xml_tree_new.getroot()

        # Erase includes
        for elem in root.iter():
            for child in list(elem):
                if child.tag == 'include':
                    elem.remove(child)
        x = etree.tostring(root)
        vkb.xml(x.decode('utf-8'), devsml_top_filename)

        # Erase unneeded files
        for filename in filenames:
            os.remove(filename)
