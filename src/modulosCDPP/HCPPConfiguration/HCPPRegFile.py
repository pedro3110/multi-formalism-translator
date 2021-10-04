from src.modulosCDPP.HCPPConfiguration.HCPPConfiguration import HCPPConfiguration


class HCPPRegFile(HCPPConfiguration):

    def run(self, atomics_names, devsml_cpp_h_directory, template_reg):
        with open(devsml_cpp_h_directory + 'reg.cpp', 'w+') as f:
            f.write(self.render_template(template_reg, {'atomics_names': atomics_names}))