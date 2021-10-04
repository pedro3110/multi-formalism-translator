from py_expression_eval import Parser
from src.modulosAuxiliares.SpecialFunctionFinder import SpecialFunctionFinder


class Equation(object):
    def __init__(self, equation, sim_specs, dimensions=[], destiny_name='', debug=False):
        self.debug = debug
        # TODO : mejorar esto (MATHEMATICAL BUILTINS)
        self.eq_dict = {
            'MIN': 'min', 
            'MAX': 'max', 
            'ABS': 'abs'
        }
        self.equation = None
        self.variables = []
        self.special_functions = []
        self.destiny_name = destiny_name
        self.set_variables_and_equation_and_functions(equation, sim_specs, dimensions)

    def __repr__(self):
        return str({
            'equation': self.equation
        })

    def __str__(self):
        return str({
            'equation': self.equation
        })

    # Setters
    def set_variables_and_equation_and_functions(self, equation, sim_specs, dimensions):

        finder = SpecialFunctionFinder()

        #parser = EquationParser.create_parser(Parsers.XMILE_FUNCTION_PARSER)#EquationParser.create_parser(Parsers.PY_EXPRESSION_EVAL_PARSER) # EquationParser.create_parser(Parsers.XMILE_FUNCTION_PARSER)
        parser = Parser()

        #######################
        # Capturo eqn invalidas (arrays o modulos por ahora)
        if equation is None or ('{' in equation and '}' in equation):
            variables, special_functions, equation = [], [], 'NO FUNCTION'

        #######################
        # Parse Special Functions => lista de objetos funciones que estan en la ecuacion
        else:                
            special_functions, equation = finder.parseEquation(equation, sim_specs, dimensions, self.destiny_name)

            # Parser de funcion clasico: asume que 'equation' es una funcion de *,/,-,+ (clasica)
            # Requiere previo procesamiento de la funcion original
            # Remuevo nombres de funciones (el parser que usamos no los diferencia de variables)
            for orig, rep in self.eq_dict.items():
                equation = equation.replace(orig, rep)
            expression = parser.parse(equation)
            variables = expression.variables()
            for func_name in self.eq_dict.values():
                if func_name in variables:
                    variables.remove(func_name)
            #print('variables:', variables)

        #######################
        # Seteo variables y special_functions
        self.variables = variables
        self.special_functions = special_functions
        self.equation = equation
        return 

    # Getters
    def get_equation(self):
        return self.equation

    def get_variables(self):
        return self.variables

    def get_special_functions(self, parent_name):
        ans = []
        for sf in self.special_functions:
            sf.set_parent(parent_name)
            ans.append(sf)
        return ans

    # TODO
    def get_paramters(self):
        return []