import unittest
import json
import os
from src.traductor.config import PROJECT_DIRECTORY


class SimulationExecutionXMILEtoCDPPTest(unittest.TestCase):
    '''
    Requires:
        - previous execution of test_translator.py
        - building each model ('cd model_directory && make')
    '''

    #@unittest.skip
    def test_teacup(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/teacup.json')
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f' cd {PROJECT_DIRECTORY}/{model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    # @unittest.skip
    def test_cell_devs(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/cell_devs.json')
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f' cd {PROJECT_DIRECTORY}/{model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                assert ans == 0

    # @unittest.skip
    def test_array(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/array.json')
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f' cd {PROJECT_DIRECTORY}/{model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    # @unittest.skip
    def test_delay(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/delay.json')
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f' cd {PROJECT_DIRECTORY}/{model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    # @unittest.skip
    def test_graphical(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/graphical.json')
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f' cd {PROJECT_DIRECTORY}/{model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    # @unittest.skip
    def test_pulse(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/pulse.json')
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f' cd {PROJECT_DIRECTORY}/{model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    # @unittest.skip
    def test_lotka_volterra(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/lotka-volterra.json')
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f' cd {PROJECT_DIRECTORY}/{model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0

    # @unittest.skip
    def test_sir(self):
        archivo_modelos_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas/sir.json')
        with open(archivo_modelos_base) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f' cd {PROJECT_DIRECTORY}/{model_directory} && atomics/bin/cd++ -mmafile.ma -eevents.ev -t00:01:00:00:000')
                # assert ans == 0


if __name__ == '__main__':
    unittest.main()
