from src.formalismos.modulosDEVS.DEVSAtomic.DEVSPulse import DEVSPulse
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSStep import DEVSStep
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSDelay import DEVSDelay
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSUniform import DEVSUniform
from src.formalismos.modulosDEVS.DEVSAtomic.DEVSArrayAgregator import DEVSArrayAgregator
import re

# TODO : hay que importar los modulos correspondientes a todas las SpecialFunctions


class SpecialFunctionFinder(object):
    def __init__(self):

        # TODO: sacar estas regex a un archivo
        self.regexs = {
            'PULSE': [
                (r"PULSE\([ ]*[\w]+[ ]*\)", r"PULSE\([ ]*([\w]+)[ ]*\)"),
                (r"PULSE\([ ]*[\w]+[ ]*,[ ]*[\w]+[ ]*\)", r"PULSE\([ ]*([\w]+)[ ]*,[ ]*([\w]+)[ ]*\)"),
                (r"PULSE\([ ]*[\w]+[ ]*,[ ]*[\w]+[ ]*,[ ]*[\w]+[ ]*\)", r"PULSE\(([\w]+),([\w]+),([\w]+)\)")
            ],
            'RAMP' : [
               (r"RAMP\([ ]*[\w]+[ ]*\)", r"RAMP\([ ]*([\w]+)[ ]*\)"),
               (r"RAMP\([ ]*[\w]+[ ]*,[ ]*[\w]+[ ]*\)", r"RAMP\([ ]*([\w]+)[ ]*,[ ]*([\w]+)[ ]*\)")
            ],
            'STEP': [
                (r"STEP\([ ]*[\w]+[ ]*\)", r"STEP\([ ]*([\w]+)[ ]*\)"),
                (r"STEP\([ ]*[\w]+[ ]*,[ ]*[\w]+[ ]*\)", r"STEP\([ ]*([\w]+)[ ]*,[ ]*([\w]+)[ ]*\)")
            ],
            'DELAY': [
                (r"DELAY\([ ]*[\w]+[ ]*,[ ]*[\w]+[ ]*\)", r"DELAY\([ ]*([\w]+)[ ]*,[ ]*([\w]+)[ ]*\)"),
                (r"DELAY\([ ]*[\w]+[ ]*,[ ]*[\w]+[ ]*,[ ]*[\w]+[ ]*\)", r"DELAY\(([\w]+),([\w]+),([\w]+)\)")
            ],
            'UNIFORM': [
                (r"UNIFORM\([ ]*[\w]+[ ]*,[ ]*[\w]+[ ]*\)", r"UNIFORM\([ ]*([\w]+)[ ]*,[ ]*([\w]+)[ ]*\)")
            ]
        }
        assert(set(self.regexs.keys()) == set(self.regexs.keys()))

        self.agregation_functions = ['SUM', 'PROD', 'MEAN']

    def getSpecialFunctionsNames(self):
        return self.regexs.keys()

    # TODO: REFACTORIZAR
    #####################################################################
    def parseEquation(self, equation, sim_specs, dimensions, destiny_name):
        special_functions = []
        array_functions = []
        
        equation = equation.replace(" ", "")

        if '[' in equation and ']' in equation:
            # Parseo funcion de agregacion sobre arrays
            array_functions_with_parameters = self.getArrayFunctions(equation)
            for array_function in array_functions_with_parameters:
                obj_func = self.parseArrayFunction(destiny_name, array_function, sim_specs, dimensions)
                array_functions.append(obj_func)
                equation = equation.replace(array_function, obj_func.get_name())

        # Parseo funciones especiales (PULSE, RAMP, STEP)
        special_functions_with_parameters = self.getSpecialFunctionsWithParameters(equation)
        for func_with_params in special_functions_with_parameters:
            obj_func = self.parseSpecialFunctionWithParameters(destiny_name, func_with_params, sim_specs)
            special_functions.append(obj_func)
            equation = equation.replace(func_with_params, obj_func.get_name())
        
        # Devuelvo todas las funciones (especiales + arrayed)
        return special_functions + array_functions, equation
    
    #####################################################################
    # ArrayFunctions
    def getArrayFunctions(self, equation):
        if "*" in equation:
            for ag_f in self.agregation_functions:
                regex = ag_f + "\(" + "[\w]+\[[\*\d+][,\*\d+]*\]" + "\)"
                search_results = re.findall(re.compile(regex), equation)
                if len(search_results) > 0:
                    break
        else:
            regex = r"[\w]+\[[\*\d+][,\*\d+]*\]"
            search_results = re.findall(re.compile(regex), equation)
        return search_results

    def parseArrayFunction(self, destiny_name, array_function, sim_specs, dimensions):

        return DEVSArrayAgregator(destiny_name, dimensions, array_function)

    #####################################################################
    # SpecialFunctionsWithParameters
    def getSpecialFunctionsWithParameters(self, equation):
        ans = []
        for func_name in self.regexs.keys():
            regexs = self.regexs[func_name]
            for regex in regexs:
                search_results = re.findall(re.compile(regex[0]), equation)
                ans = ans + search_results
        return ans
    def parseSpecialFunctionWithParameters(self, destiny_name, func_with_parameters, sim_specs):
        # Chequeo que la funcion este entre las que puedo parsear
        func_name = None
        ok = False
        for name in self.regexs.keys():
            if name in func_with_parameters:
                ok = True
                func_name = name
        assert(ok)
        assert(func_name is not None)
        return self.generateSpecialFunction(destiny_name, func_name, func_with_parameters, sim_specs)

    #####################################################################
    # Funcion auxiliar
    # SpecialFunctionGenerator
    def generateSpecialFunction(self, destiny_name, func_name, func_with_parameters, sim_specs):
        #######################
        # IMPORTANTE : 'destiny_name'. PASAR EL NOMBRE DEL PADRE (EN DONDE ESTA DEFINIDA LA FUNCION, PARA QUE SEA INCLUIDO EN EL NOMBRE)
        
        #######################
        # PULSE(volume, [<first pulse>, <interval>])
        if func_name == 'PULSE':
            devs_pulse = None
            regexs_pulse = self.regexs['PULSE']
            for regex in regexs_pulse:
                func_with_parameters = func_with_parameters.replace(' ', '')
                search_res = re.search(regex[1], func_with_parameters)
                if search_res is not None:
                    parameters = list(search_res.groups())  
                    if len(parameters) < 3:
                        raise Exception('Error : parametros incorrectos en funcion PULSE')
                    volume = parameters[0]
                    if len(parameters) > 1:
                        first_pulse = parameters[1]
                    if len(parameters) > 2:
                        interval = parameters[2]
                        dt = sim_specs['dt']
                        devs_pulse = DEVSPulse(destiny_name, volume, first_pulse, interval, dt)
            assert(devs_pulse is not None)
            return devs_pulse

        #######################
        # STEP(height, time)
        if func_name == 'STEP':
            devs_step = None
            regexs_step = self.regexs['STEP']
            for regex in regexs_step:
                func_with_parameters = func_with_parameters.replace(' ', '')
                search_res = re.search(regex[1], func_with_parameters)
                if search_res is not None:
                    parameters = list(search_res.groups())  
                    if len(parameters) < 2:
                        raise Exception('Error : parametros incorrectos en funcion STEP')
                    height = parameters[0]
                    if len(parameters) > 1:
                        time = parameters[1]
                        devs_step = DEVSStep(destiny_name, height, time)
            assert(devs_step is not None)
            return devs_step

        #######################
        # DELAY(input, delay, [<initial delay>])
        elif func_name == 'DELAY':
            devs_delay = None
            regexs_delay = self.regexs['DELAY']
            for regex in regexs_delay:
                func_with_parameters = func_with_parameters.replace(' ', '')
                search_res = re.search(regex[1], func_with_parameters)
                if search_res is not None:
                    parameters = list(search_res.groups())
                    if len(parameters) < 2:
                        raise Exception('Error: parametros incorrectos en funcion DELAY')
                    input_parameter = parameters[0]
                    delay_parameter = parameters[1]
                    if len(parameters) > 2:
                        initial_delay = parameters[2]
                    else:
                        initial_delay = None
                    devs_delay = DEVSDelay(destiny_name, input_parameter, delay_parameter, initial_delay)
            assert(devs_delay is not None)
            return devs_delay

        #######################
        # UNIFORM(min_val, max_val)
        elif func_name == 'UNIFORM':
            devs_uniform = None
            regexs_uniform = self.regexs['UNIFORM']
            for regex in regexs_uniform:
                func_with_parameters = func_with_parameters.replace(' ', '')
                search_res = re.search(regex[1], func_with_parameters)
                if search_res is not None:
                    parameters = list(search_res.groups())
                    if len(parameters) < 2:
                        raise Exception('Error: parametros incorrectos en funcion UNIFORM')
                    min_val = parameters[0]
                    max_val = parameters[1]
                    dt = sim_specs['dt']
                    devs_uniform = DEVSUniform(destiny_name, min_val, max_val, dt)
            assert(devs_uniform is not None)
            return devs_uniform

        ########################
        # ERROR
        else:
            raise Exception('Error : la funcion ' + func_name + ' no puede ser generada')