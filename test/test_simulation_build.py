import unittest
import json
import os
from src.traductor.config import PROJECT_DIRECTORY


class SimulationBuildXMILEtoCDPPTest(unittest.TestCase):
    '''
    build  simulations.
    requirements:
        1. set environment variables:
            - CDPP_PATH={local path}/binaries/cdpp_kernel/cdpp_kernel
    '''

    @unittest.skip
    def test_build_teacup(self):
        runs_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas')
        json_file = os.path.join(runs_base, 'teacup.json')
        with open(os.path.join(runs_base, json_file)) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f'cd {PROJECT_DIRECTORY}/{model_directory}/atomics && make clean && make')
                assert(ans == 0)

    # @unittest.skip
    def test_build_cell_devs(self):
        runs_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas')
        json_file = os.path.join(runs_base, 'cell_devs.json')
        with open(os.path.join(runs_base, json_file)) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f'cd {PROJECT_DIRECTORY}/{model_directory}/atomics && make clean && make')
                assert(ans == 0)

    @unittest.skip
    def test_build_delay(self):
        runs_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas')
        json_file = os.path.join(runs_base, 'delay.json')
        with open(os.path.join(runs_base, json_file)) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f'cd {PROJECT_DIRECTORY}/{model_directory}/atomics && make clean && make')
                assert(ans == 0)

    @unittest.skip
    def test_build_lotka_volterra(self):
        runs_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas')
        json_file = os.path.join(runs_base, 'lotka-volterra.json')
        with open(os.path.join(runs_base, json_file)) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f'cd {PROJECT_DIRECTORY}/{model_directory}/atomics && make clean && make')
                assert(ans == 0)

    @unittest.skip
    def test_build_graphical(self):
        runs_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas')
        json_file = os.path.join(runs_base, 'graphical.json')
        with open(os.path.join(runs_base, json_file)) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f'cd {PROJECT_DIRECTORY}/{model_directory}/atomics && make clean && make')
                assert (ans == 0)

    @unittest.skip
    def test_build_pulse(self):
        runs_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas')
        json_file = os.path.join(runs_base, 'pulse.json')
        with open(os.path.join(runs_base, json_file)) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f'cd {PROJECT_DIRECTORY}/{model_directory}/atomics && make clean && make')
                assert (ans == 0)

    @unittest.skip
    def test_build_sir(self):
        runs_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas')
        json_file = os.path.join(runs_base, 'sir.json')
        with open(os.path.join(runs_base, json_file)) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f'cd {PROJECT_DIRECTORY}/{model_directory}/atomics && make clean && make')
                assert (ans == 0)

    @unittest.skip
    def test_build_array(self):
        runs_base = os.path.join(PROJECT_DIRECTORY, 'test/corridas')
        json_file = os.path.join(runs_base, 'array.json')
        with open(os.path.join(runs_base, json_file)) as f:
            for k, d in json.load(f).items():
                model_directory = d['DIR_CDPP']
                ans = os.system(f'cd {PROJECT_DIRECTORY}/{model_directory}/atomics && make clean && make')
                assert (ans == 0)


if __name__ == '__main__':
    unittest.main()
