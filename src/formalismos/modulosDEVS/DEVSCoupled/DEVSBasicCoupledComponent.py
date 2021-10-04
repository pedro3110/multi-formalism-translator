from src.formalismos.modulosDEVS.DEVSInternalConnection import DEVSInternalConnection
from src.formalismos.modulosDEVS.DEVSExternalInputConnection import DEVSExternalInputConnection
from src.formalismos.modulosDEVS.DEVSExternalOutputConnection import DEVSExternalOutputConnection
from src.formalismos.modulosDEVS.DEVSPort import DEVSPort
from src.formalismos.modulosDEVS.DEVSComponent import DEVSComponent
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSFpm import DEVSFpm
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSFtot import DEVSFtot
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSIntegrator import DEVSIntegrator
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSGraphical import DEVSGraphical
from src.modulosAuxiliares.Equation import Equation

import logging

DEVS_BASIC_COUPLED_NAME_PREFIX = "DEVS_BASIC_COUPLED_"


class DEVSBasicCoupledComponent(DEVSComponent):

    def __init__(self, xmile_model, root_models, sim_specs,
                 name=None, atomic_components=None, coupled_components=None,
                 external_input_connections=None, external_output_connections=None, internal_connections=None,
                 input_ports=None, output_ports=None, parent_name=None):
        self.xmile_model = xmile_model
        self.root_models = root_models
        self.sim_specs = sim_specs
        self.type = 'DEVSBasicCoupledComponent'
        if name is not None:
            self.name = name
        else:
            self.name = 'DEVS_BASIC_COUPLED_' + self.xmile_model.get_name()

        # Atomic components
        if atomic_components is not None:
            self.atomic_components = atomic_components
        # Coupled components
        if coupled_components is not None:
            self.coupled_components = coupled_components
        # Output Ports
        if output_ports is not None:
            self.output_ports = output_ports
        # Input Ports
        if input_ports is not None:
            self.input_ports = input_ports
        # External input connections
        if external_input_connections is not None:
            self.external_input_connections = external_input_connections
        # External output connections
        if external_output_connections is not None:
            self.external_output_connections = external_output_connections
        # Internal connections
        if internal_connections is not None:
            self.internal_connections = internal_connections
        # Parent name
        if parent_name is not None:
            self.parent = parent_name

    ################################################################################
    # Representation functions
    def __repr__(self):
        return str({'name': self.name, 'type': self.type, 'atomic_components': self.atomic_components,
                    'coupled_components': self.coupled_components,
                    'external_input_connections': self.external_input_connections,
                    'external_output_connections': self.external_output_connections,
                    'internal_connections': self.internal_connections, 'input_ports': self.input_ports,
                    'output_ports': self.output_ports})

    def __str__(self):
        return str({'name': self.name, 'type': self.type, 'atomic_components': self.atomic_components,
                    'coupled_components': self.coupled_components,
                    'external_input_connections': self.external_input_connections,
                    'external_output_connections': self.external_output_connections,
                    'internal_connections': self.internal_connections, 'input_ports': self.input_ports,
                    'output_ports': self.output_ports})

    ################################################################################
    # Setters
    def set_parent(self, parent_name):
        self.parent = parent_name

    def set_name(self, name):
        self.name = name

    def set_atomic_components(self, atomic_components):
        self.atomic_components = atomic_components

    def set_coupled_components(self, coupled_components):
        self.coupled_components = coupled_components

    def set_output_ports(self, output_ports):
        self.output_ports = output_ports

    def set_input_ports(self, input_ports):
        self.input_ports = input_ports

    def set_external_input_connections(self, external_input_connections):
        self.external_input_connections = external_input_connections

    def set_external_output_connections(self, external_output_connections):
        self.external_output_connections = external_output_connections

    def set_internal_connections(self, internal_connections):
        self.internal_connections = internal_connections

    # Getters
    def get_parent(self):
        return self.parent

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

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
        
    # Set full instance
    def initialize(self, xmile_flows, parent_coupled, stock):
        name = DEVS_BASIC_COUPLED_NAME_PREFIX + stock.get_name()
        ###########
        # Acoplados : ninguno
        coupled_components = []
        ###########
        # Atomicos : Ftot + Integrador + Fpm's (recordar que los Cte's y Aux's los sacamos afuera)
        integrator = DEVSIntegrator(stock, name)
        ftot = DEVSFtot(stock, name)
        atomic_components = [integrator, ftot]

        #  (Fpm's + XMILESpecialFunctions)
        special_atomics = []
        devs_fpms = []
        for flow in xmile_flows:
            equation = flow.get_equation()
            # TODO: chequear si esta funcionando poner un GRAPHICAL en un flow (o si o si hay que ponerlo en un aux?)
            # Agrego el Fpm de forma normal
            if equation.get_equation() not in ['TIME']:
                devs_fpms.append(DEVSFpm(flow, [stock], name))
            elif equation.get_equation() == 'TIME':
                # Hago modificaciones necesarias en Fpm de I/O y de valor de la ecuacion
                devs_time = DEVSGraphical(flow, name)
                devs_time.set_name(suffix='_Time')
                devs_time.set_output_ports([DEVSPort(devs_time.get_name(), devs_time, 'out')])
                special_atomics.append(devs_time)
                
                x = DEVSFpm(flow, [stock], name)
                if x.get_fplus() is not None:
                    z = x.get_fplus()
                    z.set_equation(Equation(devs_time.get_name(), False))
                    z.set_input_ports([DEVSPort(devs_time.get_name(), z, 'in')])
                if x.get_fminus() is not None:
                    z = x.get_fminus()
                    z.set_equation(Equation(devs_time.get_name(), False))
                    z.set_input_ports([DEVSPort(devs_time.get_name(), z, 'in')])
                devs_fpms.append(x)

        devs_fps = list(filter(lambda x: x is not None, list(map(lambda x: x.get_fplus(), devs_fpms))))
        devs_fms = list(filter(lambda x: x is not None, list(map(lambda x: x.get_fminus(), devs_fpms))))

        ####
        # EquationSpecialFunctions (correspondientes a Fp's y Fm's)
        # Fp's
        for fp in devs_fps:
            equation = fp.get_equation()
            special_atomics_fps = equation.get_special_functions(name)
            special_atomics = special_atomics + special_atomics_fps
        # Fm's
        for fm in devs_fms:
            equation = fm.get_equation()
            special_atomics_fms = equation.get_special_functions(name)
            special_atomics = special_atomics + special_atomics_fms

        # Set atomic components
        atomic_components = atomic_components + devs_fps + devs_fms + special_atomics

        ###########
        # Inputs :
        #   . necesito 1 input para cada variable que usan los flows
        #   . necesito los inputs requeridos por cada SpecialFunction de cada Fp/Fm
        # Nota : es necesario quitar de esta lista a los que corresponden a 'stock'
        # Nota : filtro los inputs correspondientes a funciones especiales (estas quedan ADENTRO del BASIC_)
        input_ports = []
        # Agrego inputs correspondientes a la ecuacion 'pelada' del Fp/Fm
        for devs_fp in devs_fps:
            input_ports_fp = devs_fp.get_input_ports()
            for input_port_fp in input_ports_fp:
                # Chequeo que el input port venga de afuera
                if input_port_fp.get_name() != stock.get_name() and input_port_fp.get_name() not in list( map(lambda x: x.get_name(), special_atomics)):
                    input_ports.append(DEVSPort(input_port_fp.get_name(), parent_coupled, 'in'))
        for devs_fm in devs_fms:
            input_ports_fm = devs_fm.get_input_ports()
            for input_port_fm in input_ports_fm:
                # Chequeo que el input port venga de afuera
                if input_port_fm.get_name() != stock.get_name() and input_port_fm.get_name() not in list(map(lambda x: x.get_name(), special_atomics)):
                    input_ports.append(DEVSPort(input_port_fm.get_name(), parent_coupled, 'in'))
        # Agrego los inputs correspondientes a funciones especiales (DEVSPulse, DEVSGraphical)
        for special_atomic in special_atomics:
            for variable_name in special_atomic.get_all_inputs():
                input_ports.append(DEVSPort(variable_name, parent_coupled, 'in'))

        # Si un fp y fm reciben el mismo input, solo voy a querer que llegue por un unico puerto
        input_ports = list(set(input_ports))

        ###########
        # Outputs : solamente el valor del stock
        output_ports = [DEVSPort(stock.get_name(), parent_coupled, 'out')]
        for fpm in devs_fpms:
            at = fpm.get_fplus()
            if at is None:
                at = fpm.get_fminus()
            if at is not None:
                op = DEVSPort(at.get_original_name(), parent_coupled, 'out')
                output_ports.append(op)
            else:
                logging.info('ADVERTENCIA: [DEVSBasicCoupledComponent.py]. Se encontro AtomicDEVSFpm = None')
                #print 'ADVERTENCIA: [DEVSBasicCoupledComponent.py] LINEA 230. Se encontro AtomicDEVSFpm = None'
                #raise Exception('Atomic = None')

        ###########
        # External input connections : conexiones que vienen de 'input_ports', y llegan a algun componente
        # (Fp's y Fm's)
        external_input_connections = []
        for atomic_component in atomic_components:
            # TODO : esta lista deberia considerar a todas las funciones que usan inputs de afuera. 
            # Hay que estandarizar esta lista / chequear directamente la clase del atomico
            if atomic_component.get_type() in ['DEVSFplus', 'DEVSFminus', 'DEVSAux', 'DEVSPulse', 'DEVSGraphical', 'DEVSArrayAgregator']:
                for input_port_atomic in atomic_component.get_input_ports():
                    for input_port_basic_coupled in input_ports:
                        if input_port_atomic.get_name() == input_port_basic_coupled.get_name():
                            external_input_connections.append(
                                DEVSExternalInputConnection(input_port_basic_coupled, input_port_atomic,
                                                            input_port_atomic.get_component()))
        external_input_connections = list(set(external_input_connections))

        ###########
        # Output: Integradores
        external_output_connections = []
        for atomic_component in atomic_components:
            if atomic_component.get_type() == 'DEVSIntegrator':
                for output_port in atomic_component.get_output_ports():
                    external_output_connections.append(DEVSExternalOutputConnection(atomic_component, output_port,
                                                                                    DEVSPort(output_port.get_name(),
                                                                                             parent_coupled,
                                                                                             'out')))
        # TODO: Fpm => Output (External Output Connections)
        for fpm in devs_fpms:
            at = fpm.get_fplus()
            if at is None:
                at = fpm.get_fminus()
            if at is not None:
                op = DEVSPort(at.get_original_name(), parent_coupled, 'out')
                external_output_connections.append(DEVSExternalOutputConnection(at, op, op))

        ###########
        # Internal connections
        internal_connections = []
        # ftot => Integrator
        internal_connections.append(DEVSInternalConnection(DEVSPort(ftot.get_name(), ftot, 'out'), ftot,
                                                           DEVSPort('Tot' + stock.get_name(), integrator, 'in'),
                                                           integrator))
        # fp => ftot
        for fp in devs_fps:
            for output_port in fp.get_output_ports_tot():
                updated_port = ftot.add_plus_port(output_port.get_name())
                internal_connections.append(DEVSInternalConnection(output_port, fp, updated_port, ftot))
        # fm => ftot
        for fm in devs_fms:
            for output_port in fm.get_output_ports_tot():
                updated_port = ftot.add_minus_port(output_port.get_name())
                internal_connections.append(DEVSInternalConnection(output_port, fm, updated_port, ftot))

        # 1. Integrator <=> Fp's/Fm's
        # 2. {Special}Functions <=> Fp's/Fm's (las SpecialFunction's las dejo adentro del BASIC)
        # TODO: hacer un ejemplo para DEVSReset
        # - Fp's
        for fp in devs_fps:
            input_ports_fp = fp.get_input_ports()
            for input_port in input_ports_fp:
                # Integrator => Fp's
                if integrator.get_name() == input_port.get_name():
                    output_port = integrator.get_output_ports()[0]
                    internal_connections.append(
                        DEVSInternalConnection(output_port, integrator, input_port, input_port.get_component()))
                # DEVSReset => Fp's (integrator)
                for special_func_obj in special_atomics: 
                    if special_func_obj.get_type() in ['DEVSReset']: 
                        internal_connections.append(
                            DEVSInternalConnection(DEVSPort(special_func_obj.get_name(), special_func_obj, 'out'),
                                                   special_func_obj, DEVSPort('increment', integrator, 'in'),
                                                   integrator))
                    # DEVSGraphical, DEVSPulse => Fp's
                    if special_func_obj.get_type() in ['DEVSAux', 'DEVSPulse', 'DEVSGraphical', 'DEVSArrayAgregator']:
                        if input_port.get_name() == special_func_obj.get_output_ports()[0].get_name():
                            internal_connections.append(
                                DEVSInternalConnection(DEVSPort(special_func_obj.get_name(), special_func_obj, 'out'), 
                                    special_func_obj, DEVSPort(special_func_obj.get_name(), fp, 'in'), fp))

        # - Fm's
        for fm in devs_fms:
            input_ports_fm = fm.get_input_ports()
            for input_port in input_ports_fm:
                # Integrator => Fm's
                if integrator.get_name() == input_port.get_name():
                    output_port = integrator.get_output_ports()[0]
                    internal_connections.append(
                        DEVSInternalConnection(output_port, integrator, input_port, input_port.get_component()))
                # DEVSReset => Fm's (integrator)
                for special_func_obj in special_atomics:
                    if special_func_obj.get_type() in ['DEVSReset']:
                        internal_connections.append(
                            DEVSInternalConnection(DEVSPort(special_func_obj.get_name(), special_func_obj, 'out'),
                                                   special_func_obj, DEVSPort('subtract', integrator, 'in'),
                                                   integrator))
                    # DEVSGraphical, DEVSPulse => Fms's
                    if special_func_obj.get_type() in ['DEVSAux', 'DEVSPulse', 'DEVSGraphical', 'DEVSArrayAgregator']:
                        if input_port.get_name() == special_func_obj.get_output_ports()[0].get_name():
                            internal_connections.append(
                                DEVSInternalConnection(DEVSPort(special_func_obj.get_name(), special_func_obj, 'out'), 
                                    special_func_obj, DEVSPort(special_func_obj.get_name(), fm, 'in'), fm))

        internal_connections = list(set(internal_connections))

        # Append component
        self.set_parent(parent_coupled.name)
        self.set_name(name)
        self.set_atomic_components(atomic_components)
        self.set_coupled_components(coupled_components)
        self.set_output_ports(output_ports)
        self.set_input_ports(input_ports)
        self.set_external_input_connections(external_input_connections)
        self.set_external_output_connections(external_output_connections)
        self.set_internal_connections(internal_connections)
