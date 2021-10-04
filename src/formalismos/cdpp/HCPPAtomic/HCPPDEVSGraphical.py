from src.formalismos.cdpp.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSGraphical(HCPPDEVSAtomic):

    def run(self, dg, atomics_names, devsml_cpp_h_directory, template_time):
        graphical_name = dg.get('name') + dg.get('parent')
        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + graphical_name + extension, 'w+') as f:
                template_now = template_time + extension
                f.write(self.render_template(template_now, {
                    'graphical_name': dg.get('name'),
                    'graphical_name_lower': graphical_name, 'graphical_name_upper': graphical_name.upper(),
                    'xscale_min':
                        list(filter(lambda x: x.get('name') == 'xscale_min', dg.find('parameters').findall('parameter')))[0].text,
                    'xscale_max':
                        list(filter(lambda x: x.get('name') == 'xscale_max', dg.find('parameters').findall('parameter')))[0].text,
                    'yscale_min':
                        list(filter(lambda x: x.get('name') == 'yscale_min', dg.find('parameters').findall('parameter')))[0].text,
                    'yscale_max':
                        list(filter(lambda x: x.get('name') == 'yscale_max', dg.find('parameters').findall('parameter')))[0].text,
                    'ypts': list(filter(lambda x: x.get('name') == 'ypts', dg.find('parameters').findall('parameter')))[0].text,
                    'equation':
                        list(filter(lambda x: x.get('name') == 'equation', dg.find('parameters').findall('parameter')))[0].text,
                    'input_ports': list(map(lambda x: x.get('name'), dg.find('inputs').findall('input'))),
                    'output_ports': list(map(lambda x: x.get('name'), dg.find('outputs').findall('output')))
                }))
        atomics_names.append(graphical_name)
        return atomics_names