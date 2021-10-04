from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSPulse(HCPPDEVSAtomic):

    def run(self, p, atomics_names, devsml_cpp_h_directory, template_pulse):
        pulse_name = p.get('name') + p.get('parent')
        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + pulse_name + extension, 'w+') as f:
                template_now = template_pulse + extension

                f.write(self.render_template(template_now, {
                    'pulse_name': p.get('name'),
                    'pulse_name_lower': pulse_name, 'pulse_name_upper': pulse_name.upper(),
                    'output_ports': list(map(lambda x: x.get('name'), p.find('outputs').findall('output'))),
                    'equation':
                        list(filter(lambda x: x.get('name') == 'equation', p.find('parameters').findall('parameter')))[0].text,

                    'volume_param': list(filter(lambda x: x.get('name') == 'volume_param',p.find('parameters').findall('parameter')))[0].text,
                    'volume_input': list(filter(lambda x: x.get('name') == 'volume_input',p.find('parameters').findall('parameter')))[0].text,
                    'firstPulse_input': list(filter(lambda x: x.get('name') == 'firstPulse_input',p.find('parameters').findall('parameter')))[0].text,

                    'interval_param': list(filter(lambda x: x.get('name') == 'interval_param',p.find('parameters').findall('parameter')))[0].text,
                    'interval_input': list(filter(lambda x: x.get('name') == 'interval_input',p.find('parameters').findall('parameter')))[0].text,

                    'dt': list(filter(lambda x: x.get('name') == 'dt', p.find('parameters').findall('parameter')))[0].text
                }))
        atomics_names.append(pulse_name)
        return atomics_names