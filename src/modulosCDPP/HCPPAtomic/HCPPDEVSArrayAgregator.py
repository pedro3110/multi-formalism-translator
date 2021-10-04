from src.modulosCDPP.HCPPAtomic.HCPPDEVSAtomic import HCPPDEVSAtomic


class HCPPDEVSArrayAgregator(HCPPDEVSAtomic):

    def run(self, dag, atomics_names, devsml_cpp_h_directory, template_dag):
        dag_name = dag.get('name') + dag.get('parent')
        for extension in ['.h', '.cpp']:
            with open(devsml_cpp_h_directory + dag_name + extension, 'w+') as f:
                template_now = template_dag + extension
                f.write(self.render_template(template_now, {
                    'dag_name': dag.get('name'),
                    'dag_name_lower': dag_name, 'dag_name_upper': dag_name.upper(),
                    'input_ports': list(map(lambda x: x.get('name'),
                                            dag.find('inputs').findall('input'))),
                    'output_ports': list(map(lambda x: x.get('name'),
                                             dag.find('outputs').findall('output'))),
                    'dimensions': sorted(list(
                        map(lambda x: {'name': x.get('name'), 'size': x.get('size'), 'position': x.get('position')},
                            dag.find('dimensions').findall('dim'))), key=lambda y: int(y['position'])),
                    'equation': dag.find('parameters').find('parameter').text
                }))
        atomics_names.append(dag_name)
        return atomics_names