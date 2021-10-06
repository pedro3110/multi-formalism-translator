import unittest
import json
import sys, os
from src.traductor.xmile_translator import XmileTranslator
from src.formalismos.devs.DEVSGenerator import DEVSGenerator
from src.formalismos.cdpp.HCPPGenerator import HCPPGenerator
from src.traductor.config import ROOT_TEMPLATES


class SimulationExecutionXMILEtoCDPPTest(unittest.TestCase):
    '''
    Requires:
        - previous execution of test_translator.py
        - building each model ('cd model_directory && make')
    '''

    #@unittest.skip
    def test_cell_devs(self):
        archivo_modelos_base = './data/corridas/cell_devs.json'
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR']
                ans = os.system(f'cd {model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                assert ans == 0

    #@unittest.skip
    def test_array(self):
        archivo_modelos_base = './data/corridas/array.json'
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR']
                ans = os.system(f'cd {model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    #@unittest.skip
    def test_delay(self):
        archivo_modelos_base = './data/corridas/delay.json'
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR']
                ans = os.system(f'cd {model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    #@unittest.skip
    def test_graphical(self):
        archivo_modelos_base = './data/corridas/graphical.json'
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR']
                ans = os.system(f'cd {model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    #@unittest.skip
    def test_pulse(self):
        archivo_modelos_base = './data/corridas/pulse.json'
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR']
                ans = os.system(f'cd {model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    #@unittest.skip
    def test_lotka_volterra(self):
        archivo_modelos_base = './data/corridas/lotka-volterra.json'
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR']
                ans = os.system(f'cd {model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    #@unittest.skip
    def test_teacup(self):
        archivo_modelos_base = './data/corridas/teacup.json'
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR']
                ans = os.system(f'cd {model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    #@unittest.skip
    def test_sir(self):
        archivo_modelos_base = './data/corridas/sir.json'
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR']
                ans = os.system(f'cd {model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0


if __name__ == '__main__':
    unittest.main()
