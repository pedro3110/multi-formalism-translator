from src.modulosCDPP.HCPPConfiguration.HCPPConfiguration import HCPPConfiguration


class HCPPEvents(HCPPConfiguration):

    def run(self, ctes_names_values, devsml_events_filename, template_events):
        with open(devsml_events_filename, 'w+') as f:
            f.write(self.render_template(template_events, {
                # Para no repetir los inputs de Ctes que vienen de afuera y van hacia adentro de los acoplados
                'ctes_names_values': [
                    dict(tupleized) for tupleized in
                    set(tuple(item.items()) for item in ctes_names_values)
                    ]
            }))