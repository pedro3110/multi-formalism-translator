from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSCte import HCPPDEVSCte
from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSPulse import HCPPDEVSPulse
from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSStep import HCPPDEVSStep
from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSArrayCollector import HCPPDEVSArrayCollector
from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSArrayAgregator import HCPPDEVSArrayAgregator
from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSAux import HCPPDEVSAux
from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSGraphical import HCPPDEVSGraphical
from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSDelay import HCPPDEVSDelay
from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSUniform import HCPPDEVSUniform
from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSFtot import HCPPDEVSFtot
from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSIntegrator import HCPPDEVSIntegrator


class HCPPAtomicGenerator:

    def __init__(self):
        self.atomicos_parseables = {
            "DEVSArrayCollector": HCPPDEVSArrayCollector,
            "DEVSArrayAgregator": HCPPDEVSArrayAgregator,
            "DEVSAux": HCPPDEVSAux,
            "DEVSFplus": HCPPDEVSAux,
            "DEVSFminus": HCPPDEVSAux,
            "DEVSGraphical": HCPPDEVSGraphical,
            "DEVSPulse": HCPPDEVSPulse,
            "DEVSStep": HCPPDEVSStep,
            "DEVSDelay": HCPPDEVSDelay,
            "DEVSUniform": HCPPDEVSUniform,
            "DEVSFtot": HCPPDEVSFtot,
            "DEVSIntegrator": HCPPDEVSIntegrator
        }
        self.ctes = {
            "DEVSConstant": HCPPDEVSCte
        }

    def run(self, root, cpp_h_templates_filenames, devsml_cpp_h_directory):
        atomics_names = []
        ctes_names_values = []

        # Constantes + RegFile
        for devs_name, hcpp_atomic in self.ctes.items():
            template_name = cpp_h_templates_filenames[devs_name]
            atomics = filter(lambda x: x.get('model') in [devs_name], root.findall('.//atomicRef'))
            hcpp_devs = self.ctes[devs_name]()
            for ai in atomics:
                atomics_names, ctes_names_values = hcpp_devs.run(ai, atomics_names, ctes_names_values,
                                                                 devsml_cpp_h_directory, template_name)

        # Atomicos
        for devs_name, hcpp_atomic in self.atomicos_parseables.items():
            template_name = cpp_h_templates_filenames[devs_name]
            atomics = filter(lambda x: x.get('model') in [devs_name], root.findall('.//atomicRef'))
            hcpp_devs = self.atomicos_parseables[devs_name]()
            for ai in atomics:
                atomics_names = hcpp_devs.run(ai, atomics_names, devsml_cpp_h_directory, template_name)

        return atomics_names, ctes_names_values