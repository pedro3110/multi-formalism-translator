from src.formalismos.cdpp.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSAux(HCPPDEVSAtomic):

    def run(self, aa, atomics_names, devsml_cpp_h_directory, template_aux):
        aux_name = aa.get('name') + aa.get('parent')
        parameters = aa.find('parameters').findall('parameter')
        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + aux_name + extension, 'w+') as f:
                template_now = template_aux + extension
                elems =  {
                    'aux_name': aa.get('name'),
                    'aux_name_lower': aux_name, 'aux_name_upper': aux_name.upper(),
                    'input_ports': list(map(lambda x: x.get('name'), aa.find('inputs').findall('input'))),
                    'output_ports': list(map(lambda x: x.get('name'), aa.find('outputs').findall('output')))
                    # 'equation': aa.find('parameters').find('parameter').text
                }
                for param in parameters:
                    elems[param.get('name')] = param.text
                    
                f.write(self.render_template(template_now, elems))
        # por ahora el unico parametero posible es 'equation' aca } ))
        atomics_names.append(aux_name)
        return atomics_names