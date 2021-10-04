from src.formalismos.cdpp.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSFtot(HCPPDEVSAtomic):

    def run(self, at, atomics_names, devsml_cpp_h_directory,template_tot):
        tot_name = at.get('name') + at.get('parent')
        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + tot_name + extension, 'w+') as f:
                template_now = template_tot + extension
                f.write(self.render_template(template_now,
                                        {'tot_name': at.get('name'),
                                         'tot_name_lower': tot_name, 'tot_name_upper': tot_name.upper(),
                                         'plus_input_ports': list(map(lambda y: y.get('name'), filter(
                                             lambda x: x.get('type') == 'in_plus',
                                             at.find('inputs').findall('input')))),
                                         'minus_input_ports': list(map(lambda y: y.get('name'), filter(
                                             lambda x: x.get('type') == 'in_minus',
                                             at.find('inputs').findall('input')))), 'output_ports': list(
                                            map(lambda x: x.get('name'),
                                                at.find('outputs').findall('output')))}))
        atomics_names.append(tot_name)
        return atomics_names