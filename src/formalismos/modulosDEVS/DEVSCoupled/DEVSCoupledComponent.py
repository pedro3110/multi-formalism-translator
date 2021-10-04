from src.formalismos.modulosDEVS.DEVSInternalConnection import DEVSInternalConnection
from src.formalismos.modulosDEVS.DEVSExternalInputConnection import DEVSExternalInputConnection
from src.formalismos.modulosDEVS.DEVSExternalOutputConnection import DEVSExternalOutputConnection
from src.formalismos.modulosDEVS.DEVSPort import DEVSPort
from src.formalismos.modulosDEVS.DEVSComponent import DEVSComponent
from src.formalismos.modulosDEVS.DEVSCoupled.DEVSBasicCoupledComponent import DEVSBasicCoupledComponent
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSAux import DEVSAux
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSConstant import DEVSConstant
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSGraphical import DEVSGraphical
from src.formalismos.modulosDEVS.DEVSCoupled.DEVSArray import DEVSArray

DEVS_COUPLED_NAME_PREFIX = 'DEVS_COUPLED_'


class DEVSCoupledComponent(DEVSComponent):
    # TODO : buscar una forma de determinar el 'parent' de cada DEVSCoupledComponent. En ppio pareciera no ser
    # TODO : necesario para armar los h, cpp y ma
    ################################################################################
    def __init__(self, xmile_model, root_models, sim_specs,
                 name=None,
                 atomic_components=None, coupled_components=None, 
                 external_input_connections=None, external_output_connections=None, 
                 internal_connections=None,
                 input_ports=None, output_ports=None):
        self.xmile_model = xmile_model
        self.root_models = root_models
        self.sim_specs = sim_specs
        self.type = 'DEVSCoupledComponent'
        self.parent = ''
        
        if name is not None:
            self.name = name
        else:
            self.name = DEVS_COUPLED_NAME_PREFIX + self.xmile_model.get_name()
        
        # Atomic components
        if atomic_components is not None:
            self.atomic_components = atomic_components
        else:
            self.atomic_components = self.set_atomic_components()
        # Coupled components
        if coupled_components is not None:
            self.coupled_components = coupled_components
        else:
            self.coupled_components = self.set_coupled_components()
        # Output Ports
        if output_ports is not None:
            self.output_ports = output_ports
        else:
            self.output_ports = self.set_output_ports()
        # Input Ports
        if input_ports is not None:
            self.input_ports  = input_ports
        else:
            self.input_ports = self.set_input_ports()
        # External input connections
        if external_input_connections is not None:
            self.external_input_connections = external_input_connections
        else:
            self.external_input_connections = self.set_external_input_connections()
        # External output connections
        if external_output_connections is not None:
            self.external_output_connections = external_output_connections
        else:
            self.external_output_connections = self.set_external_output_connections()
        # Internal connections
        if internal_connections is not None:
            self.internal_connections = internal_connections
        else:
            self.internal_connections = self.set_internal_connections()

    ################################################################################
    # Representation functions
    def __repr__(self):
        return str({
            'name': self.name,
            'type': self.type,
            'atomic_components': self.atomic_components,
            'coupled_components': self.coupled_components,
            'external_input_connections': self.external_input_connections,
            'external_output_connections': self.external_output_connections,
            'internal_connections': self.internal_connections,
            'input_ports': self.input_ports,
            'output_ports': self.output_ports
        })

    def __str__(self):
        return str({
            'name': self.name,
            'type': self.type,
            'atomic_components': self.atomic_components,
            'coupled_components': self.coupled_components,
            'external_input_connections': self.external_input_connections,
            'external_output_connections': self.external_output_connections,
            'internal_connections': self.internal_connections,
            'input_ports': self.input_ports,
            'output_ports': self.output_ports
        })

    ################################################################################ 
    # Getters
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

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

    def get_dimensions(self):
        return []
    def get_atomics_array_position(self):
        return {}
    
    ################################################################################
    # Setters    
    def set_atomic_components(self):
        # TODO: mejorar esto..
        SPECIAL_EQ_VALUES = ['TIME']

        xmile_model = self.xmile_model
        sim_specs = self.sim_specs
        
        atomic_components = []
        devs_auxs = []
        devs_graphical = []
        devs_ctes = []
        deps = xmile_model.get_dependencies()
        xmile_ctes, xmile_auxs = [], []

        # Initialize Cte's and Aux's
        auxs = xmile_model.get_auxs()
        for aux in auxs:
            is_dependent = False
            for dep in deps:
                if aux.get_name() == dep.get_name() and len(dep.get_inputs()) > 0:
                    is_dependent = True
            if is_dependent is False:
                xmile_ctes.append(aux)
            else:
                xmile_auxs.append(aux)

        # Ctes
        for xmile_cte in xmile_ctes:
            if 'gf' not in xmile_cte.get_special_behavior() and 'array' not in xmile_cte.get_special_behavior():
                if len(xmile_cte.get_equation().get_special_functions(self.name)) == 0:
                    devs_ctes.append(DEVSConstant(xmile_cte, xmile_model))
                else:
                    aux_dependencies = []
                    for dep in deps:
                        if xmile_cte.get_name() == dep.get_name():
                            aux_dependencies = aux_dependencies + dep.get_inputs()
                    devs_auxs.append(DEVSAux(xmile_cte, xmile_model, []))
            # GRAPHICAL
            elif 'gf' in xmile_cte.get_special_behavior():
                devs_graphical.append(DEVSGraphical(xmile_cte, self.name))
            else:
                assert('array' in xmile_cte.get_special_behavior())

        # Auxs
        for xmile_aux in xmile_auxs:
            if 'gf' not in xmile_aux.get_special_behavior() and 'array' not in xmile_aux.get_special_behavior():
                aux_dependencies = []
                for dep in deps:
                    if xmile_aux.get_name() == dep.get_name():
                        aux_dependencies = aux_dependencies + dep.get_inputs()
                devs_auxs.append(DEVSAux(xmile_aux, xmile_model, aux_dependencies))
            # GRAPHICAL
            elif 'gf' in xmile_aux.get_special_behavior():
                devs_graphical.append(DEVSGraphical(xmile_aux, self.name))
            else:
                assert('array' in xmile_aux.get_special_behavior())

        # Acumulo
        atomic_components = atomic_components + devs_ctes + devs_auxs + devs_graphical
        
        # Atomicos especiales (generados a partir de una ecuacion) (ie.: DEVSPulse)
        for atomic_component in atomic_components:
            special_equation = atomic_component.get_equation()
            special_equation_name = special_equation.get_equation()
            if special_equation_name not in SPECIAL_EQ_VALUES:
                special_atomic_components = special_equation.get_special_functions(self.name)
                atomic_components = atomic_components + special_atomic_components

        return list(set(atomic_components))
    
    def set_coupled_components(self):
        # 1 acoplado por cada modulo
        xmile_modules = self.xmile_model.get_modules()
        xmile_modules_models = []
        for model in self.root_models:
            for module in xmile_modules:
                if model.get_name() == module.get_name():
                    xmile_modules_models.append(model)
        devs_modules = list(map(lambda x: DEVSCoupledComponent(x, self.root_models, self.sim_specs), xmile_modules_models))
        # 1 acoplado por cada Stock (+ Flows asociados)
        devs_generics = self.set_basic_stock_flow_coupleds(self.root_models)
        return devs_modules + devs_generics
    
    def set_output_ports(self):
        output_ports = []
        # 1 output por cada Aux
        for atomic_component in self.get_atomic_components():
            if atomic_component.get_type() in ['DEVSAux', 'DEVSPulse', 'DEVSStep', 'DEVSGraphical', 'DEVSArrayAgregator']:
                for output_port in atomic_component.get_output_ports():
                    output_ports.append(DEVSPort(output_port.get_name(), self, 'out'))
        #  1 output por cada output de cada acoplado
        for coupled_component in self.get_coupled_components():
            for output_port in coupled_component.get_output_ports():
                output_ports.append(DEVSPort(output_port.get_name(), self, 'out'))
        return list(set(output_ports))

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

        # La union de los inputs de los coupled models adentro mio, que son especificamente para Cte's
        for coupled_component in self.get_coupled_components():
            for input_port in coupled_component.get_input_ports():
                if input_port.get_is_for_constant():
                    input_ports.append(DEVSPort(input_port.get_name(), self, 'in'))
        # La union de los inputs provenientes de CoupledModels de los chabones adentro
        # mio que no se corresponden a output's Stocks / Auxs / SpecialFunctions de este DEVSCoupledComponent
        my_internal_output_names = []
        for atomic_component in self.get_atomic_components():
            if atomic_component.get_type() in ['DEVSAux', 'DEVSPulse', 'DEVSStep', 'DEVSGraphical' 'DEVSArrayAgregator']:
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
    
    # External input connections
    def set_external_input_connections(self):
        return self.set_external_input_to_atomic_connections() + self.set_external_input_to_coupled_connections()

    def set_external_input_to_atomic_connections(self):
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
                        if not (component_to.get_type() in ['DEVSAux', 'DEVSPulse', 'DEVSStep', 'DEVSGraphical' 'DEVSArrayAgregator'] and 
                            port_to.get_name() in input_names_matching_components):
                            inputs_atomic_connections.append(
                                DEVSExternalInputConnection(port_from, port_to, component_to)
                            )
        return inputs_atomic_connections

    def set_external_input_to_coupled_connections(self):
        input_coupled_connections = []
        cte_aux_names = list(map(lambda x : x.get_name(), self.get_atomic_components()))
        input_ports = self.get_input_ports()
        for input_port in input_ports:
            port_from = input_port
            for coupled_component in self.get_coupled_components():
                # si el acoplado tiene el puerto de input para esto...
                for coupled_input_port in coupled_component.get_input_ports():
                    if coupled_input_port.get_name() == input_port.get_name() and \
                                    coupled_input_port.get_name() not in cte_aux_names:
                        port_to = coupled_input_port
                        component_to = coupled_component
                        input_coupled_connections.append(
                            DEVSExternalInputConnection(port_from, port_to, component_to)
                        ) 
        return input_coupled_connections

    # External output connections
    def set_external_output_connections(self):
        return self.set_atomic_to_output_connections() + self.set_coupled_to_output_connections()

    def set_atomic_to_output_connections(self):
        atomic_output_connections = []
        for atomic_component in self.get_atomic_components():
            # Solo me interesa guardar el output de los DEVSAux (el resto sirven solo para la internalidad del DCM)
            if atomic_component.get_type() in ['DEVSAux', 'DEVSPulse', 'DEVSStep', 'DEVSGraphical' 'DEVSArrayAgregator']:
                for output_port in atomic_component.get_output_ports():
                    atomic_output_connections.append(DEVSExternalOutputConnection(
                            atomic_component, output_port, DEVSPort(output_port.get_name(), self, 'out'))
                    )
        return atomic_output_connections

    def set_coupled_to_output_connections(self):
        coupled_output_connections = []
        for coupled_component in self.get_coupled_components():
            for output_port in coupled_component.get_output_ports():
                coupled_output_connections.append(DEVSExternalOutputConnection(
                        coupled_component, output_port, DEVSPort(output_port.get_name(), self, 'out'))
                )
        return coupled_output_connections
    
    # Internal connections
    def set_internal_connections(self):
        return self.set_atomic_to_atomic_connections() + self.set_atomic_to_coupled_connections() + \
               self.set_coupled_to_atomic_connections() + self.set_coupled_to_coupled_connections()
    
    def set_atomic_to_atomic_connections(self):
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
    
    def set_atomic_to_coupled_connections(self):
        atomic_to_coupled_connections = []
        for atomic_component_from in self.get_atomic_components():
            for output_port in atomic_component_from.get_output_ports():
                for coupled_component_to in self.get_coupled_components():
                    for input_port in coupled_component_to.get_input_ports():
                        if output_port.get_name() == input_port.get_name():
                            atomic_to_coupled_connections.append(
                                DEVSInternalConnection(output_port, atomic_component_from, input_port, coupled_component_to)
                            )
        return list(set(atomic_to_coupled_connections))

    def set_coupled_to_coupled_connections(self):
        coupled_to_coupled_connections = []
        for coupled_component_from in self.get_coupled_components():
            for output_port in coupled_component_from.get_output_ports():
                for coupled_component_to in self.get_coupled_components():
                    if coupled_component_to != coupled_component_from:
                        for input_port in coupled_component_to.get_input_ports():
                            if output_port.get_name() == input_port.get_name():
                                coupled_to_coupled_connections.append(
                                    DEVSInternalConnection(output_port, coupled_component_from, input_port, coupled_component_to)
                                )
        return list(set(coupled_to_coupled_connections))

    def set_coupled_to_atomic_connections(self):
        coupled_to_atomic_connections = []
        for coupled_component_from in self.get_coupled_components():
            for output_port in coupled_component_from.get_output_ports():
                for atomic_component_to in self.get_atomic_components():
                    for input_port in atomic_component_to.get_input_ports():
                        if output_port.get_name() == input_port.get_name():
                            coupled_to_atomic_connections.append(
                                DEVSInternalConnection(output_port, coupled_component_from, input_port, atomic_component_to)
                            )
        return list(set(coupled_to_atomic_connections))

    ################################################################################
    
    def set_basic_stock_flow_coupleds(self, root_models):
        stocks = self.xmile_model.get_stocks()
        flows = self.xmile_model.get_flows()
        auxs = self.xmile_model.get_auxs()
        deps = self.xmile_model.get_dependencies()

        #############
        coupleds = []

        #############
        # Los stocks que no entran en el if, obtengo/entrego su valor mediante los puertos de input/output
        for stock in stocks:
            if stock.get_access() is None or stock.get_access() != 'input':
                basic_coupled_now = DEVSBasicCoupledComponent(self.xmile_model, root_models, self.sim_specs)
                basic_coupled_now.initialize(flows, self, stock)
                coupleds.append(basic_coupled_now)
        
        #############
        # Proceso los arrays
        xmile_ctes, xmile_auxs = [], []
        for aux in auxs:
            is_dependent = False
            for dep in deps:
                if aux.get_name() == dep.get_name() and len(dep.get_inputs()) > 0:
                    is_dependent = True
            if is_dependent is False:
                xmile_ctes.append(aux)
            else:
                xmile_auxs.append(aux)

        #######
        # Array en Ctes
        for xmile_cte in xmile_ctes:
            if 'array' in xmile_cte.get_special_behavior():
                coupleds.append(DEVSArray(xmile_cte, self.name))
        #######
        # Array en Auxs
        for xmile_aux in xmile_auxs:
            if 'array' in xmile_aux.get_special_behavior():
                coupleds.append(DEVSArray(xmile_aux, self.name))

        return coupleds