from src.formalismos.modulosCDPP.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSArrayCollector(HCPPDEVSAtomic):

    def run(self, dac, atomics_names, devsml_cpp_h_directory, template_dac):
        dac_name = dac.get('name') + dac.get('parent')

        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + dac_name + extension, 'w+') as f:
                template_now = template_dac + extension
                f.write(self.render_template(template_now, {
                    'dac_name': dac.get('name'),
                    'dac_name_lower': dac_name, 'dac_name_upper': dac_name.upper(),
                    'input_ports': list(map(lambda x: x.get('name'),
                                            dac.find('inputs').findall('input'))),
                    'output_ports': list(map(lambda x: x.get('name'),
                                             dac.find('outputs').findall('output'))),
                    'dimensions': sorted(list(map(lambda x: {
                        'name': x.get('name'), 'size': x.get('size'), 'position': x.get('position')},
                                                  dac.find('dimensions').findall('dim'))),
                                         key=lambda y: int(y['position'])),
                    'array_position_name_map_list': sorted(list({
                                                                    tuple(list(map(lambda y: int(y) - 1,
                                                                                   x.get('position').split(
                                                                                       ',')))): x.get('name')
                                                                    for x in
                                                                    dac.find('atomics_array_position').findall(
                                                                        'aap')
                                                                    }.items()))
                }))
        atomics_names.append(dac_name)
        return atomics_names