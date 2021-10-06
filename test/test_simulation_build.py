import unittest
import json
import os


class SimulationBuildXMILEtoCDPPTest(unittest.TestCase):
    '''
    build  simulations.
    requirements:
        1. set environment variables:
            - CDPP_PATH={local path}/binaries/cdpp_kernel/cdpp_kernel
    '''

    # @unittest.skip
    def test_build_simulations(self):
        runs_base = './data/corridas'
        for json_file in os.listdir(runs_base):
            with open(os.path.join(runs_base, json_file)) as f:
                for k, d in json.load(f).items():
                    model_directory = d['DIR']
                    ans = os.system(f'cd {model_directory}/atomics && make clean && make')


if __name__ == '__main__':
    unittest.main()
