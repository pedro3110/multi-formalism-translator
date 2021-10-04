from src.formalismos.cdpp.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSUniform(HCPPDEVSAtomic):

    def run(self, p, atomics_names, devsml_cpp_h_directory, template_uniform):
        uniform_name = p.get('name') + p.get('parent')
        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + uniform_name + extension, 'w+') as f:
                template_now = template_uniform + extension

                f.write(self.render_template(template_now, {
                    'uniform_name': p.get('name'),
                    'uniform_name_lower': uniform_name, 'uniform_name_upper': uniform_name.upper(),

                    'dt': list(filter(lambda x: x.get('name') == 'dt', p.find('parameters').findall('parameter')))[0].text,
                    'min_val':
                        list(filter(lambda x: x.get('name') == 'min_val', p.find('parameters').findall('parameter')))[0].text,
                    'max_val':
                        list(filter(lambda x: x.get('name') == 'max_val', p.find('parameters').findall('parameter')))[0].text,

                    'input_ports': list(map(lambda x: x.get('name'), p.find('inputs').findall('input'))),
                    'output_ports': list(map(lambda x: x.get('name'), p.find('outputs').findall('output'))),
                    'equation':
                        list(filter(lambda x: x.get('name') == 'equation', p.find('parameters').findall('parameter')))[0].text,
                }))
        atomics_names.append(uniform_name)
        return atomics_names