from src.modulosCDPP.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSDelay(HCPPDEVSAtomic):

    def run(self, p, atomics_names, devsml_cpp_h_directory, template_delay):
        delay_name = p.get('name') + p.get('parent')
        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + delay_name + extension, 'w+') as f:
                template_now = template_delay + extension

                f.write(self.render_template(template_now, {
                    'delay_name': p.get('name'),
                    'delay_name_lower': delay_name, 'delay_name_upper': delay_name.upper(),

                    'input_parameter': list(filter(lambda x: x.get('name') == 'input_parameter',
                                              p.find('parameters').findall('parameter')))[0].text,
                    'delay_parameter': list(filter(lambda x: x.get('name') == 'delay_parameter',
                                              p.find('parameters').findall('parameter')))[0].text,
                    'initial_delay_parameter': list(filter(lambda x: x.get('name') == 'initial_delay_parameter',
                                                      p.find('parameters').findall('parameter')))[0].text,

                    'output_ports': list(map(lambda x: x.get('name'), p.find('outputs').findall('output'))),
                    'equation':
                        list(filter(lambda x: x.get('name') == 'equation', p.find('parameters').findall('parameter')))[
                            0].text,
                }))
        atomics_names.append(delay_name)
        return atomics_names