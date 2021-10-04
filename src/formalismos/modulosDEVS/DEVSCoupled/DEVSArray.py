from src.formalismos.modulosDEVS.DEVSPort import DEVSPort
from src.formalismos.modulosDEVS.DEVSInternalConnection import DEVSInternalConnection
from src.formalismos.modulosDEVS.DEVSExternalInputConnection import DEVSExternalInputConnection
from src.formalismos.modulosDEVS.DEVSExternalOutputConnection import DEVSExternalOutputConnection
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSAtomicComponent import DEVSAtomicComponent
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSAux import DEVSAux
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSGraphical import DEVSGraphical
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSArrayCollector import DEVSArrayCollector

from src.formalismos.modulosXMILE.Auxiliary import Aux

import xml.etree.cElementTree as etree


class DEVSArray(DEVSAtomicComponent):
    def __init__(self, xmile_aux, parent_name):
        # TODO : llamar constructor del parent : in Python 2 use super(DEVSPulse, self).__init__()
        self.xmile_aux = xmile_aux
        # TODO: chequear que este assert este efectivamente mal
        #assert(self.xmile_aux.get_equation() is None)

        #
        self.destiny_name = ''
        self.parent = parent_name
        self.extra_inputs = []
        self.name = self.set_name()
        self.type = 'DEVSArray'

        self.special_behavior = self.xmile_aux.get_special_behavior()
        self.coupled_components = []

        self.atomic_components = self.set_atomic_components()
        self.input_ports = self.set_input_ports()
        self.output_ports = self.set_output_ports()
        self.external_input_connections = self.set_external_input_connections()
        self.external_output_connections = self.set_external_output_connections()
        self.internal_connections = self.set_internal_connections()
        self.input_ports = self.set_input_ports()
        self.output_ports = self.set_output_ports()

    ################################################################
    # Repr
    def __repr__(self):
        return str({
            'name': self.name
        })

    def __str__(self):
        return str({
            'name': self.name
        })

    ################################################################
    def get_atomic_components(self):
        return self.atomic_components

    def get_coupled_components(self):
        return self.coupled_components

    def get_external_input_connections(self):
        return self.external_input_connections

    def get_external_output_connections(self):
        return self.external_output_connections

    def get_internal_connections(self):
        return self.internal_connections

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    ################################################################
    # Setters
    def set_atomic_components(self):
        dimensions = self.special_behavior['array']['dimensions']
        sim_specs = self.special_behavior['array']['sim_specs']
        components = self.special_behavior['array']['elements']

        auxs = []
        for component in components:
            # Genero Aux
            aux = etree.Element("aux")
            aux.attrib['name'] = component['name']
            aux.attrib['subscript'] = component['subscript']

            if 'equation' in component and component['equation'] is not None:
                eqn = etree.Element("eqn")
                eqn.text = component['equation']
                aux.insert(0, eqn)

                #print component['equation']

            if 'gf' in component:
                gf = etree.Element("gf")
                xscale = etree.Element("xscale")
                yscale = etree.Element("yscale")
                ypts = etree.Element("ypts")

                xscale.attrib['min'] = component['gf']['xscale']['min']
                xscale.attrib['max'] = component['gf']['xscale']['max']
                yscale.attrib['min'] = component['gf']['yscale']['min']
                yscale.attrib['max'] = component['gf']['yscale']['max']
                ypts.text = component['gf']['ypts']

                gf.insert(0, xscale)
                gf.insert(1, yscale)
                gf.insert(2, ypts)

                if 'equation' in component['gf']:
                    equation_internal = etree.Element("eqn")
                    equation_internal.text = component['gf']['equation']
                    gf.insert(3, equation_internal)

                aux.insert(1,gf)

            # Agrego XMILEAux
            auxs.append( aux )
        
        #########
        # TODO: verificar . Seguramente hay casos en los que es necesario pasar
        # las dependencies por aca para definir input ports
        aux_dependencies = []

        #########
        # Generar los atomicos correspondientes a cada celda del array
        xmile_auxs = list(map(lambda x: Aux(x, "", self.get_name(), sim_specs, dimensions, False), auxs))
        devs_auxs, devs_graphical = [], []
        for xmile_aux in xmile_auxs:
            # Funcion normal
            if 'gf' not in xmile_aux.get_special_behavior() and 'array' not in xmile_aux.get_special_behavior():
                devs_auxs.append(DEVSAux(xmile_aux, None, aux_dependencies))
            # GRAPHICAL
            elif 'gf' in xmile_aux.get_special_behavior():
                devs_graphical.append(DEVSGraphical(xmile_aux, self.get_name()))
            else:
                raise Exception('Error: xmile_aux')

        #########
        # Generar atomico extra (debe conocer a todas las funciones de las cuales va a leer)
        devs_array_collector = [DEVSArrayCollector(self.get_name(), dimensions, devs_auxs + devs_graphical)]
        
        #########
        return devs_auxs + devs_graphical + devs_array_collector

    def set_parent(self, parent_name):
        self.parent = parent_name

    def set_name(self, suffix=''):
        if suffix == '':
            name = self.xmile_aux.get_name()
            return name
        else:
            name = self.xmile_aux.get_name() + suffix
            self.name = name
            return name

    def set_input_ports(self):
        input_ports = []
        # TODO : agregar input ports a Aux's (prestar atencion si el Aux tiene adentro un specialFunction, influye?)
        # La union de los inputs de los Const's que tengo adentro
        for atomic_component in self.get_atomic_components():
            # no sabemos si el input de estos atomicos va a venir de afuera o de algun otra acoplado interno
            if atomic_component.get_type() == 'DEVSConstant':
                for input_port in atomic_component.get_input_ports():
                    # Chequeo que el input no se corresponda a una special function, sino a la Cte propiamente
                    if input_port.get_component().get_name() == 'DEVSConstant':
                        input_ports.append(DEVSPort(input_port.get_name(), self, 'in', True))

        # La union de los inputs provenientes de CoupledModels de los chabones adentro
        # mio que no se corresponden a output's Stocks / Auxs / SpecialFunctions de este DEVSCoupledComponent
        my_internal_output_names = []
        for atomic_component in self.get_atomic_components():
            if atomic_component.get_type() in ['DEVSAux', 'DEVSPulse', 'DEVSGraphical', 'DEVSArrayAgregator']:
                atomic_outputs = atomic_component.get_output_ports()
                my_internal_output_names = my_internal_output_names + list(map(lambda x : x.get_name(), atomic_outputs))
        for coupled_component in self.get_coupled_components():
            basic_coupled_outputs = coupled_component.get_output_ports()
            for output_port in basic_coupled_outputs:
                my_internal_output_names.append(output_port.get_name())
        # Agrego inputs
        for atomic_component in self.get_atomic_components():
            for input_port in atomic_component.get_input_ports():
                if input_port.get_name() not in my_internal_output_names:
                    input_ports.append(DEVSPort(input_port.get_name(), self, 'in'))
        for coupled_component in self.get_coupled_components():
            for input_port in coupled_component.get_input_ports():
                if input_port.get_name() not in my_internal_output_names:
                        input_ports.append(DEVSPort(input_port.get_name(), self, 'in'))
        input_ports = list(set(input_ports))
        return input_ports

    def set_output_ports(self, default=[]):
        return [DEVSPort(self.name, self, 'out')]

    def set_external_input_connections(self):
        # SOLAMENTE HAY ENTRE ATOMICOS!
        flatten = lambda l: [item for sublist in l for item in sublist]
        inputs_atomic_connections = []
        input_ports = self.get_input_ports()
        # TODO : esta forma de filtrar las conexiones que ya tienen una componente matcheada funciona?
        input_names_matching_components = []
        for input_port in input_ports:
            for atomic_component in self.get_atomic_components():
                if input_port.get_name() == atomic_component.get_name():
                    input_names_matching_components.append(input_port.get_name())
        for input_port in input_ports:
            port_from = input_port
            for atomic_component in self.get_atomic_components():
                for atomic_input_port in atomic_component.get_input_ports():
                    if atomic_input_port.get_name() == input_port.get_name():
                        port_to = atomic_input_port
                        component_to = atomic_component
                        if not (component_to.get_type() in ['DEVSAux', 'DEVSPulse', 'DEVSGraphical', 'DEVSArrayAgregator', 'DEVSArrayCollector'] 
                            and port_to.get_name() in input_names_matching_components):
                            inputs_atomic_connections.append(
                                DEVSExternalInputConnection(port_from, port_to, component_to)
                            )
        return inputs_atomic_connections

    def set_external_output_connections(self):
        # SOLAMENTE HAY ENTRE ATOMICOS!
        atomic_output_connections = []
        for atomic_component in self.get_atomic_components():
            # Solo me interesa guardar el output de los DEVSAux (el resto sirven solo para la internalidad del DCM)
            if atomic_component.get_type() in ['DEVSArrayCollector']:
                for output_port in atomic_component.get_output_ports():
                    atomic_output_connections.append(DEVSExternalOutputConnection(
                            atomic_component, output_port, DEVSPort(output_port.get_name(), self, 'out'))
                    )
        return atomic_output_connections

    def set_internal_connections(self):
        # SOLAMENTE HAY ENTRE ATOMICOS!
        atomic_to_atomic_connections = []
        for atomic_component_from in self.get_atomic_components():
            for output_port in atomic_component_from.get_output_ports():
                for atomic_component_to in self.get_atomic_components():
                    # Atomico destino debe ser distinto del atomico origen para que haya una conexion de uno al otro
                    if atomic_component_from != atomic_component_to:
                        for input_port in atomic_component_to.get_input_ports():
                            if output_port.get_name() == input_port.get_name():
                                atomic_to_atomic_connections.append(DEVSInternalConnection(
                                        output_port, atomic_component_from, input_port, atomic_component_to)
                                )
        return list(set(atomic_to_atomic_connections))

    ################################################################
    # Getters
    def get_name(self):
        return self.name

    def get_parent_name(self):
        return self.parent

    def get_type(self):
        return self.type

    def get_equation(self):
        return self.equation

    def get_input_ports(self):
        return self.input_ports

    def get_output_ports(self):
        return self.output_ports

    def get_parameters(self):
        return self.equation.get_parameters()

    # devuelve todo lo que sea alfanumerico
    def get_variables(self):
        return []

    def get_all_inputs(self):
        return self.get_variables()

    def parameters(self):
        p = {  
            
        }
        return p