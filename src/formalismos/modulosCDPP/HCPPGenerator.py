from src.formalismos.modulosCDPP.HCPPAtomic.HCPPAtomicGenerator import HCPPAtomicGenerator
from src.formalismos.modulosCDPP.cdpp_model import CdppModel
from src.formalismos.modulosCDPP.cdpp_model_to_ma_file import CdppModelToMaConverter
from src.formalismos.modulosCDPP.preprocessing import preprocessing_devsml_for_ma
from src.formalismos.modulosCDPP.HCPPConfiguration.HCPPEvents import HCPPEvents
from src.formalismos.modulosCDPP.HCPPConfiguration.HCPPRegFile import HCPPRegFile
import xml.etree.ElementTree as etree


class HCPPGenerator:

    def generateHCPP(self, devsml_top_filename, devsml_cpp_h_directory, cpp_h_templates_filenames,
                     devsml_events_filename, devsml_ma_filename):

        ####################
        # Parse DEVSML file
        with open(devsml_top_filename, 'r') as xml_file:
            parser = etree.XMLParser(encoding="utf-8")
            xml_tree = etree.parse(xml_file, parser=parser)
        root = xml_tree.getroot()

        ####################
        # Simulation specs
        sim_specs = {x.get('name'): x.text for x in root.find('sim_specs').findall('spec')}

        generator = HCPPAtomicGenerator()
        atomics_names, ctes_names_values = generator.run(root, cpp_h_templates_filenames, devsml_cpp_h_directory)

        ####################
        # Events
        hcpp_events = HCPPEvents()
        template_events = cpp_h_templates_filenames['events']
        hcpp_events.run(ctes_names_values, devsml_events_filename, template_events)

        ####################
        # Reg File
        hcpp_reg_file = HCPPRegFile()
        template_reg = cpp_h_templates_filenames['reg']
        hcpp_reg_file.run(atomics_names, devsml_cpp_h_directory, template_reg)

        ####################
        # MA File + Preprocessing of DEVSML File
        devs_ml_model = preprocessing_devsml_for_ma(etree.parse(devsml_top_filename))
        cdpp_model = CdppModel.from_devsml_xml(devs_ml_model)
        mafile = CdppModelToMaConverter.parse_model(cdpp_model)
        with open(devsml_ma_filename, 'w') as f:
            f.write(str(mafile))