from src.traductor.xmile_translator import XmileTranslator
from src.formalismos.devs import DEVSGenerator
from src.formalismos.modulosCDPP.HCPPGenerator import HCPPGenerator

archivo_modelos_base = './data/corridas/array.json'
t = XmileTranslator(archivo_modelos_base)

devs_gen = DEVSGenerator()
hcpp_gen = HCPPGenerator()
t.run_devs(devs_gen, hcpp_gen)
