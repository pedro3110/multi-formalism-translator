import unittest
import os
from src.traductor.xmile_translator import XmileTranslator
from src.formalismos.devs.DEVSGenerator import DEVSGenerator
from src.formalismos.cdpp.HCPPGenerator import HCPPGenerator
from src.traductor.config import PROJECT_DIRECTORY
from src.traductor.config import ROOT_TEMPLATES


class TranslatorXMILEtoCDPPTest(unittest.TestCase):
    '''
    todo: description
    '''
    # @unittest.skip
    def test_teacup(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/teacup.json')
        root_templates = ROOT_TEMPLATES
        t = XmileTranslator(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    #@unittest.skip
    def test_cell_devs(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/cell_devs.json')
        root_templates = ROOT_TEMPLATES
        t = XmileTranslator(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    #@unittest.skip
    def test_array(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/array.json')
        root_templates = ROOT_TEMPLATES
        t = XmileTranslator(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    #@unittest.skip
    def test_delay(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/delay.json')
        root_templates = ROOT_TEMPLATES
        t = XmileTranslator(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    #@unittest.skip
    def test_graphical(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/graphical.json')
        root_templates = ROOT_TEMPLATES
        t = XmileTranslator(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    #@unittest.skip
    def test_pulse(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/pulse.json')
        root_templates = ROOT_TEMPLATES
        t = XmileTranslator(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    #@unittest.skip
    def test_lotka_volterra(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/lotka-volterra.json')
        root_templates = ROOT_TEMPLATES
        t = XmileTranslator(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    #@unittest.skip
    def test_sir(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/sir.json')
        root_templates = ROOT_TEMPLATES
        t = XmileTranslator(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)


if __name__ == '__main__':
    unittest.main()
