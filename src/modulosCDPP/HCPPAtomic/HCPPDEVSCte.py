from src.modulosCDPP.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSCte(HCPPDEVSAtomic):

    def run(self, ac, atomics_names, ctes_names_values, devsml_cpp_h_directory, template_cte):

        cte_name = ac.get('name')
        cte_full_name = cte_name + ac.get('parent')
        cte_value = filter(lambda x: x.get('name') == 'value', ac.find('parameters').findall('parameter'))[0].text
        atomics_names.append(cte_full_name)

        # TODO : ver esto. Son los casos en los que la Cte esta adentro de nn acoplado, y recibe input
        # TODO : proveniente de un Aux de mas arriba
        # Events File
        def is_numeric(text):
            try:
                float(text)
                return True
            except ValueError:
                return False

        if is_numeric(cte_value):
            ctes_names_values.append({'cte_name': cte_name, 'cte_value': cte_value})

        # DEVSConstant
        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + cte_full_name + extension, 'w+') as f:
                template_now = template_cte + extension
                f.write(self.render_template(template_now,
                                             {'cte_name_lower': cte_full_name, 'cte_name_upper': cte_full_name.upper(),
                                              'cte_name': cte_name,
                                              'input_ports': list(map(lambda x: x.get('name'),
                                                                  ac.find('inputs').findall('input'))),
                                              'output_ports': list(map(lambda x: x.get('name'),
                                                                   ac.find('outputs').findall(
                                                                      'output')))}
                                             )
                        )
        return atomics_names, ctes_names_values