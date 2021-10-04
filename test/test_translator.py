import unittest
from src.traductor.Traductor import Traductor
from src.modulosDEVS.DEVSGenerator import DEVSGenerator
from src.modulosCDPP.HCPPGenerator import HCPPGenerator
from src.traductor.config import ROOT_TEMPLATES

class ArrayTest(unittest.TestCase):

    @unittest.skip
    def test_array(self):
        archivo_modelos_base = './data/corridas/array.json'
        root_templates = ROOT_TEMPLATES
        t = Traductor(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    @unittest.skip
    def test_delay(self):
        archivo_modelos_base = './data/corridas/delay.json'
        root_templates = ROOT_TEMPLATES
        t = Traductor(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    @unittest.skip
    def test_graphical(self):
        archivo_modelos_base = './data/corridas/graphical.json'
        root_templates = ROOT_TEMPLATES
        t = Traductor(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    @unittest.skip
    def test_pulse(self):
        archivo_modelos_base = './data/corridas/pulse.json'
        root_templates = ROOT_TEMPLATES
        t = Traductor(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    @unittest.skip
    def test_lotka_volterra(self):
        archivo_modelos_base = './data/corridas/lotka-volterra.json'
        root_templates = ROOT_TEMPLATES
        t = Traductor(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    @unittest.skip
    def test_teacup(self):
        archivo_modelos_base = './data/corridas/teacup.json'
        root_templates = ROOT_TEMPLATES
        t = Traductor(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    def test_sir(self):
        archivo_modelos_base = './data/corridas/sir.json'
        root_templates = ROOT_TEMPLATES
        t = Traductor(archivo_modelos_base, root_templates)

        devs_gen = DEVSGenerator(root_templates)
        hcpp_gen = HCPPGenerator()
        t.run_devs(devs_gen, hcpp_gen)

    # def test_step_pulse(self):
    #     archivo_modelos_base = './data/corridas/step-pulse.json'
    #     root_templates = ROOT_TEMPLATES
    #     t = Traductor(archivo_modelos_base, root_templates)
    #
    #     devs_gen = DEVSGenerator(root_templates)
    #     hcpp_gen = HCPPGenerator()
    #     t.run_devs(devs_gen, hcpp_gen)

    # def test_step(self):
    #     archivo_modelos_base = './data/corridas/step.json'
    #     root_templates = ROOT_TEMPLATES
    #     t = Traductor(archivo_modelos_base, root_templates)
    #
    #     devs_gen = DEVSGenerator(root_templates)
    #     hcpp_gen = HCPPGenerator()
    #     t.run_devs(devs_gen, hcpp_gen)

    # def test_misc(self):
    #     archivo_modelos_base = './data/corridas/misc.json'
    #     root_templates = ROOT_TEMPLATES
    #     t = Traductor(archivo_modelos_base, root_templates)
    #
    #     devs_gen = DEVSGenerator(root_templates)
    #     hcpp_gen = HCPPGenerator()
    #     t.run_devs(devs_gen, hcpp_gen)

    # def test_cell_devs(self):
    #     archivo_modelos_base = './data/corridas/cell_devs.json'
    #     root_templates = ROOT_TEMPLATES
    #     t = Traductor(archivo_modelos_base, root_templates)
    #
    #     devs_gen = DEVSGenerator(root_templates)
    #     hcpp_gen = HCPPGenerator()
    #     t.run_devs(devs_gen, hcpp_gen)

if __name__ == '__main__':
    unittest.main()
