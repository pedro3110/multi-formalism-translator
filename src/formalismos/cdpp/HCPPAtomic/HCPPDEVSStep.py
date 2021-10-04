from src.formalismos.cdpp.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSStep(HCPPDEVSAtomic):

    def run(self, p, atomics_names, devsml_cpp_h_directory, template_step):
        step_name = p.get('name') + p.get('parent')
        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + step_name + extension, 'w+') as f:
                template_now = template_step + extension

                f.write(self.render_template(template_now, {
                    'step_name': p.get('name'),
                    'step_name_lower': step_name, 'step_name_upper': step_name.upper(),
                    'output_ports': list(map(lambda x: x.get('name'), p.find('outputs').findall('output'))),
                    'equation':
                        filter(lambda x: x.get('name') == 'equation', 
                            p.find('parameters').findall('parameter'))[0].text,

                    'height_param': filter(lambda x: x.get('name') == 'height_param',
                                           p.find('parameters').findall('parameter'))[0].text,
                    'height_input': filter(lambda x: x.get('name') == 'height_input',
                                           p.find('parameters').findall('parameter'))[0].text,
                    'time_input': filter(lambda x: x.get('name') == 'time_input',
                                               p.find('parameters').findall('parameter'))[0].text
                }))
        atomics_names.append(step_name)
        return atomics_names