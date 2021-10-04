from src.formalismos.cdpp.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSIntegrator(HCPPDEVSAtomic):

    def run(self, ai, atomics_names, devsml_cpp_h_directory, template_integrator):
        integrator_name = ai.get('name') + ai.get('parent')
        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + integrator_name + extension, 'w+') as f:
                template_now = template_integrator + extension
                f.write(self.render_template(template_now, {
                    'name_full': integrator_name,
                    'name_full_upper': integrator_name.upper(),
                    'name': ai.get('name')
                }))
        atomics_names.append(integrator_name)
        return atomics_names