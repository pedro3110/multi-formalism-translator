from src.traductor.Traductor import Traductor
from src.modulosDEVS.DEVSGenerator import DEVSGenerator
from src.modulosCDPP.HCPPGenerator import HCPPGenerator

archivo_modelos_base = './data/corridas/array.json'
t = Traductor(archivo_modelos_base)

devs_gen = DEVSGenerator()
hcpp_gen = HCPPGenerator()
t.run_devs(devs_gen, hcpp_gen)
